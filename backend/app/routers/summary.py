"""/api/summary: this month's income, spending and what is left (US04)."""

from fastapi import APIRouter

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.error import ErrorOut
from app.schemas.summary import SummaryOut
from app.services import summary_service

router = APIRouter(prefix="/summary", tags=["transactions"])


@router.get(
    "",
    response_model=SummaryOut,
    summary="Income, spending and what is left for one month, this month by default (US04)",
    responses={
        400: {"model": ErrorOut, "description": f'"{summary_service.INVALID_MONTH}"'},
        401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'},
    },
)
def month_summary(db: DbSession, user: CurrentUser, month: str | None = None) -> SummaryOut:
    return SummaryOut.model_validate(summary_service.month_summary(db, user.id, month=month))
