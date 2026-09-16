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

_Survey evidence: added in #36 after the survey closes on 17/09._

**Out of scope this semester:** automatic bank sync, shared ledgers, currencies other than VND,
PDF report export, and rewards for recording. One interviewee would only use an app that gives
something concrete back; what this product gives back is the amount left, shown after every
entry, not a perk.

---

## 2. Personas

Both personas come from the three interviews in `docs/research/interviews.md`. Interviewees are
identified by number only, because this repository is public.

### Persona 1 — The student on a family allowance _(primary)_

_Persona 1: written in #29._

### Persona 2 — The student who also works _(secondary)_

_Persona 2: written in #33._

### How the two differ

_How the two differ: written in #33._

### Interview note

_Interview note: written in #32._

---

## 3. Scenarios

### Scenario 1 — The student on an allowance decides whether a jacket can wait

_Scenario 1: written in #29._

### Scenario 2 — The working student keeps a fund away from their savings

_Scenario 2: written in #33._

---

## 4. User stories

_Story table: written in #27._

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

### Flow

_Flow diagram: written in #31._
