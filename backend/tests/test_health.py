"""What the server needs to be run by someone else: /health, the request log and the production
settings (docs/operations.md, sections 1 and 3; docs/testing.md, TC-79 to TC-84)."""

import logging

import pytest
from sqlalchemy.orm import Session

from app.core.config import DEV_SECRET_KEY, Settings
from app.core.deps import get_db
from app.db.session import make_engine
from app.main import app
from tests.conftest import DEMO_EMAIL, DEMO_SECRET

GOOD_KEY = "k" * 32
NEON = "postgresql://mai:pw@ep-x.neon.tech/expense?sslmode=require"
WEB = "https://g5-expense.onrender.com"


def test_tc79_health_answers_200_when_the_database_answers(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok", "version": "dev"}


def test_tc80_health_answers_503_when_the_database_does_not(client, tmp_path):
    """A SQLite file in a folder that does not exist cannot be opened: the database is down."""
    engine = make_engine(f"sqlite:///{(tmp_path / 'missing' / 'x.db').as_posix()}")

    def unreachable_database():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = unreachable_database
    response = client.get("/health")
    engine.dispose()

    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
    assert response.json()["database"] == "unreachable"


def test_tc81_the_log_has_one_line_per_request_without_the_password_or_email(
    client, account, caplog
):
    with caplog.at_level(logging.INFO, logger="app.requests"):
        client.post("/api/auth/login", json={"email": DEMO_EMAIL, "password": DEMO_SECRET})
        client.get("/api/transactions?limit=5")

    lines = [r.getMessage() for r in caplog.records if r.name == "app.requests"]
    assert lines[0].startswith("POST /api/auth/login 200 ")
    assert lines[1].startswith("GET /api/transactions 401 "), "no query string in the log"
    everything = caplog.text
    assert DEMO_SECRET not in everything
    assert DEMO_EMAIL not in everything


def test_tc82_a_slow_request_is_logged_as_a_warning(client, caplog, monkeypatch):
    monkeypatch.setattr("app.core.request_log.settings.SLOW_REQUEST_MS", -1)
    with caplog.at_level(logging.INFO, logger="app.requests"):
        client.get("/health")

    assert [r.levelname for r in caplog.records if r.name == "app.requests"] == ["WARNING"]


@pytest.mark.parametrize(
    "fields, refused",
    [
        ({"SECRET_KEY": DEV_SECRET_KEY}, "SECRET_KEY"),
        ({"SECRET_KEY": "k" * 31}, "SECRET_KEY"),
        ({"CORS_ORIGINS": "*"}, "CORS_ORIGINS"),
        ({"DATABASE_URL": "sqlite:///./expense.db"}, "DATABASE_URL"),
    ],
    ids=["the key from .env.example", "a 31-character key", "any web page", "SQLite"],
)
def test_tc83_production_refuses_a_setting_only_safe_on_a_laptop(fields, refused):
    values = {"SECRET_KEY": GOOD_KEY, "CORS_ORIGINS": WEB, "DATABASE_URL": NEON, **fields}

    with pytest.raises(ValueError, match=refused):
        Settings(_env_file=None, ENVIRONMENT="production", **values)


def test_tc84_production_starts_with_a_32_character_key_one_web_page_and_postgresql():
    settings = Settings(
        _env_file=None,
        ENVIRONMENT="production",
        SECRET_KEY=GOOD_KEY,
        CORS_ORIGINS=WEB,
        DATABASE_URL=NEON,
        RENDER_GIT_COMMIT="53a1dea0123456789",
    )

    assert settings.DATABASE_URL.startswith("postgresql+psycopg://"), "Neon's address, psycopg"
    assert settings.cors_origin_list == [WEB]
    assert settings.version == "53a1dea"


def test_root_sends_a_browser_to_the_documentation(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
