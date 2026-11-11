"""The profile and the account itself: reading and changing the profile (US16, BR15), and
deleting the account with everything it owns (US18, BR16).

Nothing here knows about HTTP; each refusal is an error from app/services/errors.py.
"""

import base64
import binascii
import re

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.models import User
from app.db.repositories import user_repo
from app.services.errors import RuleBroken

FULL_NAME_MAX = 80
NICKNAME_MAX = 40
PHONE_DIGITS_MIN, PHONE_DIGITS_MAX = 8, 15
# With the spaces and dashes between the digits; the column holds 30 characters.
PHONE_MAX = 30
AVATAR_MAX_BYTES = 200_000

NAME_TOO_LONG = f"Write a full name of at most {FULL_NAME_MAX} characters"
NICKNAME_TOO_LONG = f"Write a name of at most {NICKNAME_MAX} characters"
INVALID_PHONE = f"Enter a phone number of {PHONE_DIGITS_MIN} to {PHONE_DIGITS_MAX} digits"
INVALID_AVATAR = "Choose a PNG, JPEG or WebP picture of 200 KB or less"
CONFIRMATION_MISMATCH = "The email or password does not match this account"

# Digits, with the spaces, dots, dashes and brackets people type between them, and one + first.
PHONE_SHAPE = re.compile(r"^\+?[0-9 .()\-]+$")
AVATAR_SHAPE = re.compile(r"^data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)$")


def _text(value: str | None) -> str | None:
    """Spaces around are dropped, and an empty field means "not given"."""
    if value is None:
        return None
    value = value.strip()
    return value or None


def _phone(value: str | None) -> str | None:
    value = _text(value)
    if value is None:
        return None
    digits = sum(ch.isdigit() for ch in value)
    shaped = PHONE_SHAPE.match(value) and len(value) <= PHONE_MAX
    if not shaped or not PHONE_DIGITS_MIN <= digits <= PHONE_DIGITS_MAX:
        raise RuleBroken(INVALID_PHONE, code="invalid_phone")
    return value


def _avatar(value: str | None) -> str | None:
    if not value:
        return None
    match = AVATAR_SHAPE.match(value)
    if match is None:
        raise RuleBroken(INVALID_AVATAR, code="invalid_avatar")
    try:
        size = len(base64.b64decode(match.group(2), validate=True))
    except (binascii.Error, ValueError):
        raise RuleBroken(INVALID_AVATAR, code="invalid_avatar") from None
    if size > AVATAR_MAX_BYTES:
        raise RuleBroken(INVALID_AVATAR, code="invalid_avatar")
    return value


def update_profile(db: Session, user: User, changes: dict[str, str | None]) -> User:
    """Change only the fields sent (BR15); a field sent empty is cleared.

    The email is not one of them: the schema refuses a request that names it.
    """
    if "full_name" in changes:
        full_name = _text(changes["full_name"])
        if full_name is not None and len(full_name) > FULL_NAME_MAX:
            raise RuleBroken(NAME_TOO_LONG, code="name_too_long")
        user.full_name = full_name
    if "nickname" in changes:
        nickname = _text(changes["nickname"])
        if nickname is not None and len(nickname) > NICKNAME_MAX:
            raise RuleBroken(NICKNAME_TOO_LONG, code="nickname_too_long")
        user.nickname = nickname
    if "phone" in changes:
        user.phone = _phone(changes["phone"])
    if "avatar" in changes:
        user.avatar = _avatar(changes["avatar"])
    db.commit()
    return user


def delete_account(db: Session, user: User, *, email: str, password: str) -> None:
    """Delete the account and every entry, cap and debt it owns, for good (BR16).

    The email and the current password are asked again, even though the request is signed in:
    a phone left unlocked must not be enough to lose a year of entries. A wrong email and a wrong
    password get the same answer, as at sign-in (BR3). It is a 422, not a 401, so the app does
    not sign the person out for a typing mistake.
    """
    same_email = user_repo.normalise_email(email) == user.email
    if not verify_password(password, user.password_hash) or not same_email:
        raise RuleBroken(CONFIRMATION_MISMATCH, code="confirmation_mismatch")
    # The foreign keys of transactions, budgets and debts are ON DELETE CASCADE.
    db.delete(user)
    db.commit()
