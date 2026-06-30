"""
Test infrastructure for profile_data tests.

Strategy
--------
calculate_heatmap() queries LessonProgress via Flask-SQLAlchemy, which
needs a live app context.  We create a minimal Flask app backed by an
in-memory SQLite database, run migrations (just CREATE TABLE), and expose
an `app_ctx` fixture that wraps each test in the shared app context and
wipes the LessonProgress table before each test runs.

make_progress() inserts fake LessonProgress rows directly so tests can
control exactly which dates have completions.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(scope="session")
def test_app():
    """Flask app with a fresh in-memory SQLite DB, shared across the session."""
    from flask_app import app as flask_app
    from models import db

    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SECRET_KEY="test-secret",
        ANTHROPIC_API_KEY="dummy",
        LOGIN_DISABLED=True,
    )

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture(autouse=True)
def app_ctx(test_app):
    """Push the shared app context and wipe LessonProgress before every test."""
    from models import LessonProgress, db

    with test_app.app_context():
        db.session.query(LessonProgress).delete()
        db.session.commit()
        yield


@pytest.fixture()
def make_progress():
    """
    Factory fixture — call it inside a test to seed the DB::

        make_progress(user_id, {date: n_completions, ...})
    """
    from datetime import datetime as real_dt

    from models import LessonProgress, db

    def _factory(user_id: int, dates_with_counts: dict):
        for d, n in dates_with_counts.items():
            for i in range(n):
                db.session.add(LessonProgress(
                    user_id=user_id,
                    slug=f"test-{d.isoformat()}-{i}",
                    completed_at=real_dt(d.year, d.month, d.day, 12, 0, 0),
                ))
        db.session.commit()

    return _factory
