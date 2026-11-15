"""categories: the shared list of kinds of spending and of money received (BR6, BR8), and the
categories an account added for itself from "Other" (BR17)."""

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

KIND_SPENDING = "expense"
KIND_INCOME = "income"


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("kind IN ('expense', 'income')", name="kind_known"),
        # BR17: one account never has the same name twice. The shared names have no owner, so
        # the service checks them itself (category_service.add_category).
        UniqueConstraint("user_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    # "expense" for a kind of spending such as Food, "income" for money received such as Salary.
    kind: Mapped[str] = mapped_column(String(7))
    # None for the eleven shared categories; the owner's id for a category an account added.
    # Deleting the account deletes its categories too (BR16).
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    @property
    def custom(self) -> bool:
        """True for a category the account named itself: the app shows its name as typed."""
        return self.user_id is not None
