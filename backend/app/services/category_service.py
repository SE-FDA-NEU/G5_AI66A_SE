"""The categories: the fixed list of kinds of spending and of money received (BR6, BR8), and
how much an account put in each (US17)."""

from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Category, Transaction
from app.db.repositories import category_repo, transaction_repo
from app.services.errors import NotFound

CATEGORY_NOT_FOUND = "Category not found"
MONTHS_SHOWN = 6
RECENT_SHOWN = 10


@dataclass
class CategorySpending:
    category: Category
    this_month: int
    all_time: int
    count: int


@dataclass
class CategoryDetail(CategorySpending):
    months: list[tuple[str, int]]
    recent: list[Transaction]


def list_categories(db: Session) -> list[Category]:
    """All 11, the kinds of spending first, for the picker on /transactions/new (US03)."""
    return category_repo.list_all(db)


def spending_per_category(db: Session, user_id: int, *, today: date) -> list[CategorySpending]:
    """Every category with what this account put in it, this month and over all time (US17).

    In the order of list_categories, so the eight kinds of spending come first; a category the
    account never used is listed at 0, so the list is the same for everyone.
    """
    all_time = transaction_repo.totals_by_category(db, user_id)
    this_month = transaction_repo.totals_by_category(db, user_id, since=today.replace(day=1))
    return [
        CategorySpending(
            category=category,
            this_month=this_month.get(category.id, (0, 0))[0],
            all_time=all_time.get(category.id, (0, 0))[0],
            count=all_time.get(category.id, (0, 0))[1],
        )
        for category in category_repo.list_all(db)
    ]


def _months_back(today: date, count: int) -> list[date]:
    """The 1st of this month and of the `count - 1` months before it, oldest first."""
    firsts = []
    for back in range(count - 1, -1, -1):
        index = today.year * 12 + today.month - 1 - back
        firsts.append(date(index // 12, index % 12 + 1, 1))
    return firsts


def category_detail(db: Session, user_id: int, category_id: int, *, today: date) -> CategoryDetail:
    """One category for this account: its totals, the last six months and its newest entries."""
    category = category_repo.get_by_id(db, category_id)
    if category is None:
        raise NotFound(CATEGORY_NOT_FOUND, code="category_not_found")
    totals = next(
        s for s in spending_per_category(db, user_id, today=today) if s.category.id == category_id
    )
    firsts = _months_back(today, MONTHS_SHOWN)
    by_month = transaction_repo.category_totals_by_month(
        db, user_id, category_id, first_day=firsts[0]
    )
    months = [(f"{d.year:04d}-{d.month:02d}", 0) for d in firsts]
    months = [(key, by_month.get(key, 0)) for key, _ in months]
    recent = transaction_repo.list_in_category(db, user_id, category_id, limit=RECENT_SHOWN)
    return CategoryDetail(
        category=category,
        this_month=totals.this_month,
        all_time=totals.all_time,
        count=totals.count,
        months=months,
        recent=recent,
    )
