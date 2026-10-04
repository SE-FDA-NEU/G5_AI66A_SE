"""budgets: a monthly cap on one kind of spending (US08).

The table exists from Sprint 2 so that the data model is complete; the screen that sets caps
arrives with US08.
"""

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        # BR7: at most one cap per account, per kind of spending, per month. Saving again
        # replaces the figure instead of adding a second row.
        UniqueConstraint("user_id", "category_id", "month"),
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint("month LIKE '____-__'", name="month_yyyy_mm"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # BR8: must be a kind of spending, never money received. The service checks it, because a
    # CHECK constraint cannot look at another table.
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    # The month the cap applies to, as YYYY-MM, such as 2026-11.
    month: Mapped[str] = mapped_column(String(7))
    # The cap in whole dong.
    amount: Mapped[int] = mapped_column(BigInteger)
