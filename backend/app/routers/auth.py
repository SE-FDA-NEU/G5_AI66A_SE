"""/api/auth: signing in (US02)."""

from fastapi import APIRouter, HTTPException, status

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenOut, UserOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Sign in and receive a token that lasts 7 days (US02)",
    responses={401: {"description": f'"{auth_service.INCORRECT_SIGN_IN}" (BR3)'}},
)
def login(payload: LoginRequest, db: DbSession) -> TokenOut:
    try:
        user = auth_service.authenticate(db, email=payload.email, password=payload.password)
    except auth_service.IncorrectSignIn as failure:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(failure)) from failure
    token, expires_at = create_access_token(user.id)
    return TokenOut(access_token=token, expires_at=expires_at, user=UserOut.model_validate(user))


@router.get(
    "/me",
    response_model=UserOut,
    summary="The signed-in account; the app calls it on start to skip the password (BR10)",
    responses={401: {"description": f'"{SIGN_IN_AGAIN}": no token, or it has expired'}},
)
def me(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)
