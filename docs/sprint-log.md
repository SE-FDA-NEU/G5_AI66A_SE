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
| #56 [Chore] Sprint 2 wrap-up            | @nguyennhien2412 (SM) | Right after this log merges |

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
| #71   | design.md section 6, README, M2 checklist, PDF                    | @Chidokato5376   | Merges last | The final pull request of the sprint, merged after this log; its merge commit is on the PDF cover |
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

| Member           | Planning | Review | Retro |
| ---------------- | -------- | ------ | ----- |
| @Chidokato5376   | Yes      | Yes    | Yes   |
| @vantran2801     | Yes      | Yes    | Yes   |
| @nguyennhien2412 | Yes      | Yes    | Yes   |
| @levanduc36      | Yes      | Yes    | Yes   |

**Scrum Master for Sprint 3:** @levanduc36
