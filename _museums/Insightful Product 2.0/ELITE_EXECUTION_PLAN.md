# Elite Insights — Execution Plan

> How to implement the POV enhancements into the existing external report system.
> This document maps each POV item to specific file-level changes.

---

## System Architecture Summary (for context)

The report pipeline has 4 layers:

1. **`scripts/data_gather.py`** — Runs SQL, writes `cache/Q-XX_results.md` files
2. **`authority/query_library.md`** — Canonical SQL definitions
3. **`operators/external/guides/section_NN_*.md`** — Per-section rendering instructions for the agent
4. **`operators/external/run_prompt.md`** + **`shared_rules.md`** — Orchestration + universal rules

To add a new insight, you touch all 4 layers:
- Write the SQL in `query_library.md`
- Register the query in `data_gather.py` (batch assignment, gate check, filename)
- Add the subsection to the relevant `section_NN_*.md` guide (rendering instructions)
- Optionally add new gate flags to `data_gather.py` if conditional

---

## Phase 1 — Org Report Enhancements

### 1A. Competitive Displacement Detection

**What it does**: Detects categories/reps where eCat share is declining while total business grows — "dollars going elsewhere."

**Where it lives**: **§5 Commerce Analytics** — new subsection after current subsection 7 (eCat Capture Rate)

**Gate**: `HAS_PORTAL_ORDERS = true` (already exists)

**Files to change**:

| File | Change |
|---|---|
| `authority/query_library.md` | Add **Q-55: Category-Level Competitive Displacement** — compares `portal_order_items` by category for current vs. prior 90-day window against `orders` by same category |
| `authority/query_library.md` | Add **Q-56: Per-Rep Capture Rate Trend** — `portal_orders` by rep (current vs. prior quarter) against `orders` by rep |
| `scripts/data_gather.py` | Add Q-55 and Q-56 to **Batch F** (portal_orders conditional), write `Q-55_results.md` and `Q-56_results.md` |
| `operators/external/guides/section_05_commerce.md` | Add subsection 8: "Competitive Displacement Signals" — render when `HAS_PORTAL_ORDERS = true` AND Q-55 has data rows showing any category where eCat share declined while total grew |
| `operators/external/guides/section_05_commerce.md` | Add Q-55, Q-56 to Query Inputs block and Conditional Subsection Checklist |

**SQL sketch (Q-55)**:
```sql
WITH current_period AS (
  SELECT
    p.category_code AS category,
    SUM(poi.unit_price * poi.quantity_ordered) AS total_business_gmv,
    SUM(CASE WHEN poi.ecat_item_number IS NOT NULL THEN poi.unit_price * poi.quantity_ordered ELSE 0 END) AS ecat_match_gmv
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  JOIN products p ON p.item_number = poi.item_number AND p.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '90 days'
  GROUP BY p.category_code
),
prior_period AS (
  -- same structure for 91-180 days ago
)
SELECT
  c.category,
  c.total_business_gmv AS current_total,
  p.total_business_gmv AS prior_total,
  -- eCat share current vs. prior
  ...
```

**Note**: The exact SQL needs validation against the schema — `portal_order_items.ecat_item_number` is the join back to eCat catalog. But the core logic is: compare total-business category mix between periods and flag categories where total grew but eCat share dropped.

---

### 1B. Quantified Whitespace Summary

**What it does**: Wallet share estimation + cross-sell gaps at the org level (aggregated across top accounts).

**Where it lives**: **§3 Customer & Buyer Intelligence** — new subsection after current subsection 7 (New eCat Buyer Acquisition)

**Gate**: `PORTAL_CUSTOMER_DATA_PRESENT = true` (already exists)

**Files to change**:

| File | Change |
|---|---|
| `authority/query_library.md` | Add **Q-57: Cross-Sell Whitespace by Category** — For each top-20 customer, identify categories they DON'T buy but similar customers do. Aggregate to org level: "X categories with $Y addressable whitespace across top accounts" |
| `scripts/data_gather.py` | Add Q-57 to **Batch F** (portal_orders conditional), write `Q-57_results.md` |
| `operators/external/guides/section_03_customers.md` | Add subsection 8: "Whitespace Opportunity" — table showing categories with addressable gap + callout with aggregate opportunity |

**SQL approach**: Group customers by their purchased category mix → find "peer customers" (same 2+ categories) → identify categories present in peers but absent in target → quantify by peer average GMV in that category.

---

### 1C. Post-Market Attribution

**What it does**: Connects High Point / market commitments to actual closed orders.

**Where it lives**: **§5 Commerce Analytics** — new subsection 9 OR new **§5b section** (if it's large enough)

**Gate**: Requires `commitment_reports` data present for the org (new gate: `HAS_COMMITMENT_DATA`)

**Files to change**:

| File | Change |
|---|---|
| `scripts/data_gather.py` | Add new gate `HAS_COMMITMENT_DATA` (check `commitment_reports` count for org) in preflight |
| `authority/query_library.md` | Add **Q-58: Market Commitment Conversion** — join `commitment_reports` items to `portal_order_items` within 90 days of market date |
| `scripts/data_gather.py` | Add Q-58 to new conditional batch (gated on `HAS_COMMITMENT_DATA`), write `Q-58_results.md` |
| `operators/external/guides/section_05_commerce.md` | Add subsection 9: "Market Attribution" — conversion rate, unrealized commitments still in stock, ROI estimate |
| `scripts/data_gather.py` `GateFlags` | Add `HAS_COMMITMENT_DATA: bool = False` |

**Challenge**: `commitment_reports.items` is a text field (comma-separated item list) — needs parsing. Market code identifies which show. Need to determine date logic (market date → order window).

---

### 1D. Reorder Velocity Early Warning

**What it does**: Detects accounts whose order frequency is decelerating — 60-90 day warning before revenue drop.

**Where it lives**: **§3 Customer & Buyer Intelligence** — ENHANCE existing subsection 6 (Reorder Velocity & Early Warning, Q-14)

**This replaces/enhances existing content, not net-new.**

**Files to change**:

| File | Change |
|---|---|
| `authority/query_library.md` | **Enhance Q-14** (or add Q-14b): Add interval-over-interval comparison per account — compute `recent_avg_interval / historical_avg_interval` ratio. Flag accounts where ratio > 1.5x |
| `scripts/data_gather.py` | Modify Q-14 execution OR add Q-14b alongside it — write enhanced results to `Q-14_results.md` (or `Q-14b_results.md`) |
| `operators/external/guides/section_03_customers.md` | Enhance subsection 6 rendering rules: add "Deceleration Alert" table for accounts crossing the 1.5x threshold, with combined annual value at risk |

**SQL sketch**:
```sql
WITH customer_intervals AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    order_date,
    LAG(order_date) OVER (PARTITION BY customer_bill_to_number ORDER BY order_date) AS prev_order_date,
    order_date - LAG(order_date) OVER (...) AS interval_days
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '18 months'
),
interval_comparison AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    AVG(CASE WHEN order_date >= NOW() - INTERVAL '6 months' THEN interval_days END) AS recent_avg,
    AVG(CASE WHEN order_date < NOW() - INTERVAL '6 months' THEN interval_days END) AS historical_avg
  FROM customer_intervals
  WHERE interval_days IS NOT NULL
  GROUP BY customer_bill_to_number, customer_bill_to_name
  HAVING COUNT(*) >= 4  -- need enough data points
)
SELECT *, recent_avg / NULLIF(historical_avg, 0) AS deceleration_ratio
FROM interval_comparison
WHERE recent_avg / NULLIF(historical_avg, 0) > 1.5
ORDER BY ... -- by annual GMV at risk
```

---

### 1E. Fill Rate Revenue Impact

**What it does**: Quantifies revenue impact of stockouts/backorders by correlating backorder events with reorder interval stretching.

**Where it lives**: **§4 Product & Inventory Intelligence** — new subsection after "Top Sellers OOS" (subsection 1)

**Gate**: `HAS_PORTAL_ORDERS = true` AND `HAS_INVENTORY = true` (both already exist)

**Files to change**:

| File | Change |
|---|---|
| `authority/query_library.md` | Add **Q-59: Backorder Revenue Impact** — compute fill rate from `portal_order_items` (qty_ordered vs qty_invoiced), correlate backordered items with that customer's subsequent reorder interval |
| `scripts/data_gather.py` | Add Q-59 to **Batch G** (inventory + sales conditional), write `Q-59_results.md` |
| `operators/external/guides/section_04_product.md` | Add subsection 1b: "Fill Rate Revenue Impact" — overall fill rate + top-5 impacted SKUs with projected annual revenue at risk |

**SQL approach**: 
- Calculate org fill rate: `SUM(qty_invoiced) / SUM(qty_ordered)` from `portal_order_items`
- Identify top backordered items: group by `item_number` WHERE `quantity_backordered > 0`
- Cross-reference those items with `inventories.qty_on_backorder` for current status
- For each impacted item, multiply annual velocity × average unit price to get revenue exposure

---

## What Existing Content Gets REPLACED vs. ENHANCED

| Current Subsection | Action | Notes |
|---|---|---|
| §3.6 Reorder Velocity (Q-14) | **ENHANCE** — add deceleration alert layer | Keep current output + add early warning table |
| §5.7 eCat Capture Rate (Q-45) | **KEEP** — displacement signals go AFTER it | New subsection 8 builds on this concept |
| §4.1 Top Sellers OOS (Q-37) | **ENHANCE** — add revenue quantification layer | Current shows "what's out of stock." New adds "what it's costing you." |
| §5.4 Top Buyers (Q-13) | **KEEP** — whitespace is a separate §3 subsection | No change to existing, new stuff is additive |

---

## New Gate Flags Required

| Flag | Condition | Used By |
|---|---|---|
| `HAS_COMMITMENT_DATA` | `commitment_reports` count > 0 for org | Q-58 (Post-Market Attribution) |

All other new insights use existing gates (`HAS_PORTAL_ORDERS`, `PORTAL_CUSTOMER_DATA_PRESENT`, `HAS_INVENTORY`).

---

## New Queries Summary

| Q-ID | Name | Source | Gate | Section |
|---|---|---|---|---|
| Q-55 | Category-Level Competitive Displacement | Postgres | `HAS_PORTAL_ORDERS` | §5.8 |
| Q-56 | Per-Rep Capture Rate Trend | Postgres | `HAS_PORTAL_ORDERS` + `PORTAL_REP_DATA_PRESENT` | §5.8 |
| Q-57 | Cross-Sell Whitespace by Category | Postgres | `PORTAL_CUSTOMER_DATA_PRESENT` | §3.8 |
| Q-58 | Market Commitment Conversion | Postgres | `HAS_COMMITMENT_DATA` | §5.9 |
| Q-14b | Reorder Velocity Deceleration | Postgres | `HAS_PORTAL_ORDERS` | §3.6 (enhanced) |
| Q-59 | Backorder Revenue Impact | Postgres | `HAS_PORTAL_ORDERS` + `HAS_INVENTORY` | §4.1b |

---

## Confidence Framework Impact

The new subsections are ALL gated on `HAS_PORTAL_ORDERS` (which already drives STRONG/FULL tiers). No new confidence tier logic needed — the framework already handles this:
- Orgs WITHOUT portal_orders → these subsections don't render → section stays PARTIAL
- Orgs WITH portal_orders → these subsections render → section already at STRONG or FULL

---

## Phase 2 — Per-Customer Brief (Separate Operator)

This is a **completely separate operator** living alongside the org report. It needs:

- `operators/customer_brief/run_prompt.md` — new orchestrator
- `operators/customer_brief/guides/` — section guides for each brief section
- New queries in `query_library.md` (Q-CB-01 through Q-CB-12)
- A separate execution path in `data_gather.py` (or a new script `data_gather_customer.py`)

This is Phase 2 and should NOT be built until Phase 1 is validated.

---

## Implementation Dependencies

```
Q-55, Q-56 → §5 guide update → ready to run
Q-57       → §3 guide update → ready to run  
Q-14b      → §3 guide update → ready to run (enhances existing)
Q-58       → new gate + §5 guide update → ready to run
Q-59       → §4 guide update → ready to run
```

All 5 are independent — they can be built in any order or in parallel.
