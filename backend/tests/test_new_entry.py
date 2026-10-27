"""Logging an entry: US03, BR5, BR6 and BR11.

Test cases TC-17 to TC-30 of docs/testing.md, section 2; the ID is in each test's name or row.
BR11 is tested on the service with today fixed at 12/11/2026, as in its acceptance criterion, so
the result never depends on the day the tests run.
"""

from datetime import date, timedelta

import pytest
from sqlalchemy import func, select

from app.db.models import Transaction
from app.db.repositories import category_repo
from app.services import transaction_service
from app.services.errors import RuleBroken

TODAY = date(2026, 11, 12)


def log(client, headers, **fields):
    body = {"kind": "expense", "amount": 55_000, "note": "tra sua", **fields}
    return client.post("/api/transactions", json=body, headers=headers)


def count_entries(db) -> int:
    return db.scalar(select(func.count()).select_from(Transaction))


def spent_this_month(client, headers) -> int:
    return client.get("/api/summary", headers=headers).json()["spending"]


def test_an_entry_is_stored_and_returned(client, db, auth_headers):
    food = category_repo.get_by_name(db, "Food")

    response = log(client, auth_headers, category_id=food.id)

    assert response.status_code == 201
    body = response.json()
    assert body["amount"] == 55_000
    assert body["note"] == "tra sua"
    assert body["kind"] == "expense"
    assert body["occurred_on"] == date.today().isoformat()
    assert body["category"] == {"id": food.id, "name": "Food", "kind": "expense"}


def test_tc17_55000_on_food_adds_exactly_55000_to_spending(client, db, auth_headers):
    """TC-17, US03 criterion 2."""
    food = category_repo.get_by_name(db, "Food")
    before = spent_this_month(client, auth_headers)

    log(client, auth_headers, category_id=food.id)

    assert spent_this_month(client, auth_headers) == before + 55_000
    listed = client.get("/api/transactions", headers=auth_headers).json()["items"][0]
    assert listed["category"]["name"] == "Food"


def test_tc18_money_received_adds_to_income_only(client, db, auth_headers):
    """TC-18, US03 criterion 3."""
    salary = category_repo.get_by_name(db, "Salary")

    log(client, auth_headers, kind="income", amount=4_000_000, category_id=salary.id)

    summary = client.get("/api/summary", headers=auth_headers).json()
    assert summary["income"] == 4_000_000
    assert summary["spending"] == 0


TOO_SMALL = ("Enter an amount greater than 0", "amount_not_positive")
TOO_LARGE = ("Enter an amount of at most 1,000,000,000,000", "amount_too_large")


@pytest.mark.parametrize(
    ("amount", "refused_with"),
    [
        (None, TOO_SMALL),  # TC-19 left empty
        (0, TOO_SMALL),  # TC-20 just below the lower limit
        (1, None),  # TC-21 the smallest amount
        (-20_000, TOO_SMALL),  # TC-22 negative
        (1_000_000_000_000, None),  # TC-24 on the upper limit
        (1_000_000_000_001, TOO_LARGE),  # TC-25 just above the upper limit
        (9_223_372_036_854_775_808, TOO_LARGE),  # TC-26 above what SQLite stores: was a 500
    ],
    ids=[
        "TC-19 empty",
        "TC-20 0",
        "TC-21 1",
        "TC-22 -20,000",
        "TC-24 1,000,000,000,000",
        "TC-25 1,000,000,000,001",
        "TC-26 2^63",
    ],
)
def test_tc19_to_tc26_an_amount_is_above_0_and_at_most_one_trillion(
    client, db, auth_headers, amount, refused_with
):
    """US03 criterion 4 and BR5, both limits from both sides. A refusal stores nothing.

    TC-26 is the regression test of bug #142: it answered 500 instead of a message.
    """
    response = log(client, auth_headers, amount=amount)

    if refused_with is None:
        assert response.status_code == 201
        assert response.json()["amount"] == amount
    else:
        detail, code = refused_with
        assert response.status_code == 422
        assert response.json() == {"detail": detail, "code": code}
        assert count_entries(db) == 0


def test_tc23_a_fraction_of_a_dong_is_malformed(client, db, auth_headers):
    """TC-23, BR5: VND has no subunit in use, so 55,000.50 is not an amount at all."""
    response = log(client, auth_headers, amount=55_000.5)

    assert response.status_code == 400
    assert response.json()["code"] == "invalid_request"
    assert count_entries(db) == 0


@pytest.mark.parametrize(
    ("occurred_on", "accepted"),
    [
        (date(2026, 11, 12), True),  # TC-27 today
        (date(2026, 11, 13), False),  # TC-28 tomorrow
        (date(2026, 10, 28), True),  # TC-29 last month, written down late
    ],
    ids=["TC-27 12/11 today", "TC-28 13/11 tomorrow", "TC-29 28/10 last month"],
)
def test_tc27_to_tc29_an_entry_is_dated_today_at_the_latest(db, account, occurred_on, accepted):
    """US03 criterion 5 and BR11, as the criterion says it: today is 12/11/2026."""

    def log_on_the_service():
        return transaction_service.log_entry(
            db, account.id, kind="expense", amount=55_000, occurred_on=occurred_on, today=TODAY
        )

    if accepted:
        assert log_on_the_service().occurred_on == occurred_on
    else:
        with pytest.raises(RuleBroken, match="The date cannot be in the future"):
            log_on_the_service()
        assert count_entries(db) == 0


def test_a_date_after_today_is_refused(client, db, auth_headers):
    """BR11 through the API: the 422 and its code, with the real today."""
    tomorrow = date.today() + timedelta(days=1)

    response = log(client, auth_headers, occurred_on=tomorrow.isoformat())

    assert response.status_code == 422
    assert response.json() == {
        "detail": "The date cannot be in the future",
        "code": "date_in_future",
    }
    assert count_entries(db) == 0


def test_today_and_last_month_are_accepted(client, auth_headers):
    """BR11: a purchase written down late is still recorded (Scenario 1, step 4)."""
    today = date.today()
    last_month = today.replace(day=1) - timedelta(days=3)

    assert log(client, auth_headers, occurred_on=today.isoformat()).status_code == 201
    assert log(client, auth_headers, occurred_on=last_month.isoformat()).status_code == 201


def test_no_kind_of_spending_is_allowed_and_nothing_is_guessed(client, auth_headers):
    """BR6: none chosen stays none, never the most common category."""
    response = log(client, auth_headers, category_id=None)

    assert response.status_code == 201
    assert response.json()["category"] is None


@pytest.mark.parametrize("which", ["unknown", "income for money spent"])
def test_tc30_a_kind_of_spending_not_on_the_list_is_refused(client, db, auth_headers, which):
    """TC-30, BR6: one from the list, and of the same kind as the entry."""
    category_id = 999 if which == "unknown" else category_repo.get_by_name(db, "Salary").id

    response = log(client, auth_headers, category_id=category_id)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Choose a kind of spending from the list",
        "code": "unknown_category",
    }
    assert count_entries(db) == 0


def test_the_note_is_kept_exactly_as_typed(client, auth_headers):
    response = log(client, auth_headers, note="  Tra Sua 50% duong  ")

    assert response.json()["note"] == "  Tra Sua 50% duong  "


def test_logging_needs_a_sign_in(client, db):
    response = client.post("/api/transactions", json={"kind": "expense", "amount": 55_000})

    assert response.status_code == 401
    assert response.json()["code"] == "sign_in_again"
    assert count_entries(db) == 0


def test_the_entry_belongs_to_the_account_that_logged_it(client, db, account, auth_headers):
    """BR4: the account comes from the token, never from the request."""
    log(client, auth_headers, user_id=999)

    assert db.scalar(select(Transaction.user_id)) == account.id


def test_tc26_the_month_still_adds_up_after_the_largest_entries(client, auth_headers):
    """Bug #142: after an entry of 9,223,372,036,854,775,807 the next one made /api/summary 500.

    Two of the largest entries allowed now leave the month's totals readable.
    """
    log(client, auth_headers, amount=1_000_000_000_000)
    log(client, auth_headers, amount=1_000_000_000_000)
    refused = log(client, auth_headers, amount=9_223_372_036_854_775_807)

    assert refused.status_code == 422
    response = client.get("/api/summary", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["spending"] == 2_000_000_000_000
