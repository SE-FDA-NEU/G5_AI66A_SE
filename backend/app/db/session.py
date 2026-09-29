"""The database engine and the session factory."""

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def make_engine(url: str, **options) -> Engine:
    """Create an engine. On SQLite, foreign keys are switched on for every connection."""
    is_sqlite = url.startswith("sqlite")
    if is_sqlite:
        # uvicorn answers requests from several threads, which SQLite refuses by default.
        options.setdefault("connect_args", {"check_same_thread": False})
    engine = create_engine(url, **options)

    if is_sqlite:

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(dbapi_connection, _connection_record):
            # SQLite ignores FOREIGN KEY constraints unless each connection asks for them, and
            # BR4 relies on every entry pointing at a real account.
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.close()

    return engine


engine = make_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
