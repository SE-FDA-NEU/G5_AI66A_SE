# Setup — from a fresh clone to the running app

Follow these steps in order on a machine that has never seen the project. They end with the
overview at `http://localhost:8081/` listing entries read from the database. Plan on about
15 minutes, most of it downloads.

You will use **two terminals**: one runs the backend, the other runs the app. Where Windows and
macOS/Linux differ, both commands are given. On Windows, use PowerShell or Command Prompt; in Git
Bash, activate the virtual environment with `source .venv/Scripts/activate` instead.

---

## 1. Prerequisites

| Tool | Version | Check with | Get it from |
| --- | --- | --- | --- |
| Git | any recent version | `git --version` | https://git-scm.com/downloads |
| Python | **3.11, 3.12, 3.13 or 3.14**, 64-bit. 3.12 recommended | `python --version` (Windows: `py --version`) | https://www.python.org/downloads/ — on Windows, tick **Add python.exe to PATH** |
| Node.js | **20.19 or later**; 22 or 24 LTS recommended. npm comes with it | `node --version` | https://nodejs.org/ |
| A web browser | Chrome, Edge or Firefox | | |

Nothing else is needed: the database is a file that Python creates, so there is no database
server and no Docker to install. A phone is optional (section 7).

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
python -m pip install -r requirements.txt
copy .env.example .env
```

If `py` is not found, check that `python --version` prints 3.11 or later, then use
`python -m venv .venv` instead of the second line.

**macOS / Linux**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Your prompt now starts with `(.venv)`. Keep this terminal in `backend/` for the rest of this
section.

**Configuration.** The `.env` you just copied works as it is, so a first run needs no edits. What
each value means:

| Setting in `backend/.env` | Value in `.env.example` | Change it when |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///./expense.db`, the file `backend/expense.db` | You want the database somewhere else |
| `SECRET_KEY` | a development-only key | Always, on any machine others can reach: `python -c "import secrets; print(secrets.token_hex(32))"` prints a new one |
| `SESSION_DAYS` | `7`, how long a sign-in lasts (BR10) | Never, unless the requirements change |
| `CORS_ORIGINS` | `*`, any web page may call the API | On a server, list the exact web addresses instead |

**Create and fill the database, one command** (the same on every system):

```
python -m scripts.seed_data
```

It builds the four tables, then adds the demo data. Alembic prints a few `INFO` lines first; the
output ends with:

```
Database ready: .../backend/expense.db
  categories    11
  users         1
  transactions  25
  budgets       0
Sign in as mai@example.com with the password demo1234
```

Running it again adds nothing. `python -m scripts.seed_data --reset` empties the database and
seeds it again.

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

1. `http://localhost:8081/login` shows **Personal Expense Management App** with an email field, a
   password field and a **Sign in** button.
2. Sign in as `mai@example.com` with the password `demo1234`.
3. The address bar changes to `http://localhost:8081/` and the page shows **The 20 most recent of
   25 entries**. The first row is **tra sua · Food · −55,000 ₫** dated today; the rows run back
   nine days to **tien nha · Bills · −1,500,000 ₫**. The 19th row is money received:
   **tien bo me gui · Other income · +4,000,000 ₫**.
4. **The rows come from the database.** Open a third terminal in `G5_AI66A_SE/backend` and run the
   line below; it needs only Python, not the virtual environment. Then press **Refresh** on the
   page: the first row now reads **edited in the database**.

   ```
   python -c "import sqlite3; c = sqlite3.connect('expense.db'); c.execute('UPDATE transactions SET note = ? WHERE id = 25', ('edited in the database',)); c.commit()"
   ```

   `python -m scripts.seed_data --reset` puts the original data back.
5. **Languages.** The language buttons at the top right, **EN** and **VI** so far, change every
   text on the page, and the choice is kept when the page is reloaded. The app always opens in
   English the first time.

---

## 7. Optional: on a phone

Install **Expo Go** (it must support SDK 54). Put the phone and the computer on the same network;
campus Wi-Fi blocks devices from reaching each other, so use a phone hotspot. Start the backend
with `python -m uvicorn app.main:app --reload --host 0.0.0.0`, then scan the QR code that
`npx expo start` prints. The app finds the backend on the computer by itself.

---

## 8. Troubleshooting

| What you see | Why | Fix |
| --- | --- | --- |
| `'python' is not recognized` or `'py' is not recognized` | Python is not installed, or not on the PATH | Install Python 3.12 from python.org with **Add python.exe to PATH** ticked, then open a new terminal |
| PowerShell: `running scripts is disabled on this system` when activating | Windows blocks the activation script | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. It lasts only for this window |
| `python -m pip` fails with `No module named pip`, or with `Python was not found` | The virtual environment is not active, or it was created without pip | Activate it again until the prompt starts with `(.venv)`; if the error stays, run `python -m ensurepip --upgrade`, then the install line again |
| `ModuleNotFoundError: No module named 'fastapi'`, or `'app'`, or `'scripts'` | The virtual environment is not active, or the terminal is not in `backend/` | `cd backend`, activate again (section 3), then rerun the command |
| `pip` tries to build `pydantic-core` and asks for Rust or for Visual C++ | A Python version outside 3.11 to 3.14, or 32-bit Python | Install 64-bit Python 3.12 and create `.venv` again |
| `ImportError: cannot import name 'UTC' from 'datetime'` when seeding | Python 3.10 or older: the libraries install, but the code needs 3.11 or later | Install Python 3.12, delete the `.venv` folder, and create it again with `py -3.12 -m venv .venv` |
| The page says **Cannot reach the server at http://localhost:8000/api**, or **No connection. Tap Refresh to try again** | The backend is not running | Start it in terminal 1 (section 4), check `http://localhost:8000/health`, then press **Refresh** |
| **Incorrect email or password** for `mai@example.com` | The database was not seeded, or not in `backend/` | Run `python -m scripts.seed_data` in `backend/` |
| `'npm' is not recognized` or `'node' is not recognized` | Node.js is not installed, or it was installed while this terminal was open | Install Node.js 22 or 24 LTS from https://nodejs.org/, close VS Code and every terminal, open a new one, then check `node --version` |
| PowerShell: `npm.ps1 cannot be loaded because running scripts is disabled on this system` | Windows blocks npm's PowerShell script | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, or type `npm.cmd ci` instead of `npm ci` |
| `npm ci` stops with an engine error, or Expo will not start | Node.js is older than 20.19 | Install Node.js 22 or 24 LTS, then run `npm ci` again |
| Expo says port 8081 is in use | Another program holds the port | Accept the port Expo offers; the app still finds the backend |
| `address already in use` when the backend starts | Another program holds port 8000 | Close it, or stop an older backend still running in another terminal |

---

## Tested by

| Who | Team | Machine | Date | Time taken | Result |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Filled in by someone outside Team 05 who followed this file word for word on a machine that is
not ours. Anything they had to ask or guess becomes a fix in this file, not a note beside it.
