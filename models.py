from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generations = db.relationship('Generation', backref='user', lazy=True)

    def set_password(self, raw_password: str) -> None:
        """Hash and store the password.

        Uses pbkdf2:sha256 explicitly — werkzeug's default `scrypt` requires
        Python to be linked against an OpenSSL build that ships scrypt, which
        isn't the case on some Python 3.9 installs (raises
        `module 'hashlib' has no attribute 'scrypt'`).
        """
        self.password = generate_password_hash(raw_password, method="pbkdf2:sha256")

    def check_password(self, raw_password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        if not self.password:
            return False
        return check_password_hash(self.password, raw_password)


class Generation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spec = db.Column(db.String(500), nullable=False)
    code = db.Column(db.Text, nullable=False)
    test_code = db.Column(db.Text)
    passed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serialize for JSON responses (e.g. /history)."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "spec": self.spec,
            "code": self.code,
            "test_code": self.test_code,
            "passed": self.passed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
