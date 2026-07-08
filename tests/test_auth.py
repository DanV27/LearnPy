"""
Tests for the reworked auth flow: signup validation, username-or-email
login, and the forgot-password token lifecycle.

Uses the shared `test_app` / `app_ctx` fixtures from conftest.py (in-memory
SQLite, LOGIN_DISABLED). Each test gets a clean `user` table via the
autouse `_clean_users` fixture below.
"""
import pytest

from models import db, User, Generation
from reset_tokens import issue_reset_token, verify_reset_token


@pytest.fixture(autouse=True)
def _clean_users(app_ctx):
    """Wipe user/generation before and after each test — the underlying
    DB is shared (session-scoped) across the whole test session."""
    db.session.query(Generation).delete()
    db.session.query(User).delete()
    db.session.commit()
    yield
    db.session.query(Generation).delete()
    db.session.query(User).delete()
    db.session.commit()


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


def make_user(username="alice", email="alice@example.com", password="correct-horse-battery"):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


# ---------------------------------------------------------------------------
# Signup validation
# ---------------------------------------------------------------------------

def test_signup_rejects_mismatched_passwords(client):
    resp = client.post("/signup", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "longenoughpassword",
        "confirm_password": "different-password",
    })
    assert resp.status_code == 400
    assert "match" in resp.get_json()["error"].lower()
    assert User.query.filter_by(username="bob").first() is None


def test_signup_rejects_short_password(client):
    resp = client.post("/signup", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "short1",
        "confirm_password": "short1",
    })
    assert resp.status_code == 400
    assert "8 characters" in resp.get_json()["error"]


def test_signup_rejects_duplicate_email(client):
    make_user(username="alice", email="dup@example.com")
    resp = client.post("/signup", json={
        "username": "someoneelse",
        "email": "dup@example.com",
        "password": "longenoughpassword",
        "confirm_password": "longenoughpassword",
    })
    assert resp.status_code == 400
    assert "email" in resp.get_json()["error"].lower()


def test_signup_success_creates_user(client):
    resp = client.post("/signup", json={
        "username": "carol",
        "email": "  Carol@Example.com  ",
        "password": "longenoughpassword",
        "confirm_password": "longenoughpassword",
    })
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    user = User.query.filter_by(username="carol").first()
    assert user is not None
    # stored normalized: lowercase + stripped
    assert user.email == "carol@example.com"


# ---------------------------------------------------------------------------
# Login by username or email
# ---------------------------------------------------------------------------

def test_login_by_username(client):
    make_user(username="dave", email="dave@example.com", password="hunter2hunter2")
    resp = client.post("/login", json={"identifier": "dave", "password": "hunter2hunter2"})
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True


def test_login_by_email(client):
    make_user(username="dave", email="dave@example.com", password="hunter2hunter2")
    resp = client.post("/login", json={"identifier": "DAVE@example.com", "password": "hunter2hunter2"})
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True


def test_login_rejects_wrong_password(client):
    make_user(username="dave", email="dave@example.com", password="hunter2hunter2")
    resp = client.post("/login", json={"identifier": "dave", "password": "wrong-password"})
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Reset token round-trip / expiry / single-use (unit-level, no HTTP)
# ---------------------------------------------------------------------------

SECRET = "test-secret"


def test_reset_token_roundtrip():
    user = make_user()
    token = issue_reset_token(SECRET, user)
    redeemed = verify_reset_token(SECRET, token)
    assert redeemed is not None
    assert redeemed.id == user.id


def test_reset_token_expired_is_rejected():
    user = make_user()
    token = issue_reset_token(SECRET, user)
    # itsdangerous timestamps have 1-second resolution, so max_age=0 can
    # race within the same second. max_age=-1 makes "age > max_age" true
    # unconditionally (age is always >= 0), deterministically expiring it.
    assert verify_reset_token(SECRET, token, max_age=-1) is None


def test_reset_token_reused_after_password_change_is_rejected():
    user = make_user()
    token = issue_reset_token(SECRET, user)

    # Simulate redeeming the token: sets a new password and bumps the marker.
    user.set_password("brand-new-password")
    from datetime import datetime
    user.password_reset_at = datetime.utcnow()
    db.session.commit()

    # The same token must not work a second time.
    assert verify_reset_token(SECRET, token) is None


def test_reset_token_wrong_secret_is_rejected():
    user = make_user()
    token = issue_reset_token(SECRET, user)
    assert verify_reset_token("a-different-secret", token) is None


# ---------------------------------------------------------------------------
# /api/forgot-password — no user enumeration
# ---------------------------------------------------------------------------

def test_forgot_password_same_response_for_existing_and_nonexistent_email(client):
    make_user(username="erin", email="erin@example.com")

    existing_resp = client.post("/api/forgot-password", json={"email": "erin@example.com"})
    nonexistent_resp = client.post("/api/forgot-password", json={"email": "nobody@example.com"})

    assert existing_resp.status_code == nonexistent_resp.status_code == 200
    assert existing_resp.get_json() == nonexistent_resp.get_json()


def test_forgot_password_missing_email_still_returns_generic_200(client):
    resp = client.post("/api/forgot-password", json={})
    assert resp.status_code == 200
    assert "reset link" in resp.get_json()["message"].lower()


# ---------------------------------------------------------------------------
# /api/reset-password — full HTTP-level redemption
# ---------------------------------------------------------------------------

def test_reset_password_endpoint_updates_password_and_invalidates_token(client, test_app):
    user = make_user(username="frank", email="frank@example.com", password="old-password-123")
    token = issue_reset_token(test_app.config["SECRET_KEY"], user)

    resp = client.post("/api/reset-password", json={
        "token": token,
        "password": "new-password-456",
        "confirm_password": "new-password-456",
    })
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    refreshed = User.query.get(user.id)
    assert refreshed.check_password("new-password-456")
    assert not refreshed.check_password("old-password-123")

    # Token is single-use: redeeming it again must fail now.
    replay = client.post("/api/reset-password", json={
        "token": token,
        "password": "yet-another-789",
        "confirm_password": "yet-another-789",
    })
    assert replay.status_code == 400


def test_reset_password_endpoint_rejects_invalid_token(client):
    resp = client.post("/api/reset-password", json={
        "token": "not-a-real-token",
        "password": "new-password-456",
        "confirm_password": "new-password-456",
    })
    assert resp.status_code == 400


def test_reset_password_endpoint_rejects_mismatched_passwords(client, test_app):
    user = make_user(username="grace", email="grace@example.com")
    token = issue_reset_token(test_app.config["SECRET_KEY"], user)

    resp = client.post("/api/reset-password", json={
        "token": token,
        "password": "new-password-456",
        "confirm_password": "totally-different",
    })
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Forgot/reset pages are reachable without login
# ---------------------------------------------------------------------------

def test_forgot_password_page_accessible_without_login(client):
    resp = client.get("/forgot-password")
    assert resp.status_code == 200


def test_reset_password_page_with_invalid_token_shows_expired_state(client):
    resp = client.get("/reset-password?token=garbage")
    assert resp.status_code == 200
    assert b"expired" in resp.data.lower() or b"invalid" in resp.data.lower()


def test_reset_password_page_with_valid_token_shows_form(client, test_app):
    user = make_user(username="henry", email="henry@example.com")
    token = issue_reset_token(test_app.config["SECRET_KEY"], user)
    resp = client.get(f"/reset-password?token={token}")
    assert resp.status_code == 200
    assert b"reset-form" in resp.data
