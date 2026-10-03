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

## Business rules

The rule text is copied word for word from section 5 of `docs/requirements.md`. Change it there
first, then here. Test names are in `backend/tests/` unless a path says otherwise.

| # | Rule | Enforced where | Tested by |
| --- | --- | --- | --- |
| BR1 | An email address identifies exactly one account, ignoring capitalisation. | Database: UNIQUE `users.email` with CHECK `email = lower(email)`; `user_repo.normalise_email` lowers every address | `test_database_rules.py`: `test_the_same_address_in_capitals_cannot_make_a_second_account`, `test_an_address_is_never_stored_in_capitals` · `test_auth.py`: `test_sign_in_ignores_capitals_in_the_address` · US01 criterion 2, Sprint 3 |
| BR2 | A password is 6 to 128 characters and is never stored or shown as plain text. | `app/core/security.py`: `hash_password`, PBKDF2-SHA256; no response schema carries the hash. The 6-to-128 check arrives with US01 | `test_auth.py`: `test_password_is_stored_only_as_a_hash` · US01 criterion 3, Sprint 3 |
| BR3 | A failed sign-in returns the same message whether the email is unknown or the password is wrong. | `app/services/auth_service.py`: `authenticate` gives one status and one sentence for every failure, and checks a decoy hash so both take as long | `test_auth.py`: `test_every_failed_sign_in_gets_the_same_answer`, for a wrong password, an unknown email and a malformed email · `mobile/__tests__/i18n.test.js`: the same sentence in Vietnamese · US02 criterion 3, US11 criterion 3 |
| BR4 | An account can read and change only its own entries. | `app/db/repositories/transaction_repo.py`: every query filters on the account id taken from the token; FK `transactions.user_id` | `test_transactions.py`: `test_the_list_never_shows_another_accounts_entries` · `test_database_rules.py`: `test_an_entry_must_belong_to_an_existing_account` · US06 criterion 3, later |
| BR5 | An amount is a whole number of dong, greater than zero. | Database: CHECK `amount > 0` on an integer column. The API message arrives with US03 | `test_database_rules.py`: `test_an_amount_must_be_greater_than_zero`, for 0 and −20,000 · US03 criterion 4, Sprint 3 |
| BR6 | An entry has at most one kind of spending, chosen from Food, Transport, Shopping, Bills, Entertainment, Health, Education and Other. A suggestion never overrides what the user picks, and when nothing matches, nothing is suggested. | Database: a single nullable FK `transactions.category_id`. The suggestion arrives with US07; the server stores the kind the app sends | US03 criterion 2 · US07 criteria 2 and 4, later |
| BR7 | There is at most one cap per account, per kind of spending, per month. | Database: UNIQUE (`user_id`, `category_id`, `month`) on `budgets` | `test_database_rules.py`: `test_there_is_one_cap_per_account_kind_of_spending_and_month` · US08 criterion 2, later |
| BR8 | A cap applies only to spending, never to money received: Salary, Bonus or Other income. | Service, when a cap is saved (US08): a CHECK constraint cannot look at another table | US08 criterion 3, later |
| BR9 | A cap warns at 70% of the figure and turns to an over-budget warning above 100%. | Overview `/`, each time it loads (US09) | US09 criteria 1 to 4, later |
| BR10 | A session lasts 7 days from sign-in, then the password is required again. | `app/core/security.py`: the token expires 7 days after sign-in; `app/core/deps.py`: `get_current_user` refuses it after that. In the app, `src/api/session.js`: `isExpired` | `test_auth.py`: `test_a_sign_in_lasts_seven_days`, `test_the_token_expires_seven_days_after_sign_in` · `mobile/__tests__/session.test.js` · US02 criterion 2 |
| BR11 | An entry cannot be dated later than today. | `scripts/seed_data.py` never writes a later date; `POST /api/transactions` refuses one from Sprint 3. A SQLite CHECK cannot read today's date | `test_seed.py`: `test_no_entry_is_dated_later_than_today` · US03 criterion 5, Sprint 3 |

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
