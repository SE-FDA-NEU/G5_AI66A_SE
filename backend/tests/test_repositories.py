"""The queries in app/db/repositories, run on a database in memory, without the API.

A repository only reads and writes rows. These tests check the SQL: which rows a query finds,
and that every query keeps to one account (BR4).
"""

from datetime import date

from app.db.repositories import category_repo, debt_repo, transaction_repo
from app.db.repositories.debt_repo import OpenTotals
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


def test_spending_is_added_up_per_kind_biggest_first(db, account):
    """US10: money received and other months are left out; no kind chosen counts as one group."""
    transport = category_repo.get_by_name(db, "Transport")
    add(db, account.id, 30_000)
    add(db, account.id, 25_000)
    transaction_repo.create(
        db, user_id=account.id, kind="expense", amount=70_000, note="grab",
        occurred_on=DAY, category_id=transport.id,
    )
    transaction_repo.create(
        db, user_id=account.id, kind="expense", amount=5_000, note="",
        occurred_on=DAY, category_id=None,
    )
    add(db, account.id, 4_000_000, kind="income")
    add(db, account.id, 99_000, on=date(2026, 10, 31))

    rows = transaction_repo.spending_by_category(
        db, account.id, first_day=date(2026, 11, 1), last_day=date(2026, 11, 30)
    )

    assert [(c.name if c else None, amount) for c, amount in rows] == [
        ("Transport", 70_000),
        ("Food", 55_000),
        (None, 5_000),
    ]


def test_totals_by_month_keep_the_months_of_one_year_apart(db, account):
    """US12: 31/12/2025 belongs to 2025, 01/01/2026 to 2026."""
    add(db, account.id, 10_000, on=date(2025, 12, 31))
    add(db, account.id, 20_000, on=date(2026, 1, 1))
    add(db, account.id, 30_000, on=date(2026, 1, 31))
    add(db, account.id, 4_000_000, kind="income", on=date(2026, 2, 1))

    months = transaction_repo.totals_by_month(db, account.id, year=2026)

    assert sorted(months) == [1, 2]
    assert (months[1].spending, months[1].count) == (50_000, 2)
    assert (months[2].income, months[2].spending) == (4_000_000, 0)


def test_totals_by_year_and_month_keep_to_one_account(db, account):
    """BR4: a stranger's entries are in neither total."""
    stranger = make_account(db, email="stranger@example.com")
    add(db, stranger.id, 10_000, on=date(2025, 6, 1))
    add(db, account.id, 20_000, on=date(2026, 6, 1))

    years = transaction_repo.totals_by_year(db, account.id)

    assert {year: totals.spending for year, totals in years.items()} == {2026: 20_000}
    assert transaction_repo.totals_by_month(db, account.id, year=2025) == {}


def lend(db, user_id: int, amount: int = 200_000, **fields):
    values = {"direction": "lent", "person": "Lan", "note": "", "started_on": DAY, "due_on": None}
    return debt_repo.create(db, user_id=user_id, amount=amount, **{**values, **fields})


def test_open_debts_come_first_the_soonest_due_first(db, account):
    """US13: what to pay back next is at the top; settled debts sink to the bottom."""
    no_date = lend(db, account.id, person="Minh")
    later = lend(db, account.id, person="Lan", due_on=date(2026, 12, 1))
    sooner = lend(db, account.id, person="Hoa", due_on=date(2026, 11, 20))
    settled = lend(db, account.id, person="Nam", due_on=date(2026, 11, 13))
    debt_repo.settle(db, settled, on=DAY)

    listed = debt_repo.list_for_account(db, account.id)

    assert [debt.id for debt in listed] == [sooner.id, later.id, no_date.id, settled.id]


def test_open_totals_add_up_each_direction_and_skip_settled_debts(db, account):
    lend(db, account.id, 200_000)
    lend(db, account.id, 500_000, direction="borrowed", person="Minh")
    paid = lend(db, account.id, 300_000, direction="borrowed", person="Nam")
    debt_repo.settle(db, paid, on=DAY)

    assert debt_repo.open_totals(db, account.id) == OpenTotals(owe=500_000, owed=200_000)


def test_another_accounts_debt_is_neither_found_nor_counted(db, account):
    """BR4."""
    stranger = make_account(db, email="stranger@example.com")
    theirs = lend(db, stranger.id, 900_000)

    assert debt_repo.get_for_account(db, account.id, theirs.id) is None
    assert debt_repo.list_for_account(db, account.id) == []
    assert debt_repo.open_totals(db, account.id) == OpenTotals(owe=0, owed=0)
