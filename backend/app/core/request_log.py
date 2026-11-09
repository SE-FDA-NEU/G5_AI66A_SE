"""What the API writes to its log, and what it never writes (docs/operations.md, section 3).

One line per request: the method, the path without its query string, the status and the time it
took, with a warning when it took longer than SLOW_REQUEST_MS. Never a body, a header, a query
string, a token, a password or an email address: the body of a sign-in holds the password, and
the Authorization header holds the token. uvicorn's own access log is switched off in
scripts/start.py, because it prints the query string.
"""

import logging
import time

from fastapi import FastAPI, Request

from app.core.config import settings

logger = logging.getLogger("app.requests")


def configure_logging() -> None:
    """Lines such as `2026-11-09 10:12:03 INFO app.requests GET /api/summary 200 41ms`.

    Called by scripts/start.py on the server, after the migrations: Alembic sets up logging of
    its own from alembic.ini, and force=True replaces it. The tests leave logging as pytest sets
    it, so caplog sees every line.
    """
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


def register_request_log(app: FastAPI) -> None:
    """Register after register_error_handlers, so a crash is logged with the 500 it became."""

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        took_ms = (time.perf_counter() - started) * 1000
        level = logging.WARNING if took_ms > settings.SLOW_REQUEST_MS else logging.INFO
        logger.log(
            level,
            "%s %s %s %.0fms",
            request.method,
            request.url.path,
            response.status_code,
            took_ms,
        )
        return response
