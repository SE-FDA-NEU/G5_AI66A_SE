"""Password hashing (BR2) and sign-in tokens (BR10)."""

import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import settings

HASH_SCHEME = "pbkdf2_sha256"
TOKEN_ALGORITHM = "HS256"


def _encode(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def hash_password(password: str) -> str:
    """Return 'pbkdf2_sha256$<rounds>$<salt>$<hash>'. The password itself is never stored (BR2).

    PBKDF2 comes with Python, so nothing is compiled on install, and unlike bcrypt it uses every
    character of a 128-character password (ADR 3 in docs/design.md).
    """
    rounds = settings.PASSWORD_HASH_ITERATIONS
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, rounds)
    return f"{HASH_SCHEME}${rounds}${_encode(salt)}${_encode(digest)}"


def verify_password(password: str, stored_hash: str) -> bool:
    """True when `password` produces `stored_hash`. Compares in constant time."""
    try:
        scheme, rounds, salt, digest = stored_hash.split("$")
        expected = base64.b64decode(digest)
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), base64.b64decode(salt), int(rounds)
        )
    except ValueError:
        return False
    return scheme == HASH_SCHEME and hmac.compare_digest(candidate, expected)


def create_access_token(user_id: int, *, now: datetime | None = None) -> tuple[str, datetime]:
    """A signed token naming the account, and the moment it expires.

    BR10: a sign-in lasts SESSION_DAYS (7) from the moment it happens. The expiry travels inside
    the token, so the server keeps no session table.
    """
    issued_at = now or datetime.now(UTC)
    expires_at = issued_at + timedelta(days=settings.SESSION_DAYS)
    claims = {"sub": str(user_id), "iat": issued_at, "exp": expires_at}
    return jwt.encode(claims, settings.SECRET_KEY, algorithm=TOKEN_ALGORITHM), expires_at


def read_access_token(token: str) -> int | None:
    """The account id inside a valid token; None if it is forged, damaged or has expired."""
    try:
        claims = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[TOKEN_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        return int(claims["sub"])
    except (jwt.PyJWTError, ValueError):
        return None
