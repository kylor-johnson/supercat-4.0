---
id: PER-08
title: Dealer buyer — OUR CUSTOMER'S CUSTOMER
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
axis_note: DIFFERENT AXIS — this persona is not a SuperCat client user. Jobs are framed as what OUR CLIENT gains by serving them well.
population: 87,927 enabled / 17,532 active 90d on portal orgs (Postgres, 2026-08-25)
primary_surface: eCat Online (Catalog / Cart / Closed Site) + the buyer half of Sales Portal
depends_on: [PER-00]
jobs: [JTBD-081, JTBD-082, JTBD-083, JTBD-084, JTBD-085, JTBD-086]
---

# PER-08 — Dealer buyer ⚠️ our customer's customer

> **2026-09-15 — login seat, not the persona set.** Do **not** fold designer / dealer / chain buyer into one persona. Those are PG-02, PG-04, PG-06, PG-08 in [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). JTBD-0xx IDs below are retired. Use `JOB-02-*` … `JOB-08-*` in [`analytics/jtbd-register.md`](analytics/jtbd-register.md). Buyer jobs still land on **eCat Online**.

## Read this first — the axis

**This persona does not work for a SuperCat client. They buy from one.** A dealer, designer,
showroom or contract buyer purchasing a manufacturer's line.

**Every job below is written from the buyer's side but justified by what OUR CLIENT gets.** A buyer
job earns its place only if serving it well produces a measurable gain for the manufacturer — orders
captured, calls avoided, share of wallet held. Where a job is good for the buyer and neutral for our
client, it is cut. This persona **must not be collapsed into the internal-user personas**: they share
no session, no permission model, and — measurably — almost no users. Only **593 users** are active
on both iPad and eOL `[MEASURED]`.

## Why this persona exists at all

`[MEASURED 2026-08-25]`, and the reason it was added to scope:

| | Enabled | Active 90d |
|---|---:|---:|
| **Buyers** (`customer_number` present) | **87,927** | **17,532** |
| Reps / internal | 15,987 (eOL, portal orgs) | 2,274 |

**7.7:1 on active logins.** The buyer is the largest user population SuperCat has, on any surface.

**And they are structurally confined.** `should_show_customers_tab` requires
`customer_number.blank?`; `EcatDashboardController#index` redirects anyone failing that check to the
catalog. **A buyer cannot reach the rep views by any configuration.** Meanwhile the analytics above
Orders/Invoices are feature-gated: **Reports → 6 orgs** (`:advanced_reports`), **Territory Dashboard
→ 0 orgs**, and the buyer's own analytics page (`:link_to_customer_dashboard`) → **2 orgs** (`vic`,
`clm`) `[OBSERVED: PERSONA-EVIDENCE.md]`.

**~79% of active buyers see a two-item portal: Orders and Invoices.** That is the single largest
unserved population in the product.

**Ranked jobs.** 6 — more than any internal persona, proportionate to the population.

---

## JTBD-081 — Reorder what I know sells, without help *(rank 1)*

**Job.** When I'm restocking, I want to find and reorder what I've bought before, so I place the
order without waiting for a rep or a callback.

**What our client gets.** Orders captured that would otherwise wait for a rep visit or not happen.
This is the revenue case for the buyer surface — it converts rep-gated demand into self-service
demand.

**Trigger / cadence.** Weekly to monthly per dealer; continuous in aggregate.

**Primary metric.** **Buyer-initiated orders as a share of all orders.** *Secondary:* reorder rate
from purchase history; time from login to submitted order.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Purchase history by customer | `orders` | Yes |
| Contract/customer-specific pricing | `customers` + price levels | Yes |
| Inventory availability | `inventory` | Yes where imported |
| Cart / checkout | eOL Cart | **Yes — but only 58 orgs have `enable_online_ordering`** `[MEASURED]` |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served where Cart is enabled — 58 of 257 orgs.** Prior work found *"~67% are
missing B2B Cart"* in the Commerce-Active segment. The largest population has the thinnest
entitlement.

---

## JTBD-082 — Check what I ordered and what I was billed *(rank 2)*

**Job.** When I'm reconciling, I want my orders and invoices in one place, so I don't phone to ask.

**What our client gets.** **Deflected customer-service calls** — this is the cost case, and it lands
directly on PER-04's queue (JTBD-041). Every self-served reconciliation is a call CS doesn't take.

**Trigger / cadence.** Monthly reconciliation; ad hoc on any discrepancy.

**Primary metric.** **Self-service history lookups per inbound CS enquiry** (ratio; rising is good).
*Secondary:* buyer sessions reaching Orders or Invoices.

**Data inputs.** Orders by customer (**yes**); invoices by customer (**partial — 38/109 orgs**);
order→invoice linkage (**spec §10.4**).

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **This is the one thing essentially every buyer can already do** — Orders and
Invoices are the two items the 79% can reach. Serves the largest population and is already built.
**Protect it; don't regress it.**

---

## JTBD-083 — See what I'm entitled to pay *(rank 3)*

**Job.** When I look at a product, I want to see my price, so I can quote my own customer without
calling.

**What our client gets.** Faster dealer quoting → faster orders; and fewer pricing enquiries into CS.

**Trigger / cadence.** Every browsing session.

**Primary metric.** **Percentage of buyer product views showing a customer-specific price.**
*Secondary:* pricing enquiries into CS.

**Data inputs.** `DefaultPriceCode` per customer; price levels; user-type price visibility; markup
settings (eOL "My Account" per-browser markup). All exist.

**Varies by segment?** **YES — SEG-03.** Mid-Market Multi-Channel carries the widest price-code
spread — median 2 but a long tail to 35 `[MEASURED]` — precisely because it serves trade, retail and
online at once. Entitlement is a genuinely hard problem there and near-trivial in **SEG-04**
(median 1, flat).

**Current state.** **Served**, and one of eOL's real strengths. Listed because the segment variation
above is one of only four in the register and it should inform how the surface is tested.

---

## JTBD-084 — Know what's in stock before I promise it *(rank 4)*

**Job.** When I'm selling to my own customer, I want to know availability and next receipt date, so I
don't promise something that isn't there.

**What our client gets.** Fewer cancellations and backorder disputes; the manufacturer becomes the
easy line to sell.

**Trigger / cadence.** Every quote or order.

**Primary metric.** **Share of buyer orders placed against in-stock items.** *Secondary:*
backorder rate; age of the inventory snapshot at time of view.

**Data inputs.** `inventory` — `QtyAvailable`, `NextReceiptDate`, `NextReceiptQty`.
**Snapshot only, replaced on each import; no history and no freshness indicator surfaced to the
buyer.**

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Partially served.** Availability is shown where inventory is imported. The
buyer is not told **how old** the number is — which matters most for the segment with the largest
catalogs and highest order velocity (SEG-04). **Staleness disclosure is the gap, not the data.**

---

## JTBD-085 — Get through a market appointment and leave with an order *(rank 5)*

**Job.** When I'm at market with a rep, I want the line, my pricing and my history in front of me, so
I commit in the room.

**What our client gets.** **Market-week order capture** — the highest-density selling event of the
year for most of the install base.

**Trigger / cadence.** Market week, twice yearly.

**Primary metric.** **Orders written during market week per attending dealer.** *Secondary:*
order value written in-room vs "sent later".

**Data inputs.** Same as JTBD-081/083 plus rep-side catalog and order pad.

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served through the rep's iPad, not the buyer's own device** — and this is the
seam. The rep is offline-capable; the buyer's eOL session is not. On a market floor with poor
connectivity the buyer half simply does not work. **Directly relevant to Phase 3.**

---

## JTBD-086 — See my own account performance *(rank 6)*

**Job.** When I plan my buying, I want to see what I've bought over time, so I plan against my own
history rather than memory.

**What our client gets.** A dealer who plans against real history buys more predictably — and a
manufacturer who provides that view is harder to displace. **Switching cost, in a segment where
prior work already identifies switching cost as the defence.**

**Trigger / cadence.** Quarterly; at buying-plan time.

**Primary metric.** **Buyer's own invoiced net by period, trailing 24 months.** *Secondary:*
category mix over time; year-on-year change.

**Data inputs.** Invoiced net by customer (**partial — 38/109 orgs**); category mapping (**yes**);
`:link_to_customer_dashboard` (**enabled for 2 orgs — `vic`, `clm`**).

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Effectively unserved — 2 orgs.** `PERSONA-EVIDENCE.md` identifies this as the
biggest untapped surface in the product: rolling `:advanced_reports` from 6 orgs to all 49 portal
orgs *"reaches ~13,800 additional active buyers — a far larger delta than any refinement to the
territory dashboard."*

**Ranked last deliberately.** It has the largest reach and the weakest *decision* attached — a buyer
looking at their own history changes their behaviour only sometimes, whereas JTBD-081 and JTBD-082
change an order or a phone call every time. Reach and job-strength are different axes and this
register ranks on job-strength.

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "Compare this manufacturer's prices to others" | Actively **against** our client's interest. The axis rule kills it |
| "Manage my own retail inventory" | Different product entirely. Not our client's data |
| "See the manufacturer's other dealers" | Competitive information between our client's own customers. Never |
| "Track my shipment" | Same structural cap as JTBD-015/043 — carrier data lives in the ERP, not SuperCat |
| Splitting dealer / designer / contract buyer into three personas | They differ in **pricing entitlement**, not in jobs. Handled inside JTBD-083 as a variation. Three personas, identical job lists, would be false precision |
