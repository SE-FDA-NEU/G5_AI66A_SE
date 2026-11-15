"""Categories of an account's own, added from "Other" (BR17).

Test cases TC-103 to TC-110 of docs/testing.md, section 2.8; the ID is in each test's name.
"""

import pytest
from sqlalchemy import select

from app.db.models import Category
from tests.conftest import DEMO_SECRET, make_account


def add(client, headers, name, kind="expense"):
    return client.post("/api/categories", json={"name": name, "kind": kind}, headers=headers)


def headers_of(client, db, email):
    make_account(db, email=email)
    response = client.post("/api/auth/login", json={"email": email, "password": DEMO_SECRET})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_tc103_an_account_adds_a_category_of_its_own(client, auth_headers):
    response = add(client, auth_headers, "  Coffee  ")

    assert response.status_code == 201
    body = response.json()
    assert (body["name"], body["kind"], body["custom"]) == ("Coffee", "expense", True)
    listed = client.get("/api/categories", headers=auth_headers).json()
    assert [(c["name"], c["custom"]) for c in listed] == [
        ("Food", False),
        ("Transport", False),
        ("Coffee", True),
        ("Salary", False),
    ], "its own after the shared kinds of spending, before money received"


def test_tc104_only_the_account_that_added_it_sees_it(client, db, auth_headers):
    coffee = add(client, auth_headers, "Coffee").json()
    lan = headers_of(client, db, "lan@example.com")

    names = [c["name"] for c in client.get("/api/categories", headers=lan).json()]
    assert "Coffee" not in names
    detail = client.get(f"/api/categories/{coffee['id']}/spending", headers=lan)
    assert detail.status_code == 404, "BR4: another account's category does not exist for Lan"
    entry = {"kind": "expense", "amount": 30_000, "category_id": coffee["id"]}
    refused = client.post("/api/transactions", json=entry, headers=lan)
    assert (refused.status_code, refused.json()["code"]) == (422, "unknown_category")


def test_tc105_an_entry_can_be_filed_under_it(client, auth_headers):
    coffee = add(client, auth_headers, "Coffee").json()
    entry = {"kind": "expense", "amount": 30_000, "category_id": coffee["id"]}

    saved = client.post("/api/transactions", json=entry, headers=auth_headers)

    assert saved.status_code == 201
    assert saved.json()["category"] == coffee
    rows = client.get("/api/categories/spending", headers=auth_headers).json()
    mine = next(r for r in rows if r["category"]["id"] == coffee["id"])
    assert (mine["this_month"], mine["count"]) == (30_000, 1)


def test_tc106_br6_still_holds_for_its_own_categories(client, auth_headers):
    tips = add(client, auth_headers, "Tips", kind="income").json()
    entry = {"kind": "expense", "amount": 30_000, "category_id": tips["id"]}

    refused = client.post("/api/transactions", json=entry, headers=auth_headers)

    assert (refused.status_code, refused.json()["code"]) == (422, "unknown_category")


@pytest.mark.parametrize(
    ("name", "allowed"),
    [("", False), ("   ", False), ("a", True), ("x" * 40, True), ("x" * 41, False)],
    ids=["empty", "spaces only", "1 character", "40 characters", "41 characters"],
)
def test_tc107_a_name_is_1_to_40_characters(client, auth_headers, name, allowed):
    response = add(client, auth_headers, name)

    if allowed:
        assert response.status_code == 201
    else:
        assert response.status_code == 422
        assert response.json() == {
            "detail": "A category name is 1 to 40 characters",
            "code": "category_name_length",
        }


@pytest.mark.parametrize("name", ["Coffee", "COFFEE", "food", "Salary"])
def test_tc108_a_name_already_in_the_list_is_refused(client, auth_headers, name):
    add(client, auth_headers, "Coffee")

    response = add(client, auth_headers, name)

    assert response.status_code == 409
    assert response.json() == {
        "detail": "You already have a category with this name",
        "code": "category_name_taken",
    }


def test_tc109_two_accounts_may_use_the_same_name(client, db, auth_headers):
    add(client, auth_headers, "Coffee")
    lan = headers_of(client, db, "lan@example.com")

    assert add(client, lan, "Coffee").status_code == 201


def test_tc110_deleting_the_account_deletes_its_categories(client, db, account, auth_headers):
    add(client, auth_headers, "Coffee")
    body = {"email": account.email, "password": DEMO_SECRET}

    deleted = client.request("DELETE", "/api/users/me", json=body, headers=auth_headers)

    assert deleted.status_code == 204
    db.expire_all()
    names = db.scalars(select(Category.name).order_by(Category.id)).all()
    assert names == ["Food", "Transport", "Salary"], "Coffee went with the account, the rest stays"
