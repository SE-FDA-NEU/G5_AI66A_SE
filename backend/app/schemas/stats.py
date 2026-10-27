"""Where the money went, as /stats shows it (US10, US12)."""

from pydantic import BaseModel, ConfigDict

from app.schemas.transaction import CategoryOut


class KindShareOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # The kind of spending; null for the entries with none chosen (BR6).
    category: CategoryOut | None
    # Whole dong spent on it in the month.
    amount: int
    # A whole percentage of the month's spending, rounded half up.
    share: int


class BreakdownOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    month: str
    # All the money spent in the month; 0 means "No data yet this month".
    total: int
    # The biggest first.
    items: list[KindShareOut]


class PeriodOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # "2026-10" for a month, "2026" for a year.
    period: str
    income: int
    spending: int
    # How many entries; 0 means nothing was written down in it.
    count: int


class TrendOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Oldest first.
    periods: list[PeriodOut]
    # BR12: the period with the most spent and the one with the least; null when none can be named.
    busiest: str | None
    quietest: str | None
