# ruff: noqa: E402  (the environment below must be set before the app is imported)
"""Fixtures shared by every test.

Each test gets its own empty database in memory, so tests never touch backend/expense.db and
never affect one another.
"""

import os

# Set before the app is imported: fast password hashing, and no database file on disk.
os.environ["PASSWORD_HASH_ITERATIONS"] = "1000"
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.deps import get_db
from app.core.security import hash_password
from app.db.base import Base
from app.db.models import KIND_INCOME, KIND_SPENDING, Category, User
from app.db.repositories import user_repo
from app.db.session import make_engine
from app.main import app

DEMO_EMAIL = "mai@example.com"
DEMO_SECRET = "demo1234"


@pytest.fixture()
def db():
    """An empty in-memory database with three categories.

    StaticPool keeps one connection open, so the test and the app see the same in-memory database.
    """
    engine = make_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        session.add_all(
            [
                Category(name="Food", kind=KIND_SPENDING),
                Category(name="Transport", kind=KIND_SPENDING),
                Category(name="Salary", kind=KIND_INCOME),
            ]
        )
        session.commit()
        yield session
    engine.dispose()


@pytest.fixture()
def client(db):
    """Calls the app in-process, without starting a server, against the test database."""

    def use_test_database():
        yield db

    app.dependency_overrides[get_db] = use_test_database
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def make_account(db: Session, email: str = DEMO_EMAIL, secret: str = DEMO_SECRET) -> User:
    return user_repo.create(db, email=email, password_hash=hash_password(secret))


@pytest.fixture()
def account(db) -> User:
    return make_account(db)


@pytest.fixture()
def auth_headers(client, account) -> dict[str, str]:
    """Headers of a request made by the signed-in demo account."""
    response = client.post("/api/auth/login", json={"email": DEMO_EMAIL, "password": DEMO_SECRET})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
