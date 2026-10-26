"""/api/transactions: the entries of the signed-in account."""

from typing import Annotated

from fastapi import APIRouter, Query, status

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.error import ErrorOut
from app.schemas.transaction import TransactionIn, TransactionOut, TransactionPage
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["transactions"])

NOT_SIGNED_IN = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}


@router.get(
    "",
    response_model=TransactionPage,
    summary="The most recent entries, newest first (US05)",
    responses=NOT_SIGNED_IN,
)
def list_transactions(
    db: DbSession,
    user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=100)] = transaction_service.RECENT_DEFAULT,
) -> TransactionPage:
    entries, total = transaction_service.list_recent(db, user.id, limit=limit)
    return TransactionPage(
        items=[TransactionOut.model_validate(entry) for entry in entries], total=total
    )


@router.post(
    "",
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Log one amount spent or received (US03)",
    responses={
        **NOT_SIGNED_IN,
        422: {
            "model": ErrorOut,
            "description": (
                f'"{transaction_service.AMOUNT_NOT_POSITIVE}" (BR5) · '
                f'"{transaction_service.AMOUNT_TOO_LARGE}" (BR5) · '
                f'"{transaction_service.UNKNOWN_CATEGORY}" (BR6) · '
                f'"{transaction_service.DATE_IN_FUTURE}" (BR11)'
            ),
        },
    },
)
def log_transaction(payload: TransactionIn, db: DbSession, user: CurrentUser) -> TransactionOut:
    entry = transaction_service.log_entry(db, user.id, **payload.model_dump())
    return TransactionOut.model_validate(entry)
