"""Debts and loans: money borrowed from or lent to someone, until it is paid back (US13).

Nothing here knows about HTTP. BR13 is checked when a debt is written down and BR14 when it is
read or settled; today is a parameter, so the tests can fix it. A debt is not an entry: lending
money is not spending it, so nothing here changes the month's totals on /.
"""

from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Debt
from app.db.repositories import debt_repo
from app.services.errors import AlreadyExists, NotFound, RuleBroken
from app.services.transaction_service import DATE_IN_FUTURE, check_amount

PERSON_MIN, PERSON_MAX = 1, 60

PERSON_LENGTH = "Write a name of 1 to 60 characters"
DUE_BEFORE_START = "The due date cannot be before the start date"
ALREADY_SETTLED = "This debt is already settled"
DEBT_NOT_FOUND = "Debt not found"


@dataclass
class DebtView:
    """A debt as /debts shows it: what is stored, and whether it is overdue today (BR14)."""

    debt: Debt
    overdue: bool


@dataclass
class DebtList:
    items: list[DebtView]
    # What the account still owes, and what is still owed to it: open debts only.
    owe: int
    owed: int


def is_overdue(debt: Debt, today: date) -> bool:
    """BR14: open, with a due date, and today is after it. On the due date itself, not yet."""
    return debt.settled_on is None and debt.due_on is not None and today > debt.due_on


def list_debts(db: Session, user_id: int, *, today: date | None = None) -> DebtList:
    """The account's debts, open ones first, with what it owes and is owed (US13)."""
    today = today or date.today()
    totals = debt_repo.open_totals(db, user_id)
    debts = debt_repo.list_for_account(db, user_id)
    items = [DebtView(debt, is_overdue(debt, today)) for debt in debts]
    return DebtList(items=items, owe=totals.owe, owed=totals.owed)


def add_debt(
    db: Session,
    user_id: int,
    *,
    direction: str,
    person: str,
    amount: int | None,
    note: str = "",
    started_on: date | None = None,
    due_on: date | None = None,
    today: date | None = None,
) -> DebtView:
    """Write down one debt, open (US13).

    Checked in the order the form lists its fields, the first one broken is the answer:
    - BR13: who the money is with, 1 to 60 characters once the spaces around it are dropped;
    - BR5: the amount, as for an entry;
    - BR11: the day it started is today or earlier, today when left out;
    - BR13: the due date, if any, is not before the day it started.
    """
    today = today or date.today()
    person = person.strip()
    if not PERSON_MIN <= len(person) <= PERSON_MAX:
        raise RuleBroken(PERSON_LENGTH, code="person_length")
    check_amount(amount)
    started_on = started_on or today
    if started_on > today:
        raise RuleBroken(DATE_IN_FUTURE, code="date_in_future")
    if due_on is not None and due_on < started_on:
        raise RuleBroken(DUE_BEFORE_START, code="due_before_start")
    debt = debt_repo.create(
        db,
        user_id=user_id,
        direction=direction,
        person=person,
        amount=amount,
        note=note,
        started_on=started_on,
        due_on=due_on,
    )
    return DebtView(debt, is_overdue(debt, today))


def get_debt(db: Session, user_id: int, debt_id: int) -> Debt:
    """BR4: another account's debt answers exactly like an id that does not exist."""
    debt = debt_repo.get_for_account(db, user_id, debt_id)
    if debt is None:
        raise NotFound(DEBT_NOT_FOUND, code="debt_not_found")
    return debt


def settle_debt(db: Session, user_id: int, debt_id: int, *, today: date | None = None) -> DebtView:
    """Mark a debt paid back today. BR14: a settled debt cannot be settled twice."""
    today = today or date.today()
    debt = get_debt(db, user_id, debt_id)
    if debt.settled_on is not None:
        raise AlreadyExists(ALREADY_SETTLED, code="already_settled")
    return DebtView(debt_repo.settle(db, debt, on=today), overdue=False)


def remove_debt(db: Session, user_id: int, debt_id: int) -> None:
    """Remove a debt written down by mistake, open or settled. The app asks first."""
    debt_repo.delete(db, get_debt(db, user_id, debt_id))
