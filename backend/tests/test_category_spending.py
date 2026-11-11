"""What each category holds for one account (US17).

Test cases TC-99 to TC-102 of docs/testing.md, section 2.8; the ID is in each test's name.
"""

from datetime import date, timedelta

from app.db.repositories import category_repo, transaction_repo
from tests.conftest import make_account


def add(db, user_id: int, category: str, amount: int, occurred_on: date | None = None) -> None:
    kind = "income" if category == "Salary" else "expense"
    transaction_repo.create(
        db,
        user_id=user_id,
        kind=kind,
        amount=amount,
        note="",
        occurred_on=occurred_on or date.today(),
        category_id=category_repo.get_by_name(db, category).id,
    )


def by_name(rows) -> dict:
    return {row["category"]["name"]: row for row in rows}


def test_tc99_each_category_with_this_month_and_all_time(client, db, account, auth_headers):
    add(db, account.id, "Food", 55_000)
    add(db, account.id, "Food", 45_000)
    add(db, account.id, "Transport", 32_000)
    lan = make_account(db, email="lan@example.com")
    add(db, lan.id, "Food", 999_000)

    response = client.get("/api/categories/spending", headers=auth_headers)

    assert response.status_code == 200
    rows = by_name(response.json())
    assert list(rows) == ["Food", "Transport", "Salary"], "every category, in the usual order"
    assert (rows["Food"]["this_month"], rows["Food"]["all_time"], rows["Food"]["count"]) == (
        100_000,
        100_000,
        2,
    ), "another account's 999,000 is not counted (BR4)"
    assert rows["Salary"]["all_time"] == 0, "a category never used is listed at 0"


def test_tc100_the_last_day_of_last_month_counts_in_all_time_only(
    client, db, account, auth_headers
):
    first = date.today().replace(day=1)
    add(db, account.id, "Food", 40_000, occurred_on=first - timedelta(days=1))
    add(db, account.id, "Food", 15_000, occurred_on=first)

    food = by_name(client.get("/api/categories/spending", headers=auth_headers).json())["Food"]

    assert (food["this_month"], food["all_time"]) == (15_000, 55_000)


def test_tc101_one_category_six_months_and_its_newest_entries(
    client, db, account, auth_headers
):
    food = category_repo.get_by_name(db, "Food").id
    first = date.today().replace(day=1)
    add(db, account.id, "Food", 40_000, occurred_on=first - timedelta(days=1))
    for amount in range(1_000, 13_000, 1_000):
        add(db, account.id, "Food", amount)
    add(db, account.id, "Transport", 32_000)

    response = client.get(f"/api/categories/{food}/spending", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["category"]["name"] == "Food"
    assert [m["month"] for m in body["months"]][-1] == first.strftime("%Y-%m")
    assert len(body["months"]) == 6
    assert body["months"][-1]["amount"] == 78_000
    assert body["months"][-2]["amount"] == 40_000
    assert len(body["recent"]) == 10, "the ten newest, not all thirteen"
    assert all(entry["category"]["name"] == "Food" for entry in body["recent"])


def test_tc102_a_category_that_does_not_exist(client, auth_headers):
    response = client.get("/api/categories/999/spending", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["code"] == "category_not_found"
