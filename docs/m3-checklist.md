# Milestone 3 checklist

Checked by @Chidokato5376 on 18/10/2026, against `docs/ui.md`, `docs/SETUP.md` and the README on this
branch, and against GitHub on the same day.

## The interface document

| # | The brief requires | Result | Where |
| --- | --- | --- | --- |
| 1 | `docs/ui.md` in Markdown, four sections in order | pass · headings 1 to 4: P0 stories and status, Wireframes, Error messages, What changed since M2 | headings |
| 2 | Section 1: Story · Screen(s) · Route · Status · Issue for every P0 story; status is works, partly works or not started | pass · US01 to US05, all five **works** | §1 |
| 3 | Section 1: the updated screen flow diagram from M1 | pass · `docs/images/ui/flow.png`, with its Mermaid source | §1 |
| 4 | Section 2: one wireframe per P0 screen, each with "The user comes here to …" and the endpoints it calls | pass · `/login`, `/register`, `/`, `/transactions/new` | §2 |
| 5 | Section 2: at least one screen in all four states: empty, loading, error, data | pass · `/`, drawn and as built | §2 |
| 6 | Section 3: at least 4 messages, API error code · business rule · the exact message | pass · 10 rows: BR1, BR2, BR3, BR5, BR6, BR11, BR10, a malformed address, no answer, a crash | §3 |
| 7 | Section 3: the codes are those of the M2 API table; no "Error 422", "Something went wrong" or stack trace | pass · 400, 401, 409, 422 and 500, as in `docs/design.md` section 3; a test fails on a status shown bare (`i18n.test.js`) | §3 |
| 8 | Section 4: at least one change to `docs/design.md` that building the interface caused, and why, updated in the same pull request | pass · two: the error `code`, and a 500 inside CORS; `docs/design.md` sections 1 and 3 in this pull request | §4 |
| 9 | Wireframes and screenshots in `docs/images/ui/` | pass · `flow.png` and 7 screenshots | `docs/images/ui/` |
| 10 | No placeholder left: searched `docs/ui.md` for `_Written in #` and `<DATE>` | pass · none left | whole file |

## The four checks of the Sprint 3 Review

| # | Check | Result | How we checked |
| --- | --- | --- | --- |
| 11 | Clone, follow `docs/SETUP.md`, run: no errors, database created and seeded | pass · #112, tested by Đỗ Quang Trung of Team 04 on 17/10/2026 | SETUP.md, Tested by |
| 12 | Complete one P0 story through the interface, without typing a URL | pass · every P0 story starts from a link or button (README, Try the P0 stories) | SETUP.md §6, steps 1 to 7 |
| 13 | Break one business rule on purpose: a clear message on screen | pass · a date tomorrow on `/transactions/new` shows the BR11 message and its hint | `docs/images/ui/new-entry-future.png` |
| 14 | Open `docs/ui.md`: all four sections, in order | pass | row 1 |

## The repository

Pasted from `m3_repo_check.py`, run on 18/10/2026, after #93 merged, over #92 to #113 and the stories #14, #16 and #17.

| Check | Minimum | Result |
| --- | --- | --- |
| Merged pull requests in Sprint 3, each reviewed by someone else | 4 | pass · 20 merged |
| Issues closed in Sprint 3 | 5 | pass · 24 closed |
| [Chore] Refine backlog for Sprint 3, PO, closed | 1 | pass · assigned to Chidokato5376, closed |
| [Chore] Sprint 3 wrap-up, SM, closed | 1 | pass · assigned to levanduc36, closed |
| Reviews that say what was checked (Sprint 2 retro action) | all | pass |
| Merged with a merge commit, never squashed | all | pass |

| Member | Merged pull requests | Reviews given | Issues closed | At least one of each |
| --- | --- | --- | --- | --- |
| @Chidokato5376 | #114 #117 #123 #126 #135 | #115 #116 #118 #119 #132 | #92 #94 #97 #98 #99 | pass |
| @vantran2801 | #120 #124 #127 #130 #131 | #121 #122 #128 #133 #134 | #14 #17 #103 #104 #105 #106 #109 | pass |
| @nguyennhien2412 | #115 #116 #118 #119 #132 | #114 #117 #123 #126 #135 | #16 #95 #96 #107 #108 #111 | pass |
| @levanduc36 | #121 #122 #128 #133 #134 | #120 #124 #127 #130 #131 | #93 #100 #101 #102 #110 #112 | pass |

The script's review row only checks that every review has a written comment. Read one by one,
12 of the 19 reviews of merged pull requests also say what the reviewer ran and what it showed; see
"Did last sprint's action happen?" in `docs/retro.md`.

| # | The brief requires | Result |
| --- | --- | --- |
| 15 | `docs/SETUP.md` still works on a new machine, "Tested by" updated in Sprint 3 | pass · Đỗ Quang Trung, Team 04, 17/10/2026, 10 minutes on their own laptop; the Sprint 2 row is kept above it |
| 16 | README first screen: P0 stories, where each starts, the test account | pass · Try the P0 stories |
| 17 | `docs/sprint-log.md`, Sprint 3: committed, completed and velocity | pass · committed 11, completed 11, velocity 11 |
| 18 | Scrum Master different from Sprints 1 and 2, named in the README | pass · @levanduc36 for Sprint 3 |
| 19 | Optional: Sprint 3 retrospective, one action, one owner | not done · no retrospective meeting was held; `docs/retro.md` says so and checks the Sprint 2 action with numbers |
| 20 | CI green on `main` after the last merge | pass · green on `f5b3fad`, the merge of #93; this pull request changes documents only |

## The submission

| # | The brief requires | Result |
| --- | --- | --- |
| 21 | `Team05_M3.pdf`, exported from the merged `docs/ui.md`, uploaded to the LMS by the deadline | pending · done right after this pull request merges |
| 22 | Cover: team, topic, members with student IDs, PO, Sprint 3 Scrum Master, repository, board, setup guide link, who submitted | pending · done right after this pull request merges |
| 23 | Page 2: the board right after Sprint 3 planning and on submission day | pending · done right after this pull request merges |
| 24 | Page 3: one P0 screen with real data and one error message on screen, address bar visible | pending · done right after this pull request merges |
| 25 | The board opens from the link on the cover | pending · done right after this pull request merges |
