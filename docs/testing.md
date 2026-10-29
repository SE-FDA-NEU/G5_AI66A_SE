# Testing — Personal Expense Management App

**Team 05 · AI66A**
Milestone 4 · Sprint 4 · Weeks 11–12

Milestone 3 showed that people can use the app. This document shows that it keeps working when we
change it: every P0 story is checked by automated tests that run in about three seconds, with no
server and no real database, after every change and on every pull request.

**Run them all:** `pytest` in the cloned folder, with the virtual environment of
[docs/SETUP.md](SETUP.md) active (section 7 there). The tests live in
[`backend/tests/`](../backend/tests/); the app's own tests are in [`mobile/__tests__/`](../mobile/__tests__/).

---

## 1. What we test, and why

| Layer | Where | Test | Why |
| --- | --- | --- | --- |
| **Services** | `backend/app/services/` | Unit tests that call the service directly, with **today fixed** (12/11/2026 or 24/10/2026) and a database in memory | Every business rule lives here: BR1 to BR14. A mistake here is a wrong total or a refused entry, so this layer gets most tests, at both sides of every limit |
| **Repository** | `backend/app/db/repositories/`, the models and migrations | Tests on a database in memory (`test_repositories.py`), the table constraints written straight to the tables (`test_database_rules.py`), and the seed script on a temporary file (`test_seed.py`) | Checks the SQL: which rows a query finds, that every query keeps to one account (BR4), and that BR1, BR5, BR7 and BR13 hold even if an endpoint forgets them. CI also runs `alembic check` |
| **Routes** | `backend/app/routers/`, `backend/app/core/` | A few tests per route with FastAPI's `TestClient`, in-process: no port, no server | Only that each route answers the right status and error code, `{"detail", "code"}`, and refuses without a sign-in. The rules behind them are already tested on the services |
| **Interface** | `mobile/src/` | Jest tests (`npm test`, 101 tests) for the pure functions only: amounts, dates, the entry form, chart scaling, debt dates, the dictionaries and the routes. **No screen is tested automatically** | The screens were checked by real users in M3 and change every sprint; a screenshot test would break on every change of spacing. What a screen shows comes from the API, which is tested above |

**Where the risk is, and why we tested it most.** We tested most where a mistake costs money or
trust and where the code is new: the money rules (BR5 on entries, corrections and debts; BR11 dates;
the month totals of US04) and the sign-in rules (BR3, BR10), because a wrong total or a wrong
"Incorrect email or password" makes the app useless, and the debt rules of US13 (BR13, BR14),
because they are new this sprint and have three limits each. Every number in a rule, 6 and 128
characters, 7 days, today, 20 entries, one trillion dong, 60 characters, a due date, has a test on
each side of it. The language switch and the screen layouts are tested least: a mistake there is
visible at once and cheap to fix.

**Why a database in memory, not a fake repository.** Our services call the repository module
functions directly (`transaction_repo.month_totals(db, ...)`), so a fake would mean rewriting every
service to take its repository as a parameter. SQLite in memory is as fast as a fake, about 0.01
second per test, and it also runs the real SQL, which a fake would not. Each test gets its own empty
database from `backend/tests/conftest.py`, so tests never touch `backend/expense.db` and never
affect one another.

---

## 2. Test cases for every P0 story

_Written in #157, next commit: at least three test cases per P0 story._

---

## 3. Automated tests

_Written in #161: the command, the screenshot of its output, and which file holds which test
case. Until then: `pytest` in the cloned folder runs every test (`docs/SETUP.md`, section 7)._

---

## 4. What the tests found

_Written in #161: bug #142, found by the boundary tests of BR5, and a rule broken on purpose._
