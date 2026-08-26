---
id: FOUNDATION-CORRECTIONS
title: Proposed corrections to stamped foundation context — HELD, not applied
version: 0.1
status: held-for-approval
date: 2026-08-25
owner: Kylor Johnson
applies_to:
  - foundation/CEO_SYSTEM_CONTEXT.md
  - foundation/02_who_we_serve.md
  - foundation/sources/customer_segmentation/README.md
depends_on: [TAX-A, TAX-B, TAX-MAP]
---

# Proposed corrections — HELD

**Nothing in this file has been applied.** Correcting stamped context to point at a taxonomy that is
still in draft is worse than the current wrong claim. Apply after Layer A/B is hardened.

Sequencing is deliberate: `CEO_SYSTEM_CONTEXT.md` is the file the 10 CEO System prompts actually
read at runtime (it says so itself), so it is corrected **first**. `02_who_we_serve.md` is the
human-facing synthesis and is downstream.

Correction notes, not rewrites. **Do not touch Lens 1 or T1/T2/T3 pricing.**

---

## Procedure when applying — from `foundation/00_README.md` § Maintenance

1. Create `foundation/_archive/` (**does not exist yet** `[MEASURED]`).
2. Copy the prior version of each edited file into it before editing.
3. Bump each edited file's `Last updated`.
4. Bump `foundation/00_README.md`'s date too.
5. `AGENTS.md` warns that several foundation docs already carry edits made without bumping the
   stamp — do not add to that.

---

## Correction 1 — `CEO_SYSTEM_CONTEXT.md` § ICP Segments — Lens 2 (Selling Motion)

**Problem.** The lens router tells every runtime prompt to use Lens 2 for "GTM, messaging,
positioning, buyer mix, per-account taste" with no statement that Lens 2 is unavailable for
prospects. An agent reading it will apply a selling-motion segment to a company that has no
SuperCat data.

**Proposed addition** — new paragraph after the Lens 2 segment table:

> **Lens 2 is post-sale only.** Every field that defines a selling-motion segment — average order
> value, price-code count, customer count, order volume — exists only in SuperCat's Postgres and
> only after an instance is loaded. Predicting Lens 2 from public data alone measures 53% against a
> 30% baseline, and the largest segment (Premium Trade Brand) predicts at 30%. **Never assign a
> selling-motion segment to a prospect**, in a CRM field or otherwise. For pre-sale classification
> use the Prospect Archetypes (`foundation/sources/customer_segmentation/taxonomy/prospect-archetypes.md`),
> which are named for what is observable and never inherit a segment name — per
> `07_how_we_establish_truth.md` principle 7, enrichment is validated *against* a first-party
> segment, never seeded *from* one.
>
> Note also that the segment assignment is **a stamped roster lookup, not a computation**: an
> authored rule over the four defining fields reproduces the stamped label only 38.5% of the time
> against a 34.9% majority baseline (ceiling 50.0% even when fitted to the answer key). Look the
> org up in the MASTER roster; do not re-derive it.

**Also correct** the source pointer at the end of that section. It currently reads
`skills/customer_segmentation/` — that path does not exist `[MEASURED]`. Should read
`foundation/sources/customer_segmentation/` (README + taxonomy) and
`Customer Segmentation/current/` (v4.0 md + MASTER csv).

---

## Correction 2 — `02_who_we_serve.md` § "Why this matters here, and what it doesn't change"

**Problem.** The document states the opposite of the established finding. Current text:

> **It's a candidate input for messaging and GTM qualification**, not for pricing: a prospect's
> market selling motion (e.g. "we specify into hospitality projects" vs. "we sell through a dealer
> network") is **knowable at first-touch, before any SuperCat usage data exists** — closer in
> spirit to the marketing-niche framing below than to the D-001a tiers.

**Proposed replacement** for that bullet:

> **It's a candidate input for messaging, not for pre-sale qualification.** An earlier version of
> this doc asserted that a prospect's selling motion is "knowable at first-touch, before any
> SuperCat usage data exists." **That has been tested and is false.** Predicting the v4.0 segment
> from public data alone reaches 53% against a 30% baseline; Premium Trade Brand, the largest
> segment, predicts at 30%. Public substitutes were searched for and do not exist — dealer locators
> are private per-brand APIs, sitemaps track web platform rather than business model, and the major
> marketplaces block scraping. Selling-motion segmentation works on **customers**, not prospects.
> Pre-sale classification uses Prospect Archetypes
> (`sources/customer_segmentation/taxonomy/prospect-archetypes.md`), a separate layer whose
> measured correspondence to the segments is published rather than assumed — and is weak: 33.3%
> against a 34.5% majority baseline, with one archetype of four beating baseline.

**Leave untouched** in the same section: the "does not change T1/T2/T3 pricing" bullet and the
"open question on expansion path / WTP" bullet. Both remain correct.

---

## Correction 3 — `sources/customer_segmentation/README.md`

**Already applied** (Phase 0 remediation, capped scope): dead links repaired to point at
`Customer Segmentation/current/`, dead `agent_research/` links marked as not-imported, and the new
`taxonomy/` subtree indexed. No file was copied in — one answer key, at the path `build_v4.py`
writes.

**Still outstanding**, deferred:

- The buyer-type coverage line reads "3 reads" in one paragraph and "19 reads / 8 orgs" in another.
  Actual file: **31 rows** `[MEASURED 2026-08-25]`. Needs one accurate number.

---

## Not proposed, deliberately

| Considered | Why not |
|---|---|
| Editing the stamped v4.0 §4 signature bullets, which do not reproduce (ASSUMPTIONS F-01) | Kjael-stamped. Layer A records the discrepancy and supersedes the bullets as a *rule*; the stamped narrative stays as the historical record |
| Sweeping the "Brand-Building" alias out of Insightful profiles and `industry_context.md` | Cosmetic rename across stamped and propagated work. Alias is recorded in `taxonomy/account-segments.md` §1 |
| Anything in Lens 1 / D-001a / PRICING_CONSTITUTION | Out of scope, explicitly |
| `00_README.md`'s "five surfaces" framing vs PLATFORM_ANATOMY's four | Already adjudicated by PLATFORM_ANATOMY § Conflicts resolved; not a new conflict |
