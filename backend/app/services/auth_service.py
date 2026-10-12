"""Accounts: creating one (US01) and signing in (US02), with BR1, BR2, BR3 and BR10.

Nothing here knows about HTTP. Each failure is an error from app/services/errors.py, and
app/core/errors.py gives it its status.
"""

import re
from functools import cache

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.models import User
from app.db.repositories import user_repo
from app.services.errors import AlreadyExists, NotSignedIn, NotUnderstood, RuleBroken

INCORRECT_SIGN_IN = "Incorrect email or password"
SIGN_IN_AGAIN = "Please sign in again"
EMAIL_TAKEN = "This email is already registered"
PASSWORD_LENGTH = "Password must be 6 to 128 characters"
INVALID_EMAIL = "Enter a valid email address"

PASSWORD_MIN, PASSWORD_MAX = 6, 128

# Something before the @, something after it, and a dot in the part after it. Deliberately loose:
# the app sends no email, so an address only has to look like one a person typed on purpose.
EMAIL_SHAPE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class IncorrectSignIn(NotSignedIn):
    """BR3: the one failure a sign-in has, whether the address or the password was wrong."""

    code = "incorrect_sign_in"


class SessionOver(NotSignedIn):
    """BR10: no token, a forged one, or one older than 7 days."""

    code = "sign_in_again"


@cache
def _decoy_hash() -> str:
    """A hash to check against when the address has no account, so both failures take as long."""
    return hash_password("no account has this password")


def register(db: Session, *, email: str, password: str) -> User:
    """Create an account and return it (US01).

    Checked in this order: the address looks like one (400), the password is 6 to 128
    characters (BR2, 422), and no account has the address yet, whatever its capitals (BR1, 409).
    Only a hash of the password is stored (BR2).
    """
    if not EMAIL_SHAPE.match(email.strip()):
        raise NotUnderstood(INVALID_EMAIL, code="invalid_email")
    if not PASSWORD_MIN <= len(password) <= PASSWORD_MAX:
        raise RuleBroken(PASSWORD_LENGTH, code="password_length")
    if user_repo.get_by_email(db, email) is not None:
        raise AlreadyExists(EMAIL_TAKEN, code="email_taken")
    return user_repo.create(db, email=email, password_hash=hash_password(password))


def authenticate(db: Session, *, email: str, password: str) -> User:
    """The account these details belong to; IncorrectSignIn if there is none.

    BR3: an unknown address and a wrong password get the same status and the same sentence, and
    take the same time, so nobody can find out which addresses have an account.
    """
    user = user_repo.get_by_email(db, email)
    stored_hash = user.password_hash if user else _decoy_hash()
    if not verify_password(password, stored_hash) or user is None:
        raise IncorrectSignIn(INCORRECT_SIGN_IN)
    return user


def signed_in_account(db: Session, user_id: int) -> User | None:
    """The account a valid token names, or None if it has been deleted since (BR10)."""
    return user_repo.get_by_id(db, user_id)
