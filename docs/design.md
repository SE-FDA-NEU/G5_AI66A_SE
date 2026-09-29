# Design — Personal Expense Management App

**Team 05 · AI66A**
Milestone 2 · Sprint 2 · Weeks 7–8

How the product described in [`docs/requirements.md`](requirements.md) is built, and the walking
skeleton that proves it runs end to end. The install steps for a machine that has never seen the
project are in [`docs/SETUP.md`](SETUP.md).

---

## 1. Architecture

_Written in #68._

---

## 2. Data model

_Written in #67._

---

## 3. API design

A REST API over HTTP with JSON bodies, served by FastAPI under `/api`. Its interactive
documentation, generated from the code, is at `http://localhost:8000/docs` once the backend runs.

**Signing in.** `POST /api/auth/login` returns a token. Every other `/api` endpoint expects it in
the header `Authorization: Bearer <token>`. The token names the account and expires 7 days after
sign-in (BR10), so the server keeps no session table.

**Errors.** Every error answers with one sentence, `{"detail": "<message>"}`. The messages are the
exact ones in the acceptance criteria, always in English; the app shows each sentence it knows in
the language the user chose (US11), and any other sentence as it came. The status says whose
mistake it was: **400** a malformed request, such as a missing field or a `limit` outside 1 to
100; **401** not signed in (BR3, BR10); **409** a conflict with what is stored (BR1); **422** a
well-formed request that breaks a business rule, checked in the service (BR2, BR5, BR6, BR8, BR11).

**Paths name things.** Collections are plural nouns and the HTTP method is the verb, so creating
an account is `POST /api/users`. Signing in creates no stored row and fits no collection, so it is
a small sub-resource named as a noun, a login: `POST /api/auth/login`.

| # | Method | Path | Input | Success output | Error codes | Story | Built in |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | POST | `/api/users` | JSON `email`, `password` | **201** · `access_token`, `expires_at`, `user {id, email}`: the new account is already signed in | **409** "This email is already registered" _(BR1)_ · **422** "Password must be 6 to 128 characters" _(BR2)_ · **400** "Enter a valid email address" | US01 | Sprint 3 |
| 2 | POST | `/api/auth/login` | JSON `email`, `password` | **200** · `access_token`, `token_type` `bearer`, `expires_at` 7 days later _(BR10)_, `user {id, email}` | **401** "Incorrect email or password", the same for an unknown email, a wrong password and a malformed address _(BR3)_ | US02 | **Sprint 2** |
| 3 | GET | `/api/auth/me` | Bearer token | **200** · `{id, email}` of the signed-in account | **401** "Please sign in again": no token, a forged one, or one older than 7 days _(BR10)_ | US02 | **Sprint 2** |
| 4 | GET | `/api/transactions` | Bearer token · query `limit`, 1 to 100, 20 by default | **200** · `items`: the account's entries, newest first, each `{id, kind, amount, note, occurred_on, category {id, name, kind} or null}` · `total`: how many it has in all | **401** "Please sign in again" · **400** when `limit` is outside 1 to 100 | US05 _(BR4)_ | **Sprint 2** |
| 5 | POST | `/api/transactions` | Bearer token · JSON `kind` (`expense` or `income`), `amount`, `note`, `occurred_on`, `category_id` or null | **201** · the stored entry, in the shape of row 4 | **422** "Enter an amount greater than 0" _(BR5)_ · **422** "The date cannot be in the future" _(BR11)_ · **422** "Choose a kind of spending from the list" _(BR6)_ · **401** | US03 | Sprint 3 |
| 6 | GET | `/api/categories` | Bearer token | **200** · the 11 categories, `{id, name, kind}`, kinds of spending first | **401** "Please sign in again" | US03 | Sprint 3 |
| 7 | GET | `/api/summary` | Bearer token · query `month` as `YYYY-MM`, this month by default | **200** · `{month, income, spending, remaining, count}` for that month | **401** · **400** "Month must be written YYYY-MM" | US04 _(BR4)_ | Sprint 3 |
| 8 | GET | `/health` | none | **200** · `{"status": "ok"}` | none | all | **Sprint 2** |

Rows 1 to 7 cover all five P0 stories. Four endpoints are built this sprint; the other four are
designed now so that Sprint 3 builds against a fixed contract.

**Planned for the P1 and P2 stories:** `PATCH` and `DELETE /api/transactions/{id}` for US06,
answering **404** for another account's entry rather than 403, so its existence is never confirmed
_(BR4)_; `GET /api/categories/suggestions?note=` for US07; `PUT` and `GET /api/budgets` for US08 and
US09, with **422** "Caps apply to spending only" _(BR8)_; `GET /api/stats/breakdown?month=` for
US10.

---

## 4. Walking skeleton

_Written in #68._

---

## 5. Design decisions

_Written in #69._

---

## 6. What changed since M1

_Written in #71._
