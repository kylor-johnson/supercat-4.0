---
id: PER-01
title: Independent sales rep
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: 4058 iPad-active across 146 orgs (Postgres, 2026-08-25)
primary_surface: eCat iPad (offline)
depends_on: [PER-00]
jobs: [JTBD-011, JTBD-012, JTBD-013, JTBD-014, JTBD-015]
---

# PER-01 — Independent sales rep

**Behavioural definition.** Carries multiple manufacturers' lines. Sells in the field — a dealer's
back office, a designer's studio, a market showroom — frequently with no usable connectivity.
Writes orders on the iPad; the order is often consummated elsewhere (ERP, phone, EDI). Paid on what
ships, not on what is written. Their book is a territory, not the org.

**Existing evidence.** `PERSONA-ONE-PAGERS.md` Persona 1 phrases the core job as *"Show me the truth
about my accounts — what my customers bought and what we invoiced in my territory — so I don't have
to rebuild it in Excel."* Their documented trust failure: pick a territory, still see the whole org,
distrust every number, export to Excel. Validated live — wwjc `cmallon` YTD 1,404 / $1.46M does not
scope to `105:1 Gigi Lane` (710 / $777k) [EBR-40].

**Ranked jobs.** 5. Ranked by how often the decision recurs × how badly it is served today.

---

## JTBD-011 — Know my book before I walk in *(rank 1)*

**Job.** When I'm about to walk into an account, I want to know what they've bought, what's open, and
what they've stopped buying, so I can lead with the right conversation instead of asking them.

**Decision it changes.** What I open the meeting with, and which three products I show first.

**Trigger / cadence.** Pre-appointment. Several times a day in the field; heavily concentrated in
market week.

**Primary metric.** **Invoiced net for this account, trailing 12 months, versus the prior 12.**
*Secondary:* open order value; last order date; count of categories bought last year but not this.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Invoiced net by customer by period | Postgres `portal_invoices` | **Partial — 38 of 109 roster orgs have an invoice feed** `[OBSERVED: v4.0 §1.1]` |
| Open orders by customer | Postgres `orders` | Yes |
| Order lines by category | Postgres `orders` + `products` | Yes |
| Territory → customer mapping | Postgres customer territory | **Yes but unreliable — 32/55 orgs have an empty territory master** [F11] |

**Varies by segment?** **DOES NOT DIFFER.** The job is identical whether the account is a designer
or a big-box dealer; only the vocabulary on screen changes, and that is Lens 2 messaging, not a
different job.

**Current state.** **Not served.** The rep-facing analytics surface is the Sales Portal Territory
Dashboard, which is enabled for **zero orgs**. On the iPad the rep sees the catalog and the customer
record, not purchase history. Today this job is done from memory or a spreadsheet the rep maintains
themselves.

⚠️ **Anatomy/spec conflict bites here.** If Sales Portal is "leadership and CS" (anatomy), this job
has no home and must be built into the iPad. If it is "reps first" (spec), the Portal is the home
and the gap is that it was never enabled. **Same job, two different builds. Unresolved.**

---

## JTBD-012 — See only my territory, and trust it *(rank 2)*

**Job.** When I look at any number in the product, I want it scoped to my territory, so I can act on
it instead of re-deriving it.

**Decision it changes.** Whether the rep uses the product's numbers at all — or exports to Excel and
never comes back. This is the gate on every other analytics job.

**Trigger / cadence.** Every session.

**Primary metric.** **Percentage of the rep's sessions where the displayed total matches their
actual book.** *Secondary:* export-to-UI reconciliation rate.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| User → territory assignment | Postgres user territories | Yes |
| Customer → bill-to / ship-to territory | Postgres | **Yes but 32/55 orgs empty** [F11] |
| `access_all_customer_sales_totals` | user type | Yes |
| Invoice/order `RepNumber` | Postgres | **Partial — scalar column cannot hold comma-separated rep numbers** `[OBSERVED: spec §7.5]` |

**Varies by segment?** **YES — SEG-02.** Premium Trade Brand carries the **highest median territory
count (41)** against a lower median customer count than SEG-01 `[MEASURED]` — broad dealer networks
spread thin. Territory scoping is load-bearing there in a way it is not for a 4-territory SEG-03 org.

**Current state.** **Served badly, and it is the root failure.** EBR-40 (territory doesn't scope),
EBR-212 (dashboard variant stalled since 2022), EBR-91 (export/period drift). Spec §7.6 lists open
authorization risks including invoice show resolving without checking the territory book.

**Non-negotiable.** Fail-closed: empty territory keys → show assigned-only or nothing, **never**
whole-org.

---

## JTBD-013 — Work the whole appointment with no connectivity *(rank 3)*

**Job.** When I'm in a dealer's back office or on a market floor with no signal, I want the full
catalog, customer record and order pad to work, so the appointment doesn't stall.

**Decision it changes.** Whether the order gets written in the room or "sent later" — and orders
sent later frequently become orders not sent.

**Trigger / cadence.** Every field appointment. Continuous during market week.

**Primary metric.** **Percentage of appointments completed without connectivity-caused interruption.**
*Secondary:* time from sync to first usable screen; count of stale-data warnings shown.

**Data inputs.** Local SQLite catalog, customer file, price levels, options/matrix, inventory
snapshot — all already cached on device.

**Varies by segment?** **YES — SEG-04.** Volume Distribution runs **median 4,498 products** against
SEG-02's 1,962, and **median order count 5,759** `[MEASURED]`. Cache size and sync duration are
materially different problems at that end.

**Current state.** **Well served — this is SuperCat's strongest asset.** The iPad is *"fully
offline-capable"* `[OBSERVED: PLATFORM_ANATOMY §1.3]`. The job is listed because **any new
rep-facing analytics component inherits this constraint**, and an online-only analytics panel would
break the one thing that already works. See Phase 3.

---

## JTBD-014 — Spot the account that has gone quiet *(rank 4)*

**Job.** When I plan my week, I want to see which of my accounts have slowed or stopped, so I call
the one that's slipping instead of the one that's easy.

**Decision it changes.** Who gets the call this week.

**Trigger / cadence.** Weekly planning; monthly at minimum.

**Primary metric.** **Count of my accounts whose trailing-90-day invoiced net is down >X% against
their own prior period.** *Secondary:* dollar value at risk; days since last order.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Invoiced net by customer by period | `portal_invoices` | **Partial — 38/109 orgs** |
| Order recency by customer | `orders` | Yes |
| Per-account baseline / seasonality | — | **DOES NOT EXIST — no stored baseline** |

**Varies by segment?** **DOES NOT DIFFER** in the job. The threshold is per-account, not per-segment
— which is exactly why it does not need segment conditioning.

**Current state.** **Not served for reps.** The "accounts fading" signal (S1, EBR-198) exists in the
owner-facing Intelligence concept, not in anything a rep can reach.

---

## JTBD-015 — Answer "where is my order" without calling the office *(rank 5)*

**Job.** When a dealer asks about an order I wrote, I want its current state, so I answer in the room
instead of promising to check.

**Decision it changes.** Whether the rep interrupts customer service, and whether the dealer's
confidence in the rep holds.

**Trigger / cadence.** Reactive, several times a week.

**Primary metric.** **Percentage of order-status questions the rep answers without escalating.**
*Secondary:* order-to-invoice latency visible to the rep.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Order status / lifecycle | Postgres `orders` | Yes — but *"selling instrument ≠ order consummation"*; ERP-consummated orders may be invisible |
| Invoice against order | `portal_invoices` | **Partial — 38/109 orgs** |
| ERP status beyond SuperCat | client ERP | **DOES NOT EXIST in SuperCat** |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Partially served, and structurally capped.** Where an invoice feed exists the
rep can be told. Where it does not, no product change fixes it — the data is not ours. **Do not
build a promise this data cannot keep.**

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "See how I rank against other reps" | **No decision changes** for an independent rep carrying multiple lines — and `RS-01` named rep→revenue is barred below `REP_IDENTITY_TIER` 2, with unmapped reps never silently dropped. A leaderboard on incomplete identity mapping fabricates a ranking |
| "Track my commission" | Commission data is not in SuperCat. Would require ERP payroll integration that does not exist. Suppress rather than approximate |
| "See margin on what I sell" | **Schema-absent.** No COGS. Prior work bars it explicitly: *"No margin / COGS / AR / profitability — suppress, never estimate"* |
