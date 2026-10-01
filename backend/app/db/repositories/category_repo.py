"""Queries on categories."""

from sqlalchemy import case, select
from sqlalchemy.orm import Session

from app.db.models import KIND_SPENDING, Category


def list_all(db: Session) -> list[Category]:
    """Every category: the kinds of spending first, then money received, each in id order."""
    spending_first = case((Category.kind == KIND_SPENDING, 0), else_=1)
    return list(db.scalars(select(Category).order_by(spending_first, Category.id)))


def get_by_name(db: Session, name: str) -> Category | None:
    return db.scalar(select(Category).where(Category.name == name))
