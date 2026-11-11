"""/api/categories: the kinds of spending and of money received (BR6), and how much the
signed-in account put in each (US17)."""

from datetime import date

from fastapi import APIRouter

from app.core.deps import SIGN_IN_AGAIN, CurrentUser, DbSession
from app.schemas.category import CategoryDetailOut, CategorySpendingOut, MonthAmount
from app.schemas.error import ErrorOut
from app.schemas.transaction import CategoryOut, TransactionOut
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["transactions"])

SIGNED_OUT = {401: {"model": ErrorOut, "description": f'"{SIGN_IN_AGAIN}"'}}


@router.get(
    "",
    response_model=list[CategoryOut],
    summary="The 11 categories, kinds of spending first (US03)",
    responses=SIGNED_OUT,
)
def list_categories(db: DbSession, _user: CurrentUser) -> list[CategoryOut]:
    return [CategoryOut.model_validate(c) for c in category_service.list_categories(db)]


@router.get(
    "/spending",
    response_model=list[CategorySpendingOut],
    summary="Each category with what this account put in it, this month and in all (US17)",
    responses=SIGNED_OUT,
)
def spending(db: DbSession, user: CurrentUser) -> list[CategorySpendingOut]:
    rows = category_service.spending_per_category(db, user.id, today=date.today())
    return [
        CategorySpendingOut(
            category=CategoryOut.model_validate(row.category),
            this_month=row.this_month,
            all_time=row.all_time,
            count=row.count,
        )
        for row in rows
    ]


@router.get(
    "/{category_id}/spending",
    response_model=CategoryDetailOut,
    summary="One category: its totals, the last six months and its ten newest entries (US17)",
    responses={
        **SIGNED_OUT,
        404: {"model": ErrorOut, "description": f'"{category_service.CATEGORY_NOT_FOUND}"'},
    },
)
def spending_in_category(category_id: int, db: DbSession, user: CurrentUser) -> CategoryDetailOut:
    detail = category_service.category_detail(db, user.id, category_id, today=date.today())
    return CategoryDetailOut(
        category=CategoryOut.model_validate(detail.category),
        this_month=detail.this_month,
        all_time=detail.all_time,
        count=detail.count,
        months=[MonthAmount(month=m, amount=a) for m, a in detail.months],
        recent=[TransactionOut.model_validate(t) for t in detail.recent],
    )
