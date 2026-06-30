"""
Tests for profile_data.calculate_heatmap() and its streak helpers.

Four scenarios:
  1. Zero completions (empty state)
  2. Streak that crosses a month boundary
  3. Streak that breaks mid-month
  4. "Today" cell when today has no completion yet
"""
from datetime import date, datetime as real_dt
from unittest.mock import patch

import pytest

from profile_data import calculate_heatmap


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def real_cells(result):
    """Pull only the non-placeholder cells out of a heatmap result."""
    return [c for week in result["weeks"] for c in week if "date" in c]


def run_heatmap(user_id, year, month, today, make_progress=None, done_dates=None):
    """Seed the DB (optional), pin 'today', and run calculate_heatmap."""
    if make_progress and done_dates:
        make_progress(user_id, done_dates)
    with patch("profile_data.datetime") as mock_dt:
        mock_dt.utcnow.return_value.date.return_value = today
        # Forward datetime(...) constructor calls to the real class so that
        # start_dt / end_dt inside calculate_heatmap are real datetime objects.
        mock_dt.side_effect = real_dt
        return calculate_heatmap(user_id=user_id, year=year, month=month)


# ---------------------------------------------------------------------------
# 1. Zero completions — empty state
# ---------------------------------------------------------------------------

class TestZeroCompletions:
    TODAY = date(2026, 6, 15)

    def test_stats_are_all_zero(self, make_progress):
        result = run_heatmap(1, 2026, 6, self.TODAY)
        stats = result["stats"]
        assert stats["total_completions"] == 0
        assert stats["active_days"] == 0
        assert stats["current_streak"] == 0
        assert stats["longest_streak"] == 0

    def test_all_day_cells_are_not_done(self, make_progress):
        result = run_heatmap(1, 2026, 6, self.TODAY)
        for cell in real_cells(result):
            assert not cell["done"]
            assert cell["count"] == 0

    def test_grid_covers_full_month(self, make_progress):
        """All 30 days of June must appear as real (non-placeholder) cells."""
        result = run_heatmap(1, 2026, 6, self.TODAY)
        dates = [c["date"] for c in real_cells(result)]
        assert len(dates) == 30
        assert dates[0] == date(2026, 6, 1)
        assert dates[-1] == date(2026, 6, 30)

    def test_grid_rows_are_all_length_7(self, make_progress):
        result = run_heatmap(1, 2026, 6, self.TODAY)
        for row in result["weeks"]:
            assert len(row) == 7


# ---------------------------------------------------------------------------
# 2. Streak that crosses a month boundary
# ---------------------------------------------------------------------------

class TestMonthBoundaryStreak:
    """
    _current_streak walks backwards from today and stops when it steps out
    of the month's by_date dict.  Even if the user also completed lessons
    every day in the *previous* month, the streak count must stop at day 1
    of the viewed month because those earlier dates aren't in the cell map.
    """

    def test_streak_stops_at_day_1(self, make_progress):
        """User did every day 1-15 in June.  Streak must be 15, not 15 + May days."""
        today = date(2026, 6, 15)
        done_dates = {date(2026, 6, d): 1 for d in range(1, 16)}
        result = run_heatmap(1, 2026, 6, today, make_progress, done_dates)
        assert result["stats"]["current_streak"] == 15

    def test_first_day_of_month_is_the_boundary(self, make_progress):
        """Day 1 is done and today == day 1.  Streak should be 1, not bleed into May."""
        today = date(2026, 6, 1)
        result = run_heatmap(1, 2026, 6, today, make_progress, {today: 1})
        assert result["stats"]["current_streak"] == 1


# ---------------------------------------------------------------------------
# 3. Streak that breaks
# ---------------------------------------------------------------------------

class TestBrokenStreak:
    """Days 1-5 done, day 6 skipped, days 7-10 done.  Viewing on day 10."""

    def _done_dates(self):
        return {date(2026, 6, d): 1 for d in list(range(1, 6)) + list(range(7, 11))}

    def test_current_streak_resets_at_gap(self, make_progress):
        today = date(2026, 6, 10)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        assert result["stats"]["current_streak"] == 4  # days 7-10 only

    def test_longest_streak_spans_the_pre_gap_run(self, make_progress):
        today = date(2026, 6, 10)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        assert result["stats"]["longest_streak"] == 5  # days 1-5

    def test_active_days_counts_both_runs(self, make_progress):
        today = date(2026, 6, 10)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        assert result["stats"]["active_days"] == 9  # 5 + 4

    def test_current_streak_zero_when_today_is_the_gap(self, make_progress):
        """If the gap *is* today, current_streak must be 0."""
        today = date(2026, 6, 6)  # the skipped day
        done_dates = {date(2026, 6, d): 1 for d in range(1, 6)}
        result = run_heatmap(1, 2026, 6, today, make_progress, done_dates)
        assert result["stats"]["current_streak"] == 0


# ---------------------------------------------------------------------------
# 4. "Today" cell when today has no completion yet
# ---------------------------------------------------------------------------

class TestTodayCellNoCompletion:
    """Days 1-14 done; today (day 15) has no completion yet."""

    def _done_dates(self):
        return {date(2026, 6, d): 1 for d in range(1, 15)}

    def test_today_cell_is_not_done(self, make_progress):
        today = date(2026, 6, 15)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        cells_by_date = {c["date"]: c for c in real_cells(result)}
        assert not cells_by_date[today]["done"]
        assert cells_by_date[today]["count"] == 0

    def test_current_streak_breaks_on_empty_today(self, make_progress):
        today = date(2026, 6, 15)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        assert result["stats"]["current_streak"] == 0

    def test_longest_streak_unaffected_by_empty_today(self, make_progress):
        today = date(2026, 6, 15)
        result = run_heatmap(1, 2026, 6, today, make_progress, self._done_dates())
        assert result["stats"]["longest_streak"] == 14

    def test_current_streak_is_zero_for_past_months(self, make_progress):
        """current_streak is always 0 when viewing a month other than today's."""
        today = date(2026, 6, 15)
        done_dates = {date(2026, 5, d): 1 for d in range(1, 32)
                      if date(2026, 5, 1) <= date(2026, 5, d) <= date(2026, 5, 31)}
        result = run_heatmap(1, 2026, 5, today, make_progress, done_dates)
        assert result["stats"]["current_streak"] == 0
