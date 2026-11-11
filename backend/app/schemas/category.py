"""What each category holds for one account (US17)."""

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
