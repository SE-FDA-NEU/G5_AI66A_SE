"""Queries on transactions.

BR4: every function here takes the signed-in account's id and filters on it, so no query can
return another account's entries.
"""

from dataclasses import dataclass
from datetime import date

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import KIND_INCOME, KIND_SPENDING, Transaction


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


def month_totals(db: Session, user_id: int, *, first_day: date, last_day: date) -> MonthTotals:
    """The account's money received and spent from `first_day` to `last_day`, both included.

    One query: each SUM adds only the rows of its kind, and the WHERE keeps only this account's
    entries (BR4).
    """

    def total_of(kind: str):
        return func.coalesce(func.sum(case((Transaction.kind == kind, Transaction.amount))), 0)

    income, spending, count = db.execute(
        select(total_of(KIND_INCOME), total_of(KIND_SPENDING), func.count())
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
