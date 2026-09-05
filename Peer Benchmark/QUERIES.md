# Peer Benchmark — Query Definitions

Version: 1.0.0
Implements: README v1.0.0

> QUERIES.md and README.md version independently. QUERIES.md version increments when query logic, schema notes, or execution behavior changes. README.md version increments when the cohort assignment spec, output contract, or framework rules change. The "Implements" field above identifies which README version this file was validated against.

---

## 1. Data Sources

| ID | Source | Type | Tables |
|---|---|---|---|
| BQ | BigQuery | Cloud | `insightful_product.org_summary`, `hubspot.company` |
| PG-CACHE | Postgres cache CSVs | Local files | `pg_cat.csv`, `pg_cust.csv` |
| HV2 | Health V2 output CSV | Local file | `client_health_scores_*.csv` |

---

## 2. Input-to-Query Mapping

| README Input | Query ID | Output Column | Source | Criticality |
|---|---|---|---|---|
| `org_shortname`, `org_name`, `bundle`, `arr`, `parent_entity` | Q-HV2 | from Health V2 CSV | HV2 | Blocking |
| `vertical` | Q-VERT | `vertical` | BQ `hubspot.company` | Blocking (degrades to unresolved) |
| `lifecycle_stage` | Q-VERT | `lifecycle_stage` | BQ `org_summary` + `hubspot.company` | Degrading |
| `stack_mismatch_flag` | Q-PROV | `stack_mismatch_flag` | BQ `org_summary` | Degrading |
| `total_active_products` | Q-CAT | `catalog_scale` | PG-CACHE `pg_cat.csv` | Degrading |
| `total_customers` | Q-CUST | `customer_scale` | PG-CACHE `pg_cust.csv` | Degrading |
| `created_at` (tenure) | Q-VERT | `tenure_band` | BQ `org_summary` | Degrading |

---

## 3. Execution Order

```
Step 1: Q-HV2    → Load Health V2 output. Produces entity roster with bundle, arr, parent_entity.
Step 2: Q-VERT   → Pull vertical + lifecycle signals for all orgs from BigQuery.
                   Join to org_summary for created_at (tenure) and provisioning flags.
Step 3: Q-PROV   → Stack mismatch check (uses org_summary fields pulled in Q-VERT).
                   No separate query needed — derived from Q-VERT join output.
Step 4: Q-CAT    → Load pg_cat.csv from cache for catalog_scale bucketing.
Step 5: Q-CUST   → Load pg_cust.csv from cache for customer_scale bucketing.
Step 6: ASSIGN   → Apply cohort assignment logic (README §3).
Step 7: OUTPUT   → Write CSV.
```

### Postgres Cache Mode

This operator uses Postgres cache CSVs from the Health V2 `cache/` directory. Pass `--pg-cache-dir` pointing to that directory. No live Postgres connection is required or attempted.

If cache files are absent, the affected fields (`catalog_scale`, `customer_scale`) default to `unknown` and a warning is logged. These fields are descriptive only and do not block cohort assignment.

---

## 4. Query Definitions

### Q-HV2: Health V2 Output

**Source:** Local CSV — `--health-output` argument

The operator reads the Health V2 scored output CSV directly. Fields used:

| Column | Used For |
|---|---|
| `org_shortname` | Entity key |
| `org_name` | Display name |
| `bundle` | Axis 2 — stack assignment |
| `arr` | Axis 4 — ARR band bucketing |
| `parent_entity` | Rollup flag detection |
| `scoring_status` | Informational — passed through |

No transformation applied. Health V2 eligibility is trusted as-is.

---

### Q-VERT: Vertical + Lifecycle Signals (BigQuery)

**Source:** BigQuery — `hubspot.company` JOIN `insightful_product.org_summary`

```sql
SELECT
  os.org_shortname,
  hc.properties_segment                    AS vertical_raw,
  hc.properties_lifecyclestage             AS hs_lifecyclestage,
  hc.properties_createdate                 AS org_created_at,
  os.feature_depth,
  os.billing_status,
  os.is_active
FROM `supercat-data-pipeline.insightful_product.org_summary` os
LEFT JOIN `supercat-data-pipeline.hubspot.company` hc
  ON os.hubspot_company_id = hc.company_id
WHERE os.org_shortname IS NOT NULL
```

**Schema notes:**
- `org_summary` does NOT have a `created_at` column or provisioning flags (`has_catalog`, `has_cart`, `has_portal`).
- Tenure source: `hc.properties_createdate` — HubSpot company creation date, best available proxy for go-live date without a live Postgres connection.
- Stack mismatch detection: `has_catalog`, `has_cart`, `has_portal` are not available from BigQuery. All orgs default to `stack_mismatch_flag = null` / `stack_assignment_confidence = medium`. A future enhancement can pull these from Postgres cache.

**Vertical attribution:**
- If `properties_segment` is populated: `vertical = properties_segment`, `vertical_source = hubspot_live`
- If NULL or blank: `vertical = NULL`, `vertical_source = unresolved`

No hardcoded segment fallback. Unresolved verticals are flagged explicitly and reported in the run summary.

**Lifecycle attribution:**

| Rule | Stage |
|---|---|
| `org_created_at` < 90 days ago OR `hs_lifecyclestage = 'evangelist'` | `onboarding` |
| tenure < 1 year (and not onboarding) | `ramping` |
| tenure >= 1 year | `steady_state` |
| `org_created_at` is NULL | `steady_state` (conservative default — assume mature) |

Tenure = `CURRENT_DATE - DATE(org_created_at)` in days.

**Stack mismatch detection (Q-PROV — derived from Q-VERT output):**

Provisioning signals (`has_catalog`, `has_cart`, `has_portal`) are not available in `org_summary`. When these become available via Postgres cache, the operator will compare MAL `bundle` against them:

| Condition | Flag |
|---|---|
| `has_portal = true` AND bundle in (`iPad-only`, `iPad+Catalog`) | mismatch |
| `has_cart = false` AND bundle in (`iPad+Catalog+Cart`, `Full`) | mismatch |
| `has_catalog = false` AND bundle != `iPad-only` | mismatch |
| signals unavailable (current v1 behavior) | confidence = medium, flag = null |

---

### Q-CAT: Catalog Scale (Postgres Cache)

**Source:** `pg_cat.csv` from Health V2 cache directory

```
Columns used: org_shortname, total_active_products
```

Bucketing applied by operator:

| total_active_products | catalog_scale |
|---|---|
| < 500 | `<500` |
| 500–4,999 | `500-5K` |
| 5,000–24,999 | `5K-25K` |
| ≥ 25,000 | `25K+` |
| Missing | `unknown` |

---

### Q-CUST: Customer Scale (Postgres Cache)

**Source:** `pg_cust.csv` from Health V2 cache directory

```
Columns used: org_shortname, total_customers
```

Bucketing applied by operator:

| total_customers | customer_scale |
|---|---|
| < 100 | `<100` |
| 100–499 | `100-500` |
| 500–1,999 | `500-2K` |
| ≥ 2,000 | `2K+` |
| Missing | `unknown` |

---

### Q-MP-PBG: Mixpanel Peer Benchmark Gap Dimensions (BigQuery)

**Source:** BigQuery — `mixpanel.events` + `insightful_product.org_summary`
**Used by:** `benchmark_operator.py` (Layer 2) — Health V2 `peer_benchmark_gap` replacement
**Output file:** `bq_mp_pbg.csv` in Postgres cache directory

This query produces the three underlying dimensions of Health V2's `peer_benchmark_gap` component:

| Dimension | Metric | HV2 Usage |
|---|---|---|
| 1 | `login_intensity` = `mp_total_logins / mp_active_users` | Dim 1 of 3 |
| 2 | `primary_value_metric` (bundle-routed — see below) | Dim 2 of 3 |
| 3 | `adoption_score` (from HV2 output — no new query needed) | Dim 3 of 3 |

**Primary value metric by bundle:**

| Bundle | Metric | Source |
|---|---|---|
| `iPad-only`, `iPad+Catalog` | `presentation_actions` | Mixpanel events sum |
| `iPad+Catalog+Cart`, `Full` | `orders_90d` | `pg_ord.csv` |
| `iPad+Catalog+Portal` | `presentation_portal_avg` | Mixpanel events + portal |

**Note:** `access_sales_portal` is sourced from `view_portal` event in Mixpanel (not `access_sales_portal` event name, which has no events). Confirmed via live discovery query.

```sql
WITH events AS (
  SELECT
    COALESCE(organization_shortname, current_organization_shortname) AS org_shortname,
    event_name
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
    AND COALESCE(organization_shortname, current_organization_shortname) IS NOT NULL
),
mp_agg AS (
  SELECT
    org_shortname,
    COUNTIF(event_name = 'item_added_via_magic_button')  AS mp_item_added_via_magic_button,
    COUNTIF(event_name = 'item_email_drafted')           AS mp_item_email_drafted,
    COUNTIF(event_name = 'create_pdf_catalog')           AS mp_create_pdf_catalog,
    COUNTIF(event_name = 'document_email_drafted')       AS mp_document_email_drafted,
    COUNTIF(event_name = 'view_portal')                  AS mp_access_sales_portal
  FROM events
  GROUP BY org_shortname
),
org_usage AS (
  SELECT org_shortname, mp_total_logins, mp_active_users
  FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY org_shortname ORDER BY last_updated DESC) AS rn
    FROM `supercat-data-pipeline.insightful_product.org_summary`
    WHERE org_shortname IS NOT NULL
  ) WHERE rn = 1
)
SELECT
  o.org_shortname,
  o.mp_total_logins,
  o.mp_active_users,
  SAFE_DIVIDE(o.mp_total_logins, NULLIF(o.mp_active_users, 0))     AS login_intensity,
  COALESCE(m.mp_item_added_via_magic_button, 0)                    AS mp_item_added_via_magic_button,
  COALESCE(m.mp_item_email_drafted, 0)                             AS mp_item_email_drafted,
  COALESCE(m.mp_create_pdf_catalog, 0)                             AS mp_create_pdf_catalog,
  COALESCE(m.mp_document_email_drafted, 0)                         AS mp_document_email_drafted,
  COALESCE(m.mp_access_sales_portal, 0)                            AS mp_access_sales_portal,
  (COALESCE(m.mp_item_added_via_magic_button, 0)
   + COALESCE(m.mp_item_email_drafted, 0)
   + COALESCE(m.mp_create_pdf_catalog, 0)
   + COALESCE(m.mp_document_email_drafted, 0))                     AS presentation_actions,
  (COALESCE(m.mp_item_added_via_magic_button, 0)
   + COALESCE(m.mp_item_email_drafted, 0)
   + COALESCE(m.mp_create_pdf_catalog, 0)
   + COALESCE(m.mp_document_email_drafted, 0)
   + COALESCE(m.mp_access_sales_portal, 0)) / 2.0                  AS presentation_portal_avg
FROM org_usage o
LEFT JOIN mp_agg m USING (org_shortname)
WHERE o.org_shortname IS NOT NULL
```

Save output as `bq_mp_pbg.csv` in the Postgres cache directory. Regenerate each scoring cycle alongside other cache files.

---

## 5. Data Quality Notes

### DQ-1: Vertical Coverage

`properties_segment` has ~96% coverage in HubSpot. The operator reports exact unresolved count at run time. Orgs with `vertical = NULL` are assigned to Tier 2 fallback (bundle-only) or Tier 4 if bundle cohort is also small.

### DQ-2: org_created_at Availability

`org_summary.created_at` may be NULL for legacy orgs migrated before the field was populated. These are treated as `steady_state` (conservative default). Count of NULL tenure orgs is reported in run summary.

### DQ-3: Provisioning Signal Availability

`has_catalog`, `has_cart`, `has_portal` are fields in `org_summary`. If these columns are absent or NULL for a given org, `stack_mismatch_flag = NULL` and `stack_assignment_confidence = medium`. The bundle assignment from the MAL still stands.

### DQ-4: HubSpot lifecyclestage Coverage

`properties_lifecyclestage` may be sparse. The operator treats NULL `lifecyclestage` as no override — lifecycle is determined by tenure alone in that case.
