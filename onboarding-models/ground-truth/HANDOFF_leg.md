# Handoff — reconstruct the Legrand US (`leg`) onboarding, blind

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace. It is self-contained.

**This one is different from the previous four.** They were all backtests of finished
work. Legrand is **live and still in onboarding today** — it is the only organization in
the system with `status = 'onboarding'`. Your timeline is not a historical exercise; it
describes a client someone is working on this week.

---

## Why it has to be blind

You are building an **independent ground truth** from raw evidence only, so a separate
assessment framework can be graded against it. The hand-written client notes drift and are
sometimes flatly wrong — one sibling client's profile claimed "go-live blocked, 0 customers
imported" while the live database held 346. Read those first and you reproduce their
conclusions and their errors.

**Do not read any of these until your timeline is written:**

```
❌ every .md under eCat_Onboarding/leg/ (CLIENT_PROFILE.md, HANDOFF.md, SESSION-*.md)
❌ every .md under SuperCat_Simple_Final/02_Implementation/Legrand/
   (HANDOFF.md, SESSION-2026-07-24.md, Build/*.md — TAXONOMY.md, ADMIN_SETUP.md,
    library-plan.md, inventory-review.md)
❌ eCat_Onboarding/REGISTRY.yaml
❌ onboarding-models/Phase_Anchors.md, Phase_Progression_Framework.md,
   Flags_and_Signals.md, Output_Contract.md, RUN_PROMPT.md, overrides.yml
❌ onboarding-models/ground-truth/SCORECARD.md and other clients' JOURNEY_*.md
❌ any ecat-* skill that describes what phases mean
```

Build **artifacts** (products.csv, image lists, build_ecat_files.py) are fine to inspect as
evidence — they are data. It is the **narrative** documents that are forbidden.

If you open a forbidden file by accident, say so at the top of your output.

---

## Your inputs

| file | what it is |
|---|---|
| `eCat_Onboarding/leg/_ground_truth/CORPUS_leg.md` | **~71k tokens.** 5 calls (all transcribed), 28 HelpScout threads. Read start to finish. |
| `eCat_Onboarding/leg/_ground_truth/RAWSTATE_leg.json` | Live DB now — counts, users, import history with gap analysis, recurring-feed note. |

`supercat-postgres-vpn` (read-only SQL) and `bigquery-admin` MCPs are available. **Use them
heavily here** — the corpus covers only a fraction of this project's life (see below).

Org id **273**, shortname `leg`. VPN must be up.

---

## The seven phases — questions only, deliberately

You get the *questions* so your output is comparable, and deliberately **not** the rules the
framework uses to answer them. Those rules are what's being tested.

1. **Discovery / Kickoff** — Have we kicked off this client?
2. **Initial Import** — Has at least the products file been imported?
3. **Progress** — Is more than one core file in, without fatal errors on the most recent of each?
4. **Catalog Completeness** — Is the catalog actually buildable as a live iPad?
5. **Reps Signed In** — Are reps actually logging into the iPad?
6. **Admin Training** — Has the admin been trained, with ongoing operations covered?
7. **Go-Live** — Has the formal handoff to support happened, with ongoing client activity?

**If the real story doesn't fit these seven phases, say so.** On all four previous clients
that was among the most valuable output.

---

## Seven questions the phase model does not ask. Answer them anyway.

**A. Did this client ever go backwards?** ← *the headline question for this client.*
There is a **285-day gap** in the import record (2025-09-06 → 2026-06-18) and a 78-day gap
before it. Roughly nine and a half months in which nothing was imported at all, inside an
onboarding that is still open. What happened? Who stopped, who restarted it, and why? Did
anyone treat it as a problem at the time?

**B. Adoption — separate from go-live.** Who actually used it, how many, how often?

**C. Current trajectory.** Improving, steady, or decaying, on what evidence? Note the daily
inventory feed is still running as of this morning.

**D. Was the catalog ever *wrong* while the imports looked *clean*?** Import tiers record
only whether a file parsed, never whether the contents were right. On one previous client
images imported at clean tier for 18 days with doubled `.jpg.jpg` extensions that could
never match. On another, ~200 products carried wrong images across 86 consecutive clean
imports. Look for someone describing something wrong on the iPad, then check the import log
for that day.

**E. Placeholder or dangling references?** One client had every product at a $1.00
placeholder; another had 12 orders pointing at a deleted price level, plus a link into a
different client's org entirely. Check both directions.

**F. Check `audit_log_entries` — a known blind spot.** Global table keyed on
`(parent_type, parent_id)`; match with `data::text ILIKE '%"organization":"leg"%'`. Events
include `OrgUser destroyd`, `OrgUser created`, `user group updated`, `Organization updated`.
On one client it revealed ten destroyed accounts and a full customer reload **that appear
nowhere in HelpScout or Fathom**. Also check `organization_invitations` — self-enrolment
writes no audit row, so invitations are a third, separate source.

**G. What is the recurring feed actually doing?** Inventory has imported 31 times since
2026-07-14, roughly 06:01 daily and sometimes twice, **every single one warning-tier**
("Product not found, record ignored"). No other client in this set has an automated feed.
Is anyone reading these warnings? How many rows are being silently dropped each day?

---

## Reading notes specific to leg

- **Identity trap.** A *second* organization is also named `legrand` — shortname `lna`,
  id 93, created 2015, inactive, 101 products, 3 orders. A name match returns both. The
  live one is **id 273**. Never mix them.

- **The corpus is thin against the project's length.** The org was created 2025-06-10 and
  the first import was 2025-06-12, but **HelpScout has nothing before 2026-07-08** and the
  first call is 2025-11-07. Roughly the first year of this project has almost no written
  record you can read. Lean on the database and expect `undetermined` entries — that is the
  correct output, not a failure.

- **23 user types exist; exactly ONE has any users in it.** "Admin / Internal Legrand" holds
  all 10 users. The other 22 are empty scaffolding. Work out whether they were built for a
  rollout that hasn't happened.

- **Everyone is internal.** All 10 users are on `legrand.com` (plus one gmail and SuperCat
  staff among the admins). 5 non-admin, 3 of whom have signed into the iPad and are active
  in the last 30 days. No outside rep agency appears anywhere.

- **Zero orders. Zero order rows.** Not "zero submitted" — the `orders` table has no rows at
  all for this org after 14 months. Note `is_submitted` is **nullable**, so `WHERE
  is_submitted` and `= 0` behave differently; here both are genuinely zero.

- **310 of 1,020 products are visible** — 710 carry `hideable`. 1,018 of 1,020 have images,
  so hiding is not about missing photos. Deliberate hero-variant strategy, or unfinished?

- **29 options and 11 option_groups exist.** Check whether any *active product* actually
  references them, or whether they are orphaned from an early build.

- **153 Library items and 6 iPad report formats** — the richest configuration in the whole
  test set. Something substantial was built here recently. Find out what and when.

- **Duplicate tickets.** On one client 21 of 31 tickets were duplicate captures of 9
  conversations. Collapse on subject (ignoring `Re:` / `Fwd:` / `FW:`) before concluding
  anything from volume. With only 9 tickets here the effect is small but check anyway.

---

## What to produce

### 1. `eCat_Onboarding/leg/_ground_truth/JOURNEY_leg.md`

Open with a 10–20 line plain-language narrative. Then:

**A. Cast** — every person, email, side, first and last appearance, role changes.

**B. Phase transitions**, one entry each:

```markdown
### Phase 2 → 3 · 2025-06-19 · confidence: medium

**What changed:** <one sentence>

**Evidence:**
- [HS #14xxx, 2026-07-08T13:52, someone@legrand.com (customer)] > "verbatim quote"
- [DB] import_history: Products warning 2025-06-13; Customers clean 2025-06-19

**Against:** <what argues the other way, or "none">
```

- Every transition needs a date and evidence — a verbatim quote with author and timestamp,
  or a specific DB fact.
- Confidence: `high` / `medium` / `low`.
- **If you cannot date a transition, write `undetermined` and explain why. Do not guess.**
- Quote real text. Never paraphrase inside quote marks.

**C. Current phase as of today**, same evidence standard. This client is live — say where it
actually stands and what the next real blocker is.

**D. Turning points** — the 3–5 moments that actually moved or blocked this project.

**E. The seven extra questions** (A–G above), answered directly.

**F. The 285-day gap**, answered specifically: what stopped, what restarted it, and whether
the project that resumed in June 2026 is the same project that stopped in September 2025.

### 2. `eCat_Onboarding/leg/_ground_truth/GAPS_leg.md`

- What you could not determine, and what evidence would settle it
- Which tier-B tickets you judged irrelevant, and why
- Contradictions between sources — a thread saying one thing, the DB another
- **Corpus holes.** Critical here: name every stretch where the DB shows activity and the
  corpus shows nothing. The first year is largely undocumented.

---

## Before you finish

1. Does every transition have a date and evidence, or an explicit `undetermined`?
2. Is every quote verbatim, with author and timestamp?
3. Did you read the whole corpus? Say which parts you skimmed, if any.
4. Confirm explicitly that you avoided all the forbidden files.
5. Did you keep org 273 and org 93 straight throughout?
6. Does your narrative contradict `RAWSTATE_leg.json` anywhere? Flag it — the DB is not
   automatically right either, and a genuine contradiction is a finding.

Write both files, then stop. Do not touch any existing `CLIENT_PROFILE.md` or `HANDOFF*.md`.
