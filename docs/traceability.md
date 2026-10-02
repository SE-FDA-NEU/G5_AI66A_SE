# Traceability

Every story traces forward to the screen, endpoint and table that serve it, the rules it relies
on, and the issue that builds it. Keep it current: a pull request that adds a route, an endpoint or
a table without updating this file should not be approved (`docs/definition-of-done.md`, item 8).

## Stories

| Story | Priority | Screen | Endpoint | Table | Rules | Story issue | Sprint | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US01 Create an account | P0 | `/register` | `POST /api/users` | users | BR1, BR2 | [#14] | Backlog | Not started |
| US02 Sign in and stay signed in | P0 | `/login` | `POST /api/auth/login` · `GET /api/auth/me` | users | BR2, BR3, BR10 | [#15] | 2 | In progress |
| US03 Log a purchase in seconds | P0 | `/transactions/new` | `POST /api/transactions` · `GET /api/categories` | transactions, categories | BR5, BR6, BR11 | [#16] | Backlog | Not started |
| US04 This month's position | P0 | `/` | `GET /api/summary` | transactions | BR4 | [#17] | Backlog | Not started |
| US05 Look back over recent entries | P0 | `/` | `GET /api/transactions` | transactions, categories | BR4 | [#18] | 2 | In progress |
| US06 Correct or remove an entry | P1 | `/transactions/:id` | `PATCH` and `DELETE /api/transactions/{id}` | transactions | BR4, BR5, BR11 | [#19] | Backlog | Not started |
| US07 Suggest the kind of spending | P1 | `/transactions/new` | `GET /api/categories/suggestions` | categories | BR6 | [#20] | Backlog | Not started |
| US08 Cap spending for a month | P1 | `/budget` | `PUT` and `GET /api/budgets` | budgets | BR7, BR8 | [#21] | Backlog | Not started |
| US09 Warn before the cap is reached | P2 | `/` | `GET /api/budgets?month=` | budgets, transactions | BR9 | [#22] | Backlog | Not started |
| US10 See which kinds of spending took the most | P2 | `/stats` | `GET /api/stats/breakdown` | transactions, categories | BR6 | [#23] | Backlog | Not started |
| US11 Choose the app's language | P2 | every screen | none: the app translates what the API sends | none | BR3 | [#72] | 2 | In progress |

**Built in Sprint 2.** US02 by #58, #60, #61, #63 and #64; US05 by #60, #61, #62, #63 and #65. The
pull request of #65 closes both stories and sets their Status to Done. US11, added on 28/09, is
built by #73, whose pull request closes it and sets its Status to Done.

**Sprint** is the sprint the story is committed to; Backlog until a sprint planning picks it.
**Status:** Not started / In progress / Done.

## Screens

| Route | Purpose | Access | Priority | Stories |
| --- | --- | --- | --- | --- |
| `/login` | Sign in to reach your own records | G | P0 | US02 |
| `/register` | Create an account and enter immediately | G | P0 | US01 |
| `/` | This month's income, spending, remainder; cap warnings; recent entries | U | P0 | US04, US05, US09 |
| `/transactions/new` | Log one amount of money spent or received | U | P0 | US03, US07 |
| `/transactions/:id` | Correct or remove one entry | U | P1 | US06 |
| `/budget` | Set and read monthly caps per kind of spending | U | P1 | US08 |
| `/stats` | Breakdown of one month by kind of spending | U | P2 | US10 |

**Access:** G guest, not signed in · U signed-in user. No route needs A this semester: every
account reads and changes only its own entries (BR4).
