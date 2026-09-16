# Section Guide: §7 — Peer Benchmarking

## Section Identity
- **id**: `peer`
- **title**: Peer Benchmarking
- **section number**: 7
- **include when**: `HAS_PEER_DATA = true AND BENCHMARK_ELIGIBLE = true AND PEER_GROUP_LEVEL != 'tier4'`
- **skip when**: any of those conditions is false — omit silently from TOC and report, no note in delivered report

Cases that produce a skip:
- No peer file: omit entirely.
- `BENCHMARK_ELIGIBLE = false`: omit entirely.
- `PEER_GROUP_LEVEL = 'tier4'`: omit entirely.

## Query Inputs

Read these cache files:
- `cache/peer_benchmark_extract.md` — pre-extracted peer CSV data (wide + long format fields)
- `cache/Q-CI-03_results.md` — Feature adoption benchmarking
- `cache/Q-CI-05_results.md` — Top-performer patterns
- `cache/gate_flags.md` — for `BENCHMARK_CONFIDENCE`, `PEER_GROUP_N`, `PEER_GROUP_LEVEL`, `PEER_GROUP_ID_EFFECTIVE`

Also read: `dependencies/PEER_BENCHMARK.md` — for approved tier framing language, Python formulas, range bar math, and sentence writing guide. That file contains the detailed peer framing rules that are too extensive to duplicate in this guide.

## Inclusion / Exclusion Rules

- `BENCHMARK_CONFIDENCE = 'low'`: Include the section with plain-language directional framing. `low` reflects Tier 2/3 fallback cohort or a ramping org. Use the appropriate Tier 2 or Tier 3 plain-language framing from `dependencies/PEER_BENCHMARK.md §7`. Do not expose the word "low" or any confidence label to the client. If `PEER_GROUP_N` is also small (< 5), calibrate phrasing toward "directional context" rather than "precise benchmark."
- `BENCHMARK_CONFIDENCE = 'medium'`: Include with a brief directional note. Use `PEER_BENCHMARK.md §7` language. Do not expose the label.
- `BENCHMARK_CONFIDENCE = 'high'`: Include without caveat. No label needed.

## Segment Label Rule

The cohort must be described using plain-language framing derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle" — not the raw `{vertical} / {bundle}` label string). Internal labels (Platform-Embedded, Commerce-Active, Catalog-Focused) must not appear anywhere. See `dependencies/PEER_BENCHMARK.md §3 and §7` for approved framing patterns by tier:
- Tier 1 (vertical + bundle match): "Lighting manufacturers on the same platform bundle"
- Tier 2 fallback (vertical only): "other [vertical] manufacturers"
- Tier 3 fallback (bundle only): "other accounts on the [bundle] plan"

## Health Score Rule

Do not include health score benchmarks in this section. The `health_score` metric is internal only — suppress entirely.

## Subsection Assembly Order (do not reorder)

### 1. Peer Group Header

Write a 1-sentence description of the peer group using the plain-language framing derived from `peer_group_id_effective`. Populate `{{PEER_GROUP_DESCRIPTION}}`.

Render as a `<div class='subsection'>` with `subsection-title`, following the standard subsection structure. Do not render as a bare preamble paragraph outside the subsection wrapper.

If `BENCHMARK_CONFIDENCE` is `low` or `medium`, fold the framing note into this sentence using approved language from `dependencies/PEER_BENCHMARK.md §7`. Do not use a separate "confidence" label or footnote.

### 2. Hero Stat

Select the metric with the most striking story (positive or negative). Priority list — use the first applicable:

1. `orders_per_user` — if `HAS_CART` and `metric_applicable = true`. Most legible to a client: normalized by team size, directly comparable.
2. `engagement_score` — if the org is a strong outlier (Q4 or Q1).
3. `adoption_score` — if Q4 (leads to a positive story about platform depth).
4. `catalog_completeness` — if Q4 or Q1 (either a standout or an actionable gap).
5. `trajectory_score` — if Q3/Q4 and the org's absolute metrics are modest (momentum story).

Never use `health_score` as hero. Never use a metric where `metric_applicable = false`.

Populate these template parameters:
- `{{HERO_METRIC_LABEL}}` — plain-language metric name
- `{{HERO_METRIC_VALUE}}` — formatted org value
- `{{HERO_METRIC_SENTENCE}}` — complete sentence with org value, peer median, signed delta, peer group context
- `{{HERO_PCTILE_DISPLAY}}` — percentile badge text
- `{{HERO_PCTILE_DIRECTION}}` — CSS class for the badge

**Percentile display rules**: Round to nearest 5%. Use `"Top X%"` for Q3/Q4, `"Bottom X%"` for Q1. Apply class `.above` for Q3/Q4, `.below` for Q1, `.on-par` for Q2 on the `.peer-hero-pctile` element.

### 3. Narrative Metric Rows (Full Benchmark Breakdown)

One row per applicable metric. Skip the hero metric (already shown above) and `health_score`.

For each row:
- Write a complete sentence: org value, peer median, signed delta, peer group context in plain language.
- Compute range bar marker position: `clamp((org_value - p25) / (p75 - p25) * 100, 0, 100)`. Use `peer_p25` and `peer_p75` from the long CSV.
- Range bars are REQUIRED for each benchmark row — do not substitute with prose-only descriptions. Each row must include a `.peer-range-bar` element with a positioned `.peer-range-marker`.
- Apply `.above` / `.below` / `.on-par` to the range marker class based on quartile.
- Apply `.q4` / `.q3` / `.q2` / `.q1` to the quartile pill. Labels: "Top Quartile" / "Above Median" / "Below Median" / "Bottom Quartile".

**Metric whitelist — render ONLY these metrics. Do not render rows for any metric not in this list, even if `metric_applicable = true` in the CSV:**

| Metric Key | Display Name | Bundle Gate |
|------------|-------------|-------------|
| `orders_90d` | Orders (90-Day) | Cart/Full only |
| `orders_per_user` | Orders per User | Cart/Full only |
| `value_delivery_score` | Value Delivery | All bundles — measures core value realization across the platform |
| `engagement_score` | Engagement | All bundles |
| `adoption_score` | Adoption | All bundles |
| `operational_health_score` | **Data & Operational Health** | All bundles — see critical label rules below |
| `trajectory_score` | Trajectory | All bundles |
| `catalog_completeness` | Catalog Completeness | Catalog bundles |

Use these display names EXACTLY as written. Do not embellish or prefix with additional words (e.g., "Trajectory" not "Platform Trajectory").

**CRITICAL: `operational_health_score` label AND sentence rules:**
- `peer-metric-title` MUST be `"Data & Operational Health"` — never `"Operational Health Score"`
- The phrases `"health score"` and `"health scores"` MUST NOT appear anywhere in this row — not in the title, not in the sentence, not in supporting text
- The internal key `operational_health_score` must never appear in delivered HTML
- **Required sentence framing**: `"Catalog freshness and import health at X"` or `"Data freshness and configuration reliability at X"` — never `"import health score at X"` or `"operational health score is X"`
- This metric is external-safe. The restrictions apply to label vocabulary and sentence phrasing only.

**NEVER skip `operational_health_score` from the benchmark breakdown** — it is external-safe. The restriction covers both the title and the sentence — the word "score" must not follow "health" anywhere in the row.

### 4. What Top Performers Do

Pull 3–5 behavioral patterns from Q-CI-05 (`top_performers_by_segment`). Write each as a concrete, specific behavior with numbers where available.

**Top-performer prose guardrail**: The phrases `"health score"`, `"health scores"`, and `"operational health score"` are forbidden in all top-performer narrative rows. If a pattern relates to import consistency or data freshness, describe the behavior and its platform effect without health-score vocabulary:
- ✅ `"Top performers run automated imports across all entity types on a consistent schedule, keeping configuration data current."`
- ✅ `"Accounts with the strongest data freshness profiles import options, kit items, and price levels on the same cadence as products and inventory."`
- ❌ `"Lower operational health scores are traceable to stale configuration data."` — forbidden ("health scores")

**Order submission gap guardrail**: When `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md` and the account has historical Postgres orders, do not frame order submission as a new behavior to adopt or a missing capability. Frame it as maintaining or resuming existing activity:
- ✅ `"Top performers maintain consistent order flow through the platform, keeping their sales pipeline digital."`
- ✅ `"Accounts with the strongest commerce metrics submit orders regularly through the iPad workflow."`
- ❌ `"This account has not yet adopted order submission through the app."` — contradicts Postgres order history
- ❌ `"Top performers actively submit orders — a workflow this account has not explored."` — contradicts Postgres order history

When the flag is `false` or absent, no adjustment is needed — Q-22 and Postgres data are consistent.

`[COLLAPSE]`

### 5. Feature Adoption Table (Q-CI-03)

Render with these exact three columns — no others:

| Column Header | Source | Notes |
|---|---|---|
| Feature / Capability | Feature name from Q-CI-03 | Plain-language name |
| Your Status | Active / Configured / Not Active | Use `.badge` class with `ok` / `warn` / `muted` styling |
| Peer Adoption Rate | % of peers with feature active from Q-CI-03 | e.g., "78% of peers" |

Do not add columns beyond these three unless Q-CI-03 returns additional per-feature metrics not covered above. Never list CPQ as a gap if the client doesn't have CPQ.

`[COLLAPSE]`

### 6. Growth Trajectory (Q-CI-04)

**Skip until May 2026.** Requires 2+ monthly snapshots. Commented out in template. Do not include until data is available.

## Section-Specific Rules

- Read `dependencies/PEER_BENCHMARK.md` for the full tier framing language, Python formulas for range bar math and percentile display, and sentence writing guide. Those details are authoritative and too extensive to inline here.
- `peer_group_n` is an internal calibration signal — never expose as a literal count in client-facing output. Do not write "compared to 33 accounts" or "15-peer cohort." Let the `peer_group_id_effective` label carry the cohort description.
- Do not frame Tier 3 (bundle-only cohort) as a limitation or apology — it is a valid comparison set.
- One `what-this-means` per subsection. Do not add a section-level `what-this-means` after the last subsection's close.
