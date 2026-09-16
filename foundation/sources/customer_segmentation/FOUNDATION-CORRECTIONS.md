---
id: FOUNDATION-CORRECTIONS
title: Corrections to stamped foundation context — APPLIED 2026-08-26
version: 0.1
status: applied
date: 2026-08-25
applied: 2026-08-26
owner: Kylor Johnson
applies_to:
  - foundation/CEO_SYSTEM_CONTEXT.md
  - foundation/02_who_we_serve.md
  - foundation/sources/customer_segmentation/README.md
depends_on: [TAX-A, TAX-B, TAX-MAP]
---

# Corrections — APPLIED 2026-08-26

**Also applied 2026-09-15 (persona groups).** `CEO_SYSTEM_CONTEXT.md`, `02_who_we_serve.md`,
`01_what_we_do.md`, and `00_README.md` no longer say “jobs don’t differ / build once not on
segment.” Lineage (roster lookup, no segment on prospects) kept. Prior versions:
`foundation/_archive/*_2026-09-15_pre-persona-groups.md`. Canonical persona set:
`sources/customer_segmentation/personas/00-PERSONA-GROUPS.md`. This file remains the record of the
2026-08-26 lineage correction; it is not a second source of truth for personas.

**Status: applied.** Authorised by Kylor 2026-08-26 after the Layer A/B taxonomy was flipped to
`status: hardened`. The hold condition (*"apply after Layer A/B is hardened"*) is satisfied and
discharged.

This file is now the **record of what was changed and why**, not a proposal. The text below is the
correction as applied.

## What was applied

| File | Change | Prior version |
|---|---|---|
| `foundation/CEO_SYSTEM_CONTEXT.md` | Lens 2 section: post-sale-only rule, roster-lookup-not-computation, precise pre-sale limit. Source pointer fixed from the non-existent `skills/customer_segmentation/` | `_archive/CEO_SYSTEM_CONTEXT_2026-08-26_pre-segmentation-lineage-correction.md` |
| `foundation/02_who_we_serve.md` | E1 lineage paragraph added after the segment table; E2 "knowable at first-touch" bullet replaced | `_archive/02_who_we_serve_2026-08-26_pre-segmentation-lineage-correction.md` |
| `foundation/00_README.md` | Date bumped, one-line note pointing at both corrections | — |
| `taxonomy/*.md` (×3) | `status: draft` → `status: hardened`, `hardened: 2026-08-26` added | — |

**Not touched, deliberately:** Lens 1 / D-001a, T1/T2/T3 pricing, the segment names and counts
(33/38/24/14), the orthogonality-to-Lens-1 argument, the stamped v4.0 narrative, `build_v4.py`, the
MASTER CSV, and the "Brand-Building" alias in Insightful profiles.

## Procedure followed — `foundation/00_README.md` § Maintenance

1. ✅ Created `foundation/_archive/` — it did not exist before this change.
2. ✅ Copied the prior version of each edited file into it before editing.
3. ✅ Bumped each edited file's `Last updated`, naming the change and the archived predecessor.
4. ✅ Bumped `foundation/00_README.md`'s date.
5. ✅ `AGENTS.md` warns that several foundation docs carry edits made without bumping the stamp —
   this change did not add to that.

---

## Correction 1 — `CEO_SYSTEM_CONTEXT.md` § ICP Segments — Lens 2 (Selling Motion)

**Problem.** The lens router tells every runtime prompt to use Lens 2 for "GTM, messaging,
positioning, buyer mix, per-account taste" with no statement that Lens 2 is unavailable for
prospects. An agent reading it will apply a selling-motion segment to a company that has no
SuperCat data.

**Second problem, same section.** The Lens 2 preamble implies the segments come from the data. They
come from a stamp. Both corrections go in together.

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
> **The segment assignment is a stamped roster lookup, not a computation.** v4.0 is Kjael's
> selling-motion judgment (2026-07-09) carried from v3.2 and *corroborated* by Postgres, not
> produced by it: an authored rule over the four defining fields reproduces the stamped label only
> 38.5% of the time against a 34.9% majority baseline (n=109), with a 50.0% ceiling even when
> fitted to the answer key. Look the org up in the MASTER roster; do not re-derive it, and do not
> treat a refresh of the underlying numbers as a re-segmentation.
>
> State the pre-sale limit precisely: **binary public feature extraction cannot predict a segment
> (33.3% vs a 34.5% majority baseline, n=87); holistic site reading reaches roughly 53% vs a 30%
> baseline; neither is good enough to label a prospect.** Do not compress this to "public data
> cannot predict segment" — that overstates it.

**Also correct** the source pointer at the end of that section. It currently reads
`skills/customer_segmentation/` — that path does not exist `[MEASURED]`. Should read
`foundation/sources/customer_segmentation/` (README + taxonomy) and
`Customer Segmentation/current/` (v4.0 md + MASTER csv).

---

## Correction 2 — `02_who_we_serve.md` § "A third lens" (whole section)

**This is a bigger correction than first scoped.** The problem is not one sentence. The section
describes the v4.0 segmentation as **data-derived** throughout, and that lineage claim is wrong —
see `taxonomy/account-segments.md` §0. Two distinct errors compound:

| # | Error in the current text | Measured reality |
|---|---|---|
| E1 | Presents v4.0 as derived from first-party data (*"tested … against every available first-party data dimension"*, three axes framed as data-produced) | The segments are **stamped human judgment** carried from v3.2. An authored rule over the four defining fields reproduces the stamped label **38.5%** vs a **34.9% majority baseline (n=109)**; fitted ceiling **50.0%** |
| E2 | States selling motion is *"knowable at first-touch, before any SuperCat usage data exists"* | Tested and false. Holistic public-web reading reaches ~53% vs a 30% baseline; binary feature extraction reaches **33.3% vs a 34.5% majority baseline (n=87)** |

E1 matters more than E2, because E1 is what makes E2 sound reasonable. If the segments were
computed from data, you would expect to find proxies for that data in public sources. They are not,
so there is nothing to proxy.

### Proposed replacement for the section's framing paragraph

> **What this lens is.** The v4.0 client segmentation is a **stamped selling-motion classification —
> Kjael, 2026-07-09 — carried forward from v3.2 and corroborated against first-party Postgres data.**
> It is not computed from that data. An authored rule over the four fields most associated with it
> (average order value, price-code count, customer count, order volume) reproduces the stamped label
> only 38.5% of the time against a 34.9% majority-class baseline, and thresholds fitted directly to
> the roster cap at 50%. The Postgres enrichment was run to **test** the v3.2 model and confirmed
> it; it did not generate it.
>
> This does not weaken the lens. Stamped judgment about observed selling behaviour is a legitimate
> basis under `07_how_we_establish_truth.md` principle 7. It does mean: **the authority is the
> roster lookup, keyed on org shortname — not a recomputation.** New order data does not re-segment
> anyone, and the four fields cannot be used to audit or overturn a stamped label.

### Proposed replacement for the "knowable at first-touch" bullet

> **It is a candidate input for messaging, not for pre-sale qualification.** An earlier version of
> this doc asserted that a prospect's selling motion is "knowable at first-touch, before any
> SuperCat usage data exists." **That has been tested and is false.** Two methods were tried on the
> public web: holistic reading of whole sites reaches roughly 53% against a 30% baseline, and binary
> feature extraction reaches 33.3% against a 34.5% majority-class baseline — i.e. no better than
> guessing the largest segment. Public substitutes were searched for and do not exist: dealer
> locators are private per-brand APIs, sitemaps track web platform rather than business model, and
> the major marketplaces block scraping.
>
> State the limit precisely: **binary public feature extraction cannot predict a segment; holistic
> reading gets to roughly 53%; neither is good enough to label a prospect with a v4.0 segment.** Do
> not shorten this to "public data cannot predict segment" — that overstates the finding and
> misdescribes what a human qualifying a prospect actually does.
>
> Pre-sale classification uses Prospect Archetypes
> (`sources/customer_segmentation/taxonomy/prospect-archetypes.md`), a separate layer whose
> correspondence to the segments is published rather than assumed. One archetype of four beats
> baseline, and its most useful property is **exclusion** (0 of 20 trade-gated orgs are Mid-Market
> Multi-Channel) rather than assignment.

### Also scan and correct in the same file

Any other phrasing that implies the segments were produced by the data rather than confirmed by it,
including the §"v4.0 client segmentation" table preamble and the three-axes description. **Do not
change the segment names, counts (33/38/24/14), or the orthogonality-to-Lens-1 argument** — all
three remain correct.

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
