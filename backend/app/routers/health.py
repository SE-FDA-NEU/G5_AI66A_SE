"""GET /health: is the API running, and does its database answer?

Render calls it before it sends traffic to a new version (the service's Health Check Path), so a
version that cannot reach the database never replaces the one that can. The live check in CI
reads `version` to know that a deploy has finished (docs/operations.md, sections 1 and 3).
"""

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.deps import DbSession

logger = logging.getLogger("app.health")

router = APIRouter(tags=["system"])


@router.api_route(
    "/health",
    methods=["GET", "HEAD"],
    summary="Check that the API and its database answer",
    responses={503: {"description": "The API runs, but its database does not answer"}},
)
def health(db: DbSession) -> JSONResponse:
    """200 when the database answers `SELECT 1`; 503 when it does not."""
    body = {"status": "ok", "database": "ok", "version": settings.version}
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Health check failed: the database did not answer")
        body.update(status="unavailable", database="unreachable")
        return JSONResponse(status_code=503, content=body)
    return JSONResponse(content=body)
