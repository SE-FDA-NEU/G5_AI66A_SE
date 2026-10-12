"""/api/users: creating an account (US01)."""

from fastapi import APIRouter, status

from app.core.deps import DbSession
from app.routers.auth import signed_in
from app.schemas.auth import RegisterRequest, TokenOut
from app.schemas.error import ErrorOut
from app.services import auth_service

router = APIRouter(prefix="/users", tags=["auth"])


@router.post(
    "",
    response_model=TokenOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create an account; it is signed in at once, with no second sign-in (US01)",
    responses={
        400: {"model": ErrorOut, "description": f'"{auth_service.INVALID_EMAIL}"'},
        409: {"model": ErrorOut, "description": f'"{auth_service.EMAIL_TAKEN}" (BR1)'},
        422: {"model": ErrorOut, "description": f'"{auth_service.PASSWORD_LENGTH}" (BR2)'},
    },
)
def create_account(payload: RegisterRequest, db: DbSession) -> TokenOut:
    user = auth_service.register(db, email=payload.email, password=payload.password)
    return signed_in(user)
