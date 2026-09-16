# Customer Intelligence — Query Library

> **Status**: Production v4 — updated 2026-06-16 (CQ-06R added, CQ-19 cohort tiers)
> **Date**: 2026-06-16
> **Queries**: CQ-01 through CQ-26 (26 total)
> **Parameters**: Every query takes `{{ORG_ID}}` (integer) + `{{CUSTOMER_CODE}}` (varchar, = `customers.code` = `portal_orders.customer_bill_to_number`)
> **MCP targets**: `user-supercat-postgres-vpn` for Postgres; `user-bigquery-admin` for BigQuery (`sql` param, bound with `LIMIT`)

---

## Schema Notes — Production Gotchas

These were discovered during prototype validation against live data. Future query authors: read before writing.

| # | Gotcha | Wrong | Right |
|---|--------|-------|-------|
| 1 | **`taxonomies` type column** | `t.taxonomy_type = 'Category'` | `t.type = 'Category'` (or `'Collection'`). The column is `type`, not `taxonomy_type`. |
| 2 | **Mixpanel `time` column** | `time >= TIMESTAMP_SUB(...)` | `TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(...)`. The `time` column is `FLOAT64` epoch seconds, not a `TIMESTAMP`. |
| 3 | **`rma_requests` has no `organization_id`** | `WHERE r.organization_id = {{ORG_ID}}` | `JOIN org_users ou ON ou.id = r.org_user_id WHERE ou.organization_id = {{ORG_ID}}`. Must route through `org_users` to filter by org. |
| 4 | **`commitment_reports.items` / `placement_reports.items` are `jsonb`** | `LENGTH(items)` for item count | `jsonb_array_length(items)`. The column stores a JSON array, not a text string. |
| 5 | **Postgres date subtraction** | `EXTRACT(EPOCH FROM (MAX(d) - MIN(d))) / 86400` | `(MAX(d) - MIN(d))::numeric`. Direct date subtraction in Postgres yields an integer interval in days. |
| 6 | **`portal_orders` framing** | "total ERP business," "portal ordering," or "self-service" | **Booked order intent** — all-channel order headers synced from ERP, *not* the client's total. **Invoiced `net_amount` is the canonical total** (see Provenance Anchor). Never frame as portal-specific; `order_origin` distinguishes channel when populated. |
| 7 | **`invoice_date` is `date`, not `timestamp`** | `EXTRACT(DAY FROM invoice_date - prev_date)` | `(invoice_date - prev_date)` directly. Date minus date in Postgres yields an integer (days), not an interval. `EXTRACT` fails on integers. |
| 8 | **`placement_reports.items` / `commitment_reports.items` may be `text`** | `jsonb_array_length(items)` directly | `jsonb_array_length(items::jsonb)`. Some orgs store `items` as text-encoded JSON, not native jsonb. Always cast to be safe. |
| 9 | **`EXTRACT(MONTH FROM AGE(...))` returns component only** | `EXTRACT(MONTH FROM AGE(NOW(), date))` for total months | `EXTRACT(YEAR FROM AGE(NOW(), date)) * 12 + EXTRACT(MONTH FROM AGE(NOW(), date))`. `EXTRACT(MONTH ...)` returns 0-11, not total months elapsed. |
| 10 | **Ghost SKUs** | Assuming all invoice items exist in `products` | Some invoiced items have no matching product record (ERP item codes don't match eCat catalog). CQ-03 will show NULL description/collection. Flag but don't fail. |
| 11 | **`order_origin` may be blank** | Expecting channel classification | Some orgs never populate `order_origin` in their `order_data.csv`. CQ-12 will show 100% "Unknown." Render but note: *"Channel data not available for this client."* |
| 12 | **Collateral/sample accounts** | All accounts have real revenue | Some accounts only receive $0 catalogs, binders, and samples. CQ-23 may classify these as "Growing" ($0→$15). Check if `avg_unit_price = 0` or all items < $1 to detect. |

---

## Global Guardrails

### Orders table
```sql
AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
```

### NOT IN guard
```sql
AND customer_num IS NOT NULL
```

### portal_orders framing
`portal_orders` = ERP-synced **booked** order headers across all channels. Never "portal ordering" or "buyer self-service." **Booked ≠ invoiced** — see the Provenance Anchor below; `portal_orders.total_amount` is *booked* GMV, not the client's invoiced total business.

---

## Provenance Anchor (v5 — Layer-3 re-anchor on the invoiced spine)

> **Status**: v5 — 2026-06-29. Re-anchors every "total business" dollar in this library onto the **invoiced
> spine**, consuming the Layer-1 provenance mechanism (`provenance_spine.md` §1, §5, §6.1–§6.8). This is the
> D1 fix from `selling_customer_NORTHSTAR_MVP_reconciliation_handoff.md` §5 (item 3–4). The Layer-1
> mechanism is **locked/read-only** here — the CI brief *inherits* it, it does not redefine it.

### The canonical total (the one rule everything inherits)

> **Total business = `SUM(portal_invoices.net_amount)`** over a window clamped to `report_through_date`
> (Spine §1, §6.4). `net_amount` is the client-facing invoiced total and is **negative for credit memos**
> (returns net out). `portal_orders.total_amount` (booked headers) is **intent, off 4×–9× from invoiced** —
> it is a *labeled fallback*, never the headline when an invoice feed exists.

### G-00 — Provenance preflight (run once per org, before any other query)

The brief runs **G-00** (see `customer_gate_rules.md`) before CQ-01..CQ-26. It consumes the Layer-1
`Q-PROV-00`/`Q-ECON-00` contract and resolves, per org:

| Output | Values | Drives |
|---|---|---|
| `TOTAL_BUSINESS_SOURCE` | `INVOICES` → `ORDERS` → `SALES_DATA` → `NONE` | which dollar source every Total reads |
| `COMMERCE_CONFIDENCE` | `STRONG` / `PARTIAL` / `LIMITED` / `NONE` (**`FULL` unreachable on a single feed**) | the confidence ceiling every Total inherits |
| `FEED_COMPLETENESS` | `CORROBORATED` / `UNVERIFIED — SINGLE FEED` / `PROVABLY INCOMPLETE` / `STALE` / `DEAD` | the completeness word printed on every Total |
| `report_through_date` | `LEAST(MAX(invoice_date), CURRENT_DATE)` | the clamp on every LTM/prior window (defuses bad-date invoices, e.g. clm 4107 / jyc 2032) |
| `ecat_capture_ratio` | eCat-SALE GMV ÷ invoiced net (LTM) | the >1.05 trip that forces `PROVABLY INCOMPLETE` |

### The three binding rules (Spine §4, §5.3, §6.3 — applied to every Total in this library)

1. **Source swap.** A dollar column that means *total business* reads invoiced `net_amount` when
   `TOTAL_BUSINESS_SOURCE = INVOICES`; falls back to booked `portal_orders.total_amount` **labeled
   "booked orders (no invoice feed)"** only when `= ORDERS`; reports magnitude-only on `SALES_DATA`; and is
   **suppressed** on `NONE`.
2. **Label every Total.** Every total/denominator prints its `FEED_COMPLETENESS` word + `COMMERCE_CONFIDENCE`
   tier. **Suppress totals entirely on `PROVABLY INCOMPLETE` / `DEAD`** (do not call any number "total
   business"); report ranges/directional on `PARTIAL`/`STALE`. A composite never exceeds its lowest input's
   confidence (§5.3).
3. **Capture is a fact, attribution is gated.** eCat penetration is **capture vs invoiced** and is **never
   surfaced > 100%** as a headline (cap the display at 100% and footnote the raw ratio; a raw ratio > 105% is
   itself the `PROVABLY INCOMPLETE` signal). A capture *rate* is only valid at `FEED_COMPLETENESS =
   CORROBORATED` and `COMMERCE_CONFIDENCE ≥ STRONG`; otherwise report eCat capture in **absolute dollars only**.

### Re-anchor status by query (dollar columns)

| Query | Dollar column(s) | Re-anchor |
|---|---|---|
| **CQ-01** Account Snapshot | total business LTM/prior, YoY, eCat penetration | ✅ **rewritten below** — invoiced net + booked fallback + clamp + source/capture fields |
| **CQ-10** Spend Trajectory | quarterly revenue, AOV | ✅ **rewritten below** — invoiced net by invoice quarter |
| **CQ-22** Wallet Share | customer revenue, cohort avg/max | ✅ **rewritten below** — invoiced net (customer + cohort) |
| **CQ-23** Lifecycle | ltm_revenue, prior_revenue, cohort forecasting | ✅ **rewritten below** — revenue sums = invoiced net clamped to `report_through_date`; tenure/first_order stay on booked orders; booked variant is the labeled `ORDERS` fallback |
| **CQ-07** Frequency | `total_revenue` | 🔁 cadence (orders/months/days) stays on `portal_orders`; the **`total_revenue` dollar** uses invoiced net or is labeled "booked"; see CQ-07 note |
| **CQ-08** Seasonality | monthly revenue | 🔁 revenue uses invoiced net by `invoice_date`; cadence/timing may stay booked; see CQ-08 note |
| **CQ-12** Channel Mix | revenue by channel | ⚠ **stays on `portal_orders`** (only the booked feed carries `order_origin`); label the $ "booked," gate the split on `Q-CHAN-00`, never present as total business |
| **CQ-14** Buyer Intel | revenue by buyer | ⚠ **stays on `portal_orders`** (`buyer_name` is a booked-order field); label the $ "booked share," not invoiced total |
| **CQ-21** Same-Store | revenue by ship-to | ⚠ **stays on `portal_orders`** (ship-to grain); label the $ "booked by location," not invoiced total |
| CQ-02–06, 09, 11, 19, 20, 25, 26 | item/category revenue | ✅ already invoiced (`portal_invoice_items`) — no change |

⚠ rows are correct on booked orders **for grain reasons** (channel/buyer/ship-to live only on `portal_orders`),
but their dollars are **booked**, must be labeled as such, and must never be summed into or presented as the
invoiced total business.

---

## CQ-01: Account Snapshot

**Section**: Account at a Glance | **Source**: Postgres
**Provenance** (v5): Total business is now **invoiced `net_amount`** (Spine §1), windowed to
`report_through_date`, with booked `portal_orders` retained only as a labeled fallback/triangulation signal.
The brief stamps `COMMERCE_CONFIDENCE` + `FEED_COMPLETENESS` from **G-00** on every Total this query feeds
(§1 header, §2 glance, H1 health signal, the competitive-loss banner). `total_business_source = INVOICES`
when the org has an invoice feed, else `ORDERS` (booked, labeled). eCat penetration is **capture**, capped at
100% for display; a raw capture ratio > 105% is the `PROVABLY INCOMPLETE` trip (suppress the Total).

```sql
WITH provenance AS (
  -- Mirrors the Layer-1 Q-PROV-00 / Q-ECON-00 contract (Spine §6.1/§6.8). report_through_date is clamped to
  -- CURRENT_DATE so bad-date invoices (clm 4107, jyc 2032) can't anchor the window on a fantasy date.
  SELECT
    LEAST(MAX(invoice_date), CURRENT_DATE) AS report_through_date,
    (COUNT(*) > 0) AS has_invoice_feed
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND net_amount IS NOT NULL
),
ecat_ltm AS (
  SELECT
    COUNT(*) AS ecat_orders,
    ROUND(SUM(o.total)::numeric, 2) AS ecat_gmv,
    ROUND(AVG(o.total)::numeric, 2) AS ecat_aov,
    MAX(o.created_at) AS last_ecat_order
  FROM orders o, provenance pv
  WHERE o.organization_id = {{ORG_ID}}
    AND o.customer_num = '{{CUSTOMER_CODE}}'
    AND o.is_submitted = true
    AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
    -- eCat-SALE filter (Spine §6.5): exclude quotes/holds/tests from the capture numerator
    AND COALESCE(NULLIF(TRIM(o.order_type), ''), 'Confirmed') NOT IN
        ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND o.order_type NOT ILIKE 'HFC%' AND o.order_type NOT ILIKE 'Hold%' AND o.order_type NOT ILIKE 'TEST%'
    AND o.created_at >  pv.report_through_date - INTERVAL '12 months'
    AND o.created_at <= pv.report_through_date + INTERVAL '1 day'
),
ecat_prior AS (
  SELECT
    COUNT(*) AS ecat_orders,
    ROUND(SUM(o.total)::numeric, 2) AS ecat_gmv
  FROM orders o, provenance pv
  WHERE o.organization_id = {{ORG_ID}}
    AND o.customer_num = '{{CUSTOMER_CODE}}'
    AND o.is_submitted = true
    AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
    AND COALESCE(NULLIF(TRIM(o.order_type), ''), 'Confirmed') NOT IN
        ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND o.order_type NOT ILIKE 'HFC%' AND o.order_type NOT ILIKE 'Hold%' AND o.order_type NOT ILIKE 'TEST%'
    AND o.created_at >  pv.report_through_date - INTERVAL '24 months'
    AND o.created_at <= pv.report_through_date - INTERVAL '12 months'
),
invoiced_ltm AS (
  SELECT
    COUNT(DISTINCT pi.invoice_number) AS total_invoices,
    ROUND(SUM(pi.net_amount)::numeric, 2) AS invoiced_net
  FROM portal_invoices pi, provenance pv
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >  pv.report_through_date - INTERVAL '12 months'
    AND pi.invoice_date <= pv.report_through_date
),
invoiced_prior AS (
  SELECT ROUND(SUM(pi.net_amount)::numeric, 2) AS invoiced_net
  FROM portal_invoices pi, provenance pv
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >  pv.report_through_date - INTERVAL '24 months'
    AND pi.invoice_date <= pv.report_through_date - INTERVAL '12 months'
),
booked_ltm AS (
  SELECT
    COUNT(*) AS booked_orders,
    ROUND(SUM(po.total_amount)::numeric, 2) AS booked_gmv,
    MAX(po.order_date) AS last_order
  FROM portal_orders po, provenance pv
  WHERE po.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND po.order_date >  pv.report_through_date - INTERVAL '12 months'
    AND po.order_date <= pv.report_through_date
),
booked_prior AS (
  SELECT ROUND(SUM(po.total_amount)::numeric, 2) AS booked_gmv
  FROM portal_orders po, provenance pv
  WHERE po.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND po.order_date >  pv.report_through_date - INTERVAL '24 months'
    AND po.order_date <= pv.report_through_date - INTERVAL '12 months'
),
customer_info AS (
  SELECT
    c.name,
    c.billing_city,
    c.billing_state,
    c.default_price_code,
    c.terms,
    c.territory_codes,
    (SELECT COUNT(*) FROM shipping_locations WHERE customer_id = c.id) AS ship_to_count
  FROM customers c
  WHERE c.organization_id = {{ORG_ID}}
    AND c.code = '{{CUSTOMER_CODE}}'
),
base AS (
  SELECT
    ci.name, ci.billing_city, ci.billing_state, ci.default_price_code, ci.terms,
    ci.territory_codes, ci.ship_to_count,
    pv.report_through_date, pv.has_invoice_feed,
    CASE WHEN pv.has_invoice_feed THEN 'INVOICES' ELSE 'ORDERS' END AS total_business_source,
    -- canonical total business (invoiced net when a feed exists; else booked, labeled by the renderer)
    CASE WHEN pv.has_invoice_feed THEN il.invoiced_net ELSE bl.booked_gmv END AS total_business_ltm,
    CASE WHEN pv.has_invoice_feed THEN ip.invoiced_net ELSE bp.booked_gmv END AS total_business_prior,
    -- transaction counts: invoices when invoiced, else booked orders
    CASE WHEN pv.has_invoice_feed THEN il.total_invoices ELSE bl.booked_orders END AS total_txn_ltm,
    -- always exposed for triangulation / completeness gate
    il.invoiced_net AS invoiced_net_ltm, ip.invoiced_net AS invoiced_net_prior, il.total_invoices,
    bl.booked_gmv AS booked_gmv_ltm, bp.booked_gmv AS booked_gmv_prior, bl.booked_orders, bl.last_order,
    el.ecat_orders AS ecat_orders_ltm, el.ecat_gmv AS ecat_gmv_ltm, el.ecat_aov, el.last_ecat_order,
    ep.ecat_orders AS ecat_orders_prior, ep.ecat_gmv AS ecat_gmv_prior
  FROM customer_info ci, provenance pv,
       invoiced_ltm il, invoiced_prior ip, booked_ltm bl, booked_prior bp, ecat_ltm el, ecat_prior ep
)
SELECT
  b.*,
  -- YoY on the canonical (invoiced) total business
  CASE WHEN b.total_business_prior > 0
    THEN ROUND(100.0 * (b.total_business_ltm - b.total_business_prior) / b.total_business_prior, 1)
    END AS total_business_yoy_pct,
  CASE WHEN b.ecat_gmv_prior > 0
    THEN ROUND(100.0 * (b.ecat_gmv_ltm - b.ecat_gmv_prior) / b.ecat_gmv_prior, 1)
    END AS ecat_yoy_pct,
  -- eCat CAPTURE vs invoiced: raw (drives the PROVABLY-INCOMPLETE trip) + display (capped at 100%, §6.3 capture-vs-attribution)
  CASE WHEN b.has_invoice_feed AND b.invoiced_net_ltm > 0
    THEN ROUND(100.0 * b.ecat_gmv_ltm / b.invoiced_net_ltm, 1) END AS ecat_capture_pct_raw,
  CASE WHEN b.has_invoice_feed AND b.invoiced_net_ltm > 0
    THEN LEAST(ROUND(100.0 * b.ecat_gmv_ltm / b.invoiced_net_ltm, 1), 100.0) END AS ecat_capture_pct_display,
  -- back-compat alias for H4 (health score) — capped capture
  CASE WHEN b.has_invoice_feed AND b.invoiced_net_ltm > 0
    THEN LEAST(ROUND(100.0 * b.ecat_gmv_ltm / b.invoiced_net_ltm, 1), 100.0) END AS ecat_penetration_pct,
  -- booked-vs-invoiced ratio: the completeness triangulation signal (Spine §6.3); ~1.0 supports CORROBORATED
  CASE WHEN b.invoiced_net_ltm > 0
    THEN ROUND(b.booked_gmv_ltm / b.invoiced_net_ltm, 2) END AS booked_over_invoiced,
  (b.report_through_date - COALESCE(b.last_order, b.last_ecat_order::date))::int AS days_since_last_order
FROM base b
```

**Renderer contract** (what changed for downstream sections):
- `total_business_ltm` / `total_business_prior` / `total_business_yoy_pct` are the **canonical invoiced** numbers — use these for §1, §2, H1, and the competitive-loss banner. The legacy `total_gmv_*` names are gone; do not resurrect booked GMV as "total business."
- Always print the Total with its `FEED_COMPLETENESS` + `COMMERCE_CONFIDENCE` (from G-00). If G-00 returns `PROVABLY INCOMPLETE` or `DEAD`, **suppress the Total** and show eCat capture in absolute dollars only.
- Surface `ecat_capture_pct_display` (≤100%); footnote `ecat_capture_pct_raw` only as the incompleteness signal — never headline a capture > 100%.
- `booked_over_invoiced` and `ecat_capture_pct_raw` feed G-00's completeness triangulation; they are diagnostics, not client headlines.

---

## CQ-02: Category Breakdown

**Section**: Purchase DNA — Categories | **Source**: Postgres

```sql
WITH ltm AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue,
    SUM(pii.quantity_invoiced)::int AS units
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
  GROUP BY COALESCE(t.name, p.category_code, 'Uncategorized')
),
prior AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date BETWEEN NOW() - INTERVAL '24 months' AND NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
  GROUP BY COALESCE(t.name, p.category_code, 'Uncategorized')
),
total AS (SELECT SUM(revenue) AS total_rev FROM ltm)
SELECT
  l.category,
  l.revenue,
  ROUND(100.0 * l.revenue / NULLIF(tt.total_rev, 0), 1) AS pct_of_spend,
  l.units,
  CASE WHEN pr.revenue > 0
    THEN ROUND(100.0 * (l.revenue - pr.revenue) / pr.revenue, 1)
    ELSE NULL END AS yoy_change_pct,
  CASE WHEN pr.revenue IS NULL AND l.revenue > 0 THEN true ELSE false END AS is_new_category
FROM ltm l
LEFT JOIN prior pr ON pr.category = l.category
CROSS JOIN total tt
ORDER BY l.revenue DESC
LIMIT 15
```

---

## CQ-03: Top SKUs with Inventory Status

**Section**: Purchase DNA — Top Items | **Source**: Postgres

```sql
SELECT
  pii.item_number,
  p.long_description AS description,
  COALESCE(t.name, p.collection_code) AS collection,
  SUM(pii.quantity_invoiced)::int AS units,
  ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue,
  COALESCE(i.qty_available, 0) AS qty_available,
  COALESCE(i.qty_on_hand, 0) AS qty_on_hand,
  COALESCE(i.qty_on_backorder, 0) AS qty_on_backorder,
  i.next_scheduled_receipt_date
FROM portal_invoice_items pii
JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
LEFT JOIN taxonomies t ON t.code = p.collection_code AND t.organization_id = p.organization_id AND t.type = 'Collection'
LEFT JOIN inventories i ON i.base_item_code = pii.item_number AND i.organization_id = pii.organization_id
WHERE pii.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND pi.invoice_date >= NOW() - INTERVAL '12 months'
  AND pii.quantity_invoiced > 0
GROUP BY pii.item_number, p.long_description, COALESCE(t.name, p.collection_code),
         i.qty_available, i.qty_on_hand, i.qty_on_backorder, i.next_scheduled_receipt_date
ORDER BY revenue DESC
LIMIT 15
```

---

## CQ-04: Collection Mix

**Section**: Purchase DNA — Collections | **Source**: Postgres

```sql
SELECT
  COALESCE(t.name, p.collection_code, 'Uncategorized') AS collection,
  ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue,
  ROUND(100.0 * SUM(pii.unit_price * pii.quantity_invoiced) /
    NULLIF(SUM(SUM(pii.unit_price * pii.quantity_invoiced)) OVER(), 0), 1) AS pct_of_spend
FROM portal_invoice_items pii
JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
LEFT JOIN taxonomies t ON t.code = p.collection_code AND t.organization_id = p.organization_id AND t.type = 'Collection'
WHERE pii.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND pi.invoice_date >= NOW() - INTERVAL '12 months'
  AND pii.quantity_invoiced > 0
GROUP BY COALESCE(t.name, p.collection_code, 'Uncategorized')
ORDER BY revenue DESC
LIMIT 10
```

---

## CQ-05: New Introduction Adoption

**Section**: Purchase DNA — New Intros | **Source**: Postgres

```sql
WITH org_new_items AS (
  SELECT item_number FROM products
  WHERE organization_id = {{ORG_ID}} AND new_item = true AND deleted = false
),
customer_purchased AS (
  SELECT DISTINCT pii.item_number
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pii.item_number IN (SELECT item_number FROM org_new_items)
    AND pii.quantity_invoiced > 0
),
cohort_avg AS (
  SELECT
    ROUND(AVG(cnt)::numeric, 1) AS avg_new_items_purchased
  FROM (
    SELECT pi.customer_bill_to_number, COUNT(DISTINCT pii.item_number) AS cnt
    FROM portal_invoice_items pii
    JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
    WHERE pii.organization_id = {{ORG_ID}}
      AND pii.item_number IN (SELECT item_number FROM org_new_items)
      AND pii.quantity_invoiced > 0
      AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    GROUP BY pi.customer_bill_to_number
    HAVING COUNT(DISTINCT pii.item_number) > 0
  ) sub
)
SELECT
  (SELECT COUNT(*) FROM org_new_items) AS total_new_items,
  (SELECT COUNT(*) FROM customer_purchased) AS customer_purchased_count,
  (SELECT avg_new_items_purchased FROM cohort_avg) AS cohort_avg_new_items
```

**Step 2 — Top new intros this customer HASN'T purchased (bought by similar customers):**

```sql
WITH customer_state AS (
  SELECT billing_state FROM customers
  WHERE organization_id = {{ORG_ID}} AND code = '{{CUSTOMER_CODE}}'
),
similar_customers AS (
  SELECT DISTINCT pi.customer_bill_to_number
  FROM portal_invoices pi
  JOIN customers c ON c.code = pi.customer_bill_to_number AND c.organization_id = pi.organization_id
  WHERE pi.organization_id = {{ORG_ID}}
    AND c.billing_state = (SELECT billing_state FROM customer_state)
    AND pi.customer_bill_to_number != '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
),
customer_items AS (
  SELECT DISTINCT pii.item_number
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
)
SELECT
  pii.item_number,
  p.long_description AS description,
  COALESCE(t.name, p.collection_code) AS collection,
  COUNT(DISTINCT pi.customer_bill_to_number) AS similar_customers_bought,
  SUM(pii.quantity_invoiced)::int AS total_units_across_similar
FROM portal_invoice_items pii
JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false AND p.new_item = true
LEFT JOIN taxonomies t ON t.code = p.collection_code AND t.organization_id = p.organization_id AND t.type = 'Collection'
WHERE pii.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number IN (SELECT customer_bill_to_number FROM similar_customers)
  AND pii.item_number NOT IN (SELECT item_number FROM customer_items)
  AND pii.quantity_invoiced > 0
  AND pi.invoice_date >= NOW() - INTERVAL '12 months'
GROUP BY pii.item_number, p.long_description, COALESCE(t.name, p.collection_code)
ORDER BY similar_customers_bought DESC, total_units_across_similar DESC
LIMIT 5
```

---

## CQ-06: Next Best Product (Purchase Sequence)

**Section**: Purchase DNA — Predictions | **Source**: Postgres
**Volume gate** (v4 — tiered, audit finding §4): Tiered by customer LTM order count:
- ≤ 5,000: Run full query below as-is
- 5,001–50,000: Run **CQ-06R** (recent-window variant, see below) — restricts `sequence_pairs` to 6-month invoice window
- > 50,000: Skip entirely (ultra-high-volume accounts)

For each of this customer's top 5 items, find what other customers commonly purchase next within 90 days. Uses a simplified version (validated against Baer's — 52-customer signal on Weekender Dresser → Long Key King Bed):

```sql
WITH customer_top_items AS (
  SELECT pii.item_number, SUM(pii.quantity_invoiced) AS qty
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pii.quantity_invoiced > 0
  GROUP BY pii.item_number
  ORDER BY qty DESC
  LIMIT 5
),
customer_all_items AS (
  SELECT DISTINCT pii.item_number
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
),
sequence_pairs AS (
  SELECT
    a_pii.item_number AS anchor_item,
    b_pii.item_number AS next_item,
    COUNT(DISTINCT a_pi.customer_bill_to_number) AS customer_count
  FROM portal_invoice_items a_pii
  JOIN portal_invoices a_pi ON a_pi.invoice_number = a_pii.invoice_number AND a_pi.organization_id = a_pii.organization_id
  JOIN portal_invoices b_pi ON b_pi.customer_bill_to_number = a_pi.customer_bill_to_number
    AND b_pi.organization_id = a_pi.organization_id
    AND b_pi.invoice_date BETWEEN a_pi.invoice_date AND a_pi.invoice_date + INTERVAL '90 days'
    AND b_pi.invoice_number != a_pi.invoice_number
  JOIN portal_invoice_items b_pii ON b_pii.invoice_number = b_pi.invoice_number AND b_pii.organization_id = b_pi.organization_id
  WHERE a_pii.organization_id = {{ORG_ID}}
    AND a_pii.item_number IN (SELECT item_number FROM customer_top_items)
    AND b_pii.item_number != a_pii.item_number
    AND b_pii.item_number NOT IN (SELECT item_number FROM customer_all_items)
    AND a_pii.quantity_invoiced > 0
    AND b_pii.quantity_invoiced > 0
  GROUP BY a_pii.item_number, b_pii.item_number
  HAVING COUNT(DISTINCT a_pi.customer_bill_to_number) >= 3
)
SELECT
  sp.anchor_item,
  pa.long_description AS anchor_description,
  sp.next_item,
  pn.long_description AS next_description,
  sp.customer_count
FROM sequence_pairs sp
LEFT JOIN products pa ON pa.item_number = sp.anchor_item AND pa.organization_id = {{ORG_ID}} AND pa.deleted = false
LEFT JOIN products pn ON pn.item_number = sp.next_item AND pn.organization_id = {{ORG_ID}} AND pn.deleted = false
ORDER BY sp.customer_count DESC
LIMIT 10
```

### CQ-06R: Recent-Window Variant (v4)

For customers with 5,001–50,000 LTM orders. Identical to CQ-06 except the `sequence_pairs` CTE restricts both sides of the self-join to the most recent 6 months:

Replace the `sequence_pairs` CTE's WHERE clause with:
```sql
  WHERE a_pii.organization_id = {{ORG_ID}}
    AND a_pii.item_number IN (SELECT item_number FROM customer_top_items)
    AND b_pii.item_number != a_pii.item_number
    AND b_pii.item_number NOT IN (SELECT item_number FROM customer_all_items)
    AND a_pii.quantity_invoiced > 0
    AND b_pii.quantity_invoiced > 0
    AND a_pi.invoice_date >= NOW() - INTERVAL '6 months'
    AND b_pi.invoice_date >= NOW() - INTERVAL '6 months'
```

All other CTEs remain unchanged. When rendering, add note: *"Based on most recent 6 months of purchase patterns."*

---

## CQ-07: Order Frequency Metrics

**Section**: Buying Rhythm — Frequency | **Source**: Postgres
**Provenance** (v5): order **cadence** (count, active months, days-between) legitimately stays on
`portal_orders` — rhythm is about *when* orders are placed. But the `total_revenue` dollar column is **booked**
and must be labeled "booked" (or replaced with invoiced net per the Provenance Anchor); never present
`total_revenue` here as the customer's total business — that number comes from CQ-01.

**Step 1 — Customer frequency:**
```sql
SELECT
  COUNT(*) AS total_orders,
  ROUND(COUNT(*)::numeric / 12, 1) AS orders_per_month,
  COUNT(DISTINCT DATE_TRUNC('month', order_date)) AS active_months,
  CASE WHEN COUNT(*) > 1 THEN
    ROUND((MAX(order_date) - MIN(order_date))::numeric / NULLIF(COUNT(*) - 1, 0), 1)
  ELSE NULL END AS avg_days_between,
  ROUND(SUM(total_amount)::numeric, 2) AS total_revenue  -- BOOKED GMV — label "booked"; never present as total business (that's CQ-01 invoiced net)
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '12 months'
```

**Step 2 — Org-wide frequency stats and percentile rank:**

Substitute `{{CUSTOMER_ORDER_COUNT}}` with `total_orders` from Step 1:

```sql
SELECT
  COUNT(*) AS total_customers,
  ROUND(AVG(cust_orders)::numeric, 1) AS org_avg_orders,
  ROUND(AVG(cust_orders)::numeric / 12, 1) AS org_avg_orders_per_month,
  COUNT(CASE WHEN cust_orders <= {{CUSTOMER_ORDER_COUNT}} THEN 1 END) AS customers_at_or_below
FROM (
  SELECT customer_bill_to_number, COUNT(*) AS cust_orders
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
  GROUP BY customer_bill_to_number
) sub
```

Compute `percentile_rank = ROUND(100 * customers_at_or_below / total_customers)`. Display as "Top X%" where X = `100 - percentile_rank`.

Note: Uses org average instead of median (median requires `PERCENTILE_CONT` which some MCP validators reject). The average is slightly higher than the median for right-skewed order distributions, but the percentile rank is exact.

---

## CQ-08: Monthly Seasonality Pattern

**Section**: Buying Rhythm — Seasonality | **Source**: Postgres
**Provenance** (v5): the seasonality **shape** (which months are peaks/troughs) is valid on booked-order
cadence; but if the brief annotates monthly **dollars**, those must be invoiced `net_amount` by `invoice_date`
(swap `portal_orders`/`order_date`/`total_amount` → `portal_invoices`/`invoice_date`/`net_amount`, clamped to
`report_through_date`) when `TOTAL_BUSINESS_SOURCE = INVOICES`. Booked dollars must be labeled "booked."

```sql
SELECT
  DATE_TRUNC('month', order_date)::date AS month,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount)::numeric, 2) AS revenue  -- BOOKED GMV — label "booked"; swap to portal_invoices.net_amount by invoice_date (clamped to report_through_date) when surfacing dollars on INVOICES
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '24 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month
```

---

## CQ-09: Per-SKU Reorder Decay Detection

**Section**: Buying Rhythm — Decay Alerts | **Source**: Postgres
**Minimum interval threshold**: Only report items where `avg_interval >= 7` days. Sub-daily reorder cadences (e.g., 0.2 days for warehouse distribution accounts) produce false decay alerts when even a 1-day gap triggers "DECAY_DETECTED." Confirmed on Savoy House 71200 (Wayfair).

```sql
WITH item_orders AS (
  SELECT
    pii.item_number,
    pi.invoice_date,
    LAG(pi.invoice_date) OVER (PARTITION BY pii.item_number ORDER BY pi.invoice_date) AS prev_date
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pii.quantity_invoiced > 0
    AND pi.invoice_date >= NOW() - INTERVAL '24 months'
),
intervals AS (
  SELECT
    item_number,
    invoice_date,
    (invoice_date - prev_date) AS days_gap
  FROM item_orders
  WHERE prev_date IS NOT NULL
),
stats AS (
  SELECT
    item_number,
    COUNT(*) AS reorder_count,
    ROUND(AVG(days_gap)::numeric, 1) AS avg_interval,
    ROUND((ARRAY_AGG(days_gap ORDER BY invoice_date DESC))[1]::numeric, 1) AS latest_interval,
    ROUND((ARRAY_AGG(days_gap ORDER BY invoice_date DESC))[2]::numeric, 1) AS prev_interval,
    ROUND((ARRAY_AGG(days_gap ORDER BY invoice_date DESC))[3]::numeric, 1) AS prev2_interval
  FROM intervals
  GROUP BY item_number
  HAVING COUNT(*) >= 3
)
SELECT
  s.item_number,
  p.long_description AS description,
  s.reorder_count,
  s.avg_interval AS historical_avg_days,
  s.latest_interval,
  s.prev_interval,
  s.prev2_interval,
  CASE WHEN s.latest_interval > s.avg_interval * 1.5 THEN 'DECAY_DETECTED'
       WHEN s.latest_interval > s.avg_interval * 1.2 THEN 'SLOWING'
       ELSE 'ON_PACE' END AS status
FROM stats s
LEFT JOIN products p ON p.item_number = s.item_number AND p.organization_id = {{ORG_ID}} AND p.deleted = false
WHERE s.latest_interval > s.avg_interval * 1.2
  AND s.avg_interval >= 7
ORDER BY s.reorder_count DESC
LIMIT 10
```

---

## CQ-10: Spend Trajectory

**Section**: Money Profile — Trend | **Source**: Postgres
**Provenance** (v5): trajectory is **invoiced `net_amount`** by invoice quarter, clamped to
`report_through_date` (Provenance Anchor). When `TOTAL_BUSINESS_SOURCE = ORDERS` (no invoice feed), run the
booked fallback below and label the trend "booked orders." Carries the G-00 `COMMERCE_CONFIDENCE` /
`FEED_COMPLETENESS` label; on `PROVABLY INCOMPLETE`/`DEAD` the dollar trend is suppressed (show order *count*
cadence only).

```sql
WITH provenance AS (
  SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS report_through_date
  FROM portal_invoices WHERE organization_id = {{ORG_ID}} AND net_amount IS NOT NULL
)
SELECT
  DATE_TRUNC('quarter', pi.invoice_date)::date AS quarter,
  COUNT(DISTINCT pi.invoice_number) AS invoices,
  ROUND(SUM(pi.net_amount)::numeric, 2) AS revenue,
  ROUND((SUM(pi.net_amount) / NULLIF(COUNT(DISTINCT pi.invoice_number), 0))::numeric, 2) AS aov
FROM portal_invoices pi, provenance pv
WHERE pi.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND pi.invoice_date >  pv.report_through_date - INTERVAL '24 months'
  AND pi.invoice_date <= pv.report_through_date
GROUP BY DATE_TRUNC('quarter', pi.invoice_date)
ORDER BY quarter
```

**Booked fallback** (only when `TOTAL_BUSINESS_SOURCE = ORDERS`) — label every row "booked":
```sql
SELECT
  DATE_TRUNC('quarter', order_date)::date AS quarter,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount)::numeric, 2) AS booked_revenue,
  ROUND(AVG(total_amount)::numeric, 2) AS booked_aov
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '24 months'
GROUP BY DATE_TRUNC('quarter', order_date)
ORDER BY quarter
```

---

## CQ-11: Price & Discount Behavior

**Section**: Money Profile — Pricing | **Source**: Postgres

```sql
WITH customer_pricing AS (
  SELECT
    ROUND(AVG(pii.unit_price)::numeric, 2) AS avg_unit_price,
    SUM(pii.quantity_invoiced)::int AS total_units
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
    AND pii.unit_price > 0
),
org_pricing AS (
  SELECT ROUND(AVG(pii.unit_price)::numeric, 2) AS org_avg_unit_price
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
    AND pii.unit_price > 0
),
ecat_discounts AS (
  SELECT
    ROUND(AVG(CASE WHEN discount_percent > 0 THEN discount_percent ELSE 0 END)::numeric, 2) AS avg_discount_pct,
    ROUND(100.0 * COUNT(CASE WHEN discount_percent > 0 THEN 1 END)::numeric / NULLIF(COUNT(*), 0), 1) AS orders_with_discount_pct
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND customer_num = '{{CUSTOMER_CODE}}'
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at >= NOW() - INTERVAL '12 months'
),
price_trend AS (
  SELECT
    DATE_TRUNC('quarter', pi.invoice_date)::date AS quarter,
    ROUND(AVG(pii.unit_price)::numeric, 2) AS avg_unit_price
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '24 months'
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
  GROUP BY DATE_TRUNC('quarter', pi.invoice_date)
  ORDER BY quarter
)
SELECT
  cp.avg_unit_price, cp.total_units,
  op.org_avg_unit_price,
  ed.avg_discount_pct, ed.orders_with_discount_pct,
  (SELECT json_agg(json_build_object('quarter', quarter, 'avg_unit_price', avg_unit_price)) FROM price_trend) AS price_trend
FROM customer_pricing cp, org_pricing op, ecat_discounts ed
```

---

## CQ-12: Channel Mix

**Section**: Channel Mix | **Source**: Postgres

```sql
SELECT
  COALESCE(order_origin, 'Unknown') AS channel,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount)::numeric, 2) AS revenue,
  ROUND(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER(), 0), 1) AS pct_of_orders
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '12 months'
GROUP BY COALESCE(order_origin, 'Unknown')
ORDER BY revenue DESC
```

---

## CQ-13: Rep Engagement Profile

**Section**: Rep Engagement | **Source**: BigQuery Mixpanel

```sql
SELECT
  event_name,
  COUNT(*) AS event_count
FROM `supercat-data-pipeline.mixpanel.events`
WHERE current_organization_shortname = '{{ORG_SHORTNAME}}'
  AND selected_bill_to_code = '{{CUSTOMER_CODE}}'
  AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
GROUP BY event_name
ORDER BY event_count DESC
LIMIT 20
```

**Step 2 — Rep breakdown:**

```sql
SELECT
  username AS rep_name,
  COUNT(*) AS total_events,
  COUNT(CASE WHEN event_name = 'order_submitted' THEN 1 END) AS orders_submitted,
  COUNT(CASE WHEN event_name = 'product_search' THEN 1 END) AS product_searches,
  TIMESTAMP_SECONDS(CAST(MIN(time) AS INT64)) AS first_activity,
  TIMESTAMP_SECONDS(CAST(MAX(time) AS INT64)) AS last_activity
FROM `supercat-data-pipeline.mixpanel.events`
WHERE current_organization_shortname = '{{ORG_SHORTNAME}}'
  AND selected_bill_to_code = '{{CUSTOMER_CODE}}'
  AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
  AND username IS NOT NULL
GROUP BY username
ORDER BY total_events DESC
LIMIT 10
```

---

## CQ-14: Buyer-Within-Customer Intelligence

**Section**: Buyer Intelligence | **Source**: Postgres

```sql
SELECT
  COALESCE(buyer_name, 'Unknown') AS buyer,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount)::numeric, 2) AS revenue,
  ROUND(100.0 * SUM(total_amount) / NULLIF(SUM(SUM(total_amount)) OVER(), 0), 1) AS pct_of_revenue,
  MIN(order_date) AS first_order,
  MAX(order_date) AS last_order,
  CASE WHEN MIN(order_date) >= NOW() - INTERVAL '6 months' THEN true ELSE false END AS is_new_buyer
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '24 months'
GROUP BY COALESCE(buyer_name, 'Unknown')
ORDER BY revenue DESC
LIMIT 10
```

---

## CQ-15: Fulfillment / Fill Rate

**Section**: Fulfillment & Returns — Fill Rate | **Source**: Postgres

```sql
WITH fill AS (
  SELECT
    SUM(poi.quantity_ordered)::numeric AS total_ordered,
    SUM(poi.quantity_invoiced)::numeric AS total_invoiced,
    SUM(COALESCE(poi.quantity_backordered, 0))::numeric AS total_backordered,
    COUNT(DISTINCT poi.item_number) AS distinct_items
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND po.order_date >= NOW() - INTERVAL '12 months'
),
org_fill AS (
  SELECT
    ROUND(100.0 * SUM(poi.quantity_invoiced) / NULLIF(SUM(poi.quantity_ordered), 0), 1) AS org_fill_rate
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
    AND poi.quantity_ordered > 0
),
current_backorders AS (
  SELECT COUNT(DISTINCT poi.item_number) AS items_on_backorder
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND COALESCE(poi.quantity_backordered, 0) > 0
    AND po.order_date >= NOW() - INTERVAL '6 months'
)
SELECT
  f.total_ordered, f.total_invoiced, f.total_backordered, f.distinct_items,
  ROUND(100.0 * f.total_invoiced / NULLIF(f.total_ordered, 0), 1) AS fill_rate_pct,
  of.org_fill_rate,
  cb.items_on_backorder
FROM fill f, org_fill of, current_backorders cb
```

---

## CQ-16: Returns

**Section**: Fulfillment & Returns — Returns | **Source**: Postgres

```sql
SELECT
  r.code AS return_reason,
  COUNT(*) AS return_count,
  SUM(r.quantity)::int AS total_units_returned,
  r.item_number,
  MIN(r.created_at) AS earliest,
  MAX(r.created_at) AS latest
FROM rma_requests r
JOIN org_users ou ON ou.id = r.org_user_id
WHERE ou.organization_id = {{ORG_ID}}
  AND r.bill_to_code = '{{CUSTOMER_CODE}}'
  AND r.created_at >= NOW() - INTERVAL '24 months'
GROUP BY r.code, r.item_number
ORDER BY return_count DESC
```

---

## CQ-17: Market Commitments vs. Actuals

**Section**: Market Commitments | **Source**: Postgres
**Gate**: `commitment_reports` count > 0 for this customer

```sql
SELECT
  market_code,
  created_at AS commitment_date,
  jsonb_array_length(items::jsonb) AS item_count
FROM commitment_reports
WHERE organization_id = {{ORG_ID}}
  AND bill_to_code = '{{CUSTOMER_CODE}}'
ORDER BY created_at DESC
LIMIT 10
```

Note: `items` may be stored as text-encoded JSON in some orgs. Always cast with `items::jsonb`. Use `jsonb_array_length()` for counts. Cross-reference parsed item numbers against `portal_order_items` post-commitment-date to compute conversion rate.

---

## CQ-18: Placement / Showroom Status

**Section**: Showroom Placements | **Source**: Postgres
**Gate**: `placement_reports` count > 0 for this customer

```sql
SELECT
  showroom_location_code,
  ship_to_code,
  jsonb_array_length(items::jsonb) AS item_count,
  created_at,
  updated_at,
  EXTRACT(DAY FROM NOW() - updated_at)::int AS days_since_update
FROM placement_reports
WHERE organization_id = {{ORG_ID}}
  AND bill_to_code = '{{CUSTOMER_CODE}}'
ORDER BY updated_at DESC
```

---

## CQ-19: Cross-Sell Opportunity

**Section**: Cross-Sell | **Source**: Postgres

**v4 cohort strategy** (audit finding §5): Try cohort tiers in order. The query below shows the default (Tier 1: same state + revenue within 2x). For Tier 2, remove the revenue filter from the inner subquery. For Tier 3, remove both the `billing_state` filter and revenue filter. Stop at the first tier returning `cohort_size >= 5` in the `HAVING COUNT(*) >= 5` clause.

**Tier 1 query** (same state + within 2x LTM revenue — substitute `{{CUSTOMER_LTM_REVENUE}}` from CQ-01):

```sql
WITH customer_spend AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
  GROUP BY COALESCE(t.name, p.category_code, 'Uncategorized')
),
cohort_spend AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(AVG(cust_total)::numeric, 2) AS cohort_avg_revenue
  FROM (
    SELECT
      pi.customer_bill_to_number,
      COALESCE(t.name, p.category_code, 'Uncategorized') AS cat,
      SUM(pii.unit_price * pii.quantity_invoiced) AS cust_total
    FROM portal_invoice_items pii
    JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
    JOIN customers c ON c.code = pi.customer_bill_to_number AND c.organization_id = pi.organization_id
    LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
    LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
    WHERE pii.organization_id = {{ORG_ID}}
      AND c.billing_state = (SELECT billing_state FROM customers WHERE organization_id = {{ORG_ID}} AND code = '{{CUSTOMER_CODE}}')
      AND pi.customer_bill_to_number != '{{CUSTOMER_CODE}}'
      AND pi.invoice_date >= NOW() - INTERVAL '12 months'
      AND pii.quantity_invoiced > 0
    GROUP BY pi.customer_bill_to_number, COALESCE(t.name, p.category_code, 'Uncategorized')
  ) sub
  GROUP BY cat
  HAVING COUNT(*) >= 5
)
-- v4 NOTE: This is Tier 1 (same state, no revenue filter). For Tier 1 with revenue filter,
-- add to the inner subquery WHERE clause:
--   AND pi.customer_bill_to_number IN (
--     SELECT customer_bill_to_number FROM portal_orders
--     WHERE organization_id = {{ORG_ID}}
--       AND order_date >= NOW() - INTERVAL '12 months'
--     GROUP BY customer_bill_to_number
--     HAVING SUM(total_amount) BETWEEN {{CUSTOMER_LTM_REVENUE}} * 0.5 AND {{CUSTOMER_LTM_REVENUE}} * 2.0
--   )
-- For Tier 3 (org-wide), remove the c.billing_state filter entirely.
SELECT
  cs.category,
  cs.cohort_avg_revenue AS similar_customers_avg,
  COALESCE(csp.revenue, 0) AS this_customer,
  ROUND(COALESCE(csp.revenue, 0) - cs.cohort_avg_revenue, 2) AS gap
FROM cohort_spend cs
LEFT JOIN customer_spend csp ON csp.category = cs.category
WHERE COALESCE(csp.revenue, 0) < cs.cohort_avg_revenue
ORDER BY gap ASC
LIMIT 10
```

---

## CQ-20: Category Share Evolution

**Section**: Category Drift | **Source**: Postgres

```sql
WITH ltm AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date >= NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
  GROUP BY COALESCE(t.name, p.category_code, 'Uncategorized')
),
prior AS (
  SELECT
    COALESCE(t.name, p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  LEFT JOIN taxonomies t ON t.code = p.category_code AND t.organization_id = p.organization_id AND t.type = 'Category'
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pi.invoice_date BETWEEN NOW() - INTERVAL '24 months' AND NOW() - INTERVAL '12 months'
    AND pii.quantity_invoiced > 0
  GROUP BY COALESCE(t.name, p.category_code, 'Uncategorized')
),
ltm_total AS (SELECT SUM(revenue) AS t FROM ltm),
prior_total AS (SELECT SUM(revenue) AS t FROM prior)
SELECT
  COALESCE(l.category, p.category) AS category,
  COALESCE(l.revenue, 0) AS ltm_revenue,
  ROUND(100.0 * COALESCE(l.revenue, 0) / NULLIF((SELECT t FROM ltm_total), 0), 1) AS ltm_pct,
  COALESCE(p.revenue, 0) AS prior_revenue,
  ROUND(100.0 * COALESCE(p.revenue, 0) / NULLIF((SELECT t FROM prior_total), 0), 1) AS prior_pct,
  ROUND(100.0 * COALESCE(l.revenue, 0) / NULLIF((SELECT t FROM ltm_total), 0) -
        100.0 * COALESCE(p.revenue, 0) / NULLIF((SELECT t FROM prior_total), 0), 1) AS share_shift_pts,
  ROUND(COALESCE(l.revenue, 0) - COALESCE(p.revenue, 0), 2) AS revenue_change
FROM ltm l
FULL OUTER JOIN prior p ON p.category = l.category
ORDER BY ABS(COALESCE(l.revenue, 0) - COALESCE(p.revenue, 0)) DESC
LIMIT 10
```

---

## CQ-21: Same-Store Comps

**Section**: Multi-Location Performance | **Source**: Postgres
**Gate**: Customer has 2+ ship-to locations with order activity

```sql
SELECT
  po.customer_ship_to_number AS ship_to_code,
  COALESCE(po.customer_ship_to_name, po.customer_ship_to_number) AS location_name,
  po.customer_ship_to_city AS city,
  po.customer_ship_to_state AS state,
  COUNT(*) AS orders_ltm,
  ROUND(SUM(po.total_amount)::numeric, 2) AS revenue_ltm
FROM portal_orders po
WHERE po.organization_id = {{ORG_ID}}
  AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND po.order_date >= NOW() - INTERVAL '12 months'
  AND po.customer_ship_to_number IS NOT NULL
GROUP BY po.customer_ship_to_number, po.customer_ship_to_name, po.customer_ship_to_city, po.customer_ship_to_state
ORDER BY revenue_ltm DESC
LIMIT 15
```

---

## CQ-22: Wallet Share Estimation

**Section**: Whitespace | **Source**: Postgres
**Provenance** (v5): wallet share is **invoiced `net_amount`** for both the customer and the same-state cohort,
clamped to `report_through_date` (Provenance Anchor) — comparing booked-against-invoiced across a cohort would
mix grains. When `TOTAL_BUSINESS_SOURCE = ORDERS`, run the booked fallback for **both** the customer and the
cohort (never one of each) and label "booked." Suppress on `PROVABLY INCOMPLETE`/`DEAD`.
**Note**: Step 2 requires `billing_state` from CQ-01. If the customer has no record in the `customers` table (no billing_state), skip Step 2 and render wallet share as "customer revenue only — cohort comparison unavailable (no customer master record)." Confirmed on Savoy House 71429.

```sql
-- Step 1: This customer's LTM invoiced net (clamped)
WITH provenance AS (
  SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS report_through_date
  FROM portal_invoices WHERE organization_id = {{ORG_ID}} AND net_amount IS NOT NULL
)
SELECT ROUND(SUM(pi.net_amount)::numeric, 2) AS customer_revenue
FROM portal_invoices pi, provenance pv
WHERE pi.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND pi.invoice_date >  pv.report_through_date - INTERVAL '12 months'
  AND pi.invoice_date <= pv.report_through_date;

-- Step 2: Same-state cohort stats on invoiced net (substitute customer's billing_state)
WITH provenance AS (
  SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS report_through_date
  FROM portal_invoices WHERE organization_id = {{ORG_ID}} AND net_amount IS NOT NULL
)
SELECT
  ROUND(AVG(revenue)::numeric, 2) AS cohort_avg,
  ROUND(MAX(revenue)::numeric, 2) AS cohort_max,
  COUNT(*) AS cohort_size
FROM (
  SELECT SUM(pi.net_amount) AS revenue
  FROM portal_invoices pi, provenance pv
  JOIN customers c ON c.code = pi.customer_bill_to_number AND c.organization_id = pi.organization_id
  WHERE pi.organization_id = {{ORG_ID}}
    AND c.billing_state = '{{CUSTOMER_STATE}}'
    AND pi.invoice_date >  pv.report_through_date - INTERVAL '12 months'
    AND pi.invoice_date <= pv.report_through_date
    AND pi.customer_bill_to_number != '{{CUSTOMER_CODE}}'
  GROUP BY pi.customer_bill_to_number
  HAVING SUM(pi.net_amount) > 0
) sub
```

**Booked fallback** (only when `TOTAL_BUSINESS_SOURCE = ORDERS`, no invoice feed) — original `portal_orders`
version, label both customer and cohort "booked":
```sql
-- Step 1 (booked): customer LTM booked GMV
SELECT ROUND(SUM(total_amount)::numeric, 2) AS customer_revenue
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND order_date >= NOW() - INTERVAL '12 months';
-- Step 2 (booked): same-state cohort on booked GMV
SELECT
  ROUND(AVG(revenue)::numeric, 2) AS cohort_avg,
  ROUND(MAX(revenue)::numeric, 2) AS cohort_max,
  COUNT(*) AS cohort_size
FROM (
  SELECT SUM(po.total_amount) AS revenue
  FROM portal_orders po
  JOIN customers c ON c.code = po.customer_bill_to_number AND c.organization_id = po.organization_id
  WHERE po.organization_id = {{ORG_ID}}
    AND c.billing_state = '{{CUSTOMER_STATE}}'
    AND po.order_date >= NOW() - INTERVAL '12 months'
    AND po.customer_bill_to_number != '{{CUSTOMER_CODE}}'
  GROUP BY po.customer_bill_to_number
  HAVING SUM(po.total_amount) > 0
) sub
```

---

## CQ-23: Account Lifecycle Stage + Cohort Forecasting

**Section**: Account Health | **Source**: Postgres
**Provenance** (v5): tenure (`first_order`, `relationship_months`, `tenure_years`) is a cadence concept and
stays on booked `portal_orders`. But the **revenue measures that drive `lifecycle_stage`, `yoy_growth_pct`,
`vs_cohort_pct`, and `addressable_growth`** — `ltm_revenue`, `prior_revenue`, and the `tenure_cohorts.ltm_rev`
cohort average — must be **invoiced `net_amount`** when `TOTAL_BUSINESS_SOURCE = INVOICES`, windowed to
`report_through_date`. Recipe: keep the `MIN(order_date)` tenure logic on `portal_orders`; compute the LTM/prior
revenue sums from `portal_invoices.net_amount` joined on `customer_bill_to_number` (same window math as CQ-01),
for both `this_customer` and every member of `tenure_cohorts`. Stage thresholds (`>1.1`, `0.9–1.1`, `<0.9`) are
unchanged — only the dollars underneath them move from booked to invoiced. On `PROVABLY INCOMPLETE`/`DEAD`,
report lifecycle *stage* qualitatively but suppress the cohort-forecast dollars. The SQL below is **invoiced-net
canonical**; the booked variant (swap to `portal_orders`) is the `TOTAL_BUSINESS_SOURCE = ORDERS` fallback noted
beneath it.

```sql
WITH provenance AS (
  -- Layer-1 clamp (Spine §6.4); mirrors CQ-01. report_through_date defuses bad-date invoices.
  SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS report_through_date
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND net_amount IS NOT NULL
),
this_customer AS (
  -- Tenure stays on BOOKED orders (cadence concept): first_order = MIN(order_date).
  SELECT
    MIN(order_date) AS first_order,
    (EXTRACT(YEAR FROM AGE(NOW(), MIN(order_date))) * 12 + EXTRACT(MONTH FROM AGE(NOW(), MIN(order_date))))::int AS relationship_months,
    EXTRACT(YEAR FROM AGE(NOW(), MIN(order_date)))::int AS tenure_years
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND customer_bill_to_number = '{{CUSTOMER_CODE}}'
),
this_customer_rev AS (
  -- Revenue measures = INVOICED net_amount, windowed to report_through_date (same math as CQ-01).
  SELECT
    ROUND(SUM(CASE WHEN pi.invoice_date >  pv.report_through_date - INTERVAL '12 months'
                    AND pi.invoice_date <= pv.report_through_date THEN pi.net_amount ELSE 0 END)::numeric, 2) AS ltm_revenue,
    ROUND(SUM(CASE WHEN pi.invoice_date >  pv.report_through_date - INTERVAL '24 months'
                    AND pi.invoice_date <= pv.report_through_date - INTERVAL '12 months' THEN pi.net_amount ELSE 0 END)::numeric, 2) AS prior_revenue
  FROM portal_invoices pi, provenance pv
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
),
tenure_cohorts AS (
  -- Cohort tenure_years from BOOKED orders; cohort LTM revenue from INVOICED net_amount.
  SELECT
    tenure_years,
    ROUND(AVG(ltm_rev)::numeric, 2) AS cohort_avg_ltm,
    COUNT(*) AS cohort_size
  FROM (
    SELECT
      ten.customer_bill_to_number,
      ten.tenure_years,
      rev.ltm_rev
    FROM (
      SELECT customer_bill_to_number,
             EXTRACT(YEAR FROM AGE(NOW(), MIN(order_date)))::int AS tenure_years
      FROM portal_orders
      WHERE organization_id = {{ORG_ID}}
        AND customer_bill_to_number IS NOT NULL
      GROUP BY customer_bill_to_number
    ) ten
    JOIN (
      SELECT pi.customer_bill_to_number,
             SUM(pi.net_amount) AS ltm_rev
      FROM portal_invoices pi, provenance pv
      WHERE pi.organization_id = {{ORG_ID}}
        AND pi.customer_bill_to_number IS NOT NULL
        AND pi.invoice_date >  pv.report_through_date - INTERVAL '12 months'
        AND pi.invoice_date <= pv.report_through_date
      GROUP BY pi.customer_bill_to_number
      HAVING SUM(pi.net_amount) > 0
    ) rev ON rev.customer_bill_to_number = ten.customer_bill_to_number
  ) sub
  GROUP BY tenure_years
)
SELECT
  tc.first_order,
  tc.relationship_months,
  tc.tenure_years,
  tcr.ltm_revenue,
  tcr.prior_revenue,
  CASE WHEN tcr.prior_revenue > 0
    THEN ROUND(100.0 * (tcr.ltm_revenue - tcr.prior_revenue) / tcr.prior_revenue, 1)
    ELSE NULL END AS yoy_growth_pct,
  CASE
    WHEN tc.relationship_months < 12 THEN 'New'
    WHEN tcr.ltm_revenue > tcr.prior_revenue * 1.1 THEN 'Growing'
    WHEN tcr.ltm_revenue BETWEEN tcr.prior_revenue * 0.9 AND tcr.prior_revenue * 1.1 THEN 'Stable'
    WHEN tcr.ltm_revenue < tcr.prior_revenue * 0.9 AND tcr.ltm_revenue > 0 THEN 'Declining'
    WHEN tcr.ltm_revenue = 0 THEN 'Dormant'
    ELSE 'Unknown'
  END AS lifecycle_stage,
  cur_cohort.cohort_avg_ltm AS same_tenure_cohort_avg,
  cur_cohort.cohort_size AS same_tenure_cohort_size,
  CASE WHEN cur_cohort.cohort_avg_ltm > 0
    THEN ROUND(100.0 * (tcr.ltm_revenue - cur_cohort.cohort_avg_ltm) / cur_cohort.cohort_avg_ltm, 1)
    ELSE NULL END AS vs_cohort_pct,
  peak_cohort.cohort_avg_ltm AS projected_peak_revenue,
  peak_cohort.tenure_years AS peak_tenure_years,
  CASE WHEN peak_cohort.cohort_avg_ltm > tcr.ltm_revenue
    THEN ROUND((peak_cohort.cohort_avg_ltm - tcr.ltm_revenue)::numeric, 2)
    ELSE 0 END AS addressable_growth
FROM this_customer tc
CROSS JOIN this_customer_rev tcr
LEFT JOIN tenure_cohorts cur_cohort ON cur_cohort.tenure_years = tc.tenure_years
LEFT JOIN LATERAL (
  SELECT cohort_avg_ltm, tenure_years
  FROM tenure_cohorts
  WHERE tenure_years > tc.tenure_years
  ORDER BY cohort_avg_ltm DESC
  LIMIT 1
) peak_cohort ON true
```

> **Booked fallback (`TOTAL_BUSINESS_SOURCE = ORDERS`):** when no invoice feed exists, swap
> `portal_invoices`→`portal_orders`, `net_amount`→`total_amount`, `invoice_date`→`order_date` in the two revenue
> CTEs (the `this_customer_rev` window and the cohort `rev` subquery), drop the `provenance` clamp to a
> `NOW()`-based window, and **label every revenue output "booked."**

Note: `projected_peak_revenue` is the highest avg LTM revenue among tenure cohorts older than this customer. `addressable_growth` is the gap between current LTM and projected peak. Only render the forecast if `peak_cohort` returns data (i.e., the org has customers at higher tenure years). If the customer is already above the peak cohort avg, note: *"Tracking above cohort curve — no higher-tenure benchmark available."*

---

## CQ-24: Alternative SKU Suggestions for Stock-Outs

**Section**: Purchase DNA — Top Items (embedded in stock-out callout) | **Source**: Postgres
**Trigger**: Run once per stock-out item identified by CQ-03 (where `qty_available = 0` AND the item is in the customer's top 15). Substitute `{{STOCKOUT_ITEM}}` and `{{STOCKOUT_COLLECTION_CODE}}` from CQ-03 results.

```sql
SELECT
  p.item_number,
  p.long_description AS description,
  COALESCE(t.name, p.collection_code) AS collection,
  COALESCE(i.qty_available, 0) AS qty_available,
  p.net_price
FROM products p
LEFT JOIN inventories i ON i.base_item_code = p.item_number AND i.organization_id = p.organization_id
LEFT JOIN taxonomies t ON t.code = p.collection_code AND t.organization_id = p.organization_id AND t.type = 'Collection'
WHERE p.organization_id = {{ORG_ID}}
  AND p.collection_code = '{{STOCKOUT_COLLECTION_CODE}}'
  AND p.item_number != '{{STOCKOUT_ITEM}}'
  AND p.deleted = false
  AND COALESCE(i.qty_available, 0) > 0
ORDER BY i.qty_available DESC
LIMIT 3
```

Note: Only run for items where `collection_code` is not null. If the stock-out item has no collection, skip the alternative suggestion. Typically 0–6 stock-out items per brief, so this query runs 0–6 times.

---

## CQ-25: Commitment-to-Conversion Analysis

**Section**: Market Commitments (embedded conversion analysis) | **Source**: Postgres
**Gate**: `HAS_COMMITMENT_REPORTS` AND customer has > 0 commitment_reports

**Step 1 — Parse committed items from most recent commitment:**

```sql
SELECT
  cr.id AS commitment_id,
  cr.market_code,
  cr.created_at AS commitment_date,
  item_elem ->> 'base_item_code' AS committed_item,
  COALESCE((item_elem ->> 'commitment_quantity')::int, 0) AS committed_qty,
  COALESCE((item_elem ->> 'interest_quantity')::int, 0) AS interest_qty
FROM commitment_reports cr,
     jsonb_array_elements(cr.items::jsonb) AS item_elem
WHERE cr.organization_id = {{ORG_ID}}
  AND cr.bill_to_code = '{{CUSTOMER_CODE}}'
ORDER BY cr.created_at DESC
```

Note: Items have `base_item_code` (not `item_number`), `commitment_quantity` (firm order intent), and `interest_quantity` (soft interest). Both are string-typed in JSON — cast to int. A commitment with `commitment_quantity > 0` is a firm commit; `interest_quantity > 0` only is a soft signal.

**Step 2 — Cross-reference committed items against post-commitment invoices:**

For the most recent commitment (or each commitment if rendering multi-market view), substitute `{{COMMITMENT_DATE}}` and run:

```sql
SELECT
  pii.item_number AS committed_item,
  SUM(pii.quantity_invoiced)::int AS qty_invoiced,
  ROUND(SUM(pii.unit_price * pii.quantity_invoiced)::numeric, 2) AS revenue_invoiced
FROM portal_invoice_items pii
JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
WHERE pii.organization_id = {{ORG_ID}}
  AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
  AND pii.item_number IN ({{COMMITTED_ITEM_LIST}})
  AND pi.invoice_date >= '{{COMMITMENT_DATE}}'::date
  AND pii.quantity_invoiced > 0
GROUP BY pii.item_number
```

`{{COMMITTED_ITEM_LIST}}` is a comma-separated quoted list of `base_item_code` values from Step 1. Example: `'U610050', 'U560A04M'`.

**Step 3 — Compute conversion metrics (in-brief, not a query):**

- Per-item: `converted = true` if `qty_invoiced > 0` for that item
- Overall: `conversion_rate = items_converted / total_committed_items * 100`
- By category: Join committed items to `products.category_code` → `taxonomies.name`, group conversion by category
- Uncommitted items: List items with `committed_qty > 0` but `qty_invoiced = 0`, with current `inventories.qty_available`

**Rendering**: Show per-market conversion table, per-category conversion, and uncommitted items with stock status.

---

## CQ-26: Fulfillment Impact on Reorder Behavior

**Section**: Fulfillment & Returns — Backorder Impact | **Source**: Postgres
**Gate**: `HAS_PORTAL_INVOICES` AND customer has backorder events (check via CQ-15 `total_backordered > 0`)

This query measures whether backorder events change the customer's subsequent reorder behavior for the same items. It compares pre-backorder reorder intervals to post-backorder intervals.

```sql
WITH customer_backorders AS (
  SELECT DISTINCT
    poi.item_number,
    po.order_date AS backorder_date
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND COALESCE(poi.quantity_backordered, 0) > 0
    AND po.order_date >= NOW() - INTERVAL '24 months'
),
item_order_dates AS (
  SELECT
    pii.item_number,
    pi.invoice_date,
    LAG(pi.invoice_date) OVER (PARTITION BY pii.item_number ORDER BY pi.invoice_date) AS prev_date,
    CASE WHEN EXISTS (
      SELECT 1 FROM customer_backorders cb
      WHERE cb.item_number = pii.item_number
        AND cb.backorder_date <= pi.invoice_date
        AND cb.backorder_date > pi.invoice_date - INTERVAL '180 days'
    ) THEN true ELSE false END AS had_recent_backorder
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.customer_bill_to_number = '{{CUSTOMER_CODE}}'
    AND pii.quantity_invoiced > 0
    AND pi.invoice_date >= NOW() - INTERVAL '36 months'
    AND pii.item_number IN (SELECT DISTINCT item_number FROM customer_backorders)
),
intervals AS (
  SELECT
    item_number,
    (invoice_date - prev_date) AS days_gap,
    had_recent_backorder
  FROM item_order_dates
  WHERE prev_date IS NOT NULL
    AND (invoice_date - prev_date) >= 1
)
SELECT
  item_number,
  ROUND(AVG(CASE WHEN NOT had_recent_backorder THEN days_gap END)::numeric, 1) AS avg_interval_normal,
  ROUND(AVG(CASE WHEN had_recent_backorder THEN days_gap END)::numeric, 1) AS avg_interval_post_backorder,
  COUNT(CASE WHEN NOT had_recent_backorder THEN 1 END) AS normal_intervals,
  COUNT(CASE WHEN had_recent_backorder THEN 1 END) AS post_backorder_intervals,
  CASE WHEN AVG(CASE WHEN NOT had_recent_backorder THEN days_gap END) > 0
    THEN ROUND(
      AVG(CASE WHEN had_recent_backorder THEN days_gap END)::numeric /
      AVG(CASE WHEN NOT had_recent_backorder THEN days_gap END)::numeric, 1)
    ELSE NULL END AS slowdown_multiplier
FROM intervals
GROUP BY item_number
HAVING COUNT(CASE WHEN NOT had_recent_backorder THEN 1 END) >= 2
   AND COUNT(CASE WHEN had_recent_backorder THEN 1 END) >= 1
ORDER BY slowdown_multiplier DESC NULLS LAST
LIMIT 10
```

Note: `had_recent_backorder` is true if there was a backorder event on the same item within 180 days before the invoice date. `slowdown_multiplier` > 1.0 means reorders slowed after a backorder; > 2.0 is a strong signal. To compute annualized revenue impact, multiply each item's LTM revenue (from CQ-03) by `(1 - 1/slowdown_multiplier)` — this estimates the revenue lost to slower reordering.

**Guard**: Only render if at least 1 item has both normal and post-backorder intervals (the HAVING clause handles this). Not all orgs populate `quantity_backordered` — check CQ-15 `total_backordered > 0` first.
