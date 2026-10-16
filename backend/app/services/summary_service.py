"""This month's position: income, spending and what is left (US04)."""

import calendar
import re
from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.db.repositories import transaction_repo
from app.services.errors import NotUnderstood

INVALID_MONTH = "Month must be written YYYY-MM"

MONTH_SHAPE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")


@dataclass
class MonthSummary:
    month: str
    income: int
    spending: int
    remaining: int
    count: int


def month_bounds(month: str) -> tuple[date, date]:
    """The first and last day of a month written YYYY-MM, such as 2026-11."""
    match = MONTH_SHAPE.match(month)
    if match is None:
        raise NotUnderstood(INVALID_MONTH, code="invalid_month")
    year, number = int(match[1]), int(match[2])
    return date(year, number, 1), date(year, number, calendar.monthrange(year, number)[1])


def month_summary(
    db: Session, user_id: int, *, month: str | None = None, today: date | None = None
) -> MonthSummary:
    """What the account received and spent in `month`, this month by default, and what is left.

    `remaining` is income minus spending, so it goes below 0 when more was spent than received.
    `count` lets the app tell an empty month from one where everything adds up to 0 (US04,
    criterion 3). Only this account's entries count (BR4).
    """
    month = month or (today or date.today()).strftime("%Y-%m")
    first_day, last_day = month_bounds(month)
    totals = transaction_repo.month_totals(db, user_id, first_day=first_day, last_day=last_day)
    return MonthSummary(
        month=month,
        income=totals.income,
        spending=totals.spending,
        remaining=totals.income - totals.spending,
        count=totals.count,
    )
