"""Entries: reading the recent ones (US05), logging a new one (US03), correcting or removing one
(US06).

Nothing here knows about HTTP. A broken rule raises RuleBroken with the exact sentence of the
acceptance criteria, and app/core/errors.py answers it with 422.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Transaction
from app.db.repositories import category_repo, transaction_repo
from app.services.errors import NotFound, RuleBroken

RECENT_DEFAULT = 20

# BR5: the largest amount one entry can hold. A month adds its entries up in one SQL SUM, which
# stops at 9,223,372,036,854,775,807; at one trillion dong per entry it takes over nine million
# entries to get there, so the totals on / can never overflow (bug #142).
AMOUNT_MAX = 1_000_000_000_000

AMOUNT_NOT_POSITIVE = "Enter an amount greater than 0"
AMOUNT_TOO_LARGE = "Enter an amount of at most 1,000,000,000,000"
DATE_IN_FUTURE = "The date cannot be in the future"
UNKNOWN_CATEGORY = "Choose a kind of spending from the list"
ENTRY_NOT_FOUND = "Entry not found"


def list_recent(
    db: Session, user_id: int, *, limit: int = RECENT_DEFAULT
) -> tuple[list[Transaction], int]:
    """The signed-in account's most recent entries, newest first, and its total count.

    Only this account's entries can come back (BR4): the repository filters on user_id.
    """
    return transaction_repo.list_recent(db, user_id, limit=limit)


def check_entry(
    db: Session,
    *,
    kind: str,
    amount: int | None,
    occurred_on: date | None,
    category_id: int | None,
    today: date,
) -> date:
    """Check an entry against BR5, BR6 and BR11, and return the day it is dated.

    New and corrected entries follow the same rules, so both call this one function. The rules
    are checked in the order the form lists its fields, and the first one broken is the answer:
    - BR5: an amount is a whole number of dong, greater than 0 and at most AMOUNT_MAX. An empty
      amount breaks it too.
    - BR6: a kind of spending, when chosen, is one from the list, of the same kind as the entry:
      money spent is never filed under Salary. None chosen is allowed; nothing is guessed.
    - BR11: the date is today or earlier. No date means today.
    """
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
    return occurred_on


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

    Nothing is stored when a rule is broken (check_entry). The note is kept exactly as typed,
    such as "tra sua".
    """
    occurred_on = check_entry(
        db,
        kind=kind,
        amount=amount,
        occurred_on=occurred_on,
        category_id=category_id,
        today=today or date.today(),
    )
    return transaction_repo.create(
        db,
        user_id=user_id,
        kind=kind,
        amount=amount,
        note=note,
        occurred_on=occurred_on,
        category_id=category_id,
    )


def get_entry(db: Session, user_id: int, entry_id: int) -> Transaction:
    """One entry of the signed-in account (US06).

    BR4: another account's entry answers exactly like an id that does not exist, "Entry not found",
    so nobody can find out which ids exist.
    """
    entry = transaction_repo.get_for_account(db, user_id, entry_id)
    if entry is None:
        raise NotFound(ENTRY_NOT_FOUND, code="entry_not_found")
    return entry


def correct_entry(
    db: Session,
    user_id: int,
    entry_id: int,
    *,
    kind: str,
    amount: int | None,
    note: str = "",
    occurred_on: date | None = None,
    category_id: int | None = None,
    today: date | None = None,
) -> Transaction:
    """Replace what an entry says, under the same rules as a new one (US06).

    The month's totals follow at once: 150,000 corrected to 50,000 spends 100,000 less. When a
    rule is broken, the entry stays exactly as it was.
    """
    entry = get_entry(db, user_id, entry_id)
    occurred_on = check_entry(
        db,
        kind=kind,
        amount=amount,
        occurred_on=occurred_on,
        category_id=category_id,
        today=today or date.today(),
    )
    return transaction_repo.update(
        db,
        entry,
        kind=kind,
        amount=amount,
        note=note,
        occurred_on=occurred_on,
        category_id=category_id,
    )


def remove_entry(db: Session, user_id: int, entry_id: int) -> None:
    """Remove one entry of the signed-in account for good (US06). The app asks first."""
    transaction_repo.delete(db, get_entry(db, user_id, entry_id))
