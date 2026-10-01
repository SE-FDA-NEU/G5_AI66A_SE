"""One error shape for the whole API: {"detail": "<one sentence>"}.

HTTPException already answers that way. FastAPI's own validation errors answer with a list and
422, so the handler below turns the list into a single sentence the app can show as it is, and
answers 400: the request itself is malformed, such as a limit outside 1 to 100. 422 stays for a
well-formed request that breaks a business rule, which the services check (docs/design.md,
section 3).
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def one_sentence(_request: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0]
        field = ".".join(str(part) for part in first["loc"] if part not in ("body", "query"))
        message = f"{field}: {first['msg']}" if field else first["msg"]
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": message})
