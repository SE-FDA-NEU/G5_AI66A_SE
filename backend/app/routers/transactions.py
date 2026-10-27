"""/api/transactions: the entries of the signed-in account."""

from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.error import ErrorOut
from app.schemas.transaction import TransactionIn, TransactionOut, TransactionPage
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["transactions"])

NOT_SIGNED_IN = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}
NOT_FOUND = {
    404: {
        "model": ErrorOut,
        "description": (
            f'"{transaction_service.ENTRY_NOT_FOUND}": no such id, or another account\'s (BR4)'
        ),
    }
}
BROKEN_RULE = {
    422: {
        "model": ErrorOut,
        "description": (
            f'"{transaction_service.AMOUNT_NOT_POSITIVE}" (BR5) · '
            f'"{transaction_service.AMOUNT_TOO_LARGE}" (BR5) · '
            f'"{transaction_service.UNKNOWN_CATEGORY}" (BR6) · '
            f'"{transaction_service.DATE_IN_FUTURE}" (BR11)'
        ),
    }
}


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
    responses={**NOT_SIGNED_IN, **BROKEN_RULE},
)
def log_transaction(payload: TransactionIn, db: DbSession, user: CurrentUser) -> TransactionOut:
    entry = transaction_service.log_entry(db, user.id, **payload.model_dump())
    return TransactionOut.model_validate(entry)


@router.get(
    "/{entry_id}",
    response_model=TransactionOut,
    summary="One entry, to correct or remove it (US06)",
    responses={**NOT_SIGNED_IN, **NOT_FOUND},
)
def get_transaction(entry_id: int, db: DbSession, user: CurrentUser) -> TransactionOut:
    return TransactionOut.model_validate(transaction_service.get_entry(db, user.id, entry_id))


@router.patch(
    "/{entry_id}",
    response_model=TransactionOut,
    summary="Correct an entry: the form sends every field again, under the rules of US03 (US06)",
    responses={**NOT_SIGNED_IN, **NOT_FOUND, **BROKEN_RULE},
)
def correct_transaction(
    entry_id: int, payload: TransactionIn, db: DbSession, user: CurrentUser
) -> TransactionOut:
    entry = transaction_service.correct_entry(db, user.id, entry_id, **payload.model_dump())
    return TransactionOut.model_validate(entry)


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an entry for good (US06)",
    responses={**NOT_SIGNED_IN, **NOT_FOUND},
)
def remove_transaction(entry_id: int, db: DbSession, user: CurrentUser) -> Response:
    transaction_service.remove_entry(db, user.id, entry_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
