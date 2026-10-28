"""Debts and loans as the API receives and returns them (US13)."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class DebtIn(BaseModel):
    """One debt, as the form on /debts/new sends it."""

    # "borrowed": you owe the money. "lent": it is owed to you.
    direction: Literal["borrowed", "lent"]
    # Who the money is with. The service checks 1 to 60 characters (BR13), so the answer is the
    # sentence of US13; this limit only stops an absurdly long request.
    person: str = Field(max_length=1000)
    # Whole dong (BR5). Optional here, as for an entry, so an empty amount gets BR5's sentence.
    amount: int | None = None
    note: str = Field(default="", max_length=200)
    # The day the money changed hands; today when left out (BR11).
    started_on: date | None = None
    # When it should be paid back, or none (BR13).
    due_on: date | None = None


class DebtOut(BaseModel):
    id: int
    direction: str
    person: str
    amount: int
    note: str
    started_on: date
    due_on: date | None
    # Null while the debt is open.
    settled_on: date | None
    # BR14: open, and today is after its due date.
    overdue: bool


class DebtListOut(BaseModel):
    # Open debts first, the soonest due first; then the settled ones.
    items: list[DebtOut]
    # What you still owe, and what is still owed to you: open debts only.
    owe: int
    owed: int
