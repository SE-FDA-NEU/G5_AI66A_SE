"""Creating an account: US01, BR1 and BR2.

Test cases TC-01 to TC-08 of docs/testing.md, section 2; the ID is in each test's name or row.
"""

import pytest
from sqlalchemy import func, select

from app.db.models import User
from tests.conftest import DEMO_EMAIL


def register(client, email: str, secret: str):
    return client.post("/api/users", json={"email": email, "password": secret})


def count_accounts(db) -> int:
    return db.scalar(select(func.count()).select_from(User))


def test_tc01_a_new_account_is_signed_in_at_once(client, db):
    """TC-01, US01 criterion 1: the answer carries a token, so there is no second sign-in."""
    response = register(client, "hoa@example.com", "abcd1234")

    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "hoa@example.com"
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "hoa@example.com"


def test_the_new_account_can_sign_in_later(client):
    register(client, "hoa@example.com", "abcd1234")

    response = client.post(
        "/api/auth/login", json={"email": "hoa@example.com", "password": "abcd1234"}
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "email",
    [DEMO_EMAIL, DEMO_EMAIL.upper()],
    ids=["TC-02 the same address", "TC-03 the same address in capitals"],
)
def test_tc02_tc03_an_address_already_registered_is_refused(client, db, account, email):
    """US01 criterion 2 and BR1: no second account, whatever the capitals."""
    response = register(client, email, "abcd1234")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "This email is already registered",
        "code": "email_taken",
    }
    assert count_accounts(db) == 1


@pytest.mark.parametrize(
    ("length", "accepted"),
    [
        (5, False),  # TC-04 just below the lower limit
        (6, True),  # TC-05 on the lower limit
        (128, True),  # TC-06 on the upper limit
        (129, False),  # TC-07 just above the upper limit
    ],
    ids=["TC-04 5 chars", "TC-05 6 chars", "TC-06 128 chars", "TC-07 129 chars"],
)
def test_tc04_to_tc07_a_password_has_6_to_128_characters(client, db, length, accepted):
    """US01 criterion 3 and BR2: both edges, from both sides. A refusal stores nothing."""
    response = register(client, "hoa@example.com", "a" * length)

    if accepted:
        assert response.status_code == 201
        assert count_accounts(db) == 1
    else:
        assert response.status_code == 422
        assert response.json() == {
            "detail": "Password must be 6 to 128 characters",
            "code": "password_length",
        }
        assert count_accounts(db) == 0


def test_the_password_is_stored_only_as_a_hash(client, db):
    """BR2: neither the database nor the answer contains the password."""
    response = register(client, "hoa@example.com", "abcd1234")

    stored = db.scalar(select(User).where(User.email == "hoa@example.com"))
    assert stored.password_hash.startswith("pbkdf2_sha256$")
    assert "abcd1234" not in stored.password_hash
    assert "abcd1234" not in response.text


def test_capitals_are_stored_in_lower_case(client):
    """BR1: Hoa@Example.com is stored as hoa@example.com."""
    response = register(client, "Hoa@Example.com", "abcd1234")

    assert response.json()["user"]["email"] == "hoa@example.com"


@pytest.mark.parametrize("email", ["hoa", "hoa@example", "@example.com", "hoa @example.com"])
def test_tc08_an_address_that_is_not_one_gets_400(client, db, email):
    """TC-08: a malformed address is the caller's mistake, 400, not a broken rule."""
    response = register(client, email, "abcd1234")

    assert response.status_code == 400
    assert response.json() == {"detail": "Enter a valid email address", "code": "invalid_email"}
    assert count_accounts(db) == 0
