"""The fixed list of kinds of spending and of money received (BR6, BR8)."""

from sqlalchemy.orm import Session

from app.db.models import Category
from app.db.repositories import category_repo


def list_categories(db: Session) -> list[Category]:
    """All 11, the kinds of spending first, for the picker on /transactions/new (US03)."""
    return category_repo.list_all(db)
