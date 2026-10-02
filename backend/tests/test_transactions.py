"""The list of recent entries: US05 and BR4."""

from datetime import date, timedelta

from app.db.repositories import category_repo, transaction_repo
from tests.conftest import make_account


def add_entries(db, user_id: int, count: int) -> None:
    """`count` entries, two a day going back from today, the later one of each day added last."""
    food = category_repo.get_by_name(db, "Food")
    for number in range(count):
        transaction_repo.create(
            db,
            user_id=user_id,
            kind="expense",
            amount=1_000 * (number + 1),
            note=f"entry {number}",
            occurred_on=date.today() - timedelta(days=(count - 1 - number) // 2),
            category_id=food.id,
        )


def test_the_list_shows_the_20_most_recent_of_25_newest_first(client, db, account, auth_headers):
    """US05, criterion 1."""
    add_entries(db, account.id, 25)

    response = client.get("/api/transactions", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 25
    assert len(body["items"]) == 20
    notes = [item["note"] for item in body["items"]]
    assert notes == [f"entry {number}" for number in range(24, 4, -1)]
    dates = [item["occurred_on"] for item in body["items"]]
    assert dates == sorted(dates, reverse=True)


def test_each_row_has_amount_note_kind_of_spending_and_date(client, db, account, auth_headers):
    add_entries(db, account.id, 1)

    item = client.get("/api/transactions", headers=auth_headers).json()["items"][0]

    assert item["amount"] == 1_000
    assert item["note"] == "entry 0"
    assert item["category"]["name"] == "Food"
    assert item["occurred_on"] == date.today().isoformat()


def test_the_list_never_shows_another_accounts_entries(client, db, account, auth_headers):
    """BR4: an account reads only its own entries."""
    stranger = make_account(db, email="stranger@example.com")
    add_entries(db, stranger.id, 3)
    add_entries(db, account.id, 2)

    body = client.get("/api/transactions", headers=auth_headers).json()

    assert body["total"] == 2
    assert all(item["note"] in {"entry 0", "entry 1"} for item in body["items"])


def test_the_list_needs_a_sign_in(client):
    response = client.get("/api/transactions")

    assert response.status_code == 401
    assert response.json() == {"detail": "Please sign in again"}


def test_the_limit_must_be_between_1_and_100(client, auth_headers):
    # A malformed request is the caller's mistake, not a broken rule: 400, not 422.
    assert client.get("/api/transactions?limit=0", headers=auth_headers).status_code == 400
    assert client.get("/api/transactions?limit=101", headers=auth_headers).status_code == 400
    assert client.get("/api/transactions?limit=100", headers=auth_headers).status_code == 200
