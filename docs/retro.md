# Retrospective

One section per sprint, written within 24 hours of the Sprint Review, with no
lecturer present. Filled in through a Pull Request like everything else - the
commit date is the evidence that the retro happened when it says it did.

A retro that produces no action item is a complaint session. Exactly one action,
exactly one owner, checked at the start of the next retro.

---

## Sprint 1 - 08/09/2026 to 21/09/2026

**Scrum Master:** @vantran2801

### Keep / Stop / Start

| Keep doing                                                                                                                         | Stop doing                                                                                               | Start doing                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| One pull request per section, each replacing only its own placeholder, so four people worked in parallel without a single conflict | Pasting from an outdated copy of the shared pack: #37 merged old criteria that had to be corrected later | Asking for a reviewer the moment a pull request is opened                                      |
| Fixing the survey's decision rules before the answers came in, then applying them unchanged                                        | Leaving a pull request with no reviewer requested: #39 sat for eighteen hours because nobody was asked   | Turning format-on-save off for Markdown, so saving a file does not reformat the whole document |

### Action for next sprint

| Action                                                                                            | Owner            | Checked at     |
| ------------------------------------------------------------------------------------------------- | ---------------- | -------------- |
| Every pull request names its reviewer when it is opened, and the reviewer answers within 12 hours | @nguyennhien2412 | Sprint 2 retro |

### Did last sprint's action happen?

Not applicable - first sprint.

### Velocity

Committed: 0 points · Completed: 0 points

---

## Sprint 2 - 22/09/2026 to 05/10/2026

**Scrum Master:** @nguyennhien2412

### Keep / Stop / Start

Agreed during the Sprint 2 retrospective meeting on 04/10/2026.

| Keep doing                                                                             | Stop doing                                                                                     | Start doing                                                          |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| One pull request per task, each reviewed within 12 hours and merged only with green CI | One-line reviews such as "everything's fine" instead of saying what was run and what it showed | Starting the Saturday tasks on Friday, so the last day is not a rush |
| Asking another team to run `docs/SETUP.md` before we submit                            | Leaving PR review tasks to the last minute before merge deadlines                              |                                                                      |

### Action for next sprint

| Action                                                                                                                                         | Owner       | Checked at     |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | -------------- |
| Every reviewer provides detailed feedback or explicit verification steps on PRs within 12 hours; the Scrum Master checks open PRs each evening | @levanduc36 | Sprint 3 retro |

### Did last sprint's action happen?

Partly. The action was "Every pull request names its reviewer when it is opened, and the reviewer answers within 12 hours". All 15 merged pull requests were reviewed within 12 hours, the longest in 11.3 hours. However, communication regarding review status was mostly updated in descriptions. The table comes from `review_latency.py 55 73`, run on 04/10; #74, closed unmerged and replaced by #75, is left out.

| PR  | Title                                              | Author           | Reviewer named when opened | Time to review |
| --- | -------------------------------------------------- | ---------------- | -------------------------- | -------------- |
| #75 | [#57] Add design.md skeleton, the API design and t | @Chidokato5376   | no                         | 5.6 h          |
| #76 | [#58] Add the backend skeleton with settings and / | @Chidokato5376   | yes                        | 5.4 h          |
| #77 | [#59] Run CI from backend/ and mobile/             | @levanduc36      | yes                        | 7.6 h          |
| #78 | [#69] Add three design decisions as ADRs           | @levanduc36      | no                         | 0.7 h          |
| #79 | [#60] Add the four tables and the first Alembic mi | @nguyennhien2412 | yes                        | 7.5 h          |
| #80 | [#61] Add sign-in and GET /api/transactions        | @Chidokato5376   | no                         | 0.8 h          |
| #81 | [#62] Add a one-command seed script                | @nguyennhien2412 | yes                        | 5.8 h          |
| #82 | [#64] Add the app skeleton and the /login screen   | @vantran2801     | no                         | 0.3 h          |
| #83 | [#67] Add the data model and the ERD               | @nguyennhien2412 | yes                        | 1.1 h          |
| #84 | [#63] Test sign-in, recent entries and the databas | @levanduc36      | no                         | 10.4 h         |
| #85 | [#70] Trace every story to screen, endpoint and ta | @levanduc36      | no                         | 8.2 h          |
| #86 | [#65] List the 20 most recent entries on /         | @vantran2801     | no                         | 0.6 h          |
| #87 | [#73] Add language options, English and Vietnamese | @vantran2801     | no                         | 0.3 h          |
| #88 | [#66] Add SETUP.md for a brand-new machine         | @levanduc36      | no                         | 11.3 h         |
| #89 | [#68] Document system architecture and walking ske | @vantran2801     | no                         | 0.3 h          |

### Velocity

## Committed: 9 points, 6 at planning and 3 added on 28/09 · Completed: 9 points

## Sprint 3 - <start date> to <end date>

**Scrum Master:** @

### Keep / Stop / Start

| Keep doing | Stop doing | Start doing |
| ---------- | ---------- | ----------- |
|            |            |             |

### Action for next sprint

| Action | Owner | Checked at     |
| ------ | ----- | -------------- |
|        | @     | Sprint 4 retro |

### Did last sprint's action happen?

### Velocity

Committed: ** points · Completed: ** points

---

## Sprint 4 - <start date> to <end date>

**Scrum Master:** @

### Keep / Stop / Start

| Keep doing | Stop doing | Start doing |
| ---------- | ---------- | ----------- |
|            |            |             |

### Action for next sprint

| Action | Owner | Checked at     |
| ------ | ----- | -------------- |
|        | @     | Sprint 5 retro |

### Did last sprint's action happen?

### Velocity

Committed: ** points · Completed: ** points

---

## Sprint 5 - <start date> to <end date>

**Scrum Master:** @

### Keep / Stop / Start

| Keep doing | Stop doing | Start doing |
| ---------- | ---------- | ----------- |
|            |            |             |

### Action for next sprint

| Action | Owner | Checked at      |
| ------ | ----- | --------------- |
|        | @     | - (last sprint) |

### Did last sprint's action happen?

### Velocity

Committed: ** points · Completed: ** points

---

## Whole-semester retrospective

Written for the Milestone 5 report. What the team would keep, drop, and do
differently on the next project, and what the velocity trend across five
sprints actually showed.
