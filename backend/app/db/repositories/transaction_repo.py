"""Queries on transactions.

BR4: every function here takes the signed-in account's id and filters on it, so no query can
return another account's entries.
"""

from dataclasses import dataclass
from datetime import date

from sqlalchemy import case, extract, func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import KIND_INCOME, KIND_SPENDING, Category, Transaction


@dataclass
class MonthTotals:
    """What one account received and spent between two dates, and in how many entries."""

    income: int
    spending: int
    count: int


def list_recent(db: Session, user_id: int, *, limit: int) -> tuple[list[Transaction], int]:
    """The account's `limit` most recent entries, newest first, and how many it has in all."""
    total = db.scalar(
        select(func.count()).select_from(Transaction).where(Transaction.user_id == user_id)
    )
    entries = db.scalars(
        select(Transaction)
        .options(joinedload(Transaction.category))
        .where(Transaction.user_id == user_id)
        # Newest day first; on the same day, the entry written last comes first.
        .order_by(Transaction.occurred_on.desc(), Transaction.id.desc())
        .limit(limit)
    )
    return list(entries), total or 0


def create(
    db: Session,
    *,
    user_id: int,
    kind: str,
    amount: int,
    note: str,
    occurred_on: date,
    category_id: int | None,
) -> Transaction:
    """Add one entry. The service has already checked the amount and the date."""
    entry = Transaction(
        user_id=user_id,
        kind=kind,
        amount=amount,
        note=note,
        occurred_on=occurred_on,
        category_id=category_id,
    )
    db.add(entry)
    db.commit()
    # Load the kind of spending now, so the answer can show its name without another query.
    db.refresh(entry, ["category"])
    return entry


def _total_of(kind: str):
    """SUM of the amounts of one kind only, 0 when there are none."""
    return func.coalesce(func.sum(case((Transaction.kind == kind, Transaction.amount))), 0)


def month_totals(db: Session, user_id: int, *, first_day: date, last_day: date) -> MonthTotals:
    """The account's money received and spent from `first_day` to `last_day`, both included.

    One query: each SUM adds only the rows of its kind, and the WHERE keeps only this account's
    entries (BR4).
    """
    income, spending, count = db.execute(
        select(_total_of(KIND_INCOME), _total_of(KIND_SPENDING), func.count())
        .where(Transaction.user_id == user_id)
        .where(Transaction.occurred_on.between(first_day, last_day))
    ).one()
    return MonthTotals(income=income, spending=spending, count=count)


def get_for_account(db: Session, user_id: int, entry_id: int) -> Transaction | None:
    """The entry with this id if this account owns it; None otherwise (US06).

    Another account's entry and an id that does not exist both give None, so the service cannot
    tell them apart and neither can the caller (BR4).
    """
    return db.scalar(
        select(Transaction)
        .options(joinedload(Transaction.category))
        .where(Transaction.id == entry_id, Transaction.user_id == user_id)
    )


def update(
    db: Session,
    entry: Transaction,
    *,
    kind: str,
    amount: int,
    note: str,
    occurred_on: date,
    category_id: int | None,
) -> Transaction:
    """Replace what an entry says. The service has already checked it, as for a new one."""
    entry.kind = kind
    entry.amount = amount
    entry.note = note
    entry.occurred_on = occurred_on
    entry.category_id = category_id
    db.commit()
    db.refresh(entry, ["category"])
    return entry


def delete(db: Session, entry: Transaction) -> None:
    """Remove one entry for good. The service has already checked who owns it."""
    db.delete(entry)
    db.commit()


def spending_by_category(
    db: Session, user_id: int, *, first_day: date, last_day: date
) -> list[tuple[Category | None, int]]:
    """Money spent from `first_day` to `last_day`, added up per kind of spending (US10).

    Entries with no kind chosen (BR6) are added up together, under None. Money received is left
    out. The biggest total comes first; equal totals in category id order, None last.
    """
    total = func.sum(Transaction.amount)
    rows = db.execute(
        select(Transaction.category_id, total)
        .where(Transaction.user_id == user_id)
        .where(Transaction.kind == KIND_SPENDING)
        .where(Transaction.occurred_on.between(first_day, last_day))
        .group_by(Transaction.category_id)
        .order_by(total.desc(), Transaction.category_id.is_(None), Transaction.category_id)
    ).all()
    return [
        (db.get(Category, category_id) if category_id is not None else None, amount)
        for category_id, amount in rows
    ]


def totals_by_month(db: Session, user_id: int, *, year: int) -> dict[int, MonthTotals]:
    """The account's totals for each month of `year` that has an entry, keyed 1 to 12 (US12)."""
    month = extract("month", Transaction.occurred_on)
    rows = db.execute(
        select(month, _total_of(KIND_INCOME), _total_of(KIND_SPENDING), func.count())
        .where(Transaction.user_id == user_id)
        .where(Transaction.occurred_on.between(date(year, 1, 1), date(year, 12, 31)))
        .group_by(month)
    ).all()
    return {
        int(number): MonthTotals(income=income, spending=spending, count=count)
        for number, income, spending, count in rows
    }


def totals_by_year(db: Session, user_id: int) -> dict[int, MonthTotals]:
    """The account's totals for each year that has an entry, keyed by the year (US12)."""
    year = extract("year", Transaction.occurred_on)
    rows = db.execute(
        select(year, _total_of(KIND_INCOME), _total_of(KIND_SPENDING), func.count())
        .where(Transaction.user_id == user_id)
        .group_by(year)
    ).all()
    return {
        int(number): MonthTotals(income=income, spending=spending, count=count)
        for number, income, spending, count in rows
    }
