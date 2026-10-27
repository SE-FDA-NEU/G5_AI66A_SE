"""This month's position: US04 and BR4. Also the list of categories behind the form (US03).

Test cases TC-31 to TC-38 of docs/testing.md, section 2; the ID is in each test's name.
"""

from datetime import date, timedelta

import pytest

from app.db.repositories import category_repo, transaction_repo
from app.services import summary_service
from tests.conftest import make_account


def add(db, user_id: int, kind: str, amount: int, occurred_on: date | None = None) -> None:
    name = "Salary" if kind == "income" else "Food"
    transaction_repo.create(
        db,
        user_id=user_id,
        kind=kind,
        amount=amount,
        note="",
        occurred_on=occurred_on or date.today(),
        category_id=category_repo.get_by_name(db, name).id,
    )


def summary(client, headers, **params):
    return client.get("/api/summary", headers=headers, params=params)


def test_tc31_income_spending_and_what_is_left(client, db, account, auth_headers):
    """TC-31, US04 criterion 1: 4,000,000 in, 55,000 and 150,000 out, 3,795,000 left."""
    add(db, account.id, "income", 4_000_000)
    add(db, account.id, "expense", 55_000)
    add(db, account.id, "expense", 150_000)

    response = summary(client, auth_headers)

    assert response.status_code == 200
    assert response.json() == {
        "month": date.today().strftime("%Y-%m"),
        "income": 4_000_000,
        "spending": 205_000,
        "remaining": 3_795_000,
        "count": 3,
    }


def test_tc32_saving_30000_leaves_30000_less(client, db, account, auth_headers):
    """TC-32, US04 criterion 2: 3,795,000 left, an entry of 30,000 saved, 3,765,000 left."""
    add(db, account.id, "income", 4_000_000)
    add(db, account.id, "expense", 205_000)

    client.post(
        "/api/transactions", json={"kind": "expense", "amount": 30_000}, headers=auth_headers
    )

    assert summary(client, auth_headers).json()["remaining"] == 3_765_000


def test_tc33_an_empty_month_counts_0_entries(client, auth_headers):
    """TC-33, US04 criterion 3: count 0 lets the app say "No transactions yet this month"."""
    assert summary(client, auth_headers).json() == {
        "month": date.today().strftime("%Y-%m"),
        "income": 0,
        "spending": 0,
        "remaining": 0,
        "count": 0,
    }


@pytest.mark.parametrize(
    ("occurred_on", "counted"),
    [
        (date(2026, 10, 31), False),  # TC-34 the day before the month
        (date(2026, 11, 1), True),  # TC-35 the first day
        (date(2026, 11, 30), True),  # TC-36 the last day
        (date(2026, 12, 1), False),  # TC-36 the day after
    ],
    ids=["TC-34 31/10", "TC-35 01/11", "TC-36 30/11", "TC-36 01/12"],
)
def test_tc34_to_tc36_a_month_runs_from_its_1st_to_its_last_day(db, account, occurred_on, counted):
    """US04 counts 11/2026 from 01/11 to 30/11, both included: both edges, from both sides."""
    add(db, account.id, "expense", 99_000, occurred_on=occurred_on)

    month = summary_service.month_summary(db, account.id, month="2026-11")

    assert month.spending == (99_000 if counted else 0)
    assert month.count == (1 if counted else 0)


def test_this_month_is_the_month_of_today(db, account):
    """No month asked for means the month today is in."""
    add(db, account.id, "expense", 99_000, occurred_on=date(2026, 11, 30))

    month = summary_service.month_summary(db, account.id, today=date(2026, 11, 12))

    assert (month.month, month.spending) == ("2026-11", 99_000)


def test_last_month_is_left_out(client, db, account, auth_headers):
    last_month = date.today().replace(day=1) - timedelta(days=1)
    add(db, account.id, "expense", 99_000, occurred_on=last_month)

    assert summary(client, auth_headers).json()["count"] == 0
    earlier = summary(client, auth_headers, month=last_month.strftime("%Y-%m")).json()
    assert earlier["spending"] == 99_000


def test_more_spent_than_received_leaves_a_negative_remainder(client, db, account, auth_headers):
    add(db, account.id, "expense", 120_000)

    assert summary(client, auth_headers).json()["remaining"] == -120_000


def test_tc38_another_accounts_entries_never_count(client, db, account, auth_headers):
    """TC-38, BR4: only the signed-in account's entries are added up."""
    stranger = make_account(db, email="stranger@example.com")
    add(db, stranger.id, "income", 9_000_000)

    assert summary(client, auth_headers).json()["income"] == 0


@pytest.mark.parametrize("month", ["11/2026", "2026-13", "2026-1"])
def test_tc37_a_month_not_written_yyyy_mm_gets_400(client, auth_headers, month):
    """TC-37: a month the API cannot read is refused, never guessed."""
    response = summary(client, auth_headers, month=month)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Month must be written YYYY-MM",
        "code": "invalid_month",
    }


def test_the_summary_needs_a_sign_in(client):
    assert client.get("/api/summary").json()["code"] == "sign_in_again"


def test_categories_list_spending_first(client, auth_headers):
    """The picker on /transactions/new: the conftest seeds Food, Transport and Salary."""
    response = client.get("/api/categories", headers=auth_headers)

    assert response.status_code == 200
    assert [(c["name"], c["kind"]) for c in response.json()] == [
        ("Food", "expense"),
        ("Transport", "expense"),
        ("Salary", "income"),
    ]


def test_categories_need_a_sign_in(client):
    assert client.get("/api/categories").status_code == 401
