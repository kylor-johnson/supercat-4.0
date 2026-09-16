# External Report Query Library

> **Status**: Frozen — schema-grounded, audited against confirmed production schema (2026-04-06).
> **Semantic authority**: `reference/value_moment_catalog.md`
> **Schema basis**: Live schema discovery run 2026-04-06 against production Postgres MCP.
> **Audience tags**: Each query tagged `external`, `internal`, or `shared`.
> **MCP targets**: `user-supercat-postgres-vpn` for Postgres queries; `user-bigquery-admin` for BigQuery queries (migrated 2026-06-03 from the legacy read-only `user-bigquery-vpn`/Weld; native `supercat-data-pipeline` datasets). The admin `query` tool takes **`sql`** and has no `max_results` — bound rows with SQL `LIMIT`. Canonical warehouse reference: `/BIGQUERY_ADMIN_REFERENCE.md`.

---

## Schema Discovery Results (Run 2026-04-06)

Key findings that informed this audit:

| Table | Key Confirmed Columns | Notes |
|-------|----------------------|-------|
| `orders` | `id`, `organization_id`, `is_submitted`, `is_marked_deleted`, `created_at`, `total`, `order_source`, `order_type`, `customer_num`, `org_user_id`, `rep_first_name`, `rep_last_name`, `bill_to_company_name`, `bill_to_state` | `order_source` = `'ipad'` or `'server'`; `is_marked_deleted` is nullable |
| `customers` | `id`, `organization_id`, `code`, `name`, `billing_state`, `territory_codes`, `territory_codes_json` | `territory_codes` format **varies by org**: may be comma-separated text (`"C-14,C-15"`) or JSON-array (`["C-14"]`). `territory_codes_json` is the JSON column variant. Run Q-43 pre-flight format check before unnesting. |
| `org_users` | `id`, `organization_id`, `user_id`, `territory_codes` (JSON), `territory_codes_yaml`, `company_name`, `company_email`, `last_ipad_login_at`, `last_ecat_online_login_at` | Reps have territory assignments here; `first_name`/`last_name` are on the `users` table joined via `user_id` |
| `products` | `id`, `organization_id`, `item_number`, `category_code`, `collection_code`, `new_item`, `image_exists`, `hideable`, `net_price`, `deleted`, `long_description` | `deleted` column (not `is_deleted`); `hideable = true` = explicitly hidden; `hideable = false OR NULL` = visible (NULL is default visible state in many orgs — do not filter `hideable = false` alone) |
| `portal_orders` | `id`, `organization_id`, `order_number`, `order_date`, `order_origin`, `total_amount`, `customer_bill_to_number`, `customer_bill_to_name`, `customer_bill_to_state`, `customer_bill_to_city`, `customer_bill_to_postal_code`, `rep_number`, `rep_name`, `buyer_name` | `order_date` is a `date` type; `order_origin` tracks channel source; state column is `customer_bill_to_state` (not `bill_to_state`) |
| `portal_order_items` | `id`, `organization_id`, `item_number`, `ecat_item_number`, `description`, `quantity_ordered`, `quantity_invoiced`, `unit_price`, `order_number` | Join to `portal_orders` on `order_number` + `organization_id` |
| `import_events` | `id`, `organization_id`, `created_at`, `data` | `data` is TEXT (YAML format); check for error arrays |
| `smart_stacks` | `id`, `organization_id`, `name`, `created_at`, `updated_at`, `published`, `is_dormant`, `item_numbers` | `is_dormant` flag available; view/interaction data is Mixpanel-side only |
| `shared_resources` | `id`, `organization_id`, `label`, `resource_type`, `shared_document_file_name`, `created_at`, `updated_at` | Document-level view/email stats are Mixpanel-side only |
| `sales_data` | `id`, `organization_id`, `base_item_code`, `bill_to_code`, `ship_to_code`, `amount_invoiced`, `quantity_invoiced`, `est_ship_date` | **No `invoice_date` or `period` column** — confirms VM-38b pending engineering |
| `inventories` | `id`, `organization_id`, `base_item_code`, `qty_available`, `qty_on_hand`, `qty_on_backorder`, `next_scheduled_receipt_date` | Join to `products` on `item_number = base_item_code` |
| `data_versions` | `id`, `organization_id`, `entity_type`, `timestamp` | 4 columns only |
| `login_events` | `id`, `organization_id`, `user_id`, `created_at`, `first_name`, `last_name`, `company_name` | `first_name`/`last_name` on `login_events` directly |
| `enrollment_applicants` | `id`, `organization_id`, `user_id`, `email`, `first_name`, `last_name`, `company_name`, `status`, `created_at`, `updated_at`, `is_ecat_online` | `status` values: `accepted`, `rejected`, `pending` |
| `territories` | `id`, `organization_id`, `code`, `name` | Lookup table for territory codes |

**Critical schema note for VM-43 (territory coverage)**: Territory data lives on BOTH `customers.territory_codes` AND `org_users.territory_codes` (JSON array). Customer-to-territory attribution is most reliable via `customers.territory_codes`. **Format varies by org** — some orgs store it as plain comma-separated text (`"C-14,C-15"`), others as a JSON array (`["C-14"]`). Always run the Q-43 pre-flight format check before executing Steps 1 and 3. Use the CSV path (`string_to_array`) for plain text; use the JSON path (`jsonb_array_elements_text`) for JSON-array format. `customers.territory_codes_json` is the JSON column variant where present. Orders carry `rep_first_name`/`rep_last_name` directly — rep identity does not require joining to `org_users` for Q-43. There is no direct rep-name column on `org_users`.

**Critical schema note for VM-46 (workflow maturity)**: The eCat submit rate is best calculated as `eCat submitted orders / Mixpanel behavioral signals` — the denominator requires BigQuery Mixpanel data. The Postgres side contributes the `orders` numerator only.

**VM-38b confirmed pending engineering**: `sales_data` has no `invoice_date` or `period` column. VM-38b requires a one-column ERP import pipeline change.

---

## Global Query Guardrails

### Orders table
All queries touching `orders` must use:
```sql
AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
```
The `is_marked_deleted` column is nullable — `NULL` means not deleted. Using `= false` alone silently drops valid orders.

### NOT IN guard
Any subquery using `NOT IN` on `customer_num` must include:
```sql
AND customer_num IS NOT NULL
```
PostgreSQL `NOT IN` with a NULL in the list returns empty results.

### `portal_orders` framing (locked semantic rule)
`portal_orders` = ERP-synced total business across all channels. It is internal BI data visible in the client's Sales Portal. Any query interpretation referencing `portal_orders` must use one of:
- "orders synced from your ERP"
- "total business across all channels"
- "all-channel order volume"

Never: "portal ordering," "buyer self-service," "portal orders placed by buyers."

### VM-45 denominator validity gate (required before running Q-45)
Before running Q-45, compute LTM eCat GMV and LTM `portal_orders` GMV separately and apply both gates:
1. **Gate 1**: `portal_orders_gmv > ecat_gmv` — if eCat GMV equals or exceeds ERP GMV, the ERP sync is partial and the denominator is invalid. Skip VM-45.
2. **Gate 2**: `ecat_gmv >= 0.05 × portal_orders_gmv` — if eCat is less than 5% of ERP total, the capture rate is not interpretable as an activation signal. Skip VM-45.

If either gate fails, do not run Q-45. Do not substitute a denominator-less eCat GMV statement. Note the skip reason in the Appendix.

### VM-44 enrollment status quality gate
> **Enrollment is out of scope for the external report system.** Q-44 and Q-15 are retained in this library for potential internal or specialized use only. Do not run them as part of the standard external report operator. The gate logic below is preserved for reference but is not part of the external runtime path.

```sql
-- Retained for internal/future use only — not part of external report runtime
SELECT COUNT(*) FROM enrollment_applicants
WHERE organization_id = {{ORG_ID}} AND status IS NOT NULL;
```

---

## Org Lookup

Run this first to resolve `organization_id` from shortname.

```sql
-- audience: shared | status: live
SELECT id, shortname, name
FROM organizations
WHERE shortname = '{{ORG_SHORTNAME}}'
```

---

## Domain 1 — Rep Performance Intelligence

### Q-01: Rep Behavioral Scorecard
**Maps to**: VM-01 | **Audience**: external | **Status**: live | **Source**: BigQuery Mixpanel

**Step 1 — Behavioral data (BigQuery `mixpanel.user_feature_usage_report`):**

```sql
SELECT
  username,
  days_active,
  total_events,
  first_event,
  last_event,
  -- Customer Targeting (Dimension 1)
  (select_a_customer + search_for_customer) AS customer_targeting,
  select_a_customer,
  search_for_customer,
  -- Product Discovery (Dimension 2)
  (search_products + filter_products + search_collections) AS product_discovery,
  search_products,
  filter_products,
  -- Configuration & Bundling (Dimension 3)
  (order_configured_item + view_kit + order_kit) AS config_bundling,
  order_configured_item,
  view_kit,
  order_kit,
  -- Presentation & Communication (Dimension 4)
  (email_item_info + create_pdf_catalog + share_my_list + export_data_to_csv + export_data_to_excel) AS presentation,
  email_item_info,
  create_pdf_catalog,
  share_my_list,
  -- Information & Planning (Dimension 5)
  (view_library_entry + email_single_library_entry + email_multiple_library_entries) AS information,
  view_library_entry,
  -- Engagement Depth (Dimension 6)
  access_sales_portal,
  view_my_list,
  create_my_list,
  edit_my_list,
  view_cust_favorites,
  view_ipad_orders,
  submit_order
FROM mixpanel.user_feature_usage_report
WHERE org = '{{ORG_SHORTNAME}}'
ORDER BY total_events DESC
```

**Step 2 — Order outcomes (Postgres MCP):**

```sql
-- NOTE: org_users has no `username` column. Rep identity comes from orders directly.
-- Group by the name fields on orders, which match the `username` in Mixpanel Step 1.
SELECT
  COALESCE(o.rep_first_name || ' ' || o.rep_last_name, CAST(o.org_user_id AS text)) AS rep_name,
  COUNT(o.id) AS total_orders,
  ROUND(SUM(o.total)::numeric, 2) AS total_gmv,
  ROUND(AVG(o.total)::numeric, 2) AS avg_order_value,
  COUNT(DISTINCT o.customer_num) AS unique_customers
FROM orders o
WHERE o.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
  AND o.created_at > NOW() - INTERVAL '12 months'
  AND o.order_source = 'ipad'
GROUP BY COALESCE(o.rep_first_name || ' ' || o.rep_last_name, CAST(o.org_user_id AS text))
ORDER BY total_gmv DESC
```

**Assembly**: Join Step 1 (Mixpanel) and Step 2 (Postgres) on rep name. Mixpanel `username` typically matches `rep_first_name || ' ' || rep_last_name` from orders. Where an exact match is not possible (e.g., display name variation), use order-side data for GMV/order counts and Mixpanel data for behavioral dimensions — do not drop reps from the leaderboard just because a name join is imperfect. For each rep, calculate per-order ratios and compare to org median. Pair with Q-02 and Q-03 for archetype and funnel gap analysis.

**External claim rules**: Per-rep eCat GMV, order count, AOV, and customer count. Never claim "net-new customers" or attribute non-eCat outcomes to rep behavior.

---

### Q-02: Selling Archetype Classification
**Maps to**: VM-02 | **Audience**: external | **Status**: live (derived from Q-01)

No separate query — archetypes are derived from Q-01 behavioral ratios. Classification rules:

| Archetype | Detection Rule |
|-----------|----------------|
| Deep-Account Specialist | High `customer_targeting` + high orders + `unique_customers ≤ 3` |
| Curated Discovery Seller | Top-quartile `presentation` + high `product_discovery` + `avg_order_value` above org median |
| Volume Relationship Seller | Highest `days_active` or `total_events` + broadest `unique_customers` + AOV below org median |
| Precision Closer | Low `product_discovery` + high `config_bundling` per order + AOV well above org median |
| Non-Selling Role | `submit_order ≤ 2` + `total_events > 500` — route to Q-04 |

**Gate**: Requires 3+ active selling reps. VM-02 requires VM-01 first.

---

### Q-03: Behavioral Funnel Gap Analysis
**Maps to**: VM-03 | **Audience**: external | **Status**: live (derived from Q-01)

Derived from Q-01 dimensional scores. For each selling rep (`submit_order > 5`), assess ratio of each dimension to upstream:

1. Customer Targeting → Product Discovery: `product_discovery / customer_targeting` — if < 3:1, rep isn't discovering enough after selecting customers.
2. Product Discovery → Configuration: `config_bundling / product_discovery` — if < 0.1, browses but doesn't build complex orders.
3. Configuration → Presentation: `presentation / config_bundling` — if < 0.1, configures but doesn't share.
4. Presentation → Orders: `submit_order / presentation` — disproportionately low = closure gap.

Flag reps with any funnel ratio in the bottom quartile for the org.

**External claim rules**: Per-rep funnel gap with specific behavioral data. Quantified upside using peer AOV differences — always tag `[HYPOTHETICAL]`.

---

### Q-04: Non-Selling User Role Classification
**Maps to**: VM-04 | **Audience**: external | **Status**: live | **Source**: BigQuery Mixpanel

```sql
SELECT
  username,
  days_active,
  total_events,
  submit_order,
  search_products,
  view_library_entry,
  email_single_library_entry + email_multiple_library_entries AS library_emails,
  create_pdf_catalog,
  export_data_to_csv + export_data_to_excel AS data_exports,
  access_sales_portal,
  view_my_list + create_my_list + edit_my_list AS my_list_activity,
  CASE
    WHEN submit_order <= 2 AND (view_library_entry > 200 OR (email_single_library_entry + email_multiple_library_entries) > 20)
      THEN 'Content/Library Manager'
    WHEN submit_order <= 2 AND create_pdf_catalog > 20
      THEN 'Catalog/Data Manager'
    WHEN submit_order <= 2 AND (view_my_list + create_my_list + edit_my_list) > 50
      THEN 'Merchandising/List Curator'
    WHEN submit_order <= 2 AND access_sales_portal > 100
      THEN 'Analytics/Portal User'
    WHEN submit_order <= 2 AND total_events > 500
      THEN 'Sales Support/Inside Sales'
    WHEN submit_order <= 2 AND total_events <= 500 AND days_active > 30
      THEN 'Low-Activity User'
    WHEN submit_order > 2
      THEN 'Selling Rep'
    ELSE 'Inactive'
  END AS classified_role
FROM mixpanel.user_feature_usage_report
WHERE org = '{{ORG_SHORTNAME}}'
ORDER BY total_events DESC
```

---

### Q-05: Seat Utilization
**Maps to**: VM-05 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  (SELECT COUNT(*) FROM org_users WHERE organization_id = {{ORG_ID}} AND disabled = false) AS active_org_users,
  (SELECT COUNT(DISTINCT user_id) FROM login_events
   WHERE organization_id = {{ORG_ID}}
     AND created_at > NOW() - INTERVAL '90 days') AS logged_in_90d,
  (SELECT COUNT(DISTINCT org_user_id) FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
     AND created_at > NOW() - INTERVAL '90 days'
     AND org_user_id IS NOT NULL) AS ordering_users_90d
```

**External claim rules**: Active vs. inactive user breakdown, security hygiene recommendation. Never say "X% of your licenses are wasted."

---

### Q-06: Rep Engagement Trajectory
**Maps to**: VM-06 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
WITH rep_logins AS (
  SELECT
    first_name || ' ' || last_name AS rep_name,
    user_id,
    COUNT(CASE WHEN created_at > NOW() - INTERVAL '90 days' THEN 1 END) AS logins_current_90d,
    COUNT(CASE WHEN created_at BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days' THEN 1 END) AS logins_prev_90d
  FROM login_events
  WHERE organization_id = {{ORG_ID}}
    AND created_at > NOW() - INTERVAL '180 days'
  GROUP BY first_name, last_name, user_id
),
rep_orders AS (
  SELECT
    rep_first_name || ' ' || rep_last_name AS rep_name,
    COUNT(CASE WHEN created_at > NOW() - INTERVAL '90 days' THEN 1 END) AS orders_current_90d,
    COUNT(CASE WHEN created_at BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days' THEN 1 END) AS orders_prev_90d,
    ROUND(SUM(CASE WHEN created_at > NOW() - INTERVAL '90 days' THEN total ELSE 0 END)::numeric, 2) AS gmv_current_90d,
    ROUND(SUM(CASE WHEN created_at BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days' THEN total ELSE 0 END)::numeric, 2) AS gmv_prev_90d
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '180 days'
    AND rep_last_name IS NOT NULL
  GROUP BY rep_first_name, rep_last_name
)
SELECT
  COALESCE(l.rep_name, o.rep_name) AS rep_name,
  l.logins_prev_90d,
  l.logins_current_90d,
  CASE WHEN l.logins_prev_90d > 0
    THEN ROUND(100.0 * (l.logins_current_90d - l.logins_prev_90d) / l.logins_prev_90d, 1)
    ELSE NULL END AS login_change_pct,
  o.orders_prev_90d,
  o.orders_current_90d,
  CASE WHEN o.orders_prev_90d > 0
    THEN ROUND(100.0 * (o.orders_current_90d - o.orders_prev_90d) / o.orders_prev_90d, 1)
    ELSE NULL END AS order_change_pct,
  o.gmv_current_90d
FROM rep_logins l
FULL OUTER JOIN rep_orders o ON l.rep_name = o.rep_name
ORDER BY o.orders_current_90d DESC NULLS LAST
```

**External claim rules**: Rolling login and eCat order trend per rep. Decline percentage over 90-day windows. Never say "rep is about to leave" or attribute total-business decline to a rep.

---

### Q-43: Territory Coverage & Dormancy
**Maps to**: VM-43 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**Schema basis**: Territory codes live on `customers` in two formats depending on the org — check before running:
- `customers.territory_codes` — text field, may be comma-separated (`"C-14,C-15"`) or JSON-array formatted (`["C-14"]`)
- `customers.territory_codes_json` — JSON column (more reliable where present)

Orders carry `rep_first_name` / `rep_last_name` for rep attribution. The `territories` table provides code-to-name lookup.

**Pre-flight: detect territory_codes format and confirm data availability:**

```sql
-- Run this first. If no rows return, Q-43 is blocked for this org (see gate note below).
SELECT territory_codes
FROM customers
WHERE organization_id = {{ORG_ID}}
  AND territory_codes IS NOT NULL
  AND territory_codes != ''
LIMIT 3;
```

**Gate**: If the pre-flight returns 0 rows, also check the `territories` table:

```sql
SELECT COUNT(*) FROM territories WHERE organization_id = {{ORG_ID}};
```

If both return 0 / no rows, Q-43 is **data-gated for this org** — territory data has not been configured. Do not proceed to Steps 1–3. Document in Appendix as: "Q-43 (Territory Coverage) not executed — territories table contains no rows for this org and customer territory_codes are not populated. Classification: org-specific data gap (territory data not configured)."

If data is present: if results look like `["C-14"]` (JSON-array format), use the **JSON path** variants in Steps 1 and 3 below. If results look like `C-14` or `C-14,C-15` (plain text), use the **CSV path** variants.

**Step 1 — Customer base by territory (customer-side attribution):**

*CSV path (plain comma-separated `territory_codes`):*
```sql
SELECT
  TRIM(tc_code) AS territory_code,
  t.name AS territory_name,
  COUNT(DISTINCT c.code) AS total_assigned_customers
FROM customers c,
  LATERAL unnest(string_to_array(c.territory_codes, ',')) AS tc_code
LEFT JOIN territories t ON t.code = TRIM(tc_code) AND t.organization_id = c.organization_id
WHERE c.organization_id = {{ORG_ID}}
  AND c.territory_codes IS NOT NULL
  AND c.territory_codes != ''
GROUP BY TRIM(tc_code), t.name
ORDER BY total_assigned_customers DESC
```

*JSON path (JSON-array formatted `territory_codes`, e.g. `["C-14"]`):*
```sql
SELECT
  TRIM(tc_code) AS territory_code,
  t.name AS territory_name,
  COUNT(DISTINCT c.code) AS total_assigned_customers
FROM customers c,
  LATERAL jsonb_array_elements_text(c.territory_codes::jsonb) AS tc_code
LEFT JOIN territories t ON t.code = TRIM(tc_code) AND t.organization_id = c.organization_id
WHERE c.organization_id = {{ORG_ID}}
  AND c.territory_codes IS NOT NULL
  AND c.territory_codes != ''
  AND c.territory_codes != '[]'
GROUP BY TRIM(tc_code), t.name
ORDER BY total_assigned_customers DESC
```

**Step 2 — eCat order activity by customer (trailing 12 months):**

```sql
SELECT
  customer_num,
  COUNT(*) AS ecat_orders,
  ROUND(SUM(total)::numeric, 2) AS ecat_gmv,
  MAX(created_at) AS last_ecat_order_date
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND customer_num IS NOT NULL
GROUP BY customer_num
```

**Step 3 — Territory gap summary (customers assigned but not ordering via eCat):**

*CSV path:*
```sql
WITH assigned AS (
  SELECT
    TRIM(tc_code) AS territory_code,
    c.code AS customer_code,
    c.name AS customer_name,
    c.billing_state
  FROM customers c,
    LATERAL unnest(string_to_array(c.territory_codes, ',')) AS tc_code
  WHERE c.organization_id = {{ORG_ID}}
    AND c.territory_codes IS NOT NULL
    AND c.territory_codes != ''
),
ecat_active AS (
  SELECT DISTINCT customer_num
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '12 months'
    AND customer_num IS NOT NULL
)
SELECT
  a.territory_code,
  COUNT(DISTINCT a.customer_code) AS assigned_customers,
  COUNT(DISTINCT e.customer_num) AS ecat_active_customers,
  COUNT(DISTINCT a.customer_code) - COUNT(DISTINCT e.customer_num) AS never_or_lapsed_via_ecat
FROM assigned a
LEFT JOIN ecat_active e ON e.customer_num = a.customer_code
GROUP BY a.territory_code
ORDER BY never_or_lapsed_via_ecat DESC
```

*JSON path (replace the `assigned` CTE only — `ecat_active` CTE and final SELECT are unchanged):*
```sql
WITH assigned AS (
  SELECT
    TRIM(tc_code) AS territory_code,
    c.code AS customer_code,
    c.name AS customer_name,
    c.billing_state
  FROM customers c,
    LATERAL jsonb_array_elements_text(c.territory_codes::jsonb) AS tc_code
  WHERE c.organization_id = {{ORG_ID}}
    AND c.territory_codes IS NOT NULL
    AND c.territory_codes != ''
    AND c.territory_codes != '[]'
),
-- ... ecat_active CTE and final SELECT unchanged from CSV path above
```

**External claim rules**: Accounts assigned to reps but with no eCat order history. Territory activation rate. Never say "these accounts don't buy from you" — they may order via non-eCat channels.

---

### Q-46: eCat Selling Workflow Maturity
**Maps to**: VM-46 | **Audience**: external | **Status**: conditional (requires Mixpanel for denominator) | **Source**: Postgres MCP + BigQuery Mixpanel

**Postgres side — eCat submit count (numerator):**

```sql
SELECT
  COUNT(*) AS submitted_ecat_orders_90d
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '90 days'
```

**Mixpanel side — behavioral signal count (denominator, BigQuery):**

```sql
SELECT
  SUM(select_a_customer + search_for_customer) AS customer_targeting_events,
  SUM(search_products + filter_products) AS product_discovery_events,
  SUM(create_pdf_catalog + email_item_info + share_my_list) AS presentation_events
FROM mixpanel.org_feature_usage_report
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

**Band classification** (apply after assembling both sides):

| Submit Rate | Band | Platform Role |
|-------------|------|--------------|
| 0% | Non-submit-through | Pure selling/presentation layer |
| < 10% | Minimal submit-through | Enablement-heavy |
| 10–25% | Partial capture | Meaningful eCat orders; majority close outside |
| > 25% | Transactional | eCat is a primary order capture channel |

**External claim rules**: Submit-through rate with band label. "Your team uses eCat as a selling layer even without full order submission." Never say "low eCat submit volume = low platform value."

---

## Domain 2 — Instance Health & Data Quality

### Q-07: Catalog Completeness Score
**Maps to**: VM-07 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  CASE
    WHEN p.hideable = true THEN 'hidden'
    ELSE 'visible'   -- covers both hideable = false AND hideable IS NULL (default visible)
  END AS visibility,
  COUNT(*) AS total_products,
  COUNT(CASE WHEN p.image_exists = false OR p.image_exists IS NULL THEN 1 END) AS missing_images,
  COUNT(CASE WHEN p.net_price IS NULL THEN 1 END) AS missing_price,
  ROUND(
    100.0 * COUNT(CASE WHEN p.image_exists = true AND p.net_price IS NOT NULL THEN 1 END)
    / NULLIF(COUNT(*), 0), 1
  ) AS completeness_pct
FROM products p
WHERE p.organization_id = {{ORG_ID}}
  AND p.deleted = false
GROUP BY visibility
ORDER BY visibility
```

**Interpretation**: Visible products = `hideable = false OR hideable IS NULL` (products are visible by default unless explicitly hidden). Hidden products = `hideable = true`. Report visible completeness as the primary metric. Platform median ~74%.

**Schema note**: `hideable = NULL` is the default state in many orgs — it means "not explicitly hidden" and should be treated as visible. Do not use `hideable = false` alone as the visibility filter: it will produce near-zero counts on orgs where the field was never explicitly set, making the catalog appear empty when it is not.

---

### Q-08: Data Freshness Monitor
**Maps to**: VM-08 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  entity_type,
  timestamp AS last_updated,
  EXTRACT(DAY FROM NOW() - timestamp)::int AS days_since_update,
  CASE
    WHEN EXTRACT(DAY FROM NOW() - timestamp) <= 30 THEN 'Fresh'
    WHEN EXTRACT(DAY FROM NOW() - timestamp) <= 180 THEN 'Monitor'
    ELSE 'Stale'
  END AS status
FROM data_versions
WHERE organization_id = {{ORG_ID}}
ORDER BY timestamp ASC
```

**Label rule**: Use exactly these three labels: Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days). Never use "Acceptable," "Warning," "Critical," or any other labels.

---

### Q-09: Import Health & Sync Reliability
**Maps to**: VM-09 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**Monthly import trend:**

```sql
SELECT
  DATE_TRUNC('month', created_at) AS month,
  COUNT(*) AS import_count
FROM import_events
WHERE organization_id = {{ORG_ID}}
  AND created_at > NOW() - INTERVAL '6 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC
```

**Recent imports — error check:**

```sql
SELECT
  created_at,
  data
FROM import_events
WHERE organization_id = {{ORG_ID}}
ORDER BY created_at DESC
LIMIT 10
```

**Interpretation**: Consistent import cadence = healthy pipeline. Error arrays in the `data` YAML field (look for `:error` or `:fatal` keys with non-empty values) indicate import failures. If account manages data entirely through Admin Console with no import history, note as N/A.

---

### Q-10: Feature Enablement Gap Analysis
**Maps to**: VM-10 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  ms.enable_sales_portal,
  ms.enable_online_catalog,
  ms.enable_online_ordering,
  (SELECT COUNT(*) FROM kit_items WHERE organization_id = {{ORG_ID}}) AS kit_item_count,
  (SELECT COUNT(*) FROM contract_prices WHERE organization_id = {{ORG_ID}}) AS contract_price_count,
  (SELECT COUNT(*) FROM enrollment_applicants WHERE organization_id = {{ORG_ID}}) AS enrollment_count,
  (SELECT COUNT(*) FROM smart_stacks WHERE organization_id = {{ORG_ID}}) AS smart_stack_count,
  (SELECT COUNT(*) FROM shared_resources WHERE organization_id = {{ORG_ID}}) AS shared_resource_count,
  (SELECT COUNT(*) FROM portal_orders WHERE organization_id = {{ORG_ID}}) AS portal_order_count
FROM mobile_sites ms
WHERE ms.organization_id = {{ORG_ID}}
```

**External claim rules**: "This feature is available in your plan but not yet active." Never list eCat Online features as gaps for iPad-only clients. Never list CPQ as adoption gap for non-CPQ accounts — that is an expansion opportunity, not a gap.

---

### Q-11: Configuration Completeness
**Maps to**: VM-11 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  dv.entity_type,
  dv.timestamp AS last_updated,
  EXTRACT(DAY FROM NOW() - dv.timestamp)::int AS days_stale,
  CASE dv.entity_type
    WHEN 'sales_quotas' THEN (SELECT COUNT(*) FROM sales_quotas WHERE organization_id = {{ORG_ID}})
    WHEN 'kit_items' THEN (SELECT COUNT(*) FROM kit_items WHERE organization_id = {{ORG_ID}})
    WHEN 'contract_prices' THEN (SELECT COUNT(*) FROM contract_prices WHERE organization_id = {{ORG_ID}})
    ELSE NULL
  END AS related_record_count
FROM data_versions dv
WHERE dv.organization_id = {{ORG_ID}}
  AND dv.timestamp < NOW() - INTERVAL '30 days'
ORDER BY dv.timestamp ASC
```

---

### Q-22: Feature Usage Depth
**Maps to**: VM-22 | **Audience**: external | **Status**: live | **Source**: BigQuery Mixpanel

**Org-level feature usage (BigQuery `mixpanel.org_feature_usage_report`):**

```sql
-- Columns schema-audited against admin 2026-06-03:
--   removed product_search (dup of search_products) and view_customer (not a column);
--   view_smart_stack -> view_smartpicks (the available aggregate column).
SELECT
  org_shortname,
  org_name,
  submit_order,
  select_a_customer,
  search_for_customer,
  email_item_info,
  create_pdf_catalog,
  view_library_entry,
  view_smartpicks,
  access_sales_portal,
  filter_products,
  search_products,
  search_collections,
  order_configured_item,
  view_kit,
  order_kit,
  share_my_list,
  export_data_to_csv,
  export_data_to_excel,
  total_events,
  total_users
FROM mixpanel.org_feature_usage_report
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

**Interpretation**: Each column is an all-time cumulative event count for the org. To assess intensity, compare each feature's event count to `total_events` for a usage share, and compare to same-bundle peer medians from `segment_benchmarks_monthly` where available.

**Rendering guidance**: Render as a table with columns: Feature, Event Count (all-time), Intensity Level (High / Medium / Low — based on event volume relative to same-bundle peers if peer data available, or relative to the org's own total_events if not). Include features with non-zero counts only. Omit features with zero events.

**External claim rules**: Feature event counts and intensity levels. Comparison to same-bundle peer accounts where peer data is available. Never use internal segment labels. Never expose raw Mixpanel table names or column names in delivered HTML — use plain-language feature names (e.g., "Product Search" not "product_search", "PDF Catalog Creation" not "create_pdf_catalog").

---

### Q-47: Smart Stack Effectiveness
**Maps to**: VM-47 | **Audience**: external | **Status**: conditional — Postgres provides stack metadata; view/order join requires Mixpanel event coverage

**Postgres side — stack inventory and dormancy:**

```sql
SELECT
  id AS stack_id,
  name AS stack_name,
  published,
  is_dormant,
  created_at,
  updated_at,
  EXTRACT(DAY FROM NOW() - updated_at)::int AS days_since_update
FROM smart_stacks
WHERE organization_id = {{ORG_ID}}
ORDER BY updated_at DESC
```

**Stale stack identification (not updated in 90+ days):**

```sql
SELECT COUNT(*) AS stale_stack_count
FROM smart_stacks
WHERE organization_id = {{ORG_ID}}
  AND updated_at < NOW() - INTERVAL '90 days'
  AND published = true
```

**View and order correlation (BigQuery Mixpanel — requires event-level coverage):**
Stack view events (`view_smart_stack`) are tracked in Mixpanel at the event level — not currently surfaced in the `org_feature_usage_report` aggregate view. Full stack effectiveness analysis (views → downstream orders) requires event-level Mixpanel query by stack ID. This part of VM-47 is `pending_query` until a per-stack Mixpanel event query is written and validated.

**External claim rules**: Stack count, stale stack identification. Post-view eCat order rate only when Mixpanel event coverage confirmed. Never attribute revenue exclusively to a stack view. Never report stack performance for stacks with fewer than 5 views.

---

### Q-50: Library / Document Engagement Effectiveness
**Maps to**: VM-50 | **Audience**: external | **Status**: conditional — Postgres provides document metadata; engagement stats are Mixpanel-side

**Postgres side — document inventory:**

```sql
SELECT
  id AS resource_id,
  label AS document_name,
  resource_type,
  shared_document_file_name,
  created_at,
  updated_at,
  EXTRACT(DAY FROM NOW() - updated_at)::int AS days_since_update
FROM shared_resources
WHERE organization_id = {{ORG_ID}}
  AND parent_id IS NULL
ORDER BY updated_at DESC
```

**Stale document identification (no update in 90+ days):**

```sql
SELECT COUNT(*) AS stale_document_count
FROM shared_resources
WHERE organization_id = {{ORG_ID}}
  AND parent_id IS NULL
  AND updated_at < NOW() - INTERVAL '90 days'
```

**Note**: Document view counts (`view_document`) and email shares (`email_document`) are Mixpanel events — available via BigQuery `mixpanel.user_feature_usage_report` at the org level (aggregate: `view_library_entry`, `email_single_library_entry + email_multiple_library_entries`). Per-document breakdown requires event-level Mixpanel query and is conditional on coverage per org.

**External claim rules**: Document view and email share counts only where Mixpanel coverage confirmed. Stale document identification from Postgres metadata is always available. Never attribute sales outcomes to document views.

---

## Domain 3 — Customer & Buyer Intelligence

### Q-12: Customer Activation & ERP Penetration
**Maps to**: VM-12 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  (SELECT COUNT(DISTINCT code) FROM customers WHERE organization_id = {{ORG_ID}}) AS total_erp_customers,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
     AND customer_num IS NOT NULL) AS total_ever_ordered_via_ecat,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
     AND customer_num IS NOT NULL
     AND created_at >= NOW() - INTERVAL '12 months') AS active_12mo,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
     AND customer_num IS NOT NULL
     AND created_at >= NOW() - INTERVAL '6 months') AS active_6mo,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
     AND customer_num IS NOT NULL
     AND created_at >= NOW() - INTERVAL '3 months') AS active_3mo
```

**Derived metrics**:
- `lapsed_ecat = total_ever_ordered_via_ecat - active_12mo` — buyers who have ordered before but not in 12 months
- `never_activated = total_erp_customers - total_ever_ordered_via_ecat` — ERP records with no eCat history
- `ecat_retention_rate = active_12mo / total_ever_ordered_via_ecat`

**External claim rules**: The primary metric is `ecat_retention_rate`. ERP total is secondary context only. Never say "81% of your dealers are dormant" using ERP total as denominator. Never say "net-new customers."

---

### Q-13: Customer Concentration Risk
**Maps to**: VM-13 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
WITH customer_gmv AS (
  SELECT
    customer_num,
    bill_to_company_name,
    COUNT(*) AS orders,
    ROUND(SUM(total)::numeric, 2) AS gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '12 months'
    AND customer_num IS NOT NULL
  GROUP BY customer_num, bill_to_company_name
),
total AS (
  SELECT SUM(gmv) AS total_gmv FROM customer_gmv
)
SELECT
  c.customer_num,
  c.bill_to_company_name,
  c.orders,
  c.gmv,
  ROUND(100.0 * c.gmv / NULLIF(t.total_gmv, 0), 1) AS pct_of_ecat_gmv
FROM customer_gmv c, total t
ORDER BY c.gmv DESC
LIMIT 15
```

**External claim rules**: eCat GMV concentration percentages. Always clarify this is eCat-channel only, not total-business concentration.

---

### Q-14: Customer Reorder Frequency & Velocity
**Maps to**: VM-14 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  customer_num,
  bill_to_company_name,
  COUNT(*) AS ecat_order_count,
  ROUND(SUM(total)::numeric, 2) AS ecat_gmv,
  MIN(created_at) AS first_ecat_order,
  MAX(created_at) AS last_ecat_order,
  ROUND(
    EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at))) / 86400
    / NULLIF(COUNT(*) - 1, 0), 1
  ) AS avg_days_between_ecat_orders
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND customer_num IS NOT NULL
GROUP BY customer_num, bill_to_company_name
HAVING COUNT(*) >= 3
ORDER BY ecat_order_count DESC
LIMIT 20
```

**External claim rules**: eCat reorder frequency and trend per buyer. Always qualify as eCat-channel only. Never claim total-business reorder frequency.

---

### Q-15: Enrollment Funnel Analysis
**Maps to**: VM-15 | **Audience**: internal (non_runtime for external report) | **Status**: excluded from external scope | **Source**: Postgres MCP

> **Scope note**: Enrollment is intentionally excluded from the external report system. This query is retained for potential internal or specialized use only. Do not run it as part of the standard external report operator.

```sql
SELECT
  status,
  COUNT(*) AS count,
  MIN(created_at) AS earliest,
  MAX(created_at) AS latest,
  ROUND(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (), 0), 1) AS pct
FROM enrollment_applicants
WHERE organization_id = {{ORG_ID}}
GROUP BY status
ORDER BY count DESC
```

**External claim rules**: Acceptance rate and funnel stage breakdown. First-eCat-order conversion rate when joined to `orders`. Never say "accepted applicants = new customers" — they are not confirmed eCat buyers until they order.

---

### Q-17: Dormant eCat Customer Identification
**Maps to**: VM-17 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**Recently lapsed (ordered 4–12 months ago, NOT in last 3 months):**

```sql
SELECT
  c.code AS customer_num,
  c.name AS customer_name,
  c.billing_state,
  MAX(o.created_at) AS last_ecat_order_date,
  COUNT(o.id) AS historical_ecat_orders,
  ROUND(SUM(o.total)::numeric, 2) AS historical_ecat_gmv
FROM customers c
JOIN orders o ON o.customer_num = c.code AND o.organization_id = c.organization_id
WHERE c.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
  AND o.created_at BETWEEN NOW() - INTERVAL '12 months' AND NOW() - INTERVAL '3 months'
  AND o.customer_num IS NOT NULL
  AND c.code NOT IN (
    SELECT DISTINCT customer_num FROM orders
    WHERE organization_id = {{ORG_ID}}
      AND is_submitted = true
      AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
      AND created_at > NOW() - INTERVAL '3 months'
      AND customer_num IS NOT NULL
  )
GROUP BY c.code, c.name, c.billing_state
ORDER BY historical_ecat_gmv DESC
LIMIT 25
```

**At-risk high-value sub-view:**

```sql
SELECT
  c.code AS customer_num,
  c.name AS customer_name,
  c.billing_state,
  ROUND(SUM(o.total)::numeric, 2) AS ecat_gmv_12mo,
  MAX(o.created_at) AS last_ecat_order_date,
  EXTRACT(DAY FROM NOW() - MAX(o.created_at))::int AS days_since_last_ecat_order
FROM orders o
JOIN customers c ON c.code = o.customer_num AND c.organization_id = o.organization_id
WHERE o.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
  AND o.created_at >= NOW() - INTERVAL '12 months'
GROUP BY c.code, c.name, c.billing_state
HAVING MAX(o.created_at) < NOW() - INTERVAL '90 days'
ORDER BY ecat_gmv_12mo DESC
LIMIT 20
```

**External claim rules**: Lapsed eCat buyer count by dormancy window. At-risk high-value buyer list with last order date. Never apply "dormant" to buyers who have never ordered via eCat. Never say "net-new customers."

---

### Q-41: First-Time eCat Orderers by Channel & Rep
**Maps to**: VM-41 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**By month and channel:**

```sql
WITH first_orders AS (
  SELECT customer_num,
         MIN(created_at) AS first_ecat_order_date,
         MIN(order_source) AS first_order_source
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND customer_num IS NOT NULL
  GROUP BY customer_num
  HAVING MIN(created_at) >= NOW() - INTERVAL '15 months'
)
SELECT
  DATE_TRUNC('month', fo.first_ecat_order_date) AS month,
  CASE fo.first_order_source
    WHEN 'ipad' THEN 'Rep-Acquired (iPad)'
    WHEN 'server' THEN 'eCat Online-Acquired (self-serve)'
    ELSE 'Other'
  END AS acquisition_channel,
  COUNT(DISTINCT fo.customer_num) AS first_time_ecat_buyers
FROM first_orders fo
GROUP BY month, acquisition_channel
ORDER BY month, acquisition_channel
```

**By rep (iPad-acquired only):**

```sql
WITH first_orders AS (
  SELECT customer_num,
         MIN(created_at) AS first_ecat_order_date
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND customer_num IS NOT NULL
    AND order_source = 'ipad'
  GROUP BY customer_num
  HAVING MIN(created_at) >= NOW() - INTERVAL '15 months'
)
SELECT
  o.rep_first_name || ' ' || o.rep_last_name AS rep,
  COUNT(DISTINCT fo.customer_num) AS new_ecat_buyers_acquired
FROM first_orders fo
JOIN orders o
  ON o.customer_num = fo.customer_num
  AND o.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND o.created_at = fo.first_ecat_order_date
  AND o.order_source = 'ipad'
WHERE o.rep_last_name IS NOT NULL
GROUP BY o.rep_first_name, o.rep_last_name
ORDER BY new_ecat_buyers_acquired DESC
```

**External claim rules**: First-time eCat orderer count by channel and rep. Never say "net-new customers." Never say "eCat Online-acquired buyers are net-new accounts."

---

### Q-44: Onboarding Velocity / Time-to-First-eCat-Order
**Maps to**: VM-44 | **Audience**: internal (non_runtime for external report) | **Status**: excluded from external scope | **Source**: Postgres MCP

> **Scope note**: Enrollment is intentionally excluded from the external report system. This query is retained for potential internal or specialized use only. Do not run it as part of the standard external report operator.

```sql
WITH accepted AS (
  SELECT
    ea.id AS applicant_id,
    ea.email,
    ea.customer_number,
    ea.created_at AS accepted_at
  FROM enrollment_applicants ea
  WHERE ea.organization_id = {{ORG_ID}}
    AND ea.status = 'accepted'
    AND ea.created_at >= NOW() - INTERVAL '12 months'
    AND ea.customer_number IS NOT NULL
),
first_ecat_order AS (
  SELECT
    customer_num,
    MIN(created_at) AS first_order_date
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND customer_num IS NOT NULL
  GROUP BY customer_num
)
SELECT
  COUNT(a.applicant_id) AS total_accepted,
  COUNT(fo.first_order_date) AS converted_to_first_ecat_order,
  COUNT(a.applicant_id) - COUNT(fo.first_order_date) AS not_yet_converted,
  ROUND(100.0 * COUNT(fo.first_order_date) / NULLIF(COUNT(a.applicant_id), 0), 1) AS conversion_pct,
  ROUND(AVG(EXTRACT(DAY FROM fo.first_order_date - a.accepted_at)) FILTER (WHERE fo.first_order_date IS NOT NULL), 0) AS median_days_to_first_ecat_order,
  COUNT(CASE WHEN fo.first_order_date <= a.accepted_at + INTERVAL '30 days' THEN 1 END) AS converted_within_30d,
  COUNT(CASE WHEN fo.first_order_date > a.accepted_at + INTERVAL '30 days'
              AND fo.first_order_date <= a.accepted_at + INTERVAL '60 days' THEN 1 END) AS converted_31_60d,
  COUNT(CASE WHEN fo.first_order_date > a.accepted_at + INTERVAL '60 days' THEN 1 END) AS converted_after_60d
FROM accepted a
LEFT JOIN first_ecat_order fo ON fo.customer_num = a.customer_number
  AND fo.first_order_date >= a.accepted_at
```

**External claim rules**: Acceptance-to-first-eCat-order conversion rates at 30/60-day windows. Median days-to-first-order. Never say "acceptance = eCat buyer." Never say "net-new customers."

---

### Q-49: Buyer-Level Repeat Purchase
**Maps to**: VM-49 | **Audience**: external | **Status**: conditional — requires buyer attribution in `portal_orders` | **Source**: Postgres MCP

**Gate check — confirm buyer attribution is present:**

```sql
SELECT
  COUNT(*) AS total_portal_orders,
  COUNT(buyer_name) AS orders_with_buyer_name,
  COUNT(customer_bill_to_number) AS orders_with_bill_to
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
LIMIT 1
```

**Repeat purchase rate (if buyer attribution confirmed):**

```sql
WITH first_portal_order AS (
  SELECT
    customer_bill_to_number AS buyer_id,
    buyer_name,
    MIN(order_date) AS first_order_date
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
    AND customer_bill_to_number IS NOT NULL
  GROUP BY customer_bill_to_number, buyer_name
),
subsequent_orders AS (
  SELECT
    po.customer_bill_to_number AS buyer_id,
    MIN(po.order_date) AS second_order_date
  FROM portal_orders po
  JOIN first_portal_order fpo ON po.customer_bill_to_number = fpo.buyer_id
    AND po.order_date > fpo.first_order_date
  WHERE po.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY po.customer_bill_to_number
)
SELECT
  COUNT(fpo.buyer_id) AS new_buyers_in_period,
  COUNT(so.second_order_date) AS returned_within_period,
  COUNT(CASE WHEN so.second_order_date <= fpo.first_order_date + INTERVAL '90 days' THEN 1 END) AS returned_within_90d,
  COUNT(CASE WHEN so.second_order_date <= fpo.first_order_date + INTERVAL '180 days' THEN 1 END) AS returned_within_180d,
  ROUND(100.0 * COUNT(CASE WHEN so.second_order_date <= fpo.first_order_date + INTERVAL '90 days' THEN 1 END)
    / NULLIF(COUNT(fpo.buyer_id), 0), 1) AS repeat_rate_90d
FROM first_portal_order fpo
LEFT JOIN subsequent_orders so ON so.buyer_id = fpo.buyer_id
```

**External claim rules**: Buyer repeat purchase rate where buyer attribution confirmed. Never apply to orgs without confirmed buyer attribution. `portal_orders` = ERP-synced total business — these are all-channel orders, not eCat-specific.

---

## Domain 4 — eCat Commerce Analytics

### Q-16: ERP Total Business Visibility
**Maps to**: VM-16 | **Audience**: external | **Status**: conditional (gate: portal_orders present) | **Source**: Postgres MCP

> **Semantic correction from prior version**: This query was previously titled "Buyer Self-Service Adoption (Portal Orders)" and framed `portal_orders` as buyer ordering activity. That interpretation is incorrect and must not be used.
>
> **Correct framing**: `portal_orders` = ERP-synced total business across all channels (eCat, phone, EDI, trade shows, showroom). It feeds the client's internal Sales Intelligence Dashboard. It is not buyer activity on a portal.

```sql
SELECT
  DATE_TRUNC('month', order_date)::date AS month,
  COUNT(*) AS total_erp_orders,
  COUNT(DISTINCT customer_bill_to_number) AS unique_accounts,
  ROUND(SUM(total_amount)::numeric, 2) AS total_erp_gmv,
  SUM(CASE WHEN order_origin = 'ECAT' THEN 1 ELSE 0 END) AS ecat_originated_orders,
  ROUND(SUM(CASE WHEN order_origin = 'ECAT' THEN total_amount ELSE 0 END)::numeric, 2) AS ecat_originated_gmv,
  SUM(CASE WHEN order_origin IN ('HPMKT','AMKT','LVMKT','DMKT','DROOM','AROOM','HPROOM') THEN 1 ELSE 0 END) AS market_orders
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC
```

**External claim rules**: Total ERP order volume across all channels. Order-origin breakdown (where `order_origin` is populated). Seasonality patterns from full business data. Never describe `portal_orders` as buyer self-service orders. Never say "buyers are ordering on the portal."

---

### Q-18: eCat Order Velocity & Trend (with ERP Context)
**Maps to**: VM-18 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**Part A — eCat orders:**

```sql
SELECT
  DATE_TRUNC('month', created_at)::date AS month,
  COUNT(*) AS total_ecat_orders,
  COUNT(CASE WHEN order_source = 'ipad' THEN 1 END) AS ipad_orders,
  COUNT(CASE WHEN order_source = 'server' THEN 1 END) AS ecat_online_orders,
  ROUND(SUM(total)::numeric, 2) AS ecat_gmv,
  ROUND(AVG(total)::numeric, 2) AS ecat_aov
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC
```

**Part B — ERP total context (run only when portal_orders present):**

```sql
SELECT
  DATE_TRUNC('month', order_date)::date AS month,
  COUNT(*) AS total_erp_orders,
  ROUND(SUM(total_amount)::numeric, 2) AS total_erp_gmv
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC
```

**Assembly**: Merge Parts A and B by month. Calculate eCat share (eCat orders / ERP total orders). Part A is always run; Part B only when `portal_orders` is confirmed present.

---

### Q-19: eCat Channel Mix Evolution
**Maps to**: VM-19 | **Audience**: external | **Status**: conditional (gate: has_cart = true AND server orders confirmed) | **Source**: Derived from Q-18 Part A

Channel mix is derived from Q-18 Part A output: `ecat_online_orders / total_ecat_orders` per month. Only include for accounts where `order_source = 'server'` orders are confirmed to exist. Do not surface for iPad-only clients.

---

### Q-20: eCat AOV Analysis
**Maps to**: VM-20 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  'All eCat Orders' AS dimension,
  COUNT(*) AS order_count,
  ROUND(AVG(total)::numeric, 2) AS avg_order_value,
  ROUND(SUM(total)::numeric, 2) AS total_ecat_gmv
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'

UNION ALL

SELECT
  'iPad Orders',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND order_source = 'ipad'

UNION ALL

SELECT
  'eCat Online Orders',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND order_source = 'server'

UNION ALL

SELECT
  'Quote Orders',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND order_type = 'Quote'
```

**External claim rules**: eCat AOV by channel and order type. Always qualify as eCat-channel only. Never say "your average deal size" without clarifying this is eCat-only.

---

### Q-21: eCat Order Type & Workflow Analysis
**Maps to**: VM-21 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  order_type,
  COUNT(*) AS orders,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct,
  ROUND(SUM(total)::numeric, 2) AS gmv,
  ROUND(AVG(total)::numeric, 2) AS avg_value
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
GROUP BY order_type
ORDER BY orders DESC
```

---

### Q-45: eCat Capture Rate vs. Total Business
**Maps to**: VM-45 | **Audience**: external | **Status**: conditional (gate: portal_orders present — do NOT run without denominator) | **Source**: Postgres MCP

```sql
WITH ecat_totals AS (
  SELECT
    SUM(total) AS ecat_gmv,
    COUNT(*) AS ecat_order_count
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at >= NOW() - INTERVAL '12 months'
),
erp_totals AS (
  SELECT
    SUM(total_amount) AS erp_gmv,
    COUNT(*) AS erp_order_count
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
)
SELECT
  e.ecat_order_count,
  p.erp_order_count,
  ROUND(100.0 * e.ecat_order_count / NULLIF(p.erp_order_count, 0), 1) AS ecat_order_capture_pct,
  ROUND(e.ecat_gmv::numeric, 2) AS ecat_gmv,
  ROUND(p.erp_gmv::numeric, 2) AS erp_gmv,
  ROUND(100.0 * e.ecat_gmv / NULLIF(p.erp_gmv, 0), 1) AS ecat_gmv_capture_pct,
  CASE
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.erp_gmv, 0) > 50 THEN 'Primary transaction system'
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.erp_gmv, 0) BETWEEN 25 AND 50 THEN 'Meaningful eCat channel; dual-system'
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.erp_gmv, 0) BETWEEN 10 AND 25 THEN 'Partial capture; eCat is growing'
    ELSE 'Enablement-heavy; eCat captures little of total volume'
  END AS ecat_posture
FROM ecat_totals e, erp_totals p
```

**External claim rules**: eCat order count and GMV share of total ERP business. "eCat processes X% of your total order volume." Never run without `portal_orders` present. The ERP denominator represents orders synced from your ERP — not all-channel total business should be presented as eCat-originated. Low capture rate is not a failure — it may reflect legitimate multi-channel business.

---

## Domain 5 — Product & Inventory Intelligence

### Q-37: Inventory × Sales Intelligence (OOS Top Sellers)
**Maps to**: VM-37 | **Audience**: external | **Status**: conditional (gate: sales_data + inventories both present) | **Source**: Postgres MCP

**ERP join guard (required)**: Only surface an item as a "best seller you can't sell" when it has confirmed ERP sales history (`amount_invoiced > 0` with a non-NULL result from the `sales_data` join). If the `sales_data` join returns NULL for `amount_invoiced`, the item has no confirmed ERP sales history and must NOT be labeled as a high-demand OOS item — it may be discontinued, archived, or low-velocity. This guard is enforced by requiring `sd.amount_invoiced > 0` in the WHERE clause below (NULL rows are excluded by `> 0` comparison).

```sql
SELECT
  sd.base_item_code AS item_code,
  p.category_code,
  p.collection_code,
  p.long_description AS item_description,
  ROUND(SUM(sd.amount_invoiced)::numeric, 2) AS total_erp_invoiced,
  SUM(sd.quantity_invoiced) AS total_qty_sold,
  COALESCE(i.qty_available, 0) AS qty_available,
  COALESCE(i.qty_on_hand, 0) AS qty_on_hand,
  COALESCE(i.qty_on_backorder, 0) AS qty_on_backorder,
  i.next_scheduled_receipt_date
FROM sales_data sd
LEFT JOIN inventories i
  ON i.base_item_code = sd.base_item_code
  AND i.organization_id = sd.organization_id
LEFT JOIN products p
  ON p.item_number = sd.base_item_code
  AND p.organization_id = sd.organization_id
  AND p.deleted = false
WHERE sd.organization_id = {{ORG_ID}}
  AND sd.amount_invoiced > 0          -- ERP join guard: only items with confirmed ERP sales history
  AND COALESCE(i.qty_available, 0) <= 0
GROUP BY sd.base_item_code, p.category_code, p.collection_code, p.long_description, i.qty_available, i.qty_on_hand, i.qty_on_backorder, i.next_scheduled_receipt_date
ORDER BY total_erp_invoiced DESC
LIMIT 20
```

**Required caveat when presenting**: "Based on today's inventory import. Inventory data reflects current state only — we cannot determine how long items have been out of stock."

**External claim rules**: "These historically high-volume items currently show zero available inventory." Never say "revenue at risk" without the inventory snapshot caveat. Never claim how long items have been out of stock. Never surface items with NULL ERP sales history as "best sellers" — they have no confirmed demand signal.

---

### Q-38a: Product Velocity Trend (eCat Orders via portal_order_items)
**Maps to**: VM-38a | **Audience**: external | **Status**: conditional (gate: portal_order_items present — ~52 orgs) | **Source**: Postgres MCP

```sql
SELECT
  poi.ecat_item_number AS item_code,
  p.long_description AS item_description,
  p.category_code,
  p.collection_code,
  DATE_TRUNC('month', po.order_date)::date AS month,
  SUM(poi.quantity_ordered) AS quantity_ordered,
  COUNT(DISTINCT po.order_number) AS order_count
FROM portal_order_items poi
JOIN portal_orders po ON po.order_number = poi.order_number
  AND po.organization_id = poi.organization_id
LEFT JOIN products p ON p.item_number = poi.ecat_item_number
  AND p.organization_id = poi.organization_id
  AND p.deleted = false
WHERE poi.organization_id = {{ORG_ID}}
  AND po.order_date >= NOW() - INTERVAL '6 months'
  AND poi.ecat_item_number IS NOT NULL
GROUP BY poi.ecat_item_number, p.long_description, p.category_code, p.collection_code, month
ORDER BY item_code, month
```

**Note on VM-38b**: `sales_data` has no `invoice_date` or `period` column (confirmed in schema discovery). VM-38b (full-channel product velocity trend) requires a one-column engineering addition. Do not attempt a workaround using `est_ship_date` — that field is for pending orders only.

**External claim rules**: eCat product order velocity trend via `portal_order_items`. Accelerating vs. declining items by order count. Never claim full-channel velocity — this is eCat-side line items only.

---

### Q-39: Line Analysis by Category & Collection
**Maps to**: VM-39 | **Audience**: external | **Status**: conditional (gate: sales_data present) | **Source**: Postgres MCP

**By category:**

```sql
SELECT
  p.category_code,
  ROUND(SUM(sd.amount_invoiced)::numeric, 2) AS total_erp_sales,
  SUM(sd.quantity_invoiced) AS total_qty,
  COUNT(DISTINCT sd.base_item_code) AS item_count,
  ROUND(SUM(sd.amount_invoiced)::numeric / NULLIF(COUNT(DISTINCT sd.base_item_code), 0), 2) AS sales_per_item
FROM sales_data sd
JOIN products p ON p.item_number = sd.base_item_code
  AND p.organization_id = sd.organization_id
  AND p.deleted = false
WHERE sd.organization_id = {{ORG_ID}}
  AND sd.amount_invoiced > 0
  AND p.category_code IS NOT NULL AND p.category_code != ''
GROUP BY p.category_code
ORDER BY total_erp_sales DESC
```

**By collection:**

```sql
SELECT
  p.collection_code,
  ROUND(SUM(sd.amount_invoiced)::numeric, 2) AS total_erp_sales,
  SUM(sd.quantity_invoiced) AS total_qty,
  COUNT(DISTINCT sd.base_item_code) AS item_count,
  ROUND(SUM(sd.amount_invoiced)::numeric / NULLIF(COUNT(DISTINCT sd.base_item_code), 0), 2) AS sales_per_item
FROM sales_data sd
JOIN products p ON p.item_number = sd.base_item_code
  AND p.organization_id = sd.organization_id
  AND p.deleted = false
WHERE sd.organization_id = {{ORG_ID}}
  AND sd.amount_invoiced > 0
  AND p.collection_code IS NOT NULL AND p.collection_code != ''
GROUP BY p.collection_code
ORDER BY total_erp_sales DESC
LIMIT 25
```

---

### Q-40: Regional Sales Distribution
**Maps to**: VM-40 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

```sql
SELECT
  c.billing_state AS state,
  COUNT(DISTINCT c.id) AS customer_count,
  COUNT(DISTINCT o.id) AS ecat_order_count,
  ROUND(SUM(o.total)::numeric, 2) AS ecat_gmv
FROM orders o
JOIN customers c ON c.code = o.customer_num AND c.organization_id = o.organization_id
WHERE o.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
  AND o.created_at >= NOW() - INTERVAL '12 months'
  AND c.billing_state IS NOT NULL AND c.billing_state != ''
GROUP BY c.billing_state
ORDER BY ecat_gmv DESC
LIMIT 20
```

**Regional × Category cross-tab (requires sales_data):**

```sql
SELECT
  c.billing_state AS state,
  p.category_code,
  ROUND(SUM(sd.amount_invoiced)::numeric, 2) AS erp_sales,
  SUM(sd.quantity_invoiced) AS qty
FROM sales_data sd
JOIN products p ON p.item_number = sd.base_item_code AND p.organization_id = sd.organization_id AND p.deleted = false
JOIN customers c ON c.code = sd.bill_to_code AND c.organization_id = sd.organization_id
WHERE sd.organization_id = {{ORG_ID}}
  AND sd.amount_invoiced > 0
  AND c.billing_state IS NOT NULL AND c.billing_state != ''
  AND p.category_code IS NOT NULL AND p.category_code != ''
GROUP BY c.billing_state, p.category_code
ORDER BY erp_sales DESC
LIMIT 50
```

---

### Q-42: New Item Performance
**Maps to**: VM-42 | **Audience**: external | **Status**: conditional (gate: new_item flag + sales_data both present) | **Source**: Postgres MCP

```sql
SELECT
  p.collection_code,
  COUNT(*) AS new_item_count,
  ROUND(SUM(COALESCE(sd.amount_invoiced, 0))::numeric, 2) AS total_erp_sales,
  SUM(COALESCE(sd.quantity_invoiced, 0)) AS total_qty_sold,
  ROUND(SUM(COALESCE(sd.amount_invoiced, 0))::numeric / NULLIF(COUNT(*), 0), 2) AS sales_per_new_item
FROM products p
LEFT JOIN sales_data sd ON sd.base_item_code = p.item_number AND sd.organization_id = p.organization_id
WHERE p.organization_id = {{ORG_ID}}
  AND p.deleted = false
  AND p.new_item = true
GROUP BY p.collection_code
ORDER BY total_erp_sales DESC
```

**External claim rules**: New item sell-through by collection. Per-item productivity for new introductions. Collections with near-zero sell-through. Never attribute poor sell-through to product quality alone.

---

## Domain 6 — Cross-Instance Benchmarking

### Q-CI-01: Org Summary Lookup
**Maps to**: VM-23, VM-24, VM-27 (context only) | **Audience**: shared | **Status**: live | **Source**: BigQuery `insightful_product`

```sql
SELECT *
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

**Note**: `org_summary.health_score` is the legacy 0–1.0 scale precursor. It is not the current authoritative health score (Health V2 is). For the external report, `org_summary` is used for config flags (`has_clicky_portal`, `recurring_services`, etc.) — not for health score.

---

### Q-CI-02: Peer Comparison (VM-23, VM-25)
**Maps to**: VM-23, VM-25 | **Audience**: external | **Status**: live | **Source**: BigQuery `insightful_product`

```sql
SELECT org_shortname, org_name, segment, peer_standing,
       orders_vs_peer_pct, logins_vs_peer_pct, mrr_vs_peer_pct,
       peer_orders_median, peer_logins_median, peer_mrr_median
FROM `supercat-data-pipeline.insightful_product.segment_peer_comparison`
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

**External claim rules**: Client metrics vs. anonymized peer medians and percentiles. "You're above/below median for your plan type." Never expose internal segment labels ("Platform-Embedded," "Commerce-Active," "Catalog-Focused"). Never name specific peer clients.

---

### Q-CI-03: Feature Adoption Benchmarking (VM-24)
**Maps to**: VM-24 | **Audience**: external | **Status**: live | **Source**: BigQuery `insightful_product`

```sql
SELECT org_shortname, org_name, segment, feature_depth,
       has_clicky_portal, arr   -- arr_band removed 2026-06-03: not a column in org_summary
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

For adoption rates across peers, combine with `segment_benchmarks_monthly`:

```sql
SELECT *
FROM `supercat-data-pipeline.insightful_product.segment_benchmarks_monthly`
WHERE segment = '{{SEGMENT}}'
ORDER BY benchmark_month DESC
LIMIT 3
```

**Note on external claim**: When using `segment` values from BigQuery (`Platform-Embedded`, `Commerce-Active`, `Catalog-Focused`), these are internal labels and must never appear in external client-facing text. For external delivery, translate to bundle names or describe what the client has.

---

### Q-CI-04: Growth Trajectory (VM-25)
**Maps to**: VM-25 | **Audience**: external | **Status**: conditional (requires 2+ monthly snapshots — first available May 2026) | **Source**: BigQuery `insightful_product`

```sql
SELECT *
FROM `supercat-data-pipeline.insightful_product.segment_benchmarks_monthly`
WHERE segment = '{{SEGMENT}}'
ORDER BY benchmark_month DESC
LIMIT 6
```

**Note**: If fewer than 2 monthly snapshots exist, do not attempt time-series trending. Current-period snapshot only.

---

### Q-CI-05, Q-CI-06: Top Performers & Best Practices (VM-26)
**Maps to**: VM-26 | **Audience**: external | **Status**: live | **Source**: BigQuery `insightful_product`

```sql
SELECT segment, org_shortname, org_name, arr,
       mp_submit_order, mp_total_logins, feature_depth,
       rank_by_orders, rank_by_logins
FROM `supercat-data-pipeline.insightful_product.top_performers_by_segment`
WHERE segment = '{{SEGMENT}}'
ORDER BY rank_by_orders
```

**External claim rules**: "Top performers on your plan type share these behavioral patterns." Anonymized benchmarks only. Never name specific top-performing clients. Never use internal segment labels in client-facing text.

---

## Domain 7 — Internal Only

> **All Domain 7 VMs (VM-27, VM-28, VM-29, VM-30, VM-48) are internal_only. Queries in this section are for CS/internal use only — they must not appear in external report output.**

### Q-27: Account Health (Internal — VM-27)
**Maps to**: VM-27 | **Audience**: internal | **Status**: live — Use Health V2 operator output, not this legacy composite

The legacy composite health scoring query from the old library is **superseded by Health V2**. Do not maintain a parallel health score formula. Run the Health V2 operator (`SuperCat 4.0/Health V2/`) to get authoritative health scores.

For historical context only, `org_summary.health_score` (0–1.0 scale) is available via Q-CI-01.

### Q-HS-01 through Q-HS-06: HelpScout Support Queries (Internal — VM-30)
**Maps to**: VM-30 | **Audience**: internal | **Status**: live | **Source**: BigQuery `helpscout`

These queries are preserved from the prior library with no semantic changes needed. They are internal-only. The optional external-safe framing of VM-30 is deferred to Phase 2.

See prior library for full Q-HS-01 through Q-HS-06 SQL. Key target: `helpscout.conversations` + `helpscout.customers` joined on `primaryCustomer.id`.

---

## Domain 8 — Portal & Demand-Side Intelligence (Clicky — Gate: has_clicky = true)

> All Domain 8 queries require `has_clicky = true`. Replace `{{CLICKY_PREFIX}}` with the org's Clicky prefix from `org_summary.clicky_prefix`. If `has_clicky = false`, do not run these queries and do not mention Clicky anywhere in the external report.

### Clicky Daily Metrics — Required Deduplication Guard

**IMPORTANT**: Clicky daily_metrics tables may contain multiple rows per date due to pipeline duplication (observed: up to 11 rows per date in production). Raw `SUM()` or `COUNT()` across rows without deduplication will significantly overcount traffic metrics.

**All queries against `{CLICKY_PREFIX}_daily_metrics` MUST use `GROUP BY date` with `MAX()` aggregation to deduplicate before rolling up to month or summary level.** Never aggregate directly from raw rows.

**Required dedup CTE pattern — use this as the base for all daily_metrics queries:**

```sql
WITH daily_dedup AS (
  SELECT
    date,
    MAX(visitors_unique) AS visitors_unique,
    MAX(actions_pageviews) AS actions_pageviews,
    MAX(time_average_seconds) AS time_average_seconds
    -- Add additional MAX(column) fields as needed per query
    -- DO NOT include bounce_rate — see bounce_rate exclusion note below
  FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
  GROUP BY date
)
```

**`bounce_rate` exclusion (permanent until resolved)**: The `bounce_rate` column in Clicky daily_metrics tables returns values at an unconfirmed scale (observed values: 1,100–4,300 in production — inconsistent with a 0–1 or 0–100 scale). Do not include `bounce_rate` in any query, any report section, or any metric card. This exclusion remains in effect until the column scale is confirmed and documented by the team responsible for the Clicky BigQuery pipeline.

---

### Q-CL-01: Portal Traffic Health (VM-31)
**Maps to**: VM-31 | **Audience**: external | **Status**: conditional (has_clicky) | **Source**: BigQuery Clicky

```sql
WITH daily_dedup AS (
  SELECT
    date,
    MAX(visitors_unique) AS visitors_unique,
    MAX(actions_pageviews) AS actions_pageviews,
    MAX(time_average_seconds) AS time_average_seconds
  FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
  GROUP BY date
)
SELECT
  DATE_TRUNC(date, MONTH) AS month,
  AVG(visitors_unique) AS avg_daily_unique_visitors,
  SUM(actions_pageviews) AS total_pageviews,
  AVG(time_average_seconds) AS avg_session_seconds
FROM daily_dedup
GROUP BY month
ORDER BY month DESC
```

**Note**: `bounce_rate` is excluded — see Domain 8 header note. Column names confirmed in schema discovery: `visitors_unique`, `actions_pageviews`, `time_average_seconds`.

### Q-CL-02: Portal Content Performance (VM-32)
**Maps to**: VM-32 | **Audience**: external | **Status**: conditional (has_clicky + page data available) | **Source**: BigQuery Clicky

```sql
SELECT page, SUM(pageviews) AS total_pageviews, SUM(unique_visitors) AS unique_visitors
FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_pages`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
GROUP BY page
ORDER BY total_pageviews DESC
LIMIT 25
```

### Q-CL-03: Geographic Demand Map (VM-33)
**Maps to**: VM-33 | **Audience**: external | **Status**: conditional (has_clicky) | **Source**: BigQuery Clicky

**Schema note — `_regions` column names vary by org.** Before running, check the actual column names:

```sql
SELECT column_name
FROM `supercat-data-pipeline`.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = '{{CLICKY_PREFIX}}_regions'
ORDER BY ordinal_position
```

Two known schema variants have been observed in production:
- **Standard schema**: columns `region`, `visitors`, `country`, `date` — use the standard query below.
- **Alternative schema** (observed on orgs with `_eol_trial` or similar prefix variants): columns `title`, `value`, `date` — `title` holds the region name, `value` holds the visitor count as a string. Use the alternative query below. There is no `country` column in this variant; apply no country filter.

*Standard schema query:*
```sql
SELECT region AS state, SUM(visitors) AS total_visitors
FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_regions`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
  AND country = 'US'
GROUP BY region
ORDER BY total_visitors DESC
LIMIT 20
```

*Alternative schema query (title/value variant):*
```sql
SELECT title AS region, SUM(CAST(value AS INT64)) AS total_visitors
FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_regions`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
GROUP BY title
ORDER BY total_visitors DESC
LIMIT 20
```

### Q-CL-04: Visitor Organization Identification (VM-34)
**Maps to**: VM-34 | **Audience**: external | **Status**: conditional (has_clicky; accuracy varies) | **Source**: BigQuery Clicky

```sql
SELECT organization, SUM(visitors) AS total_visitors
FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_organizations`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
GROUP BY organization
ORDER BY total_visitors DESC
LIMIT 30
```

### Q-CL-05: Traffic Source Intelligence (VM-35)
**Maps to**: VM-35 | **Audience**: external | **Status**: conditional (has_clicky) | **Source**: BigQuery Clicky

```sql
SELECT source AS traffic_source, SUM(visitors) AS total_visitors
FROM `supercat-data-pipeline.clicky_analytics.{{CLICKY_PREFIX}}_traffic_sources`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
GROUP BY source
ORDER BY total_visitors DESC
```

---

## Preflight / Configuration Queries

### Q-PC-01: Product Configuration Check (BigQuery)
**Audience**: shared | **Status**: live | **Run before any gating decisions**

```sql
SELECT
  org_shortname, org_name, recurring_services, feature_depth,
  has_clicky_portal, clicky_prefix,
  order_configured_item, view_kit, order_kit,
  access_sales_portal
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname = '{{ORG_SHORTNAME}}'
```

**Derive flags from this output**:
- `has_clicky` = `has_clicky_portal = true`
- `has_cart` = `recurring_services` contains `eCat Online - B2B Cart`
- `has_portal` = `recurring_services` contains `eCat Online - Portal`
- `has_cpq` = `recurring_services` contains `Configurable` OR `order_configured_item > 0`

**Then confirm portal_orders presence (Postgres MCP):**

```sql
SELECT COUNT(*) AS portal_order_count FROM portal_orders WHERE organization_id = {{ORG_ID}}
```

**And portal_order_items presence (for VM-38a gating):**

```sql
SELECT COUNT(*) AS portal_order_items_count FROM portal_order_items WHERE organization_id = {{ORG_ID}}
```

### Instance Summary Query
**Audience**: shared | **Status**: live | **Source**: Postgres MCP

Run this for any org as a quick diagnostic before a report run:

```sql
SELECT
  o.id AS org_id,
  o.shortname,
  o.name,
  (SELECT COUNT(*) FROM products WHERE organization_id = o.id AND deleted = false) AS active_products,
  (SELECT COUNT(*) FROM customers WHERE organization_id = o.id) AS total_erp_customers,
  (SELECT COUNT(*) FROM org_users WHERE organization_id = o.id AND disabled = false) AS active_users,
  (SELECT COUNT(*) FROM orders WHERE organization_id = o.id AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '12 months') AS ecat_orders_12mo,
  (SELECT ROUND(SUM(total)::numeric, 2) FROM orders WHERE organization_id = o.id
    AND is_submitted = true AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '12 months') AS ecat_gmv_12mo,
  (SELECT COUNT(*) FROM portal_orders WHERE organization_id = o.id) AS portal_order_count,
  (SELECT COUNT(*) FROM portal_order_items WHERE organization_id = o.id) AS portal_order_items_count,
  (SELECT COUNT(*) FROM sales_data WHERE organization_id = o.id) AS sales_data_rows,
  (SELECT COUNT(*) FROM inventories WHERE organization_id = o.id) AS inventory_rows,
  (SELECT COUNT(*) FROM smart_stacks WHERE organization_id = o.id) AS smart_stacks,
  (SELECT COUNT(*) FROM shared_resources WHERE organization_id = o.id) AS shared_resources,
  (SELECT COUNT(*) FROM enrollment_applicants WHERE organization_id = o.id) AS enrollment_applicants,
  (SELECT COUNT(*) FROM import_events WHERE organization_id = o.id) AS import_events,
  (SELECT COUNT(*) FROM login_events WHERE organization_id = o.id) AS login_events
FROM organizations o
WHERE o.id = {{ORG_ID}}
```

---

## Query Status Summary

| Query | VM | Audience | Status |
|-------|-----|----------|--------|
| Q-01 | VM-01 | external | live |
| Q-02 | VM-02 | external | live (derived) |
| Q-03 | VM-03 | external | live (derived) |
| Q-04 | VM-04 | external | live |
| Q-05 | VM-05 | external | live |
| Q-06 | VM-06 | external | live |
| Q-07 | VM-07 | external | live |
| Q-08 | VM-08 | external | live |
| Q-09 | VM-09 | external | live |
| Q-10 | VM-10 | external | live |
| Q-11 | VM-11 | external | live |
| Q-12 | VM-12 | external | live |
| Q-13 | VM-13 | external | live |
| Q-14 | VM-14 | external | live |
| Q-15 | VM-15 | internal only | excluded from external scope |
| Q-16 | VM-16 | external | conditional (portal_orders) — **semantics corrected** |
| Q-17 | VM-17 | external | live |
| Q-18 | VM-18 | external | live |
| Q-19 | VM-19 | external | conditional (has_cart) — derived |
| Q-20 | VM-20 | external | live |
| Q-21 | VM-21 | external | live |
| Q-22 | VM-22 | external | live |
| Q-37 | VM-37 | external | conditional (sales_data + inventories) |
| Q-38a | VM-38a | external | conditional (portal_order_items) |
| Q-38b | VM-38b | — | pending_engineering (no invoice_date on sales_data) |
| Q-39 | VM-39 | external | conditional (sales_data) |
| Q-40 | VM-40 | external | live |
| Q-41 | VM-41 | external | live |
| Q-42 | VM-42 | external | conditional (new_item + sales_data) |
| Q-43 | VM-43 | external | live |
| Q-44 | VM-44 | internal only | excluded from external scope |
| Q-45 | VM-45 | external | conditional (portal_orders — no denominator-less fallback) |
| Q-46 | VM-46 | external | conditional (Postgres + Mixpanel) |
| Q-47 | VM-47 | external | conditional (Postgres metadata live; per-stack Mixpanel pending_query) |
| Q-49 | VM-49 | external | conditional (portal_orders buyer attribution) |
| Q-50 | VM-50 | external | conditional (Postgres metadata live; per-doc Mixpanel pending_query) |
| Q-CI-01 | VM-23+ | shared | live |
| Q-CI-02 | VM-23, VM-25 | external | live |
| Q-CI-03 | VM-24 | external | live |
| Q-CI-04 | VM-25 | external | conditional (2+ snapshots) |
| Q-CI-05/06 | VM-26 | external | live |
| Q-27 | VM-27 | internal | superseded by Health V2 |
| Q-HS-01—06 | VM-30 | internal | live |
| Q-CL-01—05 | VM-31—35 | external | conditional (has_clicky) |
