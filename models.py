"""
SQLAlchemy models for LearnPy.

Two tables:

  - `user`       — accounts, with hashed passwords (pbkdf2:sha256).
  - `generation` — every lesson generated via the free-form search bar,
                   so we can build a per-user history view later.

Hand-authored canonical lessons (the sidebar topics) live as Markdown files
in `lessons/` and aren't backed by the database at all.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A LearnPy account.

    Inherits `UserMixin` from Flask-Login, which gives us the boilerplate
    `is_authenticated`, `get_id()`, etc. methods for free.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Stores the hashed password (NOT the plaintext). Length is generous
    # to fit any algorithm werkzeug might use in the future.
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many: a user has many generations.
    generations = db.relationship("Generation", backref="user", lazy=True)

    def set_password(self, raw_password: str) -> None:
        """Hash and store a plaintext password.

        Uses pbkdf2:sha256 explicitly — werkzeug's default `scrypt` requires
        Python to be linked against an OpenSSL build that ships scrypt, which
        isn't the case on some Python 3.9 installs (it raises
        `module 'hashlib' has no attribute 'scrypt'`).
        """
        self.password = generate_password_hash(raw_password, method="pbkdf2:sha256")

    def check_password(self, raw_password: str) -> bool:
        """Constant-time check of a plaintext password against the stored hash."""
        if not self.password:
            return False
        return check_password_hash(self.password, raw_password)


class Generation(db.Model):
    """One AI-generated lesson, tied to the user who requested it.

    Populated by the `/generate` endpoint. Canonical sidebar lessons are
    NOT stored here — those are static files in `lessons/`.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    spec = db.Column(db.String(500), nullable=False)         # the raw search prompt
    title = db.Column(db.String(200))                         # lesson title Claude returned
    lesson_markdown = db.Column(db.Text)                      # full markdown body
    code = db.Column(db.Text)                                 # primary code snippet
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize for JSON responses — useful if/when we add a history view."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "spec": self.spec,
            "title": self.title,
            "lesson_markdown": self.lesson_markdown,
            "code": self.code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class LessonProgress(db.Model):
    """Tracks each user's progress on each canonical lesson.

    One row per (user, slug) pair. `viewed_at` is set the first time the
    user lands on the lesson page; `completed_at` is set the first time
    the user passes every test in that lesson's challenge.

    Used to render the eyeball + green check icons on topic cards and to
    pre-light the CHALLENGE COMPLETE badge on lesson pages the user has
    already beaten.
    """

    __tablename__ = "lesson_progress"
    __table_args__ = (
        db.UniqueConstraint("user_id", "slug", name="uq_lesson_progress_user_slug"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    slug = db.Column(db.String(80), nullable=False, index=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
