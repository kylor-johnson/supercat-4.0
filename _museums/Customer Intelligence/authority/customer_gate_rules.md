# Customer Intelligence Brief — Gate Rules

> **Status**: Production v5 — 2026-06-29 (added **G-00 provenance preflight** — the Layer-3 re-anchor on the
> invoiced spine). v4 baseline validated 2026-06-16 (G-10 fill rate population, G-11 new item count).
> **Scope**: Defines conditional rendering gates for the Customer Intelligence Brief.
> Each gate is a fast diagnostic query that determines whether a section will render.
> Gates run once per org (not per customer) and can be cached for the session.

---

## Gate Definitions

### G-00: `TOTAL_BUSINESS_PROVENANCE` (v5 — the provenance preflight; run FIRST)

> **This gate is the single inheritance point for the invoiced-truth re-anchor.** It mirrors the Layer-1
> `Q-PROV-00` / `Q-ECON-00` contract (`provenance_spine.md` §6.1, §6.3, §6.8 — *locked, read-only*) and
> resolves the source, confidence, completeness, and clamp that **every Total in the brief inherits**. Run it
> before CQ-01. Nothing that prints a dollar may bypass it.

**Effect**: Sets four org-level values consumed everywhere a Total is shown:

| Output | Values | Effect on the brief |
|---|---|---|
| `TOTAL_BUSINESS_SOURCE` | `INVOICES` / `ORDERS` / `SALES_DATA` / `NONE` | which dollar source CQ-01/10/22/23 read (invoiced net vs booked fallback vs suppress) |
| `COMMERCE_CONFIDENCE` | `STRONG` / `PARTIAL` / `LIMITED` / `NONE` (**never `FULL`** — a single invoice feed can't corroborate completeness) | the confidence tier stamped on every Total; a composite (health score) inherits the **lowest** input (Spine §5.3) |
| `FEED_COMPLETENESS` | `CORROBORATED` / `UNVERIFIED — SINGLE FEED` / `PROVABLY INCOMPLETE` / `STALE` / `DEAD` | the completeness word on every Total; **suppress all Totals on `PROVABLY INCOMPLETE` / `DEAD`** |
| `report_through_date` | `LEAST(MAX(invoice_date), CURRENT_DATE)` | clamps every LTM/prior window (kills bad-date invoices like clm 4107 / jyc 2032) |

**MCP**: `user-supercat-postgres-vpn`

```sql
WITH inv AS (
  SELECT
    COUNT(*)                                  AS invoice_rows,
    MAX(invoice_date)                         AS max_invoice_date,
    LEAST(MAX(invoice_date), CURRENT_DATE)    AS report_through_date,
    (CURRENT_DATE - LEAST(MAX(invoice_date), CURRENT_DATE)) AS days_since_last_invoice
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND net_amount IS NOT NULL
),
inv_ltm AS (
  SELECT COALESCE(SUM(pi.net_amount), 0) AS invoiced_net_ltm
  FROM portal_invoices pi, inv
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date >  inv.report_through_date - INTERVAL '12 months'
    AND pi.invoice_date <= inv.report_through_date
),
booked_ltm AS (
  SELECT COALESCE(SUM(po.total_amount), 0) AS booked_gmv_ltm
  FROM portal_orders po, inv
  WHERE po.organization_id = {{ORG_ID}}
    AND po.order_date >  inv.report_through_date - INTERVAL '12 months'
    AND po.order_date <= inv.report_through_date
),
ecat_ltm AS (
  SELECT COALESCE(SUM(o.total), 0) AS ecat_gmv_ltm
  FROM orders o, inv
  WHERE o.organization_id = {{ORG_ID}}
    AND o.is_submitted = true
    AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
    AND COALESCE(NULLIF(TRIM(o.order_type), ''), 'Confirmed') NOT IN
        ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND o.order_type NOT ILIKE 'HFC%' AND o.order_type NOT ILIKE 'Hold%' AND o.order_type NOT ILIKE 'TEST%'
    AND o.created_at >  inv.report_through_date - INTERVAL '12 months'
    AND o.created_at <= inv.report_through_date + INTERVAL '1 day'
)
SELECT
  inv.report_through_date,
  inv.days_since_last_invoice,
  inv_ltm.invoiced_net_ltm,
  booked_ltm.booked_gmv_ltm,
  ecat_ltm.ecat_gmv_ltm,
  CASE WHEN inv_ltm.invoiced_net_ltm > 0
       THEN ROUND(ecat_ltm.ecat_gmv_ltm / inv_ltm.invoiced_net_ltm, 3) END AS ecat_capture_ratio,
  CASE WHEN inv_ltm.invoiced_net_ltm > 0
       THEN ROUND(booked_ltm.booked_gmv_ltm / inv_ltm.invoiced_net_ltm, 3) END AS booked_over_invoiced,
  -- TOTAL_BUSINESS_SOURCE
  CASE
    WHEN inv.invoice_rows > 0 AND inv_ltm.invoiced_net_ltm > 0 THEN 'INVOICES'
    WHEN booked_ltm.booked_gmv_ltm > 0                         THEN 'ORDERS'
    ELSE 'NONE'
  END AS total_business_source,
  -- FEED_COMPLETENESS (Spine §6.3 triangulation)
  CASE
    WHEN inv.invoice_rows = 0 OR inv_ltm.invoiced_net_ltm = 0                       THEN 'DEAD'
    WHEN ecat_ltm.ecat_gmv_ltm > 1.05 * inv_ltm.invoiced_net_ltm                    THEN 'PROVABLY INCOMPLETE'
    WHEN inv.days_since_last_invoice > 45                                           THEN 'STALE'
    WHEN booked_ltm.booked_gmv_ltm BETWEEN 0.90 * inv_ltm.invoiced_net_ltm
                                       AND 1.10 * inv_ltm.invoiced_net_ltm          THEN 'CORROBORATED'
    ELSE 'UNVERIFIED — SINGLE FEED'
  END AS feed_completeness,
  -- COMMERCE_CONFIDENCE (LEAST(own ceiling, completeness); FULL unreachable)
  CASE
    WHEN inv.invoice_rows = 0 OR inv_ltm.invoiced_net_ltm = 0    THEN 'NONE'
    WHEN ecat_ltm.ecat_gmv_ltm > 1.05 * inv_ltm.invoiced_net_ltm THEN 'PARTIAL'
    WHEN inv.days_since_last_invoice > 45                        THEN 'PARTIAL'
    ELSE 'STRONG'
  END AS commerce_confidence
FROM inv, inv_ltm, booked_ltm, ecat_ltm
```

**Rules**:
- `total_business_source = NONE` → the brief runs in **behavior-only** mode (no dollar Totals; eCat capture in
  absolute dollars only, clearly labeled "captured through eCat, not total business").
- `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` → **suppress every Total** (do not print "total business
  $X"); the competitive-loss banner and revenue-at-risk headline are also suppressed (they ride the Total).
- `feed_completeness ∈ {PARTIAL, STALE}` → print Totals as **directional/ranged** with the loud completeness
  caveat; clamp windows to `report_through_date`.
- This gate's outputs are **org-level** and cached for the session; pass `report_through_date` and
  `total_business_source` to CQ-01/10/22/23.

---

### G-01: `HAS_PORTAL_INVOICES`

**Effect when false**: CQ-02 through CQ-06 (category/SKU/collection analysis) unavailable — brief runs in "orders-only" mode. Spend Trajectory (CQ-10) and Frequency (CQ-07) still work via `portal_orders`.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS invoice_item_count
FROM portal_invoice_items
WHERE organization_id = {{ORG_ID}}
  AND quantity_invoiced > 0
LIMIT 1
```

**Rule**: `true` if `invoice_item_count > 0`.

---

### G-02: `HAS_COMMITMENT_REPORTS`

**Effect when false**: CQ-17 (Market Commitments) section skipped entirely.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS commitment_count
FROM commitment_reports
WHERE organization_id = {{ORG_ID}}
```

**Rule**: `true` if `commitment_count > 0`.

---

### G-03: `HAS_PLACEMENT_REPORTS`

**Effect when false**: CQ-18 (Showroom Placements) section skipped entirely.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS placement_count
FROM placement_reports
WHERE organization_id = {{ORG_ID}}
```

**Rule**: `true` if `placement_count > 0`.

---

### G-04: `HAS_MIXPANEL_CUSTOMER`

**Effect when false**: CQ-13 (Rep Engagement) section skipped entirely. This gate is org-specific — prototype found SC has rich customer-attributed Mixpanel data, UFI/CCI have none.

**MCP**: `user-bigquery-admin`

```sql
SELECT COUNT(*) AS event_count
FROM `supercat-data-pipeline.mixpanel.events`
WHERE current_organization_shortname = '{{ORG_SHORTNAME}}'
  AND selected_bill_to_code IS NOT NULL
  AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
LIMIT 1
```

**Rule**: `true` if `event_count > 0`.

---

### G-05: `HAS_ECAT_ORDERS`

**Effect when false**: eCat portion of CQ-01 collapsed to a single-line note ("Account does not use eCat iPad — orders via [channel]") rather than a table of zeros.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS ecat_order_count
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at >= NOW() - INTERVAL '12 months'
```

**Rule**: `true` if `ecat_order_count > 0`.

---

### G-06: `HAS_RMA`

**Effect when false**: CQ-16 (Returns) section skipped entirely. Prototype found zero RMA data across all 7 test customers.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS rma_count
FROM rma_requests r
JOIN org_users ou ON ou.id = r.org_user_id
WHERE ou.organization_id = {{ORG_ID}}
```

**Rule**: `true` if `rma_count > 0`.

Note: `rma_requests` has no `organization_id` column — must route through `org_users`.

---

### G-07: `HAS_BUYER_NAMES`

**Effect when false**: CQ-14 (Buyer Intelligence) section skipped entirely. Prototype found buyer_name unpopulated for 6 of 7 customers — mostly an EDI/portal data gap.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT
  COUNT(*) AS total_orders,
  COUNT(CASE WHEN buyer_name IS NOT NULL AND TRIM(buyer_name) != '' THEN 1 END) AS has_buyer,
  ROUND(100.0 * COUNT(CASE WHEN buyer_name IS NOT NULL AND TRIM(buyer_name) != '' THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS pct_populated
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months'
```

**Rule**: `true` if `pct_populated > 5.0`.

Note: EDI orders often populate `buyer_name` as an empty string rather than NULL. The gate must check for non-empty values, not just non-NULL.

---

### G-08: `COLLECTION_COVERAGE`

**Effect when false (< 50%)**: CQ-04 (Collection Mix) folded into a single note under the Categories section instead of a standalone section. Prototype found CCI at 85-88% "Core/Unassigned" — collection taxonomy underutilized.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT
  COUNT(*) AS total_products,
  COUNT(collection_code) AS has_collection,
  ROUND(100.0 * COUNT(collection_code) / NULLIF(COUNT(*), 0), 1) AS pct_with_collection
FROM products
WHERE organization_id = {{ORG_ID}}
  AND deleted = false
```

**Rule**: `true` if `pct_with_collection >= 50.0`.

---

### G-09: `HAS_SHIP_TO_DATA`

**Effect when false**: CQ-21 (Same-Store Comps) section skipped entirely. Prototype investigation found UFI has zero ship-to population in `portal_orders`, CCI has partial (13% codes, 99.99% names), SC has 100%. This is an org-specific data-supply issue driven by the client's `order_data.csv` export.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT
  COUNT(*) AS total_orders,
  COUNT(customer_ship_to_number) AS has_ship_to,
  ROUND(100.0 * COUNT(customer_ship_to_number) / NULLIF(COUNT(*), 0), 1) AS pct_populated
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months'
```

**Rule**: `true` if `pct_populated > 10.0`.

---

### G-10: `FILL_RATE_POPULATION` (v4, audit finding §2)

**Effect when false**: §20 Fulfillment / Fill Rate section is **suppressed entirely** — brief renders a single-line note: *"Fill rate data unavailable — this org does not populate invoice quantities."* Additionally, health score signal H6 is **skipped** (excluded from both numerator and denominator).

**Why**: Three v3 pilot orgs (fsf, jyc, ril) showed 0% fill rate because `portal_order_items.quantity_invoiced` is never populated — not because orders aren't being fulfilled. The brief incorrectly presented this as critical fulfillment failure.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT
  COUNT(*) AS total_order_items,
  COUNT(CASE WHEN quantity_invoiced > 0 THEN 1 END) AS has_invoiced_qty,
  ROUND(100.0 * COUNT(CASE WHEN quantity_invoiced > 0 THEN 1 END) / NULLIF(COUNT(*), 0), 1) AS pct_populated
FROM portal_order_items poi
JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
WHERE poi.organization_id = {{ORG_ID}}
  AND po.order_date >= NOW() - INTERVAL '12 months'
```

**Rule**: `true` if `pct_populated >= 50.0`.

**Rationale for 50% threshold**: Orgs that genuinely track invoice quantities typically populate >90%. Orgs that don't populate are at 0%. The 50% threshold cleanly separates the two populations. If an org is between 10–50%, partial fill rate data is unreliable and should be suppressed.

---

### G-11: `HAS_NEW_ITEMS` (v4, audit finding — §5 empty section)

**Effect when false**: §5 New Introduction Adoption section is **skipped entirely** — no "No new items flagged (count: 0)" placeholder.

**Why**: v3 pilot showed orgs with zero `new_item=true` products rendering an empty "No new items" section that adds no intelligence.

**MCP**: `user-supercat-postgres-vpn`

```sql
SELECT COUNT(*) AS new_item_count
FROM products
WHERE organization_id = {{ORG_ID}}
  AND new_item = true
  AND deleted = false
```

**Rule**: `true` if `new_item_count > 0`.

---

## Gate Summary Table

| Gate | Query Target | Threshold | Sections Affected |
|------|-------------|-----------|-------------------|
| `TOTAL_BUSINESS_PROVENANCE` (**G-00, run first**) | `portal_invoices` + `portal_orders` + `orders` | resolves source/confidence/completeness/clamp | **Every Total** — CQ-01, CQ-10, CQ-22, CQ-23, §1/§2 header, health score, competitive-loss banner, revenue-at-risk |
| `HAS_PORTAL_INVOICES` | `portal_invoice_items` | count > 0 | CQ-02, CQ-03, CQ-04, CQ-05, CQ-06, CQ-09, CQ-11, CQ-15, CQ-19, CQ-20 |
| `HAS_COMMITMENT_REPORTS` | `commitment_reports` | count > 0 | CQ-17 |
| `HAS_PLACEMENT_REPORTS` | `placement_reports` | count > 0 | CQ-18 |
| `HAS_MIXPANEL_CUSTOMER` | BigQuery `mixpanel.events` | count > 0 with `selected_bill_to_code` | CQ-13 |
| `HAS_ECAT_ORDERS` | `orders` | count > 0 submitted in LTM | CQ-01 eCat portion |
| `HAS_RMA` | `rma_requests` via `org_users` | count > 0 | CQ-16 |
| `HAS_BUYER_NAMES` | `portal_orders` | buyer_name > 5% populated | CQ-14 |
| `COLLECTION_COVERAGE` | `products` | collection_code >= 50% | CQ-04 standalone vs. folded |
| `HAS_SHIP_TO_DATA` | `portal_orders` | ship_to_number > 10% populated | CQ-21 |
| `FILL_RATE_POPULATION` | `portal_order_items` | quantity_invoiced >= 50% populated | CQ-15, §20, H6 health signal |
| `HAS_NEW_ITEMS` | `products` | new_item count > 0 | §5 New Introduction Adoption |

---

## Customer-Level Volume Gates

These are checked per-customer, not per-org:

### V-01: `CQ06_VOLUME_SAFE` (v4, audit finding §4 — relaxed threshold + recent-window strategy)

**Effect when false**: CQ-06 (Next Best Product) runs in **recent-window mode** instead of skipping entirely.

**Tiered approach** (v4):

| Customer LTM Orders | Strategy | Notes |
|---------------------|----------|-------|
| ≤ 5,000 | Run CQ-06 as-is (full LTM) | Works fine, typical <5s |
| 5,001–50,000 | Run CQ-06 **recent-window variant** (most recent 6 months of invoices only) | Reduces self-join cardinality by ~50%. Substitute `AND pi.invoice_date >= NOW() - INTERVAL '6 months'` in the `sequence_pairs` CTE's `a_pi` and `b_pi` joins. |
| > 50,000 | **Skip CQ-06** — render: *"Purchase sequence analysis unavailable for ultra-high-volume accounts (>[X]K orders)."* | True warehouse/distribution accounts where item-level co-purchase patterns are noise. |

**Why the change**: The v3 pilot selected large accounts (Wayfair, Lamps Plus, NFM) that all exceeded the 10K threshold, making the "highest wow-factor" advanced insight unreachable for the most important accounts. The 6-month window approach keeps the self-join manageable while still capturing meaningful purchase patterns.

**Evidence**: Original timeout at 30s on Savoy House 71200 (83K orders). The 6-month window reduces the working set to ~40K orders for a customer like 71200, which is feasible. True skip reserved for >50K where even windowed analysis is too costly.

---

## Caching

Gate queries target org-level aggregates, not customer-specific data. Results can be cached for the duration of a brief-building session (typically one run). Re-run gates if the session spans more than 24 hours or if a data import is known to have occurred.

---

## Data Richness Score

Count the number of `true` gates **G-01..G-11** to produce a data richness score (0–11). **G-00 is excluded
from the richness count** — it is the always-run provenance preflight that sets the confidence ceiling, not a
section-availability gate. (A rich org with `feed_completeness = PROVABLY INCOMPLETE` still suppresses its
Totals — richness predicts *section coverage*, G-00 governs *dollar trustworthiness*.) This predicts brief quality:

| Score | Label | Expected Brief Quality |
|-------|-------|----------------------|
| 8–11 | **Rich** | Full brief with all conditional sections rendering. Best candidate for pilot/demo. |
| 5–7 | **Standard** | Core sections strong, some conditional sections skip. Typical production brief. |
| 2–4 | **Lean** | Orders-only mode likely. Brief is narrower but still valuable for wallet share, trajectory, rhythm. |
| 0–1 | **Insufficient** | No invoice-level data and no orders. Cannot produce a meaningful brief. |
