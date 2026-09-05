# Peer Benchmark — Cohort Assignment Specification

Version: 1.1.0
Effective: 2026-04-06

> **Changelog — v1.1.0 (2026-04-06)**
> - Layer 2 (`benchmark_operator.py`) is now operational, not deferred.
> - Purpose section updated to reflect both layers.
> - §3 Cohort Assignment Logic: clarified `peer_group_n` semantics (steady-state peers only, excludes self and ramping/onboarding orgs).
> - §5 Output Contract: `peer_group_n` definition tightened.
> - §6 and §8 updated with downstream consumption guidance and confidence interpretation rules.
> - §7 Open Decisions: OD-3 and OD-4 marked resolved.
> - §9 Known Caveats section added (new).

---

## Purpose

This system assigns every eligible org to a peer cohort and computes benchmark comparisons. It answers two questions:

> **Layer 1:** "Who should this org be compared against?"
> **Layer 2:** "How does this org compare to those peers on key metrics?"

This is a two-layer peer benchmarking architecture:

- **Layer 1 (`operator.py`):** Peer cohort assignment — stable, governed, reusable. Produces `peer_cohort_assignments_YYYY-MM-DD.csv`.
- **Layer 2 (`benchmark_operator.py`):** Benchmark metric computation — percentile ranks, medians, deltas, and the `hv2_pbg_composite_gap` score consumed by Health V2's Growth component. Produces `peer_benchmark_YYYY-MM-DD.csv` (wide) and `peer_benchmark_long_YYYY-MM-DD.csv` (long).

The output of Layer 1 is the stable join key for any downstream consumer (the external client intelligence report, the Health V2 `peer_benchmark_gap` component, or future analytics). Layer 2 computes benchmark metrics using those assignments without redesigning cohort logic.

---

## Design Principles

1. **Stack = product package, not observed usage.** An org on Full stays in the Full cohort even if they underuse Portal. Weak adoption is flagged, not used to redefine the cohort.
2. **Vertical = HubSpot live data, not a hardcoded map.** Unresolved verticals are flagged explicitly rather than guessed.
3. **Lifecycle = eligibility filter only.** Onboarding/ramping status affects `benchmark_eligible` and `benchmark_confidence` — it does not define the peer group itself.
4. **Fallback hierarchy is explicit, not silent.** When a Tier 1 cohort is too small, the operator applies a documented fallback and records the result in `peer_group_level`.
5. **Commercial profile = context, not grouping.** ARR band, catalog scale, customer scale, and tenure band are output as descriptive metadata for downstream normalization. They do not split cohorts in v1.

---

## §1. Input Universe

The primary input is the latest Health V2 scored output CSV. Pass via `--health-output`.

All scored entities from the Health V2 run are the candidate universe. No additional MAL parsing or eligibility filtering is performed here — Health V2 eligibility is trusted as-is.

Additional data loaded by the operator:

| Source | Fields Used |
|---|---|
| BigQuery `hubspot.company` | `properties_segment`, `properties_lifecyclestage` |
| BigQuery `insightful_product.org_summary` | `created_at`, `hubspot_company_id`, `has_catalog`, `has_cart`, `has_portal` |
| Postgres cache `pg_cat.csv` | `total_active_products` |
| Postgres cache `pg_cust.csv` | `total_customers` |

---

## §2. Five-Axis Framework

### Axis 1 — Industry Vertical (primary cohort dimension)

**Source:** `hubspot.company.properties_segment` — authoritative, no hardcoded fallback.

| Value | Benchmark Relevance |
|---|---|
| `Lighting` | High SKU counts, matrix options, spec-driven sales |
| `Furniture` | Large catalogs, visual-heavy, territory-driven |
| `Home & Decor / Housewares` | Mixed catalog complexity, gift/seasonal patterns |
| `Art Manufacturers` | Lower SKU, high-value items |
| `Generic B2B Wholesale` | Catch-all |
| NULL | Unresolvable — `vertical_source = unresolved`, excluded from Tier 1 |

### Axis 2 — Platform Stack / Bundle (secondary cohort dimension)

**Source:** Health V2 output `bundle` column (MAL-sourced, already normalized).
**Precedence:** manual override → MAL bundle. Provisioning signals used only for mismatch detection.

| Value |
|---|
| `iPad-only` |
| `iPad+Catalog` |
| `iPad+Catalog+Cart` |
| `iPad+Catalog+Portal` |
| `Full` |

Stack is the product package the org **has**, not what they use. If Postgres provisioning signals differ materially from the MAL bundle, `stack_mismatch_flag = true` and `stack_assignment_confidence` is downgraded to `medium`.

### Axis 3 — Usage Intensity (benchmarked within cohort, not used for assignment)

Deferred to Layer 2. Metrics available for downstream calculation from Health V2 output:

- `logins_90d`, `active_users_90d`, `total_users` → rep activation rate
- `orders_90d` → order velocity
- `adoption_score`, `engagement_score` → feature breadth proxies
- `mp_access_sales_portal`, `mp_submit_order` → channel mix

### Axis 4 — Commercial Profile (descriptive context, not assignment dimension)

Produced as bucketed output columns. Used for downstream normalization only.

| Column | Bands |
|---|---|
| `arr_band` | `<5K` / `5-15K` / `15-30K` / `30K+` |
| `catalog_scale` | `<500` / `500-5K` / `5K-25K` / `25K+` |
| `customer_scale` | `<100` / `100-500` / `500-2K` / `2K+` |
| `tenure_band` | `<1yr` / `1-2yr` / `2-4yr` / `4yr+` |

**Recommended v1 normalization lenses for Layer 2:**
- Orders per active rep: `orders_90d / active_users_90d`
- Active users per $10K ARR: `active_users_90d / (arr / 10000)`
- Catalog completeness: already a ratio, no normalization needed

### Axis 5 — Lifecycle Stage (eligibility filter and confidence modifier)

**Source:** `org_summary.created_at` + HubSpot `properties_lifecyclestage`

| Stage | Rule | Effect on Benchmark |
|---|---|---|
| `onboarding` | `created_at` < 90 days ago OR `lifecyclestage = 'evangelist'` | `benchmark_eligible = false` |
| `ramping` | tenure < 1 year (and not onboarding) | `benchmark_eligible = true`, `benchmark_confidence` capped at `low` |
| `steady_state` | tenure >= 1 year | Primary benchmark population, full confidence rules apply |

Lifecycle does **not** define the peer group. It only controls eligibility and confidence.

---

## §3. Cohort Assignment Logic

### Primary Cohort (Tier 1)

```
peer_group_id = "{vertical} / {bundle}"
```

Count **`steady_state` entities** in this group (excluding self, excluding ramping/onboarding):

| n (steady_state peers) | peer_group_level | benchmark_confidence |
|---|---|---|
| ≥ 8 | `tier1` | `high` |
| 5–7 | `tier1` | `medium` |
| < 5 | apply fallback | — |

> **Note on assigned vs. benchmark row counts:** `peer_group_n` counts only `steady_state` peers used to compute percentiles. Ramping orgs may be *assigned* to a Tier 1 cohort (and appear in the output with `peer_group_level = tier1`) but are not counted in `peer_group_n` and are not included in `peer_orgs`. This means the total assigned rows for a cohort may exceed `peer_group_n` — this is expected and correct.

### Fallback Hierarchy

**Tier 2 — Vertical only** (if Tier 1 count < 5):

```
peer_group_id_effective = "{vertical}"
peer_group_level = "tier2"
benchmark_confidence = "low"
```

**Tier 3 — Bundle only** (if Tier 2 count also < 5):

```
peer_group_id_effective = "{bundle}"
peer_group_level = "tier3"
benchmark_confidence = "low"
```

**Tier 4 — No viable cohort** (all fallbacks fail):

```
peer_group_level = "tier4"
benchmark_eligible = false
benchmark_confidence = "none"
peer_orgs = ""
```

### Peer Org List

`peer_orgs` lists `org_shortnames` in the effective peer group, **excluding the entity itself**, filtered to `steady_state` only. Ramping and onboarding orgs are not included as peers.

---

## §4. Stack Mismatch Detection

Compare MAL `bundle` against `org_summary` provisioning signals:

| Condition | Flag |
|---|---|
| `has_portal = true` but bundle is `iPad-only` or `iPad+Catalog` | `stack_mismatch_flag = true` |
| `has_cart = false` but bundle is `iPad+Catalog+Cart` or `Full` | `stack_mismatch_flag = true` |
| `has_catalog = false` but bundle is not `iPad-only` | `stack_mismatch_flag = true` |
| No mismatch detected | `stack_mismatch_flag = false`, `stack_assignment_confidence = high` |
| Provisioning signals unavailable | `stack_mismatch_flag = null`, `stack_assignment_confidence = medium` |

---

## §5. Output Contract

One CSV per run, one row per entity in the Health V2 input universe.

| Column | Type | Description |
|---|---|---|
| `org_shortname` | string | Entity key |
| `org_name` | string | Display name |
| `vertical` | string | Industry vertical from HubSpot — NULL if unresolved |
| `vertical_source` | string | `hubspot_live` or `unresolved` |
| `bundle` | string | Platform stack from Health V2 MAL |
| `stack_assignment_confidence` | string | `high` / `medium` |
| `stack_mismatch_flag` | boolean | True if provisioning signals differ from MAL bundle |
| `peer_group_id` | string | Canonical cohort key: `{vertical} / {bundle}` |
| `peer_group_id_effective` | string | Actual cohort used after fallback (may equal `peer_group_id`) |
| `peer_group_level` | string | `tier1` / `tier2` / `tier3` / `tier4` |
| `peer_group_n` | integer | Count of **steady_state** orgs in effective cohort used for percentile calculation, **excluding self and excluding ramping/onboarding orgs**. Ramping orgs may be assigned to a cohort (appearing in Layer 1 output) without being counted here. Total assigned rows to a cohort will exceed `peer_group_n` when ramping orgs are present — this is expected. 0 for non-eligible rows. |
| `benchmark_eligible` | boolean | True if lifecycle and cohort size qualify |
| `benchmark_confidence` | string | `high` / `medium` / `low` / `none` |
| `lifecycle_stage` | string | `steady_state` / `ramping` / `onboarding` |
| `peer_orgs` | string | Pipe-separated list of steady_state peer org_shortnames in the **effective** cohort, excluding self. Empty string for non-eligible rows (onboarding, tier4). For tier2/tier3 fallback rows, includes all steady_state orgs in the vertical or bundle — not just other fallback orgs. |
| `rollup_flag` | boolean | True only if the entity participates in a real parent/child rollup structure within the scoring universe. A child: its `parent_entity` (name-matched) resolves to a different org in the universe. A parent: at least one other org resolves to it. Self-referencing `parent_entity` values (entity's own name) do NOT trigger this flag. |
| `arr_band` | string | ARR bucket |
| `catalog_scale` | string | Product count bucket |
| `customer_scale` | string | Customer count bucket |
| `tenure_band` | string | Tenure bucket |
| `run_date` | date | ISO date of this run |
| `benchmark_month` | string | `YYYY-MM` of this run |

---

## §6. How Layer 2 Consumes This Output

```python
cohorts = pd.read_csv("peer_cohort_assignments_2026-04-06.csv")
metrics = pd.read_csv("../Health V2/runs/.../client_health_scores_*.csv")

row = cohorts[cohorts.org_shortname == target_org].iloc[0]
peer_list = [p for p in row["peer_orgs"].split("|") if p]

peer_metrics = metrics[metrics.org_shortname.isin(peer_list)]
org_value = metrics[metrics.org_shortname == target_org]["logins_90d"].values[0]
pctile = (peer_metrics["logins_90d"] <= org_value).mean()
```

`peer_group_id` is also a stable join key for any future precomputed cohort medians table.

### Downstream Confidence Interpretation

**Downstream systems that consume Layer 1 or Layer 2 output must surface three fields alongside any benchmark result:**

| Field | Why it matters |
|---|---|
| `benchmark_confidence` | `high` = Tier 1, n≥8 peers. `medium` = Tier 1, n 5–7 peers. `low` = Tier 2/3 fallback or ramping org. Downstream reports should not present `low`-confidence benchmark results with the same visual weight as `high`. |
| `peer_group_level` | Indicates whether the org is benchmarked against a vertical × bundle cohort (Tier 1), vertical-only (Tier 2), or bundle-only (Tier 3). |
| `peer_group_n` | The actual number of steady-state peers in the distribution. Small `n` means wide variance in percentile ranks. Rule of thumb: treat p-values with caution when `peer_group_n` < 5. |

**Tier 3 is not automatically "bad."** In the current portfolio, the bundle-only iPad-only cohort (Tier 3) has n=50 — larger and more stable than most Tier 1 cohorts. For Portal and Full bundles, Tier 3 (n=13–18) is larger than the corresponding Tier 1 cohorts (n=4–9). Downstream consumers should use `peer_group_n` to assess reliability, not `peer_group_level` alone.

---

## §8. Layer 2 — Benchmark Metric Calculation

**Operator:** `benchmark_operator.py`
**Version:** 1.0.0

Layer 2 consumes the Layer 1 cohort assignment CSV and computes per-org benchmark comparisons: where does each org sit relative to its effective peer cohort on each metric?

### §8.1 Inputs

| Input | Argument | Description |
|---|---|---|
| Layer 1 cohort CSV | `--cohort-output` | Output of `operator.py` — defines peers for each org |
| Health V2 output CSV | `--health-output` | Component scores (0–100) for all orgs |
| Postgres cache dir | `--pg-cache-dir` | `pg_ord.csv`, `pg_cat.csv`, `pg_users.csv` |

### §8.2 v1 Benchmark Metric Set

| Metric ID | Source | Applies To | Description |
|---|---|---|---|
| `health_score` | HV2 output | All bundles | Overall health, primary cross-org signal |
| `value_delivery_score` | HV2 output | All bundles | Core value realization score |
| `adoption_score` | HV2 output | All bundles | Feature breadth / adoption depth |
| `engagement_score` | HV2 output | All bundles | Rep engagement intensity |
| `operational_health_score` | HV2 output | All bundles | Import health, data freshness |
| `trajectory_score` | HV2 output | All bundles | Trend direction (recent vs prior period) |
| `orders_90d` | `pg_ord.csv` | Cart, Full only | Raw order volume — bundle-gated |
| `orders_per_user` | Derived | Cart, Full only | `orders_90d / total_users` — normalizes by team size |
| `catalog_completeness` | `pg_cat.csv` | Catalog+ only | Product data quality ratio |

**Deferred to v1.1:** `login_intensity`, `active_user_ratio`, `portal_engagement`, `mp_access_sales_portal`, `presentation_actions` — require a Mixpanel BigQuery pull not currently preserved in the Health V2 output. Add when Health V2 is updated to pass through raw behavioral metrics.

**Bundle-gating rule:** `orders_90d` and `orders_per_user` are only benchmarked for orgs on `iPad+Catalog+Cart` or `Full`. For other bundles, `metric_applicable = false` in long format, null in wide format. `catalog_completeness` is similarly gated to catalog-capable bundles.

**Missing data:** If an org is absent from a cache file, its value is null for that metric. It is also excluded from the peer distribution for that metric — preventing zero-inflation of cohort medians.

### §8.3 Benchmark Calculation

For each eligible org and each applicable metric:

1. Get the org's metric value
2. Get the set of peer orgs from `peer_orgs` (Layer 1)
3. Filter peer values to those where the metric is applicable and the value is non-null
4. Compute: `p25`, `p50` (median), `p75` of peer distribution
5. Compute: `percentile_rank = fraction of peers at or below this org's value`
6. Compute: `delta_vs_median = org_value - peer_median` (signed)
7. Assign quartile: `Q4 ≥ 0.75 > Q3 ≥ 0.50 > Q2 ≥ 0.25 > Q1`

Non-eligible orgs (onboarding, tier4) receive null values for all benchmark columns.

### §8.4 Output Contract

**Wide format:** `peer_benchmark_YYYY-MM-DD.csv` — one row per org

Context columns: `org_shortname`, `org_name`, `bundle`, `vertical`, `peer_group_id_effective`, `peer_group_level`, `peer_group_n`, `benchmark_eligible`, `benchmark_confidence`, `run_date`, `benchmark_month`

For each metric, 5 columns:

| Column Pattern | Type | Description |
|---|---|---|
| `{metric}_org` | float | This org's raw value |
| `{metric}_peer_median` | float | Cohort median (steady_state peers, metric-applicable) |
| `{metric}_pctile` | float 0–1 | Percentile rank within effective cohort |
| `{metric}_vs_median` | float | Signed delta: org value minus cohort median |
| `{metric}_quartile` | string | `Q1` / `Q2` / `Q3` / `Q4` |

**Long format:** `peer_benchmark_long_YYYY-MM-DD.csv` — one row per org × metric

Columns: `org_shortname`, `org_name`, `bundle`, `vertical`, `peer_group_id_effective`, `peer_group_level`, `peer_group_n`, `benchmark_eligible`, `benchmark_confidence`, `metric`, `metric_label`, `metric_applicable`, `org_value`, `peer_p25`, `peer_median`, `peer_p75`, `percentile_rank`, `delta_vs_median`, `quartile`, `n_peers_with_data`, `run_date`, `benchmark_month`

**Invariant:** For all eligible rows where `metric_applicable = true` and `n_peers_with_data > 0`, `quartile` is non-null and `percentile_rank` is in [0.0, 1.0].

### §8.5 How Downstream Systems Consume Layer 2

**External-facing report (`.peer-card` component):**

```python
bench = pd.read_csv("peer_benchmark_2026-04-03.csv")
row = bench[bench.org_shortname == target_org].iloc[0]

# "Top quartile among Furniture / Full peers on rep adoption"
adoption_quartile = row["adoption_score_quartile"]   # "Q4"
peer_group = row["peer_group_id_effective"]           # "Furniture / Full"

# "Below median on order volume per active user"
orders_pctile = row["orders_per_user_pctile"]         # 0.33
orders_delta  = row["orders_per_user_vs_median"]      # -12.4
```

**Health V2 `peer_benchmark_gap` integration (OD-3):**

```python
bench = pd.read_csv("peer_benchmark_2026-04-03.csv").set_index("org_shortname")

# Direct drop-in replacement for Health V2's score_peer_benchmark_gap():
# hv2_pbg_composite_gap uses the same three-dimension formula as Health V2,
# but computes peer percentiles against the actual vertical×stack cohort instead
# of the bundle-only median.
#
# DO NOT use health_score_pctile here — health_score already aggregates multiple
# dimensions, so using it as the peer benchmark gap input creates circularity.

org = r["org_shortname"]
if org in bench.index and pd.notna(bench.loc[org, "hv2_pbg_composite_gap"]):
    peer_benchmark_gap = int(bench.loc[org, "hv2_pbg_composite_gap"])
else:
    peer_benchmark_gap = 50  # same fallback as current small-sample default
```

---

## §9. Known Caveats and Data Hygiene Backlog

These are non-blocking issues identified in the 2026-04-06 validated run. They affect interpretation precision but do not break benchmarking.

### C-1: 16 orgs with unresolved vertical (bundle-only Tier 3)

15 of 16 have no `hubspot_company_id` in `org_summary` (HubSpot join missing). 1 (`mli` / Maxim Lighting) has a join but null `properties_segment`. All 16 fall to Tier 3 (bundle-only cohort) and carry `benchmark_confidence = low`.

**Impact by bundle:**
- iPad-only (9 orgs): Tier 3 cohort n=50 — the largest cohort in the run. Low impact.
- iPad+Catalog+Cart (3 orgs): Tier 3 n=8 = same as any Cart Tier 1 cohort. Low impact.
- iPad+Catalog+Portal (2 orgs) and Full (2 orgs): Tier 3 cohorts (n=13, n=18) are *larger* than Tier 1 cohorts (n=4–9). Negative impact — Tier 3 is actually more informative here.

**Fix:** Populate `org_summary.hubspot_company_id` for missing orgs. Update HubSpot `properties_segment` for `mli`.

### C-2: `Generic B2B Wholesale` vertical (2 orgs: `lpf`, `mpc`)

These orgs have a resolved HubSpot vertical but it is `Generic B2B Wholesale` — a catch-all bucket with no vertical-specific Tier 1 cohort. They fall to Tier 3 (bundle-only). This is correct behavior but is a HubSpot data quality issue.

**Fix:** Re-categorize in HubSpot under a real vertical (`Furniture` for `lpf` / Linon-Powell, Home & Decor for `mpc` / Pioneer Morton).

### C-3: Assigned rows vs. `peer_group_n` reporting gap

When summarizing cohort sizes from the Layer 1 output, querying `peer_group_n` (the steady-state count) gives different numbers than counting assigned rows per cohort. Both are correct for their purpose but are easily confused.

- `peer_group_n`: use when evaluating statistical reliability of percentile calculations.
- Assigned row count: use when counting how many orgs are in a given cohort for operational purposes.

### C-4: Small Portal and Full Tier 1 cohorts (n=4–9)

Tier 1 cohorts for iPad+Catalog+Portal (Furniture: n=4, Lighting: n=5) and Full (Furniture: n=6, Lighting: n=8) are small. Percentile ranks are mechanically valid but carry wide variance. A single org changing health scores can shift a peer's percentile rank by 20+ points.

**Downstream rule:** For Portal and Full cohorts, surface `peer_group_n` visibly in any report. Do not present percentile ranks without `n` context when `peer_group_n` < 8.

### C-5: 4 ramping orgs benchmarked at `low` confidence

`jcusa`, `prog`, `kl`, `wac` — all iPad-only, `<1yr` tenure, all assigned to Tier 1 Lighting/iPad-only cohort (n=16). They receive real percentile ranks but `benchmark_confidence = low`. Their own metrics may be unrepresentative of steady-state behavior.

**Downstream rule:** Do not include ramping orgs in portfolio-level benchmark aggregations unless specifically analyzing ramp performance.

---

## §7. Open Decisions

| # | Decision | Impact |
|---|---|---|
| OD-1 | L2 subsegment (`properties_subsegment`) — sparse today; add when coverage improves | Tighter peers for Lighting, Furniture (20+ entities) |
| OD-2 | Ramping cohorts — currently excluded from `peer_orgs`; consider separate ramping cohorts for TTFV benchmarks | Onboarding/ramping trajectory comparisons |
| OD-3 | ~~Wire `peer_group_id_effective` into Health V2 `peer_benchmark_gap`~~ — **Resolved in v1.1.0 / HV2 v2.4.0.** `hv2_pbg_composite_gap` from Layer 2 is now consumed by Health V2 via `--peer-benchmark`. | Resolved |
| OD-4 | ~~Precompute cohort medians into a `peer_benchmark_monthly` table~~ — **Resolved.** Layer 2 (`benchmark_operator.py`) is now operational and produces wide + long benchmark output per run. | Resolved |
