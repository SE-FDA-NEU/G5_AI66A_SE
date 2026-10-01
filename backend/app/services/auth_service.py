"""Signing in: BR2 and BR3. Nothing here knows about HTTP; the router turns a failure into 401."""

from functools import cache

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.models import User
from app.db.repositories import user_repo

INCORRECT_SIGN_IN = "Incorrect email or password"


class IncorrectSignIn(Exception):
    """BR3: the one failure a sign-in has, whether the address or the password was wrong."""


@cache
def _decoy_hash() -> str:
    """A hash to check against when the address has no account, so both failures take as long."""
    return hash_password("no account has this password")


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
