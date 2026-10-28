"""debts: money borrowed from or lent to someone, until it is settled (US13)."""

from datetime import date, datetime

from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

BORROWED = "borrowed"
LENT = "lent"


class Debt(Base):
    __tablename__ = "debts"
    __table_args__ = (
        CheckConstraint("direction IN ('borrowed', 'lent')", name="direction_known"),
        # BR13: a name of 1 to 60 characters, and an amount that follows BR5.
        CheckConstraint("length(person) BETWEEN 1 AND 60", name="person_length"),
        CheckConstraint("amount > 0", name="amount_positive"),
        # BR13: a due date is never before the day the money changed hands.
        CheckConstraint("due_on IS NULL OR due_on >= started_on", name="due_not_before_start"),
        # /debts reads one account's debts, the open ones first.
        Index("ix_debts_user_id_settled_on", "user_id", "settled_on"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # BR4: every debt belongs to exactly one account, and every read filters on it.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # "borrowed": the user owes the money. "lent": the money is owed to the user.
    direction: Mapped[str] = mapped_column(String(8))
    # Who the money is with, exactly as typed, such as "Lan".
    person: Mapped[str] = mapped_column(String(60))
    # Whole dong, as BR5 says for an entry.
    amount: Mapped[int] = mapped_column(BigInteger)
    note: Mapped[str] = mapped_column(String(200), default="", server_default="")
    # The day the money changed hands; never later than today (BR11, checked by the API).
    started_on: Mapped[date] = mapped_column(Date)
    # When it should be paid back; none means no date was agreed.
    due_on: Mapped[date | None] = mapped_column(Date)
    # The day it was paid back; none while it is open (BR14).
    settled_on: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
