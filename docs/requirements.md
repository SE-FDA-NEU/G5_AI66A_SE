# Requirements — Sổ chi tiêu G5

**Team 05 · AI66A · Personal expense tracking app**
Milestone 1 · Sprint 1 · Weeks 5–6

---

## 1. Product vision

For Vietnamese students who live on a fixed amount each month, whether an allowance from family
or wages from a job alongside their studies, and who find out they have overspent only once the money has gone,
**Sổ chi tiêu G5** shows how much of the month's money is left each time a purchase is written
down, in under 15 seconds, so that a textbook, a jacket or a night out does not quietly use up
the rest of the month. Keeping a notebook is a chore few people keep up, and a banking app lists
transfers but not what was paid in cash.

**Measured by:** one purchase written down in **under 15 seconds**, and the amount left for the
month **visible straight after saving**, with no further step.

**Why we believe this.** From the interviews in `docs/research/interviews.md`:

- All three interviewees keep a limit, whether in their head, as the whole monthly allowance, or
  as separate pots of money, and all three have gone over it at some point.
- Two of the three have never written their spending down. The third relies on an e-wallet's
  monthly list and still overspends a fund now and then.

**Survey evidence:** Shown in `docs/research/survey.md`

**Out of scope this semester:** automatic bank sync, shared ledgers, currencies other than VND,
PDF report export, and rewards for recording. One interviewee would only use an app that gives
something concrete back; what this product gives back is the amount left, shown after every
entry, not a perk.

---

## 2. Personas

Both personas come from the three interviews in `docs/research/interviews.md`.

### Persona 1 — The student on a family allowance _(primary)_

**Mai — university student living away from home**

Receives a fixed family allowance of 4,000,000 ₫ per month, spending roughly 3,000,000 ₫ on food and 1,000,000 ₫ on other living expenses. She does not write down what she spends and keeps mental estimates instead, so she often finds out she has overspent only when the money is almost gone before the next transfer.

**Goal:** make her monthly allowance last until the next transfer and know immediately whether a purchase is safe to make.

**Blocked by:** no regular spending record; relying on mental calculations makes it easy to lose track and overspend early in the month.

**In her words:** _"Bởi vì em là một người chi tiêu hơi hoang phí và cũng không hay tính toán lắm, cho nên là nhiều khi nó sẽ có nhiều thứ bị hơi lố."_ (Interviewee 1, 01:47) — "Because I spend rather lavishly and don't calculate much, things often get a bit out of hand."

**Technical context:** phone only, uses it on campus and in her room; never opens a laptop to log daily expenses. The interface has to be fast and work on a small screen.

### Persona 2 — The student who also works _(secondary)_

**Thanh — student and worker, manages shared and personal funds**

Studies and works at the same time. Pays for rent, food, coffee and outings with friends, and everyday necessities. They divide their money into personal and shared funds and use an e-wallet to track spending by category each month. Even with this system, they sometimes spend more than planned and have to take money from savings to cover the difference.

**Goal:** keep each spending fund within its monthly limit without using savings to cover overspending.

**Blocked by:** spending can exceed a fund's limit before they realise it, leaving them to use savings to cover the difference.

**In their words:** _"Tuy nhiên, cũng có nhiều lúc bị tiêu lố và phải lấy khoản tiết kiệm ra để bù vào."_ (Interviewee 2, 02:22)

**Technical skill:** regularly uses a mobile e-wallet that automatically categorises spending.

### How the two differ

Persona 1 needs to **see** what is left of a fixed monthly amount with as little effort as possible, because she has no regular habit of recording expenses.

Persona 2 already tracks spending through an e-wallet and separates money into different funds. They need to **control** these funds and avoid exceeding their planned spending limits.

In short, Persona 1 needs **visibility**, while Persona 2 needs **control** over spending limits.

### Interview note

|                           |                                                                                                                                                                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Spoke to**              | Interviewee 1, first-year student · 14/09/2026 · 02:00 minutes · by @levanduc36<br>Interviewee 2, studies and works · 14/09/2026 · 02:30 minutes · by @levanduc36<br>Interviewee 3, second-year student · 14/09/2026 · 02:00 minutes · by @levanduc36 |
| **Method**                | Open questions about monthly spending, the last time money ran out early, whether they record spending, and any limit they keep. Recorded on video, with spoken consent at the start.                                                                 |
| **Stated limitation**     | Interviewees 1 and 3 were also asked whether they would use such an app. An answer to a hypothetical question is weak evidence, so the personas rest on what the interviewees described doing, not on those two answers.                              |
| **Where the notes are**   | `docs/research/interviews.md`. The videos stay in the team's drive and are not committed, because this repository is public.                                                                                                                          |
| **Cross-checked against** | 9 survey responses, `docs/research/survey.md`                                                                                                                                                                                                         |

---

## 3. Scenarios

### Scenario 1 — The student on an allowance decides whether a jacket can wait

1. On 1 November the student's family sends the month's 4,000,000 ₫, and that evening the student
   writes it down as money received.
2. Each evening before bed they write down what they spent that day, usually about 100,000 ₫ on
   food; each purchase takes a few seconds to write down.
3. After each one they see how much of the month's money is left, without adding anything up.
4. On the 10th they realise they skipped an evening, look back over the last few days, find that a
   45,000 ₫ lunch is missing and add it, checking that nothing has been written down twice.
5. On the 12th a lecturer asks the class to buy a 180,000 ₫ textbook. Before paying, they check:
   2,530,000 ₫ is left for the 19 days until the end of the month.
6. They buy the textbook and write it down, and 2,350,000 ₫ is left.
7. They had planned to buy a 450,000 ₫ jacket that weekend. That would leave 1,900,000 ₫, exactly
   100,000 ₫ a day, which is what they spend on food alone.
8. They put the jacket off until next month's money arrives, rather than go short on meals at the
   end of this one.

### Scenario 2 — The student keeps their entertainment spending within its monthly limit

1. At the start of the month, the student sets a 1,000,000 ₫ monthly limit for going out with friends and records this limit in the system.
2. They record each outing when it happens, including a film, a game night, and a birthday karaoke.
3. By the 18th, after several outings including a 150,000 ₫ cinema trip, their entertainment spending reaches 820,000 ₫.
4. Without being asked, the system tells them that only 180,000 ₫ of the monthly limit remains, while there are still 12 days left in the month.
5. When friends suggest a karaoke outing costing 200,000 ₫ per person that weekend, the student checks the remaining amount and decides not to join because the cost would exceed the remaining limit.
6. On the 30th, they record one final 140,000 ₫ outing, bringing their entertainment spending to 960,000 ₫ for the month, so they do not need to take money from their savings.
7. They review their spending and see that entertainment accounted for 960,000 ₫ of their 4,800,000 ₫ total spending, or 20%.
8. For the following month, they keep the entertainment limit at 1,000,000 ₫.

The amounts in this scenario are illustrative and are used to demonstrate the scenario flow; they are not reported figures from Interviewee 2.

---

## 4. User stories

| ID   | Story                                                                                                                                           | Priority | Points |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------ |
| US01 | As a new user, I want to create an account with an email and a password, so that my spending stays private to me.                               | P0       | 3      |
| US02 | As a returning user, I want to sign in once and stay signed in, so that logging a purchase is never delayed by a password.                      | P0       | 3      |
| US03 | As someone who has just spent or received money, I want to write it down in seconds, so that I do it before I forget.                           | P0       | 5      |
| US04 | As a user, I want to see this month's income, spending and what is left, so that I know where I stand without adding it up.                     | P0       | 3      |
| US05 | As a user, I want to look back over recent entries, so that I can check for mistakes and duplicates.                                            | P0       | 3      |
| US06 | As a user, I want to correct or remove an entry I got wrong, so that my totals are not skewed.                                                  | P1       | 3      |
| US07 | As someone writing down a purchase, I want the kind of spending suggested from the words I type, so that I do not have to search a list for it. | P1       | 5      |
| US08 | As someone saving money, I want to cap spending on one kind of thing for a month, so that I have a number to stay under.                        | P1       | 5      |
| US09 | As someone with a cap, I want to be told before I reach it, so that I can still change what I do.                                               | P2       | 5      |
| US10 | As a user, I want to see which kinds of spending took the most, so that I know what to cut.                                                     | P2       | 5      |

**Five P0 · three P1 · two P2 · 40 points total.**

---

_Acceptance criteria for US01 to US10: written in #37._

---

## 5. Business rules

_Business rules: written in #34._

---

## 6. Screens and flow

**Access:** `G` guest, not signed in · `U` signed-in user · `A` administrator

| Route               | Purpose                                                                | Access | Priority |
| ------------------- | ---------------------------------------------------------------------- | ------ | -------- |
| `/login`            | Sign in to reach your own records                                      | **G**  | P0       |
| `/register`         | Create an account and enter immediately                                | **G**  | P0       |
| `/`                 | This month's income, spending, remainder; cap warnings; recent entries | **U**  | P0       |
| `/transactions/new` | Log one amount of money spent or received                              | **U**  | P0       |
| `/transactions/:id` | Correct or remove one entry                                            | **U**  | P1       |
| `/budget`           | Set and read monthly caps per kind of spending                         | **U**  | P1       |
| `/stats`            | Breakdown of one month by kind of spending                             | **U**  | P2       |

Seven screens against the required five. **No `A` screen exists this semester:** every account
sees only its own records (BR4), so there is no administrator role to build. This is stated so
the absence reads as a decision rather than an omission.

### Flow

_Flow diagram: written in #31._
