"""users: one row per account."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # BR1: one address is one account whatever its capitals. Addresses are stored in lower
        # case, so the UNIQUE constraint on email also catches TUAN@X.COM against tuan@x.com.
        CheckConstraint("email = lower(email)", name="email_lower_case"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # BR15: the address an account was created with never changes.
    email: Mapped[str] = mapped_column(String(254), unique=True)
    # BR2: only a one-way hash is stored, never the password itself.
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # The profile (US16, BR15). Every field is optional: an account without them is greeted by
    # its email, as before Sprint 5.
    full_name: Mapped[str | None] = mapped_column(String(80))
    # "What should we call you?": the name the greeting uses first.
    nickname: Mapped[str | None] = mapped_column(String(40))
    phone: Mapped[str | None] = mapped_column(String(30))
    # A small picture, kept in the database as a data: URL. Render's disk is emptied at every
    # deploy, so a file on disk would not survive (ADR 4); BR15 keeps it at 200 KB or less.
    avatar: Mapped[str | None] = mapped_column(Text)
