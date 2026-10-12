# User interface — Personal Expense Management App

**Team 05 · AI66A**
Milestone 3 · Sprint 3 · Weeks 9–10

How a person who has never seen the app completes every P0 story through its screens, with real
data from the database, and what they read when they break a rule. The stories are in
[`docs/requirements.md`](requirements.md), the API behind each screen in
[`docs/design.md`](design.md), and the steps to run it in [`docs/SETUP.md`](SETUP.md).

---

## 1. P0 stories and status

Every P0 story starts from a link or a button on a screen; no address has to be typed by hand. The
app opens on `/login` for someone signed out and on `/` for someone signed in within 7 days.

| Story | Screen(s) | Route | Status | Issue |
| --- | --- | --- | --- | --- |
| US01 Create an account | Create an account | `/register`, from **Create an account** on `/login` | not started | [#14] |
| US02 Sign in and stay signed in | Sign in | `/login` | works | [#15] |
| US03 Log a purchase in seconds | New entry | `/transactions/new`, from **+ Add an entry** on `/` | not started | [#16] |
| US04 This month's position | Overview | `/`, the card at the top | not started | [#17] |
| US05 Look back over recent entries | Overview | `/`, the list under the card | works | [#18] |

**Works** means a person can complete the story through the interface from a fresh clone, with
`docs/SETUP.md` and nothing else, and every acceptance criterion on the issue passes. US02 and US05
have worked since Sprint 2. US01, US03 and US04 are built this sprint, by #103 to #106 on the API of
#94 and #97 to #99, and tested by #100 and #101; their status changes as each one merges.

**The flow as built.** The M1 flow (`docs/images/flow.png`) planned seven screens. The four P0
screens below are built; the three P1 and P2 screens, dashed, come in later sprints. A broken rule
never leaves the screen: the message and what to do next appear under the form, and nothing is
stored.

![Screen flow as built in Sprint 3: /login, /register, / and /transactions/new](images/ui/flow.png)

Source of the diagram: [`docs/images/ui/flow.mmd`](images/ui/flow.mmd).

[#14]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/14
[#15]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/15
[#16]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/16
[#17]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/17
[#18]: https://github.com/SE-FDA-NEU/G5_AI66A_SE/issues/18

---

## 2. Wireframes

One wireframe per P0 screen, drawn before the screen was built. The overview at `/` is drawn in
all four states. Every screen has the language switch, **EN | VI**, at the right of its top bar
(US11), left out of the drawings below.

### `/login`, Sign in

"The user comes here to sign in once, and is then not asked again for 7 days."
Calls: `POST /api/auth/login`.

```
+- Sign in ---------------------------------------+
| Personal Expense Management App                 |
| Sign in to see this month and your recent       |
| entries.                                        |
|                                                 |
| Email     [ you@example.com                 ]   |
| Password  [ ********                        ]   |
|                                                 |
| ! Incorrect email or password                   |   <- only after a failed sign-in (BR3)
|   Check both and try again.                     |
|                                                 |
| [               Sign in                     ]   |
|          New here?  Create an account  ->       |   <- goes to /register
+-------------------------------------------------+
```

### `/register`, Create an account

"The user comes here to create an account with an email and a password, and lands on `/`
already signed in."
Calls: `POST /api/users`.

```
+- Create an account -----------------------------+
| Create an account                               |
| An email and a password are all it takes.       |
|                                                 |
| Email     [ hoa@example.com                 ]   |
| Password  [ ********                        ]   |
|           6 to 128 characters                   |
|                                                 |
| ! This email is already registered              |   <- 409 (BR1), 422 (BR2) or 400
|   Sign in with it instead, or create the        |
|   account with another address.                 |
|                                                 |
| [            Create account                 ]   |
|      Already have an account?  Sign in  ->      |   <- back to /login
+-------------------------------------------------+
```

_Written in #109._

---

## 3. Error messages

_Written in #110._

---

## 4. What changed since M2

_Written in #113._
