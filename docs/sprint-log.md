# Sprint log

One section per sprint. Fill it in **during** the sprint, not the night before
the milestone deadline - the commit timestamps on this file are part of the
evidence that the process was real.

---

## Sprint 1 - 08/09/2026 to 21/09/2026

**Committed 0 · Completed 0 · Velocity: not applicable (requirements sprint)**

### Sprint goal

The team agrees what the product is: every user story can be checked, and every business rule is fixed.

### The two required chore issues

| Issue                                   | Owner               | Closed?    |
| --------------------------------------- | ------------------- | ---------- |
| #24 [Chore] Refine backlog for Sprint 1 | @Chidokato5376 (PO) | yes, 17/09 |
| #25 [Chore] Sprint 1 wrap-up            | @vantran2801 (SM)   | yes, 20/09 |

### Committed

No story was committed for building. Sprint 1 delivered `docs/requirements.md`. The ten story
issues, #14 to #23, 40 points in total, were written and estimated this sprint, not built.

| Issue | Story                                                | Points | Owner |
| ----- | ---------------------------------------------------- | ------ | ----- |
| none  | Requirements sprint: no story committed for building | 0      |       |

**Total committed: 0 points**

### Result

| Issue | Deliverable                                                                          | Owner            | Status    | If not done, why              |
| ----- | ------------------------------------------------------------------------------------ | ---------------- | --------- | ----------------------------- |
| #26   | Section 1 product vision and the `docs/requirements.md` skeleton                     | @Chidokato5376   | Done      |                               |
| #27   | Section 4 user story table                                                           | @Chidokato5376   | Done      |                               |
| #28   | Completed `docs/requirements.md`, final review, PDF with cover block, LMS submission | @Chidokato5376   | In review | Merges last, after this issue |
| #29   | Section 2 persona 1, section 3 scenario 1                                            | @vantran2801     | Done      |                               |
| #30   | Section 6 screens table                                                              | @vantran2801     | Done      |                               |
| #31   | Section 6 flow diagram                                                               | @vantran2801     | Done      |                               |
| #32   | Interview notes and interview note                                                   | @nguyennhien2412 | Done      |                               |
| #33   | Section 2 persona 2, section 3 scenario 2                                            | @nguyennhien2412 | Done      |                               |
| #34   | Section 5 business rules with worked examples                                        | @nguyennhien2412 | Done      |                               |
| #35   | Acceptance criteria audit                                                            | @nguyennhien2412 | Done      |                               |
| #36   | Survey and competitor comparison                                                     | @levanduc36      | Done      |                               |
| #37   | Section 4 acceptance criteria for all ten stories                                    | @levanduc36      | Done      |                               |
| #38   | README: Definition of Done and team table                                            | @levanduc36      | Done      |                               |
| #39   | Repository checklist verification                                                    | @levanduc36      | Done      |                               |

**Completed: 0 points. Velocity this sprint: not applicable (requirements sprint)**

### Why the figures are zero

Sprint 1 delivered a document, not working software. Counting the 40 estimated story points as
completed would inflate the velocity that Sprint 2 is planned against, which is the number this file
exists to protect. The ten stories are the backlog Sprint 2 and Sprint 3 draw from; they are not
carried over, because they were never committed to Sprint 1 for building.

### Sprint Review

- What we demonstrated: `docs/requirements.md` on GitHub, section by section, with the research behind it in `docs/research/`
- Feedback received: the lecturer confirmed the team number, the topic name in English, and that the cover names the pull request that completed `docs/requirements.md`
- Backlog changes as a result: after the survey, BR9 and US09 warn at 70% of a cap instead of 80%, and caps for a single occasion are out of scope. No story changed priority

### Retrospective

See Sprint 1 in `docs/retro.md`.

### Attendance

| Member           | Planning | Review | Retro |
| ---------------- | -------- | ------ | ----- |
| @Chidokato5376   | yes      | yes    | yes   |
| @vantran2801     | yes      | yes    | yes   |
| @nguyennhien2412 | yes      | yes    | yes   |
| @levanduc36      | yes      | yes    | yes   |

**Scrum Master for Sprint 2:** @nguyennhien2412

---

## Sprint 2 - 22/09/2026 to 05/10/2026

**Committed 9 (6 at planning, 3 added on 28/09) · Completed 9 · Velocity: 9 points**

### Sprint goal

A signed-in user sees their 20 most recent entries, read from the real database, on a phone and in
a browser, and `docs/design.md` and `docs/SETUP.md` let a machine that has never seen the project
run it.

### Planning

Planning met on 26/09. The iteration opened on 22/09; the Sprint 2 issues #55 to #71 were written
on 27 and 28/09, and the review rotation and merge order were posted on #55 on 28/09 and
rebalanced there on 29/09.

### The two required chore issues

| Issue                                   | Owner                 | Closed?                     |
| --------------------------------------- | --------------------- | --------------------------- |
| #55 [Chore] Refine backlog for Sprint 2 | @Chidokato5376 (PO)   | Yes, 29/09                  |
| #56 [Chore] Sprint 2 wrap-up            | @nguyennhien2412 (SM) | Yes, 04/10                  |

### Committed

| Issue | Story                                          | Points | Owner            |
| ----- | ---------------------------------------------- | ------ | ---------------- |
| #15   | US02 Sign in and stay signed in                | 3      | @levanduc36      |
| #18   | US05 Look back over recent entries             | 3      | @nguyennhien2412 |
| #72   | US11 Choose the app's language, added on 28/09 | 3      | @nguyennhien2412 |

**Total committed: 9 points**, 6 at planning and 3 added on 28/09

US11 joined the sprint on 28/09 at the Product Owner's request (`docs/changelog.md`). If its task
#73 has not merged by 03/10 at 20:00, it moves to Sprint 3 with the label `carried-over`.

On 29/09 the owners of #15, #18, #70 and #72 changed, so that commits, closed issues, pull requests
and reviews stay even across the four of us over the semester; the new rotation is on #55.

The task issues #57 to #71 build these two stories, the walking skeleton and `docs/design.md`.
Tasks carry hours, not points, so velocity counts story points only, as in Sprint 1.

### Result

| Issue | Deliverable                                                       | Owner            | Status      | If not done, why                                                                                  |
| ----- | ----------------------------------------------------------------- | ---------------- | ----------- | ------------------------------------------------------------------------------------------------- |
| #15   | US02 Sign in and stay signed in, 3 points                         | @levanduc36      | Done        |                                                                                                   |
| #18   | US05 Look back over recent entries, 3 points                      | @nguyennhien2412 | Done        |                                                                                                   |
| #72   | US11 Choose the app's language, 3 points, added on 28/09          | @nguyennhien2412 | Done        |                                                                                                   |
| #57   | design.md skeleton, section 3 API design, the requirement changes | @Chidokato5376   | Done        |                                                                                                   |
| #58   | Backend skeleton: settings, /health                               | @Chidokato5376   | Done        |                                                                                                   |
| #59   | CI for backend/ and mobile/, test fixtures                        | @levanduc36      | Done        |                                                                                                   |
| #60   | Four tables, first Alembic migration, repositories                | @nguyennhien2412 | Done        |                                                                                                   |
| #61   | Sign-in API and GET /api/transactions                             | @Chidokato5376   | Done        |                                                                                                   |
| #62   | One-command seed script                                           | @nguyennhien2412 | Done        |                                                                                                   |
| #63   | Backend tests for BR1-BR5, BR7, BR10, US05 and the seed script    | @levanduc36      | Done        |                                                                                                   |
| #64   | App skeleton and the /login screen                                | @vantran2801     | Done        |                                                                                                   |
| #65   | Overview / with the 20 most recent entries                        | @vantran2801     | Done        |                                                                                                   |
| #66   | docs/SETUP.md, tested on a machine that is not ours               | @levanduc36      | Done        |                                                                                                   |
| #67   | design.md section 2: data model and ERD                           | @nguyennhien2412 | Done        |                                                                                                   |
| #68   | design.md sections 1 and 4: architecture and walking skeleton     | @vantran2801     | Done        |                                                                                                   |
| #69   | design.md section 5: three ADRs                                   | @levanduc36      | Done        |                                                                                                   |
| #70   | docs/traceability.md: story, screen, endpoint, table              | @levanduc36      | Done        |                                                                                                   |
| #71   | design.md section 6, README, M2 checklist, PDF                    | @Chidokato5376   | Done        | Merged last, on 04/10, as #91; its merge commit `350b0ed` is on the PDF cover                     |
| #73   | Language options on /login and /, English and Vietnamese first    | @vantran2801     | Done        |                                                                                                   |

**Completed: 9 points. Velocity this sprint: 9 points**: US02 #15, US05 #18 and US11 #72 all closed on 03/10.

### Sprint Review

- What we demonstrated: at the team meeting on 04/10, the walking skeleton running: sign-in and
  the 20 most recent of 25 entries on `/`, read from the database. Team 04 also ran it from
  `docs/SETUP.md` on their own machine that day, as described below.
- Feedback received: Đỗ Quang Trung (Team 04) followed `docs/SETUP.md` on their own laptop on
  04/10 and had the page in 6 minutes; `python -m pip` did not run there, so `pip install` was used.
  An earlier run on another machine stopped at `'npm' is not recognized`, because Node.js was
  missing. Both are now rows in the Troubleshooting table of `docs/SETUP.md` (#66).
- Backlog changes as a result: no story changed; the fixes went into `docs/SETUP.md`.

### Retrospective

See Sprint 2 in `docs/retro.md`.

### Attendance

| Member           | Planning | Review                    | Retro    |
| ---------------- | -------- | ------------------------- | -------- |
| @Chidokato5376   | Yes      | With the instructor, next | Not held |
| @vantran2801     | Yes      | With the instructor, next | Not held |
| @nguyennhien2412 | Yes      | With the instructor, next | Not held |
| @levanduc36      | Yes      | With the instructor, next | Not held |

**Scrum Master for Sprint 3:** @levanduc36

---

## Sprint 3 - 06/10/2026 to 19/10/2026

**Committed 11 · Completed 11 · Velocity: 11 points**

### Sprint goal

A person who has never seen the app completes every P0 story through its screens, with real data
from the database, and every broken rule gives a message that says what happened and what to do
next; `docs/ui.md` shows how.

### Planning

The iteration opened on 06/10. Planning met on 10/10, after the M2 submission; the Sprint 3 issues
#92 to #113 were written that day, and the review rotation and merge order were posted on #92 and
committed as `.github/review-rotation.json` by #102.

### The two required chore issues

| Issue                                   | Owner               | Closed?                     |
| --------------------------------------- | ------------------- | --------------------------- |
| #92 [Chore] Refine backlog for Sprint 3 | @Chidokato5376 (PO) | Yes, 10/10                  |
| #93 [Chore] Sprint 3 wrap-up            | @levanduc36 (SM)    | Right after this log merges |

@levanduc36 could not finish #93 on 18/10, so @Chidokato5376 wrote this log and the retro for it;
@levanduc36 closes #93 as Scrum Master.

### Committed

| Issue | Story                          | Points | Owner            |
| ----- | ------------------------------ | ------ | ---------------- |
| #14   | US01 Create an account         | 3      | @vantran2801     |
| #16   | US03 Log a purchase in seconds | 5      | @nguyennhien2412 |
| #17   | US04 This month's position     | 3      | @vantran2801     |

**Total committed: 11 points**, the three P0 stories not yet built. Velocity was 9 in Sprint 2;
11 was taken on because US01 and US04 reuse the screens, tables and tests Sprint 2 built, and the
API for all three was designed in M2.

The task issues #94 to #113 build these three stories and `docs/ui.md`. Tasks carry hours, not
points, so velocity counts story points only, as in Sprints 1 and 2.

### Result

| Issue | Deliverable                                                          | Owner            | Status      | If not done, why                                                                                   |
| ----- | -------------------------------------------------------------------- | ---------------- | ----------- | -------------------------------------------------------------------------------------------------- |
| #14   | US01 Create an account, 3 points                                     | @vantran2801     | Done        |                                                                                                    |
| #16   | US03 Log a purchase in seconds, 5 points                             | @nguyennhien2412 | Done        |                                                                                                    |
| #17   | US04 This month's position, 3 points                                 | @vantran2801     | Done        |                                                                                                    |
| #94   | Every API error carries a code; a crash answers 500 inside CORS      | @Chidokato5376   | Done        |                                                                                                    |
| #95   | Bug: demo entries fell into last month early in a month              | @nguyennhien2412 | Done        |                                                                                                    |
| #96   | Repository: one category by id, one month's totals                   | @nguyennhien2412 | Done        |                                                                                                    |
| #97   | POST /api/users                                                      | @Chidokato5376   | Done        |                                                                                                    |
| #98   | POST /api/transactions and GET /api/categories                       | @Chidokato5376   | Done        |                                                                                                    |
| #99   | GET /api/summary                                                     | @Chidokato5376   | Done        |                                                                                                    |
| #100  | Backend tests for US01                                               | @levanduc36      | Done        |                                                                                                    |
| #101  | Backend tests for US03 and US04                                      | @levanduc36      | Done        |                                                                                                    |
| #102  | Ask the reviewer automatically, from the rotation                    | @levanduc36      | Done        |                                                                                                    |
| #103  | A message and a hint for every error code, in the app                | @vantran2801     | Done        |                                                                                                    |
| #104  | /register, closes US01                                               | @vantran2801     | Done        |                                                                                                    |
| #105  | /transactions/new, closes US03                                       | @vantran2801     | Done        | Redone as #131 after #129 was closed unmerged; reached `main` on 17/10, a day after #106            |
| #106  | The month on /, in four states, closes US04                          | @vantran2801     | Done        |                                                                                                    |
| #107  | docs/ui.md skeleton, section 1 and the flow diagram                  | @nguyennhien2412 | Done        |                                                                                                    |
| #108  | ui.md section 2: wireframes of /login and /register                  | @nguyennhien2412 | Done        |                                                                                                    |
| #109  | ui.md section 2: wireframes of / in four states and /transactions/new | @vantran2801     | Done        |                                                                                                    |
| #110  | ui.md section 3: error messages                                      | @levanduc36      | Done        |                                                                                                    |
| #111  | docs/traceability.md for Sprint 3                                    | @nguyennhien2412 | Done        |                                                                                                    |
| #112  | docs/SETUP.md for Sprint 3, tested on a machine that is not ours     | @levanduc36      | Done        |                                                                                                    |
| #113  | ui.md section 4, design.md, README, M3 checklist, PDF                | @Chidokato5376   | Merges last | The final pull request of the sprint, merged after this log; its merge commit is on the PDF cover |

**Completed: 11 points. Velocity this sprint: 11 points**: US01 #14, US03 #16 and US04 #17 all
closed by the pull requests of #104, #105 and #106.

### Sprint Review

- What we demonstrated: nothing before the submission. The Sprint 3 Review is held with the
  instructor, who clones the repository, follows `docs/SETUP.md` and uses the four P0 screens.
- Feedback received: Đỗ Quang Trung, Team 04, followed `docs/SETUP.md` on their own machine on
  17/10/2026 (#112): every step worked, with nothing to ask and nothing to change.
- Backlog changes as a result: none.

### Retrospective

No retrospective meeting was held in Sprint 3; see Sprint 3 in `docs/retro.md`.

### Attendance

| Member           | Planning | Review | Retro |
| ---------------- | -------- | ------ | ----- |
| @Chidokato5376   | Yes      | Yes    | Yes   |
| @vantran2801     | Yes      | Yes    | Yes   |
| @nguyennhien2412 | Yes      | Yes    | Yes   |
| @levanduc36      | Yes      | Yes    | Yes   |

**Scrum Master for Sprint 4:** @Chidokato5376, as the rotation in the README says

---

## Sprint 4 - 20/10/2026 to 02/11/2026

**Committed 18 · Completed 18 · Velocity: 18 points**

### Sprint goal

Every P0 story is checked by automated tests that a machine runs in seconds, with no server and
no real database, and `docs/testing.md` says which; and the app shows where the money went, month
by month, and what is owed, on a screen that uses its whole width.

### Planning

The iteration opened on 20/10. Planning met on 24/10, after the M3 submission, and began with the
Sprint 3 retrospective that had not been held (`docs/retro.md`). The Product Owner asked for a
spending trend and for debts and loans; they became US12 and US13 (`docs/changelog.md`, 24/10).
Issues #138 to #161 were written that day, and the review rotation and merge order were
posted on #138 and committed in `.github/review-rotation.json`.

### The two required chore issues

| Issue | Owner | Closed? |
| --- | --- | --- |
| #138 [Chore] Refine backlog for Sprint 4 | @Chidokato5376 (PO) | Yes, 25/10 |
| #139 [Chore] Sprint 4 wrap-up | @Chidokato5376 (SM) | Right after this log merges |

In Sprint 4 the Product Owner is also the Scrum Master, as the rotation in the README fixed in week
1; the retrospective is facilitated by @levanduc36.

### Committed

| Issue | Story | Points | Owner |
| --- | --- | --- | --- |
| #19 | US06 Correct or remove an entry | 3 | @levanduc36 |
| #23 | US10 See which kinds of spending took the most | 5 | @vantran2801 |
| #140 | US12 See how spending changes month by month | 5 | @nguyennhien2412 |
| #141 | US13 Keep track of debts and loans | 5 | @levanduc36 |

**Total committed: 18 points**, against a velocity of 11 in Sprint 3. Taken on because US10 and
US12 share one screen and one family of endpoints, US06 reuses the form of US03, and the M4
deliverable, the tests, mostly gives the existing P0 code test case IDs rather than new code.

The tasks #142 to #161 build these four stories, give every P0 story its test cases, and write
`docs/testing.md`. Tasks carry hours, not points, so velocity counts story points only, as before.

### Result

| Issue | Deliverable | Owner | Status | If not done, why |
| --- | --- | --- | --- | --- |
| #19 | US06 Correct or remove an entry, 3 points | @levanduc36 | Done | |
| #23 | US10 See which kinds of spending took the most, 5 points | @vantran2801 | Done | |
| #140 | US12 See how spending changes month by month, 5 points | @nguyennhien2412 | Done | |
| #141 | US13 Keep track of debts and loans, 5 points | @levanduc36 | Done | |
| #142 | An amount above 9,223,372,036,854,775,807 breaks the month's totals | @Chidokato5376 | Done | |
| #143 | One command runs every test, from the repository root | @levanduc36 | Done | |
| #144 | Repository: one entry by id, corrected and removed | @nguyennhien2412 | Done | |
| #145 | Test cases TC-31 to TC-38 for US04 | @nguyennhien2412 | Done | |
| #146 | GET, PATCH and DELETE /api/transactions/{id} | @Chidokato5376 | Done | |
| #147 | Test cases TC-01 to TC-08 and TC-17 to TC-30 for US01 and US03 | @levanduc36 | Done | |
| #148 | Repository: spending per kind, and totals per month and per year | @nguyennhien2412 | Done | |
| #149 | Test cases TC-39 to TC-45 for US05 | @vantran2801 | Done | |
| #150 | GET /api/stats/breakdown, /months and /years | @Chidokato5376 | Done | |
| #151 | The debts table, migration 0002 and its queries | @nguyennhien2412 | Done | |
| #152 | /transactions/:id corrects or deletes an entry | @vantran2801 | Done | |
| #153 | Test cases TC-09 to TC-16 for US02 | @levanduc36 | Done | |
| #154 | /api/debts: write down, list, settle and remove | @Chidokato5376 | Done | |
| #155 | Demo data for Sprint 4: eleven earlier months and four debts | @nguyennhien2412 | Done | |
| #156 | /stats and the tabs between the main screens | @vantran2801 | Done | |
| #157 | docs/testing.md, sections 1 and 2 | @levanduc36 | Done | |
| #158 | /debts and /debts/new | @vantran2801 | Done | |
| #159 | Two columns on / for a wide screen | @vantran2801 | Done | |
| #160 | docs/traceability.md for Sprint 4 | @nguyennhien2412 | Done | |
| #161 | docs/testing.md sections 3 and 4, README, M4 checklist, PDF | @levanduc36 | Merges last | The pull request that completes `docs/testing.md`, merged after this log |

**Completed: 18 points. Velocity this sprint: 18 points**: US06 #19 closed by the pull request of
#152, US10 #23 and US12 #140 by #156, US13 #141 by #158.

**Velocity so far:** 9, 11, 18 points in Sprints 2 to 4. The jump is not a faster team: Sprint 4's
stories were smaller than their points suggest once the patterns of Sprints 2 and 3 existed.
Sprint 5 plans from the average, about 13.

### Sprint Review

- What we demonstrated: the Sprint 4 Review is held with the instructor, who clones the repository
  on a machine that has never seen it, follows `docs/SETUP.md`, types `pytest`, and picks a test
  case ID from `docs/testing.md`.
- Feedback received: before the review, CI ran `pytest` from the repository root on every pull
  request, on a machine that had never seen the project.
- Backlog changes as a result: none yet.

### Retrospective

See Sprint 4 in `docs/retro.md`.

### Attendance

| Member | Planning | Review | Retro |
| --- | --- | --- | --- |
| @Chidokato5376 | Yes | With the instructor, next | Yes |
| @vantran2801 | Yes | With the instructor, next | Yes |
| @nguyennhien2412 | Yes | With the instructor, next | Yes |
| @levanduc36 | Yes | With the instructor, next | Yes |

**Scrum Master for Sprint 5:** @levanduc36, as the rotation in the README says
