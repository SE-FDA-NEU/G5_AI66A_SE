"""Application settings, read from backend/.env. Every setting is listed in backend/.env.example."""

from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The backend/ folder. Settings and the database are found from here, so the app behaves the same
# whichever folder it is started from.
BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    APP_NAME: str = "Personal Expense Management API"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./expense.db"
    SECRET_KEY: str = "dev-only-change-me-3f9a1c7e5b2d4a6c8e0f1a3b5c7d9e1f"
    SESSION_DAYS: int = 7
    # PBKDF2 rounds per password (BR2). Tests lower it so they run quickly; nothing else should.
    PASSWORD_HASH_ITERATIONS: int = 600_000
    CORS_ORIGINS: str = "*"

    @field_validator("DATABASE_URL")
    @classmethod
    def anchor_sqlite_path(cls, url: str) -> str:
        """Read a relative SQLite path from backend/, not from the folder the command runs in."""
        prefix = "sqlite:///"
        path = url[len(prefix):] if url.startswith(prefix) else ""
        if path and path != ":memory:" and not Path(path).is_absolute():
            return prefix + (BACKEND_DIR / path).resolve().as_posix()
        return url

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
