"""categories: the fixed list of kinds of spending and of money received (BR6, BR8)."""

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

KIND_SPENDING = "expense"
KIND_INCOME = "income"


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (CheckConstraint("kind IN ('expense', 'income')", name="kind_known"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    # "expense" for a kind of spending such as Food, "income" for money received such as Salary.
    kind: Mapped[str] = mapped_column(String(7))
