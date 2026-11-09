"""Start the API on a server. Render runs it from backend/ as the service's Start Command:

    python -m scripts.start

1. Reads the settings. With ENVIRONMENT=production it stops here if SECRET_KEY, CORS_ORIGINS or
   DATABASE_URL still hold a value that is only safe on a laptop (app/core/config.py).
2. Brings the database to the newest migration and adds the demo data if it is missing, dating it
   again when none of it falls in this month (scripts/seed_data.py).
3. Starts uvicorn on 0.0.0.0 and the port in $PORT. uvicorn's access log is off, because it
   prints query strings; app/core/request_log.py writes one line per request instead.

If step 1 or 2 fails, the API never answers /health, Render does not switch to the new version,
and the version that was running stays online (docs/operations.md, section 1).
"""

import os

import uvicorn

from app.core.config import settings
from app.core.request_log import configure_logging
from scripts.seed_data import DEMO_EMAIL, describe, seed


def main() -> None:
    counts = seed(settings.DATABASE_URL, refresh_stale_demo=True)
    print(
        f"Database ready: {describe(settings.DATABASE_URL)}, {counts.users} accounts, "
        f"{counts.transactions} entries, {counts.debts} debts, demo account {DEMO_EMAIL}",
        flush=True,
    )
    configure_logging()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        access_log=False,
        # Render ends HTTPS at its proxy; trust its X-Forwarded-* headers for the real scheme.
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
