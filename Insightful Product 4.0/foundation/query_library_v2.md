# External Report Query Library — V2 (commerce-provenance + economics + rep-Phase-B; working canonical)

> **V2 STATUS (updated 2026-06-29)**: This is the **working canonical library**. It began as the 2026-06-25 staged merge of the commerce-provenance fixes (`commerce_provenance_queries.md`, `commerce_provenance_audit.md`) and has since absorbed **Domain 10 — Selling & Customer Economics** (`Q-ECON-00/LEAK/RETURNS/NETREV/TERMS/LEADTIME/CARRIER`, `Q-SELL-QC`; hardened on a 22-org live cohort, 2026-06-29 — **extended 2026-06-30** with the previously-pending C-series set `Q-ECON-CONC/QUALITY/SEASON/PACE/MOMENTUM/LUMP/NRR/CONTRIB` + the internal `Q-48` HubSpot query, all live-smoke-tested on cci/cfg) and the **Rung-3 rep Phase-B fixes** (`Q-63/64/65` → native `mixpanel.events`, `Q-69` → `submit_date`, `Q-70` → `user_types`/`last_ipad_login_at`; applied + live-validated). Pre-merge snapshot: `query_library_BACKUP_2026-06-25.md`; per-change tags `<!-- CHANGED v2: ... -->`; full log in `query_library_v2_CHANGELOG.md`. **Validation basis**: the Sales Portal dashboard is NOT ground truth (it reads the same source rows we do), so validation is a **source-completeness audit** (`commerce_validation_worksheet.md`) — formula correctness is proven from warehouse code, and the real gate is feed completeness (freshness/coverage/returns), encoded in `Q-PROV-00`/`Q-ECON-00`.
>
> **Core change**: "total business" is no longer `SUM(portal_orders.total_amount)`. It is now invoiced sales from `portal_invoices` (`net_amount`, line-total fallback), selected per org by the Commerce Provenance Preflight (Q-PROV-00). This matches what the client sees in their own Sales Portal. Rationale + live evidence: `commerce_provenance_audit.md`.

> **Provenance authority (Tier 0)**: [`provenance_spine.md`](provenance_spine.md) is the canonical definition of *how truth/confidence is established* — ERP-truth axiom, re-keying distortion, origin taxonomy, capture-vs-attribution, confidence tiers, the gate catalog (`Q-PROV-00`, `Q-CHAN-00`, `FEED_COMPLETENESS`, eCat-SALE, date clamps, `$5M` cap, `invoiced ≠ collected`), and the identity-resolution rules (rep / customer-parent / territory / product / customer-type). **This library is the implementation layer (Tier 2): it carries the SQL bodies; the Spine carries the meaning and the behavior.** When a gate's behavior is in question, the Spine wins.
> **Status**: Working canonical (post-2026-06-29). Schema-grounded — base schema audited 2026-04-06, extended by the 2026-06-25 commerce-provenance and 2026-06-29 economics/rep-Phase-B runs.
> **Semantic authority (capability / not runtime)**: [`capability/value_moment_catalog.md`](capability/value_moment_catalog.md) (**v4.2** — roadmap shelf; see its Domain-9 **Query-ID Reconciliation** table). Do not treat the VM catalog as what `./run.sh` executes — see [`WHAT_ACTUALLY_RUNS.md`](WHAT_ACTUALLY_RUNS.md).
> **Schema basis**: Live schema discovery run 2026-04-06 against production Postgres MCP.
> **Audience tags**: Each query tagged `external`, `internal`, or `shared`.
> **MCP targets**: `user-supercat-postgres-vpn` for Postgres queries; `user-bigquery-admin` for BigQuery queries (migrated 2026-06-03 from the legacy read-only `user-bigquery-vpn`/Weld; native `supercat-data-pipeline` datasets). The admin `query` tool takes **`sql`** and has no `max_results` — bound rows with SQL `LIMIT`. Canonical warehouse reference: `/BIGQUERY_ADMIN_REFERENCE.md`.

---

## LIVE vs BACKLOG — what the pipeline actually runs

> **Read this first.** This library documents ~120 queries. The shipped factory
> runs **24 query IDs** (`pipeline/config.py` `QUERIES_ALL`); every other query
> below is **BACKLOG** — documented/reference SQL the pipeline does not execute.
> The runtime ground truth is [`WHAT_ACTUALLY_RUNS.md`](WHAT_ACTUALLY_RUNS.md).
>
> Of the 24 live IDs, **20 have their SQL sourced from THIS file** by
> `pipeline/cache.extract_sql()`. The other 4 live IDs are sourced elsewhere and
> are **not defined here**: `RP-2`, `RS-01` (in `operators/rep_copilot_operator.md`)
> and `S1`, `C2` (in `foundation/selling_customer_exception_layer.md`).
>
> Anything not in this table is BACKLOG. Do not treat a query's presence in this
> file as evidence it runs — presence in `config.QUERIES_ALL` is the only test.

**LIVE — sourced from this library (20):**

| Query ID | Stage | Runs for |
|---|---|---|
| `Q-ECON-00` | preflight | economics preflight → `COMMERCE_CONFIDENCE`, `report_through_date`, eCat confirmed GMV |
| `Q-CHAN-00` | preflight | channel availability + eCat reconciliation |
| `Q-CHAN-06` | preflight | eCat-SALE confirmed-ratio pre-check (F1 blank-default share) |
| `Q-ECON-LEAK` | gather | org-wide + per-rep leakage (§6 cards) |
| `Q-ECON-CONC` | gather | customer concentration (top-1 / top-10 / HHI) |
| `Q-ECON-NRR` | gather | same-base retention |
| `Q-ECON-CONTRIB` | gather | top-15 by $ contribution (lifters/decliners) |
| `Q-CHAN-10` | gather | channel mix by canonical channel (LTM $) |
| `Q-CHAN-05` | gather | eCat vs non-eCat split |
| `Q-PROD-TOP` | gather | top items LTM |
| `Q-PROD-FAMILY` | gather | family rollups by collection (LTM + YoY) |
| `Q-CROSS-SELL` | gather | anchor-SKU dealers missing a target family |
| `Q-DEALER-COHORT` | gather | dealer cohort flow + cadence + same-base lift |
| `Q-08` | platform | data freshness monitor |
| `Q-09` | platform | import health & sync reliability |
| `Q-10` | platform | feature enablement gap |
| `Q-11` | platform | configuration completeness |
| `Q-R1` | platform | rep activity & cadence (behavior floor) |
| `Q-R2` | platform | coverage / territory penetration |
| `Q-R4` | platform | quote→submit discipline |

**LIVE — sourced from other docs (4, not defined here):** `RP-2`, `RS-01`
(rep_copilot_operator.md); `S1`, `C2` (selling_customer_exception_layer.md).

**BACKLOG:** every other query documented in this file (the ~95 not listed
above). Reference/roadmap SQL — not executed by the current pipeline.

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
| `portal_invoices` | `id`, `organization_id`, `invoice_number`, `invoice_date` (date, NOT NULL), `order_number`, `rep_number`, `customer_bill_to_number`, `customer_bill_to_name`, `customer_bill_to_state`, `net_amount`, `total_amount`, `discount_amount`, `freight_amount`, `tax_amount` | <!-- CHANGED v2: added --> **The invoiced-sales table (`invoice_data.csv`).** `net_amount` = client-facing invoiced total (negative for credit memos) and is the basis of "total business." Header `total_amount` is NOT the sales figure. **No `rep_name` column** (orders only) — invoices carry only `rep_number`. |
| `portal_invoice_items` | `id`, `organization_id`, `invoice_number`, `item_number`, `ecat_item_number`, `description`, `quantity_invoiced`, `quantity_ordered`, `quantity_returned`, `unit_price`, `unit_price_discount`, `extended_price_discount`, `line_number` | <!-- CHANGED v2: added --> Join to `portal_invoices` on `invoice_number` + `organization_id`. Line amount = `quantity_invoiced × (unit_price − COALESCE(unit_price_discount,0)) − COALESCE(extended_price_discount,0)`. In the Sales Portal warehouse these are prorated so each invoice's lines sum to its header `net_amount`. |
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

### Provenance Constants & Canonical Guardrails (single source of truth)
<!-- CHANGED v2: added (hardening 2026-06-25). One place for the magic numbers and the canonical eCat-SALE filter. If you change a value here, update every query that uses it AND the goldens in commerce_regression_cohort.sql. The linter commerce_guardrail_check.sh enforces that the values below match what the queries actually use. -->

These constants are referenced (by value) across the commerce queries below. They are collected here so a change is deliberate and reviewable, not scattered. Each query that uses one carries an inline value; `commerce_guardrail_check.sh` asserts the inline values match this block.

| Constant | Value | Used by | Meaning |
|---|---|---|---|
| `ECAT_SALE_FILTER` | see canonical block in "eCat SALES = confirmed orders only" just below | every `<!-- ECAT-NUMERATOR -->` query | confirmed-only eCat sales (the FAL guardrail) |
| `PARTIAL_FEED_RATIO` | `1.05` | Q-PROV-00, Q-CHAN-05, VM-45 sanity gate | confirmed eCat > 1.05x invoiced total -> partial feed -> SUPPRESS/PARTIAL |
| `STALE_DAYS` | `45` | Q-PROV-00 (`REPORT_THROUGH_DATE`) | days since last invoice > 45 -> feed stale -> PARTIAL + cap window |
| `ORDER_CAP` | `5000000` | every `orders.total` / `portal_orders.total_amount` sum | per-row sanity cap (drops corrupt mega-rows) |
| `CHAN_GATE` | `attributed_dollars >= 60% AND distinct_origins >= 2 AND booked_rows >= 25` | Q-CHAN-00 | below this -> CHANNEL_CONFIDENCE = NONE -> suppress channel section |
| `ECAT_RECON_BAND` | `0.80 .. 1.25` | Q-CHAN-00, Q-CHAN-20 | origin eCat / confirmed eCat inside band -> RELIABLE; above -> OVER-TAG; below -> UNDER-TAG |
| `DATE_CLAMP` | `DATE '2010-01-01' .. CURRENT_DATE + INTERVAL '90 days'` | every `order_date` / `invoice_date` filter | drops corrupt far-past/future dates |

> **Marker convention**: any query whose eCat dollar figure is a **sales/GMV/capture numerator** is tagged `<!-- ECAT-NUMERATOR -->` immediately above its ```sql``` fence. The linter requires every such block to contain the canonical eCat-SALE filter, byte-identical (an optional `o.` table alias is the only permitted variation). Activity/count queries are intentionally NOT tagged.

### Orders table
All queries touching `orders` must use:
```sql
AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
```
The `is_marked_deleted` column is nullable — `NULL` means not deleted. Using `= false` alone silently drops valid orders.

### eCat SALES = confirmed orders only (required for any GMV/sales/capture claim)
<!-- CHANGED v2: added (pilot-validated 2026-06-25) -->
`is_submitted = true` is NOT enough to call an eCat order a sale. `orders.order_type` includes pipeline/non-sale states that must be excluded from any **eCat sales / GMV / capture / penetration** dollar figure:
```sql
-- eCat-SALE filter (apply to every eCat GMV/sales numerator):
AND COALESCE(NULLIF(TRIM(order_type), ''), 'Confirmed') NOT IN
    ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
```
- Keeps `Confirmed`, `Confirmed - Display`, and blank/untyped (treated as confirmed). Removes quotes, holds-for-confirmation, proformas, wishlists, estimates, test orders.
- **Why**: without this, quotes are reported as eCat sales. Pilot magnitudes: `fal` $37.9M → $0.98M (97% quotes), `sccon` −88%, `sc` −69%, `clli` −84%. This is the FAL failure mode.
- **Scope**: apply to eCat **sales/GMV** metrics (Q-18 Part A GMV, Q-20 AOV, Q-45 capture numerator, Q-51/Q-52/Q-54 eCat GMV). Do NOT apply to pure **activity/usage** counts (logins, orders-created velocity) where pipeline activity is legitimately in scope — but label those "activity," never "sales."
- **Blank-type rule** (for the 100-org rollout): if an org has blank `order_type` AND any `Quote` rows, flag it in Q-PROV-00 for manual review before trusting its eCat sales (the blank-as-confirmed assumption is unsafe there). No cohort org had blanks.

### Portal date sanity (required)
<!-- CHANGED v2: added -->
All queries touching `portal_orders.order_date` or `portal_invoices.invoice_date` must clamp to a plausible window:
```sql
AND order_date   BETWEEN DATE '2010-01-01' AND CURRENT_DATE + INTERVAL '90 days'   -- portal_orders
AND invoice_date BETWEEN DATE '2010-01-01' AND CURRENT_DATE + INTERVAL '90 days'   -- portal_invoices
```
Corrupt dates exist in production (e.g. `clm` order date year 9380 / invoice 4107, `jyc` invoice 2032, `fsf` order 2028). Without this clamp they poison `MAX(date)` freshness gates and `DATE_TRUNC` period windows. The 90-day forward slack preserves legitimately future-dated ship/invoice rows.

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
<!-- CHANGED v2: denominator is now INVOICED total business, not portal_orders.total_amount. The old "Gate 1: portal_orders_gmv > ecat_gmv" was a defect — for invoice-dominant orgs (e.g. bcf) the order-header total is a tiny fraction of real sales, so eCat GMV exceeded it and capture rate was silently skipped despite a healthy 30-39% real rate. -->
Run Q-PROV-00 first. Then compute LTM eCat GMV and LTM **invoiced total business** (`SUM(net_amount)` over LTM) and apply:
1. **Provenance gate**: `TOTAL_BUSINESS_SOURCE = 'INVOICES'` (preferred) or `'ORDERS'`. If `SALES_DATA` or `NONE`, skip Q-45 — no period-level denominator.
2. **Sanity gate**: `ecat_gmv <= 1.05 × total_business` — if eCat GMV exceeds invoiced total business by >5%, the invoice feed is partial/lagging; skip Q-45 and note it (do NOT fall back to the order-header total).
3. **Materiality note (not a skip)**: if `ecat_gmv < 0.05 × total_business`, still report, but frame as early-stage adoption rather than a failure.

If gate 1 or 2 fails, do not run Q-45. Do not substitute a denominator-less eCat GMV statement. Note the skip reason and `COMMERCE_CONFIDENCE` in the Appendix.

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
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL) AND o.total < 5000000
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
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
     AND customer_num IS NOT NULL) AS total_ever_ordered_via_ecat,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
     AND customer_num IS NOT NULL
     AND created_at >= NOW() - INTERVAL '12 months') AS active_12mo,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
     AND customer_num IS NOT NULL
     AND created_at >= NOW() - INTERVAL '6 months') AS active_6mo,
  (SELECT COUNT(DISTINCT customer_num)
   FROM orders
   WHERE organization_id = {{ORG_ID}}
     AND is_submitted = true
     AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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

<!-- ECAT-NUMERATOR -->
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
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

<!-- ECAT-NUMERATOR -->
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
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
  AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
  AND created_at > NOW() - INTERVAL '12 months'
  AND customer_num IS NOT NULL
GROUP BY customer_num, bill_to_company_name
HAVING COUNT(*) >= 3
ORDER BY ecat_order_count DESC
LIMIT 20
```

**External claim rules**: eCat reorder frequency and trend per buyer. Always qualify as eCat-channel only. Never claim total-business reorder frequency.

---

### Q-14b: Account Velocity Deceleration Detection
**Maps to**: VM-14b | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS`) | **Source**: Postgres MCP

Detects accounts whose ordering frequency is stretching beyond their historical average — an early warning signal (60-90 days) before revenue actually drops.

```sql
WITH order_intervals AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    order_date,
    order_date - LAG(order_date) OVER (
      PARTITION BY customer_bill_to_number ORDER BY order_date
    ) AS interval_days
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '18 months'
    AND customer_bill_to_number IS NOT NULL
),
interval_stats AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    COUNT(*) FILTER (WHERE interval_days IS NOT NULL) AS total_intervals,
    ROUND(AVG(interval_days)::numeric, 1) AS overall_avg_interval,
    ROUND(AVG(CASE WHEN order_date >= NOW() - INTERVAL '6 months' THEN interval_days END)::numeric, 1) AS recent_avg_interval,
    ROUND(AVG(CASE WHEN order_date < NOW() - INTERVAL '6 months' THEN interval_days END)::numeric, 1) AS historical_avg_interval
  FROM order_intervals
  WHERE interval_days IS NOT NULL
  GROUP BY customer_bill_to_number, customer_bill_to_name
  HAVING COUNT(*) FILTER (WHERE interval_days IS NOT NULL) >= 4
    AND COUNT(*) FILTER (WHERE order_date >= NOW() - INTERVAL '6 months' AND interval_days IS NOT NULL) >= 2
    AND COUNT(*) FILTER (WHERE order_date < NOW() - INTERVAL '6 months' AND interval_days IS NOT NULL) >= 2
),
with_gmv AS (
  SELECT
    s.*,
    ROUND(s.recent_avg_interval / NULLIF(s.historical_avg_interval, 0), 2) AS deceleration_ratio,
    ROUND(SUM(po.total_amount)::numeric, 2) AS annual_gmv
  FROM interval_stats s
  JOIN portal_orders po ON po.customer_bill_to_number = s.customer_bill_to_number
    AND po.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
  GROUP BY s.customer_bill_to_number, s.customer_bill_to_name,
    s.total_intervals, s.overall_avg_interval, s.recent_avg_interval, s.historical_avg_interval
)
SELECT
  customer_bill_to_number,
  customer_bill_to_name,
  total_intervals,
  historical_avg_interval,
  recent_avg_interval,
  deceleration_ratio,
  annual_gmv
FROM with_gmv
WHERE deceleration_ratio >= 1.5
ORDER BY annual_gmv DESC
LIMIT 15
```

**Interpretation**: A `deceleration_ratio` of 1.5 means the account's recent order intervals are 50% longer than their historical average — they're buying significantly less frequently. At 2.0x, intervals have doubled. Combined with annual GMV, this quantifies the revenue at risk if the trend continues.

**External claim rules**: "X accounts have order frequency stretching beyond 1.5x their historical average. Combined annual value: $Y." Always hedge: "If this trend continues, projected at-risk revenue is approximately $Z." Use "all-channel order frequency" (not "portal orders" or "ERP"). Never expose `customer_bill_to_number`. Reference accounts by `customer_bill_to_name` only.

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
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL) AND o.total < 5000000
  AND o.created_at BETWEEN NOW() - INTERVAL '12 months' AND NOW() - INTERVAL '3 months'
  AND o.customer_num IS NOT NULL
  AND c.code NOT IN (
    SELECT DISTINCT customer_num FROM orders
    WHERE organization_id = {{ORG_ID}}
      AND is_submitted = true
      AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL) AND o.total < 5000000
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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

<!-- CHANGED v2: canonical total business is now INVOICED sales, not order-header total. Gate on TOTAL_BUSINESS_SOURCE='INVOICES'. -->
**V2 canonical — Total Business (Invoiced) by month** (gate: `TOTAL_BUSINESS_SOURCE = 'INVOICES'`):

```sql
WITH inv AS (
  SELECT pi.invoice_number, pi.invoice_date, pi.customer_bill_to_number,
         COALESCE(
           pi.net_amount,
           SUM(COALESCE(pii.quantity_invoiced,0) * (COALESCE(pii.unit_price,0) - COALESCE(pii.unit_price_discount,0))
               - COALESCE(pii.extended_price_discount,0))
         ) AS invoice_amount
  FROM portal_invoices pi
  LEFT JOIN portal_invoice_items pii
    ON pii.invoice_number = pi.invoice_number AND pii.organization_id = pi.organization_id
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
  GROUP BY pi.invoice_number, pi.invoice_date, pi.customer_bill_to_number, pi.net_amount
)
SELECT
  DATE_TRUNC('month', invoice_date)::date AS month,
  COUNT(*) AS invoices,
  COUNT(DISTINCT customer_bill_to_number) AS unique_accounts,
  ROUND(SUM(invoice_amount)::numeric, 2) AS total_invoiced_sales
FROM inv
GROUP BY 1
ORDER BY 1 DESC
```

**V2 claim rules**: This is "total business / all-channel sales" and matches the client's Sales Portal invoiced-sales total. Negative months/lines = credit memos (legitimate). Never call it eCat sales.

<!-- CHANGED v2: the query below is now the BOOKED-ORDER-VOLUME companion (order_origin breakdown), NOT the total-business figure. order_origin is unreliable per-org (see Q-PROV channel caveat) — do not present the ECAT/market split as authoritative. -->
**Companion — booked order volume & origin mix** (optional; only when `portal_orders` present). The `order_origin='ECAT'` / market-code split is unreliable: `order_origin` is blank for ~30 orgs and free-text/org-specific elsewhere (only 2 orgs use the literal `'ECAT'`). Present as booked-order volume context only, not as channel attribution.

```sql
SELECT
  DATE_TRUNC('month', order_date)::date AS month,
  COUNT(*) AS total_booked_orders,
  COUNT(DISTINCT customer_bill_to_number) AS unique_accounts,
  ROUND(SUM(total_amount)::numeric, 2) AS booked_order_gmv
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC
```

**External claim rules**: Total ERP order volume across all channels (booked). Never describe `portal_orders` as buyer self-service orders. Never present the order-header total as the client's sales number — use the V2 invoiced canonical above for total business.

---

### Q-18: eCat Order Velocity & Trend (with ERP Context)
**Maps to**: VM-18 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

**Part A — eCat orders (confirmed sales only):**

<!-- CHANGED v2: eCat GMV/velocity is confirmed-only (eCat-SALE filter). Quotes/holds excluded so the eCat share denominator and trend are real sales, not pipeline. -->
<!-- ECAT-NUMERATOR -->
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
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
  AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
  AND created_at > NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC
```

**Part B — ERP total context (run only when total business present):**

<!-- CHANGED v2: total context is now INVOICED sales (matches client Sales Portal), not order-header total_amount. Gate on TOTAL_BUSINESS_SOURCE='INVOICES'. -->
```sql
WITH inv AS (
  SELECT pi.invoice_number, pi.invoice_date,
         COALESCE(
           pi.net_amount,
           SUM(COALESCE(pii.quantity_invoiced,0) * (COALESCE(pii.unit_price,0) - COALESCE(pii.unit_price_discount,0))
               - COALESCE(pii.extended_price_discount,0))
         ) AS invoice_amount
  FROM portal_invoices pi
  LEFT JOIN portal_invoice_items pii
    ON pii.invoice_number = pi.invoice_number AND pii.organization_id = pi.organization_id
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
  GROUP BY pi.invoice_number, pi.invoice_date, pi.net_amount
)
SELECT
  DATE_TRUNC('month', invoice_date)::date AS month,
  COUNT(*) AS total_invoices,
  ROUND(SUM(invoice_amount)::numeric, 2) AS total_invoiced_sales
FROM inv
GROUP BY 1
ORDER BY 1 DESC
```

> Fallback when `TOTAL_BUSINESS_SOURCE='ORDERS'` (no invoices): use the booked-order companion query from Q-16 (`portal_orders`, `SUM(total_amount)`) and label the share denominator "booked orders" not "total sales."

**Assembly**: Merge Parts A and B by month. Calculate eCat share (eCat GMV / total invoiced sales). Part A is always run; Part B only when `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS}.

---

### Q-19: eCat Channel Mix Evolution
**Maps to**: VM-19 | **Audience**: external | **Status**: conditional (gate: has_cart = true AND server orders confirmed) | **Source**: Derived from Q-18 Part A

Channel mix is derived from Q-18 Part A output: `ecat_online_orders / total_ecat_orders` per month. Only include for accounts where `order_source = 'server'` orders are confirmed to exist. Do not surface for iPad-only clients.

---

### Q-20: eCat AOV Analysis
**Maps to**: VM-20 | **Audience**: external | **Status**: live | **Source**: Postgres MCP

<!-- CHANGED v2: 'All eCat', 'iPad', 'eCat Online' rows are confirmed-SALE only (eCat-SALE filter) so AOV reflects real deal size. The 'Quote Orders' row is retained intentionally as a pipeline contrast — never sum it into eCat sales. -->
<!-- ECAT-NUMERATOR --> <!-- note: also contains an intentional non-filtered 'Quote Orders' contrast row; linter requires >=1 canonical filter, which the confirmed rows supply -->
```sql
SELECT
  'All eCat Orders (confirmed)' AS dimension,
  COUNT(*) AS order_count,
  ROUND(AVG(total)::numeric, 2) AS avg_order_value,
  ROUND(SUM(total)::numeric, 2) AS total_ecat_gmv
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
  AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
  AND created_at > NOW() - INTERVAL '12 months'

UNION ALL

SELECT
  'iPad Orders (confirmed)',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
  AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
  AND created_at > NOW() - INTERVAL '12 months'
  AND order_source = 'ipad'

UNION ALL

SELECT
  'eCat Online Orders (confirmed)',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
  AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
  AND created_at > NOW() - INTERVAL '12 months'
  AND order_source = 'server'

UNION ALL

SELECT
  'Quote Orders (pipeline — NOT sales)',
  COUNT(*), ROUND(AVG(total)::numeric, 2), ROUND(SUM(total)::numeric, 2)
FROM orders
WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
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
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
  AND created_at > NOW() - INTERVAL '12 months'
GROUP BY order_type
ORDER BY orders DESC
```

---

### Q-45: eCat Capture Rate vs. Total Business
**Maps to**: VM-45 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS}) | **Source**: Postgres MCP

<!-- CHANGED v2: denominator is now INVOICED total business (net_amount), matching the client Sales Portal. The prior order-header denominator under-counted invoice-dominant orgs ~9x and made capture rate either impossible (gate-skipped) or absurd (>100%). Validated 2026-06-25: bcf capture 35.7% LTM with this denominator. -->
<!-- ECAT-NUMERATOR -->
```sql
WITH ecat_totals AS (
  SELECT
    SUM(total) AS ecat_gmv,
    COUNT(*) AS ecat_order_count
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter (confirmed sales only)
    AND created_at >= NOW() - INTERVAL '12 months'
),
total_business AS (   -- invoiced sales = the client's own Sales Portal number
  SELECT
    SUM(invoice_amount) AS tb_gmv,
    COUNT(*) AS tb_invoice_count
  FROM (
    SELECT pi.invoice_number,
           COALESCE(
             pi.net_amount,
             SUM(COALESCE(pii.quantity_invoiced,0) * (COALESCE(pii.unit_price,0) - COALESCE(pii.unit_price_discount,0))
                 - COALESCE(pii.extended_price_discount,0))
           ) AS invoice_amount
    FROM portal_invoices pi
    LEFT JOIN portal_invoice_items pii
      ON pii.invoice_number = pi.invoice_number AND pii.organization_id = pi.organization_id
    WHERE pi.organization_id = {{ORG_ID}}
      AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    GROUP BY pi.invoice_number, pi.net_amount
  ) i
)
SELECT
  e.ecat_order_count,
  p.tb_invoice_count,
  ROUND(e.ecat_gmv::numeric, 2) AS ecat_gmv,
  ROUND(p.tb_gmv::numeric, 2) AS total_business_gmv,
  ROUND(100.0 * e.ecat_gmv / NULLIF(p.tb_gmv, 0), 1) AS ecat_gmv_capture_pct,
  CASE
    WHEN e.ecat_gmv > 1.05 * NULLIF(p.tb_gmv, 0)
      THEN 'PARTIAL_INVOICE_FEED — confirmed eCat sales exceed invoiced total; invoice feed is partial/lagging. DO NOT PUBLISH capture rate (see VM-45 gate #2).'
    ELSE 'OK'
  END AS feed_integrity_flag,
  CASE
    WHEN e.ecat_gmv > 1.05 * NULLIF(p.tb_gmv, 0) THEN 'Suppressed — partial invoice feed'
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.tb_gmv, 0) > 50 THEN 'Primary transaction system'
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.tb_gmv, 0) BETWEEN 25 AND 50 THEN 'Meaningful eCat channel; dual-system'
    WHEN 100.0 * e.ecat_gmv / NULLIF(p.tb_gmv, 0) BETWEEN 10 AND 25 THEN 'Partial capture; eCat is growing'
    ELSE 'Enablement-heavy; eCat captures little of total volume'
  END AS ecat_posture
FROM ecat_totals e, total_business p
```

> **Partial-feed flag (pilot-validated 2026-06-25)**: when `feed_integrity_flag = 'PARTIAL_INVOICE_FEED'` the invoice feed does not cover all of what eCat already booked as confirmed sales (e.g. cohort client `sc`: confirmed eCat > invoiced total → 126.9% raw capture). This is a **feed-completeness defect, not a real >100% capture** — suppress the capture rate, do not fall back to the order-header denominator, and surface the completeness gap as the finding.

> **ORDERS fallback** (`TOTAL_BUSINESS_SOURCE='ORDERS'`, no invoices): swap the `total_business` CTE for `SELECT SUM(total_amount) tb_gmv, COUNT(*) tb_invoice_count FROM portal_orders WHERE organization_id={{ORG_ID}} AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'` and label the denominator "booked orders," confidence PARTIAL.

**External claim rules**: eCat GMV share of **invoiced total business** (the client's actual sales). "eCat captures X% of your total sales." Compares to invoiced sales across all channels — do not present total business as eCat-originated. Low capture rate is not a failure — it reflects legitimate multi-channel business. Label confidence from Q-PROV-00 (`FULL`/`STRONG`).

---

### Q-CHAN-05: eCat vs Non-eCat Split (the "where you sell" headline)
<!-- CHANGED v2: added (Level 1 of where-you-sell; see commerce_where_you_sell.md). -->
**Maps to**: where-you-sell (Level 1) | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS} AND NOT `PARTIAL_INVOICE_FEED`) | **Source**: Postgres MCP

The headline commerce decomposition: of the client's **total invoiced business**, how much flows through **eCat** vs **every other channel**. This needs only an invoiced total (denominator) + confirmed eCat GMV (numerator) — far more widely available than the per-channel `order_origin` cut (that's Q-CHAN-10, Level 2). The **confidence tier from Q-PROV-00 decides whether to report or suppress.**

> **Basis caveat (must accompany the number)**: the eCat numerator is *ordered* value (`orders.total` at order time); the denominator is *invoiced* value (`portal_invoices.net_amount`). We cannot link eCat orders to invoices 1:1 (order-number join ≈ 0%), so the split is an **approximation of ordered-eCat against invoiced-total**. When eCat ordered > 1.05× invoiced total the invoice feed is partial → **suppress** (do not publish a >100% or a misleading split). This is the FAL guardrail.

<!-- ECAT-NUMERATOR -->
```sql
WITH ecat AS (   -- confirmed eCat GMV (eCat-SALE filter)
  SELECT SUM(total) AS ecat_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at >= NOW() - INTERVAL '12 months'
),
total_business AS (   -- invoiced sales = client's own Sales Portal number
  SELECT SUM(invoice_amount) AS tb_gmv
  FROM (
    SELECT pi.invoice_number,
           COALESCE(
             pi.net_amount,
             SUM(COALESCE(pii.quantity_invoiced,0) * (COALESCE(pii.unit_price,0) - COALESCE(pii.unit_price_discount,0))
                 - COALESCE(pii.extended_price_discount,0))
           ) AS invoice_amount
    FROM portal_invoices pi
    LEFT JOIN portal_invoice_items pii
      ON pii.invoice_number = pi.invoice_number AND pii.organization_id = pi.organization_id
    WHERE pi.organization_id = {{ORG_ID}}
      AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    GROUP BY pi.invoice_number, pi.net_amount
  ) i
)
SELECT
  ROUND(t.tb_gmv::numeric, 2)                                          AS total_business_gmv,
  ROUND(COALESCE(e.ecat_gmv,0)::numeric, 2)                            AS ecat_gmv,
  ROUND(GREATEST(t.tb_gmv - COALESCE(e.ecat_gmv,0), 0)::numeric, 2)    AS non_ecat_gmv,
  ROUND(100.0 * COALESCE(e.ecat_gmv,0) / NULLIF(t.tb_gmv,0), 1)        AS ecat_pct,
  ROUND(100.0 * GREATEST(t.tb_gmv - COALESCE(e.ecat_gmv,0),0) / NULLIF(t.tb_gmv,0), 1) AS non_ecat_pct,
  CASE
    WHEN t.tb_gmv IS NULL OR t.tb_gmv = 0 THEN 'SUPPRESS — no invoiced total to divide into'
    WHEN COALESCE(e.ecat_gmv,0) > 1.05 * t.tb_gmv THEN 'SUPPRESS — partial invoice feed (eCat ordered > invoiced total)'
    ELSE 'REPORT — label confidence from Q-PROV-00 (FULL/STRONG/PARTIAL); add basis + gross-of-returns/stale caveats'
  END AS report_decision
FROM total_business t, ecat e
```

**Gating (from Q-PROV-00, run first)**:
- `TOTAL_BUSINESS_SOURCE = 'NONE'` or `'SALES_DATA'` → **do not run**; there is no comparable invoiced total (e.g. `uhc`, `da`, `fal`, `wag`). State eCat activity without a share.
- `TOTAL_BUSINESS_SOURCE = 'ORDERS'` (no invoices) → swap `total_business` for the booked-order companion (`portal_orders`, `SUM(total_amount)`, date-clamped) and label the split "of booked orders," confidence PARTIAL.
- `PARTIAL_INVOICE_FEED = true` or `report_decision LIKE 'SUPPRESS%'` → **suppress the split.** Never publish a >100% eCat share or fall back to the order-header denominator.
- `COMMERCE_CONFIDENCE = 'PARTIAL'` (stale, e.g. `mhc`/`bmc`) → report but cap the window at `REPORT_THROUGH_DATE` and flag staleness.

**External claim rules**: "Of your ~$X in total invoiced business, eCat accounts for Y% — the remaining Z% flows through other channels." Always pair with the confidence label and the ordered-vs-invoiced basis caveat. The non-eCat slice is **not** itself attributed to a channel here — that requires Q-CHAN-10 (`order_origin`), available for only a minority of clients. Never imply the non-eCat remainder is lost/at-risk; it is legitimate multi-channel business.

---

### Q-CHAN-06: eCat-SALE Confirmed-Ratio Pre-Check (F1 — may eCat lead?)
<!-- CHANGED v2: added (Track B / handoffs/decision_completeness_no_drift_2026-07-09.md §4 Track B, red-team F1). The eCat-SALE filter (line ~78) fails OPEN — COALESCE(...,'Confirmed') counts a blank/null order_type as a sale. Before an org's eCat figure is allowed to LEAD a report (NONE/STALE postures), this pre-check must clear. -->
**Maps to**: eCat-lead honesty gate (Spine §6.5, red-team F1) | **Audience**: internal (gate) | **Status**: required before eCat may stand as a report hero | **Source**: Postgres MCP

Answers *"is this org's confirmed eCat GMV actually explicit, or is a material share of it just blank `order_type` defaulting to 'Confirmed' via the eCat-SALE filter's `COALESCE`?"* Same LTM window as the eCat hero (`created_at >= NOW() - INTERVAL '12 months'`, matching `Q-ECON-00`'s `ecat` CTE), same base guard as every other eCat-numerator query (`is_submitted = true`, not-deleted, `total < 5000000`). Emits `confirmed_gmv` (WITH the eCat-SALE filter), `all_ecat_gmv` (same rows, WITHOUT the sale-type filter — every submitted, non-deleted eCat order regardless of type), and `blank_default_share_pct` = blank/null-`order_type` GMV ÷ `confirmed_gmv`.

<!-- ECAT-NUMERATOR -->
```sql
WITH base AS (   -- LTM eCat orders, base guard ONLY (same window as the eCat hero, Q-ECON-00's `ecat` CTE)
  SELECT
    COALESCE(NULLIF(TRIM(order_type), ''), '(blank)') AS order_type_bucket,
    total
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND total < 5000000
    AND created_at >= NOW() - INTERVAL '12 months'
)
SELECT
  ROUND(SUM(total)::numeric, 2) AS all_ecat_gmv,   -- every submitted, non-deleted eCat order in the window (no sale-type filter)
  ROUND(SUM(total) FILTER (
    WHERE order_type_bucket NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
      AND order_type_bucket NOT ILIKE 'HFC%' AND order_type_bucket NOT ILIKE 'Hold%' AND order_type_bucket NOT ILIKE 'TEST%'
  )::numeric, 2) AS confirmed_gmv,                   -- eCat-SALE filter applied (Spine §6.5); blank buckets pass through (COALESCE -> 'Confirmed')
  ROUND(COALESCE(SUM(total) FILTER (WHERE order_type_bucket = '(blank)'), 0)::numeric, 2) AS blank_gmv,
  COUNT(*) FILTER (WHERE order_type_bucket = '(blank)') AS blank_n,
  COUNT(*) AS total_n,
  ROUND(
    100.0 * COALESCE(SUM(total) FILTER (WHERE order_type_bucket = '(blank)'), 0)
    / NULLIF(SUM(total) FILTER (
        WHERE order_type_bucket NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
          AND order_type_bucket NOT ILIKE 'HFC%' AND order_type_bucket NOT ILIKE 'Hold%' AND order_type_bucket NOT ILIKE 'TEST%'
      ), 0),
  2) AS blank_default_share_pct
FROM base
```

**Rule (F1)**: if `blank_default_share_pct >= 5.0`, the eCat figure's confidence is capped and the render adds *"includes orders without an explicit sale status."* Below 5%, render clean — no caveat, no cap. Never let an unverified eCat number stand as a NONE/STALE-posture hero without this check clearing.

**Live-verified (2026-07-09, LTM window, 19-org sweep incl. every named org in the decision memo)**: every org checked — including `da` (the floor gold standard: 4,250 LTM eCat orders, $4,872,762.99 confirmed GMV, **0 blank rows**, `blank_default_share_pct = 0.00`) — currently returns a clean **0.00%**. A full-table scan (no org filter) confirms the blank-`order_type` failure mode is **historical only** (rows dated 2012–2019); no live org has a blank `order_type` row inside a trailing-12-month window today. The >=5% cap mechanism is verified against `bmc`'s **all-time** (non-LTM) shape as a threshold-logic check: all-time `confirmed_gmv` = $76,097,836.10, all-time blank GMV = $11,352,817.30 -> **14.92%**, correctly trips the >=5% rule. This query still runs on every report — the gate is drift protection for future/onboarding orgs, not a live-data necessity today.

**External claim rules**: internal gate only — never shown to a client. Drives the F1 confidence cap + caveat on any eCat figure standing as a report hero (Spine §6.5).

---

## Domain 4b — Channel Provenance (Where-You-Sell Level 2)
<!-- CHANGED v2: new domain. Level 2 of where-you-sell — splitting the non-eCat slice into sub-channels from portal_orders.order_origin. BESPOKE/GATED: a full-population scan (commerce_order_origin_population_scan.md, 2026-06-25) found only ~8 of 41 live-commerce orgs carry usable multi-channel origin, and only cci tags eCat reliably. These queries SUPPRESS for NONE-tier orgs exactly like Q-PROV-00 gates total business. -->

> **Read first**: Level 2 is **not** a default report section. `order_origin` exists only on booked orders (`portal_orders`), is bespoke per client, and is blank or single-bucket for most orgs. Run **Q-CHAN-00** first; only proceed to Q-CHAN-10/20 for orgs that clear the gate AND have a maintained per-org channel map. Channel magnitudes are **booked** dollars (order grain) — report channel **% mix** and apply that mix to the invoiced total from Q-CHAN-05 for dollar figures, captioned "channel mix from booked orders." Never present booked totals as the client's sales.

### Q-CHAN-00: Channel Availability Preflight (sets CHANNEL_CONFIDENCE)
<!-- CHANGED v2: new. Per-org order_origin fill-rate + eCat-tag reconciliation → CHANNEL_CONFIDENCE. Gate for Q-CHAN-10/20. -->
**Maps to**: where-you-sell (Level 2 gate) | **Audience**: internal | **Status**: preflight | **Source**: Postgres MCP

Quantitative gate for whether an org can support a channel decomposition at all. The tier (STRONG/PARTIAL/LIMITED/NONE) is finalized by the per-org channel map below — this query produces the signals + a recommended gate.

<!-- ECAT-NUMERATOR -->
```sql
WITH booked AS (
  SELECT NULLIF(TRIM(order_origin),'') AS origin, total_amount
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND total_amount < 5000000
),
agg AS (
  SELECT
    COUNT(*) AS booked_rows,
    SUM(total_amount) AS booked_dollars,
    SUM(CASE WHEN origin IS NOT NULL THEN total_amount ELSE 0 END) AS attributed_dollars,
    COUNT(DISTINCT origin) AS distinct_origins,
    SUM(CASE WHEN UPPER(origin) IN ('ECAT','ECAT ORDER') THEN total_amount ELSE 0 END) AS ecat_origin_dollars
  FROM booked
),
ecat AS (   -- confirmed eCat GMV (eCat-SALE filter) for tag reconciliation
  SELECT SUM(total) AS ecat_confirmed_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at >= NOW() - INTERVAL '12 months'
)
SELECT
  a.booked_rows,
  ROUND(a.booked_dollars::numeric,2)                                       AS booked_dollars,
  ROUND(100.0*a.attributed_dollars/NULLIF(a.booked_dollars,0),1)           AS pct_attributed_dollars,
  a.distinct_origins,
  ROUND(a.ecat_origin_dollars::numeric,2)                                  AS ecat_origin_dollars,
  ROUND(COALESCE(e.ecat_confirmed_gmv,0)::numeric,2)                       AS ecat_confirmed_gmv,
  ROUND(a.ecat_origin_dollars::numeric / NULLIF(e.ecat_confirmed_gmv,0),2) AS ecat_recon_ratio,
  CASE
    WHEN a.ecat_origin_dollars = 0 THEN 'NONE — eCat not tagged; overlay our orders truth'
    WHEN a.ecat_origin_dollars BETWEEN 0.8*e.ecat_confirmed_gmv AND 1.25*e.ecat_confirmed_gmv THEN 'RELIABLE — read eCat from origin (cci-style)'
    WHEN a.ecat_origin_dollars > 1.25*e.ecat_confirmed_gmv THEN 'OVER-TAG — origin ECAT > confirmed eCat; do NOT trust origin for eCat $'
    ELSE 'UNDER-TAG — origin misses most eCat; overlay our orders truth'
  END AS ecat_tag_status,
  CASE
    WHEN a.booked_rows < 25 OR a.distinct_origins < 2
         OR 100.0*a.attributed_dollars/NULLIF(a.booked_dollars,0) < 60
      THEN 'NONE — SUPPRESS channel section (insufficient origin signal: blank, single-bucket, or too sparse)'
    ELSE 'CANDIDATE — finalize STRONG/PARTIAL/LIMITED from the per-org channel map (true channels vs data-entry roles; eCat tag reliability)'
  END AS channel_confidence_gate
FROM agg a, ecat e
```

**Gate logic**: `NONE` (suppress) when `pct_attributed_dollars < 60` OR `distinct_origins < 2` OR `booked_rows < 25`. A `CANDIDATE` then becomes:
- **STRONG** — origin codes are true sales channels AND eCat tag `RELIABLE` (cci).
- **PARTIAL** — true channels but eCat folded / `OVER-TAG` / `UNDER-TAG`, or feed stale (ufi, mhc, ih, wwjc, el, sarreid, ril).
- **LIMITED** — origin codes are data-entry roles (REP/CUSTOMER), not sales channels (sc, sccon, scw, gh); eCat not separable. Also flag any test/demo org (e.g. demo2, clc, clctest) for exclusion.

**Population reference (LTM, 2026-06-25)**: 41 live-commerce orgs → ~8 STRONG/PARTIAL, ~4 LIMITED, 6 single-origin (→NONE), 20 blank (→NONE), 3 test. Full table: `commerce_order_origin_population_scan.md`.

### Per-org `order_origin → canonical_channel` map (scaffold — MUST be maintained per org)
<!-- CHANGED v2: new. Codes are bespoke per client; there is no global vocabulary. Q-CHAN-10 reads this map. Extend as orgs are onboarded to Level 2. -->

Canonical channels: **eCat** · **Online** (client web / B2B / marketplace, non-eCat) · **EDI** · **Rep** (ERP/rep-keyed) · **Cust-Direct** (phone/email/manual) · **Market** (showroom/tradeshow) · **Returns** (RMA/claims — exclude from sales mix) · **Other** · **Unattributed** (blank).

| Org | Raw `order_origin` (UPPER) | Canonical | Note |
|---|---|---|---|
| `cci` | WEB | Online | |
| `cci` | ECAT | eCat | **reliable tag** (reconciles) |
| `cci` | EDI | EDI | |
| `cci` | D | Cust-Direct | |
| `cci` | R | Rep | |
| `cci` | HPMKT, AMKT, LVMKT, DMKT, DROOM, AROOM, HPROOM | Market | |
| `ufi` | ONLINE, OCCB2B, OCC | Online | eCat folded in here |
| `ufi` | EDI | EDI | |
| `ufi` | COPY | Other | |
| `ufi` | ORDER CAPTURE QUOTES | (exclude) | quotes, not sales |
| `mhc` | E-COMMERCE, EXTERNAL WEBSITE, EC, EW | Online | feed stale 186d |
| `mhc` | CUSTOMER DIRECT, CD | Cust-Direct | |
| `mhc` | CLAIMS, CL | Returns | exclude from mix |
| `mhc` | MT, MARKET TRADESHOW | Market | |
| `ih` | WEBORDER | Online | |
| `ih` | REPORDER, EORDER | Rep | |
| `ih` | NYSR | Market | showroom |
| `ih` | MARKET | Market | |
| `ih` | CUSTPRG | Cust-Direct | |
| `wwjc` | EOL ORDER, ECOMMERCE ORDER | Online | |
| `wwjc` | ECAT ORDER | eCat | **UNDER-TAG** — overlay our orders truth |
| `wwjc` | CUSTOMER EMAILED | Cust-Direct | |
| `wwjc` | HIGH POINT MARKET ORDER, ATLANTA MARKET ORDER | Market | |
| `el` | COMMERCIAL / PROJECT, REGULAR | Cust-Direct | |
| `el` | DALLAS SHOWROOM | Market | |
| `el` | STAND ALONE, DROP SHIP | Other | |
| `sarreid` | WEB | Online | |
| `sarreid` | ROAD | Rep | |
| `sarreid` | OTHER | Other | |
| `ril` | NAV | Other | ERP-imported (non-eCat) |
| `ril` | ECAT | eCat | **OVER-TAG 12×** — do NOT trust; overlay our orders truth |
| `sc`,`sccon`,`scw`,`gh` | REP | Rep | LIMITED: role code, not channel |
| `sc`,`sccon`,`scw`,`gh` | CUSTOMER | Cust-Direct | LIMITED: role code |
| `sc`,`sccon`,`scw`,`gh` | WEB | Online | |
| `scw`,`gh` | SPS-WAYFAIR, SPS-KATHY KUO | Online | marketplace/dropship |
| `sc`,`sccon`,`scw`,`gh` | RMA | Returns | exclude from mix |

> Anything not in the map → `Other (unmapped)`; blank → `Unattributed`. Review unmapped buckets before publishing. eCat rows flagged OVER-TAG/UNDER-TAG: do not read eCat $ from origin — take eCat from our `orders` truth (Q-CHAN-05) and caveat the overlap inside the Online/Rep bucket.

### Q-CHAN-10: Where-You-Sell Decomposition (channel % mix from `order_origin`)
<!-- CHANGED v2: new. SUM(total_amount) by canonical channel via the per-org map. Booked grain → report % mix. -->
**Maps to**: where-you-sell (Level 2) | **Audience**: external | **Status**: conditional (gate: Q-CHAN-00 ≠ NONE AND per-org map present) | **Source**: Postgres MCP

Replace the `chan_map` VALUES block with the target org's rows from the scaffold above (UPPER-cased raw origin → canonical channel).

```sql
WITH chan_map(origin_upper, canonical_channel) AS (
  VALUES
    -- === EXAMPLE: cci — replace with the target org's rows ===
    ('WEB','Online'), ('ECAT','eCat'), ('EDI','EDI'), ('D','Cust-Direct'), ('R','Rep'),
    ('HPMKT','Market'), ('AMKT','Market'), ('LVMKT','Market'), ('DMKT','Market'),
    ('DROOM','Market'), ('AROOM','Market'), ('HPROOM','Market')
),
booked AS (
  SELECT UPPER(NULLIF(TRIM(order_origin),'')) AS origin_upper, total_amount
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND total_amount < 5000000
    AND COALESCE(UPPER(TRIM(order_origin)),'') NOT LIKE '%QUOTE%'   -- drop quote-origin rows
)
SELECT
  COALESCE(m.canonical_channel,
           CASE WHEN b.origin_upper IS NULL THEN 'Unattributed' ELSE 'Other (unmapped)' END) AS channel,
  ROUND(SUM(b.total_amount)::numeric, 2)                                          AS booked_dollars,
  ROUND(100.0 * SUM(b.total_amount) / NULLIF(SUM(SUM(b.total_amount)) OVER (), 0), 1) AS pct_mix
FROM booked b
LEFT JOIN chan_map m ON m.origin_upper = b.origin_upper
GROUP BY 1
ORDER BY booked_dollars DESC
```

**Gating / presentation**:
- Only run when Q-CHAN-00 `channel_confidence_gate = CANDIDATE` and a per-org map exists. For LIMITED orgs (role codes), present as "order entry by rep vs customer," **not** as sales channels.
- Magnitudes are **booked**. To express in dollars, apply `pct_mix` to the invoiced total from Q-CHAN-05 and caption "channel mix from booked orders, applied to invoiced total."
- Exclude `Returns` from the sales mix (report separately). `eCat` rows flagged OVER/UNDER-tag: replace the origin-derived eCat figure with the Q-CHAN-05 confirmed eCat and fold the difference into the adjacent bucket with a caveat.
- Suppress the section entirely (state "your feed doesn't yet tell us where these sales originate") for NONE-tier orgs.

### Q-CHAN-20: eCat-vs-Origin Reconciliation
<!-- CHANGED v2: new. Validates whether an org's eCat origin tag can be trusted, or eCat must be overlaid from our orders truth. -->
**Maps to**: where-you-sell (Level 2 trust check) | **Audience**: internal | **Status**: conditional (gate: org has an eCat origin code) | **Source**: Postgres MCP

<!-- ECAT-NUMERATOR -->
```sql
WITH origin_ecat AS (
  SELECT SUM(total_amount) AS ecat_origin_dollars
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND UPPER(TRIM(order_origin)) IN ('ECAT','ECAT ORDER')   -- per-org eCat origin code(s)
    AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND total_amount < 5000000
),
app_ecat AS (   -- our orders truth (eCat-SALE filter)
  SELECT SUM(total) AS ecat_confirmed_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at >= NOW() - INTERVAL '12 months'
)
SELECT
  ROUND(COALESCE(o.ecat_origin_dollars,0)::numeric,2)                        AS ecat_origin_dollars,
  ROUND(COALESCE(a.ecat_confirmed_gmv,0)::numeric,2)                         AS ecat_confirmed_gmv,
  ROUND(COALESCE(o.ecat_origin_dollars,0)::numeric / NULLIF(a.ecat_confirmed_gmv,0),2) AS recon_ratio,
  CASE
    WHEN COALESCE(o.ecat_origin_dollars,0) = 0 THEN 'NO eCAT ORIGIN TAG — overlay our orders truth; never read eCat from origin'
    WHEN o.ecat_origin_dollars BETWEEN 0.8*a.ecat_confirmed_gmv AND 1.25*a.ecat_confirmed_gmv THEN 'RELIABLE — eCat channel can be read from origin (cci-style)'
    WHEN o.ecat_origin_dollars > 1.25*a.ecat_confirmed_gmv THEN 'OVER-TAG — origin ECAT exceeds confirmed eCat; do not trust origin for eCat $'
    ELSE 'UNDER-TAG — origin misses most eCat; overlay our orders truth'
  END AS verdict
FROM origin_ecat o, app_ecat a
```

**Reference (LTM, 2026-06-25)**: `cci` ratio 1.01 (RELIABLE) · `ril` 12.1 (OVER-TAG) · `wwjc` 0.25 (UNDER-TAG). Only `cci` can read eCat straight from origin; everyone else overlays the Q-CHAN-05 confirmed eCat number.

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
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL) AND o.total < 5000000
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

<!-- ECAT-NUMERATOR -->
```sql
SELECT
  o.id AS org_id,
  o.shortname,
  o.name,
  (SELECT COUNT(*) FROM products WHERE organization_id = o.id AND deleted = false) AS active_products,
  (SELECT COUNT(*) FROM customers WHERE organization_id = o.id) AS total_erp_customers,
  (SELECT COUNT(*) FROM org_users WHERE organization_id = o.id AND disabled = false) AS active_users,
  (SELECT COUNT(*) FROM orders WHERE organization_id = o.id AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND created_at > NOW() - INTERVAL '12 months') AS ecat_orders_12mo,
  (SELECT ROUND(SUM(total)::numeric, 2) FROM orders WHERE organization_id = o.id
    AND is_submitted = true AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at > NOW() - INTERVAL '12 months') AS ecat_gmv_12mo,   -- eCat-SALE filter: confirmed sales only
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

## Domain 9 — ERP Enrichment Intelligence

> All Domain 9 queries require `HAS_PORTAL_ORDERS = true`. They enrich existing sections with total-business context from the client's ERP-synced order data (`portal_orders`). When `portal_orders` is absent, these queries do not run and their consuming sections render identically to the pre-enrichment behavior — no placeholders, no degradation.
>
> <!-- CHANGED v2 --> **V2 update**: "total business" is now invoiced sales (`portal_invoices.net_amount`), not order-header `total_amount`. Run the Commerce Provenance Preflight (Q-PROV-00) first to set `TOTAL_BUSINESS_SOURCE` / `COMMERCE_CONFIDENCE`. The legacy `HAS_PORTAL_ORDERS` gate is retained for back-compat but is superseded by `TOTAL_BUSINESS_SOURCE` for any total-business / capture / penetration metric.

### Q-PROV-00: Commerce Provenance Preflight
<!-- CHANGED v2: added -->
**Maps to**: provenance gate | **Audience**: internal (sets flags) | **Status**: live | **Source**: Postgres

Run once per org during Stage 1 preflight. Sets the source + confidence for every total-business metric. Validated 2026-06-25 (`commerce_validation_worksheet.md`): invoiced total = `SUM(net_amount)` reproduces the Sales Portal warehouse `SUM(amount_invoiced)` and is stable across all reconciliation/calc buckets (`net_amount` is ~100% populated in production).

<!-- ECAT-NUMERATOR -->
```sql
WITH inv AS (
  SELECT COUNT(*) n,
         MAX(invoice_date) FILTER (WHERE invoice_date BETWEEN DATE '2010-01-01' AND CURRENT_DATE + INTERVAL '90 days') AS last_inv,
         COUNT(DISTINCT DATE_TRUNC('month', invoice_date)) FILTER (WHERE invoice_date BETWEEN DATE '2010-01-01' AND CURRENT_DATE + INTERVAL '90 days') AS distinct_months,
         ROUND(100.0 * COUNT(*) FILTER (WHERE net_amount IS NOT NULL) / NULLIF(COUNT(*),0), 1) AS pct_netamount,
         COUNT(*) FILTER (WHERE net_amount < 0) AS credit_memos,   -- returns-in-feed proxy
         ROUND(SUM(net_amount) FILTER (WHERE invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days')::numeric, 2) AS inv_ltm_net   -- LTM invoiced total for partial-feed check
  FROM portal_invoices WHERE organization_id = {{ORG_ID}}
),
ret AS (   -- returns can also be line-level (quantity_returned) with no negative header
  SELECT COUNT(*) FILTER (WHERE quantity_returned > 0) AS return_lines
  FROM portal_invoice_items WHERE organization_id = {{ORG_ID}}
),
ord AS (
  SELECT COUNT(*) n,
         MAX(order_date) FILTER (WHERE order_date BETWEEN DATE '2010-01-01' AND CURRENT_DATE + INTERVAL '90 days') AS last_ord
  FROM portal_orders WHERE organization_id = {{ORG_ID}}
),
sd AS (   -- summary feed: rows alone are NOT enough — must carry dollars (client `da` had rows but $0)
  SELECT COUNT(*) n,
         ROUND(SUM(COALESCE(amount_invoiced,0))::numeric, 2) AS sd_amt
  FROM sales_data WHERE organization_id = {{ORG_ID}}
),
ecat AS (   -- LTM CONFIRMED eCat GMV (eCat-SALE filter) — for partial-invoice-feed detection
  SELECT ROUND(SUM(total)::numeric, 2) AS ecat_ltm_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at >= NOW() - INTERVAL '12 months'
),
cfg AS (
  SELECT COALESCE(properties->>'portal_data_type','OVERLAPS') AS portal_data_type,
         COALESCE(properties->>'portal_calculations','PORTAL_CALCULATIONS_20180720') AS portal_calculations
  FROM organizations WHERE id = {{ORG_ID}}
)
SELECT
  inv.n AS invoices, ord.n AS orders, sd.n AS sales_data_rows, sd.sd_amt AS sales_data_dollars,
  inv.last_inv, ord.last_ord, inv.pct_netamount, inv.distinct_months,
  (CURRENT_DATE - inv.last_inv) AS days_since_last_invoice,
  (inv.credit_memos > 0 OR ret.return_lines > 0) AS returns_in_feed,
  LEAST(inv.last_inv, CURRENT_DATE) AS report_through_date,   -- cap reporting window here when stale
  COALESCE(ecat.ecat_ltm_gmv, 0) AS ecat_ltm_confirmed_gmv,
  inv.inv_ltm_net AS invoiced_ltm_total,
  -- partial invoice feed: confirmed eCat sales exceed invoiced total by >5% → feed is incomplete, NOT real >100% capture
  (inv.n > 0 AND COALESCE(ecat.ecat_ltm_gmv,0) > 1.05 * NULLIF(inv.inv_ltm_net,0)) AS partial_invoice_feed,
  cfg.portal_data_type, cfg.portal_calculations,
  CASE
    WHEN inv.n > 0 THEN 'INVOICES'
    WHEN ord.n > 0 THEN 'ORDERS'
    WHEN sd.n  > 0 AND sd.sd_amt > 0 THEN 'SALES_DATA'   -- only when dollars present
    ELSE 'NONE'
  END AS total_business_source,
  CASE
    -- stale invoice feed: total business is incomplete for any trailing window past last_inv
    WHEN inv.n > 0 AND (CURRENT_DATE - inv.last_inv) > 45 THEN 'PARTIAL'
    -- partial invoice feed (eCat already booked more than the feed shows): cannot trust invoiced total → suppress
    WHEN inv.n > 0 AND COALESCE(ecat.ecat_ltm_gmv,0) > 1.05 * NULLIF(inv.inv_ltm_net,0) THEN 'PARTIAL'
    -- clean, fresh, contiguous, integrity OK, AND returns represented, AND default reconciliation
    WHEN inv.n > 0 AND inv.pct_netamount >= 99
         AND (inv.credit_memos > 0 OR ret.return_lines > 0)
         AND cfg.portal_data_type = 'OVERLAPS'
         AND cfg.portal_calculations = 'PORTAL_CALCULATIONS_20180720' THEN 'FULL'
    WHEN inv.n > 0 THEN 'STRONG'                 -- gross-only (no returns), LEGACY, or non-OVERLAPS: invoiced total valid; caveat returns / mixed metrics
    WHEN ord.n > 0 THEN 'PARTIAL'                -- booked orders only, no shipped truth
    WHEN sd.n  > 0 AND sd.sd_amt > 0 THEN 'LIMITED'   -- summary only, no period granularity, but real dollars
    ELSE 'NONE'                                  -- no feed, OR sales_data rows with $0 (e.g. `da`)
  END AS commerce_confidence
FROM inv, ret, ord, sd, ecat, cfg
```

**Set from results**:
- `TOTAL_BUSINESS_SOURCE` (INVOICES/ORDERS/SALES_DATA/NONE)
- `COMMERCE_CONFIDENCE` (FULL/STRONG/PARTIAL/LIMITED/NONE)
- `REPORT_THROUGH_DATE` — **cap every reporting window at this date.** When `days_since_last_invoice > 45` the feed is stale; never report a trailing-12-month window that runs past the last invoice (it injects empty months and makes business look collapsed — e.g. `mhc`, feed stopped 2025-12-22).
- `RETURNS_IN_FEED` — when false, the total is **gross of returns** (no credit memos and no `quantity_returned` lines). Label it "gross invoiced sales" and cap confidence at STRONG (e.g. `ufi`, `pf`, `jyc`, `bcf`). `cci`/`fc` send credits → net.
- `RECONCILIATION_FLAG` — true when not OVERLAPS+20180720; affects order+invoice mixed metrics (capture vs ordered, backlog), not the invoiced total.
- `PARTIAL_INVOICE_FEED` (pilot refinement #2) — **true when confirmed LTM eCat GMV > 1.05 × invoiced LTM total.** The invoice feed does not even cover what eCat already booked as confirmed sales, so the invoiced "total business" is itself incomplete. Confidence is forced to PARTIAL: **suppress capture/penetration** (Q-45/Q-51/Q-52/Q-54), do NOT fall back to the order-header denominator, and report the feed-completeness gap as the finding. Observed in cohort client `sc` (confirmed eCat > invoiced → 126.9% raw capture).
- `SALES_DATA_DOLLARS` (pilot refinement #1) — `SALES_DATA` only qualifies as `LIMITED` when `sales_data_dollars > 0`. Rows with `$0` invoiced (e.g. client `da`: rows present, all amounts zero) resolve to `TOTAL_BUSINESS_SOURCE='NONE'` / `COMMERCE_CONFIDENCE='NONE'` — **suppress the total-business figure entirely**, do not present a $0 "total."

> **Coverage note**: interior month gaps were absent across all audited orgs (`commerce_validation_worksheet.md`) — the only temporal failure mode observed is tail staleness, handled by `REPORT_THROUGH_DATE`. If `distinct_months` is far below the calendar span, investigate before reporting trends.

### Q-PROV-SD: Sales-Data-Only LIMITED Path
<!-- CHANGED v2: added -->
**Maps to**: total-business (LIMITED) | **Audience**: external (degraded) | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE='SALES_DATA'`) | **Source**: Postgres MCP

For orgs that send only summary `sales_data` (41 orgs in the census) — no `portal_invoices`/`portal_orders` line detail. `sales_data` carries `amount_invoiced` / `amount_on_order` keyed by `base_item_code` + `bill_to_code`, with only `est_ship_date` (no true invoice/order date), so it has **no reliable per-period transaction grain**. Do NOT produce monthly trends, capture rates, or per-customer penetration. Report a single LIMITED total-business figure with an explicit caveat.

Verified columns (2026-06-25): `organization_id`, `base_item_code`, `bill_to_code`, `ship_to_code`, `quantity_invoiced`, `amount_invoiced`, `qty_on_order`, `amount_on_order`, `est_ship_date`, `display_quantity`.

```sql
SELECT
  COUNT(*)                                          AS sales_data_rows,
  COUNT(DISTINCT bill_to_code)                      AS distinct_customers,
  COUNT(DISTINCT base_item_code)                    AS distinct_items,
  ROUND(SUM(COALESCE(amount_invoiced,0))::numeric, 2) AS total_business_invoiced_limited,
  ROUND(SUM(COALESCE(amount_on_order,0))::numeric, 2) AS total_on_order_limited
FROM sales_data
WHERE organization_id = {{ORG_ID}}
HAVING SUM(COALESCE(amount_invoiced,0)) > 0   -- pilot refinement #1: rows with $0 dollars produce NO row → suppress, never report a $0 total
```

> **Dollar guard (pilot refinement #1)**: this query returns **no row** when `sales_data` carries zero invoiced dollars. That is intentional — an org with `sales_data` rows but `$0` `amount_invoiced` (e.g. client `da`) has `TOTAL_BUSINESS_SOURCE='NONE'` from Q-PROV-00 and must **not** appear in the report with a $0 "total business." Suppress the section entirely and flag the org for a real feed.

**External claim rules**: Present `total_business_invoiced_limited` as "total business (summary)" with confidence LIMITED. Never derive a capture rate, trend, or channel split from `sales_data` alone — there is no line/period grain (`est_ship_date` is a forward estimate, not a sales date). Label the figure "as provided" since the period it represents is org-defined.

### Portal Orders ERP Enrichment Preflight

**Run during Stage 1 preflight (§1.3) when `HAS_PORTAL_ORDERS = true`:**

```sql
SELECT
  MAX(order_date) AS most_recent_erp_order,
  EXTRACT(DAY FROM NOW() - MAX(order_date))::int AS days_since_last_erp_order,
  COUNT(DISTINCT CASE WHEN rep_name IS NOT NULL AND rep_name != '' THEN rep_name END) AS distinct_rep_names,
  COUNT(DISTINCT CASE WHEN customer_bill_to_number IS NOT NULL THEN customer_bill_to_number END) AS distinct_bill_to_customers
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months'
```

**Set from results:**
- `PORTAL_ORDERS_FRESH` — true if `days_since_last_erp_order <= 60`
- `PORTAL_REP_DATA_PRESENT` — true if `distinct_rep_names > 0`
- `PORTAL_CUSTOMER_DATA_PRESENT` — true if `distinct_bill_to_customers > 0`

---

### Q-51: Rep-Level eCat Capture
**Maps to**: VM-51 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS} + `PORTAL_REP_DATA_PRESENT`) | **Source**: Postgres MCP

<!-- CHANGED v2: rep total business now = invoiced net_amount. portal_invoices has NO rep_name (only rep_number), so we bridge rep_number→rep_name via portal_orders. Falls back to rep_number when no name is known. If TOTAL_BUSINESS_SOURCE='ORDERS', use the prior portal_orders CTE (booked GMV, confidence PARTIAL). -->
<!-- ECAT-NUMERATOR -->
```sql
WITH rep_names AS (   -- bridge: invoices carry rep_number only
  SELECT DISTINCT rep_number, rep_name
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name != ''
),
erp_rep AS (
  SELECT
    COALESCE(rn.rep_name, pi.rep_number) AS rep_name,
    pi.rep_number,
    COUNT(*) AS erp_orders,
    ROUND(SUM(pi.net_amount)::numeric, 2) AS erp_gmv,   -- invoiced total business
    COUNT(DISTINCT pi.customer_bill_to_number) AS erp_customers
  FROM portal_invoices pi
  LEFT JOIN rep_names rn ON rn.rep_number = pi.rep_number
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND pi.rep_number IS NOT NULL AND pi.rep_number != ''
  GROUP BY COALESCE(rn.rep_name, pi.rep_number), pi.rep_number
),
ecat_rep AS (
  SELECT
    COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name,
    COUNT(*) AS ecat_orders,
    ROUND(SUM(total)::numeric, 2) AS ecat_gmv,
    COUNT(DISTINCT customer_num) AS ecat_customers
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at >= NOW() - INTERVAL '12 months'
    AND order_source = 'ipad'
  GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
)
SELECT
  e.rep_name,
  e.rep_number,
  e.erp_orders,
  e.erp_gmv,
  e.erp_customers,
  COALESCE(ec.ecat_orders, 0) AS ecat_orders,
  COALESCE(ec.ecat_gmv, 0) AS ecat_gmv,
  COALESCE(ec.ecat_customers, 0) AS ecat_customers,
  ROUND(100.0 * COALESCE(ec.ecat_gmv, 0) / NULLIF(e.erp_gmv, 0), 1) AS ecat_capture_pct
FROM erp_rep e
LEFT JOIN ecat_rep ec ON LOWER(TRIM(ec.rep_name)) = LOWER(TRIM(e.rep_name))
ORDER BY e.erp_gmv DESC
LIMIT 25
```

**Join notes**: Rep name matching between `portal_orders.rep_name` and `orders.rep_first_name || ' ' || rep_last_name` uses case-insensitive trimmed comparison. Imperfect matches are expected — reps appearing in ERP but not matched to eCat show `ecat_*` columns as 0, which is analytically correct (they have ERP business but no eCat activity). Do not drop rows for join mismatches.

**External claim rules**: Per-rep eCat capture rate as a percentage of their total business. "Rep X processes Y% of their total business through eCat." Reps with 0% capture are legitimate findings — they sell but don't use eCat. Never say "total business" means "eCat business." Never use "ERP" — use "total business" or "all-channel business." Never expose `rep_number` in client-facing output.

---

### Q-52: Customer-Level eCat Penetration
**Maps to**: VM-52 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS} + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

<!-- CHANGED v2: per-customer total business now = invoiced net_amount (matches client Sales Portal). erp_gmv column now means invoiced total business; erp_orders = invoice count. customer_bill_to_* exist on portal_invoices so this is a clean swap. ORDERS fallback = prior portal_orders CTE. -->
<!-- ECAT-NUMERATOR -->
```sql
WITH erp_customer AS (
  SELECT
    customer_bill_to_number AS customer_code,
    MAX(customer_bill_to_name) AS customer_name,
    MAX(customer_bill_to_state) AS state,
    COUNT(*) AS erp_orders,
    ROUND(SUM(net_amount)::numeric, 2) AS erp_gmv
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND customer_bill_to_number IS NOT NULL
  GROUP BY customer_bill_to_number
),
ecat_customer AS (
  SELECT
    customer_num,
    COUNT(*) AS ecat_orders,
    ROUND(SUM(total)::numeric, 2) AS ecat_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at >= NOW() - INTERVAL '12 months'
    AND customer_num IS NOT NULL
  GROUP BY customer_num
)
SELECT
  e.customer_code,
  e.customer_name,
  e.state,
  e.erp_orders,
  e.erp_gmv,
  COALESCE(ec.ecat_orders, 0) AS ecat_orders,
  COALESCE(ec.ecat_gmv, 0) AS ecat_gmv,
  ROUND(100.0 * COALESCE(ec.ecat_gmv, 0) / NULLIF(e.erp_gmv, 0), 1) AS ecat_penetration_pct
FROM erp_customer e
LEFT JOIN ecat_customer ec ON ec.customer_num = e.customer_code
ORDER BY e.erp_gmv DESC
LIMIT 30
```

**External claim rules**: Per-customer eCat penetration as a percentage of their total business. "Your top account does $X in total business — Y% flows through eCat." Customers with 0% penetration are legitimate findings. Never use "ERP" — use "total business" or "all-channel business." Never expose `customer_code` as a raw identifier in prose — use the customer name.

---

### Q-53: Unactivated High-Value ERP Accounts
**Maps to**: VM-53 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS} + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

<!-- CHANGED v2: "high-value" now ranks by invoiced total business (net_amount), so the unactivated-account opportunity is sized by real sales, not booked-order headers. ORDERS fallback = prior portal_orders CTE. -->
<!-- ECAT-NUMERATOR -->
```sql
WITH erp_active AS (
  SELECT
    customer_bill_to_number AS customer_code,
    MAX(customer_bill_to_name) AS customer_name,
    MAX(customer_bill_to_state) AS state,
    COUNT(*) AS erp_orders,
    ROUND(SUM(net_amount)::numeric, 2) AS erp_gmv
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND customer_bill_to_number IS NOT NULL
  GROUP BY customer_bill_to_number
),
any_ecat_ever AS (   -- "activated" = has ≥1 CONFIRMED eCat order; quote-only accounts count as unactivated opportunity
  SELECT DISTINCT customer_num
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND customer_num IS NOT NULL
)
SELECT
  e.customer_code,
  e.customer_name,
  e.state,
  e.erp_orders,
  e.erp_gmv
FROM erp_active e
LEFT JOIN any_ecat_ever ec ON ec.customer_num = e.customer_code
WHERE ec.customer_num IS NULL
ORDER BY e.erp_gmv DESC
LIMIT 20
```

**External claim rules**: High-value accounts that have never placed an eCat order despite active total business. "These X accounts represent $Y in annual business and haven't yet used the platform." This is an activation opportunity, not a failure — frame constructively. Never use "ERP" — use "total business." Never say "these customers don't use your platform" — they may use other channels productively.

---

### Q-54: Geographic eCat Penetration
**Maps to**: VM-54 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS} + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

<!-- CHANGED v2: per-state total business now = invoiced net_amount. customer_bill_to_state exists on portal_invoices → clean swap. ORDERS fallback = prior portal_orders CTE. -->
<!-- ECAT-NUMERATOR -->
```sql
WITH erp_geo AS (
  SELECT
    customer_bill_to_state AS state,
    COUNT(DISTINCT customer_bill_to_number) AS erp_customers,
    COUNT(*) AS erp_orders,
    ROUND(SUM(net_amount)::numeric, 2) AS erp_gmv
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND customer_bill_to_state IS NOT NULL AND customer_bill_to_state != ''
  GROUP BY customer_bill_to_state
),
ecat_geo AS (
  SELECT
    c.billing_state AS state,
    COUNT(DISTINCT o.customer_num) AS ecat_customers,
    COUNT(DISTINCT o.id) AS ecat_orders,
    ROUND(SUM(o.total)::numeric, 2) AS ecat_gmv
  FROM orders o
  JOIN customers c ON c.code = o.customer_num AND c.organization_id = o.organization_id
  WHERE o.organization_id = {{ORG_ID}}
    AND o.is_submitted = true
    AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL) AND o.total < 5000000
    AND COALESCE(NULLIF(TRIM(o.order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND o.order_type NOT ILIKE 'HFC%' AND o.order_type NOT ILIKE 'Hold%' AND o.order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND o.created_at >= NOW() - INTERVAL '12 months'
    AND c.billing_state IS NOT NULL AND c.billing_state != ''
  GROUP BY c.billing_state
)
SELECT
  COALESCE(e.state, ec.state) AS state,
  COALESCE(e.erp_customers, 0) AS erp_customers,
  COALESCE(e.erp_orders, 0) AS erp_orders,
  COALESCE(e.erp_gmv, 0) AS erp_gmv,
  COALESCE(ec.ecat_customers, 0) AS ecat_customers,
  COALESCE(ec.ecat_orders, 0) AS ecat_orders,
  COALESCE(ec.ecat_gmv, 0) AS ecat_gmv,
  ROUND(100.0 * COALESCE(ec.ecat_gmv, 0) / NULLIF(COALESCE(e.erp_gmv, 0), 0), 1) AS ecat_penetration_pct
FROM erp_geo e
FULL OUTER JOIN ecat_geo ec ON ec.state = e.state
ORDER BY COALESCE(e.erp_gmv, 0) DESC
LIMIT 20
```

**External claim rules**: Per-state eCat penetration as a share of total business. "California is your #1 market by total business — X% flows through eCat." States with high ERP volume but low eCat penetration are geographic expansion opportunities. Never use "ERP" — use "total business." Never frame low penetration as failure — it may reflect legitimate multi-channel business or market characteristics.

---

### Q-59: Fill Rate & Backorder Revenue Impact
**Maps to**: VM-59 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `HAS_INVENTORY`) | **Source**: Postgres MCP

Calculates org-level fill rate from `portal_order_items` and identifies the top items currently on backorder with their annualized revenue exposure.

```sql
WITH fill_rate AS (
  SELECT
    ROUND(100.0 * SUM(poi.quantity_invoiced) / NULLIF(SUM(poi.quantity_ordered), 0), 1) AS org_fill_rate_pct,
    SUM(poi.quantity_ordered) AS total_qty_ordered,
    SUM(poi.quantity_invoiced) AS total_qty_invoiced,
    SUM(poi.quantity_ordered - poi.quantity_invoiced) AS total_qty_unfilled,
    COUNT(DISTINCT poi.order_number) AS orders_with_items
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
),
backorder_items AS (
  SELECT
    poi.item_number,
    COALESCE(p.long_description, poi.description) AS item_description,
    COALESCE(p.category_code, 'Uncategorized') AS category,
    SUM(poi.quantity_backordered) AS total_qty_backordered,
    COUNT(DISTINCT po.customer_bill_to_number) AS affected_customers,
    COUNT(DISTINCT poi.order_number) AS affected_orders,
    ROUND(AVG(poi.unit_price)::numeric, 2) AS avg_unit_price,
    ROUND((SUM(poi.quantity_backordered) * AVG(poi.unit_price))::numeric, 2) AS backorder_exposure
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  LEFT JOIN products p ON p.item_number = poi.item_number AND p.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '6 months'
    AND poi.quantity_backordered > 0
  GROUP BY poi.item_number, COALESCE(p.long_description, poi.description), COALESCE(p.category_code, 'Uncategorized')
),
item_velocity AS (
  SELECT
    poi.item_number,
    COUNT(DISTINCT po.customer_bill_to_number) AS annual_buyers,
    SUM(poi.quantity_ordered) AS annual_qty,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS annual_revenue
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
  GROUP BY poi.item_number
)
SELECT
  'ORG_SUMMARY' AS row_type,
  NULL AS item_number,
  NULL AS item_description,
  NULL AS category,
  (SELECT org_fill_rate_pct FROM fill_rate) AS fill_rate_pct,
  (SELECT total_qty_unfilled FROM fill_rate) AS total_unfilled,
  NULL AS qty_backordered,
  NULL AS affected_customers,
  NULL AS avg_unit_price,
  NULL AS backorder_exposure,
  NULL AS annual_revenue,
  NULL AS annual_buyers
UNION ALL
SELECT
  'ITEM' AS row_type,
  b.item_number,
  b.item_description,
  b.category,
  NULL AS fill_rate_pct,
  NULL AS total_unfilled,
  b.total_qty_backordered AS qty_backordered,
  b.affected_customers,
  b.avg_unit_price,
  b.backorder_exposure,
  v.annual_revenue,
  v.annual_buyers
FROM backorder_items b
LEFT JOIN item_velocity v ON v.item_number = b.item_number
ORDER BY row_type ASC, backorder_exposure DESC NULLS LAST
LIMIT 16
```

**Result format**: Row 1 has `row_type = 'ORG_SUMMARY'` with the org fill rate and total unfilled quantity. Rows 2–16 have `row_type = 'ITEM'` with per-item backorder details sorted by exposure.

**Interpretation**: Fill rate measures what percentage of ordered units actually ship. Backorder exposure = units currently backordered × average unit price. Combined with annual revenue, this quantifies how much ongoing business each backordered SKU represents — if the backorder causes reorder decay, the annual revenue figure is what's at risk.

**External claim rules**: "Your fill rate is X%. Y items are currently on backorder, impacting Z customers. The top 5 impacted SKUs represent $A in annualized revenue." Always hedge the causal claim: "Backorders correlate with longer reorder intervals — projected revenue at risk is estimated at $B." Use "order fulfillment rate" (not "fill rate" from a technical standpoint — both are acceptable). Never use "ERP" or "portal_order_items." Never expose `item_number` without `item_description`.

---

### Q-55: Category-Level Competitive Displacement
**Maps to**: VM-55 | **Audience**: external | **Status**: conditional (gate: `TOTAL_BUSINESS_SOURCE='INVOICES'`) | **Source**: Postgres MCP

Detects categories where total business grew but eCat's share declined — a signal that dollars are going to competitors. Compares current quarter vs. prior quarter for each product category.

<!-- CHANGED v2: both total and eCat-attributed category dollars now come from INVOICED lines (portal_invoice_items prorated by discounts), so the share math is internally consistent and the denominator equals real sales. Requires TOTAL_BUSINESS_SOURCE='INVOICES'; if only orders exist, fall back to the prior portal_order_items version and label confidence PARTIAL. Line amount = quantity_invoiced*(unit_price-unit_price_discount)-extended_price_discount. -->
```sql
WITH total_by_category AS (
  SELECT
    COALESCE(p.category_code, 'Uncategorized') AS category,
    SUM(CASE WHEN pi.invoice_date >= NOW() - INTERVAL '90 days'
      THEN COALESCE(pii.quantity_invoiced,0)*(COALESCE(pii.unit_price,0)-COALESCE(pii.unit_price_discount,0))-COALESCE(pii.extended_price_discount,0) ELSE 0 END) AS current_total_gmv,
    SUM(CASE WHEN pi.invoice_date BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days'
      THEN COALESCE(pii.quantity_invoiced,0)*(COALESCE(pii.unit_price,0)-COALESCE(pii.unit_price_discount,0))-COALESCE(pii.extended_price_discount,0) ELSE 0 END) AS prior_total_gmv
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN NOW() - INTERVAL '180 days' AND CURRENT_DATE + INTERVAL '90 days'
  GROUP BY COALESCE(p.category_code, 'Uncategorized')
  HAVING SUM(CASE WHEN pi.invoice_date >= NOW() - INTERVAL '90 days'
    THEN COALESCE(pii.quantity_invoiced,0)*(COALESCE(pii.unit_price,0)-COALESCE(pii.unit_price_discount,0))-COALESCE(pii.extended_price_discount,0) ELSE 0 END) > 0
),
ecat_by_category AS (
  SELECT
    COALESCE(p.category_code, 'Uncategorized') AS category,
    SUM(CASE WHEN pi.invoice_date >= NOW() - INTERVAL '90 days'
      THEN COALESCE(pii.quantity_invoiced,0)*(COALESCE(pii.unit_price,0)-COALESCE(pii.unit_price_discount,0))-COALESCE(pii.extended_price_discount,0) ELSE 0 END) AS current_ecat_gmv,
    SUM(CASE WHEN pi.invoice_date BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days'
      THEN COALESCE(pii.quantity_invoiced,0)*(COALESCE(pii.unit_price,0)-COALESCE(pii.unit_price_discount,0))-COALESCE(pii.extended_price_discount,0) ELSE 0 END) AS prior_ecat_gmv
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.ecat_item_number AND p.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN NOW() - INTERVAL '180 days' AND CURRENT_DATE + INTERVAL '90 days'
    AND pii.ecat_item_number IS NOT NULL
  GROUP BY COALESCE(p.category_code, 'Uncategorized')
)
SELECT
  t.category,
  ROUND(t.prior_total_gmv::numeric, 2) AS prior_total_gmv,
  ROUND(t.current_total_gmv::numeric, 2) AS current_total_gmv,
  ROUND(100.0 * (t.current_total_gmv - t.prior_total_gmv) / NULLIF(t.prior_total_gmv, 0), 1) AS total_growth_pct,
  ROUND(COALESCE(e.prior_ecat_gmv, 0)::numeric, 2) AS prior_ecat_gmv,
  ROUND(COALESCE(e.current_ecat_gmv, 0)::numeric, 2) AS current_ecat_gmv,
  ROUND(100.0 * COALESCE(e.current_ecat_gmv, 0) / NULLIF(t.current_total_gmv, 0), 1) AS current_ecat_share_pct,
  ROUND(100.0 * COALESCE(e.prior_ecat_gmv, 0) / NULLIF(t.prior_total_gmv, 0), 1) AS prior_ecat_share_pct,
  ROUND(
    (100.0 * COALESCE(e.current_ecat_gmv, 0) / NULLIF(t.current_total_gmv, 0))
    - (100.0 * COALESCE(e.prior_ecat_gmv, 0) / NULLIF(t.prior_total_gmv, 0)),
  1) AS ecat_share_change_ppts
FROM total_by_category t
LEFT JOIN ecat_by_category e ON e.category = t.category
WHERE t.prior_total_gmv > 0
ORDER BY t.current_total_gmv DESC
LIMIT 15
```

**Interpretation**: A category where `total_growth_pct > 0` (total business grew) but `ecat_share_change_ppts < 0` (eCat share dropped) is a **competitive displacement signal** — the customer is spending more overall in that category, but less of it flows through your platform. The difference represents dollars likely going to a competitor.

**Displacement dollar calculation**: `(prior_ecat_share_pct / 100 * current_total_gmv) - current_ecat_gmv` = the GMV gap if eCat had maintained its prior share. This is the estimated displaced revenue.

**External claim rules**: "In [Category], total business grew X% but your platform share dropped Y percentage points — an estimated $Z shifted to other sources." Always hedge: "estimated," "likely," "suggests competitive activity." Never say "lost to competitors" definitively — could be channel shift, not competitive loss. Never use "ERP" or "portal_order_items."

---

### Q-56: Per-Rep Capture Rate Trend
**Maps to**: VM-56 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `PORTAL_REP_DATA_PRESENT`) | **Source**: Postgres MCP

Compares each rep's eCat capture rate (eCat share of their total business) between current and prior quarter to detect reps whose capture rate is declining.

<!-- ECAT-NUMERATOR -->
```sql
WITH rep_current AS (
  SELECT
    rep_name,
    COUNT(*) AS current_total_orders,
    ROUND(SUM(total_amount)::numeric, 2) AS current_total_gmv
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '90 days'
    AND rep_name IS NOT NULL AND rep_name != ''
  GROUP BY rep_name
),
rep_prior AS (
  SELECT
    rep_name,
    COUNT(*) AS prior_total_orders,
    ROUND(SUM(total_amount)::numeric, 2) AS prior_total_gmv
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days'
    AND rep_name IS NOT NULL AND rep_name != ''
  GROUP BY rep_name
),
ecat_current AS (
  SELECT
    COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name,
    COUNT(*) AS current_ecat_orders,
    ROUND(SUM(total)::numeric, 2) AS current_ecat_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at >= NOW() - INTERVAL '90 days'
    AND order_source = 'ipad'
  GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
),
ecat_prior AS (
  SELECT
    COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name,
    COUNT(*) AS prior_ecat_orders,
    ROUND(SUM(total)::numeric, 2) AS prior_ecat_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at BETWEEN NOW() - INTERVAL '180 days' AND NOW() - INTERVAL '90 days'
    AND order_source = 'ipad'
  GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
)
SELECT
  rc.rep_name,
  rc.current_total_gmv,
  rp.prior_total_gmv,
  COALESCE(ec.current_ecat_gmv, 0) AS current_ecat_gmv,
  COALESCE(ep.prior_ecat_gmv, 0) AS prior_ecat_gmv,
  ROUND(100.0 * COALESCE(ec.current_ecat_gmv, 0) / NULLIF(rc.current_total_gmv, 0), 1) AS current_capture_pct,
  ROUND(100.0 * COALESCE(ep.prior_ecat_gmv, 0) / NULLIF(rp.prior_total_gmv, 0), 1) AS prior_capture_pct,
  ROUND(
    (100.0 * COALESCE(ec.current_ecat_gmv, 0) / NULLIF(rc.current_total_gmv, 0))
    - (100.0 * COALESCE(ep.prior_ecat_gmv, 0) / NULLIF(rp.prior_total_gmv, 0)),
  1) AS capture_change_ppts
FROM rep_current rc
LEFT JOIN rep_prior rp ON LOWER(TRIM(rp.rep_name)) = LOWER(TRIM(rc.rep_name))
LEFT JOIN ecat_current ec ON LOWER(TRIM(ec.rep_name)) = LOWER(TRIM(rc.rep_name))
LEFT JOIN ecat_prior ep ON LOWER(TRIM(ep.rep_name)) = LOWER(TRIM(rc.rep_name))
WHERE rp.prior_total_gmv > 0
  AND rc.current_total_gmv > 0
ORDER BY rc.current_total_gmv DESC
LIMIT 20
```

**Join notes**: Same case-insensitive trim matching as Q-51 between `portal_orders.rep_name` and `orders` rep names. Imperfect matches expected — reps in ERP with no eCat match show 0% capture rate, which is analytically correct.

**Interpretation**: A rep where `current_total_gmv > prior_total_gmv` (their accounts are spending more) but `capture_change_ppts < 0` (their eCat share is declining) indicates competitive displacement at the rep level — their customers are growing but putting less through your platform. The rep-level view makes it coachable.

**External claim rules**: "Rep X's accounts are spending Y% more overall, but their platform capture rate dropped from Z% to W%." Frame as coaching opportunity, not failure. Never expose `rep_number`. Never use "ERP" — use "total business."

---

### Q-57: Cross-Sell Whitespace by Category
**Maps to**: VM-57 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

Identifies categories where a customer's peer group is buying but the customer is not — quantified as addressable whitespace dollars. "Peers" = other customers in the same annual spend tier (within 50%–200% of their GMV).

```sql
WITH customer_gmv AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    ROUND(SUM(total_amount)::numeric, 2) AS annual_gmv
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
    AND customer_bill_to_number IS NOT NULL
  GROUP BY customer_bill_to_number, customer_bill_to_name
  HAVING SUM(total_amount) > 0
),
top_customers AS (
  SELECT * FROM customer_gmv ORDER BY annual_gmv DESC LIMIT 20
),
customer_categories AS (
  SELECT
    po.customer_bill_to_number,
    COALESCE(p.category_code, 'Uncategorized') AS category,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS category_gmv
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  LEFT JOIN products p ON p.item_number = poi.item_number AND p.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY po.customer_bill_to_number, COALESCE(p.category_code, 'Uncategorized')
  HAVING SUM(poi.quantity_ordered * poi.unit_price) > 0
),
org_category_stats AS (
  SELECT
    category,
    COUNT(DISTINCT customer_bill_to_number) AS buyers_in_category,
    ROUND(AVG(category_gmv)::numeric, 2) AS avg_category_gmv,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY category_gmv)::numeric, 2) AS median_category_gmv
  FROM customer_categories
  WHERE customer_bill_to_number IN (SELECT customer_bill_to_number FROM customer_gmv WHERE annual_gmv > 0)
  GROUP BY category
  HAVING COUNT(DISTINCT customer_bill_to_number) >= 3
),
all_categories AS (
  SELECT DISTINCT category FROM org_category_stats
),
gaps AS (
  SELECT
    tc.customer_bill_to_number,
    tc.customer_bill_to_name,
    tc.annual_gmv,
    ac.category AS missing_category,
    ocs.buyers_in_category,
    ocs.median_category_gmv AS peer_median_spend,
    ocs.avg_category_gmv AS peer_avg_spend
  FROM top_customers tc
  CROSS JOIN all_categories ac
  LEFT JOIN customer_categories cc ON cc.customer_bill_to_number = tc.customer_bill_to_number
    AND cc.category = ac.category
  JOIN org_category_stats ocs ON ocs.category = ac.category
  WHERE cc.category IS NULL
    AND ac.category != 'Uncategorized'
    AND ocs.buyers_in_category >= 5
)
SELECT
  customer_bill_to_name,
  missing_category,
  annual_gmv AS customer_annual_gmv,
  peer_median_spend,
  buyers_in_category AS peers_buying,
  peer_median_spend AS addressable_gap
FROM gaps
ORDER BY peer_median_spend DESC, customer_annual_gmv DESC
LIMIT 20
```

**Interpretation**: Each row represents a category that a top customer does NOT buy but that a meaningful number of other accounts (≥5) DO buy. The `peer_median_spend` is the median annual spend in that category across buyers — this serves as the addressable whitespace estimate for each gap.

**Org-level aggregation for the section**: Sum `addressable_gap` across all rows (deduplicating by category) to get the total org whitespace figure. Group by category to show "X categories have untapped potential across your top accounts."

**External claim rules**: "Your top 20 accounts have zero purchases in X categories where an average of Y other customers spend $Z. Combined addressable whitespace: estimated $W." Always hedge: "estimated," "addressable," "if adoption matched peer behavior." Never guarantee these dollars are capturable — they represent opportunity, not certainty. Never use "ERP" — use "your account base" or "similar accounts." Never expose `customer_bill_to_number`.

---

### Q-58: Market Commitment Conversion
**Maps to**: VM-58 | **Audience**: external | **Status**: conditional (gate: `HAS_COMMITMENT_DATA`) | **Source**: Postgres MCP

Measures how effectively market commitments convert to actual orders. Expands committed items from `commitment_reports.items` (jsonb array), then cross-references against `portal_order_items` placed within 90 days of the commitment date.

```sql
WITH commitments_expanded AS (
  SELECT
    cr.id AS commitment_id,
    cr.bill_to_code,
    cr.market_code,
    cr.created_at AS commitment_date,
    item_elem->>'base_item_code' AS committed_item,
    COALESCE((item_elem->>'commitment_quantity')::int, 0) AS committed_qty
  FROM commitment_reports cr,
    jsonb_array_elements(cr.items) AS item_elem
  WHERE cr.organization_id = {{ORG_ID}}
    AND cr.items IS NOT NULL
    AND jsonb_array_length(cr.items) > 0
    AND COALESCE((item_elem->>'commitment_quantity')::int, 0) > 0
    AND cr.market_code IS NOT NULL
),
conversions AS (
  SELECT
    ce.market_code,
    ce.committed_item,
    ce.bill_to_code,
    ce.committed_qty,
    COALESCE(SUM(poi.quantity_ordered), 0) AS ordered_qty
  FROM commitments_expanded ce
  LEFT JOIN portal_orders po
    ON po.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number = ce.bill_to_code
    AND po.order_date BETWEEN ce.commitment_date AND ce.commitment_date + INTERVAL '90 days'
  LEFT JOIN portal_order_items poi
    ON poi.order_number = po.order_number
    AND poi.organization_id = po.organization_id
    AND poi.item_number = ce.committed_item
  GROUP BY ce.market_code, ce.committed_item, ce.bill_to_code, ce.committed_qty
)
SELECT
  ce.market_code,
  MIN(ce.commitment_date)::date AS market_start_date,
  MAX(ce.commitment_date)::date AS market_end_date,
  COUNT(DISTINCT ce.bill_to_code) AS customers_committing,
  COUNT(DISTINCT ce.committed_item) AS total_committed_items,
  SUM(ce.committed_qty) AS total_committed_qty,
  COUNT(DISTINCT CASE WHEN c.ordered_qty > 0 THEN c.committed_item END) AS items_converted,
  ROUND(
    COUNT(DISTINCT CASE WHEN c.ordered_qty > 0 THEN c.committed_item END)::numeric
    / NULLIF(COUNT(DISTINCT ce.committed_item), 0) * 100, 1
  ) AS item_conversion_pct,
  SUM(c.ordered_qty) AS total_ordered_qty,
  ROUND(
    SUM(c.ordered_qty)::numeric / NULLIF(SUM(ce.committed_qty), 0) * 100, 1
  ) AS qty_conversion_pct,
  COUNT(DISTINCT ce.committed_item) - COUNT(DISTINCT CASE WHEN c.ordered_qty > 0 THEN c.committed_item END) AS unrealized_items
FROM commitments_expanded ce
JOIN conversions c ON c.market_code = ce.market_code
  AND c.committed_item = ce.committed_item
  AND c.bill_to_code = ce.bill_to_code
GROUP BY ce.market_code
ORDER BY MIN(ce.commitment_date) DESC
```

**Interpretation**: Each row represents one market event (grouped by `market_code`). `market_start_date`/`market_end_date` show the commitment window. `item_conversion_pct` shows what fraction of committed SKUs received at least one order within 90 days. `qty_conversion_pct` shows total units ordered vs. committed. `unrealized_items` = committed SKUs with zero follow-through — these are potential lost sales or stalled decisions.

**External claim rules**: "At [Market], your accounts committed to X items and Y units. Within 90 days, Z% of those items converted to orders." Frame unrealized commitments as opportunity: "X items committed at market haven't yet converted — these may represent stalled buying decisions worth following up on." Never imply the customer failed. Never use "ERP" — use "your order history." Reference market codes by name (e.g., "High Point October 2025"). Never expose `bill_to_code`.

---

### Q-58b: Uncommitted Market Items In Stock
**Maps to**: VM-58b | **Audience**: external | **Status**: conditional (gate: `HAS_COMMITMENT_DATA` + `HAS_INVENTORY`) | **Source**: Postgres MCP

Extends Q-58 by identifying committed items that were never ordered AND are currently in stock — the most immediately actionable subset of unrealized commitments.

```sql
WITH commitments_expanded AS (
  SELECT
    cr.bill_to_code,
    cr.market_code,
    cr.created_at AS commitment_date,
    item_elem->>'base_item_code' AS committed_item,
    COALESCE((item_elem->>'commitment_quantity')::int, 0) AS committed_qty
  FROM commitment_reports cr,
    jsonb_array_elements(cr.items) AS item_elem
  WHERE cr.organization_id = {{ORG_ID}}
    AND cr.items IS NOT NULL
    AND jsonb_array_length(cr.items) > 0
    AND COALESCE((item_elem->>'commitment_quantity')::int, 0) > 0
    AND cr.market_code IS NOT NULL
    AND cr.created_at >= NOW() - INTERVAL '6 months'
),
ordered_items AS (
  SELECT DISTINCT poi.item_number
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  JOIN commitments_expanded ce ON ce.bill_to_code = po.customer_bill_to_number
    AND poi.item_number = ce.committed_item
    AND po.order_date BETWEEN ce.commitment_date AND ce.commitment_date + INTERVAL '90 days'
  WHERE poi.organization_id = {{ORG_ID}}
),
unrealized AS (
  SELECT
    ce.market_code,
    ce.committed_item,
    ce.bill_to_code,
    ce.committed_qty
  FROM commitments_expanded ce
  WHERE ce.committed_item NOT IN (SELECT item_number FROM ordered_items)
)
SELECT
  u.market_code,
  u.committed_item AS item_number,
  p.long_description AS item_description,
  COUNT(DISTINCT u.bill_to_code) AS customers_committed,
  SUM(u.committed_qty) AS total_committed_qty,
  i.qty_available AS current_stock,
  ROUND((COALESCE(i.qty_available, 0) * COALESCE(p.net_price, 0))::numeric, 2) AS stock_value
FROM unrealized u
LEFT JOIN products p ON p.item_number = u.committed_item AND p.organization_id = {{ORG_ID}} AND (p.deleted = false OR p.deleted IS NULL)
LEFT JOIN inventories i ON i.item_number = u.committed_item AND i.organization_id = {{ORG_ID}}
WHERE i.qty_available > 0
GROUP BY u.market_code, u.committed_item, p.long_description, i.qty_available, p.net_price
ORDER BY SUM(u.committed_qty) DESC
LIMIT 20
```

**Interpretation**: Each row is an item that was committed at market, never converted to an order within 90 days, AND is currently in stock. These are the most actionable unrealized commitments — the inventory exists, the buying intent was expressed, and the rep just needs to close.

**External claim rules**: "These X items were committed at market but never ordered — and they're all currently in stock. Combined committed quantity: Y units." Frame as the easiest possible action: "Your reps expressed intent for these items. The inventory is sitting in your warehouse. This is the shortest path to revenue." Never expose `bill_to_code`. Never use "ERP."

---

### Q-60: Price Erosion / Trade-Down Detection
**Maps to**: VM-60 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS`) | **Source**: Postgres MCP

Detects accounts whose average unit price is declining quarter-over-quarter — a signal that they're trading down to cheaper items or that pricing pressure is eroding margins.

```sql
WITH customer_quarterly AS (
  SELECT
    po.customer_bill_to_number,
    MAX(po.customer_bill_to_name) AS customer_bill_to_name,
    CASE
      WHEN po.order_date >= NOW() - INTERVAL '3 months' THEN 'current'
      ELSE 'prior'
    END AS period,
    AVG(poi.unit_price) AS avg_unit_price,
    SUM(poi.quantity_ordered * poi.unit_price) AS period_gmv,
    COUNT(DISTINCT po.order_number) AS order_count,
    COUNT(*) AS line_items
  FROM portal_orders po
  JOIN portal_order_items poi ON poi.order_number = po.order_number AND poi.organization_id = po.organization_id
  WHERE po.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '6 months'
    AND poi.unit_price > 0
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY po.customer_bill_to_number,
    CASE WHEN po.order_date >= NOW() - INTERVAL '3 months' THEN 'current' ELSE 'prior' END
  HAVING COUNT(*) >= 5
)
SELECT
  cur.customer_bill_to_name,
  ROUND(pri.avg_unit_price::numeric, 2) AS prior_avg_price,
  ROUND(cur.avg_unit_price::numeric, 2) AS current_avg_price,
  ROUND(((cur.avg_unit_price - pri.avg_unit_price) / NULLIF(pri.avg_unit_price, 0) * 100)::numeric, 1) AS price_change_pct,
  ROUND(cur.period_gmv::numeric, 2) AS current_quarter_gmv,
  ROUND(pri.period_gmv::numeric, 2) AS prior_quarter_gmv,
  cur.order_count AS current_orders,
  cur.line_items AS current_line_items
FROM customer_quarterly cur
JOIN customer_quarterly pri ON pri.customer_bill_to_number = cur.customer_bill_to_number
  AND pri.period = 'prior'
WHERE cur.period = 'current'
  AND ((cur.avg_unit_price - pri.avg_unit_price) / NULLIF(pri.avg_unit_price, 0) * 100) <= -4
ORDER BY cur.period_gmv DESC
LIMIT 20
```

**Interpretation**: Each row is a customer whose average unit price dropped 4%+ between prior quarter and current quarter (minimum 5 line items per quarter to filter noise). Grouped by `customer_bill_to_number` only (not name) to prevent duplicates when a customer's name varies across orders. Sorted by current GMV descending — high-value accounts trading down are the most urgent signals.

**Org-level aggregation**: Sum `current_quarter_gmv` across all declining accounts for "combined at-risk revenue." Count distinct accounts for "X accounts showing price erosion."

**External claim rules**: "X accounts are trending toward lower-priced items — average unit prices declined 4%+ quarter-over-quarter. Combined current-quarter business: $Y." Always hedge: "may indicate trading down, competitive pricing pressure, or shifting product mix." Never assert cause — only signal. Never expose `customer_bill_to_number`. Never use "ERP" — use "your order history."

---

### Q-61: New Introduction Adoption Gap
**Maps to**: VM-61 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + org has new items) | **Source**: Postgres MCP

Identifies new products (flagged `new_item = true`) and measures adoption across the customer base — which new items have traction, which have zero orders, and how top accounts compare.

```sql
WITH new_items AS (
  SELECT item_number, long_description, category_code, collection_code, net_price
  FROM products
  WHERE organization_id = {{ORG_ID}}
    AND new_item = true
    AND (deleted = false OR deleted IS NULL)
),
new_item_orders AS (
  SELECT
    poi.item_number,
    COUNT(DISTINCT po.customer_bill_to_number) AS unique_buyers,
    SUM(poi.quantity_ordered) AS total_qty_ordered,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT po.order_number) AS order_count
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND poi.item_number IN (SELECT item_number FROM new_items)
    AND po.order_date >= NOW() - INTERVAL '6 months'
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY poi.item_number
)
SELECT
  ni.item_number,
  ni.long_description AS description,
  ni.category_code AS category,
  COALESCE(nio.unique_buyers, 0) AS buyers,
  COALESCE(nio.total_qty_ordered, 0) AS qty_ordered,
  COALESCE(nio.total_revenue, 0) AS revenue,
  COALESCE(nio.order_count, 0) AS orders,
  ni.net_price AS list_price
FROM new_items ni
LEFT JOIN new_item_orders nio ON nio.item_number = ni.item_number
ORDER BY COALESCE(nio.total_revenue, 0) DESC
LIMIT 30
```

**Interpretation**: Each row is a new item with its adoption metrics. Items with `buyers = 0` have zero traction. The total count of new items vs. those with buyers gives the adoption rate. Top items by revenue show what's working; zero-buyer items show what isn't.

**Org-level aggregation**: Count total new items, count with ≥1 buyer, compute adoption rate. Sum revenue across adopted items. Flag zero-traction items count.

**External claim rules**: "You have X new introductions in your catalog. Y have been purchased by at least one account (Z% adoption). The top performers generated $W in 6-month revenue." For zero-traction items: "X new items have zero orders — these may need rep attention, merchandising support, or pricing review." Never expose item_number in client-facing text if it contains internal codes — use description. Never use "ERP."

---

### Q-62: Product Launch Velocity by Rep
**Maps to**: VM-62 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `HAS_NEW_ITEMS`) | **Source**: Postgres MCP

Measures which reps are selling new introductions vs. ignoring them. Per-rep new item adoption from order data.

```sql
WITH new_items AS (
  SELECT item_number
  FROM products
  WHERE organization_id = {{ORG_ID}}
    AND new_item = true
    AND (deleted = false OR deleted IS NULL)
),
rep_new_item_sales AS (
  SELECT
    COALESCE(NULLIF(TRIM(po.rep_name), ''), 'Unknown') AS rep_name,
    COUNT(DISTINCT poi.item_number) AS new_items_sold,
    COUNT(DISTINCT po.customer_bill_to_number) AS customers_buying_new,
    SUM(poi.quantity_ordered) AS new_item_qty,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS new_item_revenue,
    COUNT(DISTINCT po.order_number) AS orders_with_new_items
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND poi.item_number IN (SELECT item_number FROM new_items)
    AND po.order_date >= NOW() - INTERVAL '6 months'
    AND po.customer_bill_to_number IS NOT NULL
    AND UPPER(COALESCE(TRIM(po.rep_name), '')) NOT IN ('HOUSE ACCOUNT', 'UNKNOWN', '')
    AND COALESCE(TRIM(po.rep_name), '') NOT ILIKE '%showroom%'
    AND COALESCE(TRIM(po.rep_name), '') NOT ILIKE '%admin%'
    AND COALESCE(TRIM(po.rep_name), '') NOT ILIKE '%test%'
  GROUP BY COALESCE(NULLIF(TRIM(po.rep_name), ''), 'Unknown')
),
total_new_count AS (
  SELECT COUNT(*) AS total_new_items FROM new_items
)
SELECT
  r.rep_name,
  r.new_items_sold,
  t.total_new_items,
  ROUND((r.new_items_sold::numeric / NULLIF(t.total_new_items, 0) * 100), 1) AS adoption_pct,
  r.customers_buying_new,
  r.new_item_qty,
  r.new_item_revenue,
  r.orders_with_new_items
FROM rep_new_item_sales r
CROSS JOIN total_new_count t
ORDER BY r.new_item_revenue DESC
LIMIT 20
```

**Interpretation**: Each row is a rep showing how many unique new items they've sold, what % of the total new catalog that represents, and the revenue generated. Reps at the bottom with low `adoption_pct` are leaving new introductions on the table.

**External claim rules**: "Your top performer has sold X of Y new items. The bottom quartile has sold fewer than Z." Frame as opportunity: "Reps who showcase new items early generate X% more revenue from those lines." Never name individual reps without explicit org consent in report config. Use "your top seller" / "bottom quartile" phrasing. Never use "ERP."

---

### Q-63: Presentation-to-Order Conversion by Rep
**Maps to**: VM-63 | **Audience**: external | **Status**: conditional (gate: `MIXPANEL_USER_DATA_PRESENT`) | **Source**: BigQuery

Compares per-rep customer engagement activity (product searches, catalog generation, emails with a customer context) against actual orders submitted for those same customers. Measures conversion efficiency.

```sql
WITH selling_activity AS (
  SELECT
    LOWER(username) AS rep,
    selected_bill_to_code AS customer,
    COUNTIF(event_name = 'product_search') AS searches,
    COUNTIF(event_name = 'pdf_catalog_generated') AS catalogs_sent,
    COUNTIF(event_name = 'item_email_drafted') AS emails_sent,
    COUNTIF(event_name IN ('product_search', 'pdf_catalog_generated', 'item_email_drafted')) AS total_presentations,
    COUNTIF(event_name = 'order_submitted') AS orders_submitted
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE LOWER(COALESCE(organization_shortname, current_organization_shortname)) = '{{ORG_SHORTNAME}}'
    AND selected_bill_to_code IS NOT NULL
    AND selected_bill_to_code != ''
    AND username IS NOT NULL
    AND LOWER(username) NOT LIKE '%supercatsolutions.com%'
    AND LOWER(username) NOT LIKE '%test%'
    AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  GROUP BY rep, customer
  HAVING COUNTIF(event_name IN ('product_search', 'pdf_catalog_generated', 'item_email_drafted')) >= 3
)
SELECT
  rep,
  COUNT(DISTINCT customer) AS accounts_engaged,
  SUM(total_presentations) AS total_presentations,
  SUM(orders_submitted) AS total_orders,
  ROUND(SAFE_DIVIDE(SUM(orders_submitted), COUNT(DISTINCT customer)) * 100, 1) AS order_rate_pct,
  ROUND(SAFE_DIVIDE(SUM(orders_submitted), SUM(total_presentations)) * 100, 1) AS conversion_rate_pct,
  SUM(searches) AS total_searches,
  SUM(catalogs_sent) AS total_catalogs,
  SUM(emails_sent) AS total_emails
FROM selling_activity
GROUP BY rep
ORDER BY total_presentations DESC
LIMIT 20
```

**Interpretation**: Each row is a rep with their total customer engagement events vs. orders closed. `conversion_rate_pct` = orders / presentations. Low conversion with high activity = coaching opportunity (lots of activity, not closing). High conversion = efficient closer.

**External claim rules**: "Your most active rep presented to X accounts but converted Y% to orders." Frame low conversion constructively: "High-activity reps with lower conversion may benefit from targeted coaching on closing techniques or customer qualification." Never name individual reps by real name — use "Rep A", "top performer", "bottom quartile." Never expose `selected_bill_to_code`. Never use internal event names.

---

### Q-64: Rep Engagement vs Account Revenue
**Maps to**: VM-64 | **Audience**: external | **Status**: conditional (gate: `MIXPANEL_USER_DATA_PRESENT` + `HAS_PORTAL_ORDERS`) | **Source**: BigQuery

Correlates per-rep monthly engagement touches with customer revenue to quantify the relationship between engagement frequency and account productivity.

```sql
WITH monthly_touches AS (
  SELECT
    LOWER(username) AS rep,
    selected_bill_to_code AS customer,
    COUNT(*) AS touches,
    COUNT(DISTINCT DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))) AS active_days
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE LOWER(COALESCE(organization_shortname, current_organization_shortname)) = '{{ORG_SHORTNAME}}'
    AND selected_bill_to_code IS NOT NULL
    AND selected_bill_to_code != ''
    AND username IS NOT NULL
    AND LOWER(username) NOT LIKE '%supercatsolutions.com%'
    AND LOWER(username) NOT LIKE '%test%'
    AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  GROUP BY rep, customer
)
SELECT
  rep,
  COUNT(DISTINCT customer) AS accounts_touched,
  ROUND(AVG(touches), 1) AS avg_touches_per_account,
  ROUND(AVG(active_days), 1) AS avg_days_per_account,
  SUM(CASE WHEN touches >= 8 THEN 1 ELSE 0 END) AS high_engagement_accounts,
  SUM(CASE WHEN touches < 3 THEN 1 ELSE 0 END) AS low_engagement_accounts
FROM monthly_touches
GROUP BY rep
ORDER BY avg_touches_per_account DESC
LIMIT 20
```

**Interpretation**: Each row shows a rep's engagement distribution across their accounts. `high_engagement_accounts` (8+ touches in 90d) correlate with stronger revenue. `low_engagement_accounts` (< 3 touches) are under-served and represent growth opportunity.

**External claim rules**: "Reps who engage accounts 8+ times per quarter produce higher revenue per account. X accounts are receiving fewer than 3 touches — these are growth opportunities." Always hedge the causal claim: "correlate with" not "cause." Never name individual reps. Never expose `selected_bill_to_code`. Frame under-engagement as opportunity, not failure.

---

### Q-65: Selling vs Admin Time Ratio
**Maps to**: VM-65 | **Audience**: external | **Status**: conditional (gate: `MIXPANEL_USER_DATA_PRESENT`) | **Source**: BigQuery

Classifies each rep's app activity into "selling" events (customer-facing, revenue-generating) vs. "admin/browsing" events to surface time allocation patterns.

```sql
WITH classified_events AS (
  SELECT
    LOWER(username) AS rep,
    event_name,
    CASE
      WHEN event_name IN ('product_search', 'customer_selection', 'customer_search',
        'order_submitted', 'item_email_drafted', 'pdf_catalog_generated',
        'add_configured_item_to_order', 'add_kit_to_order', 'view_kit',
        'view_favorites', 'view_customer_orders', 'view_customer_on_order_items',
        'show_customer_sales_setting_changed', 'view_customer_smart_picks',
        'item_scanned', 'add_to_order_from_maybe_list', 'view_commitments',
        'view_customer_placements')
      THEN 'selling'
      ELSE 'admin'
    END AS activity_type
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE LOWER(COALESCE(organization_shortname, current_organization_shortname)) = '{{ORG_SHORTNAME}}'
    AND username IS NOT NULL
    AND LOWER(username) NOT LIKE '%supercatsolutions.com%'
    AND LOWER(username) NOT LIKE '%test%'
    AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
)
SELECT
  rep,
  COUNT(*) AS total_events,
  COUNTIF(activity_type = 'selling') AS selling_events,
  COUNTIF(activity_type = 'admin') AS admin_events,
  ROUND(SAFE_DIVIDE(COUNTIF(activity_type = 'selling'), COUNT(*)) * 100, 1) AS selling_pct,
  ROUND(SAFE_DIVIDE(COUNTIF(activity_type = 'admin'), COUNT(*)) * 100, 1) AS admin_pct
FROM classified_events
GROUP BY rep
HAVING COUNT(*) >= 20
ORDER BY selling_pct DESC
LIMIT 20
```

**Interpretation**: Each row is a rep ranked by selling activity percentage. Top sellers spend 70%+ of app time on revenue-generating activities. Reps with high admin % may need workflow optimization or are using the app differently (browsing vs. selling).

**External claim rules**: "Your top performers spend X% of their app time on customer-facing selling activities. The bottom quartile averages Y%." Frame constructively: "Increasing selling time allocation from Y% to X% correlates with Z% higher order volume." Never name individual reps. Never use event_name literals in prose. Say "customer-facing activities" not "product_search events."

---

### Q-66: Buyer-Within-Account Intelligence
**Maps to**: VM-66 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + org has populated `buyer_name`) | **Source**: Postgres MCP

Detects new buyer names appearing within existing accounts in the last 90 days — a signal of account expansion, stakeholder changes, or new decision-maker engagement.

```sql
WITH recent_buyers AS (
  SELECT
    po.customer_bill_to_number,
    po.customer_bill_to_name,
    LOWER(TRIM(po.buyer_name)) AS buyer,
    MIN(po.order_date) AS first_order_date,
    COUNT(DISTINCT po.order_number) AS order_count,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS buyer_revenue
  FROM portal_orders po
  JOIN portal_order_items poi ON poi.order_number = po.order_number AND poi.organization_id = po.organization_id
  WHERE po.organization_id = {{ORG_ID}}
    AND po.buyer_name IS NOT NULL
    AND TRIM(po.buyer_name) != ''
    AND po.customer_bill_to_number IS NOT NULL
    AND po.order_date >= NOW() - INTERVAL '6 months'
  GROUP BY po.customer_bill_to_number, po.customer_bill_to_name, LOWER(TRIM(po.buyer_name))
),
new_buyers AS (
  SELECT *
  FROM recent_buyers
  WHERE first_order_date >= NOW() - INTERVAL '90 days'
),
established_buyers AS (
  SELECT customer_bill_to_number, COUNT(DISTINCT buyer) AS existing_buyer_count
  FROM recent_buyers
  WHERE first_order_date < NOW() - INTERVAL '90 days'
  GROUP BY customer_bill_to_number
)
SELECT
  nb.customer_bill_to_name,
  COUNT(DISTINCT nb.buyer) AS new_buyers,
  COALESCE(eb.existing_buyer_count, 0) AS existing_buyers,
  SUM(nb.order_count) AS new_buyer_orders,
  SUM(nb.buyer_revenue) AS new_buyer_revenue,
  MIN(nb.first_order_date) AS earliest_new_buyer
FROM new_buyers nb
LEFT JOIN established_buyers eb ON eb.customer_bill_to_number = nb.customer_bill_to_number
GROUP BY nb.customer_bill_to_name, nb.customer_bill_to_number, eb.existing_buyer_count
HAVING COUNT(DISTINCT nb.buyer) >= 1
ORDER BY SUM(nb.buyer_revenue) DESC
LIMIT 20
```

**Interpretation**: Each row is an account with new buyer names detected in the last 90 days. New buyers represent expansion opportunities (new department, new store location, new decision-maker). Accounts with multiple new buyers are actively growing their purchasing scope.

**External claim rules**: "X of your top accounts have new buyers in the last 90 days — this signals active expansion. New buyers at [Account] have generated $Y in their first orders." Frame as opportunity: "New buyers typically expand to 2+ categories within 6 months. Early relationship building compounds." Never expose buyer_name or customer_bill_to_number. Use account name only.

---

### Q-67: Geographic Revenue Displacement
**Maps to**: VM-67 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

State-level analysis of where total business is growing but eCat capture share is declining — geographic displacement signals that competitors are gaining ground in specific markets.

```sql
WITH state_quarterly AS (
  SELECT
    COALESCE(NULLIF(TRIM(po.customer_ship_to_state), ''), 'Unknown') AS state,
    CASE
      WHEN po.order_date >= NOW() - INTERVAL '3 months' THEN 'current'
      ELSE 'prior'
    END AS period,
    SUM(poi.quantity_ordered * poi.unit_price) AS total_gmv,
    COUNT(DISTINCT po.customer_bill_to_number) AS active_customers,
    COUNT(DISTINCT po.order_number) AS order_count
  FROM portal_orders po
  JOIN portal_order_items poi ON poi.order_number = po.order_number AND poi.organization_id = po.organization_id
  WHERE po.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '6 months'
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY COALESCE(NULLIF(TRIM(po.customer_ship_to_state), ''), 'Unknown'),
    CASE WHEN po.order_date >= NOW() - INTERVAL '3 months' THEN 'current' ELSE 'prior' END
  HAVING SUM(poi.quantity_ordered * poi.unit_price) >= 5000
)
SELECT
  cur.state,
  ROUND(pri.total_gmv::numeric, 2) AS prior_gmv,
  ROUND(cur.total_gmv::numeric, 2) AS current_gmv,
  ROUND(((cur.total_gmv - pri.total_gmv) / NULLIF(pri.total_gmv, 0) * 100)::numeric, 1) AS gmv_change_pct,
  cur.active_customers AS current_customers,
  pri.active_customers AS prior_customers,
  cur.active_customers - pri.active_customers AS customer_change,
  cur.order_count AS current_orders
FROM state_quarterly cur
JOIN state_quarterly pri ON pri.state = cur.state AND pri.period = 'prior'
WHERE cur.period = 'current'
ORDER BY cur.total_gmv DESC
LIMIT 25
```

**Interpretation**: Each row is a state with quarter-over-quarter GMV comparison. States with declining GMV or customer count despite overall org growth signal geographic displacement. States with growing GMV and growing customers are strongholds.

**External claim rules**: "Your strongest state is [State] at $X (+Y% QoQ). [State] is showing decline: -Z% QoQ, losing N active customers." Frame declines as actionable: "States losing customers may benefit from rep coverage review or competitive response." Never attribute decline to specific causes — say "may indicate" or "signals." Never use internal field names.

---

### Q-68: Spending Contraction Detection (Historical Peak Comparison)
**Maps to**: VM-68 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT`) | **Source**: Postgres MCP

For each customer with sufficient history, compares their trailing-12-month spend to their own historical peak rolling-12-month total — surfacing accounts with demonstrated spending capacity that has contracted. Replaces the prior peer-group-average methodology which produced data artifacts from decile boundary clustering.

```sql
WITH monthly_spend AS (
  SELECT
    po.customer_bill_to_number,
    MAX(po.customer_bill_to_name) AS customer_bill_to_name,
    COALESCE(NULLIF(TRIM(po.customer_ship_to_state), ''), 'Unknown') AS primary_state,
    DATE_TRUNC('month', po.order_date) AS order_month,
    ROUND(SUM(poi.quantity_ordered * poi.unit_price)::numeric, 2) AS monthly_gmv
  FROM portal_orders po
  JOIN portal_order_items poi ON poi.order_number = po.order_number AND poi.organization_id = po.organization_id
  WHERE po.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number IS NOT NULL
  GROUP BY po.customer_bill_to_number,
    COALESCE(NULLIF(TRIM(po.customer_ship_to_state), ''), 'Unknown'),
    DATE_TRUNC('month', po.order_date)
),
rolling_12m AS (
  SELECT
    customer_bill_to_number,
    customer_bill_to_name,
    primary_state,
    order_month,
    SUM(monthly_gmv) OVER (
      PARTITION BY customer_bill_to_number
      ORDER BY order_month
      ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ) AS rolling_12m_spend,
    COUNT(*) OVER (
      PARTITION BY customer_bill_to_number
      ORDER BY order_month
      ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ) AS months_in_window
  FROM monthly_spend
),
customer_peaks AS (
  SELECT
    customer_bill_to_number,
    MAX(customer_bill_to_name) AS customer_bill_to_name,
    MAX(primary_state) AS primary_state,
    MAX(rolling_12m_spend) AS peak_spend,
    MAX(CASE WHEN rolling_12m_spend = (
      SELECT MAX(r2.rolling_12m_spend) FROM rolling_12m r2
      WHERE r2.customer_bill_to_number = rolling_12m.customer_bill_to_number
    ) THEN order_month END) AS peak_period_end
  FROM rolling_12m
  WHERE months_in_window >= 6
  GROUP BY customer_bill_to_number
),
current_spend AS (
  SELECT
    customer_bill_to_number,
    ROUND(SUM(monthly_gmv)::numeric, 2) AS customer_spend,
    COUNT(DISTINCT order_month) AS active_months
  FROM monthly_spend
  WHERE order_month >= DATE_TRUNC('month', NOW()) - INTERVAL '12 months'
  GROUP BY customer_bill_to_number
  HAVING SUM(monthly_gmv) >= 1000
)
SELECT
  cp.customer_bill_to_name,
  cp.primary_state,
  cs.customer_spend,
  ROUND(cp.peak_spend::numeric, 2) AS peak_spend,
  ROUND((cp.peak_spend - cs.customer_spend)::numeric, 2) AS gap_to_peak,
  ROUND((cs.customer_spend / NULLIF(cp.peak_spend, 0) * 100)::numeric, 1) AS current_vs_peak_pct,
  cs.active_months
FROM customer_peaks cp
JOIN current_spend cs ON cs.customer_bill_to_number = cp.customer_bill_to_number
WHERE cs.customer_spend < cp.peak_spend * 0.75
  AND cp.peak_spend >= 5000
ORDER BY (cp.peak_spend - cs.customer_spend) DESC
LIMIT 20
```

**Interpretation**: Each row is a customer whose current trailing-12-month spend is <75% of their own historical peak rolling-12-month total. This avoids the peer-group-average methodology which produced clustering artifacts at decile boundaries. The peak must be ≥$5K to exclude trivially small accounts. `gap_to_peak` quantifies the demonstrated spending capacity that has not been recaptured. `current_vs_peak_pct` shows what fraction of their peak they currently represent (e.g., 38% means they're spending about a third of what they used to). Accounts need ≥6 months of data within a rolling window to establish a meaningful peak.

**External claim rules**: "X accounts are spending below their historical peak. The combined contraction represents $Y in demonstrated capacity." Frame as recovery: "[Account] currently spends $X but historically peaked at $Z — a contraction of $W." Always use "demonstrated capacity," "historical peak," "contraction" — not "should be spending" or "underperforming." Never guarantee outcomes. Never expose bill_to_number. Use account name and state only.

---

### Q-69: Order Timing Distribution (Day-of-Week & Hour)
**Maps to**: VM-69 | **Audience**: external | **Status**: conditional (gate: `HAS_ORDERS`) | **Source**: Postgres MCP

Surfaces order submission patterns by day of week and hour of day. Reveals when reps are actively selling and whether there are systematic timing gaps (e.g., no Friday afternoon orders, no early-morning submissions) that suggest scheduling or workflow opportunities.

<!-- CHANGED v2 (Phase-B query hygiene, rep_intelligence_layer2_build §7.2, applied + live-validated cci 2026-06-29): `orders.submitted_at` does NOT exist → `submit_date`; `status NOT IN (...)` replaced with the actual submission/soft-delete flags (`is_submitted` / `is_marked_deleted`). This is eCat order timing (behavior), not total-business timing. -->
```sql
SELECT
  TRIM(TO_CHAR(o.submit_date, 'Day')) AS day_of_week,
  EXTRACT(DOW FROM o.submit_date) AS day_num,
  EXTRACT(HOUR FROM o.submit_date) AS hour_of_day,
  COUNT(*) AS order_count,
  ROUND(SUM(o.total)::numeric, 2) AS gmv,
  ROUND(AVG(o.total)::numeric, 2) AS avg_order_value
FROM orders o
WHERE o.organization_id = {{ORG_ID}}
  AND o.is_submitted = true
  AND (o.is_marked_deleted = false OR o.is_marked_deleted IS NULL)
  AND o.submit_date >= NOW() - INTERVAL '12 months'
GROUP BY
  TRIM(TO_CHAR(o.submit_date, 'Day')),
  EXTRACT(DOW FROM o.submit_date),
  EXTRACT(HOUR FROM o.submit_date)
ORDER BY day_num, hour_of_day
```

**Interpretation**: Each row shows orders submitted during a specific day+hour window. Peaks indicate when reps are most active in the selling workflow. Valleys indicate gaps — if competitors are ordering on Fridays and your reps aren't, that's a scheduling opportunity. The day-of-week distribution reveals whether selling is concentrated in early-week bursts or spread evenly. Hour-of-day reveals whether reps sell during traditional business hours or have extended selling windows.

**External claim rules**: "X% of your orders are placed Monday–Wednesday, with Friday accounting for only Y%. If your team added consistent Friday selling, that could represent $Z in additional weekly volume." Always hedge projections. Never expose `submit_date` as a raw timestamp. Frame gaps as scheduling opportunities, not rep failures. **This is eCat order timing (behavior), not total-business timing — label accordingly.**

---

### Q-70: Inactive Reps with Territory Revenue (Login Gaps)
**Maps to**: VM-70 | **Audience**: external | **Status**: conditional (gate: `HAS_PORTAL_ORDERS` + `PORTAL_REP_DATA_PRESENT`) | **Source**: Postgres MCP

Identifies reps who have not logged into the platform in 90+ days but manage territories with active revenue flowing through other channels. These are reps with selling responsibility who aren't using their digital tools.

<!-- CHANGED v2 (Phase-B query hygiene, rep_intelligence_layer2_build §7.3, applied + live-validated cci/clm/ufi 2026-06-29): `org_users.role/active/last_login` do NOT exist. Role lives on `user_types` (via `user_type_id`); recency is `last_ipad_login_at`; the disable flag is `disabled` (not `active`). Outcome side is re-anchored on INVOICED `net_amount` and re-gated on the rep-identity tier (Spine §7.1). NOTE: `portal_invoices` carries `rep_number` ONLY — names come via the `portal_orders` rep_number→rep_name bridge (same as RS-01/Q-51), so the name join is a Tier-2-only operation. -->
```sql
-- Inactive reps (90d+) with live territory revenue. Tier 2 only for NAMED output.
WITH rep_seats AS (   -- named seats + login recency (rep-seat proxy: last_ipad_login_at present, not disabled)
  SELECT ou.id, ou.user_id,
         u.first_name || ' ' || u.last_name AS rep_name,
         ou.last_ipad_login_at,
         EXTRACT(DAY FROM NOW() - ou.last_ipad_login_at)::int AS days_since_login
  FROM org_users ou
  JOIN users u       ON u.id = ou.user_id
  JOIN user_types ut ON ut.id = ou.user_type_id          -- role lives here (user_type_id → user_types)
  WHERE ou.organization_id = {{ORG_ID}}
    AND ou.last_ipad_login_at IS NOT NULL                 -- rep-seat proxy (Rep map §3.3)
    AND COALESCE(ou.disabled, false) = false
),
rep_names AS (   -- invoices carry rep_number only; bridge to name via portal_orders (Tier-2 name bridge)
  SELECT DISTINCT rep_number, rep_name
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> ''
),
rep_rev AS (      -- territory revenue on INVOICED net, by rep_number, name-bridged
  SELECT pi.rep_number,
         MAX(rn.rep_name) AS rep_name,
         ROUND(SUM(pi.net_amount)::numeric, 0) AS territory_invoiced_ltm
  FROM portal_invoices pi
  LEFT JOIN rep_names rn ON rn.rep_number = pi.rep_number
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND pi.rep_number IS NOT NULL AND pi.rep_number <> ''
  GROUP BY pi.rep_number
)
SELECT s.rep_name, s.days_since_login, r.territory_invoiced_ltm
FROM rep_seats s
JOIN rep_rev r ON LOWER(TRIM(s.rep_name)) = LOWER(TRIM(r.rep_name))   -- requires Tier 2 name bridge
WHERE s.days_since_login >= 90 AND r.territory_invoiced_ltm > 0
ORDER BY r.territory_invoiced_ltm DESC
LIMIT 15
```

**Tier gate (Spine §7.1 / `rep_intelligence_layer2_build` §7.3):** the name join only works on **Tier 2** orgs (name bridge ≥82% promotion, or ≥78% deadband-hold for declared carry-overs — hysteresis-banded 2026-06-30; see Spine §7.1 + `rep_copilot_operator.md` §1). On **Tier 1**, drop the name join and report at `rep_number` grain (label `rep <n>`, no names — see snippet below). On **Tier 0** (`ufi`/`heb`/`kll`/`lpf` — zero invoice `rep_number`) this query cannot run; **suppress** the revenue side and use login-recency behavior only. Live-validated 2026-06-29: cci (161) named output runs; clm (64) drops to `rep_number` grain; ufi (18) has 0 of 61,718 invoice rows with a `rep_number` → suppressed.

```sql
-- Tier 1 variant — rep_number grain, NO name join (no reliable name bridge inside/below the hysteresis deadband):
WITH rep_rev AS (
  SELECT rep_number, ROUND(SUM(net_amount)::numeric, 0) AS territory_invoiced_ltm
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE + INTERVAL '90 days'
    AND rep_number IS NOT NULL AND rep_number <> ''
  GROUP BY rep_number
)
SELECT 'rep ' || rep_number AS rep_label, territory_invoiced_ltm
FROM rep_rev WHERE territory_invoiced_ltm > 0
ORDER BY territory_invoiced_ltm DESC LIMIT 15
```

**Interpretation**: Each row is a rep who hasn't logged into the iPad in 90+ days (`last_ipad_login_at`) but has live **invoiced** territory revenue. High-value inactive reps are the highest-leverage re-activation targets — they already have the customer relationships, they just aren't using the platform. `territory_invoiced_ltm` shows what's at stake (invoiced net, capped at `COMMERCE_CONFIDENCE`).

**External claim rules**: "X reps with $Y in combined territory revenue haven't logged into the platform in 90+ days. These aren't inactive territories — they're active sellers managing their business offline. Re-engaging these reps is the fastest path to platform adoption growth." Frame as activation opportunity. Never expose user IDs or internal role codes. Use "haven't used the platform" not "haven't logged in" in client-facing text.

**Note**: The name join between `org_users`/`users` seats and the invoiced `rep_number`→`rep_name` bridge is approximate (case-insensitive name match) and **only valid on Tier 2** (name bridge ≥82% promotion, or ≥78% deadband-hold for declared carry-overs — hysteresis-banded 2026-06-30; see Spine §7.1). Some mismatches are expected — validate per-org (census §E4). On Tier 1, use the `rep_number`-grain variant; on Tier 0, suppress the revenue side.

---

### Q-R1: Rep Activity & Cadence (Behavior Floor, OWNED)
**Maps to**: VM-R1 | **Audience**: external | **Status**: active (gate: `org_users.last_ipad_login_at` present — always true on any org with iPad seats) | **Source**: Postgres MCP

Counts iPad-active seats, recent login recency, and confirmed order authorship over the trailing 90 days. Produces one org-level summary row. This is the always-on leg — it fires for every org regardless of ERP feed or Mixpanel.

**Active-seat roster** = `org_users.last_ipad_login_at IS NOT NULL AND NOT COALESCE(disabled, false)` per Spine §7.1 / catalog line 1976. Row-level names are never emitted by this query (prose uses aggregate counts only).

```sql
WITH active_seats AS (
  SELECT
    id AS org_user_id,
    last_ipad_login_at,
    EXTRACT(DAY FROM NOW() - last_ipad_login_at)::int AS days_since_login
  FROM org_users
  WHERE organization_id = {{ORG_ID}}
    AND last_ipad_login_at IS NOT NULL
    AND COALESCE(disabled, false) = false
)
SELECT
  COUNT(*)                                                              AS active_seats,
  COUNT(*) FILTER (WHERE days_since_login <= 30)                       AS logins_30d,
  COUNT(*) FILTER (WHERE days_since_login > 30 AND days_since_login <= 90) AS quiet_seats,
  COUNT(*) FILTER (WHERE days_since_login > 90)                        AS dark_seats,
  MIN(days_since_login)                                                AS min_days_since_login,
  (
    SELECT COUNT(DISTINCT org_user_id)
    FROM orders
    WHERE organization_id = {{ORG_ID}}
      AND created_at >= CURRENT_DATE - INTERVAL '90 days'
      AND org_user_id IS NOT NULL
      AND COALESCE(is_marked_deleted, false) = false
  )                                                                    AS order_authors_90d,
  (
    SELECT COUNT(*)
    FROM orders
    WHERE organization_id = {{ORG_ID}}
      AND created_at >= CURRENT_DATE - INTERVAL '90 days'
      AND COALESCE(NULLIF(TRIM(order_type), ''), 'Confirmed')
          NOT IN ('Quote','Estimate','Proforma','WishList','Wish List',
                  'Interest','Liked','Draft Order','Select Order Type')
      AND order_type NOT ILIKE 'HFC%'
      AND order_type NOT ILIKE 'Hold%'
      AND order_type NOT ILIKE 'TEST%'
      AND is_submitted = true
      AND COALESCE(is_marked_deleted, false) = false
  )                                                                    AS confirmed_orders_90d
FROM active_seats
```

**Interpretation**: `active_seats` = iPad-seat roster. `logins_30d` = seats active in the last month. `quiet_seats` = seats with 31–90 day login gap (coaching target). `dark_seats` = seats silent 90+ days. `order_authors_90d` = distinct reps who placed at least one order. `confirmed_orders_90d` = confirmed (non-quote) orders placed through the platform.

**External claim rules**: Frame as org-level behavioral metrics: "X of your Y active reps logged in this month." "Z reps have been quiet for 30+ days." Never name individual reps. Never imply revenue causation. Use "active" not "performing."

---

### Q-R2: Coverage / Territory Penetration (Behavior Floor, OWNED)
**Maps to**: VM-R2 | **Audience**: external | **Status**: active (gate: `customers` table present — always true) | **Source**: Postgres MCP

Computes what fraction of the org's active customer book received at least one platform order in the trailing 90 days. Org-level summary, one row.

```sql
WITH active_customers AS (
  SELECT DISTINCT code AS bill_to_code
  FROM customers
  WHERE organization_id = {{ORG_ID}}
),
touched_customers AS (
  SELECT DISTINCT customer_num
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND created_at >= CURRENT_DATE - INTERVAL '90 days'
    AND customer_num IS NOT NULL
    AND customer_num <> ''
    AND COALESCE(is_marked_deleted, false) = false
)
SELECT
  COUNT(ac.bill_to_code)                                                           AS total_customers,
  COUNT(tc.customer_num)                                                           AS touched_customers,
  ROUND(
    100.0 * COUNT(tc.customer_num)
          / NULLIF(COUNT(ac.bill_to_code), 0),
    1
  )                                                                                AS coverage_pct,
  COUNT(ac.bill_to_code) - COUNT(tc.customer_num)                                 AS untouched_customers
FROM active_customers ac
LEFT JOIN touched_customers tc ON tc.customer_num = ac.bill_to_code
```

**Interpretation**: `coverage_pct` = share of the active customer book that received at least one platform order in 90 days. `untouched_customers` = accounts in the book with zero digital activity — growth opportunity or dormant accounts.

**External claim rules**: "Your team covered X% of your active accounts through the platform this quarter." Frame `untouched_customers` as opportunity: "Y accounts in your book haven't received a platform order in 90 days." Never imply these accounts are inactive with the client (they may be served offline); frame as platform coverage gap.

---

### Q-R4: Quote→Submit Discipline (Behavior Floor, OWNED)
**Maps to**: VM-R4 | **Audience**: external | **Status**: active (gate: `orders` table present — always true on any eCat org) | **Source**: Postgres MCP

Classifies every platform order in the trailing 90 days as either a confirmed order (passes the eCat-SALE filter + `is_submitted = true`) or a draft/quote (excluded by the filter or not yet submitted). Produces one org-level summary row.

The eCat-SALE filter (Spine §6.5) is applied exactly as specified in the library: `COALESCE(NULLIF(TRIM(order_type), ''), 'Confirmed') NOT IN (...)`.

```sql
WITH orders_90d AS (
  SELECT
    CASE
      WHEN COALESCE(NULLIF(TRIM(order_type), ''), 'Confirmed')
           IN ('Quote','Estimate','Proforma','WishList','Wish List',
               'Interest','Liked','Draft Order','Select Order Type')
        OR order_type ILIKE 'HFC%'
        OR order_type ILIKE 'Hold%'
        OR order_type ILIKE 'TEST%'
        OR NOT COALESCE(is_submitted, false)
      THEN 'draft'
      ELSE 'confirmed'
    END AS order_class,
    order_type
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND created_at >= CURRENT_DATE - INTERVAL '90 days'
    AND COALESCE(is_marked_deleted, false) = false
)
SELECT
  COUNT(*)                                                               AS total_orders,
  COUNT(*) FILTER (WHERE order_class = 'confirmed')                     AS confirmed_orders,
  COUNT(*) FILTER (WHERE order_class = 'draft')                         AS draft_orders,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE order_class = 'confirmed')
          / NULLIF(COUNT(*), 0),
    1
  )                                                                      AS submit_rate_pct,
  -- Top draft type by count (informational, not client-facing directly)
  (
    SELECT order_type
    FROM orders_90d
    WHERE order_class = 'draft' AND order_type IS NOT NULL AND order_type <> ''
    GROUP BY order_type
    ORDER BY COUNT(*) DESC
    LIMIT 1
  )                                                                      AS top_draft_type
FROM orders_90d
```

**Interpretation**: `submit_rate_pct` = confirmed orders as a share of all platform orders. Low submit rates indicate reps are creating draft or quote orders that never convert to confirmed submissions — a coaching opportunity on closing discipline. `top_draft_type` identifies the most common non-submission category (e.g., "Quote," "Estimate") for targeted coaching.

**External claim rules**: "X% of platform orders in the last 90 days were confirmed submissions. Y orders remain as drafts or quotes." Frame constructively: "Converting draft orders to confirmed submissions is the fastest path to accurate order flow data." Never say "eCat-SALE" or expose internal order_type codes directly. Say "draft orders" / "confirmed orders." Never name individual reps in this org-level summary.

---

## Query Status Summary

| Query | VM | Audience | Status |
|-------|-----|----------|--------|
| Q-PROV-00 | provenance gate | internal | **v2 NEW — sets TOTAL_BUSINESS_SOURCE + COMMERCE_CONFIDENCE** |
| Q-PROV-SD | total-business (LIMITED) | external | **v2 NEW — sales_data-only path** |
| Q-CHAN-05 | where-you-sell L1 | external | **v2 NEW — eCat vs non-eCat split; gated on Q-PROV-00** |
| Q-CHAN-06 | eCat-lead honesty gate (F1) | internal | **v2 NEW — Track B — eCat-SALE confirmed-ratio pre-check (blank-`order_type` default-share); gates whether eCat may lead a NONE/STALE report** |
| Q-CHAN-00 | where-you-sell L2 gate | internal | **v2 NEW — Channel Availability Preflight → CHANNEL_CONFIDENCE** |
| Q-CHAN-10 | where-you-sell L2 | external | **v2 NEW — bespoke; channel mix via per-org order_origin map; SUPPRESS NONE-tier** |
| Q-CHAN-20 | where-you-sell L2 trust | internal | **v2 NEW — eCat-vs-origin reconciliation (RELIABLE/OVER-TAG/UNDER-TAG)** |
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
| Q-16 | VM-16 | external | **v2 — total business = INVOICED sales; order-header is booked-volume companion** |
| Q-17 | VM-17 | external | live |
| Q-18 | VM-18 | external | **v2 — Part B total context now invoiced** |
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
| Q-45 | VM-45 | external | **v2 — denominator = INVOICED total business; old GMV gate removed** |
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
| Q-51 | VM-51 | external | **v2 — invoiced GMV per rep; rep_number→name bridge** |
| Q-52 | VM-52 | external | **v2 — invoiced GMV per customer** |
| Q-53 | VM-53 | external | **v2 — unactivated accounts ranked by invoiced GMV** |
| Q-54 | VM-54 | external | **v2 — invoiced GMV per state** |
| Q-CL-01—05 | VM-31—35 | external | conditional (has_clicky) |
| Q-55 | VM-55 | external | **v2 — invoiced category dollars (num + denom)** |
| Q-56 | VM-56 | external | conditional (portal_orders + rep data + Q-55 displacement) |
| Q-57 | VM-57 | external | conditional (portal_orders + customer data) |
| Q-58 | VM-58 | external | conditional (commitment_data) |
| Q-58b | VM-58b | external | conditional (commitment_data + inventory) |
| Q-60 | VM-60 | external | conditional (portal_orders + QoQ price data) |
| Q-62 | VM-62 | external | conditional (portal_orders + new_items) |
| Q-63 | VM-63 | external | conditional (Mixpanel) |
| Q-64 | VM-64 | external | conditional (Mixpanel + portal_orders) |
| Q-65 | VM-65 | external | conditional (Mixpanel) |
| Q-66 | VM-66 | external | conditional (portal_orders + buyer data) |
| Q-67 | VM-67 | external | conditional (portal_orders + customer data) |
| Q-68 | VM-68 | external | conditional (portal_orders + customer data) — **methodology revised: historical peak comparison** |
| Q-69 | VM-69 | external | conditional (orders — order timing distribution; **v2 Phase-B: `submit_date` + `is_submitted`/`is_marked_deleted`**) |
| Q-70 | VM-70 | external | conditional (org_users/user_types + portal_invoices — inactive reps w/ territory revenue; **v2 Phase-B: invoiced + Tier-2 name gate**) |
| Q-R1 | VM-R1 | external | active — OWNED, always-on (org_users `last_ipad_login_at` + orders `created_at`; rep activity & cadence floor; ERP-optional) |
| Q-R2 | VM-R2 | external | active — OWNED, always-on (customers + orders `customer_num`/`created_at`; territory coverage penetration floor; ERP-optional) |
| Q-R4 | VM-R4 | external | active — OWNED, always-on (orders `order_type`/`is_submitted`/`created_at`; quote→submit discipline floor; ERP-optional) |
| Q-ORG-DECAY | SIG-DECAY-01/02 | external | conditional (portal_orders OR orders, 6+ months) |
| Q-ORG-NBP | SIG-OPP-01 | external | conditional (portal_order_items OR sales_data) |
| Q-ORG-GHOST | SIG-ANOMALY-01 | external | conditional (sales_data OR portal_order_items) |
| Q-ORG-STOCKOUT | SIG-ANOMALY-02 | external | conditional (inventories + sales_data/portal_order_items) |
| Q-ORG-CONTRACTION | SIG-DECAY-04/ANOMALY-03 | external | conditional (portal_orders, 12+ months) |
| Q-ORG-VELOCITY | SIG-MOM-01 | external | conditional (portal_orders OR orders, 6+ months) |
| Q-ORG-PRICE-SHIFT | SIG-MOM-03 | external | conditional (portal_order_items OR sales_data) |
| Q-ORG-NEWITEM | SIG-OPP-04 | external | conditional (products.new_item + sales_data/portal_order_items) |
| Q-ECON-00 | economics gate | internal | **v2 — sets economics flags + COMMERCE_CONFIDENCE cap (run first)** |
| Q-ECON-LEAK | VM-C2/C12 | external | conditional (`leakage_dispersion_ok`) — tier-aware dispersion |
| Q-ECON-RETURNS | VM-C5 | external | conditional (`returns_ok`) |
| Q-ECON-NETREV | VM-C16 | external | conditional (`netrev_freight_ok`) — net-of-freight, **not** margin |
| Q-ECON-TERMS | VM-C15 | external | conditional (`terms_ok`) — billed ≠ collected |
| Q-ECON-LEADTIME | VM-C15 | external | conditional (`leadtime_ok`) |
| Q-ECON-CARRIER | VM-C18 | external | conditional (`carrier_ok` + carrier-like `ship_via`) |
| Q-ECON-CONC | VM-C3 | external | **v2 (2026-06-30) — concentration + HHI; live-validated cci** |
| Q-ECON-QUALITY | VM-C7 | external | **v2 (2026-06-30) — recurring vs one-time; needs ≥2 windows; live-validated cci** |
| Q-ECON-SEASON | VM-C8 | external | **v2 (2026-06-30) — multi-year month-share; live-validated cci** |
| Q-ECON-PACE | VM-C9 | external | **v2 (2026-06-30) — pacing-band inputs (never a point); live-validated cci** |
| Q-ECON-MOMENTUM | VM-C10 | external | **v2 (2026-06-30) — comparable-window YoY; live-validated cci** |
| Q-ECON-LUMP | VM-C11 | external | **v2 (2026-06-30) — size dist + Gini; live-validated cci** |
| Q-ECON-NRR | VM-C17 | external | **v2 (2026-06-30) — dollar NRR; needs ≥2 yrs; live-validated cci** |
| Q-ECON-CONTRIB | VM-C20 | external | **v2 (2026-06-30) — contribution proxy (not margin); live-validated cci** |
| Q-SELL-QC | VM-C24 | external | conditional (≥200 quoting custs + eCat share ≥20%) — eCat-channel only |
| Q-SEG-DERIVE | segmentation | external | 🧊 frozen (owner directive) |
| Q-48 | VM-48 | **internal only** | **v2 (2026-06-30) — HubSpot expansion signals (BigQuery); live-validated cfg** |

---

## 3.0 Signal Detection Queries (Org-Level)

> **Added for Insightful Product 3.0**. These queries port v4 Customer Intelligence per-customer pattern detection to org-wide scope. They run against the same MCP infrastructure.

---

### Q-ORG-DECAY: Account & Item Reorder Decay Detection
**Maps to**: SIG-DECAY-01, SIG-DECAY-02 | **Audience**: external | **Status**: live | **Source**: Postgres

**Step 1 — Account-level reorder cadence (top 50 accounts):**

```sql
WITH account_orders AS (
  SELECT
    customer_num,
    MAX(bill_to_company_name) AS customer_name,
    MAX(bill_to_state) AS state,
    COUNT(*) AS ltm_orders,
    ROUND(SUM(total)::numeric, 2) AS ltm_gmv,
    MAX(created_at) AS last_order,
    EXTRACT(DAY FROM NOW() - MAX(created_at)) AS days_since_last
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND created_at >= NOW() - INTERVAL '12 months'
  GROUP BY customer_num
  HAVING COUNT(*) >= 5
  ORDER BY SUM(total) DESC
  LIMIT 50
),
intervals AS (
  SELECT
    customer_num,
    created_at,
    LAG(created_at) OVER (PARTITION BY customer_num ORDER BY created_at) AS prev_order,
    EXTRACT(DAY FROM created_at - LAG(created_at) OVER (PARTITION BY customer_num ORDER BY created_at)) AS gap_days
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND created_at >= NOW() - INTERVAL '18 months'
    AND customer_num IN (SELECT customer_num FROM account_orders)
),
avg_intervals AS (
  SELECT
    customer_num,
    ROUND(AVG(gap_days)::numeric, 1) AS avg_days_between,
    COUNT(*) AS interval_count
  FROM intervals
  WHERE gap_days IS NOT NULL AND gap_days > 0
  GROUP BY customer_num
)
SELECT
  ao.customer_num,
  ao.customer_name,
  ao.state,
  ao.ltm_orders,
  ao.ltm_gmv,
  ao.last_order,
  ao.days_since_last,
  ai.avg_days_between,
  ROUND((ao.days_since_last / NULLIF(ai.avg_days_between, 0))::numeric, 1) AS decay_ratio
FROM account_orders ao
JOIN avg_intervals ai ON ai.customer_num = ao.customer_num
WHERE ao.days_since_last > ai.avg_days_between * 2.5
  AND ao.ltm_gmv > 10000
ORDER BY ao.ltm_gmv * (ao.days_since_last / NULLIF(ai.avg_days_between, 0)) DESC
LIMIT 25
```

**Step 2 — Item-level reorder decay (for top 50 accounts with portal_order_items):**

```sql
WITH top_accounts AS (
  SELECT customer_bill_to_number AS customer_code
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
  GROUP BY customer_bill_to_number
  ORDER BY SUM(total_amount) DESC
  LIMIT 50
),
item_orders AS (
  SELECT
    po.customer_bill_to_number AS customer_code,
    po.customer_bill_to_name AS customer_name,
    poi.item_number,
    poi.description,
    po.order_date,
    poi.quantity_ordered,
    ROUND((poi.unit_price * poi.quantity_ordered)::numeric, 2) AS line_revenue
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number
    AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.customer_bill_to_number IN (SELECT customer_code FROM top_accounts)
    AND po.order_date >= NOW() - INTERVAL '18 months'
),
item_intervals AS (
  SELECT
    customer_code,
    customer_name,
    item_number,
    description,
    order_date,
    LAG(order_date) OVER (PARTITION BY customer_code, item_number ORDER BY order_date) AS prev_date,
    (order_date - LAG(order_date) OVER (PARTITION BY customer_code, item_number ORDER BY order_date)) AS gap_days
  FROM item_orders
),
item_stats AS (
  SELECT
    customer_code,
    MAX(customer_name) AS customer_name,
    item_number,
    MAX(description) AS description,
    COUNT(*) AS reorder_count,
    ROUND(AVG(gap_days)::numeric, 1) AS avg_interval,
    MAX(order_date) AS last_order,
    (CURRENT_DATE - MAX(order_date)::date) AS days_since_last
  FROM item_intervals
  WHERE gap_days IS NOT NULL AND gap_days > 0
  GROUP BY customer_code, item_number
  HAVING COUNT(*) >= 5
),
item_revenue AS (
  SELECT
    customer_code,
    item_number,
    ROUND(SUM(line_revenue)::numeric, 2) AS ltm_revenue
  FROM item_orders
  WHERE order_date >= NOW() - INTERVAL '12 months'
  GROUP BY customer_code, item_number
)
SELECT
  s.customer_code,
  s.customer_name,
  s.item_number,
  s.description,
  s.reorder_count,
  s.avg_interval,
  s.days_since_last,
  ROUND((s.days_since_last / NULLIF(s.avg_interval, 0))::numeric, 1) AS decay_ratio,
  COALESCE(r.ltm_revenue, 0) AS ltm_revenue,
  CASE
    WHEN s.days_since_last > s.avg_interval * 3 THEN 'DECAY_DETECTED'
    WHEN s.days_since_last > s.avg_interval * 2 THEN 'SLOWING'
    ELSE 'NORMAL'
  END AS status
FROM item_stats s
LEFT JOIN item_revenue r ON r.customer_code = s.customer_code AND r.item_number = s.item_number
WHERE s.days_since_last > s.avg_interval * 2.5
  AND COALESCE(r.ltm_revenue, 0) > 5000
ORDER BY COALESCE(r.ltm_revenue, 0) * (s.days_since_last / NULLIF(s.avg_interval, 0)) DESC
LIMIT 30
```

---

### Q-ORG-NBP: Next Best Product (Collaborative Filtering)
**Maps to**: SIG-OPP-01 | **Audience**: external | **Status**: live | **Source**: Postgres

**Requires**: `portal_order_items` present for the org.

```sql
WITH customer_items AS (
  SELECT DISTINCT
    po.customer_bill_to_number AS customer_code,
    poi.item_number
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number
    AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
    AND poi.quantity_ordered > 0
),
co_purchase AS (
  SELECT
    a.item_number AS anchor_item,
    b.item_number AS suggested_item,
    COUNT(DISTINCT a.customer_code) AS co_purchase_customers
  FROM customer_items a
  JOIN customer_items b ON a.customer_code = b.customer_code
    AND a.item_number != b.item_number
  GROUP BY a.item_number, b.item_number
  HAVING COUNT(DISTINCT a.customer_code) >= 10
),
top_accounts AS (
  SELECT
    po.customer_bill_to_number AS customer_code,
    po.customer_bill_to_name AS customer_name,
    ROUND(SUM(po.total_amount)::numeric, 2) AS ltm_gmv
  FROM portal_orders po
  WHERE po.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '12 months'
  GROUP BY po.customer_bill_to_number, po.customer_bill_to_name
  ORDER BY SUM(po.total_amount) DESC
  LIMIT 50
),
gaps AS (
  SELECT
    ta.customer_code,
    ta.customer_name,
    ta.ltm_gmv AS customer_ltm,
    cp.anchor_item,
    cp.suggested_item,
    cp.co_purchase_customers
  FROM top_accounts ta
  JOIN customer_items ci ON ci.customer_code = ta.customer_code
  JOIN co_purchase cp ON cp.anchor_item = ci.item_number
  WHERE NOT EXISTS (
    SELECT 1 FROM customer_items ci2
    WHERE ci2.customer_code = ta.customer_code
      AND ci2.item_number = cp.suggested_item
  )
)
SELECT
  g.customer_code,
  g.customer_name,
  g.customer_ltm,
  g.anchor_item,
  pa.long_description AS anchor_desc,
  g.suggested_item,
  ps.long_description AS suggested_desc,
  g.co_purchase_customers
FROM gaps g
LEFT JOIN products pa ON pa.organization_id = {{ORG_ID}} AND pa.item_number = g.anchor_item AND (pa.deleted = false OR pa.deleted IS NULL)
LEFT JOIN products ps ON ps.organization_id = {{ORG_ID}} AND ps.item_number = g.suggested_item AND (ps.deleted = false OR ps.deleted IS NULL)
ORDER BY g.co_purchase_customers DESC, g.customer_ltm DESC
LIMIT 50
```

---

### Q-ORG-GHOST: Ghost SKU Detection
**Maps to**: SIG-ANOMALY-01 | **Audience**: external | **Status**: live | **Source**: Postgres

```sql
WITH invoiced_items AS (
  SELECT
    sd.base_item_code AS item_number,
    COUNT(DISTINCT sd.bill_to_code) AS customer_count,
    SUM(sd.amount_invoiced) AS total_revenue,
    SUM(sd.quantity_invoiced) AS total_units
  FROM sales_data sd
  WHERE sd.organization_id = {{ORG_ID}}
  GROUP BY sd.base_item_code
  HAVING SUM(sd.amount_invoiced) > 5000
)
SELECT
  ii.item_number,
  ii.customer_count,
  ROUND(ii.total_revenue::numeric, 2) AS total_revenue,
  ii.total_units,
  'GHOST — no catalog record' AS status
FROM invoiced_items ii
LEFT JOIN products p ON p.organization_id = {{ORG_ID}}
  AND p.item_number = ii.item_number
WHERE p.id IS NULL
ORDER BY ii.total_revenue DESC
LIMIT 20
```

---

### Q-ORG-STOCKOUT: Stock-Out Impact with Customer Mapping
**Maps to**: SIG-ANOMALY-02 | **Audience**: external | **Status**: live | **Source**: Postgres

```sql
WITH top_items AS (
  SELECT
    sd.base_item_code AS item_number,
    SUM(sd.amount_invoiced) AS ltm_revenue,
    SUM(sd.quantity_invoiced) AS ltm_units
  FROM sales_data sd
  WHERE sd.organization_id = {{ORG_ID}}
  GROUP BY sd.base_item_code
  ORDER BY SUM(sd.amount_invoiced) DESC
  LIMIT 100
),
stocked_out AS (
  SELECT
    ti.item_number,
    ti.ltm_revenue,
    ti.ltm_units,
    p.long_description,
    p.collection_code,
    i.qty_available,
    i.qty_on_hand,
    i.qty_on_backorder,
    i.next_scheduled_receipt_date
  FROM top_items ti
  JOIN inventories i ON i.organization_id = {{ORG_ID}} AND i.base_item_code = ti.item_number
  LEFT JOIN products p ON p.organization_id = {{ORG_ID}} AND p.item_number = ti.item_number
    AND (p.deleted = false OR p.deleted IS NULL)
  WHERE i.qty_available = 0
),
customer_impact AS (
  SELECT
    sd.base_item_code AS item_number,
    sd.bill_to_code AS customer_code,
    MAX(c.name) AS customer_name,
    SUM(sd.amount_invoiced) AS customer_item_revenue,
    SUM(sd.quantity_invoiced) AS customer_item_units
  FROM sales_data sd
  LEFT JOIN customers c ON c.organization_id = {{ORG_ID}} AND c.code = sd.bill_to_code
  WHERE sd.organization_id = {{ORG_ID}}
    AND sd.base_item_code IN (SELECT item_number FROM stocked_out)
  GROUP BY sd.base_item_code, sd.bill_to_code
),
alternatives AS (
  SELECT
    so.item_number AS stocked_out_item,
    so.collection_code,
    p2.item_number AS alt_item,
    p2.long_description AS alt_desc,
    i2.qty_available AS alt_available
  FROM stocked_out so
  JOIN products p2 ON p2.organization_id = {{ORG_ID}}
    AND p2.collection_code = so.collection_code
    AND p2.item_number != so.item_number
    AND (p2.deleted = false OR p2.deleted IS NULL)
    AND (p2.hideable = false OR p2.hideable IS NULL)
  JOIN inventories i2 ON i2.organization_id = {{ORG_ID}}
    AND i2.base_item_code = p2.item_number
    AND i2.qty_available > 0
  WHERE so.collection_code IS NOT NULL
)
SELECT
  so.item_number,
  so.long_description,
  so.collection_code,
  ROUND(so.ltm_revenue::numeric, 2) AS ltm_revenue,
  so.ltm_units,
  so.qty_on_backorder,
  so.next_scheduled_receipt_date,
  (SELECT json_agg(json_build_object(
    'customer', ci.customer_name,
    'revenue', ROUND(ci.customer_item_revenue::numeric, 2)
  ) ORDER BY ci.customer_item_revenue DESC)
   FROM customer_impact ci WHERE ci.item_number = so.item_number
   LIMIT 5) AS top_customers,
  (SELECT json_agg(json_build_object(
    'item', a.alt_item,
    'desc', a.alt_desc,
    'available', a.alt_available
  ) ORDER BY a.alt_available DESC)
   FROM alternatives a WHERE a.stocked_out_item = so.item_number
   LIMIT 3) AS alternatives
FROM stocked_out so
ORDER BY so.ltm_revenue DESC
LIMIT 20
```

---

### Q-ORG-CONTRACTION: Account Spending Contraction & Competitive Displacement
**Maps to**: SIG-DECAY-04, SIG-ANOMALY-03 | **Audience**: external | **Status**: live | **Source**: Postgres

<!-- ECAT-NUMERATOR -->
```sql
WITH account_ltm AS (
  SELECT
    customer_bill_to_number AS customer_code,
    MAX(customer_bill_to_name) AS customer_name,
    MAX(customer_bill_to_state) AS state,
    COUNT(*) AS ltm_orders,
    ROUND(SUM(total_amount)::numeric, 2) AS ltm_gmv
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '12 months'
  GROUP BY customer_bill_to_number
  HAVING SUM(total_amount) > 25000
),
account_prior AS (
  SELECT
    customer_bill_to_number AS customer_code,
    COUNT(*) AS prior_orders,
    ROUND(SUM(total_amount)::numeric, 2) AS prior_gmv
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date BETWEEN NOW() - INTERVAL '24 months' AND NOW() - INTERVAL '12 months'
  GROUP BY customer_bill_to_number
),
ecat_ltm AS (
  SELECT
    customer_num AS customer_code,
    COUNT(*) AS ecat_ltm_orders,
    ROUND(SUM(total)::numeric, 2) AS ecat_ltm_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at >= NOW() - INTERVAL '12 months'
  GROUP BY customer_num
),
ecat_prior AS (
  SELECT
    customer_num AS customer_code,
    COUNT(*) AS ecat_prior_orders,
    ROUND(SUM(total)::numeric, 2) AS ecat_prior_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'   -- eCat-SALE filter
    AND created_at BETWEEN NOW() - INTERVAL '24 months' AND NOW() - INTERVAL '12 months'
  GROUP BY customer_num
)
SELECT
  al.customer_code,
  al.customer_name,
  al.state,
  al.ltm_gmv AS total_ltm,
  COALESCE(ap.prior_gmv, 0) AS total_prior,
  CASE WHEN COALESCE(ap.prior_gmv, 0) > 0
    THEN ROUND(((al.ltm_gmv - ap.prior_gmv) / ap.prior_gmv * 100)::numeric, 1)
    ELSE NULL END AS total_yoy_pct,
  COALESCE(el.ecat_ltm_gmv, 0) AS ecat_ltm,
  COALESCE(ep.ecat_prior_gmv, 0) AS ecat_prior,
  CASE WHEN COALESCE(ep.ecat_prior_gmv, 0) > 0
    THEN ROUND(((COALESCE(el.ecat_ltm_gmv, 0) - ep.ecat_prior_gmv) / ep.ecat_prior_gmv * 100)::numeric, 1)
    ELSE NULL END AS ecat_yoy_pct,
  CASE
    WHEN COALESCE(ap.prior_gmv, 0) > 0 AND al.ltm_gmv < ap.prior_gmv * 0.8
      THEN 'CONTRACTING'
    WHEN COALESCE(ep.ecat_prior_gmv, 0) > 0
      AND COALESCE(el.ecat_ltm_gmv, 0) < ep.ecat_prior_gmv * 0.9
      AND al.ltm_gmv > COALESCE(ap.prior_gmv, 0)
      THEN 'COMPETITIVE_DISPLACEMENT'
    ELSE 'STABLE_OR_GROWING'
  END AS signal_type
FROM account_ltm al
LEFT JOIN account_prior ap ON ap.customer_code = al.customer_code
LEFT JOIN ecat_ltm el ON el.customer_code = al.customer_code
LEFT JOIN ecat_prior ep ON ep.customer_code = al.customer_code
WHERE (
  (COALESCE(ap.prior_gmv, 0) > 0 AND al.ltm_gmv < ap.prior_gmv * 0.8)
  OR
  (COALESCE(ep.ecat_prior_gmv, 0) > 0
   AND COALESCE(el.ecat_ltm_gmv, 0) < ep.ecat_prior_gmv * 0.9
   AND al.ltm_gmv > COALESCE(ap.prior_gmv, 0))
)
ORDER BY
  CASE
    WHEN COALESCE(ap.prior_gmv, 0) > 0 THEN ABS(al.ltm_gmv - ap.prior_gmv)
    ELSE 0
  END DESC
LIMIT 25
```

---

### Q-ORG-VELOCITY: Account Quarterly Trajectory with Inflection Detection
**Maps to**: SIG-MOM-01 | **Audience**: external | **Status**: live | **Source**: Postgres

```sql
WITH quarterly AS (
  SELECT
    customer_bill_to_number AS customer_code,
    MAX(customer_bill_to_name) AS customer_name,
    DATE_TRUNC('quarter', order_date)::date AS quarter,
    COUNT(*) AS orders,
    ROUND(SUM(total_amount)::numeric, 2) AS revenue
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}}
    AND order_date >= NOW() - INTERVAL '24 months'
  GROUP BY customer_bill_to_number, DATE_TRUNC('quarter', order_date)
),
with_prev AS (
  SELECT
    customer_code,
    customer_name,
    quarter,
    orders,
    revenue,
    LAG(revenue) OVER (PARTITION BY customer_code ORDER BY quarter) AS prev_revenue,
    CASE WHEN LAG(revenue) OVER (PARTITION BY customer_code ORDER BY quarter) > 0
      THEN ROUND(((revenue - LAG(revenue) OVER (PARTITION BY customer_code ORDER BY quarter))
            / LAG(revenue) OVER (PARTITION BY customer_code ORDER BY quarter) * 100)::numeric, 1)
      ELSE NULL END AS qoq_pct
  FROM quarterly
),
acceleration AS (
  SELECT
    customer_code,
    MAX(customer_name) AS customer_name,
    COUNT(*) FILTER (WHERE qoq_pct > 30) AS accel_quarters,
    MAX(revenue) AS peak_quarter_revenue,
    MAX(quarter) AS latest_quarter,
    MAX(qoq_pct) AS max_qoq
  FROM with_prev
  WHERE quarter >= NOW() - INTERVAL '12 months'
  GROUP BY customer_code
  HAVING COUNT(*) FILTER (WHERE qoq_pct > 30) >= 2
)
SELECT
  a.customer_code,
  a.customer_name,
  a.accel_quarters,
  a.peak_quarter_revenue,
  a.max_qoq,
  json_agg(json_build_object(
    'quarter', wp.quarter,
    'revenue', wp.revenue,
    'qoq_pct', wp.qoq_pct
  ) ORDER BY wp.quarter) AS trajectory
FROM acceleration a
JOIN with_prev wp ON wp.customer_code = a.customer_code
  AND wp.quarter >= NOW() - INTERVAL '12 months'
GROUP BY a.customer_code, a.customer_name, a.accel_quarters, a.peak_quarter_revenue, a.max_qoq
ORDER BY a.peak_quarter_revenue DESC
LIMIT 15
```

---

### Q-ORG-PRICE-SHIFT: Account-Level Price Migration Detection
**Maps to**: SIG-MOM-03 | **Audience**: external | **Status**: live | **Source**: Postgres

```sql
WITH quarterly_prices AS (
  SELECT
    po.customer_bill_to_number AS customer_code,
    MAX(po.customer_bill_to_name) AS customer_name,
    DATE_TRUNC('quarter', po.order_date)::date AS quarter,
    ROUND(AVG(poi.unit_price)::numeric, 2) AS avg_unit_price,
    SUM(poi.quantity_ordered) AS total_units
  FROM portal_order_items poi
  JOIN portal_orders po ON po.order_number = poi.order_number
    AND po.organization_id = poi.organization_id
  WHERE poi.organization_id = {{ORG_ID}}
    AND po.order_date >= NOW() - INTERVAL '24 months'
    AND poi.unit_price > 0
    AND poi.quantity_ordered > 0
  GROUP BY po.customer_bill_to_number, DATE_TRUNC('quarter', po.order_date)
  HAVING SUM(poi.quantity_ordered) >= 10
),
trends AS (
  SELECT
    customer_code,
    customer_name,
    quarter,
    avg_unit_price,
    LAG(avg_unit_price) OVER (PARTITION BY customer_code ORDER BY quarter) AS prev_price,
    ROW_NUMBER() OVER (PARTITION BY customer_code ORDER BY quarter) AS qtr_num,
    COUNT(*) OVER (PARTITION BY customer_code) AS total_quarters
  FROM quarterly_prices
),
uptrenders AS (
  SELECT
    customer_code,
    MAX(customer_name) AS customer_name,
    MIN(avg_unit_price) AS baseline_price,
    MAX(avg_unit_price) AS latest_price,
    COUNT(*) FILTER (WHERE avg_unit_price > COALESCE(prev_price, 0)) AS up_quarters,
    COUNT(*) AS total_quarters
  FROM trends
  WHERE total_quarters >= 4
  GROUP BY customer_code
  HAVING COUNT(*) FILTER (WHERE avg_unit_price > COALESCE(prev_price, 0)) >= 3
    AND MAX(avg_unit_price) > MIN(avg_unit_price) * 1.2
)
SELECT
  u.customer_code,
  u.customer_name,
  u.baseline_price,
  u.latest_price,
  ROUND(((u.latest_price - u.baseline_price) / u.baseline_price * 100)::numeric, 1) AS price_change_pct,
  u.up_quarters,
  u.total_quarters,
  json_agg(json_build_object(
    'quarter', t.quarter,
    'avg_price', t.avg_unit_price
  ) ORDER BY t.quarter) AS price_trajectory
FROM uptrenders u
JOIN trends t ON t.customer_code = u.customer_code
GROUP BY u.customer_code, u.customer_name, u.baseline_price, u.latest_price, u.up_quarters, u.total_quarters
ORDER BY u.latest_price - u.baseline_price DESC
LIMIT 15
```

---

### Q-ORG-NEWITEM: New Item Adoption Gap Detection
**Maps to**: SIG-OPP-04 | **Audience**: external | **Status**: live | **Source**: Postgres

```sql
WITH new_items AS (
  SELECT
    p.item_number,
    p.long_description,
    p.collection_code
  FROM products p
  WHERE p.organization_id = {{ORG_ID}}
    AND p.new_item = true
    AND (p.deleted = false OR p.deleted IS NULL)
    AND (p.hideable = false OR p.hideable IS NULL)
),
new_item_sales AS (
  SELECT
    ni.item_number,
    ni.long_description,
    ni.collection_code,
    COUNT(DISTINCT sd.bill_to_code) AS customers_purchased,
    SUM(sd.amount_invoiced) AS total_revenue,
    SUM(sd.quantity_invoiced) AS total_units
  FROM new_items ni
  LEFT JOIN sales_data sd ON sd.organization_id = {{ORG_ID}}
    AND sd.base_item_code = ni.item_number
  GROUP BY ni.item_number, ni.long_description, ni.collection_code
),
collection_buyers AS (
  SELECT
    sd.bill_to_code AS customer_code,
    MAX(c.name) AS customer_name,
    p.collection_code,
    ROUND(SUM(sd.amount_invoiced)::numeric, 2) AS collection_revenue
  FROM sales_data sd
  JOIN products p ON p.organization_id = {{ORG_ID}} AND p.item_number = sd.base_item_code
  LEFT JOIN customers c ON c.organization_id = {{ORG_ID}} AND c.code = sd.bill_to_code
  WHERE sd.organization_id = {{ORG_ID}}
    AND p.collection_code IN (SELECT DISTINCT collection_code FROM new_items WHERE collection_code IS NOT NULL)
  GROUP BY sd.bill_to_code, p.collection_code
  HAVING SUM(sd.amount_invoiced) > 10000
)
SELECT
  nis.item_number,
  nis.long_description,
  nis.collection_code,
  COALESCE(nis.customers_purchased, 0) AS customers_purchased,
  COALESCE(ROUND(nis.total_revenue::numeric, 2), 0) AS total_revenue,
  (SELECT json_agg(json_build_object(
    'customer_code', cb.customer_code,
    'customer_name', cb.customer_name,
    'collection_revenue', cb.collection_revenue
  ) ORDER BY cb.collection_revenue DESC)
   FROM collection_buyers cb
   WHERE cb.collection_code = nis.collection_code
     AND NOT EXISTS (
       SELECT 1 FROM sales_data sd2
       WHERE sd2.organization_id = {{ORG_ID}}
         AND sd2.bill_to_code = cb.customer_code
         AND sd2.base_item_code = nis.item_number
     )
   LIMIT 5) AS should_buy_customers
FROM new_item_sales nis
WHERE COALESCE(nis.customers_purchased, 0) < 3
ORDER BY nis.collection_code, nis.item_number
LIMIT 30
```

---

## Domain 10 — Selling & Customer Economics (Hardened)
<!-- CHANGED v2: new domain. Authored from the Phase-A.5 hardening pilot (selling_customer_pilot_test_worksheet.md, 22-org live cohort, 2026-06-29). Only GO candidates are here. Every query inherits the Q-ECON-00 gate. The naive "% off list" leakage was KILLED in hardening (list semantics vary MSRP vs wholesale → would report a false 58% leak); leakage ships as same-SKU realized-price dispersion instead. -->
<!-- CHANGED v2 (audit remediation 2026-06-29): renumbered Domain 9 → Domain 10 (the pre-existing Domain 9 is "ERP Enrichment Intelligence" ~line 2242). Defect B. -->
> **Numbering note:** this is **Domain 10**. The "Domain 9" at ~line 2242 is the older "ERP Enrichment Intelligence" block; do not conflate the two.
>
> **Templating note:** every windowed economics query takes `{{REPORT_THROUGH_DATE}}` — set it from `Q-ECON-00.report_through_date` (the today-clamped MAX invoice date). For a fresh feed it equals `CURRENT_DATE`; for a stale feed (e.g. `bmc`) it pins the window to the last real invoice so the trailing 12 months aren't padded with empty months. Substitute alongside `{{ORG_ID}}`.

> **Inherits the Spine** ([`provenance_spine.md`](provenance_spine.md)): ERP-truth axiom, capture-vs-attribution, confidence tiers, date clamps, `$5M` cap, `invoiced ≠ collected`. **`Q-ECON-00` is the local gate** — run it first; every economics query below reads its flags and **suppresses** where the flag is false.

### Hard-gap guardrails (DO NOT approximate — confirmed absent at schema level)
- **Gross / true margin** — no cost/COGS column exists anywhere in the schema. Never compute or imply margin. `Q-ECON-NETREV` is net-of-freight *revenue*, NOT margin.
- **AR / DSO / collections** — the only payment tables (`stripe_invoices`, `subscription_invoices`) are SuperCat's own SaaS billing to the manufacturer; `orders.payment_*` is eCat checkout only. There is **no dealer-level AR**. `terms` is *billed* terms, not collection behavior.
- **Damage / claims by carrier** — no claims/damage table. `Q-ECON-CARRIER` can only do freight$/shipment-count per carrier.
- **Quoted lead time, market/showroom ROI, inventory aging** — no source. Suppress and say so.

---

### Q-ECON-00: Economics Preflight Gate (run first; sets the economics flags AND the completeness cap)
<!-- CHANGED v2: new. Encodes R1 (bad-date clamp) + R2 (priced-line presence, NOT a products join). -->
<!-- CHANGED v2 (audit remediation 2026-06-29): now emits COMMERCE_CONFIDENCE + report_through_date (Defects A/D/H/J). leakage_dispersion_ok gates on PRICED invoice lines, not a products join (Defect: pf has 0% product join yet valid dispersion). Audit: selling_customer_confidence_audit.md. -->
**Maps to**: economics preflight | **Audience**: internal (gate) | **Status**: required-before-any-Domain-10 | **Source**: Postgres MCP

Sets per-org availability AND the **completeness ceiling** for every economics query. Two jobs:
1. **Availability flags** (can this metric run at all): `report_through_date` is **clamped to today** so the bad-date orgs (live: `clm` had an invoice dated 4107, `jyc` 2032) cannot anchor a window on a fantasy date. `leakage_dispersion_ok` requires **priced invoice lines** (`unit_price>0`), **not** an invoice→product join — the dispersion metric never touches `products` (live: `pf` has 0% product-line join but fully valid dispersion; the old join gate wrongly suppressed it).
2. **`COMMERCE_CONFIDENCE` cap** (Defect A fix): mirrors `Q-PROV-00`/Spine §6.3. **No economics number may exceed this tier.** A feed that is **stale** (>45d since last invoice, e.g. `bmc`) or **provably incomplete** (confirmed eCat GMV > 1.05× invoiced LTM, e.g. `sc` at 126%) caps at **PARTIAL**, no matter how green the availability flags are. **`FULL` is unreachable** for economics — it requires `FEED_COMPLETENESS = CORROBORATED` (Spine §6.3), which no single invoice feed provides; the economics ceiling is **STRONG**. Every downstream query's effective confidence = `LEAST(its own ceiling, COMMERCE_CONFIDENCE)`.

```sql
WITH inv AS (
  SELECT COUNT(*) AS n_inv,
         MAX(invoice_date) FILTER (WHERE invoice_date <= CURRENT_DATE) AS report_through_date,  -- R1 clamp
         ROUND(SUM(net_amount)::numeric,2) AS inv_ltm_net,   -- net of credits; denominator for the partial-feed check
         ROUND(100.0*COUNT(*) FILTER (WHERE freight_amount IS NOT NULL AND freight_amount<>0)/NULLIF(COUNT(*),0),1) AS freight_pct,
         ROUND(100.0*COUNT(*) FILTER (WHERE COALESCE(NULLIF(TRIM(terms),''),'')<>'')/NULLIF(COUNT(*),0),1) AS terms_pct,
         ROUND(100.0*COUNT(*) FILTER (WHERE COALESCE(ship_via,tracking_carrier,'')<>'')/NULLIF(COUNT(*),0),1) AS carrier_pct,
         COUNT(*) FILTER (WHERE net_amount < 0) AS credit_memos
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE   -- R1: upper-clamped
),
invall AS (   -- freshness uses the all-time newest invoice (window-independent), clamped to today
  SELECT MAX(invoice_date) FILTER (WHERE invoice_date <= CURRENT_DATE) AS last_inv_alltime
  FROM portal_invoices WHERE organization_id = {{ORG_ID}}
),
pricecov AS (   -- R2 CORRECTED: dispersion gate = PRICED invoice lines, NOT a products join (pf: 0% product join, valid dispersion)
  SELECT ROUND(100.0*COUNT(*) FILTER (WHERE pii.unit_price > 0 AND pii.quantity_invoiced > 0)/NULLIF(COUNT(*),0),1) AS priced_line_pct
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number=pii.invoice_number AND pi.organization_id=pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}} AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
),
ecat AS (   -- LTM CONFIRMED eCat GMV (eCat-SALE filter, Spine §6.5) — the completeness cross-check numerator
  SELECT ROUND(SUM(total)::numeric,2) AS ecat_ltm_gmv
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true AND (is_marked_deleted = false OR is_marked_deleted IS NULL) AND total < 5000000
    AND COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') NOT IN ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
    AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
    AND created_at >= NOW() - INTERVAL '12 months'
),
sd AS (   -- summary feed total (NO dates) — soft completeness triangulation only, never a reportable total here
  SELECT ROUND(SUM(COALESCE(amount_invoiced,0))::numeric,2) AS sd_amt FROM sales_data WHERE organization_id = {{ORG_ID}}
),
po AS (
  SELECT ROUND(100.0*COUNT(*) FILTER (WHERE ship_date IS NOT NULL)/NULLIF(COUNT(*),0),1) AS ship_pct,
         COUNT(DISTINCT NULLIF(order_origin,'')) AS distinct_origins
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND order_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
)
SELECT
  inv.n_inv, inv.report_through_date, inv.inv_ltm_net, inv.freight_pct, inv.terms_pct, inv.carrier_pct, inv.credit_memos,
  pc.priced_line_pct, po.ship_pct, po.distinct_origins,
  COALESCE(ecat.ecat_ltm_gmv,0) AS ecat_ltm_confirmed_gmv,
  (CURRENT_DATE - invall.last_inv_alltime) AS days_since_last_invoice,
  ROUND(sd.sd_amt / NULLIF(inv.inv_ltm_net,0), 2) AS salesdata_over_invoiced,   -- soft signal: >~1.3 ⇒ invoices likely a channel subset (Spine §6.3 UNVERIFIED)
  -- availability flags (can the metric run?)
  (inv.n_inv > 0)                                          AS invoice_feed_present,
  (inv.n_inv > 0 AND pc.priced_line_pct >= 60)             AS leakage_dispersion_ok,  -- R2 CORRECTED: priced lines, NOT products join
  (inv.n_inv > 0 AND inv.freight_pct >= 20)                AS netrev_freight_ok,      -- R6
  (inv.n_inv > 0 AND inv.credit_memos > 0)                 AS returns_ok,             -- R5
  (inv.n_inv > 0 AND inv.terms_pct >= 50)                  AS terms_ok,               -- R7
  (inv.n_inv > 0 AND inv.carrier_pct >= 50)                AS carrier_ok,             -- R9
  (po.ship_pct >= 50)                                      AS leadtime_ok,            -- R8
  (po.distinct_origins >= 2)                               AS channel_ok,
  -- COMPLETENESS CAP (Defect A): the ceiling every economics confidence inherits. FULL is intentionally unreachable.
  CASE
    WHEN inv.n_inv = 0 THEN 'NONE'
    WHEN (CURRENT_DATE - invall.last_inv_alltime) > 45 THEN 'PARTIAL'                            -- STALE feed (e.g. bmc)
    WHEN COALESCE(ecat.ecat_ltm_gmv,0) > 1.05 * NULLIF(inv.inv_ltm_net,0) THEN 'PARTIAL'         -- PROVABLY INCOMPLETE: eCat alone > invoiced (e.g. sc 126%)
    ELSE 'STRONG'                                                                                -- single fresh feed; ceiling is STRONG (FULL needs CORROBORATED, Spine §6.3)
  END AS commerce_confidence
FROM inv, invall, pricecov pc, ecat, sd, po
```
**External claim rules**: internal gate only — never shown to a client. Drives REPORT/SUPPRESS **and the confidence ceiling** for every query below. **Binding rule (Spine §5.3):** every economics query reports at `LEAST(its own ceiling, commerce_confidence)`; a `PARTIAL`/`NONE` here forces every dependent dollar to PARTIAL or suppression regardless of its individual availability flags.

---

### Q-ECON-LEAK: Price-Realization Leakage (tier-aware same-SKU dispersion)
<!-- CHANGED v2: new. The vs-list version was KILLED in hardening (R3): products.net_price is MSRP for some orgs (cci/scw/gh ~58-69% "off list" = wholesale spread, not leakage) and wholesale for others. Ships as list-agnostic same-SKU realized-price dispersion. -->
<!-- CHANGED v2 (audit remediation 2026-06-29): REDESIGNED tier-aware (Defects E/F/G). (1) reference is now a TRUE MEDIAN at customer grain (the shipped trimmed-MEAN over-reported vs the median the gut-check demanded); (2) TIER GUARD — a price shared by >=5 customers is a sanctioned price class, not a leak; (3) VOLUME GUARD — accounts driving >=10% of a SKU's units (negotiated volume, e.g. Wayfair) are set aside, not flagged. Live-revalidated; the cci 9000-0143 Wayfair tier no longer scores. Audit: selling_customer_confidence_audit.md §3. -->
<!-- CHANGED v2 (owner sign-off 2026-06-29): label APPROVED — ships capped at COMMERCE_CONFIDENCE (directional on PARTIAL feeds). House accounts now AUTO-DETECTED + flagged (house_suspect) and excluded from the headline pending per-org review; thresholds kept (tier >=5 custs, volume >=10%, band 10%). selling_customer_label_signoff.md. -->
**Maps to**: CFO price realization / discount leakage | **Audience**: external (CFO) | **Status**: conditional (gate: `leakage_dispersion_ok`) | **Source**: Postgres MCP | **Confidence**: **STRONG, capped at `COMMERCE_CONFIDENCE`** (so PARTIAL/directional on `sc`/`bmc`-type feeds; suppressed at NONE) — **label approved 2026-06-29**. FULL unreachable.

Answers *"where am I giving margin away in **discretionary** pricing?"* without a trustworthy list price, while **not** mistaking a legitimate price tier for a leak. For each SKU sold to **≥5 distinct customers**, it builds a **true median** reference at **customer grain** (one qty-weighted price per customer, so one big buyer's many lines don't drag the median), then counts a customer's spend as leakage only when its price is **>10% below** that median **AND** that price is **not a recognized tier** (a price point shared by ≥5 customers) **AND** the account is **not a strategic-volume buyer** (≥10% of the SKU's units). **House/sample/accommodation accounts are auto-detected and flagged** (`house_suspect`: `ZZ*` hard-dropped, plus code patterns like `ACCOM*`/`SAMPLE*`/`DISPLAY*`/`SHOWROOM*` and the tiny-revenue-huge-leakage signature) and **excluded from the headline pending per-org owner review** (R-LEAK-B). Live-revalidated guarded range (2026-06-29): **cci $0.41M / 0.63%, asi $0.79M / 1.26%, pf $2.93M / 4.53%, gh $0.30M / 1.24%, scw $0.53M / 1.76%** — far below the retired trimmed-mean figures (cci $2.66M, asi $5.27M) and the dangerous original off-list ($99.5M). `sc` computes $1.28M / 6.55% but is **capped to PARTIAL** (its feed is provably incomplete).

```sql
WITH custagg AS (   -- customer grain: one qty-weighted price per customer per SKU (de-weights a big buyer's many lines)
  SELECT pii.item_number AS item, pi.customer_bill_to_number AS cust,
         SUM(pii.quantity_invoiced) AS qty,
         SUM(pii.quantity_invoiced*pii.unit_price)/NULLIF(SUM(pii.quantity_invoiced),0) AS realized
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number=pii.invoice_number AND pi.organization_id=pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date  -- R1: gate-supplied; defaults to CURRENT_DATE
    AND pi.net_amount > 0                       -- exclude credit memos
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'ZZ%'   -- R-LEAK-B: drop house/accommodation accts (CONFIRM prefix per org)
  GROUP BY pii.item_number, pi.customer_bill_to_number
),
itemagg AS (   -- SKUs sold to >=5 distinct customers; tot_units feeds the volume guard
  SELECT item, COUNT(*) AS ncust, SUM(qty) AS tot_units
  FROM custagg GROUP BY item HAVING COUNT(*) >= 5
),
ranked AS (    -- R-LEAK-A (corrected): TRUE median per SKU via row-number (PERCENTILE_DISC is MCP-rejected)
  SELECT c.item, c.realized,
         ROW_NUMBER() OVER (PARTITION BY c.item ORDER BY c.realized) AS rn,
         COUNT(*)     OVER (PARTITION BY c.item)                     AS cnt
  FROM custagg c JOIN itemagg i ON i.item = c.item
),
ref AS (       -- median = avg of the middle one/two ranked rows (handles odd & even counts)
  SELECT item, AVG(realized) AS ref_price
  FROM ranked WHERE rn IN (FLOOR((cnt+1)/2.0), CEIL((cnt+1)/2.0))
  GROUP BY item
),
tier AS (      -- TIER GUARD: a price point shared by >=5 customers is a sanctioned price class, not a one-off discount
  SELECT c.item, ROUND(c.realized,2) AS px
  FROM custagg c JOIN itemagg i ON i.item = c.item
  GROUP BY c.item, ROUND(c.realized,2) HAVING COUNT(*) >= 5
),
scored AS (
  SELECT c.cust, c.item, c.qty, c.realized, r.ref_price,
         (t.px IS NOT NULL)            AS at_tier,    -- recognized shared price tier
         (c.qty >= 0.10 * i.tot_units) AS strategic   -- VOLUME GUARD: account drives >=10% of this SKU's units
  FROM custagg c
  JOIN itemagg i ON i.item = c.item
  JOIN ref r     ON r.item = c.item
  LEFT JOIN tier t ON t.item = c.item AND t.px = ROUND(c.realized,2)
),
per_cust AS (
  SELECT
    cust,
    ROUND(SUM(qty*realized)::numeric,0)                                                                                  AS revenue_realized,
    ROUND(SUM(qty*(ref_price-realized)) FILTER (WHERE realized < ref_price*0.90 AND NOT at_tier AND NOT strategic)::numeric,0) AS leakage_dollars,
    COUNT(*)             FILTER (WHERE realized < ref_price*0.90 AND NOT at_tier AND NOT strategic)                      AS skus_underpriced,
    ROUND(SUM(qty*(ref_price-realized)) FILTER (WHERE realized < ref_price*0.90 AND (at_tier OR strategic))::numeric,0)  AS tier_or_volume_setaside  -- shown for transparency, NOT leakage
  FROM scored
  GROUP BY cust
)
SELECT
  cust AS customer_bill_to_number,
  revenue_realized, leakage_dollars, skus_underpriced, tier_or_volume_setaside,
  -- HOUSE-ACCOUNT AUTO-DETECT (R-LEAK-B, owner-approved 2026-06-29): flag, exclude from the headline, surface for per-org review.
  (   cust ILIKE 'ACCOM%' OR cust ILIKE 'SAMPLE%' OR cust ILIKE 'HOUSE%' OR cust ILIKE 'DISPLAY%'
   OR cust ILIKE 'SHOWROOM%' OR cust ILIKE 'MODEL%' OR cust ILIKE 'PHOTO%' OR cust ILIKE 'TEST%'
   OR cust ILIKE 'MISC%' OR cust ILIKE 'NOCHARGE%' OR cust ILIKE 'NO CHARGE%' OR cust ILIKE 'COMP %'
   OR leakage_dollars > revenue_realized   -- tiny-revenue / huge-"leakage" signature = almost certainly sample/comp/house
  ) AS house_suspect   -- anchored prefixes only (avoid false-flagging FRANCO/COMPANY); ZZ* is already hard-dropped in `base`
FROM per_cust
WHERE leakage_dollars > 0
ORDER BY house_suspect ASC, leakage_dollars DESC   -- real accounts first; suspects sink to the bottom for review
LIMIT 50
```
**The client headline sums `leakage_dollars` WHERE `house_suspect = false` only.** The flagged rows are the **per-org house-account review list** — confirm them with the owner (a one-time per-org classification) before promoting any of them back into the client dollar.

**Gating**: run only when `leakage_dispersion_ok` (**priced invoice lines** ≥60% AND invoice feed present — NOT a products join; this is the corrected gate that rescues `pf`). Where false (`fal`/`uhc`/`da`/`wag` no invoices) → **suppress**. **Confidence caps at `COMMERCE_CONFIDENCE`**: on a PARTIAL feed (`sc`, `bmc`) the figure is PARTIAL/directional, never STRONG.

**External claim rules**: *"The same product is being sold to some accounts materially below the price your other customers pay — set against negotiated tiers and volume accounts, the discretionary spread is ~$X."* Frame as **discretionary price dispersion** (after tier/volume guards), never as "% off list" and never including a recognized price tier or a volume account. **Any dollar figure requires a human gut-check** (worksheet A.5.6); house-suspect accounts are auto-excluded but the per-org list must be owner-confirmed.

---

### Q-SEG-DERIVE: Behavior-Derived Customer Segmentation
> **🧊 FROZEN (owner directive, 2026-06-29).** Segmentation is the **final step** of this program — deferred until everything else is locked. Do **not** advance, extend, add dimensions/clusters, or wire this into any deliverable. It may be confidence-audited like any other query, but not built on. See `selling_customer_SKEPTICAL_AUDIT_handoff.md` §5.
<!-- CHANGED v2: new. R4: price band derived from REALIZED price (NTILE over avg realized line price), NOT products.net_price — so it works on list-absent orgs (ufi/kll/vic). Live-validated non-degenerate (9/9 cells, max ~24%) incl. list-absent ufi. -->
**Maps to**: customer segmentation (price × cadence × category) | **Audience**: external (sales leader) | **Status**: **FROZEN** (was: conditional, gate `invoice_feed_present`) | **Source**: Postgres MCP | **Confidence**: STRONG *(unverified — pending audit; not completeness-capped)*

Segments customers on **realized price band × order cadence** (category/collection mix optional 3rd axis where `category_code` coverage allows). Price band is list-independent (derived from each customer's average realized line price), so it works even where `products.net_price` is absent.

```sql
WITH cust AS (
  SELECT pi.customer_bill_to_number AS cust,
         COUNT(DISTINCT pi.invoice_number) AS n_inv,
         SUM(pii.quantity_invoiced*pii.unit_price) AS rev,
         SUM(pii.quantity_invoiced*pii.unit_price)/NULLIF(SUM(pii.quantity_invoiced),0) AS avg_unit
  FROM portal_invoices pi
  JOIN portal_invoice_items pii ON pii.invoice_number=pi.invoice_number AND pii.organization_id=pi.organization_id
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0 AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
  GROUP BY pi.customer_bill_to_number
  HAVING SUM(pii.quantity_invoiced*pii.unit_price) > 0
),
banded AS (
  SELECT cust, rev, n_inv,
         NTILE(3) OVER (ORDER BY avg_unit) AS price_band,   -- R4: realized-price band, list-independent
         CASE WHEN n_inv = 1 THEN 'one_time'
              WHEN n_inv BETWEEN 2 AND 4 THEN 'occasional'
              ELSE 'frequent' END AS cadence
  FROM cust
)
SELECT
  CASE price_band WHEN 1 THEN 'value' WHEN 2 THEN 'mid' ELSE 'premium' END AS price_band,
  cadence,
  COUNT(*) AS customers,
  ROUND(SUM(rev)::numeric,0) AS revenue
FROM banded
GROUP BY price_band, cadence
ORDER BY price_band, cadence
```
**Gating**: run when `invoice_feed_present`. Add the category axis only where `products.category_code` is populated and human-readable (not cryptic codes).

**External claim rules**: *"Your book splits into these behavioral segments — premium-frequent accounts drive $X while value one-timers are a long tail."* Descriptive segmentation, not a value judgment.

---

### Q-SELL-QC: eCat-Channel Quote→Purchase Rate (proxy)
<!-- CHANGED v2: new. R10: this is a CUSTOMER-level proxy (did a quoting customer also buy?), NOT document-level quote win rate — no quote→order link field exists. Live-validated: cleanly separates real selling (sc/scw/gh 67-84%) from vanity-quoting (fal/hfg ~6%). -->
<!-- CHANGED v2 (audit remediation 2026-06-29, Defect C): this is built ENTIRELY on the eCat `orders` table — it is an eCat-CHANNEL behavior metric, not a statement about the client's total selling. It cannot see a quote closed off-eCat (emailed PO keyed to ERP), so it understates real conversion. Added an eCat-SHARE gate; renamed "eCat-channel" and downgraded to LIMITED. -->
<!-- CHANGED v2 (owner sign-off 2026-06-29): label APPROVED — LIMITED, "eCat-channel quote→purchase rate"; eCat-share suppression cutoff set to 20% (per owner). selling_customer_label_signoff.md. -->
**Maps to**: eCat-channel quote→order conversion | **Audience**: external (sales leader) | **Status**: conditional (gate: ≥~200 quoting customers LTM **AND eCat share ≥20%**) | **Source**: Postgres MCP (eCat `orders` only) | **Confidence**: **LIMITED (eCat-channel behavior only — not selling-wide), capped at `COMMERCE_CONFIDENCE`** — **label approved 2026-06-29**.

For customers who quote **through eCat**, what share also placed a **confirmed eCat sale order** in the window. **This describes eCat-channel behavior only** — it is blind to off-eCat closes (phone/email/EDI keyed to the ERP), so it is a floor, not the client's true conversion. Useful to flag a client using eCat as a quote-printer; **not** a selling-wide win rate.

```sql
-- eCat-share gate (owner-approved cutoff = 20%): only meaningful where eCat is a material share of commerce.
-- Read ecat_ltm_confirmed_gmv and inv_ltm_net from Q-ECON-00; SUPPRESS (or label "eCat-channel only, low share")
-- when eCat share < 20% — there the quote→purchase rate describes a small slice and must NOT be read as selling-wide.
WITH o AS (
  SELECT customer_num AS cust,
         CASE WHEN order_type ILIKE '%quote%' OR order_type ILIKE '%estimate%' OR order_type ILIKE '%proforma%' THEN 'q'
              WHEN COALESCE(NULLIF(TRIM(order_type),''),'Confirmed') IN ('WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
                   OR order_type ILIKE 'Hold%' OR order_type ILIKE 'HFC%' OR order_type ILIKE 'TEST%' THEN 'x'
              ELSE 's' END AS b
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at >= NOW() - INTERVAL '12 months'
    AND COALESCE(NULLIF(TRIM(customer_num),''),'') <> ''
),
q AS (SELECT DISTINCT cust FROM o WHERE b='q'),
s AS (SELECT DISTINCT cust FROM o WHERE b='s')
SELECT
  COUNT(DISTINCT q.cust)                                                       AS quoting_customers,
  COUNT(DISTINCT s.cust)                                                       AS also_purchased,
  ROUND(100.0*COUNT(DISTINCT s.cust)/NULLIF(COUNT(DISTINCT q.cust),0),1)       AS ecat_quote_to_purchase_pct
FROM q LEFT JOIN s ON s.cust = q.cust
```
**Gating**: suppress where quoting_customers < ~200 (most orgs don't quote materially in eCat) **AND** where the eCat share of commerce (`ecat_ltm_confirmed_gmv / inv_ltm_net` from Q-ECON-00) is **< 20%** (owner-approved cutoff) — below that the rate describes a small channel slice, never the client's selling. Confidence caps at `COMMERCE_CONFIDENCE`.

**External claim rules**: label exactly *"eCat-channel quote→purchase rate"* — **eCat behavior only**, **not** a document-level win rate, **not** proof the order came from the quote, and **not** the client's total selling effectiveness (off-eCat closes are invisible). A low rate (e.g. ~6%) flags eCat being used as a quote display; a high rate is a floor on eCat closing, not a ceiling on selling.

---

### Q-ECON-RETURNS: Returns / Credit-Memo Rate (dollar-based)
<!-- CHANGED v2: new. R5: measured by DOLLARS not invoice count — clli is 35% credit memos by count but only 8% by dollars; a count basis false-trips the alarm. -->
**Maps to**: returns analytics | **Audience**: external (CFO) | **Status**: conditional (gate: `returns_ok`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

```sql
SELECT
  ROUND(SUM(net_amount) FILTER (WHERE net_amount > 0)::numeric,0)                                          AS gross_sales,
  ROUND(SUM(ABS(net_amount)) FILTER (WHERE net_amount < 0)::numeric,0)                                     AS credit_dollars,
  ROUND(100.0*SUM(ABS(net_amount)) FILTER (WHERE net_amount < 0)
        /NULLIF(SUM(net_amount) FILTER (WHERE net_amount > 0),0),1)                                        AS returns_pct_of_gross
FROM portal_invoices
WHERE organization_id = {{ORG_ID}}
  AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped (defaults to CURRENT_DATE)
```
**Gating**: run when `returns_ok` (credit memos present). Many orgs post returns outside the feed → suppress where absent. Flag (don't crash) when `returns_pct_of_gross` > 25% (rare; investigate the feed).

**External claim rules**: *"Credit memos run ~X% of gross sales."* This is returns/credits as fed, not damage/claims (a hard gap). Always dollar-based.

---

### Q-ECON-NETREV: Net-of-Freight Realized Revenue (NOT margin)
<!-- CHANGED v2: new. R6: floor per-invoice net-of-freight at 0 (pf has 871 small invoices where freight > net). Explicitly NOT margin (no COGS). -->
**Maps to**: net realized revenue | **Audience**: external (CFO) | **Status**: conditional (gate: `netrev_freight_ok`) | **Source**: Postgres MCP | **Confidence**: PARTIAL, capped at `COMMERCE_CONFIDENCE`

```sql
SELECT
  ROUND(SUM(net_amount) FILTER (WHERE net_amount > 0)::numeric,0)                                   AS gross_invoiced,
  ROUND(SUM(GREATEST(net_amount - COALESCE(freight_amount,0), 0)) FILTER (WHERE net_amount > 0)::numeric,0) AS net_ex_freight,  -- R6 floor
  ROUND(SUM(freight_amount) FILTER (WHERE freight_amount > 0)::numeric,0)                            AS freight_billed
FROM portal_invoices
WHERE organization_id = {{ORG_ID}}
  AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
```
**Gating**: run when `netrev_freight_ok` (freight ≥ 20% of invoices). Where freight absent, report gross only and label.

**External claim rules**: *"Of $X invoiced, ~$Y is freight you billed through."* **This is revenue net of freight, NOT margin** — there is no COGS in the data. Never call it margin or profit.

---

### Q-ECON-TERMS: Payment-Terms Mix (billed, NOT collected)
<!-- CHANGED v2: new. R7: normalize free-text terms strings before distribution (clli shows 48 raw variants). Mandatory billed≠collected caveat. -->
**Maps to**: terms distribution | **Audience**: external | **Status**: conditional (gate: `terms_ok`) | **Source**: Postgres MCP | **Confidence**: PARTIAL, capped at `COMMERCE_CONFIDENCE`

```sql
WITH norm AS (
  SELECT CASE
           WHEN REGEXP_REPLACE(UPPER(TRIM(terms)),'[^0-9A-Z]','','g') ~ 'NET0*30' THEN 'NET 30'
           WHEN REGEXP_REPLACE(UPPER(TRIM(terms)),'[^0-9A-Z]','','g') ~ 'NET0*60' THEN 'NET 60'
           WHEN REGEXP_REPLACE(UPPER(TRIM(terms)),'[^0-9A-Z]','','g') ~ 'NET0*90' THEN 'NET 90'
           WHEN UPPER(TRIM(terms)) LIKE '%CREDIT CARD%' OR UPPER(TRIM(terms)) LIKE '%CC%' OR UPPER(TRIM(terms)) LIKE '%PREPAID%' THEN 'PREPAID/CC'
           WHEN COALESCE(NULLIF(TRIM(terms),''),'') = '' THEN '(blank)'
           ELSE 'OTHER'
         END AS terms_bucket,
         net_amount
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
    AND net_amount > 0
)
SELECT terms_bucket,
       COUNT(*) AS invoices,
       ROUND(100.0*SUM(net_amount)/SUM(SUM(net_amount)) OVER (),1) AS pct_of_sales
FROM norm GROUP BY terms_bucket ORDER BY pct_of_sales DESC
```
**Gating**: run when `terms_ok` (terms ≥ 50% populated).

**External claim rules**: *"Your invoiced sales bill on these terms."* **MANDATORY caveat: these are billed terms, NOT collection behavior — SuperCat has no dealer AR/DSO data.** Never present as cash-conversion or aging.

---

### Q-ECON-LEADTIME: Order-to-Ship Lead Time (narrow)
<!-- CHANGED v2: new. R8: AVG + [order_date, +365] guard, exclude negative leadtime; drops PERCENTILE_DISC (MCP validator rejects ordered-set aggregates). -->
**Maps to**: fulfillment lead time | **Audience**: external | **Status**: conditional (gate: `leadtime_ok`) | **Source**: Postgres MCP | **Confidence**: PARTIAL, capped at `COMMERCE_CONFIDENCE`

```sql
SELECT
  COUNT(*) FILTER (WHERE ship_date >= order_date)                                          AS shipped_orders,
  ROUND(AVG(ship_date - order_date) FILTER (
        WHERE ship_date >= order_date AND ship_date - order_date <= 365)::numeric,1)        AS avg_days_to_ship,
  COUNT(*) FILTER (WHERE ship_date < order_date)                                            AS excluded_negative
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
```
**Gating**: run only when `leadtime_ok` (`ship_date` ≥ 50% populated — live: clli/jyc/bmc-type orgs). Suppress otherwise.

**External claim rules**: *"Orders ship in ~N days on average."* Actual fulfillment lead time, NOT quoted/promised lead time (a hard gap).

---

### Q-ECON-CARRIER: Carrier Freight Profile (conditional)
<!-- CHANGED v2: new. R9: ship_via semantics are org-dependent (real carrier for pf/rw; freight-terms code like 'PPD'/'FREE FREIGHT' for cci). Falls back to portal_invoice_tracking_records.carrier. Damage-by-carrier is a HARD GAP. -->
**Maps to**: carrier/freight analytics | **Audience**: external | **Status**: conditional (gate: `carrier_ok` AND ship_via is carrier-like) | **Source**: Postgres MCP | **Confidence**: LIMITED, capped at `COMMERCE_CONFIDENCE`

```sql
SELECT
  COALESCE(NULLIF(TRIM(ship_via),''),'(blank)') AS carrier,
  COUNT(*)                                       AS shipments,
  ROUND(SUM(freight_amount) FILTER (WHERE freight_amount > 0)::numeric,0) AS freight_billed
FROM portal_invoices
WHERE organization_id = {{ORG_ID}}
  AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
GROUP BY COALESCE(NULLIF(TRIM(ship_via),''),'(blank)')
ORDER BY shipments DESC
LIMIT 15
```
**Gating**: run only when `carrier_ok` AND `ship_via` holds carrier names (FedEx/Daylight/Maersk-style), not freight-payment codes (PPD/3RD PARTY/FREE FREIGHT). Where `ship_via` is a freight-method, try `portal_invoice_tracking_records.carrier` instead, else suppress.

**External claim rules**: *"Freight spend and shipment counts by carrier."* **Damage rates / claims by carrier are a HARD GAP** (no claims data) — never imply this measures carrier quality, only freight volume.

---

### Q-ECON-CONC: Revenue Concentration & Single-Account Risk (VM-C3)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161, RTD 2026-06-26): 7,586 customers / $70.5M LTM net; top-1 6.0%, top-5 12.3%, top-10 16.2%; HHI 54 (very diversified). Inherits Q-ECON-00 denominator/clamp. -->
**Maps to**: VM-C3 customer concentration risk | **Audience**: external (CFO/board) | **Status**: conditional (gate: `invoice_feed_present`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Billing-entity concentration of invoiced revenue: top-1 / top-5 / top-10 customer share + Herfindahl (HHI, share² ×10,000). HHI <1,500 = diversified, 1,500–2,500 = moderate, >2,500 = concentrated. Single-account risk = `top1_pct`.

```sql
WITH cust AS (
  SELECT customer_bill_to_number AS cust, SUM(net_amount) AS rev
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
    AND COALESCE(NULLIF(TRIM(customer_bill_to_number),''),'') <> ''
  GROUP BY customer_bill_to_number
  HAVING SUM(net_amount) > 0          -- net of credits; a customer net-negative on the year is excluded from the share base
),
tot AS (SELECT SUM(rev) AS total_rev, COUNT(*) AS n_cust FROM cust),
ranked AS (
  SELECT cust, rev, rev/NULLIF((SELECT total_rev FROM tot),0) AS share,
         ROW_NUMBER() OVER (ORDER BY rev DESC) AS rnk
  FROM cust
)
SELECT
  (SELECT n_cust FROM tot)                          AS customers,
  (SELECT ROUND(total_rev::numeric,0) FROM tot)     AS ltm_net,
  ROUND(100.0*MAX(share),1)                         AS top1_pct,
  ROUND(100.0*SUM(share) FILTER (WHERE rnk<=5),1)   AS top5_pct,
  ROUND(100.0*SUM(share) FILTER (WHERE rnk<=10),1)  AS top10_pct,
  ROUND(SUM(share*share)*10000,0)                   AS hhi
FROM ranked
```
**Gating**: run when `invoice_feed_present`. On a PARTIAL feed (stale/incomplete) the shares describe only the invoiced subset — caps at `COMMERCE_CONFIDENCE`.

**External claim rules**: *"Your top account is X% of revenue and your top 10 are Y% — concentration is [low/moderate/high]."* Concentration of **invoiced** revenue at **billing-entity** grain (a parent buying under many bill-to codes reads as diversified — note where known). Never imply a single account "will" churn; this sizes exposure, not probability.

---

### Q-ECON-QUALITY: Recurring vs One-Time Revenue (VM-C7)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): recurring 94% / one-off 6%; 5,838 recurring vs 1,730 one-off customers. Needs two comparable windows; inherits Q-ECON-00. -->
**Maps to**: VM-C7 revenue durability / recurring share | **Audience**: dual (CFO/board) | **Status**: conditional (gate: `invoice_feed_present` AND ≥2 comparable windows of data) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Splits LTM net into **durable/recurring** vs **one-and-done**. A customer is recurring if it bought in the prior 12-month window too **OR** invoiced in ≥2 distinct months this year; otherwise one-off. Reorder-interval stability can be layered later; this is the durable-share headline.

```sql
WITH base AS (
  SELECT customer_bill_to_number AS cust,
         SUM(net_amount) FILTER (WHERE invoice_date > {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months')                                AS cur,
         COUNT(DISTINCT date_trunc('month', invoice_date)) FILTER (WHERE invoice_date > {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') AS cur_months,
         SUM(net_amount) FILTER (WHERE invoice_date <= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months')                               AS prior
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '24 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped, 2 windows
    AND COALESCE(NULLIF(TRIM(customer_bill_to_number),''),'') <> ''
  GROUP BY customer_bill_to_number
)
SELECT
  ROUND(SUM(COALESCE(cur,0))::numeric,0)                                                                                       AS ltm_net,
  ROUND(100.0*SUM(COALESCE(cur,0)) FILTER (WHERE COALESCE(prior,0)>0 OR cur_months>=2)/NULLIF(SUM(COALESCE(cur,0)),0),1)       AS recurring_pct,
  ROUND(100.0*SUM(COALESCE(cur,0)) FILTER (WHERE COALESCE(prior,0)=0 AND cur_months<2)/NULLIF(SUM(COALESCE(cur,0)),0),1)       AS oneoff_pct,
  COUNT(*) FILTER (WHERE COALESCE(cur,0)>0 AND (COALESCE(prior,0)>0 OR cur_months>=2))                                         AS recurring_custs,
  COUNT(*) FILTER (WHERE COALESCE(cur,0)>0 AND COALESCE(prior,0)=0 AND cur_months<2)                                           AS oneoff_custs
FROM base
```
**Gating**: needs **two comparable windows** (≥24 months of feed). With <2 windows or a LIMITED/SALES_DATA source (no dates) → **suppress**. Pair with Q-ECON-SEASON to keep multi-year seasonal buyers from misclassifying as one-off.

**External claim rules**: *"~X% of your revenue is durable reorder business; the rest is one-and-done you re-win each year."* Durable-share, not a churn prediction. Forbidden on <2 windows.

---

### Q-ECON-SEASON: Seasonality & Cash Calendar (VM-C8)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): Oct 17.8% / Nov 17.0% / Dec 14.5% peak, Jul–Sep ~8.5% trough; years_observed column exposes thin months (cci feed starts ~Oct 2023 so Jul–Sep show 2 yrs). Inherits Q-ECON-00. -->
**Maps to**: VM-C8 seasonality / cash calendar | **Audience**: dual (CFO/Ops) | **Status**: conditional (gate: `invoice_feed_present` AND ≥2 full years) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Multi-year month-share curve. Computes each calendar month's share **within its own year**, then averages those shares across years so a single record month can't dominate. `years_observed` surfaces thin months (don't read a 1-year month as "the pattern").

```sql
WITH m AS (
  SELECT EXTRACT(YEAR FROM invoice_date)::int AS yr,
         EXTRACT(MONTH FROM invoice_date)::int AS mo,
         SUM(net_amount) AS net
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '36 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped, 3 years
    AND net_amount > 0
  GROUP BY 1,2
),
yr_tot AS (SELECT yr, SUM(net) AS yr_net FROM m GROUP BY yr),
sh AS (SELECT m.mo, m.net/NULLIF(y.yr_net,0) AS month_share FROM m JOIN yr_tot y ON y.yr=m.yr)
SELECT mo AS month,
       ROUND(100.0*AVG(month_share),1) AS avg_month_share_pct,
       COUNT(*)                         AS years_observed
FROM sh GROUP BY mo ORDER BY mo
```
**Gating**: needs ≥2 full years. With <2 years → suppress. Cross-reference `portal_orders.order_origin` market codes (where present) to label recurring market/showroom spikes.

**External claim rules**: *"Two months drive ~Z% of your year — shape cash, inventory and staffing around that curve."* A median/averaged multi-year curve, never a single year presented as the pattern.

---

### Q-ECON-MOMENTUM: True Comparable-Window Momentum (VM-C10)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): LTM $70.2M vs prior $66.7M = +5.2% YoY. BOTH windows end at RTD (the mhc fake-collapse fix). Inherits Q-ECON-00. -->
**Maps to**: VM-C10 YoY/QoQ momentum | **Audience**: dual (CEO/board) | **Status**: conditional (gate: `invoice_feed_present` AND ≥2 comparable windows) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Equal-length trailing windows **both ending at `report_through_date`**, so a lagging feed can't fake a crash (a window running into empty post-feed months would). Decompose into volume vs price/realization via Q-ECON-LEAK where needed.

```sql
SELECT
  ROUND(SUM(net_amount) FILTER (WHERE invoice_date >  {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months')::numeric,0)  AS ltm_net,
  ROUND(SUM(net_amount) FILTER (WHERE invoice_date <= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months')::numeric,0)  AS prior_ltm_net,
  ROUND(100.0*( SUM(net_amount) FILTER (WHERE invoice_date >  {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months')
              - SUM(net_amount) FILTER (WHERE invoice_date <= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months'))
        / NULLIF(SUM(net_amount) FILTER (WHERE invoice_date <= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months'),0),1) AS yoy_pct
FROM portal_invoices
WHERE organization_id = {{ORG_ID}}
  AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '24 months' AND {{REPORT_THROUGH_DATE}}::date         -- R1: gate-clamped
```
**Gating**: needs ≥2 windows. **Suppress the trend on LIMITED / SALES_DATA** sources (no dates). Both windows anchor on `report_through_date` — never `CURRENT_DATE` on a stale feed.

**External claim rules**: *"Your real YoY is N% on equal, fully-billed windows."* Never present a trailing window that runs into empty post-feed months as a decline.

---

### Q-ECON-LUMP: Revenue Lumpiness / Big-Deal Dependence (VM-C11)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): 56,037 invoices, Gini 0.532; top-1%-of-invoices 10.1% of $, top-5% 27.3%, ten largest invoices 0.6%. This is the suppression check that keeps the rest of the domain honest. Inherits Q-ECON-00. -->
**Maps to**: VM-C11 lumpiness / concentration of growth | **Audience**: dual (CFO/FP&A) | **Status**: conditional (gate: `invoice_feed_present`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Invoice-grain size distribution: share of dollars in the top 1% / top 5% of invoices (by count) and in the ten largest single invoices, plus a **Gini** on invoice size (row-number method — `PERCENTILE_DISC` is MCP-rejected). High top-share + high Gini = a few big deals carry the headline.

```sql
WITH inv AS (
  SELECT invoice_number, SUM(net_amount) AS amt
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
  GROUP BY invoice_number
  HAVING SUM(net_amount) > 0          -- positive invoices only; credit memos handled by Q-ECON-RETURNS
),
r AS (
  SELECT amt,
         ROW_NUMBER() OVER (ORDER BY amt DESC) AS rd,
         ROW_NUMBER() OVER (ORDER BY amt ASC)  AS ra
  FROM inv
),
agg AS (SELECT COUNT(*) AS n, SUM(amt) AS tot FROM inv)
SELECT
  a.n                                                                                            AS invoices,
  ROUND(a.tot::numeric,0)                                                                        AS ltm_net,
  ROUND(100.0*SUM(r.amt) FILTER (WHERE r.rd <= GREATEST(1, a.n/100))/NULLIF(a.tot,0),1)          AS top1pct_invoices_share,
  ROUND(100.0*SUM(r.amt) FILTER (WHERE r.rd <= GREATEST(1, a.n/20)) /NULLIF(a.tot,0),1)          AS top5pct_invoices_share,
  ROUND(100.0*SUM(r.amt) FILTER (WHERE r.rd <= 10)                  /NULLIF(a.tot,0),1)          AS ten_largest_invoices_share,
  ROUND((2.0*SUM(r.ra*r.amt)/NULLIF(a.n*a.tot,0) - (a.n+1.0)/a.n)::numeric,3)                     AS gini
FROM r CROSS JOIN agg a
GROUP BY a.n, a.tot
```
**Gating**: run when `invoice_feed_present`. Invoice grain (one big PO split across several invoices reads as several mid invoices — annotate known large contract orders, don't auto-discount).

**External claim rules**: *"Strip the top N invoices and growth was flat — here's how much is broad-based vs a few big deals."* Use to **gate** the momentum/pacing headlines; never present a lumpy headline as broad-based.

---

### Q-ECON-PACE: Year-End Pacing Range (VM-C9)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161, RTD 2026-06-26): YTD $36.9M over 177 days → naive-annualized $76.2M; trailing-12mo $73.9M; prior-YTD $35.8M (+3.3%). Building blocks for a BAND, never a point. Inherits Q-ECON-00. -->
**Maps to**: VM-C9 run-rate pacing | **Audience**: dual (CEO/CFO/FP&A) | **Status**: conditional (gate: `invoice_feed_present` AND ≥24 months) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Emits the **inputs to a pacing band** (never a point forecast): calendar-YTD invoiced, naive day-of-year annualization, trailing-12mo, and same-period-prior-year. The shipped band = **seasonally-adjust** the remaining months with Q-ECON-SEASON weights (not a flat day-rate) and **widen** by Q-ECON-LUMP (a lumpy book → wider band). Present as a range; label it a pacing line, not a forecast.

```sql
WITH ytd AS (
  SELECT SUM(net_amount) AS ytd_net FROM portal_invoices
  WHERE organization_id = {{ORG_ID}} AND net_amount > 0
    AND invoice_date BETWEEN date_trunc('year', {{REPORT_THROUGH_DATE}}::date) AND {{REPORT_THROUGH_DATE}}::date
),
ltm AS (
  SELECT SUM(net_amount) AS ltm_net FROM portal_invoices
  WHERE organization_id = {{ORG_ID}} AND net_amount > 0
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date
),
prioryr AS (
  SELECT SUM(net_amount) AS py_net FROM portal_invoices
  WHERE organization_id = {{ORG_ID}} AND net_amount > 0
    AND invoice_date BETWEEN date_trunc('year', {{REPORT_THROUGH_DATE}}::date) - INTERVAL '1 year'
                         AND ({{REPORT_THROUGH_DATE}}::date - INTERVAL '1 year')
)
SELECT
  ROUND((SELECT ytd_net FROM ytd)::numeric,0)                                                          AS ytd_net,
  EXTRACT(DOY FROM {{REPORT_THROUGH_DATE}}::date)::int                                                 AS days_elapsed,
  ROUND(((SELECT ytd_net FROM ytd) * 365.0 / EXTRACT(DOY FROM {{REPORT_THROUGH_DATE}}::date))::numeric,0) AS naive_annualized,
  ROUND((SELECT ltm_net FROM ltm)::numeric,0)                                                          AS trailing_12mo,
  ROUND((SELECT py_net FROM prioryr)::numeric,0)                                                        AS same_period_prior_yr,
  ROUND(100.0*((SELECT ytd_net FROM ytd)-(SELECT py_net FROM prioryr))/NULLIF((SELECT py_net FROM prioryr),0),1) AS ytd_vs_prior_pct
FROM ytd
```
**Gating**: needs ≥24 months for the seasonal weights; clamp far-future corruptions via `report_through_date`. **Always a band, never a point.**

**External claim rules**: *"At today's pace plus your open book you land the year at `$W ± band`, X% off last year."* Forbidden: a point estimate, or the words "forecast"/"prediction"/"oracle." The naive annualization is a sanity anchor only — the reported band must be seasonally adjusted (Q-ECON-SEASON) and lumpiness-widened (Q-ECON-LUMP).

---

### Q-ECON-NRR: Net Revenue Retention — Dollar-Based (VM-C17)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): prior cohort 7,807 custs / $66.9M base → $58.8M this year = 88.0% NRR$; expansion +$17.0M, contraction −$25.0M, 3,047 fully churned. Needs ≥2 yrs + stable keys; inherits Q-ECON-00. -->
**Maps to**: VM-C17 net revenue retention ($) | **Audience**: dual (CEO/CFO/investors) | **Status**: conditional (gate: `invoice_feed_present` AND ≥2 contiguous years) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Dollar NRR on the **prior-year cohort**: of every customer that invoiced in the prior 12-month window, what fraction of that base did the **same** customers spend this year (retained + expansion − contraction − churn). Decomposes expansion vs contraction dollars and counts full churns. Money-framed sibling of the who's-churning view (VM-K3).

```sql
WITH base AS (
  SELECT customer_bill_to_number AS cust,
         SUM(net_amount) FILTER (WHERE invoice_date >  {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') AS cur,
         SUM(net_amount) FILTER (WHERE invoice_date <= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') AS prior
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '24 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
    AND COALESCE(NULLIF(TRIM(customer_bill_to_number),''),'') <> ''
  GROUP BY customer_bill_to_number
)
SELECT
  COUNT(*) FILTER (WHERE prior > 0)                                                              AS prior_cohort_custs,
  ROUND(SUM(prior) FILTER (WHERE prior > 0)::numeric,0)                                          AS prior_base,
  ROUND(SUM(COALESCE(cur,0)) FILTER (WHERE prior > 0)::numeric,0)                                AS retained_plus_expansion,
  ROUND(100.0*SUM(COALESCE(cur,0)) FILTER (WHERE prior > 0)/NULLIF(SUM(prior) FILTER (WHERE prior>0),0),1) AS nrr_pct,
  ROUND(SUM(GREATEST(COALESCE(cur,0)-prior,0)) FILTER (WHERE prior>0)::numeric,0)                AS expansion_dollars,
  ROUND(SUM(LEAST(COALESCE(cur,0)-prior,0))    FILTER (WHERE prior>0)::numeric,0)                AS contraction_dollars,
  COUNT(*) FILTER (WHERE prior>0 AND COALESCE(cur,0)=0)                                          AS fully_churned_custs
FROM base
```
**Gating**: needs ≥2 contiguous years and **stable customer keys** — if the ERP re-keyed bill-to numbers or split accounts mid-window, reconcile keys first and present a band. Gross-of-returns slightly inflates NRR (credit memos net into `cur`/`prior`).

**External claim rules**: *"Existing accounts are worth ~N cents on the dollar YoY — you refill a leaky bucket before counting a new logo."* NRR$ band + expansion/contraction split. Forbidden on unstable keys without a band.

---

### Q-ECON-CONTRIB: Account Contribution Tiering (VM-C20)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on cci (org 161): surfaces accounts whose contribution rank drops vs revenue rank (e.g. NTDTX #95 rev → #123 contrib, −28). CONTRIBUTION PROXY (net − freight − returns), NOT gross profit — there is no COGS in the schema (hard gap). Inherits Q-ECON-00 + the C2/C5/C18 caveats. -->
**Maps to**: VM-C20 customer contribution / margin tiering | **Audience**: dual, internal-lead (CFO) | **Status**: conditional (gate: `invoice_feed_present`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Per-account **contribution proxy** = net invoiced − freight billed − returns (credit memos). Ranks each account by revenue vs by contribution and surfaces the biggest **rank drops** (looks big, contributes less — renegotiation targets). **This is a proxy, not gross profit** — landed cost is a hard gap. For the fuller proxy, layer each account's discretionary discount from `Q-ECON-LEAK` (per-customer `leakage_dollars`); this standalone version nets freight + returns only.

```sql
WITH cust AS (
  SELECT customer_bill_to_number AS cust,
         MAX(customer_bill_to_name) AS name,
         SUM(net_amount)                                   AS net,
         SUM(COALESCE(freight_amount,0))                   AS freight,
         SUM(ABS(net_amount)) FILTER (WHERE net_amount<0)  AS credits
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1: gate-clamped
    AND COALESCE(NULLIF(TRIM(customer_bill_to_number),''),'') <> ''
  GROUP BY customer_bill_to_number
  HAVING SUM(net_amount) > 0
),
calc AS (
  SELECT cust, name, net, (net - freight - COALESCE(credits,0)) AS contribution_proxy FROM cust
),
ranked AS (
  SELECT cust, name, net, contribution_proxy,
         ROW_NUMBER() OVER (ORDER BY net DESC)                AS rev_rank,
         ROW_NUMBER() OVER (ORDER BY contribution_proxy DESC) AS contrib_rank
  FROM calc
)
SELECT cust AS customer_bill_to_number, name,
       ROUND(net::numeric,0)                AS ltm_net,
       ROUND(contribution_proxy::numeric,0) AS contribution_proxy,
       rev_rank, contrib_rank,
       (rev_rank - contrib_rank)            AS rank_shift   -- negative = contributes worse than its revenue rank
FROM ranked
WHERE rev_rank <= 100                        -- focus on material accounts; widen as needed
ORDER BY (rev_rank - contrib_rank) ASC       -- biggest drops first (renegotiation list)
LIMIT 25
```
**Gating**: inherits every Q-ECON-LEAK / Q-ECON-RETURNS / Q-ECON-NETREV caveat. Freight allocation is header-level (not per-line); bundled-freight orgs understate the freight drag.

**External claim rules**: *"Your #3 account by revenue is your #11 by what you actually keep — discounts, returns and freight eat the difference."* **Label it a contribution proxy, never gross profit or margin.** Landed cost would unlock true margin (VM-C19/C21) but the single-feed ceiling stays STRONG.

---

### RS-01: Rep Leaderboard, Invoiced LTM (VM-C2-rep) — `pending_query`, prior-year window
<!-- FLAGGED v2 (2026-07-09, Track D honesty pass, decision_completeness_no_drift_2026-07-09.md §4 Track D / audit_cci_mode1_2026-07-09.md §2): RS-01 is referenced by `pipeline/config.py` (QUERIES_ALL manifest + column-alias table) and consumed by `gather.load_reps()`, but its SQL body has never been authored in this library. `gather.load_reps()` already reads a `prior_ltm_invoiced` column and computes `yoy_pct` from it — the *consumer* code supports a YoY comparison today. The query just never emits that column, so `prior_ltm_invoiced` defaults to `0.0` → `yoy_pct=None` for every rep on every org, regardless of actual tenure. This is a **flag, not a fix**: per the Track D guardrail ("do not invent pipeline SQL"), no SQL is authored here. The rendered fix (stop calling every rep "first-year") shipped in `section_06_team.md.j2`; this entry just gives the eventual prior-year-window query a canonical home so it isn't invented ad hoc in a template pass. -->
**Maps to**: VM-C2-rep (rep leaderboard; also feeds Layer 3 of §5 What's Driving) | **Audience**: external | **Status**: `pending_query` — current-year figure only, no prior-year window | **Source**: Postgres MCP (not yet authored)

**What exists today**: a rep-grain LTM-invoiced rollup (columns per `pipeline/config.py`: `rep_label`, `invoiced_net_ltm` required; aliases `ltm_invoiced`/`net_amount`, `accounts`/`customer_count`/`n_customers`, plus `is_house_rep_label`). **What's missing**: a second, prior-12-month window per rep (mirroring the `Q-ECON-NRR` / rep-YoY pattern already used elsewhere in this library — `SUM(...) FILTER (WHERE invoice_date > ... )` vs `FILTER (WHERE invoice_date <= ...)`, keyed on `rep_number` instead of `customer_bill_to_number`) so `gather.load_reps()` can populate `prior_ltm_invoiced` and compute a real `yoy_pct`.

**Before authoring**: confirm the rep-identity bridge/tier rules (Spine §7.1) apply the same way to a prior-window rep key as the current window — a rep whose `rep_number` changed between periods (re-assignment, re-coding) would otherwise show a fake "new" or a fake swing.

**External claim rules**: none yet — do not render a rep YoY % or a "first/new-book" claim until this query exists and is wired into `gather.py`. See `section_06_team.md.j2` ("No prior-year comp available") and `section_05_layers.md.j2` §Layer 3 ("No non-house reps with prior-year comparisons available") for the current, honest placeholder language.

---

### Q-48: HubSpot Expansion Signals (Internal — VM-48)
<!-- CHANGED v2 (2026-06-30): authored + live-validated on BigQuery. Join key is hubspot.company.properties_org_id = SuperCat SHORTNAME (e.g. 'cci'), populated for 177 client companies of 20,070. cfg → 2 open "Exp. Tier 3" deals, stage "Qualifying" (10% win prob), last activity 2026-06-25. NOTE: company.properties_hs_last_sales_activity_date is a corrupted load (epoch shows 1970) — use DEAL-level recency (hs_lastmodifieddate) instead. -->
**Maps to**: VM-48 HubSpot expansion signals | **Audience**: **internal only** (CS/account team — never client-facing) | **Status**: conditional (gate: company exists in HubSpot with `properties_org_id` set) | **Source**: BigQuery (`hubspot` dataset) | **Confidence**: internal signal (not completeness-capped; HubSpot is CRM hygiene, not ground truth)

For a client (matched by **shortname**), surfaces open-deal pipeline: count, summed open amount (often null — HubSpot deals frequently omit amount), readable stage label + win probability (from `pipeline_stage`), and deal-level last-activity recency. The expansion signal is an existing `customer` with open deals in flight.

```sql
WITH co AS (
  SELECT company_id,
         properties_name          AS company,
         properties_org_id        AS org_shortname,   -- = SuperCat shortname (e.g. 'cci'), NOT the numeric org id
         properties_lifecyclestage AS lifecycle
  FROM `hubspot.company`
  WHERE properties_org_id = '{{ORG_SHORTNAME}}'
),
d AS (
  SELECT dc.company_id,
         d.properties_dealname                            AS dealname,
         ps.label                                         AS stage_label,
         SAFE_CAST(ps.metadata_probability AS FLOAT64)    AS win_prob,
         d.properties_dealtype                            AS dealtype,
         SAFE_CAST(d.properties_amount AS FLOAT64)        AS amount,
         d.properties_hs_is_closed                        AS is_closed,
         d.properties_hs_is_closed_won                    AS is_won,
         SAFE_CAST(d.properties_createdate AS TIMESTAMP)        AS created,
         SAFE_CAST(d.properties_hs_lastmodifieddate AS TIMESTAMP) AS last_modified
  FROM `hubspot.deal` d
  JOIN `hubspot.deal_company` dc ON dc.deal_id = d.deal_id
  LEFT JOIN `hubspot.pipeline_stage` ps
         ON ps.stage_id = d.properties_dealstage AND ps.pipeline_id = d.properties_pipeline
)
SELECT
  co.company, co.org_shortname, co.lifecycle,
  COUNTIF(d.is_closed = false)                                            AS open_deals,
  ROUND(COALESCE(SUM(IF(d.is_closed = false, d.amount, 0)), 0), 0)        AS open_pipeline_amount,
  COUNTIF(d.is_closed = true AND d.is_won = true)                         AS closed_won_deals,
  MAX(IF(d.is_closed = false, d.last_modified, NULL))                     AS last_open_deal_activity,
  ARRAY_AGG(
    IF(d.is_closed = false, STRUCT(d.dealname, d.stage_label, d.win_prob, d.amount, d.created), NULL)
    IGNORE NULLS ORDER BY d.created DESC LIMIT 10)                        AS open_deal_detail
FROM co LEFT JOIN d ON d.company_id = co.company_id
GROUP BY 1,2,3
```
**Gating**: suppress (return nothing) where the client has no HubSpot company with `properties_org_id` set — only 177 of 20,070 companies are mapped. `open_pipeline_amount` is **0/null** when deals carry no amount — report the deal **count + stage**, not a dollar, in that case.

**External claim rules**: **INTERNAL ONLY — never put HubSpot pipeline in a client deliverable.** This is CS prep ("they have 2 open expansion deals stalled in Qualifying since April"), not a measured claim. Deal amounts and stages are CRM hygiene, frequently stale or blank; treat as a prompt to look, not a fact to report.

---

### Q-PROD-TOP: Top Products by Revenue (LTM)
<!-- CHANGED v2 (2026-07-01): authored + live-validated on cci (org 161): top 25 items by invoiced revenue LTM. Joins portal_invoice_items → products for description fallback. cci: #1 = 9000-0135 NOTTAWAY LARGE BRONZE CHANDELIER $724K / 780 units / 263 dealers. -->
**Maps to**: top-selling items (revenue, units, distribution breadth) | **Audience**: external (sales leader / product) | **Status**: conditional (gate: `invoice_feed_present`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Top items by invoiced revenue in the trailing 12-month window. Distinct dealer count measures distribution breadth (not just revenue concentration in one account). Description falls back through invoice-line description → product `long_description` → `short_description` → item_number.

```sql
WITH item_agg AS (
  SELECT pii.item_number,
         COALESCE(MAX(pii.description), MAX(p.long_description), MAX(p.short_description), pii.item_number) AS description,
         SUM(pii.quantity_invoiced * pii.unit_price) AS ltm_revenue,
         SUM(pii.quantity_invoiced) AS units,
         COUNT(DISTINCT pi.customer_bill_to_number) AS dealers
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  LEFT JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
  GROUP BY pii.item_number
  HAVING SUM(pii.quantity_invoiced * pii.unit_price) > 0
)
SELECT item_number, description, ROUND(ltm_revenue::numeric, 0) AS ltm_revenue, units, dealers
FROM item_agg
ORDER BY ltm_revenue DESC
LIMIT 25
```
**Gating**: inherits `invoice_feed_present` from Q-ECON-00. No additional conditions.

**External claim rules**: *"Your #1 item reaches N dealers — distribution breadth, not just volume from one big buyer."* Item-level, LTM only; no margin or velocity commentary beyond what the data shows.

---

### Q-PROD-FAMILY: Product Family/Collection Rollup (LTM + YoY)
<!-- CHANGED v2 (2026-07-01): authored + live-validated on cci (org 161): groups by products.collection_code. cci: 12 named collections, BUNNY WILLIAMS #1 at $1.71M (+56.1% YoY). Excludes NULL collection_code items (the "unassigned" majority) — those are the mainline catalog, not a branded family. -->
**Maps to**: product family performance (revenue, growth, breadth) | **Audience**: external (sales leader / product) | **Status**: conditional (gate: `invoice_feed_present` AND ≥1 named collection in `products.collection_code`) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Groups invoiced items by `products.collection_code` (the org's named product families/designer collaborations). Computes LTM revenue, YoY growth, distinct dealer count, and SKU count per family. Families with no prior-year revenue are flagged `is_new`. Items with no collection_code are excluded (they are the mainline catalog, not a branded family).

```sql
WITH item_sales AS (
  SELECT pii.item_number,
         p.collection_code,
         pi.customer_bill_to_number AS cust,
         pii.quantity_invoiced * pii.unit_price AS line_rev
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND p.collection_code IS NOT NULL AND TRIM(p.collection_code) <> ''
),
prior_fam AS (
  SELECT p.collection_code AS family_label,
         SUM(pii.quantity_invoiced * pii.unit_price) AS prior_revenue
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '24 months' AND CURRENT_DATE - INTERVAL '12 months'
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND p.collection_code IS NOT NULL AND TRIM(p.collection_code) <> ''
  GROUP BY p.collection_code
),
fam_ltm AS (
  SELECT collection_code AS family_label,
         SUM(line_rev) AS ltm_revenue,
         COUNT(DISTINCT item_number) AS sku_count,
         COUNT(DISTINCT cust) AS dealer_count
  FROM item_sales
  GROUP BY collection_code
)
SELECT l.family_label,
       l.family_label AS pattern,
       ROUND(l.ltm_revenue::numeric, 0) AS ltm_revenue,
       CASE WHEN p.prior_revenue IS NULL OR p.prior_revenue = 0 THEN NULL
            ELSE ROUND(((l.ltm_revenue - p.prior_revenue) / p.prior_revenue * 100)::numeric, 1) END AS yoy_pct,
       l.dealer_count,
       l.sku_count,
       (p.prior_revenue IS NULL OR p.prior_revenue = 0) AS is_new
FROM fam_ltm l
LEFT JOIN prior_fam p ON p.family_label = l.family_label
WHERE l.ltm_revenue > 0
ORDER BY l.ltm_revenue DESC
LIMIT 20
```
**Gating**: needs `invoice_feed_present` AND at least one product with a non-null `collection_code`. If the org doesn't use collections (all NULL), this returns empty and the template falls back gracefully.

**External claim rules**: *"Your Bunny Williams collection is up 56% YoY at 660 dealers — it's outpacing the catalog."* Family-level only; do not infer margin or inventory health from revenue alone. Collections with no prior-year sales are labeled "new" — they may be new launches or recently re-coded.

---

### Q-CROSS-SELL: Cross-Sell Overlap (Anchor-SKU Dealers × Target Family)
<!-- ADDED v2 (2026-07-02): authored + live-validated on cci (org 161): anchor 9000-0135 (263 dealers) × target BUNNY WILLIAMS → 184 gap dealers (70% of anchor base never bought BW). Also validated ali (0 gap — full overlap) and bri (10 gap dealers). Powers the §3 Play 1 cross-sell sentence. -->
**Maps to**: cross-sell opportunity sizing (gap list for field push) | **Audience**: external (sales leader / product) | **Status**: conditional (gate: `invoice_feed_present` AND Q-PROD-TOP non-empty AND Q-PROD-FAMILY non-empty) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Self-contained query that identifies the #1 item by LTM revenue (the anchor SKU) and the #1 product family by LTM revenue (the target family), then returns every dealer who bought the anchor but has NEVER bought any SKU in the target family within the trailing 12-month window. The result is the pre-qualified cross-sell list: same buyer profile, proven purchasing relationship, zero exposure to the growth family.

```sql
WITH anchor AS (
  SELECT pii.item_number
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
  GROUP BY pii.item_number
  ORDER BY SUM(pii.quantity_invoiced * pii.unit_price) DESC
  LIMIT 1
),
target_family AS (
  SELECT p.collection_code
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND p.collection_code IS NOT NULL AND TRIM(p.collection_code) <> ''
  GROUP BY p.collection_code
  ORDER BY SUM(pii.quantity_invoiced * pii.unit_price) DESC
  LIMIT 1
),
anchor_dealers AS (
  SELECT DISTINCT pi.customer_bill_to_number AS dealer
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND pii.item_number = (SELECT item_number FROM anchor)
),
target_buyers AS (
  SELECT DISTINCT pi.customer_bill_to_number AS dealer
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number = pii.invoice_number AND pi.organization_id = pii.organization_id
  JOIN products p ON p.item_number = pii.item_number AND p.organization_id = pii.organization_id AND p.deleted = false
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN CURRENT_DATE - INTERVAL '12 months' AND CURRENT_DATE
    AND pi.net_amount > 0
    AND pii.quantity_invoiced > 0 AND pii.unit_price > 0
    AND p.collection_code = (SELECT collection_code FROM target_family)
)
SELECT ad.dealer AS dealer_code,
       (SELECT item_number FROM anchor) AS anchor_item,
       (SELECT collection_code FROM target_family) AS target_family
FROM anchor_dealers ad
WHERE ad.dealer NOT IN (SELECT dealer FROM target_buyers)
ORDER BY ad.dealer
```
**Gating**: inherits `invoice_feed_present` from Q-ECON-00. Requires both Q-PROD-TOP and Q-PROD-FAMILY to have non-empty results (i.e., at least one item sold AND at least one named collection). If either is empty, the template falls back to the existing `QUERY-NEEDED`-free degraded path.

**External claim rules**: *"184 of your 263 anchor-SKU dealers have never bought from the Bunny Williams family."* Factual count only. Do not infer intent or conversion probability — the list is pre-qualified by purchase history, not by propensity modeling.

---

### Q-DEALER-COHORT: Dealer Cohort Flow & Cadence Decomposition
<!-- CHANGED v2 (2026-07-01): authored + live-validated on cci (org 161): active 7,570 → 7,807 prior; 2,870 new / 3,107 lapsed / 4,700 returning (+3.8% same-base lift); cadence: 1,747 frequent ($49.2M) / 3,145 occasional ($15.5M) / 2,678 one-time ($5.5M); second-year return 59.9%. Single-row summary for the §9 template. -->
**Maps to**: dealer base health (cohort flow + cadence + same-base lift) | **Audience**: external (sales leader / CEO) | **Status**: conditional (gate: `invoice_feed_present` AND ≥2 contiguous years) | **Source**: Postgres MCP | **Confidence**: STRONG, capped at `COMMERCE_CONFIDENCE`

Single-row summary decomposing the active dealer count into cohort flow (new / returning / lapsed), returning-dealer expansion/contraction, order-cadence buckets (frequent / occasional / one-time), and the second-year return rate (of last year's new dealers, how many came back). The template uses this to surface whether topline is carried by same-base expansion or new-dealer intake.

```sql
WITH cust_windows AS (
  SELECT customer_bill_to_number AS cust,
         SUM(net_amount) FILTER (WHERE invoice_date > CURRENT_DATE - INTERVAL '12 months') AS ltm_rev,
         COUNT(DISTINCT invoice_number) FILTER (WHERE invoice_date > CURRENT_DATE - INTERVAL '12 months') AS ltm_invoices,
         SUM(net_amount) FILTER (WHERE invoice_date BETWEEN CURRENT_DATE - INTERVAL '24 months' AND CURRENT_DATE - INTERVAL '12 months') AS prior_rev,
         MIN(invoice_date) AS first_ever
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN CURRENT_DATE - INTERVAL '24 months' AND CURRENT_DATE
    AND COALESCE(NULLIF(TRIM(customer_bill_to_number),''),'') <> ''
  GROUP BY customer_bill_to_number
),
cohorts AS (
  SELECT cust, ltm_rev, ltm_invoices, prior_rev, first_ever,
         CASE
           WHEN COALESCE(ltm_rev, 0) > 0 AND COALESCE(prior_rev, 0) > 0 THEN 'returning'
           WHEN COALESCE(ltm_rev, 0) > 0 AND COALESCE(prior_rev, 0) <= 0 THEN 'new'
           WHEN COALESCE(ltm_rev, 0) <= 0 AND COALESCE(prior_rev, 0) > 0 THEN 'lapsed'
           ELSE 'inactive'
         END AS cohort
  FROM cust_windows
),
second_year AS (
  SELECT COUNT(*) FILTER (WHERE cohort = 'returning' AND first_ever > CURRENT_DATE - INTERVAL '24 months') AS returned_from_new,
         (SELECT COUNT(*) FROM cust_windows WHERE COALESCE(prior_rev, 0) > 0 AND first_ever > CURRENT_DATE - INTERVAL '24 months' AND first_ever <= CURRENT_DATE - INTERVAL '12 months') AS new_last_year
  FROM cohorts
),
returning_detail AS (
  SELECT
    COUNT(*) FILTER (WHERE ltm_rev > prior_rev * 1.05) AS returning_grew,
    COUNT(*) FILTER (WHERE ltm_rev < prior_rev * 0.95) AS returning_declined,
    COUNT(*) FILTER (WHERE ltm_rev BETWEEN prior_rev * 0.95 AND prior_rev * 1.05) AS returning_flat,
    SUM(GREATEST(ltm_rev - prior_rev, 0)) AS expansion_dollars,
    SUM(LEAST(ltm_rev - prior_rev, 0)) AS contraction_dollars,
    SUM(ltm_rev) AS returning_ltm_total,
    SUM(prior_rev) AS returning_prior_total
  FROM cohorts WHERE cohort = 'returning'
),
cadence AS (
  SELECT
    COUNT(*) FILTER (WHERE ltm_invoices >= 6) AS frequent_count,
    COUNT(*) FILTER (WHERE ltm_invoices BETWEEN 2 AND 5) AS occasional_count,
    COUNT(*) FILTER (WHERE ltm_invoices = 1) AS one_time_count,
    COALESCE(SUM(ltm_rev) FILTER (WHERE ltm_invoices >= 6), 0) AS frequent_rev,
    COALESCE(SUM(ltm_rev) FILTER (WHERE ltm_invoices BETWEEN 2 AND 5), 0) AS occasional_rev,
    COALESCE(SUM(ltm_rev) FILTER (WHERE ltm_invoices = 1), 0) AS one_time_rev
  FROM cohorts WHERE COALESCE(ltm_rev, 0) > 0
)
SELECT
  (SELECT COUNT(*) FROM cohorts WHERE COALESCE(ltm_rev, 0) > 0) AS active_ltm,
  (SELECT COUNT(*) FROM cohorts WHERE COALESCE(prior_rev, 0) > 0) AS active_prior_ltm,
  (SELECT COUNT(*) FROM cohorts WHERE cohort = 'new') AS new_dealers,
  (SELECT COUNT(*) FROM cohorts WHERE cohort = 'lapsed') AS lapsed,
  (SELECT COUNT(*) FROM cohorts WHERE cohort = 'returning') AS returning,
  rd.returning_grew, rd.returning_declined, rd.returning_flat,
  ROUND(rd.expansion_dollars::numeric, 0) AS returning_expansion_dollars,
  ROUND(rd.contraction_dollars::numeric, 0) AS returning_contraction_dollars,
  CASE WHEN rd.returning_prior_total > 0
       THEN ROUND(((rd.returning_ltm_total - rd.returning_prior_total) / rd.returning_prior_total * 100)::numeric, 1)
       ELSE NULL END AS same_base_lift_pct,
  c.frequent_count, c.occasional_count, c.one_time_count,
  ROUND(c.frequent_rev::numeric, 0) AS frequent_rev,
  ROUND(c.occasional_rev::numeric, 0) AS occasional_rev,
  ROUND(c.one_time_rev::numeric, 0) AS one_time_rev,
  CASE WHEN sy.new_last_year > 0
       THEN ROUND(sy.returned_from_new::numeric / sy.new_last_year, 3)
       ELSE NULL END AS second_year_return_rate
FROM returning_detail rd
CROSS JOIN cadence c
CROSS JOIN second_year sy
```
**Gating**: needs `invoice_feed_present` AND ≥2 contiguous years of invoice data (same as Q-ECON-NRR). Single-row output; if the CTE produces zero rows (org with <12 months data), the pipeline handles it as None.

**External claim rules**: *"Your dealer count barely moved (7,807 → 7,570) but the flow underneath was much larger — 2,870 new, 3,107 lapsed."* Cohort labels are observational (bought/didn't buy), not a value judgment. Second-year return rate is a leading indicator — "every 5-point move is ~$X on the new-dealer base."

---
