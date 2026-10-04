"""transactions: one row per amount of money spent or received."""

from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.category import Category


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        # BR5: an amount is greater than zero. It is an integer column because VND has no
        # subunit in use, so 55,000.50 cannot be stored at all.
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint("kind IN ('expense', 'income')", name="kind_known"),
        # The list on / reads one account's entries, newest first (US05).
        Index("ix_transactions_user_id_occurred_on", "user_id", "occurred_on"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # BR4: every entry belongs to exactly one account, and every read filters on it.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # BR6: at most one kind of spending, and none when the user has not chosen one.
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    # "expense" for money spent, "income" for money received.
    kind: Mapped[str] = mapped_column(String(7))
    # Whole dong. BigInteger, so a large amount cannot overflow a 32-bit column.
    amount: Mapped[int] = mapped_column(BigInteger)
    # What the user typed, kept exactly as typed, such as "tra sua".
    note: Mapped[str] = mapped_column(String(200), default="", server_default="")
    # The day the money was spent or received; never later than today (BR11, checked by the API).
    occurred_on: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category: Mapped[Category | None] = relationship()
