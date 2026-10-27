"""Where the money went: US10 by kind of spending, US12 month by month and year by year (BR12).

Test cases TC-53 to TC-65 of docs/testing.md, section 2; the ID is in each test's name or row. The
rules are tested on the service with today fixed at 24/10/2026, and the routes once each.
"""

from datetime import date

import pytest

from app.db.repositories import category_repo, transaction_repo
from app.services import stats_service
from app.services.errors import NotUnderstood, RuleBroken
from tests.conftest import make_account

TODAY = date(2026, 10, 24)


def add(db, user_id: int, amount: int, on: date, kind_of_spending: str | None = "Food"):
    category = category_repo.get_by_name(db, kind_of_spending) if kind_of_spending else None
    transaction_repo.create(
        db,
        user_id=user_id,
        kind=category.kind if category else "expense",
        amount=amount,
        note="",
        occurred_on=on,
        category_id=category.id if category else None,
    )


def months(db, user_id: int, year: str | None = "2026"):
    return stats_service.by_month(db, user_id, year=year, today=TODAY)


def spending_of(trend) -> dict[str, int]:
    return {period.period: period.spending for period in trend.periods if period.count}


# US10: one month by kind of spending.


def test_tc53_food_3000000_of_4000000_comes_first_at_75_percent(db, account):
    """TC-53, US10 criterion 1."""
    add(db, account.id, 3_000_000, TODAY, "Food")
    add(db, account.id, 1_000_000, TODAY, "Transport")

    month = stats_service.breakdown(db, account.id, month="2026-10")

    assert month.total == 4_000_000
    first = month.items[0]
    assert (first.category.name, first.amount, first.share) == ("Food", 3_000_000, 75)
    assert month.items[1].share == 25


def test_tc54_a_month_with_no_entries_has_nothing_to_break_down(db, account):
    """TC-54, US10 criterion 2: total 0 lets the app say "No data yet this month"."""
    month = stats_service.breakdown(db, account.id, month="2026-10")

    assert (month.total, month.items) == (0, [])


def test_tc55_money_received_is_never_in_the_breakdown(db, account):
    add(db, account.id, 4_000_000, TODAY, "Salary")
    add(db, account.id, 55_000, TODAY, "Food")

    month = stats_service.breakdown(db, account.id, month="2026-10")

    assert [(item.category.name, item.share) for item in month.items] == [("Food", 100)]


def test_tc56_entries_with_no_kind_are_one_line_of_their_own(db, account):
    """BR6: nothing is guessed, so the app shows them as "No kind of spending"."""
    add(db, account.id, 60_000, TODAY, "Food")
    add(db, account.id, 40_000, TODAY, None)

    month = stats_service.breakdown(db, account.id, month="2026-10")

    assert [(item.category, item.share) for item in month.items][1] == (None, 40)


@pytest.mark.parametrize(
    ("part", "whole", "share"),
    [(1, 3, 33), (2, 3, 67), (1, 8, 13), (1, 200, 1), (1, 201, 0)],
    ids=["1/3", "2/3", "12.5% rounds up", "0.5% rounds up", "0.497% rounds down"],
)
def test_tc57_shares_are_whole_percentages_rounded_half_up(part, whole, share):
    assert stats_service.percent(part, whole) == share


# US12: month by month, year by year (BR12).


def test_tc58_october_is_named_the_month_with_the_most_spent(db, account):
    """TC-58, US12 criterion 1: 2,931,000 in October, 1,200,000 in September."""
    add(db, account.id, 1_200_000, date(2026, 9, 15))
    add(db, account.id, 2_931_000, date(2026, 10, 3))

    trend = months(db, account.id)

    assert len(trend.periods) == 12
    assert spending_of(trend) == {"2026-09": 1_200_000, "2026-10": 2_931_000}
    assert (trend.busiest, trend.quietest) == ("2026-10", "2026-09")


def test_tc59_the_months_after_this_one_are_never_named(db, account):
    """TC-59, US12 criterion 2 and BR12: November and December have nothing yet."""
    add(db, account.id, 900_000, date(2026, 9, 1))
    add(db, account.id, 50_000, TODAY)

    trend = months(db, account.id)

    future = [p for p in trend.periods if p.period in ("2026-11", "2026-12")]
    assert [(p.spending, p.count) for p in future] == [(0, 0), (0, 0)]
    assert trend.quietest == "2026-10"


def test_tc60_a_tie_goes_to_the_earlier_month(db, account):
    """TC-60, US12 criterion 3 and BR12's example: February and March, 900,000 each."""
    add(db, account.id, 900_000, date(2026, 2, 10))
    add(db, account.id, 900_000, date(2026, 3, 10))
    add(db, account.id, 2_931_000, date(2026, 10, 3))

    trend = months(db, account.id)

    assert (trend.busiest, trend.quietest) == ("2026-10", "2026-02")


def test_tc61_a_month_with_no_entries_is_never_the_quietest(db, account):
    """BR12: January has no entries, so it is not the month with the least spent, even at 0."""
    add(db, account.id, 4_000_000, date(2026, 2, 1), "Salary")
    add(db, account.id, 500_000, date(2026, 3, 1))

    trend = months(db, account.id)

    assert trend.quietest == "2026-02"


def test_tc62_31_december_and_1_january_fall_in_different_years(db, account):
    """TC-62, US12 criterion 4."""
    add(db, account.id, 10_000, date(2025, 12, 31))
    add(db, account.id, 20_000, date(2026, 1, 1))

    trend = stats_service.by_year(db, account.id)

    assert spending_of(trend) == {"2025": 10_000, "2026": 20_000}
    assert (trend.busiest, trend.quietest) == ("2026", "2025")


@pytest.mark.parametrize(
    ("year", "allowed"),
    [("2026", True), ("2027", False)],  # TC-63 this year, and the year after
    ids=["TC-63 2026 this year", "TC-63 2027 next year"],
)
def test_tc63_a_year_later_than_this_one_is_refused(db, account, year, allowed):
    """US12 criterion 5 and BR12, both sides of this year."""
    if allowed:
        assert months(db, account.id, year).periods[0].period == "2026-01"
    else:
        with pytest.raises(RuleBroken, match="The year cannot be in the future"):
            months(db, account.id, year)


@pytest.mark.parametrize("year", ["26", "20266", "abcd"])
def test_tc64_a_year_not_written_yyyy_is_malformed(db, account, year):
    with pytest.raises(NotUnderstood, match="Year must be written YYYY"):
        months(db, account.id, year)


def test_tc65_a_year_with_no_entries_names_no_month(db, account):
    """TC-65, US12 criterion 6: every month is 0, so the app says "No entries in this year"."""
    trend = months(db, account.id, "2025")

    assert all(period.count == 0 for period in trend.periods)
    assert (trend.busiest, trend.quietest) == (None, None)


def test_another_accounts_spending_is_never_in_the_charts(db, account):
    """BR4."""
    stranger = make_account(db, email="stranger@example.com")
    add(db, stranger.id, 9_000_000, TODAY)

    assert spending_of(months(db, account.id)) == {}
    assert stats_service.breakdown(db, account.id, month="2026-10").total == 0
    assert stats_service.by_year(db, account.id).periods == []


def test_the_routes_answer_200_400_and_422(client, auth_headers):
    """The HTTP side once each: the status codes and the error codes."""
    assert client.get("/api/stats/breakdown", headers=auth_headers).status_code == 200
    assert client.get("/api/stats/years", headers=auth_headers).json()["periods"] == []
    this_year = client.get("/api/stats/months", headers=auth_headers).json()
    assert this_year["periods"][0]["period"] == f"{date.today().year}-01"

    malformed = client.get("/api/stats/months?year=26", headers=auth_headers)
    assert malformed.status_code == 400
    assert malformed.json()["code"] == "invalid_year"
    future = client.get(f"/api/stats/months?year={date.today().year + 1}", headers=auth_headers)
    assert future.status_code == 422
    assert future.json() == {"detail": "The year cannot be in the future", "code": "year_in_future"}
    bad_month = client.get("/api/stats/breakdown?month=2026-13", headers=auth_headers)
    assert bad_month.json()["code"] == "invalid_month"


def test_the_charts_need_a_sign_in(client):
    assert client.get("/api/stats/months").status_code == 401
