"""Queries on debts (US13).

BR4: every function here takes the signed-in account's id and filters on it, so no query can
return another account's debts.
"""

from dataclasses import dataclass
from datetime import date

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.db.models import BORROWED, LENT, Debt


@dataclass
class OpenTotals:
    """What the account still owes, and what is still owed to it: open debts only (BR14)."""

    owe: int
    owed: int


def list_for_account(db: Session, user_id: int) -> list[Debt]:
    """The account's debts: open ones first, the soonest due first and those with no due date
    after them; then the settled ones, the most recently settled first.
    """
    return list(
        db.scalars(
            select(Debt)
            .where(Debt.user_id == user_id)
            .order_by(
                Debt.settled_on.is_not(None),
                Debt.due_on.is_(None),
                Debt.due_on,
                Debt.settled_on.desc(),
                Debt.id.desc(),
            )
        )
    )


def get_for_account(db: Session, user_id: int, debt_id: int) -> Debt | None:
    """The debt with this id if this account owns it; None otherwise (BR4)."""
    return db.scalar(select(Debt).where(Debt.id == debt_id, Debt.user_id == user_id))


def create(
    db: Session,
    *,
    user_id: int,
    direction: str,
    person: str,
    amount: int,
    note: str,
    started_on: date,
    due_on: date | None,
) -> Debt:
    """Add one debt, open. The service has already checked BR13."""
    debt = Debt(
        user_id=user_id,
        direction=direction,
        person=person,
        amount=amount,
        note=note,
        started_on=started_on,
        due_on=due_on,
    )
    db.add(debt)
    db.commit()
    return debt


def settle(db: Session, debt: Debt, *, on: date) -> Debt:
    """Mark a debt paid back on `on`. The service has already checked it was open (BR14)."""
    debt.settled_on = on
    db.commit()
    return debt


def delete(db: Session, debt: Debt) -> None:
    db.delete(debt)
    db.commit()


def open_totals(db: Session, user_id: int) -> OpenTotals:
    """One query: what the account owes and is owed, adding up its open debts only."""

    def total_of(direction: str):
        return func.coalesce(func.sum(case((Debt.direction == direction, Debt.amount))), 0)

    owe, owed = db.execute(
        select(total_of(BORROWED), total_of(LENT))
        .where(Debt.user_id == user_id)
        .where(Debt.settled_on.is_(None))
    ).one()
    return OpenTotals(owe=owe, owed=owed)
