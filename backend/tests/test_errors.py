"""Every error answers {"detail": <one sentence>, "code": <what went wrong>}, whatever caused it.

The app picks the message it shows by `code`, so a missing code is a blank or wrong message on
screen (docs/ui.md, section 3).
"""

import pytest

from app.services import transaction_service


def test_a_malformed_request_gets_400_and_invalid_request(client, auth_headers):
    response = client.get("/api/transactions?limit=0", headers=auth_headers)

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "invalid_request"
    assert body["detail"].startswith("limit:")


def test_a_path_that_does_not_exist_gets_404_and_not_found(client):
    response = client.get("/api/nothing-here")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found", "code": "not_found"}


def test_a_401_says_how_to_sign_in(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.fixture()
def broken_list(monkeypatch):
    """Make the list of entries crash, as a bug in the code would."""

    def crash(*_args, **_kwargs):
        raise RuntimeError("a bug")

    monkeypatch.setattr(transaction_service, "list_recent", crash)


def test_a_crash_gets_500_with_a_sentence_not_a_stack_trace(client, auth_headers, broken_list):
    response = client.get("/api/transactions", headers=auth_headers)

    assert response.status_code == 500
    assert response.json() == {
        "detail": "The server could not finish this request",
        "code": "server_error",
    }
    assert "RuntimeError" not in response.text


def test_a_crash_still_carries_the_cors_header(client, auth_headers, broken_list):
    """Without the header the browser hides the answer, and the app shows "Cannot reach the
    server" for a server that is running."""
    headers = {**auth_headers, "Origin": "http://localhost:8081"}

    response = client.get("/api/transactions", headers=headers)

    assert response.status_code == 500
    assert response.headers["access-control-allow-origin"] == "*"
