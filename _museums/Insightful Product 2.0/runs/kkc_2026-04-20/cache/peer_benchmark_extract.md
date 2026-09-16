# Peer Benchmark Extract — Kindel Furniture (kkc)
- **Source**: peer_benchmark_2026-04-14.csv (Peer Benchmark run 2026-04-14 — 6 days old)
- **Run date**: 2026-04-20
- **benchmark_eligible**: True
- **benchmark_confidence**: high (internal only — not in delivered HTML)
- **peer_group_level**: tier1 (internal only — not in delivered HTML)
- **peer_group_n**: 16 (internal only — calibrates plain-language framing strength; never exposed as a literal number in external output)
- **peer_group_id_effective**: Furniture / iPad-only (source value for building plain-language cohort framing; never exposed as a raw label in external prose)

## Score Comparison vs. Peer Group

| Dimension | Org Score | Peer Median | Percentile | vs. Median | Quartile |
|-----------|-----------|-------------|------------|------------|---------|
| Overall Health Score | 56 | 45 | 62.5% | +11 | Q3 |
| Value Delivery Score | 40 | 40 | 56.2% | 0 | Q3 |
| Adoption Score | 57 | 64 | 50.0% | −7 | Q3 |
| Engagement Score | 50 | 60 | 25.0% | −10 | Q2 |
| Operational Health Score | 100 | 65 | 100.0% | +35 | Q4 |
| Trajectory Score | 50 | 25 | 68.8% | +25 | Q3 |

## Metric Comparison vs. Peer Group

| Metric | Org Value | Peer Median | Notes |
|--------|-----------|-------------|-------|
| Orders (90-day) | 0 | — | No peer comparison available (many peers at 0 in this group) |
| Orders per user | 0 | — | No peer comparison available |
| Catalog completeness | 99.6% | — | No peer comparison available |
| Login intensity | — | — | No peer comparison available in this extract |

## Peer Comparison from BigQuery segment_peer_comparison

| Metric | Org Value | Peer Median | vs. Peer % | Notes |
|--------|-----------|-------------|------------|-------|
| LTM eCat orders | 0 | 0 | — | Catalog-Focused segment; many peers at 0 |
| All-time Mixpanel logins | 1,258 | 271 | +364.2% | Substantially above peer median |
| MRR | $2,460 | $725 (implied) | +239.3% | Above peer median |
| peer_standing | Needs Attention | — | — | Driven by 0 eCat orders |

## HV2 Peer Benchmark Group Metrics (internal reference)

| Metric | Value |
|--------|-------|
| hv2_pbg_login_intensity_pctile | — (not available) |
| hv2_pbg_primary_value_pctile | — (not available) |
| hv2_pbg_adoption_pctile | 50th percentile |
| hv2_pbg_primary_value_metric_id | presentation_actions |
| hv2_pbg_composite_gap | 47 |

## Cohort Description for External Use (§4 Peer Benchmarking)

Do NOT use segment labels ("Catalog-Focused", "Platform-Embedded") or raw peer_group_id_effective value ("Furniture / iPad-only") in external prose. Describe in plain language:
> "furniture manufacturers using the iPad platform for rep selling and presentation"

The cohort includes 16 peers at the tier1 confidence level. Benchmark confidence is high.

## Stage 2 Guidance

- Overall health score (56 vs. 45 median): Above peer median at 62nd percentile — strengths are operational health (Q4, top of peer group) and trajectory (Q3, 69th percentile)
- Engagement score (Q2, 25th percentile) and Adoption score (at median, 50th percentile) are below-average — likely reflecting lapsed order submission and underuse of order capture features
- Operational health score = 100 (top of peer group) — reflects clean data import pipeline and catalog quality despite lapse
- primary_value_metric = presentation_actions — this org's primary measurable value signal is presentation activity (PDF catalogs, library usage, item emails)
- peer_standing = "Needs Attention" — driven primarily by 0 eCat order submissions; re-framing for Mode 3: the platform is configured and operationally healthy; the re-engagement gap is behavioral, not infrastructural
