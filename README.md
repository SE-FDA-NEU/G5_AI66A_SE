# Personal Expense Management App

An application designed for individuals who want to **manage their daily income and expenses**, automatically categorize transactions, track monthly spending, and receive alerts when their spending exceeds the set budget.

**Group:** G5_AI66A
**Product Owner (fixed for the entire semester):** @Chidokato5376
**Scrum Master (rotates every sprint):** @vantran2801 (Sprint 1)
**Board:** [Sprint Board — Personal Expense Management App](https://github.com/orgs/SE-FDA-NEU/projects/12/views/1)

## Team

| Member            | GitHub           | Role                                       | Owns                                      |
| ----------------- | ---------------- | ------------------------------------------ | ----------------------------------------- |
| Nguyen Hoang Tuan | @Chidokato5376   | Product Owner · backend and business logic | `core/` `schemas/` `services/` `routers/` |
| Nguyen Thi Nhien  | @nguyennhien2412 | Database and data layer                    | `db/` `alembic/` `scripts/`               |
| Tran Khai Van     | @vantran2801     | Mobile app and UI                          | `mobile/`                                 |
| Duong Dinh Anh    | @levanduc36      | Testing and CI                             | `backend/tests/` `.github/`               |

Each member edits only what they own. A change that crosses a boundary is requested in the pull
request and made by the owner, which is what lets four people work in parallel without
colliding.

### Scrum Master rotation

| Sprint       | 1            | 2                | 3           | 4              | 5           |
| ------------ | ------------ | ---------------- | ----------- | -------------- | ----------- |
| Scrum Master | @vantran2801 | @nguyennhien2412 | @levanduc36 | @Chidokato5376 | @levanduc36 |

## Definition of Done

An issue is Done only when every line below is true. No exceptions, including for chores.

1. Every acceptance criterion on the issue passes, and the reviewer checked it personally
2. The work runs from a clean clone using only the steps in this README
3. At least one automated test covers the new behaviour
4. CI is green on the pull request branch
5. Approved through **Review changes** by someone who did not write it
6. Merged into `main` through a pull request whose description contains `Closes #<issue>`
7. No secrets, `.env` files, database dumps, interview recordings or personal data in the diff
8. Story IDs and issue numbers in the documents match the board

Sprint 1 produces documents rather than code, so criteria 3 and 4 do not apply to its issues.
The other six stand unchanged. Full text: [docs/definition-of-done.md](docs/definition-of-done.md).

## Documents

| File                                         | What it holds                                                                    |
| -------------------------------------------- | -------------------------------------------------------------------------------- |
| [docs/requirements.md](docs/requirements.md) | Milestone 1 — vision, personas, scenarios, user stories, business rules, screens |
| [docs/process.md](docs/process.md)           | How the team works: branches, commits, pull requests, reviews                    |
| [docs/sprint-log.md](docs/sprint-log.md)     | One block per sprint: goal, committed, completed, velocity                       |
| [docs/retro.md](docs/retro.md)               | Retrospective per sprint, one action with one owner                              |
| [docs/daily.md](docs/daily.md)               | Daily notes, committed on the day they were written                              |
| [docs/research/](docs/research/)             | Interview notes and survey results behind the personas                           |

## Running the Project

```bash
# Clone the repository
git clone https://github.com/SE-FDA-NEU/G5_AI66A_SE.git
cd G5_AI66A_SE

# Installation and run commands
# TODO: added at Milestone 2, when the walking skeleton lands
```

## If a member stops responding

After 3 days: the Scrum Master messages them privately.
After 5 days: the team informs the lecturer and redistributes the work.
