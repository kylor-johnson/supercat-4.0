# Section 06 Build Plan — Platform Context

Confidence header: N/A — §6 (Platform Context) does NOT use a data confidence header.
Section render mode: collapsed `<details class="section-collapse" id="platform">`.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status Dashboard | MANDATORY | MET (Q-07, Q-08, Q-09, Q-22 all have data) | YES |
| Operational Alerts | CONDITIONAL | MET (Q-08: 11 entities 313d Critical, 2 entities 96d Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22: 10 active features; MIXPANEL_ORDER_TRACKING_GAP=False so Order Submission retained) | YES |
| Catalog Operational Recommendations | CONDITIONAL | MET (Q-07: 78 items missing images > 50 threshold) | YES |
| Feature Adoption vs Peers | CONDITIONAL | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | CONDITIONAL | PERMANENTLY EXCLUDED | NO |
| Import Pipeline Detail | CONDITIONAL | MET (Q-09: cadence irregular — dip to 3/mo Jan–Feb, recovery to 26–36/mo Mar–Jun) | YES |

## Health Dashboard card logic
- Catalog: visible completeness 97.6% ≥95% → `.badge.ok` Healthy
- Feature Adoption: 10 active features ≥5 → `.badge.ok` Healthy
- Smart Stacks: Q-08 smart_stacks refreshed 4d ago → `.badge.ok` Maintained
- Core Pipeline: LTM avg ≈19 imports/mo (<50) → `.badge.warn` Low Volume
- Data Freshness: 11 entities >90d stale (>3) → `.badge.danger` Stale

## Notes
- Q-CI-02 / Q-CI-03 / Q-CI-03-bench / Q-CI-05 / peer_benchmark_extract: NOT read/referenced (peer data excluded).
- Missing Price = 0 across all rows (price-level pricing — valid config, not a gap).
- Section-level what-this-means: NOT required for §6.
