"""Entries as the API receives and returns them."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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


class TransactionIn(BaseModel):
    """One amount spent or received, as the form on /transactions/new sends it (US03)."""

    # "expense" for money spent, "income" for money received.
    kind: Literal["expense", "income"]
    # Whole dong. Optional here so that an empty or zero amount reaches the service, which answers
    # with the sentence of BR5 instead of FastAPI's generic text. 55,000.50 is still malformed.
    amount: int | None = None
    note: str = Field(default="", max_length=200)
    # The day the money moved; today when left out. Never later than today (BR11).
    occurred_on: date | None = None
    # One kind of spending from GET /api/categories, or none (BR6).
    category_id: int | None = None
