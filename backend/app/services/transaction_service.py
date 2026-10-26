"""Entries: reading the recent ones (US05) and logging a new one (US03).

Nothing here knows about HTTP. A broken rule raises RuleBroken with the exact sentence of the
acceptance criteria, and app/core/errors.py answers it with 422.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Transaction
from app.db.repositories import category_repo, transaction_repo
from app.services.errors import RuleBroken

RECENT_DEFAULT = 20

# BR5: the largest amount one entry can hold. A month adds its entries up in one SQL SUM, which
# stops at 9,223,372,036,854,775,807; at one trillion dong per entry it takes over nine million
# entries to get there, so the totals on / can never overflow (bug #142).
AMOUNT_MAX = 1_000_000_000_000

AMOUNT_NOT_POSITIVE = "Enter an amount greater than 0"
AMOUNT_TOO_LARGE = "Enter an amount of at most 1,000,000,000,000"
DATE_IN_FUTURE = "The date cannot be in the future"
UNKNOWN_CATEGORY = "Choose a kind of spending from the list"


def list_recent(
    db: Session, user_id: int, *, limit: int = RECENT_DEFAULT
) -> tuple[list[Transaction], int]:
    """The signed-in account's most recent entries, newest first, and its total count.

    Only this account's entries can come back (BR4): the repository filters on user_id.
    """
    return transaction_repo.list_recent(db, user_id, limit=limit)


def log_entry(
    db: Session,
    user_id: int,
    *,
    kind: str,
    amount: int | None,
    note: str = "",
    occurred_on: date | None = None,
    category_id: int | None = None,
    today: date | None = None,
) -> Transaction:
    """Store one amount spent or received for the signed-in account, and return it (US03).

    The rules are checked in the order the form lists its fields, and the first one broken is the
    answer:
    - BR5: an amount is a whole number of dong, greater than 0 and at most AMOUNT_MAX. An empty
      amount breaks it too.
    - BR6: a kind of spending, when chosen, is one from the list, of the same kind as the entry:
      money spent is never filed under Salary. None chosen is allowed; nothing is guessed.
    - BR11: the date is today or earlier. No date means today.
    The note is kept exactly as typed, such as "tra sua".
    """
    today = today or date.today()
    if amount is None or amount <= 0:
        raise RuleBroken(AMOUNT_NOT_POSITIVE, code="amount_not_positive")
    if amount > AMOUNT_MAX:
        raise RuleBroken(AMOUNT_TOO_LARGE, code="amount_too_large")
    if category_id is not None:
        category = category_repo.get_by_id(db, category_id)
        if category is None or category.kind != kind:
            raise RuleBroken(UNKNOWN_CATEGORY, code="unknown_category")
    occurred_on = occurred_on or today
    if occurred_on > today:
        raise RuleBroken(DATE_IN_FUTURE, code="date_in_future")
    return transaction_repo.create(
        db,
        user_id=user_id,
        kind=kind,
        amount=amount,
        note=note,
        occurred_on=occurred_on,
        category_id=category_id,
    )
