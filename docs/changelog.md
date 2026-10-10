# Change Log — Team G5

Records every requirement or technology change made after a sprint has started, as committed in
`docs/process.md`, Section 4, rule 5. Each entry states **when** the change happened, **why**, and
**what it cost us**. Entries are appended, never rewritten.

Format: `YYYY-MM-DD — What changed`, then Reason and Impact.

---

## 2026-08-12 — Initial client decision: web application

**Reason.** First team plan assumed a browser-based client, reusing Vân's existing web
experience.

**Impact.** Directory layout, screen list and the UI section of the plan were all written against
a web client.

---

## 2026-08-13 — Client changed from web application to mobile application

**Reason.** The project brief describes a personal-expense *app*. A browser client would not
demonstrate the platform constraints the team wanted to work with, and the instructor's brief
asks for a live demo.

**Impact.** The entire client layer was re-planned. Screen list, navigation model and the client
half of the technology stack were replaced. The backend, database schema and REST API were **not**
affected — the client–server split contained the change to one layer. This is the first evidence
cited in `docs/process.md`, Section 2, question 1.

---

## 2026-08-13 — Mobile SDK dropped by three major versions

**Reason.** The spike was built against the newest published SDK. The store version of the
runtime installed on the team's demo device supports only an older SDK line, and that runtime
refuses to open a project built on a newer one. The constraint is external: the team does not
control which runtime version the app store ships.

**Impact.** Downgraded the SDK and every framework version tied to it. Two follow-on repairs were
needed that the automated version tool did not handle: the navigation library had to be removed
and reinstalled rather than upgraded in place, because installing over the old version produced a
peer-dependency conflict; and one build-time package that used to arrive as an indirect
dependency had to be declared explicitly. Verified afterwards that the client still bundled and
that all unit tests passed.

**Lesson recorded.** This is the "price of reuse" discussed in week 3: a dependency the team does
not control can rewrite the plan. It is the second evidence cited in `docs/process.md`,
Section 2, question 1, and the mechanism behind Section 3.

---

## 2026-08-13 — Constraint found: campus Wi-Fi blocks device-to-device traffic

**Reason.** The campus network isolates connected clients from each other, so the demo device
could not reach the development machine even on the same network. Discovered only by running the
client on real hardware.

**Impact.** Demos and integration testing now run over a phone hotspot instead of campus Wi-Fi.
Recorded as a standing constraint for the final demo in week 15, not a one-off workaround.

---

## 2026-09-27 — BR11: an entry cannot be dated later than today

**Reason.** Designing the transactions table and the seed data for Sprint 2 raised a question that
`docs/requirements.md` never answered: may an entry carry a future date? One dated next week would
lower what is left this month before the money is spent, which works against the measure in
section 1, the amount left visible straight after saving. A date in the past stays allowed,
because Scenario 1, step 4, adds a lunch that was missed days earlier.

**Impact.** New rule BR11 with a worked example, and a fifth criterion on US03 (#16). The seed
script never writes a future date (#62), and the API design rejects one with 422 "The date cannot
be in the future" (`docs/design.md`, section 3). No story changed priority or points; the check
itself is built with US03 in Sprint 3.

---

## 2026-09-27 — US05: the list is refreshed with a Refresh button

**Reason.** The M2 check opens the walking skeleton in a browser, on a machine that has never seen
the project, and the page it opens is the list of recent entries. A browser has no pull-down
gesture, so there the only way to refresh would be to reload the page, which throws away the
entries already on screen: exactly what criterion 2 protects.

**Impact.** Criterion 2 of US05 (#18) now reads: when the user taps Refresh with no network, the
message is "No connection. Tap Refresh to try again" and the loaded entries stay on screen. On a
phone, pulling the list down still refreshes it too. Points unchanged at 3; built by #65.

---

## 2026-09-28 — US11: language options, English and Vietnamese first

**Reason.** Both personas are Vietnamese students, and all three interviews were held in
Vietnamese. An app that speaks only English puts a language barrier in front of the people it is
built for. The Product Owner asked on 28/09 for language options, English and Vietnamese first,
and on 29/09 the story was worded for any language, so offering another one later needs no new
story. The documents stay in English, as the lecturer asked on 18/09; only the app's screens gain
other languages.

**Impact.** New story US11, P2, 3 points; the backlog grows from 40 to 43 points. It joins
Sprint 2 as #72, built by #73, so Sprint 2 commits 9 points instead of 6 (`docs/sprint-log.md`).
English stays the default, so every acceptance criterion and `docs/SETUP.md` still read word for
word. The API keeps answering in English and the app translates the sentences it knows. From now on
every screen adds its text to every language's dictionary, and a test fails when a language is
missing a text that English has. A new language is one more dictionary; no screen changes.

---

## 2026-10-10 — API errors carry a code as well as a sentence

**Reason.** Drawing `/transactions/new` in its error state for `docs/ui.md` showed that the app
could not keep translating errors by matching their English sentences: the new form has six
messages in two languages, a reworded sentence would silently leave the Vietnamese screen in
English, and a malformed request answered with FastAPI's own text, which no user should read. The
same work showed that a crash in the API reached the browser without its CORS header, so the app
said "Cannot reach the server" while the server was running.

**Impact.** Every error now answers `{"detail": "<sentence>", "code": "<what went wrong>"}`, and a
crash answers 500 in the same shape, inside CORS (#94). The sentences are unchanged, so no
acceptance criterion changed and no story changed priority or points. The app picks each message,
and a hint saying what to do next, by `code` (#103). `docs/design.md`, section 3, and
`docs/ui.md`, section 4, describe it (#113). Cost: one extra commit by the testing owner on the
same branch, because six existing tests compared whole error answers.
