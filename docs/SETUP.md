# Setup — from a fresh clone to the running app

Follow these steps in order on a machine that has never seen the project. They end with every
P0 story working in the browser at `http://localhost:8081/`, on data read from the database.
Plan on about 15 minutes, most of it downloads.

You will use **two terminals**: one runs the backend, the other runs the app. Where Windows and
macOS/Linux differ, both commands are given. On Windows, use PowerShell or Command Prompt; in Git
Bash, activate the virtual environment with `source .venv/Scripts/activate` instead.

---

## 1. Prerequisites

| Tool          | Version                                                         | Check with                                   | Get it from                                                                     |
| ------------- | --------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------- |
| Git           | any recent version                                              | `git --version`                              | https://git-scm.com/downloads                                                   |
| Python        | **3.11, 3.12, 3.13 or 3.14**, 64-bit. 3.12 recommended          | `python --version` (Windows: `py --version`) | https://www.python.org/downloads/ — on Windows, tick **Add python.exe to PATH** |
| Node.js       | **20.19 or later**; 22 or 24 LTS recommended. npm comes with it | `node --version`                             | https://nodejs.org/                                                             |
| A web browser | Chrome, Edge or Firefox                                         |                                              |                                                                                 |

Nothing else is needed: the database is a file that Python creates, so there is no database
server and no Docker to install. A phone is optional (section 8).

Run every **Check with** command before section 2; each must print a version. If you install
anything now, close VS Code and every terminal, then open a new one, so the new program is found.

---

## 2. Get the code

```bash
git clone https://github.com/SE-FDA-NEU/G5_AI66A_SE.git
cd G5_AI66A_SE
```

---

## 3. Backend: install, configure, create the database (terminal 1)

**Windows**

```
cd backend
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
copy .env.example .env
```

If `py` is not found, check that `python --version` prints 3.11 or later, then use
`python -m venv .venv` instead of the second line.

**macOS / Linux**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
```

`requirements-dev.txt` installs the app's libraries from `requirements.txt` and the tools that test
it, pytest among them (section 7). Your prompt now starts with `(.venv)`. Keep this terminal in `backend/` for the rest of this
section.

**Configuration.** The `.env` you just copied works as it is, so a first run needs no edits. What
each value means:

| Setting in `backend/.env` | Value in `.env.example`                                 | Change it when                                                                                                       |
| ------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `DATABASE_URL`            | `sqlite:///./expense.db`, the file `backend/expense.db` | You want the database somewhere else                                                                                 |
| `SECRET_KEY`              | a development-only key                                  | Always, on any machine others can reach: `python -c "import secrets; print(secrets.token_hex(32))"` prints a new one |
| `SESSION_DAYS`            | `7`, how long a sign-in lasts (BR10)                    | Never, unless the requirements change                                                                                |
| `CORS_ORIGINS`            | `*`, any web page may call the API                      | On a server, list the exact web addresses instead                                                                    |

**Create and fill the database, one command** (the same on every system):

```
python -m scripts.seed_data
```

It builds the five tables, then adds the demo data. Alembic prints a few `INFO` lines first; the
output ends with:

```
Database ready: .../backend/expense.db
  categories    11
  users         1
  transactions  91
  budgets       0
  debts         4
Sign in as mai@example.com with the password demo1234
```

Running it again adds nothing. `python -m scripts.seed_data --reset` empties the database and
seeds it again.

**Test accounts.** These exist only in the database this command creates; none of them is anyone's
real password.

| Email                                 | Password                           | What it holds                                                                           |
| ------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------- |
| `mai@example.com`                     | `demo1234`                         | Persona 1, Mai: 25 entries dated this month, 4,000,000 ₫ received and 2,931,000 ₫ spent; 66 entries in the eleven months before; 4 debts |
| any address you create on `/register` | 6 to 128 characters of your choice | Nothing yet: the overview says "No transactions yet this month"                         |

This month's 25 entries are dated from today back over twelve days, and never before the 1st of
this month, so the overview shows the same totals on whatever day the project is set up. The other
66 fill the eleven months before it, six a month, for the charts on `/stats`, and the four debts
are dated from today too: Mai owes 500,000 ₫ to anh Minh, overdue since two days ago, and is owed
350,000 ₫ by Lan and Hoa.

---

## 4. Start the backend (terminal 1)

```
python -m uvicorn app.main:app --reload
```

Leave it running. Check it in the browser:

- `http://localhost:8000/health` shows `{"status":"ok"}`
- `http://localhost:8000/` opens the interactive API documentation

---

## 5. Start the app (terminal 2)

Open a second terminal in the `G5_AI66A_SE` folder:

```
cd mobile
npm ci
npx expo start --web
```

`npm ci` installs the exact versions in `package-lock.json`; it takes one to three minutes and
may print warnings, which are normal. Expo then opens `http://localhost:8081` in your browser; if
it does not, open that address yourself. The first page load builds the app and can take up to a
minute.

---

## 6. How to know it worked

Each step below is one P0 story, done through the screens only: no address needs typing after the
first. Every number assumes a freshly seeded database (`python -m scripts.seed_data --reset`).

1. **Sign in, US02.** `http://localhost:8081/login` shows **Personal Expense Management App** with
   an email field, a password field, a **Sign in** button and a **Create an account** link. Sign
   in as `mai@example.com` with the password `demo1234`.
2. **This month, US04.** The address bar changes to `http://localhost:8081/`. The card at the top
   reads **Received 4,000,000 ₫ · Spent 2,931,000 ₫ · Left 1,069,000 ₫**.
3. **Recent entries, US05.** Under the card: **The 20 most recent of 91 entries**. The first row
   is **tra sua · Food · −55,000 ₫** dated today, and the money received,
   **tien bo me gui · Other income · +4,000,000 ₫**, is the 19th row.
4. **The rows come from the database.** Open a third terminal in `G5_AI66A_SE/backend` and run the
   line below; it needs only Python, not the virtual environment. Then press **Refresh** on the
   page: the first row now reads **edited in the database**.

   ```
   python -c "import sqlite3; c = sqlite3.connect('expense.db'); c.execute('UPDATE transactions SET note = ? WHERE id = 91', ('edited in the database',)); c.commit()"
   ```

   `python -m scripts.seed_data --reset` puts the original data back; press **Refresh** again.

5. **Log a purchase, US03.** Press **+ Add an entry**. The address bar shows
   `/transactions/new`, and the amount field has the cursor. Type `30000`, tap **Food**, type the
   note `banh mi`, and press **Save**. Back on `/`, the card reads **Spent 2,961,000 ₫ · Left
   1,039,000 ₫**, and **banh mi · Food · −30,000 ₫** is the first row of **92 entries**.
6. **Break a rule on purpose, BR11.** Press **+ Add an entry** again, type `55000`, and change the
   date to tomorrow. **Save** shows, under the form, **The date cannot be in the future** and why,
   and nothing is stored: **Cancel**, and the card still reads **Left 1,039,000 ₫**. An amount of
   `0` shows **Enter an amount greater than 0** in the same place (BR5).
7. **Create an account, US01.** Press **Sign out**, then **Create an account** on `/login`.
   `mai@example.com` shows **This email is already registered** (BR1), and a password of 5
   characters **Password must be 6 to 128 characters** (BR2). With a new address, such as
   `hoa@example.com`, and the password `abcd1234`, **Create account** opens `/` already signed in,
   showing **No transactions yet this month**.
8. **Languages, US11.** The language buttons at the top right, **EN** and **VI** so far, change
   every text on the page, error messages included, and the choice is kept when the page is
   reloaded. The app always opens in English the first time.

Every message the app can show, and the rule behind it, is listed in `docs/ui.md`, section 3.

---

## 7. Run the automated tests

The tests need no server and no database: each one builds its own database in memory, or in a
temporary folder, and throws it away, so `backend/expense.db` is never touched and the backend does
not have to be running. In a terminal with the virtual environment active (section 3), in the
`G5_AI66A_SE` folder:

```
pytest
```

`pytest -v` lists every test by name, with the test case ID from `docs/testing.md` in it. The last
line reads `75 passed`, in about two seconds; nothing may fail or be skipped. The same command
works from `backend/`.

The app has tests of its own, for how amounts, dates and messages are shown. In terminal 2, in
`mobile/`: `npm test`.

---

## 8. Optional: on a phone

Install **Expo Go** (it must support SDK 54). Put the phone and the computer on the same network;
campus Wi-Fi blocks devices from reaching each other, so use a phone hotspot. Start the backend
with `python -m uvicorn app.main:app --reload --host 0.0.0.0`, then scan the QR code that
`npx expo start` prints. The app finds the backend on the computer by itself.

---

## 9. Troubleshooting

| What you see                                                                                                           | Why                                                                           | Fix                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `'python' is not recognized` or `'py' is not recognized`                                                               | Python is not installed, or not on the PATH                                   | Install Python 3.12 from python.org with **Add python.exe to PATH** ticked, then open a new terminal                                           |
| PowerShell: `running scripts is disabled on this system` when activating                                               | Windows blocks the activation script                                          | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. It lasts only for this window                           |
| `python -m pip` fails with `No module named pip`, or with `Python was not found`                                       | The virtual environment is not active, or it was created without pip          | Activate it again until the prompt starts with `(.venv)`; if the error stays, run `python -m ensurepip --upgrade`, then the install line again |
| `ModuleNotFoundError: No module named 'fastapi'`, or `'app'`, or `'scripts'`                                           | The virtual environment is not active, or the terminal is not in `backend/`   | `cd backend`, activate again (section 3), then rerun the command                                                                               |
| `pip` tries to build `pydantic-core` and asks for Rust or for Visual C++                                               | A Python version outside 3.11 to 3.14, or 32-bit Python                       | Install 64-bit Python 3.12 and create `.venv` again                                                                                            |
| `ImportError: cannot import name 'UTC' from 'datetime'` when seeding                                                   | Python 3.10 or older: the libraries install, but the code needs 3.11 or later | Install Python 3.12, delete the `.venv` folder, and create it again with `py -3.12 -m venv .venv`                                              |
| The page says **Cannot reach the server at http://localhost:8000/api**, or **No connection. Tap Refresh to try again** | The backend is not running                                                    | Start it in terminal 1 (section 4), check `http://localhost:8000/health`, then press **Refresh**                                               |
| **Incorrect email or password** for `mai@example.com`                                                                  | The database was not seeded, or not in `backend/`                             | Run `python -m scripts.seed_data` in `backend/`                                                                                                |
| `'npm' is not recognized` or `'node' is not recognized`                                                                | Node.js is not installed, or it was installed while this terminal was open    | Install Node.js 22 or 24 LTS from https://nodejs.org/, close VS Code and every terminal, open a new one, then check `node --version`           |
| PowerShell: `npm.ps1 cannot be loaded because running scripts is disabled on this system`                              | Windows blocks npm's PowerShell script                                        | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, or type `npm.cmd ci` instead of `npm ci`                                     |
| `npm ci` stops with an engine error, or Expo will not start                                                            | Node.js is older than 20.19                                                   | Install Node.js 22 or 24 LTS, then run `npm ci` again                                                                                          |
| Expo says port 8081 is in use                                                                                          | Another program holds the port                                                | Accept the port Expo offers; the app still finds the backend                                                                                   |
| `address already in use` when the backend starts                                                                       | Another program holds port 8000                                               | Close it, or stop an older backend still running in another terminal                                                                           |
| **The server does not offer this yet** on `/register` or `/transactions/new`                                           | The backend still runs code from before Sprint 3                              | `git pull` in the repository, stop the backend with Ctrl+C, then start it again (section 4)                                                    |
| The page shows an older screen after `git pull`                                                                        | Expo still holds the old bundle                                               | Stop Expo with Ctrl+C, then `npx expo start --web --clear`                                                                                     |
| **This email is already registered** for an address you meant to create                                                | You created it on an earlier run; the database keeps it                       | Use another address, or `python -m scripts.seed_data --reset` to start again from the demo data                                                |
| `/stats` shows only this month, or `/debts` is empty, for `mai@example.com`                                             | The database was seeded before Sprint 4; running the seed again adds nothing to an account that has entries | `python -m scripts.seed_data --reset` in `backend/`, then reload the page                                                                      |
| `'pytest' is not recognized`, or `No module named pytest`                                                              | The virtual environment is not active, or it was filled from `requirements.txt` only | Activate it (section 3), then `python -m pip install -r requirements-dev.txt` in `backend/`                                                   |
| `ModuleNotFoundError: No module named 'app'` when running pytest                                                       | pytest was started outside the project, so it found no `pytest.ini`           | `cd` to the `G5_AI66A_SE` folder or to `backend/`, then run `pytest` again                                                                     |

---

## Tested by

| Who            | Team    | Machine                                                                 | Date       | Time taken                                      | Result |
| -------------- | ------- | ----------------------------------------------------------------------- | ---------- | ----------------------------------------------- | ------ |
| Đỗ Quang Trung | Team 04 | Windows laptop, Python 3.12.10, Node.js 24.15.0, both already installed | 04/10/2026 | 6 minutes, from `git clone` to the list on `/` | Worked: `python -m pip install -r requirements.txt` failed with <python -m>, and `pip install -r requirements.txt` worked; after that the seed printed 11/1/25/0, `/health` answered ok, `/` showed the 20 most recent of 25 entries, the proof line changed row 1, and EN/VI stayed after a reload |
| Đỗ Quang Trung | Team 04 | Windows laptop, Python 3.12.10, Node.js 24.15.0, both already installed | 17/10/2026 | 10 minutes, from `git clone` to the list on `/` | Worked: every step of section 6, through the screens only, with nothing to ask or guess and nothing to change |

Filled in by someone outside Team 05 who followed this file word for word on a machine that is
not ours. Anything they had to ask or guess becomes a fix in this file, not a note beside it.
