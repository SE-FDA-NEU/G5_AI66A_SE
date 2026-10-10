"""One error shape for the whole API: {"detail": "<one sentence>", "code": "<what went wrong>"}.

`detail` is the exact sentence of the acceptance criteria, in English. `code` names the error and
never changes when the sentence is reworded, so the app chooses the message it shows, in the
user's language, by `code` (docs/ui.md, section 3).

Each kind of refusal a service raises gets its status here, once: 400 a malformed request, 401 not
signed in, 409 a conflict with what is stored, 422 a well-formed request that breaks a business
rule (docs/design.md, section 3). Anything else that goes wrong is a 500 in the same shape, never
a stack trace.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.services.errors import AlreadyExists, NotSignedIn, NotUnderstood, RuleBroken, ServiceError

logger = logging.getLogger("app")

SERVER_ERROR = "The server could not finish this request"

STATUS_OF = {
    NotUnderstood: status.HTTP_400_BAD_REQUEST,
    NotSignedIn: status.HTTP_401_UNAUTHORIZED,
    AlreadyExists: status.HTTP_409_CONFLICT,
    RuleBroken: status.HTTP_422_UNPROCESSABLE_CONTENT,
}

# Codes for the errors FastAPI raises on its own, such as a path that does not exist.
CODE_OF_STATUS = {
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
}


def error_response(
    status_code: int, detail: str, code: str, headers: dict[str, str] | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"detail": detail, "code": code}, headers=headers
    )


def status_of(error: ServiceError) -> int:
    for kind, status_code in STATUS_OF.items():
        if isinstance(error, kind):
            return status_code
    return status.HTTP_400_BAD_REQUEST


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def refused(_request: Request, error: ServiceError) -> JSONResponse:
        status_code = status_of(error)
        # A 401 says how to sign in, as HTTP asks.
        headers = {"WWW-Authenticate": "Bearer"} if status_code == 401 else None
        return error_response(status_code, error.message, error.code, headers)

    @app.exception_handler(RequestValidationError)
    async def malformed(_request: Request, exc: RequestValidationError) -> JSONResponse:
        # FastAPI's own validation answers with a list and 422. A request the app never sends,
        # such as a limit outside 1 to 100, is malformed: 400, one sentence, code invalid_request.
        first = exc.errors()[0]
        field = ".".join(str(part) for part in first["loc"] if part not in ("body", "query"))
        message = f"{field}: {first['msg']}" if field else first["msg"]
        return error_response(status.HTTP_400_BAD_REQUEST, message, "invalid_request")

    @app.exception_handler(StarletteHTTPException)
    async def http_error(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = CODE_OF_STATUS.get(exc.status_code, f"http_{exc.status_code}")
        return error_response(exc.status_code, str(exc.detail), code, exc.headers)

    @app.middleware("http")
    async def unexpected(request: Request, call_next):
        """Turn a crash into a 500 in the usual shape.

        main.py adds the CORS middleware after this one, so CORS wraps it and the browser still
        gets the CORS headers. A crash answered outside CORS reaches the browser without them,
        and the app cannot tell it from a server that is not running at all.
        """
        try:
            return await call_next(request)
        except Exception:
            logger.exception("Unexpected error on %s %s", request.method, request.url.path)
            return error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR, SERVER_ERROR, "server_error"
            )
