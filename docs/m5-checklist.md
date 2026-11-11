# Milestone 5 checklist

Interim status checked on 2026-11-12 against the repository, GitHub and the live endpoints. This is
not final sign-off: Sprint 5 ends on 16/11, #212 is still open, v1.0 has not been released, and the
final interactive demo has not happened yet.

## The URL

| # | The brief requires | Result | How we checked |
| --- | --- | --- | --- |
| 1 | A public `https://` address that opens in a private window, on a phone and a laptop, with nothing to install | URL returned HTTP 200 on 2026-11-12; private-window, phone and laptop checks are pending | HTTP request to the public URL; interactive checks remain for the final demo |
| 2 | Every P0 story completed by clicking, from the first page | Pending — the final browser walkthrough has not happened | The table "Try the P0 stories" in the README, to be checked on the URL |
| 3 | Data from the database, surviving a reload; sample data on the first screen | Pending — persistence and sample data have not been checked in the final demo | Save an entry, reload the page, and inspect the demo account's `/` |
| 4 | Test accounts in the README, never a real password | pass · `mai@example.com` / `demo1234` | README, first screen |
| 5 | `/health` 200 when the app and the database are fine, 503 when not | Pass — live `/health` returned 200 on 2026-11-12; TC-80 test passed for the 503 case | https://g5-expense-api.onrender.com/health; `pytest backend/tests/test_health.py -k tc80` |
| 6 | Deployed from `main` only when CI is green | pass · the job *Deploy to Render* `needs` the four checks and runs on a push to `main` only | `.github/workflows/ci.yml` |
| 7 | The URL runs the commit tagged v1.0 | Pending — `/health` reports `3b27e75`; v1.0 has not been released | https://g5-expense-api.onrender.com/health; GitHub releases |
| 8 | Stays online until the grades are published | the live check runs every morning | `.github/workflows/live-check.yml` |

## The repository

| # | The brief requires | Result |
| --- | --- | --- |
| 9 | `ci.yml`: install and test; its latest run on `main` green | Pass — latest checked run succeeded on `3b27e7571a989c06de3bdca6aa5a3226118b7a9f` | https://github.com/SE-FDA-NEU/G5_AI66A_SE/actions/runs/43081913655 |
| 10 | Branch protection on `main`: pull request, approval, green check | pass · rulesets `main-protection` and `ci-must-pass`; `docs/operations.md`, section 2 |
| 11 | `docs/operations.md`: six sections in order, the minimums, at most 800 words of prose | Pending — final structure and word-count audit has not been recorded; `tools/m5_repo_check.py` is not present in this checkout |
| 12 | README first screen: the URL, test accounts, the CI badge, the P0 stories, the team | pass |
| 13 | 4 merged pull requests in Sprint 5, each with a green check and a review by someone else | Pending — final Sprint 5 audit is not recorded; PR #236 is still open |
| 14 | Per member: a merged pull request, a review given, an issue closed | Pending — per-member GitHub evidence audit is not recorded |
| 15 | [Chore] Sprint 5 wrap-up, Scrum Master, closed | #185 |
| 16 | `docs/sprint-log.md`, Sprint 5: committed, completed, velocity, and a table of all five sprints | pass · 16 · 16 · 16 |
| 17 | Release v1.0 on the commit running at the URL | Pending — no v1.0 release exists yet |
| 18 | Optional: `docs/retro.md`, a final retrospective | pass · "Whole-semester retrospective" |
