"""Debts and loans: US13, with BR4, BR5, BR11, BR13 and BR14.

Test cases TC-66 to TC-78 of docs/testing.md, section 2; the ID is in each test's name or row. The
rules are tested on the service with today fixed at 24/10/2026, and the routes once each.
"""

from datetime import date, timedelta

import pytest
from sqlalchemy import func, select

from app.db.models import Debt
from app.services import debt_service, summary_service
from app.services.errors import AlreadyExists, NotFound, RuleBroken
from tests.conftest import make_account

TODAY = date(2026, 10, 24)
YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)


def add(db, user_id: int, **fields):
    values = {"direction": "lent", "person": "Lan", "amount": 200_000, "today": TODAY}
    return debt_service.add_debt(db, user_id, **{**values, **fields})


def debts(db, user_id: int, today: date = TODAY):
    return debt_service.list_debts(db, user_id, today=today)


def count_debts(db) -> int:
    return db.scalar(select(func.count()).select_from(Debt))


def test_tc66_lending_200000_to_lan_is_owed_to_you(db, account):
    """TC-66, US13 criterion 1."""
    before = debts(db, account.id).owed

    add(db, account.id, due_on=TODAY + timedelta(days=10))

    listed = debts(db, account.id)
    assert listed.owed == before + 200_000
    assert listed.owe == 0
    assert listed.items[0].debt.settled_on is None


def test_tc67_settling_500000_borrowed_owes_exactly_500000_less(db, account):
    """TC-67, US13 criterion 2."""
    borrowed = add(db, account.id, direction="borrowed", person="Minh", amount=500_000)
    assert debts(db, account.id).owe == 500_000

    settled = debt_service.settle_debt(db, account.id, borrowed.debt.id, today=TODAY)

    assert settled.debt.settled_on == TODAY
    assert debts(db, account.id).owe == 0


def test_tc68_a_debt_cannot_be_settled_twice(db, account):
    """TC-68, US13 criterion 2 and BR14: the first day it was settled is kept."""
    borrowed = add(db, account.id, direction="borrowed", person="Minh", amount=500_000)
    debt_service.settle_debt(db, account.id, borrowed.debt.id, today=YESTERDAY)

    with pytest.raises(AlreadyExists, match="This debt is already settled"):
        debt_service.settle_debt(db, account.id, borrowed.debt.id, today=TODAY)

    assert borrowed.debt.settled_on == YESTERDAY


@pytest.mark.parametrize(
    ("due_on", "overdue"),
    [
        (YESTERDAY, True),  # TC-69 due yesterday: overdue
        (TODAY, False),  # TC-70 due today: not yet
        (TOMORROW, False),  # TC-70 due tomorrow
        (None, False),  # TC-70 no due date: never overdue
    ],
    ids=["TC-69 due yesterday", "TC-70 due today", "TC-70 due tomorrow", "TC-70 no due date"],
)
def test_tc69_tc70_an_open_debt_is_overdue_from_the_day_after_it_is_due(
    db, account, due_on, overdue
):
    """US13 criterion 3 and BR14, both sides of the due date."""
    add(db, account.id, started_on=TODAY - timedelta(days=20), due_on=due_on)

    assert debts(db, account.id).items[0].overdue is overdue


def test_tc71_a_settled_debt_is_never_overdue(db, account):
    """BR14."""
    lent = add(db, account.id, started_on=TODAY - timedelta(days=20), due_on=YESTERDAY)
    debt_service.settle_debt(db, account.id, lent.debt.id, today=TODAY)

    assert debts(db, account.id, today=TODAY + timedelta(days=30)).items[0].overdue is False


@pytest.mark.parametrize(
    ("due_on", "accepted"),
    [
        (YESTERDAY, False),  # TC-72 one day before it started
        (TODAY, True),  # TC-73 the same day
    ],
    ids=["TC-72 due the day before", "TC-73 due the same day"],
)
def test_tc72_tc73_a_due_date_is_not_before_the_start(db, account, due_on, accepted):
    """US13 criterion 4 and BR13, both sides of the day it started."""
    if accepted:
        assert add(db, account.id, started_on=TODAY, due_on=due_on).debt.due_on == due_on
    else:
        with pytest.raises(RuleBroken, match="The due date cannot be before the start date"):
            add(db, account.id, started_on=TODAY, due_on=due_on)
        assert count_debts(db) == 0


@pytest.mark.parametrize(
    ("person", "accepted"),
    [
        ("", False),  # TC-74 no name
        ("   ", False),  # TC-74 only spaces
        ("L", True),  # TC-74 one character
        ("x" * 60, True),  # TC-74 60 characters, on the limit
        ("x" * 61, False),  # TC-74 61 characters, just above it
    ],
    ids=["TC-74 empty", "TC-74 spaces", "TC-74 1 char", "TC-74 60 chars", "TC-74 61 chars"],
)
def test_tc74_a_name_has_1_to_60_characters(db, account, person, accepted):
    """US13 criterion 5 and BR13, both edges."""
    if accepted:
        assert add(db, account.id, person=person).debt.person == person
    else:
        with pytest.raises(RuleBroken, match="Write a name of 1 to 60 characters"):
            add(db, account.id, person=person)
        assert count_debts(db) == 0


@pytest.mark.parametrize("amount", [None, 0, -200_000, 1_000_000_000_001])
def test_tc75_a_debts_amount_follows_br5(db, account, amount):
    with pytest.raises(RuleBroken) as refused:
        add(db, account.id, amount=amount)

    assert refused.value.code in ("amount_not_positive", "amount_too_large")
    assert count_debts(db) == 0


@pytest.mark.parametrize(
    ("started_on", "accepted"),
    [(TODAY, True), (TOMORROW, False)],
    ids=["TC-76 started today", "TC-76 started tomorrow"],
)
def test_tc76_a_debt_started_today_at_the_latest(db, account, started_on, accepted):
    """BR11 for debts, both sides of today."""
    if accepted:
        assert add(db, account.id, started_on=started_on).debt.started_on == TODAY
    else:
        with pytest.raises(RuleBroken, match="The date cannot be in the future"):
            add(db, account.id, started_on=started_on)


def test_tc77_a_debt_does_not_change_the_months_totals(db, account):
    """US13 criterion 6: lending money is not spending it."""
    add(db, account.id, amount=200_000)
    add(db, account.id, direction="borrowed", person="Minh", amount=500_000)

    month = summary_service.month_summary(db, account.id, month="2026-10")

    assert (month.income, month.spending, month.count) == (0, 0, 0)


def test_tc78_another_accounts_debt_is_not_found(db, account):
    """US13 criterion 7 and BR4."""
    stranger = make_account(db, email="stranger@example.com")
    theirs = add(db, stranger.id)

    for act in (
        lambda: debt_service.settle_debt(db, account.id, theirs.debt.id, today=TODAY),
        lambda: debt_service.remove_debt(db, account.id, theirs.debt.id),
    ):
        with pytest.raises(NotFound, match="Debt not found"):
            act()
    assert debts(db, account.id).items == []
    assert debts(db, stranger.id).items[0].debt.settled_on is None


def test_the_routes_answer_201_200_409_204_and_404(client, auth_headers):
    """The HTTP side once: add, list, settle twice, remove."""
    created = client.post(
        "/api/debts",
        json={"direction": "borrowed", "person": "Minh", "amount": 500_000},
        headers=auth_headers,
    )
    assert created.status_code == 201
    debt = created.json()
    assert (debt["person"], debt["overdue"], debt["settled_on"]) == ("Minh", False, None)

    listed = client.get("/api/debts", headers=auth_headers).json()
    assert (listed["owe"], listed["owed"], len(listed["items"])) == (500_000, 0, 1)

    settle = f"/api/debts/{debt['id']}/settle"
    assert client.post(settle, headers=auth_headers).status_code == 200
    again = client.post(settle, headers=auth_headers)
    assert again.status_code == 409
    assert again.json() == {"detail": "This debt is already settled", "code": "already_settled"}

    assert client.delete(f"/api/debts/{debt['id']}", headers=auth_headers).status_code == 204
    gone = client.delete(f"/api/debts/{debt['id']}", headers=auth_headers)
    assert gone.json() == {"detail": "Debt not found", "code": "debt_not_found"}


def test_a_broken_rule_answers_422(client, auth_headers):
    response = client.post(
        "/api/debts",
        json={"direction": "lent", "person": "x" * 61, "amount": 200_000},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Write a name of 1 to 60 characters",
        "code": "person_length",
    }


def test_debts_need_a_sign_in(client):
    assert client.get("/api/debts").status_code == 401
