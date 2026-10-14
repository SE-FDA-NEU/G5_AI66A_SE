"""Creating an account: US01, BR1 and BR2."""

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
