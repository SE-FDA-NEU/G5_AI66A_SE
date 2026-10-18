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

Committed: 9 points, 6 at planning and 3 added on 28/09 · Completed: 9 points

---

## Sprint 3 - 06/10/2026 to 19/10/2026

**Scrum Master:** @levanduc36

### Keep / Stop / Start

Agreed during the Sprint 3 retrospective meeting on 17/10/2026.

| Keep doing | Stop doing | Start doing |
| --- | --- | --- |
| Drawing the wireframes before building the P0 screens, so the interface and documentation stay aligned | Opening replacement pull requests late, which leaves less time for a meaningful review | Recording the exact checks and result in every review comment |
| Having another team follow `docs/SETUP.md` on its own machine before submission | Treating a closed, replaced pull request as evidence of completed review | |

### Action for next sprint

| Action | Owner | Checked at |
| --- | --- | --- |
| Check the review queue every evening and follow up immediately on any pull request without a reviewer or a review within 12 hours | @Chidokato5376 | Sprint 4 retro |

### Did last sprint's action happen?

The action was "Every reviewer provides detailed feedback or explicit verification steps on PRs
within 12 hours; the Scrum Master checks open PRs each evening". Partly, from
`review_latency.py 92 113`, checked on 18/10/2026: 15 of 21 pull requests had a reviewer named
when opened and were reviewed within 12 hours. The longest review took 45.1 hours; 19 completed
reviews named the checks run and their result. Pull requests #125 and #129 were closed and replaced
before a review. Since #102, the workflow requests the reviewer from the rotation when a pull
request opens.

| PR | Title | Author | Reviewer named when opened | Time to review |
| --- | --- | --- | --- | --- |
| #114 | [#94] Give every API error a code, and a crash a 500 in the same shape | @Chidokato5376 | yes | 9.1 h |
| #115 | [#95] Keep every demo entry inside the current month | @nguyennhien2412 | yes | 21.8 h |
| #116 | [#107] Add docs/ui.md with its P0 stories and the screen flow | @nguyennhien2412 | yes | 9.9 h |
| #117 | [#97] Add POST /api/users, signed in at once | @Chidokato5376 | yes | 3.3 h |
| #118 | [#96] Add the queries behind US03 and US04 | @nguyennhien2412 | yes | 0.1 h |
| #119 | [#108] Wireframe /login and /register | @nguyennhien2412 | yes | 0.2 h |
| #120 | [#109] Wireframes for Overview and New Entry | @vantran2801 | no | 45.1 h |
| #121 | [#102] Ask the reviewer from the rotation when a pull request opens | @levanduc36 | no | 5.5 h |
| #122 | [#100] Test creating an account, US01 with BR1 and BR2 | @levanduc36 | yes | 5.4 h |
| #123 | [#98] Add POST /api/transactions and GET /api/categories | @Chidokato5376 | yes | 1.8 h |
| #124 | [#103] Error messages app | @vantran2801 | yes | 11.1 h |
| #125 | [#104] Register screen | @vantran2801 | yes | no review yet |
| #126 | [#99] Add GET /api/summary | @Chidokato5376 | yes | 1.2 h |
| #127 | [#104] Register screen | @vantran2801 | yes | 1.0 h |
| #128 | [#101] Test logging an entry and this month's position | @levanduc36 | yes | 4.0 h |
| #129 | [#105] New entry screen | @vantran2801 | yes | no review yet |
| #130 | [#106] Overview month | @vantran2801 | yes | 1.3 h |
| #131 | [#105] new entry redo | @vantran2801 | yes | 13.6 h |
| #132 | [#111] Trace US01, US03 and US04 to what built and tested them | @nguyennhien2412 | yes | 3.4 h |
| #133 | [#110] List every error message in docs/ui.md | @levanduc36 | yes | 1.3 h |
| #134 | [#112] Check every P0 story in SETUP.md, tested by another team | @levanduc36 | yes | 12.0 h |

### Velocity

Committed: 11 points · Completed: 11 points

---

## Sprint 4

**Scrum Master:** @Chidokato5376

This section will be completed during Sprint 4.

---

## Sprint 5

This section will be completed during Sprint 5.

---

## Whole-semester retrospective

Written for the Milestone 5 report. What the team would keep, drop, and do
differently on the next project, and what the velocity trend across five
sprints actually showed.
