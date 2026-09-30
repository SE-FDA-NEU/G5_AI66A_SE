"""Queries on users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User


def normalise_email(email: str) -> str:
    """BR1: capitals never make a second account, so every address is compared in lower case."""
    return email.strip().lower()


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == normalise_email(email)))


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def create(db: Session, *, email: str, password_hash: str) -> User:
    """Add an account. The caller has already hashed the password (BR2)."""
    user = User(email=normalise_email(email), password_hash=password_hash)
    db.add(user)
    db.commit()
    return user
