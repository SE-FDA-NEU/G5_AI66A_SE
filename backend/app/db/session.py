"""The database engine and the session factory."""

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def make_engine(url: str, **options) -> Engine:
    """Create an engine. On SQLite, foreign keys are switched on for every connection.

    The values sent with a query are left out of SQLAlchemy's error messages, so a crash logged
    by app/core/errors.py never shows an email address or a password hash.
    """
    options.setdefault("hide_parameters", True)
    is_sqlite = url.startswith("sqlite")
    if is_sqlite:
        # uvicorn answers requests from several threads, which SQLite refuses by default.
        options.setdefault("connect_args", {"check_same_thread": False})
    else:
        # Neon suspends an idle database after a few minutes and drops its connections. Testing a
        # connection before use replaces a dropped one instead of failing the request; the timeout
        # makes /health answer 503 within seconds when the database cannot be reached.
        options.setdefault("pool_pre_ping", True)
        options.setdefault("pool_recycle", 300)
        options.setdefault("connect_args", {"connect_timeout": 3})
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
