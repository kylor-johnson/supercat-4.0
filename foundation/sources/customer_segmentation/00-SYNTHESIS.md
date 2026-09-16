---
id: SYNTHESIS
title: Who we serve, and what we should build — synthesis
version: 0.2
status: draft
date: 2026-09-15
owner: Kylor Johnson
note: 2026-09-15 restores personas-within-segments. Aug 25 lineage/prospect findings kept. "Build once, jobs don't differ by motion" withdrawn as product doctrine.
depends_on: [TAX-A, TAX-B, TAX-MAP, PERSONA-GROUPS, JTBD-REG, PROD-MAP]
---

# Synthesis

---

## 1. Who we serve (unchanged)

**Selling-motion segments are a stamped roster lookup, not a computation.** v4.0 is Kjael's judgment, corroborated by Postgres, not produced by it. Look the org up. Do not re-segment from a refresh of AOV. **Never put a segment label on a prospect** — public-web methods are not good enough (binary extraction 33.3% vs 34.5% baseline; holistic reading ~53%). Pre-sale uses Prospect Archetypes, named for what is observable.

That lineage correction was right. It is not a reason to treat a spec house and a volume feeder as the same product problem.

---

## 2. Persona groups → analytics jobs → surfaces

**The persona set is who consumes which SuperCat product** — admin, VP of sales, executive, sales rep, customer/dealer/buyer. Selling motion parameterizes jobs on **rep** and **buyer** only. That is the July 7 next step, demoted from "eight SuperCat people" to job packs.

**Seats that remain true and useful:**

- Reps and buyers are near-disjoint (4,058 iPad-active vs 17,532 active buyers; 593 overlap).
- Buyers are our customer's customer — jobs only if they pay the manufacturer.
- No incumbent rep analytics surface (`:portal_portal` = 0 orgs).

**Surface lock:**

| Who | Where |
|---|---|
| Buyer jobs | **eCat Online** — eOL fit is highest at spec/trade, medium at multi-channel long-tail, near-zero at volume core |
| Field-rep analytics | **New web component in the iPad** — one shell, job pack keyed off the stamped segment |
| HQ | Sales Portal / Admin / Insightful — here "build once, parameterise" still applies, except decline windows, merch grain, and intro-landing |

Invoice feed still present for **38 of 109** orgs. Commercial-truth jobs suppress without it.

Detail: [`personas/00-PERSONA-GROUPS.md`](personas/00-PERSONA-GROUPS.md) · [`analytics/jtbd-register.md`](analytics/jtbd-register.md) · [`product/surface-mapping.md`](product/surface-mapping.md).

---

## 3. What we'd build, in order

| | Item | Size |
|---|---|---|
| 1 | Export/UI reconciliation (EBR-91) | S |
| 2 | Inventory snapshot age in the UI | S |
| 3 | Catalog completeness view | S |
| 4 | Territory fail-closed (never whole-org) | M |
| 5 | iPad-EC shell + extract | L |
| 6 | PG-01 + PG-03 job packs (spec and trade — where eCat is the selling surface) | M each |
| 7 | PG-05 "my book" excluding marketplace/EDI | M |
| 8 | Motion-aware account-decline (HQ) | M |

**Skip by default:** a volume-rep analytics panel (PG-07); eOL as a growth bet for volume buyers; agency-principal rollup.

**Client motion, not a sprint:** invoice feeds for the 71 orgs without one.

---

## 4. HPMKT (unchanged track)

The exhibitor frame is already ~83% worked. Market week is displacement and re-engagement, not discovery. Lane 3 runs thin at High Point on purpose. Competitor-platform installs (AmpTab, WizCommerce) are a qualification signal, not a segment signal. Field kit is still the deadline-driven gap (Fall 17–21 Oct).

---

## 5. Open decisions

| # | Decision | Status |
|---|---|---|
| **1** | Foundation lineage (roster lookup, no segment on prospects) | **Applied** 2026-08-26 |
| **2** | Field-rep analytics on iPad-EC vs Portal-first | **Picked for this register: iPad-EC.** Offline is the unsolved constraint. HQ stays on Portal. |
| **3** | Expose buyer purchase history org-wide? | Still a client-risk review, not a build |
| **4** | PER-02 agency entity this cycle? | **No.** |
| **5** | Invoice-feed push for 71 orgs? | Still the commercial ceiling |
| **6** | Delete `Customer Segmentation 2` | **Done** 2026-09-15 (byte-identical duplicate) |

Stamp of the nested persona register is **yours** — this is the restored model, not a new segmentation.

---

## Where things are

| Layer | File |
|---|---|
| **Persona groups (start here)** | `personas/00-PERSONA-GROUPS.md` |
| Jobs | `analytics/jtbd-register.md` — `JOB-*` per group |
| Product | `product/surface-mapping.md` · `product/data-gaps.md` (old JTBD-0xx ids, split still valid) |
| Engineering | `engineering/01-NO-NEW-DATA-PACK.md` · `02-IPAD-ACCOUNT-BRIEF-SPEC.md` (PG-01 only) · `03-ROADMAP.md` |
| Review HTML | `PERSONA-GROUPS-REVIEW.html` — stamp packet. August HTMLs are withdrawn stubs |
| Login seats / headcounts | `personas/PER-00-persona-set.md` + PER-01…08 (banners: demoted) |
| Taxonomy | `taxonomy/account-segments.md` · `prospect-archetypes.md` · `segment-archetype-mapping.md` |
| Roster | `Customer Segmentation/current/` — do not duplicate |
| Prospects / field kit | `prospects/` · `field-kit/` — separate track |
