"""
Password-reset token issuance and verification.

Tokens are itsdangerous URLSafeTimedSerializer payloads signed with the
app's SECRET_KEY under a dedicated salt (so a leaked reset token can't be
replayed against any other signed-cookie use in the app). The payload
carries the user id plus a snapshot of `password_reset_at` at issue time,
which gives us single-use enforcement for free: redeeming a token after
it's already been used (or after a newer reset happened) fails, because
the user's *current* `password_reset_at` no longer matches what's
embedded in the token.
"""
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from models import User

RESET_SALT = "password-reset"
RESET_MAX_AGE_SECONDS = 30 * 60  # 30 minutes


def _serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key, salt=RESET_SALT)


def _reset_marker(user: User) -> str:
    return user.password_reset_at.isoformat() if user.password_reset_at else "never"


def issue_reset_token(secret_key: str, user: User) -> str:
    """Mint a reset token for `user`, tagged with their current reset marker."""
    return _serializer(secret_key).dumps({"uid": user.id, "prat": _reset_marker(user)})


def verify_reset_token(secret_key: str, token: str, max_age: int = RESET_MAX_AGE_SECONDS):
    """Return the User a still-valid token was issued for, else None.

    None covers a malformed/tampered token, an expired one (older than
    `max_age`), a token whose user no longer exists, or a token that's
    already been redeemed (or superseded by a newer reset) — all
    indistinguishable to the caller by design.
    """
    try:
        data = _serializer(secret_key).loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None

    user = User.query.get(data.get("uid"))
    if user is None or data.get("prat") != _reset_marker(user):
        return None
    return user
