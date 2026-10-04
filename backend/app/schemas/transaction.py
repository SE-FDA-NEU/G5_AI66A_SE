"""Entries as the API returns them."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    kind: str


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    amount: int
    note: str
    occurred_on: date
    # The kind of spending; null when none was chosen (BR6).
    category: CategoryOut | None


class TransactionPage(BaseModel):
    items: list[TransactionOut]
    # How many entries the account has in all, not only the ones in `items`.
    total: int
