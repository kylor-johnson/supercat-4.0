# Handoff — reconstruct the Magic Lite | NSL (`mali`) onboarding, blind

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace. It is self-contained. Client 4 of 4 — the last and largest.

---

## What you are doing, and why it has to be blind

You are building an **independent ground truth** for one client's onboarding, from raw
evidence only, so a separate assessment framework can be graded against it.

The existing hand-written client notes drift and are sometimes flatly wrong — a sibling
client's profile claimed "go-live blocked, 0 customers imported" while the live database
held 346. If you read those notes first you will reproduce their conclusions and their
errors.

**Do not read any of these until your timeline is written:**

```
❌ eCat_Onboarding/mali/CLIENT_PROFILE.md
❌ eCat_Onboarding/mali/HANDOFF*.md, READINESS_CHECKLIST*.md, LIBRARY-BUILD-CHECKLIST.md
   (mali has many loose notes — treat every .md in eCat_Onboarding/mali/ as forbidden)
❌ eCat_Onboarding/REGISTRY.yaml
❌ onboarding-models/Phase_Anchors.md, Phase_Progression_Framework.md,
   Flags_and_Signals.md, Output_Contract.md, RUN_PROMPT.md, overrides.yml
❌ onboarding-models/ground-truth/SCORECARD.md and other clients' JOURNEY_*.md
❌ any ecat-* skill that describes what phases mean
```

If you open one by accident, say so at the top of your output. A contaminated run that
admits it is useful. One that hides it is worse than none.

---

## Your inputs — read in two passes

| file | what it is |
|---|---|
| `CORPUS_mali_part1.md` | **~108k tokens.** Everything through 2026-03-31. 8 calls, 116 threads. |
| `CORPUS_mali_part2.md` | **~151k tokens.** 2026-04-01 onward. 10 calls, 150 threads. |
| `RAWSTATE_mali.json` | Live DB now — counts, 7 user groups with login stats, audit-log summary. |

All under `eCat_Onboarding/mali/_ground_truth/`.

**Read part 1 fully, write your part-1 notes, then read part 2.** Do not try to hold both
at once. If context gets tight, write an interim timeline after part 1 and extend it.

`supercat-postgres-vpn` (read-only SQL) and `bigquery-admin` MCPs are available — use them
freely. Org id `285`, shortname `mali`. VPN must be up.

---

## The seven phases — questions only, deliberately

You get the *questions* so your output is comparable, and deliberately **not** the rules
the framework uses to answer them. Those rules are what's being tested.

1. **Discovery / Kickoff** — Have we kicked off this client?
2. **Initial Import** — Has at least the products file been imported?
3. **Progress** — Is more than one core file in, without fatal errors on the most recent of each?
4. **Catalog Completeness** — Is the catalog actually buildable as a live iPad?
5. **Reps Signed In** — Are reps actually logging into the iPad?
6. **Admin Training** — Has the admin been trained, with ongoing operations covered?
7. **Go-Live** — Has the formal handoff to support happened, with ongoing client activity?

Answer each from evidence. **If the real story doesn't fit these seven phases, say so** —
on all three previous clients that was among the most valuable output.

---

## Seven questions the phase model does not ask. Answer them anyway.

**A. Did this client ever go backwards?** Stall, regress, nearly churn, go silent? When,
what triggered it, what ended it?

**B. Adoption — separate from go-live.** Who actually used it, how many, how often, doing
what? Names, counts, dates.

**C. Current trajectory.** Improving, steady, or decaying, on what evidence?

**D. Was the catalog ever *wrong* while the imports looked *clean*?** Import tiers record
only whether a file parsed, never whether its contents were right. On one previous client
images imported at clean tier for 18 days with doubled `.jpg.jpg` extensions that could
never match. Look for moments where someone describes something wrong on the iPad, then
check what the import log says about that same day.

**E. Is anything priced as a placeholder, or pointing somewhere that no longer exists?**
On one client every product sat at a $1.00 placeholder. On another, 12 orders worth
$264,130 referenced a price level that had been deleted. Check both directions.

**F. Check `audit_log_entries` — this is a known blind spot.** It is a global table keyed
on `(parent_type, parent_id)`; match this org with
`data::text ILIKE '%"organization":"mali"%'`. Events include `OrgUser destroyd`,
`OrgUser created`, `user group updated`, `Organization updated`. On a previous client it
revealed ten user accounts destroyed and a full customer reload **that appear nowhere in
HelpScout or Fathom**. The summary in `RAWSTATE_mali.json` shows modest activity here —
confirm it and see what the events actually were.

**G. Are the orders bookings or quotations?** Not applicable in the usual way here — see
below — but the underlying question is: **what does "using the system" actually mean for
this client, and has anything ever completed?**

---

## Reading notes specific to mali — this is the most unusual client in the set

- **Zero submitted orders. Ever.** `orders` where org 285 and `is_submitted` = **0**,
  across the org's entire history since 2025-11-21. Meanwhile `status = 'active'`. Whatever
  "live" means here, it does not mean transacting. This is the central fact to explain.

- **Two brands in one org, and they are not equally alive.** ML (Magic Lite, Canada) and
  NSL (US) are separated by user group:

  | group | users | ever logged in | active 30d |
  |---|---|---|---|
  | NSL Reps | 10 | 3 | 3 (most recent **today**) |
  | ML Reps | 5 | **0** | 0 |

  **The entire Magic Lite rep team has never signed in.** Any statement about "mali" that
  doesn't separate the brands is probably wrong. Collections, price levels, email templates
  and branding may diverge per group — check rather than assume.

- **Dual product line.** There are two eOL groups (`eOL ML Public Site`,
  `eOL NSL Public Site`) alongside the iPad groups. This client has a browser catalog as
  well as the iPad. Work out which surface the project was actually about, and whether
  effort went into one at the other's expense.

- **117 of 725 products are visible** — 84% carry `hideable`. That is either a deliberate
  hero-variant strategy or a catalog that never got finished. The record should say which.
  652 of 725 have images, so the hiding is not about missing photos.

- **3,418 customers** — by far the largest in the cohort (next is 389). With 0 orders.

- **`order_email_recipient` is empty.** Nothing has been configured to receive an order.
  Consider whether that is cause or symptom of the zero-order state.

- **Endeavour Solutions is the Business Central integrator** (`endeavoursolutions.com`,
  `endeavor4solutions.com`) and attends calls. Their threads are in the corpus as tier C.
  An ERP integration workstream runs in parallel to onboarding — track it separately and
  say whether it helped or blocked.

- **Part 1 is dominated by internal chatter: 51 tier-B tickets vs 5 tier-A.** Tier B is
  internal SuperCat threads mentioning Magic Lite. That ratio inverts in part 2 (13 A / 6 B).
  Judge tier-B relevance yourself and record what you discarded — a mention is not proof.

- **Duplicate tickets.** On one previous client 21 of 31 tickets were duplicate captures of
  9 conversations. Collapse on subject (ignoring `Re:` / `Fwd:` / `FW:`) before drawing any
  conclusion from ticket volume.

- **`.co` domain variants** (`nslusa.co`, `magiclite.co`) are in the corpus filter and are
  probably typos of the `.com` addresses. Confirm rather than assume.

---

## What to produce

### 1. `eCat_Onboarding/mali/_ground_truth/JOURNEY_mali.md`

Open with a 10–20 line plain-language narrative. Then:

**A. Cast** — every person, email, which side (Magic Lite / NSL / SuperCat / Endeavour),
first and last appearance, role changes.

**B. Phase transitions**, one entry each — and **where ML and NSL diverge, give both**:

```markdown
### Phase 4 → 5 (Reps Signed In) · NSL 2026-06-xx / ML not reached · confidence: high

**What changed:** <one sentence>

**Evidence:**
- [HS #14xxx, 2026-06-xx, jen@magiclite.com (customer)] > "verbatim quote"
- [DB] NSL Reps: 3 of 10 ever logged in; ML Reps: 0 of 5

**Against:** <what argues the other way, or "none">
```

- Every transition needs a date and evidence — verbatim quote with author and timestamp,
  or a specific DB fact.
- Confidence: `high` / `medium` / `low`.
- **If you cannot date a transition, write `undetermined` and explain why. Do not guess.**
- Quote real text. Never paraphrase inside quote marks.

**C. Current phase** as of today — per brand if they differ.

**D. Turning points** — the 3–5 moments that actually moved or blocked this project.

**E. The seven extra questions** (A–G above), answered directly.

**F. The zero-order question**, answered explicitly: why has this client never submitted an
order, and does anyone appear to have noticed?

### 2. `eCat_Onboarding/mali/_ground_truth/GAPS_mali.md`

- What you could not determine, and what evidence would settle it
- Which tier-B tickets you judged irrelevant, and why (part 1 has 51 of them)
- Contradictions between sources — a thread saying one thing, the DB another
- Corpus holes — stretches where the DB shows activity and the corpus shows nothing

---

## Before you finish

1. Does every transition have a date and evidence, or an explicit `undetermined`?
2. Is every quote verbatim, with author and timestamp?
3. Did you read **both** corpus parts in full? Say which parts you skimmed, if any.
4. Confirm explicitly that you avoided all the forbidden files.
5. Did you treat ML and NSL separately wherever the evidence differs?
6. Does your narrative contradict `RAWSTATE_mali.json` anywhere? Flag it — the DB is not
   automatically right either, and a real contradiction is a finding.

Write both files, then stop. Do not touch `CLIENT_PROFILE.md` or any existing `HANDOFF*.md`.
