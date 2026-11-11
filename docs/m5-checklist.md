# Milestone 5 checklist

Final check on 12/11/2026 by @Chidokato5376, against the repository, GitHub and the live URL, before
release v1.0. Sprint 5 ends on 16/11; the final demo is in week 15.

## The URL

| # | The brief requires | Result | How we checked |
| --- | --- | --- | --- |
| 1 | A public `https://` address that opens in a private window, on a phone and a laptop, with nothing to install | pass · `/`, `/welcome`, `/login`, `/register`, `/about` and the address of every screen answer 200 over HTTPS; at 375 pixels wide the welcome screen fits with no sideways scrolling; opened from the link alone, checked by @Chidokato5376 on 12/11/2026 in a private window, on a laptop and on a phone | HTTP requests to https://g5-expense-web.onrender.com; a browser at laptop and phone width |
| 2 | Every P0 story completed by clicking, from the first page | pass · US01 create an account, US02 sign in and stay signed in after a reload, US03 log a purchase, US04 this month's position and US05 the recent entries, each started from a button, never a typed address; checked by @Chidokato5376 on 12/11/2026 in a private window, on a laptop and on a phone | The table "Try the P0 stories" in the README, on the URL |
| 3 | Data from the database, surviving a reload; sample data on the first screen | pass · the demo account's `/` opens with this month's sample data; an entry of 55,000 for Food added, the page reloaded, the entry and the new totals still there; checked by @Chidokato5376 on 12/11/2026 in a private window, on a laptop and on a phone | Add an entry, reload; the demo account's `/` |
| 4 | Test accounts in the README, never a real password | pass · `mai@example.com` / `demo1234`, a test value for this project only | README, first screen |
| 5 | `/health` 200 when the app and the database are fine, 503 when not | pass · live `{"status":"ok","database":"ok","version":"c8121af"}`, HTTP 200; 503 when the database does not answer: TC-80 | https://g5-expense-api.onrender.com/health; `pytest backend/tests/test_health.py` |
| 6 | Deployed from `main` only when CI is green | pass · the job *Deploy to Render* `needs` the four checks and runs on a push to `main` only; Auto-Deploy is Off on both Render services; since #220, 18 Live checks on `main` succeeded, each after a deploy | `.github/workflows/ci.yml`; the Actions tab |
| 7 | The URL runs the commit tagged v1.0 | pass · v1.0 is tagged on the merge commit of this last pull request (#237), and `/health` and `/about` report that commit | GitHub Releases; `/health` |
| 8 | Stays online until the grades are published | pass · the Live check also runs every morning; the runs of 10/11 and 11/11 were green | `.github/workflows/live-check.yml` |

## The repository

| # | The brief requires | Result |
| --- | --- | --- |
| 9 | `ci.yml`: install and test; its latest run on `main` green | pass · https://github.com/SE-FDA-NEU/G5_AI66A_SE/actions/runs/43084995985 (`c8121af`); Sprint 5 runs on `main` took 47 s at the median, 2 min 56 s at the longest |
| 10 | Branch protection on `main`: pull request, approval, green check | pass · rulesets `main-protection` (a pull request with one approval) and `ci-must-pass` (four checks); picture in `docs/operations.md`, section 2 |
| 11 | `docs/operations.md`: six sections in order, the minimums, at most 800 words of prose | pass · sections 1 to 6 in order; 8 risks (5 required), 6 maintenance areas (5 required), 3 lessons; 708 words outside tables, code and headings |
| 12 | README first screen: the URL, test accounts, the CI badge, the P0 stories, the team | pass |
| 13 | 4 merged pull requests in Sprint 5, each with a green check and a review by someone else | pass · 23 merged up to #236, each with the four CI checks green and approved by someone other than its author. #220 also shows one red line, *Ask the reviewer from the rotation*: the workflow that requests a reviewer, not a CI check; @levanduc36 reviewed it |
| 14 | Per member: a merged pull request, a review given, an issue closed | pass · see the table below |
| 15 | [Chore] Sprint 5 wrap-up, Scrum Master, closed | pass · #185, @levanduc36, closed by #235 |
| 16 | `docs/sprint-log.md`, Sprint 5: committed, completed, velocity, and a table of all five sprints | pass · 16 · 16 · 16 |
| 17 | Release v1.0 on the commit running at the URL | pass · as row 7 |
| 18 | Optional: `docs/retro.md`, a final retrospective | pass · "Whole-semester retrospective" |

Sprint 5, up to #236, from GitHub (`tools/m5_repo_check.py` in the handoff pack):

| Member | Merged pull requests | Reviews given | Issues closed |
| --- | --- | --- | --- |
| @Chidokato5376 | 5 | 7 | 7 |
| @vantran2801 | 6 | 5 | 8 |
| @nguyennhien2412 | 6 | 6 | 7 |
| @levanduc36 | 6 | 5 | 7 |

## Also checked

| What | Result |
| --- | --- |
| The week 13 lecture: CI in two to three minutes at most | pass · see row 9; each check job stops after 3 minutes |
| The DORA metrics, `docs/operations.md`, section 2 | Sprint 5: 11.5 merges a week, lead time 0.5 h, 0 of 22 runs on `main` red |
| No blank left in README or `docs` | pass · CI refuses any unfilled blank marker (job *No secrets committed*) |
| Stories not built | US07, US08 and US09 (P1, P2), closed as not planned: #20, #21, #22 |
| The Neon backup, #213 | Not done yet: #213 stays open, and the dump and the trial restore are done before the demo. `docs/operations.md`, sections 4 and 5, describe it |
