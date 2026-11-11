"""The profile (US16, BR15) and deleting an account (US18, BR16).

Test cases TC-87 to TC-98 of docs/testing.md, section 2.8; the ID is in each test's name.
"""

import base64
from datetime import date

import pytest
from sqlalchemy import func, select

from app.db.models import Debt, Transaction, User
from app.db.repositories import category_repo, debt_repo, transaction_repo
from tests.conftest import DEMO_EMAIL, DEMO_SECRET, make_account

ME = "/api/users/me"


def picture(size: int, kind: str = "png") -> str:
    return f"data:image/{kind};base64," + base64.b64encode(b"\x00" * size).decode()


def patch(client, headers, **fields):
    return client.patch(ME, json=fields, headers=headers)


def sign_in(client, email=DEMO_EMAIL, password=DEMO_SECRET):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def test_tc87_a_new_account_has_an_empty_profile(client, auth_headers):
    response = client.get(ME, headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == {
        "id": response.json()["id"],
        "email": DEMO_EMAIL,
        "full_name": None,
        "nickname": None,
        "phone": None,
        "avatar": None,
    }


def test_tc88_the_profile_is_saved_and_comes_back_at_sign_in(client, auth_headers):
    response = patch(
        client,
        auth_headers,
        full_name="  Nguyen Thi Mai ",
        nickname="Mai",
        phone="+84 912 345 678",
    )

    assert response.status_code == 200
    user = sign_in(client).json()["user"]
    assert (user["full_name"], user["nickname"], user["phone"]) == (
        "Nguyen Thi Mai",
        "Mai",
        "+84 912 345 678",
    )


def test_tc89_only_the_fields_sent_change_and_an_empty_one_is_cleared(client, auth_headers):
    patch(client, auth_headers, full_name="Nguyen Thi Mai", nickname="Mai")

    patch(client, auth_headers, nickname="")

    body = client.get(ME, headers=auth_headers).json()
    assert body["full_name"] == "Nguyen Thi Mai"
    assert body["nickname"] is None


@pytest.mark.parametrize(
    "field, length, accepted",
    [
        ("full_name", 80, True),
        ("full_name", 81, False),
        ("nickname", 40, True),
        ("nickname", 41, False),
    ],
)
def test_tc90_a_full_name_has_at_most_80_characters_a_nickname_40(
    client, auth_headers, field, length, accepted
):
    response = patch(client, auth_headers, **{field: "a" * length})

    assert response.status_code == (200 if accepted else 422)
    if not accepted:
        code = "name_too_long" if field == "full_name" else "nickname_too_long"
        assert response.json()["code"] == code


@pytest.mark.parametrize(
    "phone, accepted",
    [
        ("0912 3456", True),  # 8 digits
        ("0912 345", False),  # 7 digits
        ("+84 912 345 678 9012", True),  # 15 digits
        ("+84 912 345 678 90123", False),  # 16 digits
        ("  ".join("0" * 15), False),  # 15 digits, but 43 characters
        ("0912-abc-678", False),
        ("84+912345678", False),
    ],
)
def test_tc91_a_phone_number_has_8_to_15_digits(client, auth_headers, phone, accepted):
    response = patch(client, auth_headers, phone=phone)

    assert response.status_code == (200 if accepted else 422)
    if not accepted:
        assert response.json()["code"] == "invalid_phone"


def test_tc92_the_email_cannot_be_changed(client, auth_headers):
    response = patch(client, auth_headers, email="new@example.com", nickname="Mai")

    assert response.status_code == 400
    body = client.get(ME, headers=auth_headers).json()
    assert body["email"] == DEMO_EMAIL
    assert body["nickname"] is None, "nothing of a refused request is saved"


@pytest.mark.parametrize(
    "avatar, accepted",
    [
        (picture(200_000), True),
        (picture(200_001), False),
        (picture(1_000, "jpeg"), True),
        (picture(1_000, "gif"), False),
        ("https://example.com/me.png", False),
        ("data:image/png;base64,not base64!", False),
    ],
    ids=["200,000 bytes", "200,001 bytes", "JPEG", "GIF", "a link", "broken base64"],
)
def test_tc93_a_picture_is_png_jpeg_or_webp_of_200_kb_or_less(
    client, auth_headers, avatar, accepted
):
    response = patch(client, auth_headers, avatar=avatar)

    assert response.status_code == (200 if accepted else 422)
    if accepted:
        assert client.get(ME, headers=auth_headers).json()["avatar"] == avatar
        assert patch(client, auth_headers, avatar=None).json()["avatar"] is None
    else:
        assert response.json()["code"] == "invalid_avatar"


def test_tc94_signed_out_nobody_reads_or_changes_a_profile(client, account):
    assert client.get(ME).status_code == 401
    assert client.patch(ME, json={"nickname": "x"}).status_code == 401
    assert client.request("DELETE", ME, json={"email": "x", "password": "y"}).status_code == 401


def own_things(db, user_id: int) -> None:
    transaction_repo.create(
        db,
        user_id=user_id,
        kind="expense",
        amount=55_000,
        note="tra sua",
        occurred_on=date.today(),
        category_id=category_repo.get_by_name(db, "Food").id,
    )
    debt_repo.create(
        db,
        user_id=user_id,
        direction="lent",
        person="Lan",
        amount=200_000,
        note="",
        started_on=date.today(),
        due_on=None,
    )


def count(db, model, user_id: int) -> int:
    return db.scalar(select(func.count()).select_from(model).where(model.user_id == user_id))


def delete(client, headers, email=DEMO_EMAIL, password=DEMO_SECRET):
    body = {"email": email, "password": password}
    return client.request("DELETE", ME, json=body, headers=headers)


def test_tc95_the_right_email_and_password_delete_the_account_and_all_it_owns(
    client, db, account, auth_headers
):
    own_things(db, account.id)
    user_id = account.id

    response = delete(client, auth_headers)

    assert response.status_code == 204
    db.expire_all()
    assert db.get(User, user_id) is None
    assert count(db, Transaction, user_id) == 0
    assert count(db, Debt, user_id) == 0
    assert sign_in(client).status_code == 401, "the password no longer opens anything"
    assert client.get(ME, headers=auth_headers).status_code == 401, "the old token is dead"


@pytest.mark.parametrize(
    "email, password",
    [(DEMO_EMAIL, "demo1235"), ("lan@example.com", DEMO_SECRET)],
    ids=["wrong password", "another account's email"],
)
def test_tc96_a_wrong_email_or_password_deletes_nothing(
    client, db, account, auth_headers, email, password
):
    make_account(db, email="lan@example.com")

    response = delete(client, auth_headers, email=email, password=password)

    assert response.status_code == 422
    assert response.json()["code"] == "confirmation_mismatch"
    assert client.get(ME, headers=auth_headers).status_code == 200


def test_tc97_the_email_may_be_typed_in_capitals(client, auth_headers):
    """BR1: MAI@EXAMPLE.COM is the same account as mai@example.com."""
    assert delete(client, auth_headers, email="MAI@Example.com").status_code == 204


def test_tc98_deleting_one_account_leaves_every_other_account_alone(
    client, db, account, auth_headers
):
    lan = make_account(db, email="lan@example.com")
    own_things(db, lan.id)

    delete(client, auth_headers)

    db.expire_all()
    assert count(db, Transaction, lan.id) == 1
    assert count(db, Debt, lan.id) == 1
