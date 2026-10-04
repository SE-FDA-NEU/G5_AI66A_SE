"""users: one row per account."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, func
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
    email: Mapped[str] = mapped_column(String(254), unique=True)
    # BR2: only a one-way hash is stored, never the password itself.
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
