"""The rules the database itself enforces: BR1, BR4, BR5, BR7 and BR13.

These go straight to the tables, without the API, so a rule still holds if a future endpoint
forgets to check it.
"""

from datetime import date

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.db.models import Budget, Debt, Transaction
from app.db.repositories import category_repo
from tests.conftest import make_account


def test_the_same_address_in_capitals_cannot_make_a_second_account(db):
    """BR1: TUAN@X.COM is registered, so tuan@x.com is taken."""
    make_account(db, email="TUAN@X.COM")

    with pytest.raises(IntegrityError):
        make_account(db, email="tuan@x.com")


def test_an_address_is_never_stored_in_capitals(db):
    """BR1: the CHECK constraint refuses capitals even when the repository is bypassed."""
    with pytest.raises(IntegrityError):
        db.execute(
            text("INSERT INTO users (email, password_hash) VALUES ('Tuan@X.com', 'x')")
        )


@pytest.mark.parametrize("amount", [0, -20_000])
def test_an_amount_must_be_greater_than_zero(db, account, amount):
    """BR5: 0 and -20,000 are refused."""
    db.add(
        Transaction(
            user_id=account.id, kind="expense", amount=amount, note="", occurred_on=date.today()
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()


def test_an_entry_must_belong_to_an_existing_account(db):
    """BR4: an entry always has an owner, so it cannot point at an account that does not exist."""
    db.add(
        Transaction(user_id=999, kind="expense", amount=1_000, note="", occurred_on=date.today())
    )
    with pytest.raises(IntegrityError):
        db.commit()


def test_there_is_one_cap_per_account_kind_of_spending_and_month(db, account):
    """BR7: a second food cap for 11/2026 is refused; one for 12/2026 is fine."""
    food = category_repo.get_by_name(db, "Food")
    db.add(Budget(user_id=account.id, category_id=food.id, month="2026-11", amount=3_000_000))
    db.add(Budget(user_id=account.id, category_id=food.id, month="2026-12", amount=3_000_000))
    db.commit()

    db.add(Budget(user_id=account.id, category_id=food.id, month="2026-11", amount=2_000_000))
    with pytest.raises(IntegrityError):
        db.commit()


def debt(account, **fields) -> Debt:
    values = {"direction": "lent", "person": "Lan", "amount": 200_000}
    values["started_on"] = date(2026, 11, 12)
    return Debt(user_id=account.id, **{**values, **fields})


@pytest.mark.parametrize(
    "fields",
    [
        {"due_on": date(2026, 11, 11)},
        {"person": ""},
        {"person": "x" * 61},
        {"amount": 0},
        {"direction": "given"},
    ],
    ids=["due before start", "no name", "61-character name", "amount 0", "unknown direction"],
)
def test_a_debt_that_breaks_br13_cannot_be_stored(db, account, fields):
    """BR13 and BR5 hold in the table itself, even if a future endpoint forgets to check."""
    db.add(debt(account, **fields))
    with pytest.raises(IntegrityError):
        db.commit()


def test_a_debt_due_the_day_it_started_can_be_stored(db, account):
    """BR13: the same day is the edge that is still allowed."""
    db.add(debt(account, due_on=date(2026, 11, 12), person="x" * 60))
    db.commit()
