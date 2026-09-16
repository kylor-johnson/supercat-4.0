---
id: JTBD-REG
title: JTBD register — analytics jobs per SuperCat persona
version: 0.3
status: draft
date: 2026-09-15
owner: Kylor Johnson
depends_on: [PERSONA-GROUPS]
supersedes: v0.2 (jobs listed under PG-01…08 as if those were personas)
note: Old JTBD-0xx IDs are retired. PG-01…08 are motion packs on sales-rep / buyer, not personas.
---

# JTBD register — per SuperCat persona

**Persona = who consumes which product.** Jobs below are the analytics (and the few adjacent) requirements for that person. Selling motion does not mint extra personas. It changes grain on **sales rep** and **buyer** only.

Surfaces are locked in [`../product/surface-mapping.md`](../product/surface-mapping.md):

| Persona | Analytics / requirements land on |
|---|---|
| Admin | **Admin Console** |
| VP of sales | **Sales Portal** |
| Executive | **Insightful** (topline); Portal for account-risk |
| Sales rep | **Existing iPad** for selling. **New iPad-EC** (web component in the offline app) for book analytics. Not Portal-first. |
| Customer / dealer / buyer | **eCat Online** (Catalog / Cart / Closed Site). Not the iPad. |

Invoice feed exists for **38 of 109** roster orgs `[MEASURED]`. Any job whose metric is invoiced net is **STRONG** where the feed exists and **must degrade or suppress** where it does not — never silently substitute eCat-submitted dollars as the business.

---

## 1. Admin — Admin Console

They keep the instance running. They do not want a sales dashboard. Mixpanel will barely see them.

| ID | Job | Decision it changes | Primary metric | Why this surface |
|---|---|---|---|---|
| **JOB-ADM-1** (was HQ-9) | Find where the catalog is broken before a rep does | What to fix this week | Active items missing image, price, or category | Fix happens in Admin. 179,577 of 938,394 active items had no image `[SQL 2026-08-27]` |
| **JOB-ADM-2** (was HQ-4) | Did last night's data land | Whether to trust today's catalog / customers | Import jobs failed in 24h, pushed not visited | Admin is where imports run. An `Error` row silently skips deletes — a failure that looks like success |
| **JOB-ADM-3** (was HQ-7) | Key the order at the right customer and price | Whether CS/order-entry ships garbage | Order-entry error rate | Already served in Admin. Load worse where price codes explode |

**Do not build for admin:** a Portal clone, a rep leaderboard, buyer velocity charts.

---

## 2. VP of sales — Sales Portal

They want the book, the team, and an export that matches the screen. Anatomy already put "sales leadership and CS" here. Portal is **on for 52 of 102** sites. Territory Dashboard is enabled for **0** orgs — so this is not the field-rep surface.

| ID | Job | Decision it changes | Primary metric | Why this surface |
|---|---|---|---|---|
| **JOB-VP-1** (was HQ-5) | Make the export match the screen | Whether anyone trusts Portal | Export-to-UI reconciliation | **EBR-91. Do this first.** Until it ships, Excel is the system of record |
| **JOB-VP-2** (was HQ-3) | Is the team actually using it | Coaching vs. seat-count panic | Reps active 30d ÷ seats licensed | Login-based. Do **not** ungate the `enable_rep_activity` CRM pilot — it is a different feature |
| **JOB-VP-3** (was HQ-6) | Reconstruct one account for a call | First-contact resolution | Time to a full order + invoice history | Best existing Portal fit. Coverage, not a new build. CS shares this job |
| **JOB-VP-4** (was HQ-2) | Which accounts are slipping | Who the team visits | Dollars at risk | **Window follows the client's motion** (below). One T90D rule is wrong for spec and noisy for volume |

**Motion on JOB-VP-4 only:** Luxury Spec → project / 24-month (lumpy is the cycle). Premium Trade → T12M vs prior. Multi-Channel → dealer slice, not marketplace. Volume → replenishment cadence.

**Do not build for VP:** a field-rep "account brief" in Portal. The rep is not here (Mixpanel 90d: 1,933 `product_search` users vs 650 `view_portal` from the iPad WebView).

---

## 3. Executive — Insightful

One number they can defend. Not catalog ops. Not a territory walk-in.

| ID | Job | Decision it changes | Primary metric | Why this surface |
|---|---|---|---|---|
| **JOB-EX-1** (was HQ-1) | One topline I can stand behind | What I say in a board / bank / buyer meeting | Invoiced net, org-wide, period, with provenance | Insightful already exists. **Suppress** without an invoice feed. Do not substitute eCat GMV |
| **JOB-EX-2** | Same as JOB-VP-4, one altitude up | Whether the sales org is working | Dollars at risk, honesty-labelled | Portal or Insightful — not a third product |

**Do not build:** a second Portal. Honesty labelling is the job.

---

## 4. Sales rep — existing iPad (selling) + iPad-EC (analytics)

**Two different things.** Mixing them is how you break the one SuperCat asset that already works.

### 4a. Selling — already served. Protect it.

Catalog, customer, price, stock, write the order, **offline**. Mixpanel 90d: `product_search` 404k events, `customer_search` 174k, `order_submitted` 28k. This is the job. **No new component may spin on a market floor or block this path.**

### 4b. Book analytics — greenfield. New web component inside the iPad.

There is no incumbent (`:portal_portal` = 0 orgs). The constraint is offline, so this cannot live only in Sales Portal. One shell (WebView, extract, staleness, fail-closed). **Job pack keyed off the client's stamped segment.**

| ID | Job | Decision it changes | Primary metric | Pack |
|---|---|---|---|---|
| **JOB-REP-1** | Know this account before I walk in | What I open with | See pack | **PG-01** spec: specified/invoiced, **24 months, by collection**. **PG-03** trade: dealer line vs holes (T12M by collection + SKUs peers carry). **PG-05** mix: *my* dealers only — exclude marketplace/EDI. **PG-07** volume: **skip an L panel**; catalog as reference + fringe |
| **JOB-REP-2** | Answer the question in the appointment | Whether we lose the job to a call-back | Open items + next receipt / lead time for SKUs on the table | All packs. ERP "where is the truck" is **not ours** |
| **JOB-REP-3** | See only my territory, and trust it | Whether I come back or go to Excel | Displayed total = the accounts I cover | Fail closed. Empty territory → show nothing, never whole-org. Caps launch: only **667 of 4,058** iPad-active reps are scopable today `[SQL 2026-08-27]` |

**Do not build:** T90D "account gone quiet" as the spec-rep hero. Pack/velocity as the spec-rep hero. A Portal-first brief. Success metrics based on iPad order-submit at volume (most of that revenue never touches the device).

---

## 5. Customer / dealer / buyer — eCat Online

Our *client's* customer. 87,013 enabled · 18,691 eOL-90d · 62 touched iPad. They cannot reach rep views. **Everything buyer-analytics / buyer-reorder lands on eOL.** That was the original constraint.

| ID | Job | What our client gets | Primary metric | eOL fit by motion |
|---|---|---|---|---|
| **JOB-BUY-1** | Order without waiting for a rep | Capture that otherwise waits for a visit | Buyer-initiated orders as a share of the account | **Spec: highest** (specify / reorder). **Trade: high** (restock the line). **Multi-channel: medium** (fill-in, long tail — not Wayfair). **Volume: near-zero** (Walmart Retail Link will not be replaced) |
| **JOB-BUY-2** | See my price, and whether it's on the floor | Fewer "what's my cost / is it stocked" calls | % product views with entitled price + stock + snapshot age | Same surface. Entitlement is load-bearing at multi-channel (messy price-code tail) |
| **JOB-BUY-3** | Check what I ordered and was billed | CS deflection | Self-service order / invoice lookups | Exists. GA 90d: `/orders` 60k views, `/invoices` 32k — real use. History *beyond* that is a **client-risk config**, not a blanket ungate |

**Do not build:** buyer analytics on the iPad. A velocity dashboard as if the designer were TJX. eOL as a volume growth bet. Ungating purchase history org-wide without the client's say (pricing entitlement + competitive exposure).

Cart is on at ~55 orgs — **coverage and targeting**, not a new surface. Target spec then trade.

---

## ID bridge (engineering)

| New (persona) | Old (v0.2 cell) |
|---|---|
| JOB-ADM-1 / 2 / 3 | JOB-HQ-9 / 4 / 7 |
| JOB-VP-1 / 2 / 3 / 4 | JOB-HQ-5 / 3 / 6 / 2 |
| JOB-EX-1 | JOB-HQ-1 |
| JOB-REP-1 | JOB-01-1 / 03-1 / 05-1 / 07-1 (packs) |
| JOB-REP-2 | JOB-01-2 |
| JOB-REP-3 | JOB-01-3 / 03-3 |
| JOB-BUY-1 / 2 / 3 | JOB-02-1+04-1+06-1+08-1 / 02-2+04-2 / 02-3+04-3 |
| JOB-HQ-8 / 10 (merch grain / intro) | still merch-under-admin; not a sixth persona |

Engineering specs still cite `JOB-01-1` etc. Those remain valid as **pack IDs** on JOB-REP-1.

---

## Cuts (keep)

- Margin / COGS / AR / commission / CSAT — **no data, do not estimate**
- Buyer comparing this manufacturer to others — **against our client's interest**
- Shipment carrier as a SuperCat job — **wrong system (ERP)**
- Agency rollup — **no agency entity; suppress**
- One T90D decline rule for every client — **wrong for spec, noisy for volume**
