# Health Intelligence v2 — Scoring Specification

Version: 2.5.1
Effective: 2026-04-14

> **Changelog — v2.5.1 (2026-04-14)**
> - §1.4 MAL column requirements extended: `mrr`, `arr`, `cohort_year` added as required columns (sourced from Pricing Refresh Master Data).
> - §9 Output column contract: `arr_source` updated from `direct / parent / none` to `mal_csv` — ARR is now sourced exclusively from the MAL CSV.
> - C-3 (NULL/zero ARR for 21 orgs) resolved. See KNOWN_CAVEATS.md.
>
> **Changelog — v2.4.0 (2026-04-06)**
> - §1 Eligibility rewritten to reflect validated runtime behavior. Active subscription is now the primary gate. HubSpot lifecycle status and ARR are demoted to warning-only signals. Parent ARR carveout removed as an eligibility condition.
> - §1.2 Warning flags section added (new).
> - §1.3 MAL column requirements updated.
> - §9 Output format updated: `hs_lifecycle_stale`, `hs_join_missing`, `arr_data_gap` eligibility warning columns added to column contract.
> - §11 Known Caveats section added (new).

---

## 1. Client Universe and Eligibility

### Canonical Key

Every scored entity is identified by `org_shortname`. One output row = one `org_shortname`.

### Inclusion Criteria

An entity is scored if ALL of the following are true:

1. Present in the **Master Account List** with a valid `bundle` assignment.
2. Resolvable to a valid `org_shortname` via `org_summary` (company name lookup or `MAL_COMPANY_OVERRIDES`).
3. Has at least one active subscription (`subscriptions.status = 'active'` in Postgres).
4. Not a demo, test, staging, or internal org (see Exclusion Criteria below).

### 1.1 Eligibility Gate: Active Subscription

The primary eligibility gate is a live Postgres query against the `subscriptions` table:

```sql
SELECT org_shortname, BOOL_OR(status = 'active') AS has_active_sub
FROM organizations o
LEFT JOIN subscriptions s ON s.organization_id = o.id
GROUP BY org_shortname
```

An org with no active subscription row is excluded from scoring regardless of HubSpot status or ARR. This is the single authoritative gate for "is this a live paying customer?"

When running with `--pg-cache-dir`, the cache file `pg_sub.csv` is used. If `pg_sub.csv` is absent from the cache, the operator warns and passes all MAL orgs through (subscription gate bypassed).

### 1.2 Warning-Only Signals

The following signals are surfaced as output flags but do **not** exclude any org from scoring:

| Signal | Output Column | Behavior |
|---|---|---|
| HubSpot `engagement_status` = "Lost" or "Churn" | `hs_lifecycle_stale` | Warning flag only. Org is scored. |
| HubSpot join missing (`hubspot_company_id` not present) | `hs_join_missing` | Warning flag only. Org is scored. |
| `arr` is NULL or 0 | `arr_data_gap` | Warning flag only. Org is scored. |

These flags are present in every output row so downstream consumers can apply their own caveats. They are not used as scoring gates.

**Rationale:** HubSpot lifecycle and ARR data can lag operational reality. An org with a "Lost" HubSpot status but an active subscription is a scoring candidate; the stale lifecycle status is the downstream follow-up action, not a reason to omit a score.

### 1.3 Exclusion Criteria

An entity is excluded if ANY of the following are true:

1. `org_shortname` contains "test", "demo", "staging", "sandbox", or "template" (case-insensitive).
2. `org_name` contains "Test Account", "Demo Org", "Sample", "Don't Use", or "For Jimmy" (case-insensitive).
3. `org_shortname` is in the `KNOWN_INTERNAL_ORGS` set defined in `operator.py` (maintained in code; covers legacy internal, demo, staging, and client-specific test environments).
4. Present on the **Explicit Exclusion List** passed via `--exclusion-list` (optional).

### 1.4 Master Account List (MAL)

The canonical MAL is a CSV with these required columns:

| Column | Description |
|---|---|
| `company` | Display name used to resolve `org_shortname` via `org_summary` |
| `parent_entity` | Parent company name for downstream grouping (nullable) |
| `ord_id` | Informational field carried through; not used for identity resolution |
| `stack` | Product bundle (normalized to canonical bundle name via `BUNDLE_NORMALIZATION`) |
| `mrr` | Monthly recurring revenue (contracted). Sourced from Pricing Refresh Master Data. Numeric, no `$` or commas. |
| `arr` | Annual recurring revenue (contracted). Sourced from Pricing Refresh Master Data. Numeric, no `$` or commas. If `mrr` is provided and `arr` is missing, `arr = mrr × 12`. |
| `cohort_year` | Year the org was onboarded (integer). Used for cohort analysis and downstream reporting. |

The operator resolves `company` → `org_shortname` via `org_summary.org_name` lookup. Known name mismatches are handled by `MAL_COMPANY_OVERRIDES` in `operator.py`. If `company` cannot be resolved and no override exists, the row is dropped with a `[WARN]` log entry.

**`arr` is the authoritative source for RM-1 and downstream ARR reporting.** It is loaded directly from the MAL CSV and is not sourced from or overridden by BigQuery `org_summary.arr`. The operator gracefully handles older MAL files that lack these columns by defaulting them to `None`.

**Canonical MAL location (as of 2026-04-14):**
```
Health V2/inputs/master_account_list_2026-04-14_canonical.csv
```

### 1.5 Entity vs. Parent

Scoring grain is the entity (`org_shortname`). `parent_entity` is included in the output for downstream grouping. Parent-level summaries are not part of this model.

---

## 2. Product Bundle Framework

Every scored entity is assigned exactly one bundle from the Master Account List. Bundle determines which Health dimensions apply, which features count toward Adoption, and which Growth components are active.

| Bundle | Products Included |
|---|---|
| **iPad-only** | eCat iPad |
| **iPad+Catalog** | eCat iPad, eCat Online (closed site) |
| **iPad+Catalog+Cart** | eCat iPad, eCat Online, B2B Cart |
| **iPad+Catalog+Portal** | eCat iPad, eCat Online, Sales Portal |
| **Full** | eCat iPad, eCat Online, B2B Cart, Sales Portal |

Entity counts per bundle are derived from the Master Account List at run time. See `operator.py` output for current counts.

### Product Definitions

| Product | Function |
|---|---|
| eCat iPad | Mobile catalog and guided selling for field reps |
| eCat Online (closed site) | Web-based product browsing for dealers/customers, no ordering |
| B2B Cart | Online ordering layer on eCat Online |
| Sales Portal | Sales management dashboards, curated lists, self-service utilities |
| Admin Console | Backend management hub (included in all bundles, not scored separately) |

---

## 3. Global Scoring Rules

### 3.1 Time Windows

- **Current period**: trailing 90 days from score date.
- **Prior period**: days 91–180 from score date.
- All behavioral metrics use the current period unless stated otherwise.
- Trajectory calculations compare current period to prior period.

### 3.2 Scoring Scale

Both Health and Growth scores use a **0–100** integer scale. Component and dimension scores also use 0–100 internally before weighting.

### 3.3 Non-Applicable Components

When a component does not apply to a bundle (e.g., Customer Headroom for iPad-only), that component's weight is redistributed **proportionally** among the remaining applicable components within the same score.

Formula:

```
adjusted_weight_i = base_weight_i / sum(base_weights of all applicable components)
```

### 3.4 Missing Data

Missing data is surfaced, not hidden.

**Blocked**: If all inputs for **3 or more of the 5 Health dimensions** are unavailable, the entity cannot be reliably scored. Output the row with:
- `health_score` = null, `growth_score` = null
- `classification` = "BLOCKED"
- `health_band` = null, `growth_band` = null
- All flags = false
- `scoring_status` = "blocked"
- `missing_data_flags` = list of unavailable metrics
- `score_explanation` = "Scoring blocked: insufficient data for {blocked dimensions}."

**Partial**: If some inputs are missing but the entity is not blocked, score with available data. Do not substitute a midpoint. Log every missing metric in `missing_data_flags` and set `scoring_status` = "partial". The `score_explanation` must note the gap.

**Complete**: All inputs retrieved. `scoring_status` = "complete", `missing_data_flags` = null.

### 3.5 Thresholds

All thresholds in this spec are **absolute values**, not percentile-based, unless explicitly labeled as peer-relative. Scoring is deterministic without portfolio-level context.

### 3.6 Rounding

Final Health and Growth scores are rounded to the nearest integer. Component scores are carried at full precision during calculation and rounded to integer in the output.

---

## 4. Client Health Score

**Range**: 0–100
**Purpose**: Measures current platform health across engagement, adoption, value realization, operational hygiene, and momentum.

### Architecture

| Dimension | Base Weight | Applies To |
|---|---|---|
| Engagement | 25% | All bundles |
| Adoption | 20% | All bundles |
| Value Delivery | 30% | All bundles |
| Operational Health | 15% | All bundles |
| Trajectory | 10% | All bundles |

All five dimensions apply universally. Bundle-specific variation occurs **within** each dimension (different inputs, different thresholds), not at the weight level.

### Formula

```
health_raw = (engagement × 0.25) + (adoption × 0.20) + (value_delivery × 0.30)
           + (operational_health × 0.15) + (trajectory × 0.10)

health_score = min(health_raw, risk_modifier_cap)
```

If no risk modifier fires, `risk_modifier_cap` = 100 (no cap).

### Health Bands

| Band | Range |
|---|---|
| Thriving | 80–100 |
| Healthy | 60–79 |
| Watch | 40–59 |
| At Risk | 20–39 |
| Critical | 0–19 |

---

### 4.1 Engagement (25%)

Measures whether users are logging in and actively using the platform.

**Inputs**:
- `logins_90d` — total login events in current period
- `active_users_90d` — distinct users with any activity in current period
- `total_users` — total user accounts provisioned

**Derived Metrics**:
- `login_intensity` = `logins_90d` / `active_users_90d` (logins per active user)
- `active_user_ratio` = `active_users_90d` / `total_users`

If `active_users_90d` = 0, `login_intensity` = 0.
If `total_users` = 0, `active_user_ratio` = 0.

**Sub-Scores** (each 0–100, averaged):

| login_intensity | login_intensity_score |
|---|---|
| ≥ 50 | 100 |
| ≥ 35 | 80 |
| ≥ 20 | 60 |
| ≥ 10 | 40 |
| > 0 | 20 |
| 0 | 0 |

| active_user_ratio | active_user_ratio_score |
|---|---|
| ≥ 30% | 100 |
| ≥ 20% | 80 |
| ≥ 10% | 60 |
| ≥ 5% | 40 |
| > 0% | 20 |
| 0% | 0 |

**Engagement Score** = (`login_intensity_score` + `active_user_ratio_score`) / 2

---

### 4.2 Adoption (20%)

Measures breadth of feature usage within the entity's bundle. A feature counts as **used** if its event count exceeds the minimum threshold in the current period.

**Feature Catalog**

| # | Feature | Metric | Min Threshold | iPad-only | +Catalog | +Cat+Cart | +Cat+Portal | Full |
|---|---|---|---|---|---|---|---|---|
| 1 | Product Search | mp_search_products | > 50 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | Customer Selection | mp_select_a_customer | > 20 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 | Presentations | mp_item_added_via_magic_button | > 20 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 | Email Sharing | mp_item_email_drafted | > 10 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 | PDF Catalogs | mp_create_pdf_catalog | > 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6 | Document Viewing | mp_view_document | > 50 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 7 | Stacks/Lists | smart_stack_count > 0 | ≥ 1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 8 | eCat Online | has_catalog = true AND portal_visitors > 0 | ≥ 1 visitor | | ✓ | ✓ | ✓ | ✓ |
| 9 | Order Submission | mp_submit_order | > 10 | | | ✓ | | ✓ |
| 10 | Sales Portal | mp_access_sales_portal | > 10 | | | | ✓ | ✓ |

**Features Available by Bundle**

| Bundle | Available Features | Count |
|---|---|---|
| iPad-only | 1–7 | 7 |
| iPad+Catalog | 1–8 | 8 |
| iPad+Catalog+Cart | 1–9 | 9 |
| iPad+Catalog+Portal | 1–8, 10 | 9 |
| Full | 1–10 | 10 |

**Adoption Score** = (`features_used` / `features_available`) × 100

---

### 4.3 Value Delivery (30%)

Measures depth of value realization. Inputs and formulas vary by bundle.

#### Presentation Score (used by iPad-only, iPad+Catalog, iPad+Catalog+Portal)

`presentation_actions` = `mp_item_added_via_magic_button` + `mp_item_email_drafted` + `mp_create_pdf_catalog` + `mp_document_email_drafted`

| presentation_actions (90d) | presentation_score |
|---|---|
| ≥ 1000 | 100 |
| ≥ 500 | 80 |
| ≥ 100 | 60 |
| ≥ 50 | 40 |
| > 0 | 20 |
| 0 | 0 |

#### Order Volume Score (used by iPad+Catalog+Cart, Full)

| orders_90d | order_volume_score |
|---|---|
| ≥ 500 | 100 |
| ≥ 200 | 80 |
| ≥ 50 | 60 |
| ≥ 20 | 40 |
| > 0 | 20 |
| 0 | 0 |

#### Customer Activation Score (used by iPad+Catalog+Cart, Full)

`customer_activation_rate` = customers with orders in current period / total active customers

| customer_activation_rate | customer_activation_score |
|---|---|
| ≥ 30% | 100 |
| ≥ 20% | 80 |
| ≥ 10% | 60 |
| ≥ 5% | 40 |
| > 0% | 20 |
| 0% | 0 |

#### eCat Online Share Score (used by iPad+Catalog+Cart, Full)

`eol_share` = eCat Online orders in current period / total orders in current period

| eol_share | eol_share_score |
|---|---|
| ≥ 40% | 100 |
| ≥ 25% | 80 |
| ≥ 15% | 60 |
| ≥ 5% | 40 |
| > 0% | 20 |
| 0% | 0 |

#### Portal Engagement Score (used by iPad+Catalog+Portal, Full)

| mp_access_sales_portal (90d) | portal_engagement_score |
|---|---|
| ≥ 300 | 100 |
| ≥ 150 | 80 |
| ≥ 50 | 60 |
| ≥ 20 | 40 |
| > 0 | 20 |
| 0 | 0 |

#### Value Delivery Formula by Bundle

| Bundle | Formula |
|---|---|
| **iPad-only** | `presentation_score` |
| **iPad+Catalog** | `presentation_score` |
| **iPad+Catalog+Cart** | (`order_volume_score` + `customer_activation_score` + `eol_share_score`) / 3 |
| **iPad+Catalog+Portal** | (`presentation_score` + `portal_engagement_score`) / 2 |
| **Full** | (`order_volume_score` + `customer_activation_score` + `eol_share_score` + `portal_engagement_score`) / 4 |

---

### 4.4 Operational Health (15%)

Measures data quality and platform maintenance. Import success matters more than update frequency — many clients legitimately update infrequently.

**Inputs**:
- `import_success_rate` — successful imports / total import attempts in current period
- `last_import_had_errors` — boolean, whether the most recent import completed with warnings or errors
- `catalog_completeness` — % of active products with at least one image AND a price > $0
- `days_since_critical_update` — max days since most recent update to products, customers, or inventory

**Sub-Score Weights**:

| Sub-Score | Weight |
|---|---|
| Import Health | 50% |
| Catalog Completeness | 30% |
| Data Freshness | 20% |

#### Import Health (50%)

| Condition | import_health_score |
|---|---|
| `import_success_rate` ≥ 95% AND last import clean | 100 |
| `import_success_rate` ≥ 95% AND last import had errors | 80 |
| `import_success_rate` ≥ 80% | 60 |
| `import_success_rate` ≥ 60% | 40 |
| `import_success_rate` < 60% | 20 |

**No import history**: Some entities manage data through Admin Console and never use the importer. If zero imports exist for the entity, Import Health is non-applicable. Redistribute its weight:

```
operational_health = (catalog_completeness_score × 0.60) + (data_freshness_score × 0.40)
```

#### Catalog Completeness (30%)

| catalog_completeness | catalog_completeness_score |
|---|---|
| ≥ 95% | 100 |
| ≥ 85% | 80 |
| ≥ 75% | 60 |
| ≥ 60% | 40 |
| ≥ 40% | 20 |
| < 40% | 0 |

#### Data Freshness (20%)

| days_since_critical_update | data_freshness_score |
|---|---|
| ≤ 7 | 100 |
| ≤ 30 | 80 |
| ≤ 60 | 60 |
| ≤ 90 | 40 |
| ≤ 180 | 20 |
| > 180 | 0 |

**Operational Health Score** = (`import_health_score` × 0.50) + (`catalog_completeness_score` × 0.30) + (`data_freshness_score` × 0.20)

---

### 4.5 Trajectory (10%)

Measures momentum by comparing current period to prior period.

**Inputs**:
- `primary_value_change_pct` — % change in the bundle's primary value metric (current 90d vs. prior 90d)
- `login_change_pct` — % change in total logins (current 90d vs. prior 90d)

**Primary Value Metric by Bundle**

| Bundle | Primary Value Metric |
|---|---|
| iPad-only | presentation_actions |
| iPad+Catalog | presentation_actions |
| iPad+Catalog+Cart | orders_90d |
| iPad+Catalog+Portal | (presentation_actions + mp_access_sales_portal) / 2 |
| Full | orders_90d |

If prior period value = 0 and current > 0, change = +100%.
If both periods = 0, change = 0%.

**Sub-Scores** (each 0–100, averaged):

| primary_value_change_pct | value_trend_score |
|---|---|
| ≥ +20% | 100 |
| ≥ +10% | 80 |
| ≥ −5% | 60 |
| ≥ −15% | 40 |
| ≥ −30% | 20 |
| < −30% | 0 |

| login_change_pct | login_trend_score |
|---|---|
| ≥ +15% | 100 |
| ≥ +5% | 80 |
| ≥ −5% | 60 |
| ≥ −15% | 40 |
| ≥ −30% | 20 |
| < −30% | 0 |

**Trajectory Score** = (`value_trend_score` + `login_trend_score`) / 2

---

## 5. Health Risk Modifiers

Risk modifiers override the calculated health score by applying a cap. If multiple modifiers fire, the **lowest cap** applies.

| # | Condition | Cap | Severity |
|---|---|---|---|
| RM-1 | ARR > $5,000 AND `logins_90d` = 0 | 20 | immediate |
| RM-2 | `primary_value_change_pct` < −60% AND `value_delivery_score` < 20 | 20 | immediate |
| RM-3 | 5+ support escalations (L3+) in current period | 30 | near-term |
| RM-4 | `days_since_critical_update` > 180 for 2+ entity types | 30 | near-term |

When a modifier fires:
- `health_score` = min(`health_raw`, cap)
- `risk_modifier_applied` = modifier ID (e.g., "RM-1")
- `churn_risk` = true
- `churn_risk_severity` = modifier severity

---

## 6. Growth Potential Score

**Range**: 0–100
**Purpose**: Measures commercial expansion opportunity independent of current health.

### Architecture

| Component | Base Weight | Applies To |
|---|---|---|
| Bundle Upgrade Signal | 30% | All bundles except Full |
| Feature Gap | 25% | All bundles |
| Customer Headroom | 25% | Ordering bundles only (iPad+Cat+Cart, Full) |
| Peer Benchmark Gap | 20% | All bundles |

When a component is non-applicable, its weight redistributes per §3.3.

### Formula

```
growth_score = sum(component_score_i × adjusted_weight_i) for all applicable components
```

### Growth Bands

| Band | Range |
|---|---|
| Prime | 80–100 |
| Ready | 60–79 |
| Developing | 40–59 |
| Not Ready | 0–39 |

---

### 6.1 Bundle Upgrade Signal (30%)

Identifies behavioral evidence that the entity has outgrown its current bundle.

**Full bundle**: component is N/A (score = 0, weight redistributed).

#### Upgrade Signals by Bundle

**iPad-only**

| Signal | Condition |
|---|---|
| External ordering | Orders exist in Postgres AND `mp_submit_order` = 0 |
| iPad ordering | `mp_submit_order` > 0 |
| High presentation volume | `presentation_actions` > 500 |
| Team scale | `active_users_90d` ≥ 10 |

**iPad+Catalog**

| Signal | Condition |
|---|---|
| External ordering | Orders exist in Postgres |
| High online traffic | eCat Online daily visitors ≥ 30 |
| Team scale | `active_users_90d` ≥ 10 |

**iPad+Catalog+Cart**

| Signal | Condition |
|---|---|
| Team scale | `active_users_90d` ≥ 10 |
| Deep adoption | `adoption_score` ≥ 70 AND `active_users_90d` ≥ 8 |

**iPad+Catalog+Portal**

| Signal | Condition |
|---|---|
| External ordering | Orders exist in Postgres AND `mp_submit_order` = 0 |
| High order-intent | `mp_select_a_customer` > 100 AND `presentation_actions` > 300 |
| Deep portal engagement | `mp_access_sales_portal` ≥ 150 AND `adoption_score` ≥ 80 |

#### Signal Count → Score

| Qualifying Signals | bundle_upgrade_signal |
|---|---|
| ≥ 3 | 100 |
| 2 | 75 |
| 1 | 50 |
| 0 | 0 |
| Full bundle (N/A) | 0 (weight redistributed) |

---

### 6.2 Feature Gap (25%)

Identifies add-on products or capabilities the entity does not currently have but whose behavior suggests they would benefit from.

#### Add-On Signals

| Add-On | Signal Condition | Applicable Bundles |
|---|---|---|
| CPQ | `mp_order_configured_item` > 50 AND `has_cpq` = false | Cart, Full |
| Library | `mp_create_pdf_catalog` > 100 | All bundles |

#### Signal Count → Score

| Qualifying Signals | feature_gap_score |
|---|---|
| 2 | 75 |
| 1 | 50 |
| 0 | 0 |

Under the current design, CPQ and Library are the only active signals. The practical maximum is 75 (2 signals). A third signal slot exists in the scoring ladder if a future product-truth-aligned signal is added.

---

### 6.3 Customer Headroom (25%)

Measures untapped revenue opportunity within the existing customer base.

**Applies to**: iPad+Catalog+Cart, Full.
**All other bundles**: N/A (weight redistributed per §3.3).

**Inputs**:
- `dormant_customers` — customers who placed orders before the current period but none within it
- `customer_activation_rate` — ordering customers / total active customers (same as §4.3)
- `geographic_cv` — coefficient of variation of order count across states/regions

**Sub-Scores** (each 0–100, averaged):

| dormant_customers | dormant_opportunity_score |
|---|---|
| ≥ 100 | 100 |
| ≥ 50 | 80 |
| ≥ 20 | 60 |
| ≥ 5 | 40 |
| > 0 | 20 |
| 0 | 0 |

| 1 − customer_activation_rate | activation_headroom_score |
|---|---|
| ≥ 80% unactivated | 100 |
| ≥ 60% | 80 |
| ≥ 40% | 60 |
| ≥ 20% | 40 |
| < 20% | 20 |

| geographic_cv | geographic_gap_score |
|---|---|
| ≥ 1.0 | 100 |
| ≥ 0.7 | 80 |
| ≥ 0.5 | 60 |
| ≥ 0.3 | 40 |
| < 0.3 | 20 |

**Customer Headroom Score** = (`dormant_opportunity_score` + `activation_headroom_score` + `geographic_gap_score`) / 3

---

### 6.4 Peer Benchmark Gap (20%)

Compares the entity's key metrics against its peer cohort. Larger gaps below peer cohort = larger growth opportunity.

**Source (as of v2.4.0):** The standalone Peer Benchmark system (Layer 2) computes peer benchmark gaps using actual vertical × stack cohorts (`peer_group_id_effective`) rather than bundle-only medians. The operator reads `hv2_pbg_composite_gap` from the Peer Benchmark Layer 2 output CSV and uses it directly. Pass the file via `--peer-benchmark`.

**Three dimensions benchmarked** (identical to the prior internal method, now against real peer cohorts):
1. `login_intensity` — logins / active users vs. cohort
2. Primary value metric (per §4.5 table) vs. cohort — bundle-routed: `presentation_actions` (iPad-only, iPad+Catalog), `orders_90d` (Cart, Full), `presentation_portal_avg` (Portal)
3. `adoption_score` vs. cohort

**Per-Metric Gap Score** (unchanged):

| Entity Position vs. Peer Cohort | gap_score |
|---|---|
| Below p25 | 100 |
| p25–p50 | 75 |
| p50–p75 | 40 |
| Above p75 | 10 |

**Peer Benchmark Gap Score** = average of the three per-metric gap scores.

**Peer cohort definition:** Tier 1 = vertical × stack bundle (minimum n=5). Falls back to vertical-only (Tier 2), bundle-only (Tier 3), or no cohort (Tier 4) per the Peer Benchmark Layer 1 fallback hierarchy. See Peer Benchmark `README.md` §3.

**Fallback behavior:** If `--peer-benchmark` is not provided, or if no value exists for an org in the file, the operator falls back to the internal bundle-median method (§6.4 original). For non-eligible orgs (onboarding, Tier 4), `peer_benchmark_gap` = 50, flagged as `peer_benchmark_gap_small_sample`.

**Non-circularity note:** `hv2_pbg_composite_gap` is derived from `login_intensity`, `primary_value_metric`, and `adoption_score` — three underlying behavioral dimensions. It does NOT use `health_score` as an input, which would create circular dependency between Health and Growth.

---

## 7. Final Classification

Classification is a function of both scores mapped to a quadrant.

|  | Health ≥ 60 | Health < 60 |
|---|---|---|
| **Growth ≥ 60** | **Expand** | **Stabilize First** |
| **Growth < 60** | **Maintain** | **Intervene** |

| Classification | Definition |
|---|---|
| **Expand** | Healthy and showing strong commercial opportunity. Prioritize upsell/cross-sell. |
| **Stabilize First** | Growth signals exist but health must improve first. Fix before selling. |
| **Maintain** | Healthy with limited near-term growth. Protect with standard cadence. |
| **Intervene** | Unhealthy with no growth offset. Requires immediate save/recovery plan. |

---

## 8. Operational Flags

Three mutually exclusive flags. An entity receives **at most one**.

### 8.1 churn_risk

**Trigger**: ANY of the following:
- Any Health Risk Modifier fired (§5)
- `health_score` < 20

**Output fields**:
- `churn_risk` = true
- `churn_risk_severity` = `immediate` | `near-term` | `monitored`

Severity assignment:
- If RM-1 or RM-2 fired → `immediate`
- If RM-3 or RM-4 fired → `near-term`
- If triggered by `health_score` < 20 alone (no modifier) → `monitored`

### 8.2 expansion_ready

**Trigger**: ALL of the following:
- `health_score` ≥ 60
- `growth_score` ≥ 60
- `churn_risk` = false

**Output fields**:
- `expansion_ready` = true
- `expansion_type` = highest-scoring Growth component from: `bundle_upgrade` | `feature_gap` | `customer_headroom`

### 8.3 healthy_complete

**Trigger**: ALL of the following:
- `health_score` ≥ 70
- `growth_score` < 40
- `churn_risk` = false
- `expansion_ready` = false

**Output fields**:
- `healthy_complete` = true

### Flag Precedence

Evaluate in order: churn_risk → expansion_ready → healthy_complete. First match wins. If none match, all three flags = false.

---

## 9. Output Format

The operator produces a single CSV file: `client_health_scores_YYYY-MM-DD.csv`.

### Column Contract

| Column | Type | Description |
|---|---|---|
| `org_shortname` | string | Canonical entity key |
| `org_name` | string | Display name |
| `parent_entity` | string | Parent entity for grouping (null if standalone) |
| `bundle` | string | One of the 5 bundle values |
| `arr` | decimal | Annual recurring revenue |
| `health_score` | integer | 0–100, after risk modifier caps |
| `health_band` | string | Thriving / Healthy / Watch / At Risk / Critical |
| `growth_score` | integer | 0–100 |
| `growth_band` | string | Prime / Ready / Developing / Not Ready |
| `classification` | string | Expand / Stabilize First / Maintain / Intervene |
| `churn_risk` | boolean | |
| `churn_risk_severity` | string | immediate / near-term / monitored / null |
| `expansion_ready` | boolean | |
| `expansion_type` | string | bundle_upgrade / feature_gap / customer_headroom / null |
| `healthy_complete` | boolean | |
| `engagement_score` | integer | 0–100 |
| `adoption_score` | integer | 0–100 |
| `value_delivery_score` | integer | 0–100 |
| `operational_health_score` | integer | 0–100 |
| `trajectory_score` | integer | 0–100 |
| `bundle_upgrade_signal` | integer | 0–100 (0 if N/A) |
| `feature_gap_score` | integer | 0–100 |
| `customer_headroom_score` | integer | 0–100 (0 if N/A) |
| `peer_benchmark_gap` | integer | 0–100 |
| `risk_modifier_applied` | string | Modifier ID (e.g., "RM-1") or null |
| `scoring_status` | string | complete / partial / blocked |
| `missing_data_flags` | string | Comma-separated list of unavailable metrics, or null |
| `score_explanation` | string | 1–2 sentence plain-English summary |
| `arr_source` | string | `mal_csv` — ARR is sourced from the MAL CSV (Pricing Refresh Master Data) for all orgs |
| `hs_lifecycle_stale` | boolean | **Warning flag only.** True if HubSpot `engagement_status` = "Lost"/"Churn", or no HubSpot record exists. Does not affect scoring. |
| `hs_join_missing` | boolean | **Warning flag only.** True if no HubSpot join exists for this org. Does not affect scoring. |
| `arr_data_gap` | boolean | **Warning flag only.** True if ARR is NULL or 0. Does not affect scoring. |

### Score Explanation Format

The `score_explanation` column follows this template:

```
{org_name} ({bundle}) scores {health_score} Health / {growth_score} Growth → {classification}.
{Primary driver sentence based on highest and lowest dimension scores.}
```

When `classification` = "Stabilize First", the explanation must reference both the health deficit and the growth opportunity.

Examples:
> Acme Corp (iPad+Catalog+Cart) scores 72 Health / 81 Growth → Expand. Strong order volume and customer activation drive health; high dormant customer count signals significant headroom for growth.

> Beta Inc (iPad+Catalog+Portal) scores 38 Health / 67 Growth → Stabilize First. Engagement and adoption have declined sharply; however, strong bundle upgrade signals indicate expansion opportunity once health recovers.

---

## 10. File Governance

| File | Purpose | Authority |
|---|---|---|
| `README.md` | Scoring specification (this file) | Defines all rules, formulas, thresholds |
| `QUERIES.md` | Data retrieval | All SQL, MCP calls, and API queries needed to populate inputs |
| `operator.py` | Execution | Reads README rules, runs QUERIES, produces output CSV |

README is the authoritative source. QUERIES implements the data retrieval README requires. The operator implements the logic README defines. If QUERIES or the operator conflict with README, README wins.

---

## 11. Open Decisions

Items calibrated or deferred:

| # | Decision | Impact |
|---|---|---|
| OD-1 | Calibrate all absolute thresholds (§4, §6) against actual portfolio distribution after first full run | Threshold bands may shift |
| OD-2 | Org-size normalization for `active_user_ratio` — large orgs with ERP-loaded user bases skew the denominator | Engagement accuracy |
| OD-3 | ~~Peer Benchmark Gap reliability for small bundles~~ — **Resolved in v2.4.0.** Peer benchmark now uses cohort-based vertical × stack peer groups from the standalone Peer Benchmark system. Small-bundle fallback hierarchy is handled by Peer Benchmark Layer 1. | Resolved |
| OD-4 | CPQ as an adoption feature vs. growth-only signal — currently growth-only (§6.2) | Adoption score for CPQ subscribers |
| OD-5 | eCat Online engagement signal adequacy — `has_clicky_portal` and `portal_visitors_daily` are the confirmed available signals; whether this level of measurement is sufficient for Catalog bundles is an open product decision | Adoption and Value Delivery for Catalog bundles |
| OD-6 | Help Scout org attribution fidelity — email-domain matching is operational and covers ~95% of eligible entities, but is inherently approximate; escalation tag vocabulary should be reviewed periodically against actual production tags | Risk modifier coverage |
| OD-7 | Geographic CV calculation — confirm state/region field availability in order data | Customer Headroom accuracy |
| OD-8 | Trajectory scoring when prior period has zero activity — current rule (+100% if current > 0) may over-reward reactivation | Trajectory accuracy |
| OD-9 | iPad+Catalog Value Delivery online uplift — evaluate after first run whether eCat Online traffic for iPad+Catalog entities warrants an additive bonus on `presentation_score` | Value Delivery accuracy for iPad+Catalog |
| OD-10 | Import success/failure data availability — confirm import logs with success/error status are queryable in Postgres before implementation; if not, fall back to binary (imports exist in period = 100, no imports = 0) | Operational Health accuracy |

---

## 12. Known Caveats and Data Hygiene Backlog

These are non-blocking issues carried forward from the 2026-04-06 validated run. They affect data quality or downstream interpretation but do not break scoring.

### C-1: HubSpot join key gaps (15 orgs)

15 orgs have no `hubspot_company_id` in `org_summary`, meaning HubSpot lifecycle and vertical data cannot be joined for them. They are scored normally (subscription gate passes) but carry `hs_join_missing = true` and fall to bundle-only (Tier 3) in the Peer Benchmark.

**Root cause:** `org_summary.hubspot_company_id` is not populated for these orgs in the pipeline.
**Fix:** Populate `hubspot_company_id` in the pipeline for these orgs. Not urgent — scoring is unaffected.

### C-2: Stale HubSpot lifecycle for active customers (31 orgs as of 2026-04-06)

31 orgs have `hs_lifecycle_stale = true`, meaning HubSpot shows "Lost", "Churn", or no status — but all have active subscriptions and are scored. HubSpot lifecycle data lags operational reality for a significant portion of the portfolio.

**Downstream implication:** Do not use `hs_lifecycle_stale` alone to infer churn risk. Use `churn_risk` and `health_score` instead.

### C-3: NULL/zero ARR (21 orgs as of 2026-04-06)

21 orgs have `arr_data_gap = true`. ARR is used only for the RM-1 risk modifier (ARR > $5,000 AND zero logins). Missing ARR means RM-1 cannot fire for these orgs even if they have zero logins.

**Downstream implication:** RM-1 may be underreported for these 21 orgs.

### C-4: `operator.py` naming conflict — resolved (2026-04-07)

The script was renamed from `operator.py` to `health_operator.py` (and the Peer Benchmark script from `operator.py` to `peer_benchmark_operator.py`). The old files have been deleted. Both operators now run cleanly from their own directories with no workaround required.

**Invoke as:** `python health_operator.py --mal ...` from the `Health V2/` directory.

### C-5: `pg_sub.csv` not in the static cache

The subscription gate cache file (`pg_sub.csv`) is not committed to `Health V2/cache/`. It lives only in individual run `pg_cache/` subdirectories. If the static cache is used for a new run without copying `pg_sub.csv`, the subscription gate silently passes all MAL orgs.

**Fix:** Either add `pg_sub.csv` to the static cache or add a hard warning in the operator when `pg_sub.csv` is absent from `--pg-cache-dir`.
