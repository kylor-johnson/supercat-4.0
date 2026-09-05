# BigQuery Operationalization Handoff — Health V2 + Peer Benchmark

**For:** Kev  
**From:** Kylor  
**Date:** 2026-04-06  
**Project:** `supercat-data-pipeline` (existing GCP project)  
**Target dataset:** `insightful_product` (already exists, already has `org_summary`)

---

## What This Is

We have a working client health scoring system (Health V2) and peer benchmarking system (Peer Benchmark) that run as Python scripts and currently read/write CSV files. The scoring logic, formulas, and output contracts are fully validated and documented.

The goal is to migrate the data layer to BigQuery so:

1. The MAL (master account list) lives as a BQ table instead of a local CSV
2. Postgres behavioral data is synced to BQ so we don't need a live VPN connection to run scores
3. Health scores and peer benchmark results write directly to BQ tables (partitioned by run date) instead of CSV files
4. Downstream reports (EBR, external reports) can query scored results directly from BQ

**This is a data infrastructure change only. No scoring logic changes.**

---

## Current Architecture (what exists today)

```
[Local CSV]           master_account_list_*.csv          → Health V2 reads directly
[Postgres / VPN]      organizations, products, orders,
                      customers, subscriptions,
                      import_events, data_versions,
                      smart_stacks, org_users             → Health V2 reads via live connection
                                                            or manual CSV cache files
[BigQuery - live]     mixpanel.events                    → Health V2 reads directly
[BigQuery - live]     hubspot.company                    → Health V2 reads directly
[BigQuery - live]     insightful_product.org_summary     → Health V2 reads directly (join/ref only)
[BigQuery - live]     helpscout.conversations            → Health V2 reads directly

[Local CSV output]    client_health_scores_*.csv         → Layer 1 Peer Benchmark reads
[Local CSV output]    peer_cohort_assignments_*.csv      → Layer 2 Peer Benchmark reads
[Local CSV output]    peer_benchmark_*.csv               → External reports read
```

---

## Target Architecture (after migration)

```
[BigQuery]   insightful_product.master_account_list     ← NEW: replaces local CSV
[BigQuery]   ecat.organizations                         ← NEW: Postgres sync
[BigQuery]   ecat.products                              ← NEW: Postgres sync
[BigQuery]   ecat.orders                                ← NEW: Postgres sync
[BigQuery]   ecat.customers                             ← NEW: Postgres sync
[BigQuery]   ecat.subscriptions                         ← NEW: Postgres sync (highest priority)
[BigQuery]   ecat.import_events                         ← NEW: Postgres sync
[BigQuery]   ecat.data_versions                         ← NEW: Postgres sync
[BigQuery]   ecat.smart_stacks                          ← NEW: Postgres sync
[BigQuery]   ecat.org_users                             ← NEW: Postgres sync

[BigQuery]   insightful_product.client_health_scores    ← NEW: Health V2 writes here (partitioned)
[BigQuery]   insightful_product.peer_benchmark          ← NEW: Peer Benchmark writes here (partitioned)
```

All existing BigQuery sources (`mixpanel.events`, `hubspot.company`, `insightful_product.org_summary`, `helpscout.conversations`) stay exactly as-is. No changes to those tables.

---

## Part 1: Three New BigQuery Tables

### Table 1: `insightful_product.master_account_list`

Replaces `/Health V2/inputs/master_account_list_*.csv`. Manually maintained (small, ~100 rows). We'll populate it from the current canonical CSV and update it going forward instead of editing CSVs.

```sql
CREATE TABLE `supercat-data-pipeline.insightful_product.master_account_list` (
  org_shortname   STRING    NOT NULL,   -- canonical entity key (e.g. 'bcf', 'ta')
  company         STRING    NOT NULL,   -- display name from MAL
  parent_entity   STRING,               -- parent company name (nullable)
  ord_id          STRING,               -- informational field from original MAL
  bundle          STRING    NOT NULL,   -- one of: iPad-only | iPad+Catalog | iPad+Catalog+Cart | iPad+Catalog+Portal | Full
  updated_at      TIMESTAMP NOT NULL    -- row-level freshness, default CURRENT_TIMESTAMP
);
```

**Notes:**
- `org_shortname` should be unique. Add a constraint or rely on the operator to deduplicate.
- `bundle` values are normalized to the exact strings above — no variations.
- We maintain this table manually; no automated pipeline needed.

---

### Table 2: `insightful_product.client_health_scores`

Replaces `Health V2/runs/*/client_health_scores_*.csv`. Partitioned by `run_date` so every run's output is preserved and queryable. The operator appends rows; it does not overwrite.

```sql
CREATE TABLE `supercat-data-pipeline.insightful_product.client_health_scores`
PARTITION BY run_date
AS (
  SELECT
    CAST(NULL AS STRING)    AS org_shortname,
    CAST(NULL AS STRING)    AS org_name,
    CAST(NULL AS STRING)    AS parent_entity,
    CAST(NULL AS STRING)    AS bundle,
    CAST(NULL AS FLOAT64)   AS arr,
    CAST(NULL AS STRING)    AS arr_source,           -- 'direct' | 'parent' | 'none'
    CAST(NULL AS INT64)     AS health_score,         -- 0–100, null if blocked
    CAST(NULL AS STRING)    AS health_band,          -- Thriving | Healthy | Watch | At Risk | Critical
    CAST(NULL AS INT64)     AS growth_score,         -- 0–100, null if blocked
    CAST(NULL AS STRING)    AS growth_band,          -- Prime | Ready | Developing | Not Ready
    CAST(NULL AS STRING)    AS classification,       -- Expand | Stabilize First | Maintain | Intervene | BLOCKED
    CAST(NULL AS BOOL)      AS churn_risk,
    CAST(NULL AS STRING)    AS churn_risk_severity,  -- immediate | near-term | monitored | null
    CAST(NULL AS BOOL)      AS expansion_ready,
    CAST(NULL AS STRING)    AS expansion_type,       -- bundle_upgrade_signal | feature_gap | customer_headroom | null
    CAST(NULL AS BOOL)      AS healthy_complete,
    CAST(NULL AS INT64)     AS engagement_score,
    CAST(NULL AS INT64)     AS adoption_score,
    CAST(NULL AS INT64)     AS value_delivery_score,
    CAST(NULL AS INT64)     AS operational_health_score,
    CAST(NULL AS INT64)     AS trajectory_score,
    CAST(NULL AS INT64)     AS bundle_upgrade_signal,
    CAST(NULL AS INT64)     AS feature_gap_score,
    CAST(NULL AS INT64)     AS customer_headroom_score,
    CAST(NULL AS INT64)     AS peer_benchmark_gap,
    CAST(NULL AS STRING)    AS risk_modifier_applied, -- RM-1 | RM-2 | RM-3 | RM-4 | null
    CAST(NULL AS STRING)    AS scoring_status,        -- complete | partial | blocked
    CAST(NULL AS STRING)    AS missing_data_flags,
    CAST(NULL AS STRING)    AS score_explanation,
    CAST(NULL AS BOOL)      AS hs_lifecycle_stale,   -- warning flag: HubSpot Lost/Churn/missing
    CAST(NULL AS BOOL)      AS hs_join_missing,      -- warning flag: no HubSpot join
    CAST(NULL AS BOOL)      AS arr_data_gap,         -- warning flag: NULL or zero ARR
    CAST(NULL AS DATE)      AS run_date              -- partition key
  WHERE FALSE
);
```

**Downstream query pattern:**
```sql
-- Latest run only
SELECT *
FROM `supercat-data-pipeline.insightful_product.client_health_scores`
WHERE run_date = (
  SELECT MAX(run_date)
  FROM `supercat-data-pipeline.insightful_product.client_health_scores`
)
ORDER BY health_score DESC;
```

---

### Table 3: `insightful_product.peer_benchmark`

Replaces both `peer_cohort_assignments_*.csv` and `peer_benchmark_*.csv`. Combines Layer 1 cohort assignment and Layer 2 benchmark metrics in one table. Partitioned by `run_date`.

```sql
CREATE TABLE `supercat-data-pipeline.insightful_product.peer_benchmark`
PARTITION BY run_date
AS (
  SELECT
    -- Identity
    CAST(NULL AS STRING)  AS org_shortname,
    CAST(NULL AS STRING)  AS org_name,
    CAST(NULL AS STRING)  AS bundle,
    CAST(NULL AS STRING)  AS vertical,               -- from HubSpot properties_segment, null if unresolved
    -- Cohort assignment (Layer 1)
    CAST(NULL AS STRING)  AS peer_group_id,
    CAST(NULL AS STRING)  AS peer_group_id_effective,
    CAST(NULL AS STRING)  AS peer_group_level,        -- tier1 | tier2 | tier3 | tier4
    CAST(NULL AS INT64)   AS peer_group_n,            -- steady-state peers used for percentile math
    CAST(NULL AS BOOL)    AS benchmark_eligible,
    CAST(NULL AS STRING)  AS benchmark_confidence,    -- high | medium | low | none
    CAST(NULL AS STRING)  AS lifecycle_stage,         -- steady_state | ramping | onboarding
    CAST(NULL AS STRING)  AS peer_orgs,               -- pipe-separated org_shortnames
    -- Commercial context
    CAST(NULL AS STRING)  AS arr_band,
    CAST(NULL AS STRING)  AS catalog_scale,
    CAST(NULL AS STRING)  AS customer_scale,
    CAST(NULL AS STRING)  AS tenure_band,
    -- Benchmark metrics — health_score
    CAST(NULL AS FLOAT64) AS health_score_org,
    CAST(NULL AS FLOAT64) AS health_score_peer_median,
    CAST(NULL AS FLOAT64) AS health_score_pctile,
    CAST(NULL AS FLOAT64) AS health_score_vs_median,
    CAST(NULL AS STRING)  AS health_score_quartile,
    -- Benchmark metrics — value_delivery_score
    CAST(NULL AS FLOAT64) AS value_delivery_score_org,
    CAST(NULL AS FLOAT64) AS value_delivery_score_peer_median,
    CAST(NULL AS FLOAT64) AS value_delivery_score_pctile,
    CAST(NULL AS FLOAT64) AS value_delivery_score_vs_median,
    CAST(NULL AS STRING)  AS value_delivery_score_quartile,
    -- Benchmark metrics — adoption_score
    CAST(NULL AS FLOAT64) AS adoption_score_org,
    CAST(NULL AS FLOAT64) AS adoption_score_peer_median,
    CAST(NULL AS FLOAT64) AS adoption_score_pctile,
    CAST(NULL AS FLOAT64) AS adoption_score_vs_median,
    CAST(NULL AS STRING)  AS adoption_score_quartile,
    -- Benchmark metrics — engagement_score
    CAST(NULL AS FLOAT64) AS engagement_score_org,
    CAST(NULL AS FLOAT64) AS engagement_score_peer_median,
    CAST(NULL AS FLOAT64) AS engagement_score_pctile,
    CAST(NULL AS FLOAT64) AS engagement_score_vs_median,
    CAST(NULL AS STRING)  AS engagement_score_quartile,
    -- Benchmark metrics — operational_health_score
    CAST(NULL AS FLOAT64) AS operational_health_score_org,
    CAST(NULL AS FLOAT64) AS operational_health_score_peer_median,
    CAST(NULL AS FLOAT64) AS operational_health_score_pctile,
    CAST(NULL AS FLOAT64) AS operational_health_score_vs_median,
    CAST(NULL AS STRING)  AS operational_health_score_quartile,
    -- Benchmark metrics — trajectory_score
    CAST(NULL AS FLOAT64) AS trajectory_score_org,
    CAST(NULL AS FLOAT64) AS trajectory_score_peer_median,
    CAST(NULL AS FLOAT64) AS trajectory_score_pctile,
    CAST(NULL AS FLOAT64) AS trajectory_score_vs_median,
    CAST(NULL AS STRING)  AS trajectory_score_quartile,
    -- Benchmark metrics — orders_90d (Cart + Full only)
    CAST(NULL AS FLOAT64) AS orders_90d_org,
    CAST(NULL AS FLOAT64) AS orders_90d_peer_median,
    CAST(NULL AS FLOAT64) AS orders_90d_pctile,
    CAST(NULL AS FLOAT64) AS orders_90d_vs_median,
    CAST(NULL AS STRING)  AS orders_90d_quartile,
    -- Benchmark metrics — catalog_completeness (Catalog+ only)
    CAST(NULL AS FLOAT64) AS catalog_completeness_org,
    CAST(NULL AS FLOAT64) AS catalog_completeness_peer_median,
    CAST(NULL AS FLOAT64) AS catalog_completeness_pctile,
    CAST(NULL AS FLOAT64) AS catalog_completeness_vs_median,
    CAST(NULL AS STRING)  AS catalog_completeness_quartile,
    -- Benchmark metrics — login_intensity
    CAST(NULL AS FLOAT64) AS login_intensity_org,
    CAST(NULL AS FLOAT64) AS login_intensity_peer_median,
    CAST(NULL AS FLOAT64) AS login_intensity_pctile,
    CAST(NULL AS FLOAT64) AS login_intensity_vs_median,
    CAST(NULL AS STRING)  AS login_intensity_quartile,
    -- Health V2 PBG composite (replaces bundle-median fallback in Growth score)
    CAST(NULL AS FLOAT64) AS hv2_pbg_login_intensity_pctile,
    CAST(NULL AS FLOAT64) AS hv2_pbg_primary_value_pctile,
    CAST(NULL AS FLOAT64) AS hv2_pbg_adoption_pctile,
    CAST(NULL AS STRING)  AS hv2_pbg_primary_value_metric_id,
    CAST(NULL AS INT64)   AS hv2_pbg_composite_gap,  -- 0–100, consumed by Health V2 Growth score
    CAST(NULL AS DATE)    AS run_date                 -- partition key
  WHERE FALSE
);
```

---

## Part 2: Postgres → BigQuery Sync

The Health V2 scoring engine needs data from the eCat application Postgres database. Currently this is either a live VPN connection or manually exported CSV cache files. Both are fragile.

### Recommended approach

Set up a recurring sync (nightly is sufficient) from the eCat Postgres DB to a new dataset in BigQuery. We already have service account credentials (`supercat-data-pipeline-*.json`). Recommend Airbyte, Fivetran, or a custom Cloud Run job depending on what's simplest to operate.

The target dataset can be `ecat` (new) or a schema within `insightful_product`. Suggested: `ecat` to keep it clearly separated from curated output tables.

### Tables to sync (in priority order)

| Priority | Postgres table | Why needed | BQ query used for |
|---|---|---|---|
| 🔴 High | `organizations` | Join key for everything — shortname, id, created_at | All Postgres queries |
| 🔴 High | `subscriptions` | **Eligibility gate** — `status = 'active'` is the primary inclusion criterion | `pg_sub` — blocks scoring if missing |
| 🟡 Medium | `products` | Catalog completeness scoring | `pg_cat` |
| 🟡 Medium | `orders` | Order volume, online order share, customer activation | `pg_ord`, `pg_cust` |
| 🟡 Medium | `customers` | Total customer count per org | `pg_cust` |
| 🟡 Medium | `org_users` | Total user count per org (engagement denominator) | `pg_users` |
| 🟡 Medium | `smart_stacks` | Stack/list feature adoption | `pg_stacks` |
| 🟠 Lower | `import_events` | Import health scoring (operational health dimension) | `pg_imp` |
| 🟠 Lower | `data_versions` | Data freshness scoring (operational health dimension) | `pg_fresh` |

### Exact SQL the operators run against these tables

These are verbatim queries from the current `Health V2/operator.py`. Kev can use these to validate the sync is working correctly after setup.

**Subscriptions (eligibility gate):**
```sql
SELECT
  o.shortname AS org_shortname,
  BOOL_OR(s.status = 'active') AS has_active_sub
FROM organizations o
LEFT JOIN subscriptions s ON s.organization_id = o.id
GROUP BY o.shortname
```

**Catalog completeness:**
```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(*) FILTER (WHERE p.deleted = false) AS total_active_products,
  COUNT(*) FILTER (
    WHERE p.deleted = false AND p.image_exists = true
    AND p.net_price IS NOT NULL AND p.net_price > 0
  ) AS complete_products,
  CASE WHEN COUNT(*) FILTER (WHERE p.deleted = false) = 0 THEN NULL
  ELSE ROUND(
    COUNT(*) FILTER (
      WHERE p.deleted = false AND p.image_exists = true
      AND p.net_price IS NOT NULL AND p.net_price > 0
    )::numeric / COUNT(*) FILTER (WHERE p.deleted = false)::numeric, 4)
  END AS catalog_completeness
FROM organizations o
LEFT JOIN products p ON p.organization_id = o.id
GROUP BY o.shortname
```

**Order metrics:**
```sql
SELECT
  o.shortname AS org_shortname,
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active') AS orders_90d,
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true
    AND ord.submit_date >= CURRENT_DATE - INTERVAL '180 days'
    AND ord.submit_date < CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active') AS orders_prior_90d,
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active' AND LOWER(ord.order_source) = 'ipad') AS ipad_orders_90d,
  COUNT(*) FILTER (
    WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
    AND ord.order_state = 'active' AND LOWER(ord.order_source) != 'ipad') AS online_orders_90d,
  CASE WHEN COUNT(*) FILTER (WHERE ord.is_submitted = true) > 0
       THEN true ELSE false END AS orders_exist_any_time
FROM organizations o
LEFT JOIN orders ord ON ord.organization_id = o.id
GROUP BY o.shortname
```

**Customer activation and dormancy:**
```sql
WITH customer_orders AS (
  SELECT o.shortname AS org_shortname, ord.customer_num, ord.ship_to_state,
    MAX(ord.submit_date) AS last_order_date,
    COUNT(*) FILTER (WHERE ord.submit_date >= CURRENT_DATE - INTERVAL '90 days')
      AS orders_current_period
  FROM orders ord JOIN organizations o ON ord.organization_id = o.id
  WHERE ord.is_submitted = true AND ord.order_state = 'active' AND ord.customer_num IS NOT NULL
  GROUP BY o.shortname, ord.customer_num, ord.ship_to_state
),
org_customer_counts AS (
  SELECT o.shortname AS org_shortname, COUNT(c.id) AS total_customers
  FROM organizations o
  LEFT JOIN customers c ON c.organization_id = o.id
  GROUP BY o.shortname
),
activation_metrics AS (
  SELECT org_shortname,
    COUNT(DISTINCT customer_num) FILTER (WHERE orders_current_period > 0) AS ordering_customers_90d,
    COUNT(DISTINCT customer_num) FILTER (
      WHERE orders_current_period = 0 AND last_order_date IS NOT NULL) AS dormant_customers
  FROM customer_orders GROUP BY org_shortname
),
geographic_metrics AS (
  SELECT org_shortname,
    CASE WHEN COUNT(DISTINCT ship_to_state) < 2 THEN 0
    ELSE ROUND(STDDEV(state_order_count)::numeric
         / NULLIF(AVG(state_order_count), 0)::numeric, 4) END AS geographic_cv
  FROM (
    SELECT org_shortname, ship_to_state, SUM(orders_current_period) AS state_order_count
    FROM customer_orders
    WHERE orders_current_period > 0 AND ship_to_state IS NOT NULL AND ship_to_state != ''
    GROUP BY org_shortname, ship_to_state
  ) state_agg GROUP BY org_shortname
)
SELECT occ.org_shortname, occ.total_customers,
  COALESCE(am.ordering_customers_90d, 0) AS ordering_customers_90d,
  COALESCE(am.dormant_customers, 0) AS dormant_customers,
  COALESCE(gm.geographic_cv, 0) AS geographic_cv
FROM org_customer_counts occ
LEFT JOIN activation_metrics am ON occ.org_shortname = am.org_shortname
LEFT JOIN geographic_metrics gm ON occ.org_shortname = gm.org_shortname
```

**Import health:**
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
  CASE WHEN COUNT(*) FILTER (
    WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days') = 0 THEN NULL
  ELSE ROUND(
    COUNT(*) FILTER (
      WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
      AND ie.data NOT LIKE '%:error%' AND ie.data NOT LIKE '%:fatal%'
    )::numeric / COUNT(*) FILTER (
      WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days')::numeric, 4)
  END AS import_success_rate,
  (SELECT CASE
    WHEN ie2.data LIKE '%:error%' OR ie2.data LIKE '%:fatal%' THEN true
    ELSE false END
   FROM import_events ie2
   WHERE ie2.organization_id = o.id
   ORDER BY ie2.created_at DESC LIMIT 1
  ) AS last_import_had_errors
FROM organizations o
LEFT JOIN import_events ie ON ie.organization_id = o.id
GROUP BY o.id, o.shortname
```

**Data freshness:**
```sql
SELECT
  o.shortname AS org_shortname,
  MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END) AS last_products_update,
  MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END) AS last_customers_update,
  MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END) AS last_inventories_update,
  EXTRACT(DAY FROM (CURRENT_TIMESTAMP - GREATEST(
    COALESCE(MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END), '1970-01-01'),
    COALESCE(MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END), '1970-01-01'),
    COALESCE(MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END), '1970-01-01')
  )))::integer AS days_since_critical_update
FROM organizations o
LEFT JOIN data_versions dv ON dv.organization_id = o.id
  AND dv.entity_type IN ('products', 'customers', 'inventories')
GROUP BY o.shortname
```

**User counts:**
```sql
SELECT o.shortname AS org_shortname, COUNT(ou.id) AS total_users
FROM organizations o
LEFT JOIN org_users ou ON ou.organization_id = o.id
GROUP BY o.shortname
```

**Smart stacks:**
```sql
SELECT o.shortname AS org_shortname, COUNT(ss.id) AS smart_stack_count
FROM organizations o
LEFT JOIN smart_stacks ss ON ss.organization_id = o.id
GROUP BY o.shortname
```

---

## Part 3: Code Changes in the Operators (Kylor's side)

Once the BQ tables exist and the Postgres sync is running, the operator code changes are minimal. All scoring logic stays unchanged. Only the read/write endpoints change.

### What changes in `Health V2/operator.py`

**MAL load:** Replace `pd.read_csv(path)` with:
```python
query = "SELECT org_shortname, parent_entity, bundle FROM `supercat-data-pipeline.insightful_product.master_account_list`"
df = bq.query(query).to_dataframe()
```

**Postgres queries:** Replace each `_pg_query(pg, sql)` call with a BQ equivalent pointed at `ecat.*` tables. Since these are the same SQL queries, it's mostly a table prefix change (`organizations` → `ecat.organizations`, etc.) and converting Postgres-specific syntax (`FILTER (WHERE ...)`, `BOOL_OR`) to BigQuery equivalents (`COUNTIF`, `LOGICAL_OR`).

**Output write:** Replace `output_df.to_csv(output_file, index=False)` with:
```python
bq.load_table_from_dataframe(
    output_df.assign(run_date=date.today()),
    "supercat-data-pipeline.insightful_product.client_health_scores",
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
    )
)
```

Same pattern for both Peer Benchmark operators.

---

## Part 4: Phased Rollout

### Phase 1 — Highest impact, least effort (target: next 2 weeks)
- [ ] Kev: Create `insightful_product.master_account_list` table in BQ
- [ ] Kylor: Upload current canonical MAL CSV to that table
- [ ] Kev: Sync `organizations` + `subscriptions` tables from Postgres → `ecat` dataset in BQ
- [ ] Kylor: Update Health V2 operator to read MAL from BQ and subscription gate from BQ
- [ ] Kev: Create `insightful_product.client_health_scores` table

**Result:** MAL is version-controlled in BQ. Subscription gate is live data. No more `pg_sub.csv` footgun.

### Phase 2 — Full behavioral data in BQ (target: ~1 month)
- [ ] Kev: Sync remaining Postgres tables (`products`, `orders`, `customers`, `org_users`, `smart_stacks`, `import_events`, `data_versions`) → `ecat` dataset
- [ ] Kylor: Update all Postgres cache reads in Health V2 to query `ecat.*` directly
- [ ] Kev: Create `insightful_product.peer_benchmark` table

**Result:** Health V2 and Peer Benchmark run entirely from BQ — no CSV files, no VPN, no manual cache refresh.

### Phase 3 — Scheduled runs (target: ongoing)
- [ ] Set up Cloud Scheduler or Cloud Run job to trigger Health V2 + Peer Benchmark pipeline on a schedule (weekly recommended)
- [ ] Downstream reports (EBR, external report) query `client_health_scores` and `peer_benchmark` directly from BQ with `WHERE run_date = CURRENT_DATE`

---

## Credentials

The service account JSON files are already in the repo:
```
integrations/bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json
```

This service account already has write access to `supercat-data-pipeline.insightful_product` — confirmed working during the 2026-04-06 run.

For the Postgres sync, credentials are managed separately via the VPN connection. Kev has access to those.

---

## Questions / Decisions Needed

| # | Question | Recommended answer |
|---|---|---|
| 1 | What tool for Postgres → BQ sync? | Airbyte if already in the stack; otherwise a custom Cloud Run job is straightforward |
| 2 | New dataset name for Postgres tables? | `ecat` (clean separation from curated `insightful_product` output) |
| 3 | Full table sync or incremental? | Full is fine for Phase 1 given row counts (~200–300 orgs). Incremental later if volume grows. |
| 4 | Run schedule for scoring? | Weekly, Monday morning. Health V2 + Peer Benchmark together take ~60 seconds. |
| 5 | Keep CSV outputs as backup? | Yes for now — keep the `--output-dir` CSV write as a fallback until BQ writes are validated |

---

## Reference: Current Run Stats (2026-04-06 baseline)

| Metric | Value |
|---|---|
| MAL orgs | 104 |
| Scored orgs | 102 |
| Excluded | 2 (1 no active subscription, 1 unresolvable company name) |
| Run time | ~60 seconds (Health V2 + Peer Benchmark Layer 1 + Layer 2) |
| BQ project | `supercat-data-pipeline` |
| BQ dataset | `insightful_product` |
| Postgres tables needed | 9 (listed in Part 2) |
