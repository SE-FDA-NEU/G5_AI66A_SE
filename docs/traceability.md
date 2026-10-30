# Traceability

Every story traces forward to the screen, endpoint and table that serve it, the rules it relies
on, and the issue that builds it. Keep it current: a pull request that adds a route, an endpoint or
a table without updating this file should not be approved (`docs/definition-of-done.md`, item 8).

## Stories

| Story | Priority | Screen | Endpoint | Table | Rules | Story issue | Sprint | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US01 Create an account | P0 | `/register` | `POST /api/users` | users | BR1, BR2 | [#14] | 3 | Done |
| US02 Sign in and stay signed in | P0 | `/login` | `POST /api/auth/login` · `GET /api/auth/me` | users | BR2, BR3, BR10 | [#15] | 2 | Done |
| US03 Log a purchase in seconds | P0 | `/transactions/new` | `POST /api/transactions` · `GET /api/categories` | transactions, categories | BR4, BR5, BR6, BR11 | [#16] | 3 | Done |
| US04 This month's position | P0 | `/` | `GET /api/summary` | transactions | BR4 | [#17] | 3 | Done |
| US05 Look back over recent entries | P0 | `/` | `GET /api/transactions` | transactions, categories | BR4 | [#18] | 2 | Done |
| US06 Correct or remove an entry | P1 | `/transactions/:id` | `GET`, `PATCH` and `DELETE /api/transactions/{id}` | transactions | BR4, BR5, BR6, BR11 | [#19] | 4 | Done |
| US07 Suggest the kind of spending | P1 | `/transactions/new` | `GET /api/categories/suggestions` | categories | BR6 | [#20] | Backlog | Not started |
| US08 Cap spending for a month | P1 | `/budget` | `PUT` and `GET /api/budgets` | budgets | BR7, BR8 | [#21] | Backlog | Not started |
| US09 Warn before the cap is reached | P2 | `/` | `GET /api/budgets?month=` | budgets, transactions | BR9 | [#22] | Backlog | Not started |
| US10 See which kinds of spending took the most | P2 | `/stats`, and a card on `/` | `GET /api/stats/breakdown` | transactions, categories | BR4, BR6 | [#23] | 4 | Done |
| US11 Choose the app's language | P2 | every screen | none: the app translates what the API sends | none | BR3 | [#72] | 2 | Done |
| US12 See how spending changes month by month | P1 | `/stats`, and a card on `/` | `GET /api/stats/months` · `GET /api/stats/years` | transactions | BR4, BR12 | [#140] | 4 | Done |
| US13 Keep track of debts and loans | P1 | `/debts`, `/debts/new`, and a card on `/` | `GET` and `POST /api/debts` · `POST /api/debts/{id}/settle` · `DELETE /api/debts/{id}` | debts | BR4, BR5, BR11, BR13, BR14 | [#141] | 4 | Done |

**Built in Sprint 2.** US02 by #58, #60, #61, #63 and #64; US05 by #60, #61, #62, #63 and #65. The
pull request of #65 closes both stories and sets their Status to Done. US11, added on 28/09, is
built by #73, whose pull request closes it and sets its Status to Done.

**Built in Sprint 3.** Every story relies on #94, which gives each error a code, and #103, which
shows it as a message and a hint (`docs/ui.md`, section 3).

| Story | API | Database | Tests | Screen, whose pull request closes the story |
| --- | --- | --- | --- | --- |
| US01 | #97 `POST /api/users` | users, as built in Sprint 2 | #100 `test_users.py` | #104 `/register` |
| US03 | #98 `POST /api/transactions`, `GET /api/categories` | #96 `category_repo.get_by_id` | #101 `test_new_entry.py` | #105 `/transactions/new` |
| US04 | #99 `GET /api/summary` | #96 `transaction_repo.month_totals`; #95 keeps the demo inside the month | #95 `test_seed.py`, #101 `test_summary.py` | #106 `/` |

**Built in Sprint 4.** Every story's test cases are listed by ID in `docs/testing.md`, section 2,
and the tests carry the same IDs in their names.

| Story | Database | API and its tests | Screen, whose pull request closes the story |
| --- | --- | --- | --- |
| US06 | #144 `transaction_repo.get_for_account`, `update`, `delete` | #146 rows 9 to 11 of `docs/design.md`, section 3; TC-46 to TC-52 | #152 `/transactions/:id` |
| US10 | #148 `transaction_repo.spending_by_category` | #150 row 12; TC-53 to TC-57 | #156 `/stats`; #159 the card on `/` |
| US12 | #148 `totals_by_month`, `totals_by_year`; #155 eleven earlier months | #150 rows 13 and 14; TC-58 to TC-65 | #156 `/stats`; #159 the card on `/` |
| US13 | #151 table `debts`, migration `0002`; #155 four debts | #154 rows 15 to 18; TC-66 to TC-78 | #158 `/debts`, `/debts/new`; #159 the card on `/` |

The P0 stories got their test case IDs in Sprint 4 too: US01 to US03 by #147 and #153,
US04 by #145, US05 by #149. Bug #142 gave BR5 its upper limit.

**Sprint** is the sprint the story is committed to; Backlog until a sprint planning picks it.
**Status:** Not started / In progress / Done.

## Screens

| Route | Purpose | Access | Priority | Stories |
| --- | --- | --- | --- | --- |
| `/login` | Sign in to reach your own records | G | P0 | US02 |
| `/register` | Create an account and enter immediately | G | P0 | US01 |
| `/` | This month's income, spending, remainder; cap warnings; recent entries; on a wide screen, cards for US10, US12 and US13 | U | P0 | US04, US05, US09, US10, US12, US13 |
| `/transactions/new` | Log one amount of money spent or received | U | P0 | US03, US07 |
| `/transactions/:id` | Correct or remove one entry; opened by tapping a row on `/` | U | P1 | US06 |
| `/budget` | Set and read monthly caps per kind of spending | U | P1 | US08 |
| `/stats` | Spending month by month and year by year; one month by kind of spending | U | P1 | US10, US12 |
| `/debts` | Money borrowed and lent: who, how much, by when; mark it settled | U | P1 | US13 |
| `/debts/new` | Write down one debt or loan | U | P1 | US13 |

**Access:** G guest, not signed in · U signed-in user. No route needs A this semester: every
account reads and changes only its own entries (BR4).

## Business rules

The rule text is copied word for word from section 5 of `docs/requirements.md`. Change it there
first, then here. Test cases are named by their ID from `docs/testing.md`, section 2; each is a test in
`backend/tests/` with that ID in its name. A file name is a test without an ID.

| # | Rule | Enforced where | Tested by |
| --- | --- | --- | --- |
| BR1 | An email address identifies exactly one account, ignoring capitalisation. | Database: UNIQUE `users.email` with CHECK `email = lower(email)`; `user_repo.normalise_email`; `auth_service.register` answers 409 `email_taken` | TC-02, TC-03, TC-10 · `test_database_rules.py` |
| BR2 | A password is 6 to 128 characters and is never stored or shown as plain text. | `app/core/security.py`: PBKDF2-SHA256; `auth_service.register` answers 422 `password_length` | TC-04 to TC-07 · `test_users.py`, `test_auth.py`: the hash tests |
| BR3 | A failed sign-in returns the same message whether the email is unknown or the password is wrong. | `auth_service.authenticate`: one status, one sentence, a decoy hash | TC-11 to TC-13 · `mobile/__tests__/i18n.test.js` |
| BR4 | An account can read and change only its own entries. | Every query in `transaction_repo` and `debt_repo` filters on the account of the token; another account's id answers 404, never 403 | TC-38, TC-43, TC-48, TC-78 · `test_repositories.py` · `test_database_rules.py` |
| BR5 | An amount is a whole number of dong, greater than zero and at most 1,000,000,000,000. | Database: CHECK `amount > 0` on integer columns; `transaction_service.check_amount`, for entries, corrections and debts | TC-19 to TC-26, TC-50, TC-75 · `test_database_rules.py` |
| BR6 | An entry has at most one kind of spending, chosen from Food, Transport, Shopping, Bills, Entertainment, Health, Education and Other. A suggestion never overrides what the user picks, and when nothing matches, nothing is suggested. | One nullable FK `transactions.category_id`; `transaction_service.check_entry` answers 422 `unknown_category` | TC-17, TC-30, TC-56 · US07, later |
| BR7 | There is at most one cap per account, per kind of spending, per month. | Database: UNIQUE (`user_id`, `category_id`, `month`) on `budgets` | `test_database_rules.py` · US08, later |
| BR8 | A cap applies only to spending, never to money received: Salary, Bonus or Other income. | Service, when a cap is saved (US08) | US08, later |
| BR9 | A cap warns at 70% of the figure and turns to an over-budget warning above 100%. | Overview `/`, each time it loads (US09) | US09, later |
| BR10 | A session lasts 7 days from sign-in, then the password is required again. | `app/core/security.py`: the token expires 7 days after sign-in; `deps.get_current_user` refuses it; in the app, `src/api/session.js` | TC-14 to TC-16 · `mobile/__tests__/session.test.js` |
| BR11 | An entry cannot be dated later than today. | `transaction_service.check_entry` and `debt_service.add_debt` answer 422 `date_in_future`; the seed never writes a later date | TC-27 to TC-29, TC-51, TC-52, TC-76 · `test_seed.py` |
| BR12 | Months and years are compared on money spent. The month with the most spent and the month with the least are chosen among the months up to this one that have at least one entry; on a tie, the earlier month. A year later than this one cannot be chosen. | `stats_service.busiest_and_quietest` and `read_year` | TC-58 to TC-65 |
| BR13 | A debt names who the money is with in 1 to 60 characters, and its amount follows BR5. It started today or earlier (BR11), and its due date, if it has one, is not before the day it started. | Database: CHECK on `debts.person` length and `due_on >= started_on`; `debt_service.add_debt` answers 422 `person_length` or `due_before_start` | TC-72 to TC-76 · `test_database_rules.py` |
| BR14 | An open debt is overdue from the day after its due date; on the due date itself it is not yet overdue. A settled debt is never overdue and cannot be settled twice. | `debt_service.is_overdue` and `settle_debt`, 409 `already_settled`; the app's words in `src/utils/debts.js` | TC-68 to TC-71 · `mobile/__tests__/debts.test.js` |

[#14]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/14
[#15]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/15
[#16]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/16
[#17]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/17
[#18]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/18
[#19]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/19
[#20]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/20
[#21]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/21
[#22]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/22
[#23]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/23
[#72]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/72
[#140]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/140
[#141]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/141
