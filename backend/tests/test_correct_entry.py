"""Correcting or removing an entry: US06, with BR4, BR5 and BR11.

Test cases TC-46 to TC-52 of docs/testing.md, section 2; the ID is in each test's name. The rules
are tested on the service, with today fixed at 12/11/2026, and the routes once each for their
status codes.
"""

from datetime import date

import pytest

from app.db.repositories import category_repo, transaction_repo
from app.services import summary_service, transaction_service
from app.services.errors import NotFound, RuleBroken
from tests.conftest import make_account

TODAY = date(2026, 11, 12)


def add(db, user_id: int, amount: int, on: date = TODAY):
    return transaction_repo.create(
        db,
        user_id=user_id,
        kind="expense",
        amount=amount,
        note="ao khoac",
        occurred_on=on,
        category_id=category_repo.get_by_name(db, "Food").id,
    )


def correct(db, user_id: int, entry_id: int, **fields):
    body = {"kind": "expense", "amount": 50_000, "note": "ao khoac", "occurred_on": TODAY}
    return transaction_service.correct_entry(
        db, user_id, entry_id, **{**body, **fields}, today=TODAY
    )


def spent_in_november(db, user_id: int) -> int:
    return summary_service.month_summary(db, user_id, month="2026-11").spending


def test_tc46_correcting_150000_to_50000_spends_exactly_100000_less(db, account):
    """US06, criterion 1."""
    entry = add(db, account.id, 150_000)
    before = spent_in_november(db, account.id)

    correct(db, account.id, entry.id, amount=50_000)

    assert spent_in_november(db, account.id) == before - 100_000


def test_tc47_a_removed_entry_is_gone_and_no_longer_counted(db, account):
    """US06, criterion 2: after "Delete this entry?" and Delete."""
    kept = add(db, account.id, 30_000)
    removed = add(db, account.id, 150_000)

    transaction_service.remove_entry(db, account.id, removed.id)

    entries, total = transaction_service.list_recent(db, account.id)
    assert (total, [entry.id for entry in entries]) == (1, [kept.id])
    assert spent_in_november(db, account.id) == 30_000


def test_tc48_another_accounts_entry_is_not_found(db, account):
    """US06, criterion 3 and BR4: not "forbidden", which would confirm that the id exists."""
    stranger = make_account(db, email="stranger@example.com")
    theirs = add(db, stranger.id, 150_000)

    for act in (
        lambda: transaction_service.get_entry(db, account.id, theirs.id),
        lambda: correct(db, account.id, theirs.id, amount=1_000),
        lambda: transaction_service.remove_entry(db, account.id, theirs.id),
    ):
        with pytest.raises(NotFound, match="Entry not found"):
            act()
    assert transaction_repo.get_for_account(db, stranger.id, theirs.id).amount == 150_000


def test_tc49_an_id_that_does_not_exist_is_not_found(db, account):
    with pytest.raises(NotFound) as refused:
        transaction_service.get_entry(db, account.id, 999)

    assert refused.value.code == "entry_not_found"


@pytest.mark.parametrize("amount", [0, None], ids=["zero", "empty"])
def test_tc50_a_correction_to_no_amount_is_refused_and_nothing_changes(db, account, amount):
    """BR5 holds for a correction as for a new entry."""
    entry = add(db, account.id, 150_000)

    with pytest.raises(RuleBroken, match="Enter an amount greater than 0"):
        correct(db, account.id, entry.id, amount=amount)

    assert transaction_repo.get_for_account(db, account.id, entry.id).amount == 150_000


@pytest.mark.parametrize(
    ("occurred_on", "accepted"),
    [
        (date(2026, 11, 12), True),  # TC-51 today
        (date(2026, 11, 13), False),  # TC-52 tomorrow
    ],
    ids=["TC-51 today", "TC-52 tomorrow"],
)
def test_tc51_tc52_a_corrected_date_is_today_at_the_latest(db, account, occurred_on, accepted):
    """BR11, both sides of today."""
    entry = add(db, account.id, 150_000, on=date(2026, 11, 10))

    if accepted:
        assert correct(db, account.id, entry.id, occurred_on=occurred_on).occurred_on == occurred_on
    else:
        with pytest.raises(RuleBroken, match="The date cannot be in the future"):
            correct(db, account.id, entry.id, occurred_on=occurred_on)
        stored = transaction_repo.get_for_account(db, account.id, entry.id)
        assert stored.occurred_on == date(2026, 11, 10)


def test_the_routes_answer_200_204_and_404(client, db, account, auth_headers):
    """The HTTP side once: read, correct, remove, then the id is gone."""
    entry = add(db, account.id, 150_000, on=date.today())
    path = f"/api/transactions/{entry.id}"
    body = {"kind": "expense", "amount": 50_000, "note": "ao khoac"}

    assert client.get(path, headers=auth_headers).json()["amount"] == 150_000
    corrected = client.patch(path, json=body, headers=auth_headers)
    assert (corrected.status_code, corrected.json()["amount"]) == (200, 50_000)
    assert client.delete(path, headers=auth_headers).status_code == 204
    gone = client.get(path, headers=auth_headers)
    assert gone.status_code == 404
    assert gone.json() == {"detail": "Entry not found", "code": "entry_not_found"}


def test_a_correction_that_breaks_a_rule_answers_422(client, db, account, auth_headers):
    entry = add(db, account.id, 150_000, on=date.today())

    response = client.patch(
        f"/api/transactions/{entry.id}",
        json={"kind": "expense", "amount": -20_000},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert response.json()["code"] == "amount_not_positive"


def test_correcting_needs_a_sign_in(client, db, account):
    entry = add(db, account.id, 150_000)

    assert client.delete(f"/api/transactions/{entry.id}").status_code == 401
