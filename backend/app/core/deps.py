"""What an endpoint can ask for: a database session, and the signed-in account."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import read_access_token
from app.db.models import User
from app.db.session import SessionLocal
from app.services import auth_service

SIGN_IN_AGAIN = auth_service.SIGN_IN_AGAIN

bearer = HTTPBearer(auto_error=False)


def get_db() -> Iterator[Session]:
    """One session per request, closed when the response has been sent."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> User:
    """The account named by the bearer token.

    A missing, forged or expired token (BR10), or one for a deleted account, all answer 401 with
    the same sentence and the code sign_in_again; the app then shows the sign-in screen.
    """
    user_id = read_access_token(credentials.credentials) if credentials else None
    user = auth_service.signed_in_account(db, user_id) if user_id is not None else None
    if user is None:
        raise auth_service.SessionOver(SIGN_IN_AGAIN)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
