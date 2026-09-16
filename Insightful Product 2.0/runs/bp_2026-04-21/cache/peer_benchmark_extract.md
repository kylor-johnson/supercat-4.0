# Peer Benchmark Extract — Buster & Punch (bp, org_id=250)
- **Run date**: 2026-04-21
- **Segment**: Commerce-Active
- **Peer group size**: 52
- **Benchmark source**: BigQuery segment_peer_comparison + segment_benchmarks_monthly

## Org vs. Peer Comparison

| metric | bp_value | peer_median | peer_p25 | peer_p75 | bp_vs_median_pct | quartile |
|--------|---------|-------------|----------|----------|-----------------|----------|
| submit_order (all-time) | 66 | 245 | 103 | 290 | -73.1% | Below p25 |
| total_logins (all-time) | 2,411 | 2,578 | 1,476 | 5,605 | -6.5% | p25–median |
| search_products (all-time) | 2,244 | 5,017 | 3,455 | 28,432 | — | Below p25 |
| feature_depth | 3 | — | — | — | — | — |
| arr | — | $10,240 | $7,902.50 | $22,228.50 | N/A | N/A |

## Peer Standing

- **Overall**: Needs Attention
- **Key gap**: Order submission is 73% below median — login engagement is nearly at par, suggesting the platform is used for browsing/presentation but orders are not consistently submitted through eCat

## Segment Feature Adoption Context

| feature | segment_adoption_pct | bp_has_feature |
|---------|---------------------|---------------|
| Library | 100% | Yes (891 views) |
| PDF Catalog | 94.2% | Yes (29 catalogs created) |
| Sales Portal | 50.0% | No |
| Portal Orders (ERP sync) | 50.0% | No (0 portal_orders) |
| CPQ | 11.5% | No |
| Kit Items | 7.7% | No |
