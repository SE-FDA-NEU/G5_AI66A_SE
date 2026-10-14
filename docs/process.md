# Software Process Dossier — Team G5

## Section 1 — Chosen process and its position on the spectrum

### (a) The model

We follow the **Incremental model**: the product is built in two-week increments, each a working
slice, inside the four milestone gates the course fixes. Prototyping is a technique inside it,
not a lifecycle.

Tuấn cuts the sprint's slice into issues. Tuan and Nhiên agree the interface between the data and
service layers — function names, inputs, outputs — and write it down before either codes. With
that contract fixed all four work in parallel: Nhiên the data layer, Tuấn the service and routing
layers, Vân the screens, Đình Anh the tests. At the midpoint everything merged so far is run
together. At sprint end the build on `main` runs on a device, does more than before, and passes
its tests, on a preview tool chosen in week 2.

Nothing unfinished reaches `main`; the agreed interface is what lets four people work at once.

### (b) The position

Agile in execution, plan-driven at the boundaries — roughly 80% to 20%. The milestone dates and
artefacts, the architecture, the technology stack and code ownership are frozen all semester,
being too costly to re-open; everything else changes each sprint — which stories enter the slice,
screen layout, and how the categorisation rules evolve.

## Section 2 — The five diagnostic questions

**1. Are requirements stable or volatile? What evidence?**
Volatile in detail, stable in purpose. The goal has not moved since week 1 — record spending,
categorise it, warn before the budget runs out. Two decisions under it changed within three
weeks: we replaced a planned browser client with a mobile one, and moved the framework back three
major versions when our spike would not run on our demo phone.

**2. Safety or legal impact demanding formal documentation and change control?**
None: the app records self-reported spending and moves no money, so it has no safety-critical or
regulated financial function requiring formal change control.

**3. Team large and distributed, or small and co-located?**
Four members, co-located, same weekly class: communication cost is low, so documentation stays
light. It does not remove integration risk — members whose layers meet still write their
interface down.

**4. Can the customer engage continuously?**
The instructor engages weekly as an active customer, but acceptance falls only at four graded
checkpoints.

**5. What do culture and contract constraints allow?**
The course fixes four milestones (weeks 5, 8, 12, 15), their weights, the artefacts due at each,
the demo date, and mandatory Git/GitHub, tests and CI.

## Section 3 — Critical thinking: risks of the opposite choice

Fully plan-driven, our single biggest risk would be **writing the whole specification up front
and integrating only near the end**.

Its value sits in two things nobody can judge on paper: categorising a transaction from the words
a user types, and knowing when a budget warning helps rather than annoys. Apps in this category
ship small releases every week or two; HealthCare.gov did the opposite and collapsed on launch
day.

Mechanism: Waterfall pushes integration and validation to the tail, so the first real feedback
arrives when change costs most.

First symptom: at the first end-to-end run most transactions land in "Uncategorised", because the
keyword rules were written from imagination, not from what people type. In our process that
surfaces in sprint 2 and costs one sprint; under Waterfall it surfaces near week 12, with no time
left to retune.

## Section 4 — Process rules the team commits to

1. Every change reaches `main` through a Pull Request approved by another member. Nobody
   approves their own.
2. A sprint is two weeks. The backlog is re-prioritised at each sprint start and every slice
   becomes an issue. 
3. A Pull Request is merged only after the automated tests pass; a failing run blocks it.
4. Each member owns a fixed part of the codebase and does not edit another's; cross-boundary
   changes are requested in the Pull Request and made by the owner. When the two changes must
   merge together, such as a new error shape and the tests that expect it, the owner pushes a
   commit to the same branch, so `main` never sees one without the other.
5. Any requirement or technology change after a sprint starts is recorded in `docs/changelog.md`
   with date, reason and cost.
6. The reviewer is asked the moment a Pull Request is opened, from the rotation agreed at sprint
   planning in `.github/review-rotation.json`; the Request reviewer workflow does the asking. A
   review says what the reviewer ran and what it showed, never only "looks good".
