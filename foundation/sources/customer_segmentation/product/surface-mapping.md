---
id: PROD-MAP
title: Surface mapping — persona-group jobs onto eOL, iPad-EC, Portal
version: 0.2
status: draft
date: 2026-09-15
owner: Kylor Johnson
depends_on: [PERSONA-GROUPS, JTBD-REG]
supersedes: Aug 25 mapping that placed 31 seat-jobs and forbade segment-conditional variants
---

# Surface mapping

**Locked product constraint:**

| Persona | Where analytics / requirements go | Why |
|---|---|---|
| **Customer / dealer / buyer** | **eCat Online** (Catalog / Cart / Closed Site) | They are not on the iPad. 18,691 eOL-90d vs 62 buyer iPad-90d. A buyer cannot reach rep views. |
| **Sales rep** — selling | **Existing iPad** | Already the job. Protect it. Mixpanel lives here. |
| **Sales rep** — book analytics | **iPad-EC** — a new web component in the offline iPad | No incumbent (`:portal_portal` = 0). Offline is the unsolved constraint. Portal-first leaves the field case unsolved. |
| **Admin** | **Admin Console** | Catalog, imports, users. Fix happens here. |
| **VP of sales** (and CS) | **Sales Portal** | The book and the team. Portal on 52/102 sites. |
| **Executive** | **Insightful** | One topline. Suppress without an invoice feed. |

**Do not** put spec-rep book analytics only in Sales Portal. **Do not** put buyer reorder on the iPad. **Do not** ship one "account brief" widget for all four motions.

Build the **iPad-EC component once** (one WebView, one extract pipeline, one staleness UI). **Configure JOB-REP-1 by stamped segment** — spec does not get the volume home screen. That is not four products. It is one shell with a motion-specific job list.

---

## 1. Mapping table

Build size: **S** ≤2 weeks · **M** 2–6 weeks · **L** >6 weeks. iPad-EC rows inherit the offline rules in §3.

| ID | Group | Surface | Size | Notes |
|---|---|---|---|---|
| JOB-01-1 | PG-01 spec rep | **iPad-EC** | **L** | Needs invoice feed or labelled order-proxy. 24-month grain, by collection. |
| JOB-01-2 | PG-01 | **iPad** (exists) + **iPad-EC** for open/lead-time | **M** | Lead time/next receipt; ERP ship status is not ours |
| JOB-01-3 | PG-01 | **iPad-EC** | **M** | Territory fail-closed. Fix, not a new idea (EBR-40) |
| JOB-02-1 | PG-02 spec buyer | **eOL Cart** | — | Exists where Cart is on (~55 orgs). Highest-value eOL motion. Coverage, not a new surface |
| JOB-02-2 | PG-02 | **eOL** | **S** | Price + stock already conceptually there; stock needs snapshot age |
| JOB-02-3 | PG-02 | **eOL / buyer Portal** | — | Protect Orders + Invoices. History beyond that is a **client-risk config**, not a build |
| JOB-03-1 | PG-03 trade rep | **iPad-EC** | **L** | Dealer line / holes — different extract than JOB-01-1 |
| JOB-03-2 | PG-03 | **iPad-EC** | **M** | Under-penetrated dealers. Needs a baseline store |
| JOB-03-3 | PG-03 | **iPad-EC** | **M** | Same territory-trust job as 01-3 |
| JOB-04-1 | PG-04 dealer buyer | **eOL Cart** | — | Restock-the-line. Same Cart, different default path than spec |
| JOB-04-2 | PG-04 | **eOL** | **S** | Entitled price + stock |
| JOB-04-3 | PG-04 | **eOL / buyer Portal** | — | Protect |
| JOB-05-1 | PG-05 mix rep | **iPad-EC** | **M** | Book must *exclude* marketplace/EDI accounts the rep does not sell |
| JOB-05-2 | PG-05 | **iPad** (exists) | — | Availability + price — protect |
| JOB-06-1 | PG-06 reorder buyer | **eOL Cart** | — | Long-tail only. Do not sell as Wayfair replacement |
| JOB-06-2 | PG-06 | **eOL** | — | Entitlement; this motion has the messy price-code tail |
| JOB-07-1 | PG-07 volume rep | **iPad** (exists) | — | Catalog reference. **Do not** fund an L analytics panel |
| JOB-07-2 | PG-07 | **iPad-EC** | **S** | Fringe-only; must not ingest chain HQ volume as "my book" |
| JOB-08-1 | PG-08 volume buyer | **eOL Cart** | — | Fringe only. **Not a growth bet** |
| JOB-08-2 | PG-08 | **eOL** | **S** | Next receipt + snapshot age, if we bother |
| JOB-HQ-1 | HQ | **Insightful** (exists) | — | Honesty ceiling: invoice feed or suppress |
| JOB-HQ-2 | HQ | **Portal** | **M** | Motion-aware decline window. Do not ship one T90D rule |
| JOB-HQ-3 | HQ | **Portal** | **S** | Gate is off (`enable_rep_activity` on a handful of orgs), not missing data |
| JOB-HQ-4 | HQ | **Admin** | **S** | Push/alert; data exists, nothing notifies |
| JOB-HQ-5 | HQ | **Portal** | **S** | EBR-91 — gates trust in every Portal number. Do this first among HQ |
| JOB-HQ-6 | HQ | **Portal** (exists) | — | Best current fit. Coverage |
| JOB-HQ-7 | HQ | **Admin** (exists) | — | Load varies; surface does not |
| JOB-HQ-8 | HQ | **Portal** | **M** | Grain by motion (collection vs velocity) |
| JOB-HQ-9 | HQ | **Admin** | **S** | Aggregation, no new fields. Cheapest new HQ job |
| JOB-HQ-10 | HQ | **Portal** | **M** | Needs a launch date / "new" flag. Skip for volume orgs |

---

## 2. What to build, in order

Engineering, ours:

| # | Item | Serves | Size |
|---|---|---|---|
| 1 | Export/UI reconciliation (EBR-91) | JOB-HQ-5 — trust ceiling for every Portal number | S |
| 2 | Inventory snapshot age in the UI | JOB-02-2, 04-2, 08-2, HQ-9 | S |
| 3 | Catalog completeness view | JOB-HQ-9, also PG-07's reason to open the iPad | S |
| 4 | Territory fail-closed (never whole-org) | JOB-01-3, 03-3 | M |
| 5 | iPad-EC shell + per-rep extract | All field analytics | L — **one shell** |
| 6 | PG-01 and PG-03 job packs on that shell | Spec + trade — where eCat is the selling surface | M each |
| 7 | PG-05 exclusion of marketplace/EDI from "my book" | Multi-channel honesty | M |
| 8 | PG-07 fringe pack **or skip** | Volume — default skip unless a named client asks | S |
| 9 | Motion-aware account-decline (JOB-HQ-2) | Owner/VP | M |
| 10 | Product launch date | JOB-HQ-10 | S (nullable column) |

**eOL expansion targeting follows the motion**, as the June 29 brief already had:

| Motion | eOL | Why |
|---|---|---|
| Luxury Spec (PG-02) | **Highest** | Showrooms/designers will use a portal |
| Premium Trade (PG-04) | **High** | Dealer restock |
| Multi-Channel (PG-06) | **Medium** | Long tail only; Wayfair never |
| Volume (PG-08) | **Minimal** | Chain HQ never logs in |

That targeting is a GTM/CS rule, not a fourth product.

**Client must send:** invoice feed for the 71 roster orgs without one. Without it, JOB-01-1 / 03-1 / HQ-1 / HQ-2 cannot be invoiced-net. Degrade to labelled eCat-order views only where the job is "what's the trend on this rail"; **suppress** when the job is "what really happened commercially."

**Do not commit this cycle:** PER-02 agency entity; buyer purchase-history ungate as a blanket (client-risk: pricing entitlement + competitive exposure); a Portal-first rep analytics bet that leaves the field case unsolved.

---

## 3. iPad-EC — offline rules (field components only)

Applies to JOB-01-*, 03-*, 05-1, 07-2. Not to eOL. Not to HQ.

The iPad already embeds WebViews (established pattern, not a new architecture). These components are **read-only**. That removes write-conflict handling.

- **Cache a pre-aggregated extract**, never raw orders/invoices. Budget ~6–8 MB typical, 15 MB for the fat tail. Size on the org's account count / territory size.
- **PG-01 extract ≠ PG-03 extract ≠ PG-07 extract.** Same pipeline, different grain (project/collection vs dealer line vs fringe-only). Segment comes from the roster, not from a threshold on AOV.
- **No network call on render.** Market week is the design case (worst connectivity, highest use).
- Always show data **with its age**. Never empty-state when a cache exists. Never block the existing catalog/customer path if the extract is missing.
- Permission scope is **baked into the extract at sync**. Fail closed. Revocation is not real-time — do not claim it is.
- Sync is a full replace, piggybacked on existing catalog/customer sync. Partial failure leaves the previous complete extract.

**Buyer offline (a dealer on their own phone at market)** is a different and harder problem. Do not assume iPad-EC transfers. Flagged, not solved.

---

## 4. Anatomy vs spec — decided for this register

Sales Portal anatomy says leadership+CS; the Portal spec lists reps first. For **field-rep analytics** this register picks the iPad, because the unsolved constraint is offline, not which web app wraps the query. Getting that wrong toward Portal leaves the field case unsolved. HQ stays on Portal.

If later we enable Territory Dashboard for leadership, that is JOB-HQ-*, not a replacement for iPad-EC.

---

## 5. What August got right, and what it got wrong

Right: disjoint rep/buyer populations; no incumbent rep analytics surface; iPad-EC as the field wrapper; eOL as the buyer surface; invoice feed as the commercial ceiling; agency unservable; EBR-91 first.

Wrong: "one surface serves everyone" as a product conclusion; mapping 31 seat-jobs as if PG-01 and PG-07 shared a home screen; ranking eOL work without the motion targeting the June brief already had.
