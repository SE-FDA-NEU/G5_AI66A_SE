"""What each category holds for one account (US17)."""

from typing import Literal

from pydantic import BaseModel

from app.schemas.transaction import CategoryOut, TransactionOut


class CategorySpendingOut(BaseModel):
    category: CategoryOut
    # Whole dong in this category: this month, and since the account's first entry.
    this_month: int
    all_time: int
    # How many entries, over all time.
    count: int


class MonthAmount(BaseModel):
    month: str  # "YYYY-MM"
    amount: int


class CategoryDetailOut(CategorySpendingOut):
    # The last six months, oldest first, months without an entry at 0.
    months: list[MonthAmount]
    # The ten newest entries of the category, newest first.
    recent: list[TransactionOut]


class CategoryIn(BaseModel):
    # BR17: 1 to 40 characters once the spaces around it are gone; checked by the service, so
    # the answer is the rule's own sentence.
    name: str
    kind: Literal["expense", "income"] = "expense"
