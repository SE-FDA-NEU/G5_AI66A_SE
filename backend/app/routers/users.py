"""/api/users: creating an account (US01), its profile (US16) and deleting it (US18)."""

from fastapi import APIRouter, Response, status

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.routers.auth import signed_in
from app.schemas.auth import RegisterRequest, TokenOut, UserOut
from app.schemas.error import ErrorOut
from app.schemas.profile import AccountDeletion, ProfileUpdate
from app.services import auth_service, profile_service

router = APIRouter(prefix="/users", tags=["auth"])

SIGNED_OUT = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}


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


@router.get(
    "/me",
    response_model=UserOut,
    summary="The signed-in account and its profile (US16)",
    responses=SIGNED_OUT,
)
def read_profile(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)


@router.patch(
    "/me",
    response_model=UserOut,
    summary="Change the profile: full name, the name to call you, phone, picture (US16, BR15)",
    responses={
        **SIGNED_OUT,
        400: {"model": ErrorOut, "description": "A field that does not exist, such as email"},
        422: {"model": ErrorOut, "description": "A field that breaks BR15"},
    },
)
def update_profile(payload: ProfileUpdate, db: DbSession, user: CurrentUser) -> UserOut:
    changes = payload.model_dump(include=payload.model_fields_set)
    return UserOut.model_validate(profile_service.update_profile(db, user, changes))


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete the account and everything it owns, after its email and password (BR16)",
    responses={
        **SIGNED_OUT,
        422: {"model": ErrorOut, "description": f'"{profile_service.CONFIRMATION_MISMATCH}"'},
    },
)
def delete_account(payload: AccountDeletion, db: DbSession, user: CurrentUser) -> Response:
    profile_service.delete_account(db, user, email=payload.email, password=payload.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
