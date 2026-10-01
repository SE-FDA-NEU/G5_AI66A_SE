"""/api/transactions: the entries of the signed-in account."""

from typing import Annotated

from fastapi import APIRouter, Query

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.transaction import TransactionOut, TransactionPage
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get(
    "",
    response_model=TransactionPage,
    summary="The most recent entries, newest first (US05)",
    responses={401: {"description": f'"{SIGN_IN_AGAIN}"'}},
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
