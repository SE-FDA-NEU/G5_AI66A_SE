# Milestone 4 checklist

Checked by @levanduc36 on 01/11/2026, against `docs/testing.md`, `docs/SETUP.md` and the README on
this branch, and against GitHub on the same day.

## The testing document

| # | The brief requires | Result | Where |
| --- | --- | --- | --- |
| 1 | `docs/testing.md` in Markdown, four sections in order | pass · 1 What we test, and why · 2 Test cases for every P0 story · 3 Automated tests · 4 What the tests found | headings |
| 2 | Section 1: one row per layer, services, repository, routes, interface, with its kind of test or why none; two or three sentences on risk | pass · four rows; the risk paragraph names the money, sign-in and debt rules | §1 |
| 3 | Section 2: ID · Story · Input · Expected result · Kind, every P0 story with 3 or more cases, at least one normal and one error | pass · US01 8, US02 8, US03 14, US04 8, US05 7 test cases; 33 more for US06, US10, US12, US13 | §2 |
| 4 | Section 2: a rule with a number has boundary cases on both sides | pass · BR2 5/6/128/129 characters, BR10 7 days ± 1 minute, BR5 0/1 and 1,000,000,000,000 ± 1, BR11 today/tomorrow, US04 the month's first and last day, US05 20/21, BR13 60/61 characters and the start date, BR14 the due date | §2 |
| 5 | Section 3: every test case of section 2 is a pytest test in `tests/` with its ID in the name or a comment | pass · TC-01 to TC-78 all in `backend/tests/`, IDs in the names; `pytest --collect-only -q` lists them | §3 |
| 6 | Section 3: one command runs them all, without a server and without the real database; the command and a screenshot | pass · `pytest`, 177 passed; `docs/images/testing/pytest-output.png` | §3 |
| 7 | Section 4: a bug the tests found, its issue, the fix and the test that guards it | pass · bug #142, the BR5 upper limit, TC-24 to TC-26; and BR14 broken on purpose, with its red output | §4 |
| 8 | `docs/SETUP.md` still works and says how to run the tests | pass · section 7, and step 12 of section 6 | SETUP.md |

## The five checks of the Sprint 4 Review

| # | Check | Result | How we checked |
| --- | --- | --- | --- |
| 9 | Clone and follow `docs/SETUP.md`: the app runs with no errors | pass · a fresh clone into a new folder on 01/11/2026 | SETUP.md §1 to §6 |
| 10 | Type `pytest`: all tests pass, with no hand edits | pass · 177 passed on the fresh clone; CI runs the same command from the root on every pull request | SETUP.md §7 |
| 11 | Pick a P0 story in `docs/testing.md`: 3 or more test cases, an error case among them | pass · row 3 | §2 |
| 12 | Read one test for a rule with a number limit: both sides of the limit | pass · for example `test_tc04_to_tc07_a_password_has_6_to_128_characters` | `test_users.py` |
| 13 | Pick one test case ID: its pytest test exists and passes | pass · `pytest -k tc15` runs TC-15, the session at exactly 7 days | `test_auth.py` |

## The repository

From `m4_repo_check.py`, run on 01/11/2026 after #139 merged, over #138 to #161 and the stories #19, #23, #140 and #141.

| Check | Minimum | Result |
| --- | --- | --- |
| Merged pull requests in Sprint 4, each reviewed by someone else | 4 | pass · 21 merged before this one |
| Issues closed in Sprint 4 | 5 | pass · 25 closed |
| Per member: a merged pull request, a review given, an issue closed | 1 each | pass |
| Per member: a test in `backend/tests/` | 1 each | pass · see `docs/testing.md`, section 3 |
| `docs/SETUP.md` on `main`, with how to run the tests | yes | pass |
| [Chore] Refine backlog for Sprint 4, PO, closed | 1 | pass · #138 |
| [Chore] Sprint 4 wrap-up, SM, closed | 1 | pass · #139 |
| `docs/sprint-log.md`, Sprint 4: committed, completed, velocity | yes | pass · 18 · 18 · 18 |
| Scrum Master named in the README, not the one of Sprint 3 | yes | pass · @Chidokato5376, after @levanduc36 |
| Optional: `docs/retro.md`, Sprint 4, one action with one owner | yes | pass · @levanduc36 |
