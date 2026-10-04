"""Queries on transactions.

BR4: every function here takes the signed-in account's id and filters on it, so no query can
return another account's entries.
"""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Transaction


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
    return entry
