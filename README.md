# Personal Expense Management App

An application designed for individuals who want to **manage their daily income and expenses**, automatically categorize transactions, track monthly spending, and receive alerts when their spending exceeds the set budget.

**Run it:** [docs/SETUP.md](docs/SETUP.md) takes a fresh clone to the running app, step by step.

**Group:** G5_AI66A
**Product Owner (fixed for the entire semester):** @Chidokato5376
**Scrum Master (rotates every sprint):** @vantran2801 (Sprint 1) · @nguyennhien2412 (Sprint 2) · @levanduc36 (Sprint 3)
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

Sprint 1 produced documents rather than code, so criteria 3 and 4 did not apply to its issues.
From Sprint 2 all eight apply. Criterion 3 is checked per story: backend tests belong to the testing
owner, so a story's tests come from the testing task that names it as parent (#63 in Sprint 2), and
the story closes only after that task has merged. Every pull request, documents included, still
needs CI green. Full text: [docs/definition-of-done.md](docs/definition-of-done.md).

## Documents

| File                                         | What it holds                                                                    |
| -------------------------------------------- | -------------------------------------------------------------------------------- |
| [docs/requirements.md](docs/requirements.md) | Milestone 1 — vision, personas, scenarios, user stories, business rules, screens |
| [docs/design.md](docs/design.md)             | Milestone 2 — architecture, data model, API, walking skeleton, design decisions  |
| [docs/SETUP.md](docs/SETUP.md)               | Install and run the project on a machine that has never seen it                  |
| [docs/traceability.md](docs/traceability.md) | Every story traced to its screen, endpoint, table, rules and issue               |
| [docs/changelog.md](docs/changelog.md)       | Every requirement or technology change after a sprint started, with its cost     |
| [docs/process.md](docs/process.md)           | How the team works: branches, commits, pull requests, reviews                    |
| [docs/sprint-log.md](docs/sprint-log.md)     | One block per sprint: goal, committed, completed, velocity                       |
| [docs/retro.md](docs/retro.md)               | Retrospective per sprint, one action with one owner                              |
| [docs/daily.md](docs/daily.md)               | Daily notes, committed on the day they were written                              |
| [docs/research/](docs/research/)             | Interview notes and survey results behind the personas                           |

## Running the Project

Every step, with its expected output and a troubleshooting table, is in
[docs/SETUP.md](docs/SETUP.md). You need Git, Python 3.11 to 3.14 and Node.js 20.19 or later. The
short version uses two terminals.

**Terminal 1, the backend, on Windows** (PowerShell or Command Prompt):

```
git clone https://github.com/SE-FDA-NEU/G5_AI66A_SE.git
cd G5_AI66A_SE\backend
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python -m scripts.seed_data
python -m uvicorn app.main:app --reload
```

**Terminal 1, the backend, on macOS or Linux:**

```bash
git clone https://github.com/SE-FDA-NEU/G5_AI66A_SE.git
cd G5_AI66A_SE/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_data
python -m uvicorn app.main:app --reload
```

`python -m scripts.seed_data` creates the database and prints 11 categories, 1 user,
25 transactions and 0 budgets.

**Terminal 2, the app**, opened in the folder you cloned into, on every system:

```bash
cd G5_AI66A_SE/mobile
npm ci
npx expo start --web
```

Open http://localhost:8081 and sign in as `mai@example.com` with the password `demo1234`. The page
lists the 20 most recent of 25 entries, read from the database. The language buttons at the top
right, **EN** and **VI** so far, change every text on the page.

## If a member stops responding

After 3 days: the Scrum Master messages them privately.
After 5 days: the team informs the lecturer and redistributes the work.
