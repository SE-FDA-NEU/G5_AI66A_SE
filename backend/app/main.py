"""The FastAPI application: creates the app and mounts every router."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.routers import auth

app = FastAPI(
    title=settings.APP_NAME,
    version="0.2.0",
    description="API of the Personal Expense Management App, Team 05 (AI66A).",
)
register_error_handlers(app)

# The Expo web page is served from another port, so the browser needs CORS to call the API.
# Sign-in travels as a bearer token, not a cookie, so credentials stay switched off.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Opening the API in a browser lands on its interactive documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["system"], summary="Check that the API is running")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.API_PREFIX)
