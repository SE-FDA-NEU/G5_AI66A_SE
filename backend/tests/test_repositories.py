"""The queries in app/db/repositories, run on a database in memory, without the API.

A repository only reads and writes rows. These tests check the SQL: which rows a query finds,
and that every query keeps to one account (BR4).
"""

from datetime import date

from app.db.repositories import category_repo, transaction_repo
from tests.conftest import make_account

DAY = date(2026, 11, 12)


def add(db, user_id: int, amount: int = 55_000, *, kind: str = "expense", on: date = DAY):
    category = category_repo.get_by_name(db, "Salary" if kind == "income" else "Food")
    return transaction_repo.create(
        db,
        user_id=user_id,
        kind=kind,
        amount=amount,
        note="tra sua",
        occurred_on=on,
        category_id=category.id,
    )


def test_an_account_finds_its_own_entry_by_id(db, account):
    entry = add(db, account.id)

    found = transaction_repo.get_for_account(db, account.id, entry.id)

    assert found.id == entry.id
    assert found.category.name == "Food"


def test_another_accounts_entry_is_not_found_by_id(db, account):
    """BR4: the id exists, but not for this account, so it is the same as no entry at all."""
    stranger = make_account(db, email="stranger@example.com")
    entry = add(db, stranger.id)

    assert transaction_repo.get_for_account(db, account.id, entry.id) is None
    assert transaction_repo.get_for_account(db, account.id, 999) is None


def test_update_replaces_what_the_entry_says(db, account):
    entry = add(db, account.id, 150_000)
    transport = category_repo.get_by_name(db, "Transport")

    transaction_repo.update(
        db,
        entry,
        kind="expense",
        amount=50_000,
        note="grab",
        occurred_on=date(2026, 11, 10),
        category_id=transport.id,
    )

    stored = transaction_repo.get_for_account(db, account.id, entry.id)
    assert (stored.amount, stored.note, stored.occurred_on) == (50_000, "grab", date(2026, 11, 10))
    assert stored.category.name == "Transport"


def test_delete_removes_only_that_entry(db, account):
    kept = add(db, account.id, 30_000)
    removed = add(db, account.id, 45_000)

    transaction_repo.delete(db, removed)

    entries, total = transaction_repo.list_recent(db, account.id, limit=20)
    assert total == 1
    assert [entry.id for entry in entries] == [kept.id]
