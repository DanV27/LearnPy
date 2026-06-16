'''
profile data helpers - compute the heatmap and stats for a user

Only data. The route in flask_app calls calculate_heatmap() and hands the
result to the template.
'''


import calendar
from collections import Counter
from datetime import date, datetime, timedelta

from models import LessonProgress


# which weekday starts each row of the heatmap grid. Sun = 6 (Python's
# date.weekday() is Mon=0..Sun=6). Change to 0 for Monday-first weeks.
week_start = 6


def calculate_heatmap(user_id: int, year: int = None, month: int = None):
    """Build a one-month heatmap of challenge completions for a user.

    Every day in the requested calendar month becomes a cell. A cell is
    "done" if the user passed at least one challenge that day; otherwise
    it's empty. Cells before the 1st and after the last day of the month
    are returned as `placeholder` cells so the grid stays a clean
    rectangle of 7-column rows.

    Defaults to the current UTC year/month if `year` / `month` aren't given.

    Returns:
        {
            "year": int,
            "month": int,                  # 1-12
            "label": "June 2026",
            "weeks": [[cell, cell, ...]],  # length-7 rows, Sun..Sat
            "stats": {
                "total_completions": int,
                "active_days": int,
                "current_streak": int,     # 0 unless viewing the current month
                "longest_streak": int,
            },
        }

    Where each cell is one of:
        {"placeholder": True}                          # blank slot
        {"date": date, "count": int, "done": bool}     # real day
    """

    # 1. Resolve the requested month, defaulting to today's UTC month.
    today = datetime.utcnow().date()
    if year is None or month is None:
        year, month = today.year, today.month

    # 2. Boundaries of the requested month.
    first_day = date(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]  # days in this month
    last_day = date(year, month, last_day_num)

    # Half-open [start, end) range used to filter completed_at.
    start_dt = datetime(year, month, 1)
    end_dt = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    # 3. Pull the user's completions inside the month.
    rows = (
        LessonProgress.query
        .filter(LessonProgress.user_id == user_id)
        .filter(LessonProgress.completed_at.isnot(None))
        .filter(LessonProgress.completed_at >= start_dt)
        .filter(LessonProgress.completed_at < end_dt)
        .all()
    )

    # 4. Bucket completions by calendar date.
    counts = Counter(r.completed_at.date() for r in rows)

    # 5. Leading / trailing placeholder counts so the grid stays rectangular.
    #    leading  = blanks before day 1 (so the 1st lands in the right column)
    #    trailing = blanks after the last day (so the final row has 7 cells)
    leading = (first_day.weekday() - week_start) % 7
    trailing = (week_start - 1 - last_day.weekday()) % 7

    # 6. Build the flat cell list.
    cells = [{"placeholder": True} for _ in range(leading)]
    for day_num in range(1, last_day_num + 1):
        d = date(year, month, day_num)
        count = counts.get(d, 0)
        cells.append({"date": d, "count": count, "done": count > 0})
    cells.extend({"placeholder": True} for _ in range(trailing))

    # 7. Slice into rows of 7.
    weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)]

    # 8. Stats - walk only the real-day cells (skip placeholders).
    day_cells = [c for c in cells if "date" in c]
    total_completions = sum(c["count"] for c in day_cells)
    active_days = sum(1 for c in day_cells if c["done"])
    longest_streak = _longest_streak(day_cells)
    current_streak = (
        _current_streak(day_cells, today)
        if (year, month) == (today.year, today.month)
        else 0
    )

    return {
        "year": year,
        "month": month,
        "label": first_day.strftime("%B %Y"),
        "weeks": weeks,
        "stats": {
            "total_completions": total_completions,
            "active_days": active_days,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        },
    }


def _longest_streak(day_cells: list) -> int:
    """Longest run of consecutive `done` days anywhere in the month."""
    longest = run = 0
    for c in day_cells:
        if c["done"]:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return longest


def _current_streak(day_cells: list, today: date) -> int:
    """Number of consecutive `done` days ending today (within this month).

    Walks backwards from `today` one day at a time. Stops at the first
    `not done` day, or when we step out of the month being viewed.
    """
    by_date = {c["date"]: c for c in day_cells}
    streak = 0
    d = today
    while d in by_date and by_date[d]["done"]:
        streak += 1
        d -= timedelta(days=1)
    return streak
