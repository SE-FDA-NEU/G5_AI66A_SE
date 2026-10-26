"""Logging an entry: US03, BR5, BR6 and BR11."""

from datetime import date, timedelta

import pytest
from sqlalchemy import func, select

from app.db.models import Transaction
from app.db.repositories import category_repo


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


def test_55000_on_food_adds_exactly_55000_to_spending(client, db, auth_headers):
    """US03, criterion 2."""
    food = category_repo.get_by_name(db, "Food")
    before = spent_this_month(client, auth_headers)

    log(client, auth_headers, category_id=food.id)

    assert spent_this_month(client, auth_headers) == before + 55_000
    listed = client.get("/api/transactions", headers=auth_headers).json()["items"][0]
    assert listed["category"]["name"] == "Food"


def test_money_received_adds_to_income_only(client, db, auth_headers):
    """US03, criterion 3."""
    salary = category_repo.get_by_name(db, "Salary")

    log(client, auth_headers, kind="income", amount=4_000_000, category_id=salary.id)

    summary = client.get("/api/summary", headers=auth_headers).json()
    assert summary["income"] == 4_000_000
    assert summary["spending"] == 0


@pytest.mark.parametrize("amount", [None, 0, -20_000], ids=["empty", "zero", "negative"])
def test_an_amount_that_is_not_above_0_is_refused(client, db, auth_headers, amount):
    """US03, criterion 4 and BR5: nothing is stored."""
    response = log(client, auth_headers, amount=amount)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Enter an amount greater than 0",
        "code": "amount_not_positive",
    }
    assert count_entries(db) == 0


def test_a_fraction_of_a_dong_is_malformed(client, db, auth_headers):
    """BR5: VND has no subunit in use, so 55,000.50 is not an amount at all."""
    response = log(client, auth_headers, amount=55_000.5)

    assert response.status_code == 400
    assert response.json()["code"] == "invalid_request"
    assert count_entries(db) == 0


def test_a_date_after_today_is_refused(client, db, auth_headers):
    """US03, criterion 5 and BR11."""
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
def test_a_kind_of_spending_not_on_the_list_is_refused(client, db, auth_headers, which):
    """BR6: one from the list, and of the same kind as the entry."""
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


@pytest.mark.parametrize(
    ("amount", "status"),
    [
        (1_000_000_000_000, 201),
        (1_000_000_000_001, 422),
        (9_223_372_036_854_775_808, 422),
    ],
    ids=["on the limit", "one dong above", "above what SQLite stores"],
)
def test_an_amount_above_one_trillion_is_refused(client, db, auth_headers, amount, status):
    """BR5's upper limit. Regression test for bug #142: the last amount answered 500."""
    response = log(client, auth_headers, amount=amount)

    assert response.status_code == status
    if status == 422:
        assert response.json() == {
            "detail": "Enter an amount of at most 1,000,000,000,000",
            "code": "amount_too_large",
        }
        assert count_entries(db) == 0


def test_the_month_still_adds_up_after_the_largest_entries(client, auth_headers):
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
