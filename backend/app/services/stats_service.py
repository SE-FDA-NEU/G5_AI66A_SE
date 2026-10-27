"""Where the money went: one month by kind of spending (US10), and spending month by month and
year by year, with the months that cost the most and the least (US12, BR12).

Nothing here knows about HTTP. Only the signed-in account's entries are counted (BR4): every
query in the repository filters on its id.
"""

import re
from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Category
from app.db.repositories import transaction_repo
from app.db.repositories.transaction_repo import MonthTotals
from app.services.errors import NotUnderstood, RuleBroken
from app.services.summary_service import month_bounds

INVALID_YEAR = "Year must be written YYYY"
YEAR_IN_FUTURE = "The year cannot be in the future"

YEAR_SHAPE = re.compile(r"^\d{4}$")


@dataclass
class KindShare:
    # None for the entries with no kind of spending chosen (BR6).
    category: Category | None
    amount: int
    # A whole percentage of the month's spending, rounded half up: 3,000,000 of 4,000,000 is 75.
    share: int


@dataclass
class Breakdown:
    month: str
    # All the money spent in the month; 0 means "No data yet this month" (US10, criterion 2).
    total: int
    items: list[KindShare]


@dataclass
class PeriodTotals:
    # "2026-10" for a month, "2026" for a year.
    period: str
    income: int
    spending: int
    count: int


@dataclass
class Trend:
    periods: list[PeriodTotals]
    # BR12: the period with the most spent and the one with the least, or None when no period
    # can be named.
    busiest: str | None
    quietest: str | None


def percent(part: int, whole: int) -> int:
    """`part` as a whole percentage of `whole`, rounded half up, in integers only."""
    return (part * 200 + whole) // (whole * 2)


def breakdown(
    db: Session, user_id: int, *, month: str | None = None, today: date | None = None
) -> Breakdown:
    """One month's spending by kind, the biggest first (US10). Money received is left out."""
    month = month or (today or date.today()).strftime("%Y-%m")
    first_day, last_day = month_bounds(month)
    rows = transaction_repo.spending_by_category(
        db, user_id, first_day=first_day, last_day=last_day
    )
    total = sum(amount for _, amount in rows)
    items = [KindShare(category, amount, percent(amount, total)) for category, amount in rows]
    return Breakdown(month=month, total=total, items=items)


def busiest_and_quietest(periods: list[PeriodTotals]) -> tuple[str | None, str | None]:
    """BR12: among the periods given, those with at least one entry, the one with the most spent
    and the one with the least. `periods` run oldest first, and min and max keep the first of
    equals, so a tie goes to the earlier period.
    """
    candidates = [period for period in periods if period.count > 0]
    if not candidates:
        return None, None
    busiest = max(candidates, key=lambda period: period.spending)
    quietest = min(candidates, key=lambda period: period.spending)
    return busiest.period, quietest.period


def read_year(year: str | None, today: date) -> int:
    """The year asked for, this one by default. BR12: never a year later than this one."""
    if year is None:
        return today.year
    if not YEAR_SHAPE.match(year):
        raise NotUnderstood(INVALID_YEAR, code="invalid_year")
    if int(year) > today.year:
        raise RuleBroken(YEAR_IN_FUTURE, code="year_in_future")
    return int(year)


def by_month(
    db: Session, user_id: int, *, year: str | None = None, today: date | None = None
) -> Trend:
    """The twelve months of a year, January first, each with what was received and spent (US12).

    A month after this one cannot have entries yet (BR11), so it shows 0 and, like a month with no
    entries, is never named the busiest or the quietest (BR12).
    """
    today = today or date.today()
    number = read_year(year, today)
    found = transaction_repo.totals_by_month(db, user_id, year=number)
    empty = MonthTotals(income=0, spending=0, count=0)
    periods = [
        PeriodTotals(f"{number}-{month:02d}", **vars(found.get(month, empty)))
        for month in range(1, 13)
    ]
    up_to_now = [p for p in periods if p.period <= today.strftime("%Y-%m")]
    busiest, quietest = busiest_and_quietest(up_to_now)
    return Trend(periods=periods, busiest=busiest, quietest=quietest)


def by_year(db: Session, user_id: int) -> Trend:
    """Every year the account has entries in, oldest first, with its totals (US12)."""
    found = transaction_repo.totals_by_year(db, user_id)
    periods = [PeriodTotals(str(year), **vars(found[year])) for year in sorted(found)]
    busiest, quietest = busiest_and_quietest(periods)
    return Trend(periods=periods, busiest=busiest, quietest=quietest)
