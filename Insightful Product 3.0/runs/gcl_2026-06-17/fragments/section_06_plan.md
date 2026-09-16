# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Operational Alerts (Action Required) | CONDITIONAL | MET (9 entities Critical 181+; 313d/281d stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 13+ tracked features; MIXPANEL_ORDER_TRACKING_GAP=False so submit_order retained) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | MET (Q-09 irregular: Dec=2, Jan=30, then 14/15/11/7/12 — declining/irregular cadence) | YES |

## Notes
- §6 uses NO confidence header (per shared contract §2).
- §6 renders as collapsed `<details>`.
- Health badges per defined thresholds:
  - Core Pipeline: avg monthly imports = (12+7+11+15+14+30+2)/7 ≈ 13/mo → <50 → `.badge.warn` "Low Volume" (not <10, recent month Jun=12 ≠ 0)
  - Data Freshness: >3 Stale entities (9 at 313d + kit_items 281d = 10 Stale >90d) → `.badge.danger`
  - Feature Adoption: distinct active features ≥5 → `.badge.ok`
  - Smart Stacks: Q-10 returned 0 rows; smart_stacks entity is Fresh (13d) in Q-08 → configured → `.badge.ok` (>0)... but Q-10 (enablement gap) returned no rows. smart_stacks present & fresh in Q-08 → treat as configured → `.badge.ok`.
- Catalog card omitted from dashboard (no Q-07 data).
- Entity-specific staleness overrides applied (inventory stale after 7d, products/price after 30d).
