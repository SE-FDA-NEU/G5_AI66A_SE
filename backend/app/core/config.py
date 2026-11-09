"""Application settings, read from backend/.env. Every setting is listed in backend/.env.example."""

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The key in backend/.env.example. Anyone can read it on GitHub: a server must never use it.
DEV_SECRET_KEY = "dev-only-change-me-3f9a1c7e5b2d4a6c8e0f1a3b5c7d9e1f"

# The backend/ folder. Settings and the database are found from here, so the app behaves the same
# whichever folder it is started from.
BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    APP_NAME: str = "Personal Expense Management API"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./expense.db"
    SECRET_KEY: str = DEV_SECRET_KEY
    SESSION_DAYS: int = 7
    # PBKDF2 rounds per password (BR2). Tests lower it so they run quickly; nothing else should.
    PASSWORD_HASH_ITERATIONS: int = 600_000
    CORS_ORIGINS: str = "*"
    # "development" on a laptop, in Codespaces and in CI; "production" on Render. In production
    # the app refuses to start with a setting that is only safe on a laptop (check_production).
    ENVIRONMENT: str = "development"
    # Render sets RENDER_GIT_COMMIT to the commit it deployed. /health reports its first seven
    # characters, so anyone can see which version is answering (docs/operations.md, section 1).
    RENDER_GIT_COMMIT: str = ""
    LOG_LEVEL: str = "INFO"
    # A request slower than this is logged as a warning (docs/operations.md, section 3).
    SLOW_REQUEST_MS: int = 1000

    @field_validator("DATABASE_URL")
    @classmethod
    def anchor_sqlite_path(cls, url: str) -> str:
        """Read a relative SQLite path from backend/, not from the folder the command runs in.

        Neon gives a PostgreSQL address as postgresql://... or postgres://...; SQLAlchemy is
        told to use the psycopg driver for it (ADR 4, docs/design.md).
        """
        for scheme in ("postgres://", "postgresql://"):
            if url.startswith(scheme):
                return "postgresql+psycopg://" + url[len(scheme):]
        prefix = "sqlite:///"
        path = url[len(prefix):] if url.startswith(prefix) else ""
        if path and path != ":memory:" and not Path(path).is_absolute():
            return prefix + (BACKEND_DIR / path).resolve().as_posix()
        return url

    @model_validator(mode="after")
    def check_production(self) -> "Settings":
        """On a server, refuse the three defaults that are only safe on a laptop."""
        if self.ENVIRONMENT != "production":
            return self
        if self.SECRET_KEY == DEV_SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY: set a random value of 32 characters or more")
        if "*" in self.cors_origin_list:
            raise ValueError("CORS_ORIGINS: list the web app's address instead of *")
        if self.DATABASE_URL.startswith("sqlite"):
            raise ValueError("DATABASE_URL: SQLite is emptied on every deploy; use PostgreSQL")
        return self

    @property
    def version(self) -> str:
        """The deployed commit, short, or "dev" on a laptop."""
        return self.RENDER_GIT_COMMIT[:7] or "dev"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
