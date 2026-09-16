---
id: PER-05
title: Product / merchandising
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: UNKNOWN — not separately keyed in Postgres. Weakest-evidenced persona kept.
primary_surface: Admin Console (action) + Sales Portal (evidence)
depends_on: [PER-00]
jobs: [JTBD-051, JTBD-052, JTBD-053, JTBD-054]
---

# PER-05 — Product / merchandising

> **2026-09-15 — login seat, not the persona set.** Maps to **PG-HQ** in [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). Grain of "what sold" **does** differ by selling motion. JTBD-0xx IDs below are retired.

**Behavioural definition.** Owns what is in the catalog and how it is presented — categories,
collections, options, images, what launches, what gets discontinued. Judged on whether the
assortment sells, not on individual transactions.

**Why kept.** Admin Console's first capability cluster is *"Catalog & taxonomy ops"*
`[OBSERVED: PLATFORM_ANATOMY §B]`, and catalog structure is substantial and actively maintained —
median **2,344–4,498 products** and **30–381 distinct collections** per org depending on segment
`[MEASURED]`. Someone owns that, and their decisions are exactly the kind analytics should inform.

**Stated plainly: this is the weakest-evidenced persona in the set.** There is no product/merch role
in the schema, no login pattern that isolates them, and no prior persona document names them. It is
kept because the *work* is demonstrably being done, not because the *user* has been observed.
**First candidate to cut if customer evidence does not support it.**

**Ranked jobs.** 4.

---

## JTBD-051 — Know which products are actually selling *(rank 1)*

**Job.** When I plan the next introduction or a discontinuation, I want to see what moved and what
didn't over a real season, so I cut and add on evidence.

**Decision it changes.** What gets discontinued, what gets reordered, what gets developed next.

**Trigger / cadence.** Pre-market (twice yearly) and at line-review.

**Primary metric.** **Units and invoiced net by item for the season, ranked.** *Secondary:*
number of distinct accounts buying each item — breadth, not just volume; sell-through against
inventory received.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Order lines by item | `orders` | Yes |
| Invoiced lines by item | `portal_invoices` | **Partial — 38/109 orgs** |
| Item → category / collection | `products` | Yes |
| Inventory received / on-hand history | `inventory` | **Snapshot only — no history retained** |
| Item lifecycle (launch / discontinue date) | — | **DOES NOT EXIST as a field** |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Partially served.** Sales Portal Dashboard has Top Products — but on
**ordered** amount, not invoiced, and spec §4.5 flags *"Top Product scope under a selected
territory"* as an unresolved area. Reports (Product Detail) is gated to **6 orgs**. Breadth-of-buyers
is not available anywhere.

---

## JTBD-052 — See which options and finishes are chosen *(rank 2)*

**Job.** When I decide which finishes, fabrics or configurations to keep, I want to see what was
actually specified on orders, so I stop carrying dead options.

**Decision it changes.** Which options survive the next catalog — each one carries real cost in
samples, swatches and SKU complexity.

**Trigger / cadence.** Pre-market; at catalog rebuild.

**Primary metric.** **Order-line count per option value over the season.** *Secondary:* options with
zero selections; option combinations that fail validation.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Option selections on order lines | `orders` | **Partial — depends on how options are captured per org** |
| Option / option-group definitions | `options`, `option_groups` | Yes |
| Matrix option pricing | `matrix_options` | Yes |

**Varies by segment?** **DOES NOT DIFFER** — but it only *matters* where CPQ is deployed. Only
**16 orgs** carry the CPQ plan `[OBSERVED: PLATFORM_ANATOMY §2]`. This is a job for a minority of
the install base, and a differentiating one: CPQ depth is named as SuperCat's deepest competitive
advantage.

**Current state.** **Not served.** No option-level analytics exists on any surface.

---

## JTBD-053 — Find where the catalog is broken before a rep does *(rank 3)*

**Job.** When I maintain the catalog, I want to see items missing images, prices or taxonomy, so a
rep never presents a blank tile to a dealer.

**Decision it changes.** What gets fixed this week — and whether a rep is embarrassed in front of a
customer.

**Trigger / cadence.** Weekly; urgently before market.

**Primary metric.** **Count of active items failing a completeness check** (no image, no price, no
category). *Secondary:* items whose images failed to match on import.

**Data inputs.** `products` (image filename, price, category/collection), image-matching results
from import, price level coverage. All exist — **no completeness view aggregates them**.

**Varies by segment?** **YES — SEG-04.** Volume Distribution runs **median 4,498 products against
median 30 collections** — the largest catalogs with the least structure `[MEASURED]`. Manual
eyeballing does not scale there; for a 600-item SEG-01 catalog it is tractable by hand.

**Current state.** **Not served as analytics.** Import status reports errors at load time; nothing
reports standing catalog health. **Cheapest genuinely new job in this register** — the data is all
present and needs only aggregation.

---

## JTBD-054 — See whether a new introduction landed *(rank 4)*

**Job.** After a market introduction, I want to see whether the new group is being ordered and by
whom, so I know within weeks rather than at the next market.

**Decision it changes.** Whether to push, promote, reprice, or quietly drop the introduction.

**Trigger / cadence.** Weekly for the 8–12 weeks after market.

**Primary metric.** **Distinct accounts ordering the new collection, week by week since launch.**
*Secondary:* attach rate to existing lines; first-order lag.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Order lines by collection | `orders` + `products` | Yes |
| **Launch date / "new" flag** | — | **DOES NOT EXIST** — no launch date on a product |
| Account-level first-order date per collection | derivable from `orders` | Yes, computable |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served, and blocked on one missing field.** Everything else is computable;
without a launch date "new" cannot be defined except by manual list. See
[`product/data-gaps.md`](product/data-gaps.md).

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "See margin by product" | **Schema-absent.** No COGS. This is the single most-wanted merchandising metric in the industry and we cannot honestly produce it |
| "Benchmark my assortment against similar brands" | Cross-client comparison. Belongs to the Insights Layer under explicit governance, not to a client-facing persona job |
| "Manage pricing strategy" | Price *setting* happens in the ERP; SuperCat reflects price levels. Wrong system |
| "Plan inventory buys" | Inventory is a **snapshot with no history retained** — a buy-planning job would need trend data that is overwritten on every import |
