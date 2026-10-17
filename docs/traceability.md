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
| US06 Correct or remove an entry | P1 | `/transactions/:id` | `PATCH` and `DELETE /api/transactions/{id}` | transactions | BR4, BR5, BR11 | [#19] | Backlog | Not started |
| US07 Suggest the kind of spending | P1 | `/transactions/new` | `GET /api/categories/suggestions` | categories | BR6 | [#20] | Backlog | Not started |
| US08 Cap spending for a month | P1 | `/budget` | `PUT` and `GET /api/budgets` | budgets | BR7, BR8 | [#21] | Backlog | Not started |
| US09 Warn before the cap is reached | P2 | `/` | `GET /api/budgets?month=` | budgets, transactions | BR9 | [#22] | Backlog | Not started |
| US10 See which kinds of spending took the most | P2 | `/stats` | `GET /api/stats/breakdown` | transactions, categories | BR6 | [#23] | Backlog | Not started |
| US11 Choose the app's language | P2 | every screen | none: the app translates what the API sends | none | BR3 | [#72] | 2 | Done |

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
| BR1 | An email address identifies exactly one account, ignoring capitalisation. | Database: UNIQUE `users.email` with CHECK `email = lower(email)`; `user_repo.normalise_email` lowers every address; `auth_service.register` answers 409 `email_taken` before the database has to | `test_database_rules.py`: `test_the_same_address_in_capitals_cannot_make_a_second_account`, `test_an_address_is_never_stored_in_capitals` · `test_auth.py`: `test_sign_in_ignores_capitals_in_the_address` · `test_users.py`: `test_an_address_already_registered_is_refused`, `test_capitals_are_stored_in_lower_case` · US01 criterion 2 |
| BR2 | A password is 6 to 128 characters and is never stored or shown as plain text. | `app/core/security.py`: `hash_password`, PBKDF2-SHA256; no response schema carries the hash. `auth_service.register` answers 422 `password_length` outside 6 to 128 | `test_auth.py`: `test_password_is_stored_only_as_a_hash` · `test_users.py`: `test_a_password_outside_6_to_128_characters_is_refused`, `test_6_and_128_characters_are_accepted`, `test_the_password_is_stored_only_as_a_hash` · US01 criterion 3 |
| BR3 | A failed sign-in returns the same message whether the email is unknown or the password is wrong. | `app/services/auth_service.py`: `authenticate` gives one status and one sentence for every failure, and checks a decoy hash so both take as long | `test_auth.py`: `test_every_failed_sign_in_gets_the_same_answer`, for a wrong password, an unknown email and a malformed email, all with code `incorrect_sign_in` · `mobile/__tests__/i18n.test.js`: the same sentence in Vietnamese, picked by its code · US02 criterion 3, US11 criterion 3 |
| BR4 | An account can read and change only its own entries. | `app/db/repositories/transaction_repo.py`: every query filters on the account id taken from the token, `month_totals` included; a new entry takes its account from the token, never from the request; FK `transactions.user_id` | `test_transactions.py`: `test_the_list_never_shows_another_accounts_entries` · `test_database_rules.py`: `test_an_entry_must_belong_to_an_existing_account` · `test_summary.py`: `test_another_accounts_entries_never_count` · `test_new_entry.py`: `test_the_entry_belongs_to_the_account_that_logged_it` · US06 criterion 3, later |
| BR5 | An amount is a whole number of dong, greater than zero. | Database: CHECK `amount > 0` on an integer column. `transaction_service.log_entry` answers 422 `amount_not_positive` for an empty, zero or negative amount; a fraction of a dong is a malformed request, 400 | `test_database_rules.py`: `test_an_amount_must_be_greater_than_zero`, for 0 and −20,000 · `test_new_entry.py`: `test_an_amount_that_is_not_above_0_is_refused`, `test_a_fraction_of_a_dong_is_malformed` · `mobile/__tests__/entryForm.test.js` · US03 criterion 4 |
| BR6 | An entry has at most one kind of spending, chosen from Food, Transport, Shopping, Bills, Entertainment, Health, Education and Other. A suggestion never overrides what the user picks, and when nothing matches, nothing is suggested. | Database: a single nullable FK `transactions.category_id`. `transaction_service.log_entry` answers 422 `unknown_category` for a category that does not exist or is of the other kind, and stores none when none is chosen. The suggestion arrives with US07 | `test_new_entry.py`: `test_no_kind_of_spending_is_allowed_and_nothing_is_guessed`, `test_a_kind_of_spending_not_on_the_list_is_refused`, `test_55000_on_food_adds_exactly_55000_to_spending` · US03 criterion 2 · US07 criteria 2 and 4, later |
| BR7 | There is at most one cap per account, per kind of spending, per month. | Database: UNIQUE (`user_id`, `category_id`, `month`) on `budgets` | `test_database_rules.py`: `test_there_is_one_cap_per_account_kind_of_spending_and_month` · US08 criterion 2, later |
| BR8 | A cap applies only to spending, never to money received: Salary, Bonus or Other income. | Service, when a cap is saved (US08): a CHECK constraint cannot look at another table | US08 criterion 3, later |
| BR9 | A cap warns at 70% of the figure and turns to an over-budget warning above 100%. | Overview `/`, each time it loads (US09) | US09 criteria 1 to 4, later |
| BR10 | A session lasts 7 days from sign-in, then the password is required again. | `app/core/security.py`: the token expires 7 days after sign-in; `app/core/deps.py`: `get_current_user` refuses it after that. In the app, `src/api/session.js`: `isExpired` | `test_auth.py`: `test_a_sign_in_lasts_seven_days`, `test_the_token_expires_seven_days_after_sign_in` · `mobile/__tests__/session.test.js` · every endpoint answers 401 with code `sign_in_again`, and the app opens `/login` · US02 criterion 2 |
| BR11 | An entry cannot be dated later than today. | `scripts/seed_data.py` never writes a later date; `transaction_service.log_entry` answers 422 `date_in_future`. A SQLite CHECK cannot read today's date | `test_seed.py`: `test_no_entry_is_dated_later_than_today` · `test_new_entry.py`: `test_a_date_after_today_is_refused`, `test_today_and_last_month_are_accepted` · US03 criterion 5 |

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
