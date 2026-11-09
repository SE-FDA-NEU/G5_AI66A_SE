# Operations — Personal Expense Management App

How the app runs on the internet, how a change reaches it, how we watch it and how someone else
could look after it. Team 05 (G5_AI66A), Sprint 5.

## 1. How to run and release

| What | Where |
| --- | --- |
| The app, for everyone | **https://g5-expense-web.onrender.com** |
| The API and its documentation | https://g5-expense-api.onrender.com · https://g5-expense-api.onrender.com/docs |
| Health | https://g5-expense-api.onrender.com/health |
| Platform | Render, free plan: a Web Service for the API, a Static Site for the web app |
| Database | PostgreSQL 16 on Neon, free plan (ADR 4, `docs/design.md`) |
| Test account | `mai@example.com` / `demo1234`, a test value seeded at start-up, never a real password |

**How a new version gets there.** Nobody copies files to a server. A merge into `main` is a release:

1. A pull request is opened; CI runs its four check jobs; a teammate approves it through
   **Review changes**. The ruleset on `main` keeps the merge button locked until both happen.
2. The merge pushes to `main`, and CI runs again on the merged code.
3. Only if all four checks pass, the job **Deploy to Render** calls the two deploy hooks.
4. Render builds the API (`pip install -r requirements.txt`) and starts it with
   `python -m scripts.start`: migrations, demo data if missing, then uvicorn on `$PORT`. It sends
   traffic to the new version only once its `/health` answers 200; until then the old one answers.
   In parallel it builds the web app (`npm ci && npm run build`) and publishes `mobile/dist`.
5. The workflow **Live check** waits until `/health` reports the new commit, then opens `/`,
   `/login` and `/register`.

**Render settings**, so the services can be rebuilt by someone who has never seen them:

| Service | Setting | Value |
| --- | --- | --- |
| API, Web Service | Root directory · Build · Start | `backend` · `pip install -r requirements.txt` · `python -m scripts.start` |
| | Health check path · Auto-Deploy | `/health` · **Off** (CI deploys through the hook) |
| | Environment | `ENVIRONMENT=production`, `DATABASE_URL` (Neon), `SECRET_KEY` (random, 64 hex), `CORS_ORIGINS=https://g5-expense-web.onrender.com`, `PYTHON_VERSION=3.12.12` |
| Web, Static Site | Root directory · Build · Publish | `mobile` · `npm ci && npm run build` · `dist` |
| | Rewrite · Auto-Deploy | `/*` → `/index.html` · **Off** |
| | Environment | `EXPO_PUBLIC_API_URL=https://g5-expense-api.onrender.com/api`, `NODE_VERSION=22` |
| GitHub | Secrets · Variables | `RENDER_DEPLOY_HOOK_API`, `RENDER_DEPLOY_HOOK_WEB` · `API_URL`, `APP_URL` |

**Rolling back.** If a release breaks something:

1. **At once:** Render → the service → *Events* → the last good deploy → **Rollback**. The URL runs
   the old commit again within a minute. Do it for the API and the web app separately.
2. **Then, for good:** open a pull request that `git revert`s the merge, let CI pass and merge it.
   CI deploys the reverted code, so `main` and the URL agree again. Until then `/health` reports
   the old commit while `main` has the new one, which is how anyone can tell a rollback is in place.

A release that cannot reach the database never goes live: its `/health` answers 503, and Render
keeps the previous version.
