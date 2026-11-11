# Milestone 5 checklist

Checked by @Chidokato5376 on ⟦FILL: the date of the check⟧, against the URL, the repository and
GitHub on that day, after #212 merged and v1.0 was released.

## The URL

| # | The brief requires | Result | How we checked |
| --- | --- | --- | --- |
| 1 | A public `https://` address that opens in a private window, on a phone and a laptop, with nothing to install | https://g5-expense-web.onrender.com | A private window on a laptop and on a phone |
| 2 | Every P0 story completed by clicking, from the first page | ⟦FILL: pass, or what failed⟧ | The table "Try the P0 stories" in the README, on the URL |
| 3 | Data from the database, surviving a reload; sample data on the first screen | ⟦FILL: pass, or what failed⟧ | An entry saved, the page reloaded; the demo account's `/` |
| 4 | Test accounts in the README, never a real password | pass · `mai@example.com` / `demo1234` | README, first screen |
| 5 | `/health` 200 when the app and the database are fine, 503 when not | ⟦FILL: pass, with the time it was opened⟧ | https://g5-expense-api.onrender.com/health; TC-79 and TC-80 for the 503 |
| 6 | Deployed from `main` only when CI is green | pass · the job *Deploy to Render* `needs` the four checks and runs on a push to `main` only | `.github/workflows/ci.yml` |
| 7 | The URL runs the commit tagged v1.0 | ⟦FILL: the commit /health reports, and the commit of v1.0⟧ | https://g5-expense-api.onrender.com/health and the release page |
| 8 | Stays online until the grades are published | the live check runs every morning | `.github/workflows/live-check.yml` |

## The repository

| # | The brief requires | Result |
| --- | --- | --- |
| 9 | `ci.yml`: install and test; its latest run on `main` green | https://github.com/SE-FDA-NEU/G5_AI66A_SE/actions/runs/42662453565 |
| 10 | Branch protection on `main`: pull request, approval, green check | pass · rulesets `main-protection` and `ci-must-pass`; `docs/operations.md`, section 2 |
| 11 | `docs/operations.md`: six sections in order, the minimums, at most 800 words of prose | ⟦FILL: the word count from tools/m5_repo_check.py⟧ |
| 12 | README first screen: the URL, test accounts, the CI badge, the P0 stories, the team | pass |
| 13 | 4 merged pull requests in Sprint 5, each with a green check and a review by someone else | ⟦FILL: from tools/m5_repo_check.py⟧ |
| 14 | Per member: a merged pull request, a review given, an issue closed | ⟦FILL: from tools/m5_repo_check.py⟧ |
| 15 | [Chore] Sprint 5 wrap-up, Scrum Master, closed | #185 |
| 16 | `docs/sprint-log.md`, Sprint 5: committed, completed, velocity, and a table of all five sprints | pass · 16 · 16 · 16 |
| 17 | Release v1.0 on the commit running at the URL | ⟦FILL: the link of the release⟧ |
| 18 | Optional: `docs/retro.md`, a final retrospective | pass · "Whole-semester retrospective" |
