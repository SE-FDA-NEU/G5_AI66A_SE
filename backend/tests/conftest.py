# ruff: noqa: E402  (the environment below must be set before the app is imported)
"""Fixtures shared by every test.

Each test gets its own empty database in memory, so tests never touch backend/expense.db and
never affect one another.

With TEST_DATABASE_URL set to a PostgreSQL database, the same tests run there instead, as the
production database does (ADR 4, docs/design.md). The tables are made once; each test runs inside
one transaction that is rolled back at the end, so the tests still never see one another's rows.
CI runs both, in the jobs "Python tests" and "Python tests on PostgreSQL".
"""

import os

# Set before the app is imported: fast password hashing, and no database file on disk.
os.environ["PASSWORD_HASH_ITERATIONS"] = "1000"
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
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


TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "")


def add_categories(session: Session) -> None:
    session.add_all(
        [
            Category(name="Food", kind=KIND_SPENDING),
            Category(name="Transport", kind=KIND_SPENDING),
            Category(name="Salary", kind=KIND_INCOME),
        ]
    )
    session.commit()


@pytest.fixture(scope="session")
def postgres_engine():
    """One PostgreSQL engine for the whole run, its tables made from the models once."""
    engine = make_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def db(request):
    """An empty database with three categories.

    On SQLite, a new in-memory database per test; StaticPool keeps one connection open, so the
    test and the app see the same database. On PostgreSQL, one transaction per test, rolled back
    at the end: the app's own commits become savepoints inside it.
    """
    if TEST_DATABASE_URL:
        engine: Engine = request.getfixturevalue("postgres_engine")
        connection = engine.connect()
        outer = connection.begin()
        session = Session(
            bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )
        add_categories(session)
        yield session
        session.close()
        outer.rollback()
        connection.close()
        return

    engine = make_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        add_categories(session)
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
