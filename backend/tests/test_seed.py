"""The seed script: row counts, running twice, --reset, and BR11."""

from datetime import date

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.models import Transaction, User
from app.db.session import make_engine
from scripts.seed_data import DEMO_EMAIL, DEMO_PASSWORD, RowCounts, seed

EXPECTED = RowCounts(categories=11, users=1, transactions=25, budgets=0)


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
    assert oldest == date(2026, 10, 31)


def test_the_demo_account_can_sign_in(database_url):
    seed(database_url)

    engine = make_engine(database_url)
    with Session(engine) as db:
        account = db.scalar(select(User).where(User.email == DEMO_EMAIL))
    engine.dispose()
    assert verify_password(DEMO_PASSWORD, account.password_hash)
