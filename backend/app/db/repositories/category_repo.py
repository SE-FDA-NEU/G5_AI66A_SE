"""Queries on categories."""

from sqlalchemy import case, func, or_, select
from sqlalchemy.orm import Session

from app.db.models import KIND_SPENDING, Category


def _visible_to(user_id: int | None):
    """The shared categories, and with an account, the ones it added (BR17)."""
    if user_id is None:
        return Category.user_id.is_(None)
    return or_(Category.user_id.is_(None), Category.user_id == user_id)


def list_all(db: Session, user_id: int | None = None) -> list[Category]:
    """The shared categories and the account's own: kinds of spending first, then money
    received; in each, the shared ones in id order, then the account's own in the order added."""
    spending_first = case((Category.kind == KIND_SPENDING, 0), else_=1)
    own_last = case((Category.user_id.is_(None), 0), else_=1)
    query = select(Category).where(_visible_to(user_id))
    return list(db.scalars(query.order_by(spending_first, own_last, Category.id)))


def get_by_name(db: Session, name: str) -> Category | None:
    """A shared category by its name, such as "Food"."""
    return db.scalar(select(Category).where(Category.name == name, Category.user_id.is_(None)))


def get_by_id(db: Session, category_id: int, user_id: int | None = None) -> Category | None:
    """The category with this id if this account may use it, or None (BR4): a shared one, or
    one the account added. Another account's own category answers like an id that does not
    exist."""
    return db.scalar(select(Category).where(Category.id == category_id, _visible_to(user_id)))


def name_taken(db: Session, user_id: int, name: str) -> bool:
    """Whether a shared category, or one of this account's, already has this name, whatever its
    capitals."""
    query = select(func.count()).where(
        _visible_to(user_id), func.lower(Category.name) == name.lower()
    )
    return bool(db.scalar(query))


def create(db: Session, *, user_id: int, name: str, kind: str) -> Category:
    category = Category(user_id=user_id, name=name, kind=kind)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
