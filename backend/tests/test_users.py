"""Creating an account: US01, BR1 and BR2."""

import pytest
from sqlalchemy import func, select

from app.db.models import User
from tests.conftest import DEMO_EMAIL


def register(client, email: str, secret: str):
    return client.post("/api/users", json={"email": email, "password": secret})


def count_accounts(db) -> int:
    return db.scalar(select(func.count()).select_from(User))


def test_a_new_account_is_signed_in_at_once(client, db):
    """US01, criterion 1: the answer carries a token, so there is no second sign-in."""
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


def test_an_address_already_registered_is_refused(client, db, account):
    """US01, criterion 2 and BR1: no second account, whatever the capitals."""
    for email in (DEMO_EMAIL, DEMO_EMAIL.upper()):
        response = register(client, email, "abcd1234")

        assert response.status_code == 409
        assert response.json() == {
            "detail": "This email is already registered",
            "code": "email_taken",
        }
    assert count_accounts(db) == 1


@pytest.mark.parametrize("length", [5, 129])
def test_a_password_outside_6_to_128_characters_is_refused(client, db, length):
    """US01, criterion 3 and BR2: 5 and 129 characters are refused, and nothing is stored."""
    response = register(client, "hoa@example.com", "a" * length)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Password must be 6 to 128 characters",
        "code": "password_length",
    }
    assert count_accounts(db) == 0


@pytest.mark.parametrize("length", [6, 128])
def test_6_and_128_characters_are_accepted(client, length):
    """BR2, both edges."""
    assert register(client, "hoa@example.com", "a" * length).status_code == 201


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
def test_an_address_that_is_not_one_gets_400(client, db, email):
    response = register(client, email, "abcd1234")

    assert response.status_code == 400
    assert response.json() == {"detail": "Enter a valid email address", "code": "invalid_email"}
    assert count_accounts(db) == 0
