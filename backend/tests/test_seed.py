"""The seed script: row counts, running twice, --reset, BR11, and the demo of every screen."""

from datetime import date

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.models import Transaction, User
from app.db.session import make_engine
from app.services import debt_service, stats_service, summary_service
from scripts.seed_data import DEMO_EMAIL, DEMO_PASSWORD, RowCounts, seed

EXPECTED = RowCounts(categories=11, users=1, transactions=91, budgets=0, debts=4)


@pytest.fixture()
def database_url(tmp_path) -> str:
    return f"sqlite:///{(tmp_path / 'seed.db').as_posix()}"


def test_one_command_creates_and_fills_the_database(database_url):
    assert seed(database_url) == EXPECTED


def test_running_it_twice_adds_nothing(database_url):
    seed(database_url)

    assert seed(database_url) == EXPECTED


def test_reset_starts_again(database_url):
    seed(database_url)

    assert seed(database_url, reset=True) == EXPECTED


def test_no_entry_is_dated_later_than_today(database_url):
    """BR11. The seed runs as if today were 12/11/2026."""
    seed(database_url, today=date(2026, 11, 12))

    engine = make_engine(database_url)
    with Session(engine) as db:
        newest = db.scalar(select(func.max(Transaction.occurred_on)))
        oldest = db.scalar(select(func.min(Transaction.occurred_on)))
    engine.dispose()
    assert newest == date(2026, 11, 12)
    assert oldest == date(2025, 12, 2)


def test_the_demo_account_can_sign_in(database_url):
    seed(database_url)

    engine = make_engine(database_url)
    with Session(engine) as db:
        account = db.scalar(select(User).where(User.email == DEMO_EMAIL))
    engine.dispose()
    assert verify_password(DEMO_PASSWORD, account.password_hash)


def open_seeded(database_url):
    engine = make_engine(database_url)
    db = Session(engine)
    account = db.scalar(select(User).where(User.email == DEMO_EMAIL))
    return engine, db, account


@pytest.mark.parametrize("today", [date(2026, 11, 1), date(2026, 11, 3), date(2026, 11, 30)])
def test_this_months_25_entries_fall_in_the_month_the_seed_runs(database_url, today):
    """US04 totals this month only, so the demo must show the same month on any day."""
    seed(database_url, today=today)

    engine, db, account = open_seeded(database_url)
    month = summary_service.month_summary(db, account.id, today=today)
    db.close()
    engine.dispose()
    assert (month.count, month.income, month.spending) == (25, 4_000_000, 2_931_000)


@pytest.mark.parametrize("today", [date(2026, 1, 15), date(2026, 10, 24)])
def test_the_eleven_months_before_give_stats_a_whole_year(database_url, today):
    """US12: twelve months with entries, back across new year when the seed runs in January."""
    seed(database_url, today=today)

    engine, db, account = open_seeded(database_url)
    years = stats_service.by_year(db, account.id)
    months_with_entries = 0
    for year in years.periods:
        trend = stats_service.by_month(db, account.id, year=year.period, today=today)
        months_with_entries += sum(1 for period in trend.periods if period.count)
    db.close()
    engine.dispose()
    assert months_with_entries == 12
    assert years.busiest is not None


def test_the_four_debts_owe_500000_overdue_and_are_owed_350000(database_url):
    """US13: one overdue debt, one open, one with no due date, one settled; BR13 holds."""
    today = date(2026, 10, 24)
    seed(database_url, today=today)

    engine, db, account = open_seeded(database_url)
    debts = debt_service.list_debts(db, account.id, today=today)
    db.close()
    engine.dispose()
    assert (debts.owe, debts.owed) == (500_000, 350_000)
    overdue = [view.debt.person for view in debts.items if view.overdue]
    assert overdue == ["anh Minh"]
    for view in debts.items:
        assert view.debt.started_on <= today
        assert view.debt.due_on is None or view.debt.due_on >= view.debt.started_on
