# Health Intelligence v2 — Data Retrieval Specification

Version: 2.3.0
Implements: README v2.5.1

> README.md and QUERIES.md version independently. QUERIES.md version increments when query logic, schema notes, or execution behavior changes. README.md version increments when scoring rules, thresholds, or output contracts change. The "Implements" field above identifies which README version this query file was last validated against.
Effective: 2026-04-14

> **Changelog — v2.3.0 (2026-04-14)**
> - Q-MAL: `mrr`, `arr`, `cohort_year` added as required output columns (now sourced from MAL CSV).
> - Q-ORG: `arr` removed from SELECT. ARR is no longer sourced from `org_summary` — it is authoritative in the MAL CSV. Input-to-query mapping table updated accordingly.
>
> **Changelog — v2.2.0 (2026-04-06)**
> - Implements README v2.4.0. No query SQL changes. Version bumped to reflect README alignment after eligibility rewrite (active subscription gate, HubSpot/ARR warning-only demotion).

---

## 0. Preflight Validation (Blocking)

These checks must pass before the operator runs any scoring queries. If a preflight fails, the operator halts with an explicit error.

### PF-1: HubSpot Join Key

The join between `org_summary` and HubSpot uses `org_summary.hubspot_company_id` → `hubspot.company.company_id`.

**Validation query** (BigQuery):

```sql
SELECT
  COUNT(*) AS total_orgs,
  COUNTIF(hubspot_company_id IS NOT NULL) AS with_hs_id,
  COUNTIF(hubspot_company_id IS NULL) AS without_hs_id
FROM `supercat-data-pipeline.insightful_product.org_summary`
```

**Pass condition**: `with_hs_id / total_orgs >= 0.80`. If fewer than 80% of org_summary rows have a hubspot_company_id, the join is unreliable and the operator must halt.

**Confirmed**: As of 2026-04-03, the join works. Sample validated: `org_summary.hubspot_company_id` successfully joins to `hubspot.company.company_id` returning `properties_engagement_status`, `properties_type`, and `properties_name`.

### PF-2: Mixpanel Org Attribution

Mixpanel events carry org identity in two different columns depending on the event source:

| Column | Populated By | Coverage |
|---|---|---|
| `organization_shortname` | Web/API events (`api_access`) | 100% of `api_access` events, 0% of all others |
| `current_organization_shortname` | iPad/mobile events (presentations, kits, documents, etc.) | 100% of iPad events, 0% of `api_access` |

The two fields are mutually exclusive. Q-MP uses `COALESCE(organization_shortname, current_organization_shortname)` to unify them.

**Pass condition**: The operator counts distinct orgs resolved via either field. If coverage drops below 100 orgs, halt and investigate.

### PF-3: Postgres Org ID Resolution

Postgres tables use `organization_id` (integer), not `org_shortname`. The `organizations` table provides the mapping: `organizations.id` → `organizations.shortname`.

**Validation**: The operator must confirm `organizations.shortname` is populated for all orgs returned by the eligibility step.

### PF-4: Help Scout Org Mapping

Help Scout `conversations` do not have a direct `org_shortname` field. Attribution uses the `primaryCustomer.email` domain, matched against a domain-to-org mapping derived from Postgres `users` + `org_users` tables. Generic email domains (`gmail.com`, `yahoo.com`, `supercatsolutions.com`, etc.) are excluded from the mapping.

`customFields` is always empty (`[]`) across all conversations and is not usable for attribution.

**Mapping coverage**: 4,792 domain-to-org mappings from Postgres. Covers ~95% of eligible entities. Orgs whose contacts exclusively use personal email addresses are not attributable.

**Pass condition**: Non-blocking. If the domain mapping file is unavailable or no orgs are matched, the operator logs a warning and continues. RM-3 is gated by a `_support_data_reliable` flag that only fires when attribution is present.

Treat all Q-HELP outputs as `degrading` criticality. Missing Help Scout data does not block scoring.

---

## 1. Data Source Reference

| Source ID | System | Connection | Dataset / Schema | Key Tables |
|---|---|---|---|---|
| BQ-ORG | BigQuery | MCP `user-bigquery-vpn` | `insightful_product` | `org_summary` |
| BQ-MP | BigQuery | MCP `user-bigquery-vpn` | `mixpanel` | `events` |
| BQ-HS | BigQuery | MCP `user-bigquery-vpn` | `hubspot` | `company` |
| BQ-HELP | BigQuery | MCP `user-bigquery-vpn` | `helpscout` | `conversations` |
| PG | Postgres | MCP `user-supercat-postgres-vpn` | `public` | `organizations`, `products`, `customers`, `orders`, `import_events`, `data_versions`, `smart_stacks`, `org_users` |
| CSV | Local file | Filesystem | — | Master Account List |

### BigQuery Source Separation

| Category | Tables | Contains |
|---|---|---|
| **Curated** | `insightful_product.org_summary` | Pre-joined reference data: org identity, HubSpot link, ARR, config flags. 484 rows. Behavioral fields are **all-time cumulative** — not 90-day windowed. |
| **Raw (Airbyte/Hevo/WELD)** | `mixpanel.events`, `hubspot.company`, `helpscout.conversations` | Source-of-truth event and entity data. All time-windowed metrics must come from raw tables. |

### org_summary: Reference-Only Fields

These fields from `org_summary` are used for identity, config, and join keys only. They are **not scoreable inputs**.

| Field | Use |
|---|---|
| `org_shortname` | Canonical entity key |
| `org_name` | Display name |
| `hubspot_company_id` | Join key to HubSpot |
| `has_clicky_portal` | Config flag for Clicky analytics presence |
| `portal_visitors_daily` | Clicky-sourced metric — acceptable as reference for catalog bundles |
| `is_active` | Reference flag (not used for eligibility — HubSpot is authoritative) |

> **`arr` removed from org_summary usage (2026-04-14):** ARR is now sourced from the MAL CSV. `org_summary.arr` is not selected and must not be used for RM-1 or any ARR-dependent logic.

All `mp_*` fields in org_summary (`mp_total_logins`, `mp_submit_order`, etc.) are **all-time cumulative totals** and must not be used for time-windowed scoring. Use `mixpanel.events` with explicit date filters instead.

---

## 2. Validated Mixpanel Event Mapping

Discovered from `mixpanel.events` on 2026-04-03. Only events relevant to README inputs are included.

| Raw `event_name` | README Metric Name | README Section | Org Attribution Field |
|---|---|---|---|
| `api_access` | `logins_90d` (proxy) | §4.1 Engagement | `organization_shortname` |
| `product_search` | `mp_search_products` | §4.2 Adoption #1 | `current_organization_shortname` |
| `customer_selection` | `mp_select_a_customer` | §4.2 Adoption #2 | `current_organization_shortname` |
| `item_added_via_magic_button` | `mp_item_added_via_magic_button` | §4.2 Adoption #3 | `current_organization_shortname` |
| `item_email_drafted` | `mp_item_email_drafted` | §4.2 Adoption #4, §4.3 Value Delivery | `current_organization_shortname` |
| `pdf_catalog_generated` | `mp_create_pdf_catalog` | §4.2 Adoption #5 | `current_organization_shortname` |
| `view_document` | `mp_view_document` | §4.2 Adoption #6 | `current_organization_shortname` |
| `order_submitted` | `mp_submit_order` | §4.2 Adoption #9, §6.1 Upgrade Signal | `current_organization_shortname` |
| `view_portal` | `mp_access_sales_portal` | §4.2 Adoption #10, §4.3 Value Delivery | `current_organization_shortname` |
| `add_configured_item_to_order` | `mp_order_configured_item` | §6.2 Feature Gap (CPQ) | `current_organization_shortname` |
| `document_email_drafted` | `mp_document_email_drafted` | §4.3 Value Delivery | `current_organization_shortname` |

### Event Name Corrections

The README uses metric names (e.g., `mp_search_products`) that differ from the actual Mixpanel `event_name` values. The mapping above is the canonical translation. The operator must use the raw `event_name` column values from this table.

**org_summary name mismatches** (for awareness only — org_summary behavioral fields are not used for scoring):

| org_summary field | Actual raw event_name |
|---|---|
| `search_products` | `product_search` |
| `select_a_customer` | `customer_selection` |
| `mp_submit_order` | `order_submitted` |
| `order_configured_item` | `add_configured_item_to_order` |
| `create_pdf_catalog` | `pdf_catalog_generated` |
| `access_sales_portal` | `view_portal` |

### Login Proxy

There is no explicit "login" event in Mixpanel. The `api_access` event fires when a user authenticates and accesses the API. It carries `organization_shortname` and serves as the login proxy for:
- `logins_90d` = COUNT of `api_access` events per org (current period)
- `active_users_90d` = COUNT(DISTINCT `distinct_id`) of `api_access` events per org (current period)

### Org Attribution Strategy

Every Mixpanel event carries org identity in exactly one of two columns:

| Column | Set By |
|---|---|
| `organization_shortname` | `api_access` (web/API logins) |
| `current_organization_shortname` | iPad/mobile actions (presentations, searches, orders, etc.) |

The two fields are mutually exclusive. Q-MP uses a single `all_events` CTE that applies `COALESCE(organization_shortname, current_organization_shortname)` to produce one unified `org_shortname` per event row. No intermediate user-mapping CTE is needed.

---

## 3. Input-to-Query Mapping Table

Every README input is traced to exactly one query. The `Criticality` column determines missing-data behavior per README §3.4.

| Criticality | Meaning |
|---|---|
| **blocking** | If missing, the dimension cannot be scored. Counts toward the 3-dimension block threshold. |
| **degrading** | If missing, the dimension is scored with reduced precision. Flagged in `missing_data_flags`. |
| **optional** | If missing, the component is skipped or set to neutral. No flag needed unless it affects classification. |

| README Input | README Section | Query ID | Output Column | Source Table | Criticality |
|---|---|---|---|---|---|
| `org_shortname` | §1 | Q-MAL | `org_shortname` | Master Account List CSV | blocking |
| `parent_entity` | §1 | Q-MAL | `parent_entity` | Master Account List CSV | optional |
| `bundle` | §2 | Q-MAL | `bundle` | Master Account List CSV | blocking |
| `engagement_status` | §1.1 | Q-HS | `engagement_status` | `hubspot.company` | blocking |
| `type` | §1.1 | Q-HS | `hs_type` | `hubspot.company` | blocking |
| `arr` | §1, §5 RM-1 | Q-MAL | `arr` | Master Account List CSV (Pricing Refresh Master Data) | blocking |
| `mrr` | §1.4 | Q-MAL | `mrr` | Master Account List CSV (Pricing Refresh Master Data) | optional |
| `cohort_year` | §1.4 | Q-MAL | `cohort_year` | Master Account List CSV (Pricing Refresh Master Data) | optional |
| `org_name` | §9 | Q-ORG | `org_name` | `insightful_product.org_summary` | optional |
| `hubspot_company_id` | join key | Q-ORG | `hubspot_company_id` | `insightful_product.org_summary` | blocking |
| `has_clicky_portal` | telemetry | Q-ORG | `has_clicky_portal` | `insightful_product.org_summary` | optional |
| `portal_visitors_daily` | §4.2 #8 | Q-ORG | `portal_visitors_daily` | `insightful_product.org_summary` | degrading |
| `logins_90d` | §4.1 | Q-MP | `logins_90d` | `mixpanel.events` (api_access) | blocking |
| `logins_prior_90d` | §4.5 | Q-MP | `logins_prior_90d` | `mixpanel.events` (api_access) | degrading |
| `active_users_90d` | §4.1 | Q-MP | `active_users_90d` | `mixpanel.events` (api_access) | blocking |
| `total_users` | §4.1 | Q-PG-USERS | `total_users` | `pg.org_users` | blocking |
| `mp_search_products` | §4.2 #1 | Q-MP | `mp_search_products` | `mixpanel.events` | blocking |
| `mp_select_a_customer` | §4.2 #2 | Q-MP | `mp_select_a_customer` | `mixpanel.events` | blocking |
| `mp_item_added_via_magic_button` | §4.2 #3, §4.3 | Q-MP | `mp_item_added_via_magic_button` | `mixpanel.events` | blocking |
| `mp_item_email_drafted` | §4.2 #4, §4.3 | Q-MP | `mp_item_email_drafted` | `mixpanel.events` | degrading |
| `mp_create_pdf_catalog` | §4.2 #5, §4.3, §6.2 | Q-MP | `mp_create_pdf_catalog` | `mixpanel.events` | degrading |
| `mp_view_document` | §4.2 #6 | Q-MP | `mp_view_document` | `mixpanel.events` | degrading |
| `mp_submit_order` | §4.2 #9, §6.1 | Q-MP | `mp_submit_order` | `mixpanel.events` | blocking (Cart/Full only) |
| `mp_access_sales_portal` | §4.2 #10, §4.3 | Q-MP | `mp_access_sales_portal` | `mixpanel.events` | blocking (Portal/Full only) |
| `mp_access_sales_portal_prior` | §4.5 | Q-MP | `mp_access_sales_portal_prior` | `mixpanel.events` | degrading |
| `mp_order_configured_item` | §6.2 | Q-MP | `mp_order_configured_item` | `mixpanel.events` | optional |
| `mp_document_email_drafted` | §4.3 | Q-MP | `mp_document_email_drafted` | `mixpanel.events` | degrading |
| `presentation_actions_prior` | §4.5 | Q-MP | `presentation_actions_prior` | `mixpanel.events` (computed) | degrading |
| `smart_stack_count` | §4.2 #7 | Q-PG-STACKS | `smart_stack_count` | `pg.smart_stacks` | degrading |
| `orders_90d` | §4.3, §4.5 | Q-PG-ORD | `orders_90d` | `pg.orders` | blocking (Cart/Full only) |
| `orders_prior_90d` | §4.5 | Q-PG-ORD | `orders_prior_90d` | `pg.orders` | degrading |
| `orders_90d_by_source` | §4.3 | Q-PG-ORD | `ipad_orders_90d`, `online_orders_90d` | `pg.orders` | degrading |
| `orders_exist_any_time` | §6.1 | Q-PG-ORD | `orders_exist_any_time` | `pg.orders` | optional |
| `customer_activation_rate` | §4.3, §6.3 | Q-PG-CUST | `ordering_customers_90d`, `total_customers` | `pg.orders` + `pg.customers` | blocking (Cart/Full only) |
| `dormant_customers` | §6.3 | Q-PG-CUST | `dormant_customers` | `pg.orders` + `pg.customers` | degrading |
| `geographic_cv` | §6.3 | Q-PG-CUST | `geographic_cv` | `pg.orders` | optional |
| `catalog_completeness` | §4.4 | Q-PG-CAT | `catalog_completeness` | `pg.products` | blocking |
| `import_success_rate` | §4.4 | Q-PG-IMP | `import_success_rate` | `pg.import_events` | blocking |
| `last_import_had_errors` | §4.4 | Q-PG-IMP | `last_import_had_errors` | `pg.import_events` | degrading |
| `total_imports_90d` | §4.4 | Q-PG-IMP | `total_imports_90d` | `pg.import_events` | blocking |
| `days_since_critical_update` | §4.4, §5 RM-4 | Q-PG-FRESH | `days_since_critical_update` | `pg.data_versions` | degrading |
| `days_since_update_by_type` | §5 RM-4 | Q-PG-FRESH | `days_since_products`, `days_since_customers`, `days_since_inventories` | `pg.data_versions` | degrading |
| `support_escalations` | §5 RM-3 | Q-HELP | `support_escalations_90d` | `helpscout.conversations` | degrading |

---

## 4. Execution Order

```
Step 1: Q-MAL     → Load Master Account List. Resolve company → org_shortname.
                     Produces entity roster with bundle.
Step 2: Q-ORG     → org_summary reference fields (org_name, hubspot_company_id, ARR, config flags).
         Q-HS     → HubSpot eligibility. Joins through Q-ORG's hubspot_company_id.
Step 3: FILTER    → Intersect Q-MAL ∩ (Q-HS eligible) → eligible entity list.
                     Apply exclusion criteria (test/demo/sample patterns).
                     Apply ARR > 0 rule with parent carveout.
Step 4: ALL REMAINING QUERIES — only for eligible entities:
         Q-MP         (BigQuery batch — all Mixpanel behavioral metrics)
         Q-PG-CAT     (Postgres batch — catalog completeness)
         Q-PG-IMP     (Postgres batch — import health)
         Q-PG-ORD     (Postgres batch — order metrics)
         Q-PG-CUST    (Postgres batch — customer activation + dormancy + geography)
         Q-PG-FRESH   (Postgres batch — data freshness)
         Q-PG-USERS   (Postgres batch — total user counts)
         Q-PG-STACKS  (Postgres batch — smart stack counts)
         Q-HELP       (BigQuery batch — support escalation domains, then domain map join)
Step 5: JOIN      → Join all query outputs by org_shortname.
Step 6: SCORE     → Apply README scoring logic.
         PEER BM  → (Optional) Load Peer Benchmark Layer 2 output via --peer-benchmark.
                     If provided, hv2_pbg_composite_gap replaces the internal bundle-median
                     peer benchmark gap for each org. See §6.4 note below.
Step 7: OUTPUT    → Write CSV.
```

BigQuery queries in Step 4 can run in parallel. Postgres queries in Step 4 can also run in parallel. The only sequential dependency is Steps 1–3 (eligibility) before Step 4 (data retrieval).

### Postgres Cache Mode (`--pg-cache-dir`)

When a direct Postgres connection is unavailable (e.g., running from Cursor without VPN), Postgres queries can be satisfied from pre-fetched CSV files. Pass `--pg-cache-dir /path/to/cache` to the operator. The cache directory must contain:

| File | Populated By | Required? |
|---|---|---|
| `pg_cat.csv` | Q-PG-CAT | yes |
| `pg_imp.csv` | Q-PG-IMP | yes |
| `pg_ord.csv` | Q-PG-ORD | yes |
| `pg_cust.csv` | Q-PG-CUST | yes |
| `pg_fresh.csv` | Q-PG-FRESH | yes |
| `pg_users.csv` | Q-PG-USERS | yes |
| `pg_stacks.csv` | Q-PG-STACKS | yes |
| `pg_sub.csv` | Q-PG-SUB | **REQUIRED** — operator exits with [FATAL] if absent |
| `pg_domain_map.csv` | Q-PG-DOMAIN (used by Q-HELP for org attribution) | yes |

When `--pg-cache-dir` is set, the operator skips the Postgres connection entirely and loads from CSVs. Cache files should be regenerated whenever Postgres data materially changes (imports, new customers, user provisioning). Use the MCP `user-supercat-postgres-vpn` tool to run each query and save the output.

**pg_sub.csv is a hard requirement** (as of v2.5.0): if this file is absent in cache mode, the operator will exit with [FATAL] rather than silently passing all MAL orgs through the subscription gate. Regenerate with Q-PG-SUB before each canonical run.

### Peer Benchmark Mode (`--peer-benchmark`)

As of v2.4.0, the `peer_benchmark_gap` Growth component can be sourced from the standalone Peer Benchmark system instead of the internal bundle-median method.

**Source**: `peer_benchmark_*.csv` from the Peer Benchmark Layer 2 operator (`benchmark_operator.py`). This file is produced by a separate run of the Peer Benchmark system and contains `hv2_pbg_composite_gap` — a cohort-based peer benchmark gap score using vertical × stack peer groups.

**How it differs from the internal method**: The internal method compares an org against all same-bundle entities (bundle-only medians). The Layer 2 method compares an org against entities in the same vertical AND same stack tier (`peer_group_id_effective = "{vertical} / {bundle}"`), with a documented fallback hierarchy when cohort size is too small.

**Regeneration**: Regenerate the Peer Benchmark Layer 2 output each scoring cycle by running:
1. `operator.py` in the Peer Benchmark workspace (Layer 1 — cohort assignment)
2. `benchmark_operator.py` in the Peer Benchmark workspace (Layer 2 — metric calculation)

The `bq_mp_pbg.csv` cache file in the Postgres cache directory must also be regenerated (BigQuery pull — see Peer Benchmark `QUERIES.md` Q-MP-PBG).

**Pass to operator**: `--peer-benchmark /path/to/peer_benchmark_2026-04-03.csv`

---

## 5. Query Definitions

### Q-MAL: Master Account List

**Source**: Local CSV file (`Pricing Refresh Master Data V2 - v2 Master Account.csv` or equivalent maintained file).

**Method**: Pandas `read_csv`.

**Column structure**: The MAL does not contain an `org_shortname` column. It uses `company` (display name). The operator resolves `company` → `org_shortname` in two passes:

1. **Override map** (`MAL_COMPANY_OVERRIDES` in operator.py): An explicit dictionary for names that don't exact-match `org_summary.org_name` (e.g., apostrophes, parenthetical suffixes, partial names). This resolves before the BigQuery lookup.
2. **org_summary name lookup**: The operator queries `org_summary.org_name`, lowercases both sides, and joins on exact match. Unresolved rows are logged as warnings and dropped from scoring.

If a company name cannot be resolved through either pass, it is excluded and logged. This is expected for orgs not yet in `org_summary` (e.g., newly onboarded clients).

**Required columns**: `company`, `parent_entity`, `bundle` (or `stack` — normalized via `BUNDLE_NORMALIZATION` in operator.py), `mrr`, `arr`, `cohort_year`.

**Bundle values**: `iPad-only`, `iPad+Catalog`, `iPad+Catalog+Cart`, `iPad+Catalog+Portal`, `Full`.

**MAL CSV format notes**: Google Sheets exports may include a blank first row and unnamed index columns. The operator auto-detects and skips these. `arr` and `mrr` values are stripped of `$` signs and commas and coerced to numeric at load time.

**Output**:

| Column | Type |
|---|---|
| `org_shortname` | string (resolved from `company`) |
| `parent_entity` | string (nullable) |
| `bundle` | string (normalized to canonical value) |
| `mrr` | float (monthly recurring revenue, contracted) |
| `arr` | float (annual recurring revenue, contracted) |
| `cohort_year` | int (onboarding year) |

---

### Q-ORG: org_summary Reference

**Source**: BigQuery — `insightful_product.org_summary`

```sql
SELECT
  org_shortname,
  org_name,
  hubspot_company_id,
  has_clicky_portal,
  portal_visitors_daily
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname IS NOT NULL
```

**Output**: One row per org with identity, join key, and config flags.

**Note**: Do not select `mp_*` fields or use them for scoring. They are all-time cumulative.

> **ARR removed from Q-ORG (2026-04-14):** `arr` is no longer selected from `org_summary`. It was found to be unreliable for contracted ARR (backward-looking actuals, frequent NULLs, entity-level mismatches for parent accounts). ARR is now authoritative in the MAL CSV (Pricing Refresh Master Data) and loaded via Q-MAL. The `bq_org_ref.csv` cache file may still contain a stale `arr` column from prior runs — regenerate the cache before the next canonical run to avoid confusion.

---

### Q-HS: HubSpot Eligibility

**Source**: BigQuery — `hubspot.company` joined via `org_summary.hubspot_company_id`

```sql
SELECT
  os.org_shortname,
  hc.properties_engagement_status AS engagement_status,
  hc.properties_type AS hs_type,
  hc.properties_annualrevenue AS hs_annual_revenue
FROM `supercat-data-pipeline.insightful_product.org_summary` os
JOIN `supercat-data-pipeline.hubspot.company` hc
  ON os.hubspot_company_id = hc.company_id
WHERE os.org_shortname IS NOT NULL
```

**Eligibility logic** (applied in operator per README §1.1):

```
eligible = (engagement_status = 'Customer')
        OR (engagement_status IS NULL/blank AND hs_type = 'Client')

excluded = (engagement_status = 'Churn')
        OR (engagement_status = 'Lost')
        OR (engagement_status IS NULL/blank AND hs_type IS NULL/blank)
```

**Orgs with NULL HubSpot properties**: Some orgs have a valid `hubspot_company_id` but NULL properties in the company table. These are treated as engagement_status = NULL for eligibility evaluation and excluded unless `hs_type = 'Client'`.

---

### Q-MP: Mixpanel Behavioral Metrics (Batch)

**Source**: BigQuery — `mixpanel.events`

A single batch query producing all time-windowed Mixpanel metrics for all orgs. Attribution is unified via `COALESCE(organization_shortname, current_organization_shortname)` — no intermediate user-mapping join required.

```sql
WITH all_events AS (
  SELECT
    LOWER(COALESCE(
      NULLIF(organization_shortname, ''),
      NULLIF(current_organization_shortname, '')
    )) AS org_shortname,
    event_name,
    distinct_id,
    CASE
      WHEN DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
           >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) THEN 'current'
      ELSE 'prior'
    END AS period
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
        >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY)
    AND COALESCE(
          NULLIF(organization_shortname, ''),
          NULLIF(current_organization_shortname, '')
        ) IS NOT NULL
),

login_metrics AS (
  SELECT
    org_shortname,
    COUNTIF(event_name = 'api_access' AND period = 'current') AS logins_90d,
    COUNTIF(event_name = 'api_access' AND period = 'prior') AS logins_prior_90d,
    COUNT(DISTINCT CASE
      WHEN event_name = 'api_access' AND period = 'current'
      THEN distinct_id END) AS active_users_90d
  FROM all_events
  GROUP BY org_shortname
),

feature_metrics AS (
  SELECT
    org_shortname,
    COUNTIF(event_name = 'product_search' AND period = 'current')
      AS mp_search_products,
    COUNTIF(event_name = 'customer_selection' AND period = 'current')
      AS mp_select_a_customer,
    COUNTIF(event_name = 'item_added_via_magic_button' AND period = 'current')
      AS mp_item_added_via_magic_button,
    COUNTIF(event_name = 'item_email_drafted' AND period = 'current')
      AS mp_item_email_drafted,
    COUNTIF(event_name = 'pdf_catalog_generated' AND period = 'current')
      AS mp_create_pdf_catalog,
    COUNTIF(event_name = 'view_document' AND period = 'current')
      AS mp_view_document,
    COUNTIF(event_name = 'order_submitted' AND period = 'current')
      AS mp_submit_order,
    COUNTIF(event_name = 'view_portal' AND period = 'current')
      AS mp_access_sales_portal,
    COUNTIF(event_name = 'add_configured_item_to_order' AND period = 'current')
      AS mp_order_configured_item,
    COUNTIF(event_name = 'document_email_drafted' AND period = 'current')
      AS mp_document_email_drafted,
    -- Prior period (91–180d) for trajectory
    COUNTIF(event_name = 'item_added_via_magic_button' AND period = 'prior')
    + COUNTIF(event_name = 'item_email_drafted' AND period = 'prior')
    + COUNTIF(event_name = 'pdf_catalog_generated' AND period = 'prior')
    + COUNTIF(event_name = 'document_email_drafted' AND period = 'prior')
      AS presentation_actions_prior,
    COUNTIF(event_name = 'order_submitted' AND period = 'prior')
      AS orders_mp_prior_90d,
    COUNTIF(event_name = 'view_portal' AND period = 'prior')
      AS mp_access_sales_portal_prior
  FROM all_events
  GROUP BY org_shortname
)

SELECT
  COALESCE(l.org_shortname, f.org_shortname) AS org_shortname,
  COALESCE(l.logins_90d, 0) AS logins_90d,
  COALESCE(l.logins_prior_90d, 0) AS logins_prior_90d,
  COALESCE(l.active_users_90d, 0) AS active_users_90d,
  COALESCE(f.mp_search_products, 0) AS mp_search_products,
  COALESCE(f.mp_select_a_customer, 0) AS mp_select_a_customer,
  COALESCE(f.mp_item_added_via_magic_button, 0) AS mp_item_added_via_magic_button,
  COALESCE(f.mp_item_email_drafted, 0) AS mp_item_email_drafted,
  COALESCE(f.mp_create_pdf_catalog, 0) AS mp_create_pdf_catalog,
  COALESCE(f.mp_view_document, 0) AS mp_view_document,
  COALESCE(f.mp_submit_order, 0) AS mp_submit_order,
  COALESCE(f.mp_access_sales_portal, 0) AS mp_access_sales_portal,
  COALESCE(f.mp_order_configured_item, 0) AS mp_order_configured_item,
  COALESCE(f.mp_document_email_drafted, 0) AS mp_document_email_drafted,
  COALESCE(f.presentation_actions_prior, 0) AS presentation_actions_prior,
  COALESCE(f.orders_mp_prior_90d, 0) AS orders_mp_prior_90d,
  COALESCE(f.mp_access_sales_portal_prior, 0) AS mp_access_sales_portal_prior
FROM login_metrics l
FULL OUTER JOIN feature_metrics f ON l.org_shortname = f.org_shortname
```

**Output**: One row per org with all Mixpanel-sourced metrics for both current and prior periods.

---

### Q-PG-CAT: Catalog Completeness

**Source**: Postgres — `organizations` LEFT JOIN `products`

Anchored to `organizations` so orgs with zero products return a row (with `catalog_completeness = NULL`) rather than being silently absent.

```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(*) FILTER (WHERE p.deleted = false) AS total_active_products,
  COUNT(*) FILTER (
    WHERE p.deleted = false
    AND p.image_exists = true
    AND p.net_price IS NOT NULL
    AND p.net_price > 0
  ) AS complete_products,
  CASE
    WHEN COUNT(*) FILTER (WHERE p.deleted = false) = 0 THEN NULL
    ELSE ROUND(
      COUNT(*) FILTER (
        WHERE p.deleted = false
        AND p.image_exists = true
        AND p.net_price IS NOT NULL
        AND p.net_price > 0
      )::numeric
      / COUNT(*) FILTER (WHERE p.deleted = false)::numeric,
      4
    )
  END AS catalog_completeness
FROM organizations o
LEFT JOIN products p ON p.organization_id = o.id
GROUP BY o.shortname
```

**Key field**: `products.image_exists` (boolean) — directly indicates whether a product has at least one image. No need to join to `product_images`.

**Zero-product orgs**: `catalog_completeness` = NULL. The operator applies the README §4.4 weight redistribution when this input is absent.

---

### Q-PG-IMP: Import Health

**Source**: Postgres — `import_events` + `organizations`

**Priority**: This query is more important than Q-PG-FRESH for Operational Health scoring (50% weight vs 20%).

```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(*) FILTER (
    WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
  ) AS total_imports_90d,
  COUNT(*) FILTER (
    WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
    AND ie.data NOT LIKE '%:error%'
    AND ie.data NOT LIKE '%:fatal%'
  ) AS successful_imports_90d,
  CASE
    WHEN COUNT(*) FILTER (
      WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
    ) = 0 THEN NULL
    ELSE ROUND(
      COUNT(*) FILTER (
        WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
        AND ie.data NOT LIKE '%:error%'
        AND ie.data NOT LIKE '%:fatal%'
      )::numeric
      / COUNT(*) FILTER (
        WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
      )::numeric,
      4
    )
  END AS import_success_rate,
  -- Most recent import error status
  (
    SELECT
      CASE
        WHEN ie2.data LIKE '%:error%' OR ie2.data LIKE '%:fatal%' THEN true
        ELSE false
      END
    FROM import_events ie2
    WHERE ie2.organization_id = o.id
    ORDER BY ie2.created_at DESC
    LIMIT 1
  ) AS last_import_had_errors
FROM organizations o
LEFT JOIN import_events ie ON ie.organization_id = o.id
GROUP BY o.id, o.shortname
```

**Import event data format**: YAML text with status markers `:warning`, `:error`, `:fatal`. An import is considered successful if its `data` field contains no `:error` or `:fatal` markers. Warnings alone do not constitute failure.

**No import history**: When `total_imports_90d` = 0, set `import_success_rate` = NULL. The operator applies the README §4.4 redistribution rule (Catalog Completeness 60%, Data Freshness 40%).

---

### Q-PG-ORD: Order Metrics

**Source**: Postgres — `orders` + `organizations`

```sql
SELECT
  o.shortname AS org_shortname,
  -- Current period orders
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true
    AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active'
  ) AS orders_90d,
  -- Prior period orders (for trajectory)
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true
    AND ord.submit_date >= CURRENT_DATE - INTERVAL '180 days'
    AND ord.submit_date < CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active'
  ) AS orders_prior_90d,
  -- Orders by source (for eol_share)
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true
    AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active'
    AND LOWER(ord.order_source) = 'ipad'
  ) AS ipad_orders_90d,
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true
    AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active'
    AND LOWER(ord.order_source) != 'ipad'
  ) AS online_orders_90d,
  -- Any orders ever (for bundle upgrade signal §6.1)
  CASE
    WHEN COUNT(*) FILTER (WHERE ord.is_submitted = true) > 0 THEN true
    ELSE false
  END AS orders_exist_any_time
FROM organizations o
LEFT JOIN orders ord ON ord.organization_id = o.id
GROUP BY o.shortname
```

**Key field**: `orders.order_source` — defaults to `'ipad'`. Non-iPad orders (online/web) have a different value. The `eol_share` metric = `online_orders_90d / orders_90d`.

---

### Q-PG-CUST: Customer Activation and Geography

**Source**: Postgres — `organizations` LEFT JOIN `customers` + `orders`

`org_customer_counts` is anchored to `organizations` so orgs with zero customers return `total_customers = 0` rather than being silently absent.

```sql
WITH customer_orders AS (
  SELECT
    o.shortname AS org_shortname,
    ord.customer_num,
    ord.ship_to_state,
    MAX(ord.submit_date) AS last_order_date,
    COUNT(*) FILTER (
      WHERE ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    ) AS orders_current_period
  FROM orders ord
  JOIN organizations o ON ord.organization_id = o.id
  WHERE ord.is_submitted = true
    AND ord.order_state = 'active'
    AND ord.customer_num IS NOT NULL
  GROUP BY o.shortname, ord.customer_num, ord.ship_to_state
),

org_customer_counts AS (
  SELECT
    o.shortname AS org_shortname,
    COUNT(c.id) AS total_customers
  FROM organizations o
  LEFT JOIN customers c ON c.organization_id = o.id
  GROUP BY o.shortname
),

activation_metrics AS (
  SELECT
    org_shortname,
    COUNT(DISTINCT customer_num) FILTER (
      WHERE orders_current_period > 0
    ) AS ordering_customers_90d,
    COUNT(DISTINCT customer_num) FILTER (
      WHERE orders_current_period = 0
      AND last_order_date IS NOT NULL
    ) AS dormant_customers
  FROM customer_orders
  GROUP BY org_shortname
),

geographic_metrics AS (
  SELECT
    org_shortname,
    CASE
      WHEN COUNT(DISTINCT ship_to_state) < 2 THEN 0
      ELSE ROUND(
        STDDEV(state_order_count)::numeric / NULLIF(AVG(state_order_count), 0)::numeric,
        4
      )
    END AS geographic_cv
  FROM (
    SELECT
      org_shortname,
      ship_to_state,
      SUM(orders_current_period) AS state_order_count
    FROM customer_orders
    WHERE orders_current_period > 0
      AND ship_to_state IS NOT NULL
      AND ship_to_state != ''
    GROUP BY org_shortname, ship_to_state
  ) state_agg
  GROUP BY org_shortname
)

SELECT
  occ.org_shortname,
  occ.total_customers,
  COALESCE(am.ordering_customers_90d, 0) AS ordering_customers_90d,
  COALESCE(am.dormant_customers, 0) AS dormant_customers,
  COALESCE(gm.geographic_cv, 0) AS geographic_cv
FROM org_customer_counts occ
LEFT JOIN activation_metrics am ON occ.org_shortname = am.org_shortname
LEFT JOIN geographic_metrics gm ON occ.org_shortname = gm.org_shortname
```

**Derived by operator**:
- `customer_activation_rate` = `ordering_customers_90d / total_customers`
- Used in §4.3 (Value Delivery) and §6.3 (Customer Headroom)

---

### Q-PG-FRESH: Data Freshness

**Source**: Postgres — `data_versions` + `organizations`

```sql
SELECT
  o.shortname AS org_shortname,
  MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END)
    AS last_products_update,
  MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END)
    AS last_customers_update,
  MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END)
    AS last_inventories_update,
  EXTRACT(DAY FROM (
    CURRENT_TIMESTAMP - GREATEST(
      MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END),
      MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END),
      MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END)
    )
  ))::integer AS days_since_critical_update
FROM organizations o
LEFT JOIN data_versions dv ON dv.organization_id = o.id
  AND dv.entity_type IN ('products', 'customers', 'inventories')
GROUP BY o.shortname
```

**Entity types available** (discovered 2026-04-03): `products` (245 orgs), `customers` (242 orgs), `inventories` (241 orgs), `smart_stacks` (245), plus 19 other types.

**`days_since_critical_update`** = days since the most recent update across products, customers, and inventories. Used in §4.4 and RM-4.

**For RM-4**: The operator also needs per-type days to check whether 2+ entity types exceed 180 days. The query provides `last_products_update`, `last_customers_update`, and `last_inventories_update` for this calculation.

---

### Q-PG-USERS: Total User Counts

**Source**: Postgres — `organizations` LEFT JOIN `org_users` LEFT JOIN `users`

Anchored to `organizations` so orgs with zero provisioned users return a row with `total_users = 0` rather than being silently absent.

**Internal-user exclusion** (implemented 2026-04-07, v2.5.0): Known internal/admin/seeded domains are excluded from the `total_users` count so they do not inflate `active_user_ratio`. The exclusion list was validated via a cross-org domain census (V-1 query) as part of the Data Trust Audit. The following domains are excluded:

| Domain | Org Count | Reason |
|---|---|---|
| `supercatsolutions.com` | 221 | SuperCat internal staff — confirmed |
| `jimmythrasher.com` | 47 | Seeded admin account — confirmed |
| `lojic.com` | 33 | SuperCat developer — confirmed |
| `railsfever.com` | 20 | SuperCat developer — confirmed |
| `samedis.com` | 18 | Implementation-adjacent consultant — likely |
| `upwardtechnologies.com` | 16 | Implementation partner — likely |

```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(ou.id) FILTER (
    WHERE u.email IS NULL
      OR LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN (
        'lojic.com',
        'railsfever.com',
        'samedis.com',
        'supercatsolutions.com',
        'jimmythrasher.com',
        'upwardtechnologies.com'
      )
  ) AS total_users
FROM organizations o
LEFT JOIN org_users ou ON ou.organization_id = o.id
LEFT JOIN users u ON u.id = ou.user_id
GROUP BY o.shortname
```

**Note**: Counts client-representative user accounts per org, excluding confirmed and likely internal/admin users. Used as the denominator for `active_user_ratio` in §4.1. The `INTERNAL_USER_DOMAINS` constant in `operator.py` is the authoritative source for this list — update it there and regenerate `pg_users.csv` to keep in sync.

---

### Q-PG-STACKS: Smart Stack Counts

**Source**: Postgres — `organizations` LEFT JOIN `smart_stacks`

Anchored to `organizations` so orgs with no stacks return `smart_stack_count = 0` rather than being silently absent.

```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(ss.id) AS smart_stack_count
FROM organizations o
LEFT JOIN smart_stacks ss ON ss.organization_id = o.id
GROUP BY o.shortname
```

**Used in**: §4.2 Adoption feature #7 (`smart_stack_count > 0`).

---

### Q-HELP: Help Scout Support Escalations

**Source**: BigQuery — `helpscout.conversations`

**Schema notes**:
- `tags` is a JSON array of objects (e.g., `[{"tag": "l1 - handled by frontline support", ...}]`). Use `TO_JSON_STRING(tags)` for text matching — `CAST(tags AS STRING)` fails.
- `customFields` is always `[]` across all conversations and is not usable for attribution.
- `mailboxId` is a numeric ID, not an org name. Do not use it for attribution.
- Attribution is via `primaryCustomer.email` domain, matched against the domain-to-org mapping in `pg_cache/pg_domain_map.csv`.

**Step 1 — Extract email domains and detect escalations** (BigQuery):

```sql
SELECT
  LOWER(REGEXP_EXTRACT(
    SAFE.STRING(primaryCustomer.email), r'@(.+)$'
  )) AS email_domain,
  COUNTIF(
    LOWER(TO_JSON_STRING(tags)) LIKE '%escalat%'
    OR LOWER(TO_JSON_STRING(tags)) LIKE '%urgent%'
    OR LOWER(TO_JSON_STRING(tags)) LIKE '%critical%'
  ) AS support_escalations_90d,
  COUNT(*) AS support_conversations_90d
FROM `supercat-data-pipeline.helpscout.conversations`
WHERE PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))
      >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND status != 'spam'
  AND SAFE.STRING(primaryCustomer.email) IS NOT NULL
GROUP BY email_domain
HAVING email_domain IS NOT NULL
```

**Step 2 — Map email domains to org_shortname** (operator, using `pg_cache/pg_domain_map.csv`):

The domain mapping is generated from Postgres `users` + `org_users`. Generic domains (`gmail.com`, `yahoo.com`, `hotmail.com`, `aol.com`, `outlook.com`, `icloud.com`, `supercatsolutions.com`, `comcast.net`, `msn.com`, `me.com`, `att.net`, `live.com`) are excluded. The mapping is pre-built and cached — it is not regenerated on each run unless Postgres is live.

The operator joins Step 1 output to the domain map on `email_domain = domain`, then aggregates `support_escalations_90d` and `support_conversations_90d` by `org_shortname`.

**Escalation tag vocabulary** (confirmed in production data): `l1 - handled by frontline support`, `product - ecat`, `s4 - low`, `type: feature request`. Escalation detection uses `escalat`, `urgent`, `critical` keyword matching against the full serialized tags JSON.

**Criticality**: `degrading`. Missing Help Scout data does not block scoring. RM-3 only fires when `_support_data_reliable = true` for the entity.

**Domain mapping dependency**: If `pg_cache/pg_domain_map.csv` is absent, the operator logs a warning and skips Help Scout attribution for the run. Run Q-PG-DOMAIN (below) to regenerate it.

**Q-PG-DOMAIN: Domain-to-Org Mapping** (Postgres, regenerated when Postgres is live):

```sql
WITH domain_counts AS (
  SELECT
    o.shortname AS org_shortname,
    LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) AS domain,
    COUNT(*) AS user_count
  FROM users u
  JOIN org_users ou ON ou.user_id = u.id
  JOIN organizations o ON ou.organization_id = o.id
  WHERE u.email::text LIKE '%@%'
    AND LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN (
      'gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'outlook.com',
      'icloud.com', 'supercatsolutions.com', 'comcast.net', 'msn.com',
      'me.com', 'att.net', 'live.com', 'sbcglobal.net', 'verizon.net',
      'bellsouth.net', 'charter.net', 'cox.net', 'earthlink.net',
      'ymail.com', 'mac.com', 'protonmail.com'
    )
  GROUP BY o.shortname, LOWER(SUBSTRING(u.email::text FROM '@(.+)$'))
),
ranked AS (
  SELECT org_shortname, domain, user_count,
    ROW_NUMBER() OVER (PARTITION BY domain ORDER BY user_count DESC) AS rn
  FROM domain_counts
  WHERE user_count >= 2
)
SELECT org_shortname, domain
FROM ranked
WHERE rn = 1
ORDER BY org_shortname
```

**Output**: `pg_cache/pg_domain_map.csv` with columns `org_shortname`, `domain`.

---

## 6. Data Quality Notes

### Confirmed Findings

#### DQ-1: Mixpanel Attribution

iPad/mobile events carry `current_organization_shortname` at 100% coverage. Web/API events (`api_access`) carry `organization_shortname` at 100% coverage. Q-MP unifies both fields via `COALESCE`. The main remaining attribution gap is anonymous web sessions (no authenticated user) and users who have never triggered either field in the 180-day window.

**Impact**: Monitor by comparing `total_users` (Postgres) vs `active_users_90d` (Mixpanel) per org. A large gap may indicate users who are provisioned but have not authenticated in the scoring window.

#### DQ-2: HubSpot Engagement Status Values

Confirmed values observed in production (2026-04-03):

| engagement_status | type | Count | Eligibility |
|---|---|---|---|
| `Customer` | `Client` | 120 | **Eligible** |
| `Churn` | `Former Client` | 52 | Excluded |
| `Lost` | `Client` | 17 | Excluded |
| `""` (blank) | `Product User` | 96 | Excluded (not Client) |
| NULL | various | varies | Evaluated by fallback rule |

The operator uses `"Churn"` and excludes `"Lost"` explicitly. Both match README §1.1.

#### DQ-3: Help Scout Org Attribution

Attribution uses email-domain matching against a Postgres-derived mapping (4,792 domain-to-org pairs, covering ~95% of eligible entities). The matching is approximate: orgs whose contacts exclusively use generic or personal email addresses are unattributable. Multi-brand sales rep firms with shared email domains may misattribute. RM-3 is gated by `_support_data_reliable` and only fires when the entity has matched support data.

#### DQ-4: Test/Demo/Staging Orgs in Mixpanel

The following org_shortnames appear in Mixpanel data but must be excluded per README §1:
`bpstaging`, `clctest`, `ctest`, `demo`, `demo1`, `demo2`, `demo3`, `demolighting`, `fmsstaging`, `pf_test`, `sc_test`, `tam-staging`, `test1`, `tlastaging`, `ufistaging`, `ufitest`, `vcgstaging`, `vcgcon`, `sccon`.

The exclusion filter (Step 3) removes these before scoring.

---

### Open Questions

#### DQ-5: org_summary Staleness

`org_summary` appears to be a materialized view or periodically refreshed table. Its `last_updated` timestamp should be checked before each run. If `last_updated` is more than 7 days old, ARR and config flags may be stale.

#### DQ-6: Import Event Parsing

Import event `data` is a YAML text blob. Success/failure is determined by scanning for `:error` and `:fatal` markers. This is string matching, not structured parsing. Edge cases:
- An import that fails to start may not create an `import_events` row at all.
- An import with only `:warning` markers is counted as successful.
