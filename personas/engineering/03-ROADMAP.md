---
id: ENG-03
title: Prioritised roadmap — persona-group jobs
version: 1.1
status: ready for engineering
date: 2026-09-15
owner: Kylor Johnson
depends_on: [JTBD-REG, PROD-MAP, PROD-GAPS]
supersedes: v1.0 (2026-08-27) "all 31 jobs" seat-register ranking
---

# Roadmap — persona-group jobs, ordered

Canonical order is [`../product/surface-mapping.md`](../product/surface-mapping.md) §2. This file
is the engineering ranking of that list, plus what is declined.

**Trust-before-features (A6 / EBR-91 first) still holds.**

## The reasoning, in five lines

1. **Trust before features.** HQ jobs land on the Sales Portal. A6 fixes the defect that undermines
   every number on it, so it goes first and everything Portal-shaped queues behind it.
2. **Then protect what already works** — existing iPad selling (catalog, customer, price, stock,
   write the order, offline) and eOL Cart / entitled price / order+invoice history where they are on.
   A regression here costs more than any new job earns.
3. **Then no-new-data value, cheapest first** — catalog completeness, snapshot age, login-based
   adoption.
4. **Then the iPad-EC shell, then job packs keyed off the stamped segment** — PG-01 and PG-03 first
   (where eCat is the selling surface). Not one "account brief" for all four motions.
5. **Client-blocked work is ordered by whether we can start the conversation now**, not by job
   strength. The invoice feed is present for 38 of 109 roster orgs. That is a commercial motion, not
   a sprint.

**One thing the ordering does not encode: fixing territory-master coverage would unblock more field
value than any single build below.** `[SQL 2026-08-27]` only **23 of 145** orgs with active iPad reps
have a populated `territories` master, and **935 of 4,058** active reps carry no territory codes at
all. Under the mandatory fail-closed rule those reps see nothing. That sits next to the invoice-feed
push, not in an engineering queue.

---

## A. Ship now — no new data

| # | Job | Group | What | Size | Item |
|---:|---|---|---|---|---|
| 1 | **JOB-HQ-5** | PG-HQ | Make the export match the screen | S | **A6 / SERV-2449** — gates trust in every Portal number |
| 2 | *(protect)* | Field | Existing iPad selling, offline | — | SuperCat's strongest asset; the bar every new component must clear |
| 3 | JOB-02-3 / 04-3 | PG-02 / 04 | Check what I ordered and was billed | — | **Protect.** The one thing ~79% of 17,532 active buyers can already do |
| 4 | JOB-02-2 / 04-2 | PG-02 / 04 | See what I'm entitled to pay | — | **Protect.** eOL's real strength |
| 5 | JOB-HQ-7 | PG-HQ | Key an order from phone/email/EDI | — | **Protect.** Already served |
| 6 | **JOB-HQ-9** | PG-HQ | Find where the catalog is broken | S | **A3.** 179,577 of 938,394 active items have no image `[SQL 2026-08-27]` |
| 7 | **JOB-HQ-3** | PG-HQ | Know the team is actually using it | S | **A4, re-scoped** — login-based view, not the `enable_rep_activity` pilot |
| 8 | JOB-02-2 / 04-2 / 08-2 | Buyers + field extract | Stock with snapshot age | S | **A2.** `max(inventories.updated_at)` is an exact snapshot age |
| 9 | **JOB-HQ-1** | PG-HQ | Get one topline I can defend | S | Honesty labelling only — **STRONG, never FULL**. Ships for the 38 feed orgs; suppress without a feed |
| 10 | JOB-HQ-6 | PG-HQ | Reconstruct one account's history fast | — | Coverage, not build. Portal's strongest existing fit |
| 11 | JOB-02-1 / 04-1 | PG-02 / 04 | Specify / restock without a visit | — | **Config, not build.** Cart `enable_online_ordering`, ~55 orgs. **Target spec then trade.** Not volume. |

---

## B. iPad-EC — one shell, job pack by segment

Sequence after SERV-2196 (blank ship-to over-grant). Not blocked on the invoice feed — `ECAT_ONLY`
ships labelled.

| # | Job | Group | What | Size |
|---:|---|---|---|---|
| 12 | JOB-01-3 / 03-3 | PG-01 / 03 | Territory fail-closed (never whole-org) | M — extract rule, not a widget |
| 13 | *(shell)* | Field | iPad-EC WebView + per-rep extract + staleness | L — **one shell** |
| 14 | **JOB-01-1** | PG-01 | 24-month specified / invoiced by collection | L — `02-IPAD-ACCOUNT-BRIEF-SPEC.md` |
| 15 | JOB-01-2 | PG-01 | Open items + next receipt on that panel | M — ERP truck-status stays blocked |
| 16 | **JOB-03-1** | PG-03 | Dealer line vs holes | L — **different extract grain**, same shell |
| 17 | JOB-03-2 | PG-03 | Under-penetrated dealers | M — needs a baseline store |
| 18 | JOB-05-1 | PG-05 | Dealer slice; exclude marketplace/EDI from "my book" | M |
| 19 | JOB-07-2 | PG-07 | Fringe-only pack | S — **default skip** unless a named client asks |

**Do not** ship #14 as the home screen for #16–19. **Do not** fund an L analytics panel for PG-07.

---

## C. Needs a field we add

Ordered by value ÷ effort, per `data-gaps.md` §D.

| # | Job | Group | Needs | Size |
|---:|---|---|---|---|
| 20 | **JOB-HQ-10** | PG-HQ | Product launch date — one nullable column | S — skip for volume orgs |
| 21 | **JOB-HQ-4** | PG-HQ | Push alerting + failure reason codes | S |
| 22 | **JOB-HQ-2** | PG-HQ | Per-account baseline / **motion-aware** decline window | M — project vs T12M vs replenishment. Do not ship one T90D rule |
| 23 | JOB-HQ-8 | PG-HQ | Inventory history for sell-through | L — grain is collection (spec/trade) vs velocity (volume) |
| 24 | *(CS)* | PG-HQ | Order-failure reason codes | M |

**A5 (JOB-HQ-4) carries a trap worth naming in its ticket:** an `Error` row silently suppresses
deletion of omitted records — a failure that looks like success.

---

## D. Blocked on client data

No surface work fixes any of these.

| # | Job | Group | Blocker |
|---:|---|---|---|
| 25 | JOB-01-3 / 03-3 | Field | **Territory master** — empty in 122 of 145 orgs with active reps `[SQL 2026-08-27]`. Full fix also needs multi-value `RepNumber` (L, EBR-180/SERV-2178, paused) |
| 26 | JOB-01-2 (ERP half) | PG-01 | **ERP open-order status.** Next receipt on inventory is ours; "where is the truck" is not |
| 27 | JOB-HQ-1 / HQ-2 invoiced-net | PG-HQ + field | **Invoice feed.** Order value does not reconcile to a ledger; substituting it defeats the job. Ranked above for the 38 feed orgs; suppress for the rest |

**The invoice feed is the single largest constraint for field and HQ invoiced-net jobs — present
for 38 of 109 roster orgs.** Buyer jobs barely feel it (the feed gap is rep-shaped: half the rep
base, ~6% of buyers — `_measured/00-FINDINGS.md`). Onboarding a feed is the highest-leverage single
change available for those unfed accounts, and it is a conversation, not a sprint.

**Correction to `data-gaps.md` B3.** It states ERP ship status / carrier / tracking is *"not in
SuperCat at all, and not on any current integration path."* That is overstated. `[SQL 2026-08-27]`:
`portal_invoices.tracking_number` is populated on **1,121,123 of 4,940,477** invoices across **26
organizations**, with `tracking_carrier` on 744,046 and `ship_via` on 2,712,248, plus a dedicated
`portal_invoice_tracking_records` table. **This does not unblock JOB-01-2's truck-status half** —
tracking is post-invoice and that job asks about *open* items — so it stays in this bucket. B3's
conclusion stands: **do not build a ship-date promise on data we do not hold.** But a "where did it
ship" answer for already-invoiced orders is available to 26 orgs today and is worth a separate look.

---

## E. Declined this cycle

| Job | Group | Why |
|---|---|---|
| Agency whole-book / sub-rep / prove-agency-value | Agency principal (seat PER-02) | **No agency entity in the schema.** `primary_rep_group` on 142 of 1,980 user types across 39 orgs, 617 iPad-active — but there is no entity behind it, only a boolean and **11,873 distinct free-text `company_name` values**. An agency view built on free-text names would silently merge distinct agencies and split single ones. **Suppress, do not degrade.** |
| PG-07 L analytics panel | PG-07 | Catalog as reference. Most volume revenue never touches the iPad. Default skip. |
| eOL as a volume growth bet | PG-08 | TJX / Walmart / Amazon will not log into eOL. Fringe only, and say so. |
| Buyer purchase-history ungate as a blanket | PG-02/04/06/08 | Client-risk: pricing entitlement + competitive exposure. Config, per client. |
| Portal-first field analytics | PG-01/03/05 | Leaves the offline field case unsolved. HQ stays on Portal. |
| T90D "account gone quiet" as PG-01 hero | PG-01 | Project buying is lumpy. Motion-aware decline is JOB-HQ-2, not the spec-rep panel. |

**View-as (A9)** is severable from the agency entity. If it gets built for "why can't this user see
their book," a scoped preview comes nearly free. It does not reopen the agency persona.

---

## Not on this roadmap, deliberately

Jobs cut for absent data and **kept visible, not deleted** — `data-gaps.md` §C: rep commission,
margin/COGS, AR/cash, CSAT, returns/RMA. **None is a roadmap item.** They are recorded so that when
someone asks why reps cannot see their commission, the answer is a documented schema gap with a
known cost rather than a shrug.

The most significant is **commission**. A rep is paid on what ships, not what they write, and the
system they use every day cannot tell them what they have earned. That is a finding about the
schema, not about the job. It would need ERP payroll integration. **No current path.**

---

## eOL expansion (GTM, not a fourth product)

From the June 29 brief, still the rule:

| Motion | eOL | Why |
|---|---|---|
| Luxury Spec (PG-02) | **Highest** | Showrooms/designers will use a portal |
| Premium Trade (PG-04) | **High** | Dealer restock |
| Multi-Channel (PG-06) | **Medium** | Long tail only; Wayfair never |
| Volume (PG-08) | **Minimal** | Chain HQ never logs in |
