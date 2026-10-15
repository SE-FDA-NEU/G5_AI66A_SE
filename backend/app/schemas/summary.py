"""This month's position, as the overview on / shows it (US04)."""

from pydantic import BaseModel, ConfigDict


class SummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # The month the totals are for, as YYYY-MM.
    month: str
    # Whole dong received and spent in that month.
    income: int
    spending: int
    # income minus spending; below 0 when more was spent than received.
    remaining: int
    # How many entries the month has; 0 means "No transactions yet this month", not three zeros.
    count: int
