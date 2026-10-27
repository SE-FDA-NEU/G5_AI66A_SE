"""/api/stats: where the money went (US10), month by month and year by year (US12)."""

from fastapi import APIRouter

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.error import ErrorOut
from app.schemas.stats import BreakdownOut, TrendOut
from app.services import stats_service, summary_service

router = APIRouter(prefix="/stats", tags=["stats"])

NOT_SIGNED_IN = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}


@router.get(
    "/breakdown",
    response_model=BreakdownOut,
    summary="One month's spending by kind, the biggest first; this month by default (US10)",
    responses={
        **NOT_SIGNED_IN,
        400: {"model": ErrorOut, "description": f'"{summary_service.INVALID_MONTH}"'},
    },
)
def breakdown(db: DbSession, user: CurrentUser, month: str | None = None) -> BreakdownOut:
    return BreakdownOut.model_validate(stats_service.breakdown(db, user.id, month=month))


@router.get(
    "/months",
    response_model=TrendOut,
    summary="The twelve months of a year, this year by default; the busiest and quietest (US12)",
    responses={
        **NOT_SIGNED_IN,
        400: {"model": ErrorOut, "description": f'"{stats_service.INVALID_YEAR}"'},
        422: {"model": ErrorOut, "description": f'"{stats_service.YEAR_IN_FUTURE}" (BR12)'},
    },
)
def by_month(db: DbSession, user: CurrentUser, year: str | None = None) -> TrendOut:
    return TrendOut.model_validate(stats_service.by_month(db, user.id, year=year))


@router.get(
    "/years",
    response_model=TrendOut,
    summary="Every year with entries, oldest first, and the busiest and quietest (US12)",
    responses=NOT_SIGNED_IN,
)
def by_year(db: DbSession, user: CurrentUser) -> TrendOut:
    return TrendOut.model_validate(stats_service.by_year(db, user.id))
