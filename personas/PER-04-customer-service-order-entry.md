---
id: PER-04
title: Customer service / order entry
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: within the 2,365 internal admin records; not separately keyed in Postgres
primary_surface: Sales Portal (research) + Admin Console (action)
depends_on: [PER-00]
jobs: [JTBD-041, JTBD-042, JTBD-043, JTBD-044]
---

# PER-04 — Customer service / order entry

> **2026-09-15 — login seat, not the persona set.** Maps to **PG-HQ** in [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). JTBD-0xx IDs below are retired.

**Behavioural definition.** Answers inbound from dealers and reps, keys orders that arrive by phone
/ email / EDI, and researches history when something is disputed. Measured on responsiveness and
accuracy, not on revenue. Works reactively — the queue sets the agenda.

**Why kept.** The Sales Portal spec names them directly as a primary user population:
*"customer-service representatives researching customer, order, and invoice history"*
`[OBSERVED: 00-SALES-PORTAL-SYSTEM-SPEC.md §3]`. And `PLATFORM_ANATOMY §1.6` puts CS alongside
leadership as the Portal's audience — the one point both documents agree on.

**Not separately keyed.** There is no CS role in the schema; they sit inside the 2,365 `is_admin`
records. **That is itself a finding** — we cannot count them, so any claim about CS population is
UNKNOWN.

**Ranked jobs.** 4.

---

## JTBD-041 — Reconstruct one account's history fast *(rank 1)*

**Job.** When a dealer calls disputing something, I want their full order and invoice history in one
place, so I resolve it on the call.

**Decision it changes.** Whether the call ends resolved or becomes a callback — and whether a credit
gets issued on incomplete information.

**Trigger / cadence.** Daily, continuously. The core loop of the role.

**Primary metric.** **Percentage of enquiries resolved on first contact.** *Secondary:*
time-to-answer; count of callbacks created.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Orders by customer, with lines | `orders` | Yes |
| Invoices by customer, with lines | `portal_invoices` | **Partial — 38/109 orgs** |
| Ship-to context | Postgres customers | Yes |
| Order → invoice linkage | Postgres | Spec §10.4 "linked context" |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served — this is the Portal's strongest existing fit.** Customer detail gives
open-order and recent-invoice snapshots plus purchased products (spec §4.2). The gap is not the
surface, it is coverage: with no invoice feed, half the history is missing.

⚠️ **Authorization risk, flagged not resolved.** Spec §7.6: *"Customer detail may allow any
non-customer user with a blank customer number"* and *"invoice show may resolve within the
organization without checking the user's territory book."* A CS user probably *should* see
everything — but that should be a **granted permission**, not an accidental consequence of a blank
field.

---

## JTBD-042 — Key an order that didn't come through the system *(rank 2)*

**Job.** When an order arrives by phone, email or EDI, I want to enter it against the right customer
at the right price, so it flows like any other.

**Decision it changes.** Whether the order is captured correctly first time, or generates a
downstream pricing correction.

**Trigger / cadence.** Daily, continuous.

**Primary metric.** **Order-entry error rate (orders requiring post-entry correction).**
*Secondary:* time per order keyed.

**Data inputs.** Customer file with `DefaultPriceCode`; price levels; options/matrix; inventory.
All exist.

**Varies by segment?** **YES — SEG-03 vs SEG-04.** Price-code complexity differs materially:
SEG-03 median 2 but with a long tail to 35, against **SEG-04 median 1** (flat pricing)
`[MEASURED]`. Picking the right price level is a real decision in a multi-code org and a non-decision
in a flat-priced one.

**Current state.** **Served** via Admin Console / order entry. Listed because it is the volume job
of the role and any analytics built for CS must not interrupt it.

---

## JTBD-043 — Answer "where is it" with a defensible date *(rank 3)*

**Job.** When someone asks when an order ships, I want the best available status, so I give a date I
won't have to walk back.

**Decision it changes.** What the customer is told — and whether they are told something wrong.

**Trigger / cadence.** Daily.

**Primary metric.** **Percentage of status answers given without escalating to another system.**
*Secondary:* count of dates later corrected.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Order status | `orders` | Yes, for SuperCat-submitted orders |
| Invoice against order | `portal_invoices` | **Partial** |
| Ship date / carrier / tracking | client ERP | **DOES NOT EXIST in SuperCat** |
| Inventory next-receipt date | `inventory` | Yes where imported (`NextReceiptDate`) |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Structurally capped, like JTBD-015.** The definitive answer lives in the ERP.
**Do not build a ship-date promise on data we do not hold.** The honest product move is to show
what we have and label its provenance, not to infer a date.

---

## JTBD-044 — Catch the order that will fail before it does *(rank 4)*

**Job.** When an order comes in against stale or missing data, I want to catch it at entry, so it
doesn't fail downstream and come back as a complaint.

**Decision it changes.** Whether the problem is fixed at entry — cheap — or after fulfilment — expensive.

**Trigger / cadence.** Per order; concentrated after an import runs.

**Primary metric.** **Orders rejected or corrected downstream per 1,000 submitted.**
*Secondary:* orders referencing discontinued or soft-deleted items.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Product active / soft-deleted state | `products` | Yes |
| Inventory freshness | `inventory` + import events | Yes, but staleness is not surfaced at entry |
| Import failure state | import events | Yes — Admin Console only |
| **Order-failure reason codes** | — | **DOES NOT EXIST as a queryable field** |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served.** Depends on the missing failure-reason field — see
[`product/data-gaps.md`](product/data-gaps.md). Without it the metric above cannot be
computed at all, only estimated from support tickets.

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "See my own ticket/response volume" | That is a helpdesk metric from a helpdesk system (HelpScout), not SuperCat data. Wrong product |
| "Track customer satisfaction" | No CSAT data in SuperCat |
| "Manage returns / RMA" | Returns are largely absent — prior work bars *"$0 returns"* on gross-only orgs, requiring "returns not represented". Cannot build a job on a field that is systematically empty |
