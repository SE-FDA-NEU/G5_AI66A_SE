# Milestone 2 checklist

Checked by @Chidokato5376 on 04/10/2026, against `docs/design.md` and `docs/SETUP.md` on this
branch, and against GitHub on the same day.

## The design document

| # | The brief requires | Result | Where |
| --- | --- | --- | --- |
| 1 | `docs/design.md` in Markdown, six sections in order | pass · headings 1 to 6: Architecture, Data model, API design, Walking skeleton, Design decisions, What changed since M1 | headings |
| 2 | Section 1: one diagram at the container level, at least 4 components, every arrow labelled with what travels along it | pass · 7 components and 7 labelled arrows in `docs/images/architecture.png` | §1 |
| 3 | Section 2: an ERD in `docs/images/erd.png` with every table, PK, FK and multiplicity; a table with each table's purpose, columns and types, PK, FK and the M1 rule each constraint enforces; ERD and table agree | pass · 4 tables, 4 relationships with multiplicity; BR1, BR2, BR4, BR5, BR6, BR7 and BR8 named, BR11 explained | §2 |
| 4 | Section 3: at least 6 endpoints in a Method / Path / Input / Success output / Error codes table, covering every P0 story, at least 2 error codes | pass · 8 endpoints, US01 to US05 covered, error codes 400, 401, 409 and 422 with their messages | §3 |
| 5 | Section 4: the route, the table it reads, a screenshot of the running page, the SQL behind it, at least 10 rows | pass · route `/`, table `transactions` with 25 seeded rows, the SQL; the screenshot is `docs/images/walking-skeleton.png` | §4 |
| 6 | Section 5: at least 2 decisions as ADRs, each with options, choice, why and what would change our mind | pass · 3 ADRs: SQLite, Expo with a web target, PBKDF2, each also naming the quality it buys | §5 |
| 7 | Section 6: at least 2 changes since M1, with why | pass · three: BR11, the US05 Refresh criterion, and US11 | §6 |
| 8 | Diagrams as images in `docs/images/` | pass · `architecture.png`, `erd.png`, `walking-skeleton.png`, with their `.mmd` sources | `docs/images/` |
| 9 | No placeholder left: searched `docs/design.md` for `_Written in #` and `__` | pass · no `_Written in #` left; the only `__` is the pattern `'____-__'` of the budgets month check | whole file |

## The setup guide

| # | The brief requires | Result | Where |
| --- | --- | --- | --- |
| 10 | Prerequisites with versions, nothing assumed installed | pass · Git, Python 3.11 to 3.14, Node.js 20.19 or later, a browser | §1 |
| 11 | Copy-paste commands in order, Windows and macOS/Linux where they differ | pass | §2 to §5 |
| 12 | Which values to copy from `.env.example` and what to put in them | pass · all four settings explained | §3 |
| 13 | One command creates and seeds the database, and how many rows to expect | pass · `python -m scripts.seed_data`: 11, 1, 25, 0 | §3 |
| 14 | The URL to open and exactly what should appear | pass · `http://localhost:8081/`, the first, 19th and last rows named | §6 |
| 15 | At least two troubleshooting rows | pass · 13 rows | §8 |
| 16 | Tested by: who, on a machine that is not the author's, date, time taken | pass · Đỗ Quang Trung, Team 04, on their own Windows laptop, 04/10/2026, 6 minutes | Tested by |
| 17 | Linked from the first screen of the README | pass · the line under the description | README |

## The repository

Pasted from `m2_repo_check.py`, run on 04/10/2026 over #55 to #73 and the stories #15 and #18.

| Check | Minimum | Result |
| --- | --- | --- |
| Merged pull requests in Sprint 2, each reviewed by someone else | 4 | pass · 16 merged |
| Issues closed in Sprint 2 | 5 | pass · 20 closed |
| [Chore] Refine backlog for Sprint 2, PO, closed | 1 | pass · assigned to Chidokato5376, closed |
| [Chore] Sprint 2 wrap-up, SM, closed | 1 | pass · assigned to nguyennhien2412, closed |
| Merged with a merge commit, never squashed | all | pass |

| Member | Merged pull requests | Reviews given | Issues closed | At least one of each |
| --- | --- | --- | --- | --- |
| @Chidokato5376 | #75 #76 #80 | #77 #78 #84 #88 | #55 #57 #58 #61 | pass |
| @vantran2801 | #82 #86 #87 #89 | #75 #76 #80 | #64 #65 #68 #73 | pass |
| @nguyennhien2412 | #79 #81 #83 #90 | #82 #85 #86 #87 #89 | #18 #56 #60 #62 #67 #72 | pass |
| @levanduc36 | #77 #78 #84 #85 #88 | #79 #81 #83 #90 | #15 #59 #63 #66 #69 #70 | pass |

| # | The brief requires | Result |
| --- | --- | --- |
| 18 | `docs/sprint-log.md`, Sprint 2: committed, completed and velocity | pass · committed 9, completed 9, velocity 9 |
| 19 | A Scrum Master other than Sprint 1's, named in the README | pass · @nguyennhien2412 for Sprint 2 |
| 20 | `docs/SETUP.md` on `main`, "Tested by" filled | pass · merged with #66, tested by Đỗ Quang Trung of Team 04 |
| 21 | Optional: Sprint 2 retrospective, one action, one owner | pass · one action, owner @levanduc36 |
| 22 | Optional: `docs/traceability.md`, Story · Screen · Endpoint · Table, one row per P0 story | pass · all eleven stories |
| 23 | CI green on `main` after the last merge | pass on `eba0e8c`, the merge of #56; checked again right after this pull request merges |

## The submission

| # | The brief requires | Result |
| --- | --- | --- |
| 24 | `Team05_M2.pdf`, exported from the merged `docs/design.md`, uploaded to the LMS by the deadline | pending · done right after this pull request merges |
| 25 | Cover: team, topic, members with student IDs, PO, Sprint 2 Scrum Master, repository, board, setup guide link, who submitted; this pull request and its merge commit hash | pending · done right after this pull request merges |
| 26 | Page 2: the board after Sprint 2 planning and on submission day | pending · done right after this pull request merges |
| 27 | Page 3: the walking skeleton running, with the browser address bar visible | pending · done right after this pull request merges |
| 28 | The board opens from the link on the cover | pending · done right after this pull request merges |
