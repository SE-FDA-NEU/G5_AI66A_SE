"""Signing in: US02, BR2, BR3 and BR10."""

from datetime import UTC, datetime, timedelta

import pytest

from app.core.security import create_access_token, verify_password
from tests.conftest import DEMO_EMAIL, DEMO_SECRET


def sign_in(client, email: str, secret: str):
    return client.post("/api/auth/login", json={"email": email, "password": secret})


def test_sign_in_returns_a_token_and_the_account(client, account):
    response = sign_in(client, DEMO_EMAIL, DEMO_SECRET)

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"] == {"id": account.id, "email": DEMO_EMAIL}


def test_sign_in_ignores_capitals_in_the_address(client, account):
    """BR1: MAI@EXAMPLE.COM is the same account as mai@example.com."""
    assert sign_in(client, "MAI@Example.COM", DEMO_SECRET).status_code == 200


@pytest.mark.parametrize(
    ("email", "secret"),
    [
        (DEMO_EMAIL, "wrong-one"),
        ("ghost@example.com", DEMO_SECRET),
        ("not-an-email", DEMO_SECRET),
    ],
    ids=["wrong password", "unknown email", "malformed email"],
)
def test_every_failed_sign_in_gets_the_same_answer(client, account, email, secret):
    """BR3: nobody can tell from the answer whether an address has an account."""
    response = sign_in(client, email, secret)

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect email or password",
        "code": "incorrect_sign_in",
    }


def test_password_is_stored_only_as_a_hash(client, account):
    """BR2: the database holds a one-way hash, and no response ever contains either."""
    assert account.password_hash != DEMO_SECRET
    assert DEMO_SECRET not in account.password_hash
    assert account.password_hash.startswith("pbkdf2_sha256$")
    assert verify_password(DEMO_SECRET, account.password_hash)

    response_text = sign_in(client, DEMO_EMAIL, DEMO_SECRET).text
    assert DEMO_SECRET not in response_text
    assert account.password_hash not in response_text


def test_me_returns_the_signed_in_account(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == DEMO_EMAIL


def test_me_without_a_token_asks_to_sign_in_again(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Please sign in again", "code": "sign_in_again"}


def test_a_forged_token_is_refused(client, account):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer made.up.token"})

    assert response.status_code == 401


def test_a_sign_in_lasts_seven_days(client, account):
    """BR10: signed in 7 days ago minus an hour still works; 7 days plus an hour does not."""
    now = datetime.now(UTC)
    fresh, _ = create_access_token(account.id, now=now - timedelta(days=7) + timedelta(hours=1))
    stale, _ = create_access_token(account.id, now=now - timedelta(days=7) - timedelta(hours=1))

    still_valid = client.get("/api/auth/me", headers={"Authorization": f"Bearer {fresh}"})
    assert still_valid.status_code == 200
    expired = client.get("/api/auth/me", headers={"Authorization": f"Bearer {stale}"})
    assert expired.status_code == 401
    assert expired.json() == {"detail": "Please sign in again", "code": "sign_in_again"}


def test_the_token_expires_seven_days_after_sign_in(client, account):
    before = datetime.now(UTC)
    body = sign_in(client, DEMO_EMAIL, DEMO_SECRET).json()
    expires_at = datetime.fromisoformat(body["expires_at"])

    assert timedelta(days=7) <= expires_at - before < timedelta(days=7, minutes=1)
