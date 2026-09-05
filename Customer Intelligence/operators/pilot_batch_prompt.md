# Customer Intelligence Pilot — Batch Generation Prompt

> **Purpose**: Generate ~40 Customer Intelligence Briefs across ~20 data-rich SuperCat clients.
> **Agents**: Designed for multi-agent execution. Agent 1 produces a manifest; Agents 2-5 each generate ~10 briefs.
> **Authority**: All brief generation follows `customer_brief_run_prompt.md` exactly.

---

## Prerequisites

- Cursor with `user-supercat-postgres-vpn` and `user-bigquery-admin` MCPs enabled
- VPN active
- Authority files available at `Customer Intelligence/authority/`

---

# Phase A: Discovery & Manifest (Agent 1)

Run this phase first. It produces a manifest that subsequent agents consume.

## A1 — Discover Active Organizations

```sql
-- Postgres (user-supercat-postgres-vpn)
SELECT o.id AS org_id, o.shortname, o.name,
       COUNT(DISTINCT po.customer_bill_to_number) AS distinct_customers,
       COUNT(*) AS total_orders_ltm,
       ROUND(SUM(po.total_amount)::numeric, 2) AS total_revenue_ltm
FROM organizations o
JOIN portal_orders po ON po.organization_id = o.id
WHERE po.order_date >= NOW() - INTERVAL '12 months'
  AND o.shortname NOT ILIKE '%test%'
  AND o.shortname NOT ILIKE '%staging%'
  AND o.shortname NOT ILIKE '%demo%'
GROUP BY o.id, o.shortname, o.name
HAVING COUNT(*) >= 100
ORDER BY total_revenue_ltm DESC
```

This returns all orgs with at least 100 LTM orders, excluding test/staging/demo environments.

## A2 — Profile Each Org (Run Gate Queries)

For **each org** from A1, run all 11 gate queries from `authority/customer_gate_rules.md`:

| Gate | Query Target | MCP |
|------|-------------|-----|
| G-01 `HAS_PORTAL_INVOICES` | `portal_invoice_items WHERE organization_id = {ORG_ID} AND quantity_invoiced > 0` | Postgres |
| G-02 `HAS_COMMITMENT_REPORTS` | `commitment_reports WHERE organization_id = {ORG_ID}` | Postgres |
| G-03 `HAS_PLACEMENT_REPORTS` | `placement_reports WHERE organization_id = {ORG_ID}` | Postgres |
| G-04 `HAS_MIXPANEL_CUSTOMER` | BigQuery events WHERE `current_organization_shortname = '{SHORTNAME}' AND selected_bill_to_code IS NOT NULL` | BigQuery |
| G-05 `HAS_ECAT_ORDERS` | `orders WHERE organization_id = {ORG_ID} AND is_submitted = true AND created_at >= NOW() - INTERVAL '12 months'` | Postgres |
| G-06 `HAS_RMA` | `rma_requests r JOIN org_users ou ON ou.id = r.org_user_id WHERE ou.organization_id = {ORG_ID}` | Postgres |
| G-07 `HAS_BUYER_NAMES` | `portal_orders WHERE organization_id = {ORG_ID}` → pct_populated > 5.0 | Postgres |
| G-08 `COLLECTION_COVERAGE` | `products WHERE organization_id = {ORG_ID} AND deleted = false` → pct >= 50.0 | Postgres |
| G-09 `HAS_SHIP_TO_DATA` | `portal_orders WHERE organization_id = {ORG_ID}` → ship_to pct > 10.0 | Postgres |
| G-10 `FILL_RATE_POPULATION` (v4) | `portal_order_items` quantity_invoiced > 0 for >= 50% of LTM items | Postgres |
| G-11 `HAS_NEW_ITEMS` (v4) | `products WHERE new_item = true AND deleted = false` count > 0 | Postgres |

**Batch optimization**: Gates G-01 through G-11 (except G-04) can all be combined into a single Postgres query per org by using subqueries. G-04 requires BigQuery and must be run separately per org.

**Combined Postgres gate query** (run once per org):

```sql
WITH g01 AS (
  SELECT COUNT(*) AS cnt FROM portal_invoice_items
  WHERE organization_id = {{ORG_ID}} AND quantity_invoiced > 0 LIMIT 1
), g02 AS (
  SELECT COUNT(*) AS cnt FROM commitment_reports WHERE organization_id = {{ORG_ID}}
), g03 AS (
  SELECT COUNT(*) AS cnt FROM placement_reports WHERE organization_id = {{ORG_ID}}
), g05 AS (
  SELECT COUNT(*) AS cnt FROM orders
  WHERE organization_id = {{ORG_ID}} AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at >= NOW() - INTERVAL '12 months'
), g06 AS (
  SELECT COUNT(*) AS cnt FROM rma_requests r
  JOIN org_users ou ON ou.id = r.org_user_id WHERE ou.organization_id = {{ORG_ID}}
), g07 AS (
  SELECT COUNT(*) AS total,
    COUNT(CASE WHEN buyer_name IS NOT NULL AND TRIM(buyer_name) != '' THEN 1 END) AS has_buyer
  FROM portal_orders WHERE organization_id = {{ORG_ID}} AND order_date >= NOW() - INTERVAL '12 months'
), g08 AS (
  SELECT COUNT(*) AS total, COUNT(collection_code) AS has_coll
  FROM products WHERE organization_id = {{ORG_ID}} AND deleted = false
), g09 AS (
  SELECT COUNT(*) AS total, COUNT(customer_ship_to_number) AS has_st
  FROM portal_orders WHERE organization_id = {{ORG_ID}} AND order_date >= NOW() - INTERVAL '12 months'
), g10 AS (
  SELECT COUNT(*) AS total,
    COUNT(CASE WHEN poi.quantity_invoiced > 0 THEN 1 END) AS has_inv
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}} AND po.order_date >= NOW() - INTERVAL '12 months'
), g11 AS (
  SELECT COUNT(*) AS cnt FROM products
  WHERE organization_id = {{ORG_ID}} AND new_item = true AND deleted = false
)
SELECT
  (SELECT cnt > 0 FROM g01) AS has_portal_invoices,
  (SELECT cnt > 0 FROM g02) AS has_commitments,
  (SELECT cnt > 0 FROM g03) AS has_placements,
  (SELECT cnt > 0 FROM g05) AS has_ecat_orders,
  (SELECT cnt > 0 FROM g06) AS has_rma,
  (SELECT CASE WHEN total > 0 THEN 100.0 * has_buyer / total > 5.0 ELSE false END FROM g07) AS has_buyer_names,
  (SELECT CASE WHEN total > 0 THEN 100.0 * has_coll / total >= 50.0 ELSE false END FROM g08) AS has_collection_coverage,
  (SELECT CASE WHEN total > 0 THEN 100.0 * has_st / total > 10.0 ELSE false END FROM g09) AS has_ship_to_data,
  (SELECT CASE WHEN total > 0 THEN 100.0 * has_inv / total >= 50.0 ELSE false END FROM g10) AS fill_rate_population,
  (SELECT cnt > 0 FROM g11) AS has_new_items
```

**BigQuery gate query** (run once per org):

```sql
SELECT COUNT(*) AS event_count
FROM `supercat-data-pipeline.mixpanel.events`
WHERE current_organization_shortname = '{{SHORTNAME}}'
  AND selected_bill_to_code IS NOT NULL
  AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
LIMIT 1
```

## A3 — Compute Data Richness & Select Top 20

Count true gates per org to get the richness score (0-11).

**Selection criteria:**
- Richness >= 5 (Standard or Rich)
- Sort by richness score DESC, then by total_revenue_ltm DESC
- Take top 20

If fewer than 20 orgs meet the threshold, take all that qualify.

## A4 — Select 2 Customers per Org

For each selected org, find the **2 best pilot customers**:

```sql
SELECT customer_bill_to_number AS customer_code,
       c.name AS customer_name,
       c.billing_city, c.billing_state,
       COUNT(*) AS total_orders_ltm,
       ROUND(SUM(po.total_amount)::numeric, 2) AS ltm_revenue,
       COUNT(DISTINCT DATE_TRUNC('month', po.order_date)) AS active_months
FROM portal_orders po
LEFT JOIN customers c ON c.code = po.customer_bill_to_number AND c.organization_id = po.organization_id
WHERE po.organization_id = {{ORG_ID}}
  AND po.order_date >= NOW() - INTERVAL '12 months'
  AND po.customer_bill_to_number IS NOT NULL
GROUP BY po.customer_bill_to_number, c.name, c.billing_city, c.billing_state
HAVING COUNT(*) >= 10
ORDER BY ltm_revenue DESC
LIMIT 2
```

**Requirements:**
- Minimum 10 LTM orders (enough data for interesting analysis)
- Sorted by revenue for the most impactful examples
- `LEFT JOIN customers` provides name/location — may be NULL for some orgs

## A5 — Produce Manifest

Write the manifest to `Customer Intelligence/runs/pilot_manifest.md`:

```markdown
# Customer Intelligence Pilot Manifest

Generated: {{DATE}}

## Org Discovery
- Total orgs with 100+ LTM orders: X
- Orgs with richness >= 4: Y
- Selected for pilot: 20

## Selected Organizations

| # | Org ID | Shortname | Name | Richness | Gates True | LTM Revenue | Customers Selected |
|---|--------|-----------|------|----------|------------|-------------|-------------------|
| 1 | ... | ... | ... | 7/9 | INV,CMT,PLC,MXP,ECAT,COLL,SHP | $X.XM | code1, code2 |
...

## Agent Assignments

### Agent 2 — Orgs 1-5
| Org | Shortname | Org ID | Customer Code | Customer Name |
|-----|-----------|--------|---------------|---------------|
...

### Agent 3 — Orgs 6-10
...

### Agent 4 — Orgs 11-15
...

### Agent 5 — Orgs 16-20
...

## Gate Legend
INV = HAS_PORTAL_INVOICES, CMT = HAS_COMMITMENT_REPORTS, PLC = HAS_PLACEMENT_REPORTS,
MXP = HAS_MIXPANEL_CUSTOMER, ECAT = HAS_ECAT_ORDERS, RMA = HAS_RMA,
BUY = HAS_BUYER_NAMES, COLL = COLLECTION_COVERAGE, SHP = HAS_SHIP_TO_DATA,
FILL = FILL_RATE_POPULATION (v4), NEW = HAS_NEW_ITEMS (v4)
```

---

# Phase B: Brief Generation (Agents 2-5)

Each brief-generating agent receives its assignment from the manifest and runs the full v4 workflow for each org/customer pair.

## B1 — Agent Setup

1. Read the manifest at `Customer Intelligence/runs/pilot_manifest.md`
2. Identify your assigned orgs/customers (Agent 2 = orgs 1-5, Agent 3 = orgs 6-10, etc.)
3. Read all authority files:
   - `authority/customer_query_library.md`
   - `authority/customer_brief_sections.md`
   - `authority/customer_gate_rules.md`
   - `authority/health_score_spec.md`

## B2 — For Each Org/Customer Pair

Follow `operators/customer_brief_run_prompt.md` exactly with these parameters:

| Parameter | Value |
|-----------|-------|
| Client name | From manifest |
| Shortname | From manifest |
| Org ID | From manifest |
| Customer code | From manifest |
| Run date | Current date |

**Output**: `Customer Intelligence/runs/{shortname}/{customer_code}/brief.md`

### Gate caching

Gate results from the manifest can be reused — do not re-run gates. The manifest already contains the full gate profile for each org.

### Execution order within an org

1. Run CQ-01 for customer A → check CQ06_VOLUME_SAFE → run remaining queries → assemble brief A
2. Repeat for customer B
3. Move to next org

### Error handling

- If a query fails, note the error in the brief's cache directory as `errors.md` and skip that section
- If the entire org is unreachable, note it in the manifest and move on
- **Never stop the batch for a single failure**

## B3 — Post-Generation

After all briefs are generated, report a summary:

```
## Batch Complete: Agent N

| Org | Customer | Status | Sections | Health Score |
|-----|----------|--------|----------|-------------|
| ufi | 3002 | Success | 20/23 | 77 |
| ufi | 5001 | Success | 18/23 | 62 |
...

Errors: [list any]
```

---

# Parallelization Guide

Running 40 briefs sequentially in one agent session will likely time out or hit context limits. The recommended split:

| Agent | Role | Orgs | Est. Briefs | Est. Runtime |
|-------|------|------|-------------|-------------- |
| Agent 1 | Discovery + manifest | All | 0 | 10-15 min |
| Agent 2 | Brief generation | 1-5 | 10 | 30-45 min |
| Agent 3 | Brief generation | 6-10 | 10 | 30-45 min |
| Agent 4 | Brief generation | 11-15 | 10 | 30-45 min |
| Agent 5 | Brief generation | 16-20 | 10 | 30-45 min |

**Launching instructions:**

1. Run Agent 1 first — wait for `pilot_manifest.md` to be written
2. Then launch Agents 2-5 in parallel, each with this prompt:

```
You are generating Customer Intelligence Briefs for your assigned orgs from the pilot manifest.

Read the manifest at: Customer Intelligence/runs/pilot_manifest.md
You are Agent [N] — take orgs [X] through [Y] from the manifest.

Follow the Phase B instructions in: Customer Intelligence/operators/pilot_batch_prompt.md

Do not stop for individual failures. Generate all assigned briefs and report a summary when complete.
```

---

# Notes

- The **org ID in the manifest is authoritative** — do not look up org IDs from the organizations table (this was a source of error in v3 testing where the plan had an incorrect org ID).
- Gate G-04 (Mixpanel) requires BigQuery — if BigQuery MCP is unavailable, mark it as false and proceed.
- CQ-06 (Next Best Product) uses tiered volume gate (v4): ≤5K full query, 5K–50K uses CQ-06R 6-month window, >50K skips.
- Placement data may be very old (2017-2019 vintage for some orgs) — still render it with staleness warnings.
- "Uncategorized" categories use tiered callout format (v4): ≤15% no callout, 16-50% inline note, >50% prominent top-of-section callout.
- Ghost SKUs (v4): Distinguish from real stock-outs in §4 — ghost SKUs show "no catalog record", real stock-outs show inventory details + alternatives.
- Fill rate (v4): G-10 gate suppresses §20 and H6 health signal for orgs that don't populate `quantity_invoiced`.
- New intros (v4): G-11 gate skips §5 entirely for orgs with zero `new_item=true` products.

---

*Created: 2026-06-15 | Updated: 2026-06-16 (v4 gates, paths, tiered V-01) | Part of Customer Intelligence v4 Package*
