"""Reading entries (US05)."""

from sqlalchemy.orm import Session

from app.db.models import Transaction
from app.db.repositories import transaction_repo

RECENT_DEFAULT = 20


def list_recent(
    db: Session, user_id: int, *, limit: int = RECENT_DEFAULT
) -> tuple[list[Transaction], int]:
    """The signed-in account's most recent entries, newest first, and its total count.

    Only this account's entries can come back (BR4): the repository filters on user_id.
    """
    return transaction_repo.list_recent(db, user_id, limit=limit)
