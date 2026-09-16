# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08/Q-09/Q-22/Q-10 all have data) | YES |
| Action Required | CONDITIONAL | MET (15 entities >90d stale in Q-08; Q-11 confirms config drift) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 12+ tracked features) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — cannot evaluate completeness) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (pipeline healthy & consistent — ~118/mo avg, no stalled month) | NO |

## Health Dashboard card logic
- Core Pipeline: avg ~118 imports/mo (828/7) → `.badge.ok` Healthy
- Data Freshness: 15 entities >90d stale → `.badge.danger` (>3 Stale)
- Feature Adoption: 12 active tracked features → `.badge.ok` (≥5)
- Smart Stacks: 63 published (Q-10) → `.badge.ok`
- Catalog card OMITTED (Q-07 not present, cannot compute completeness %)

## Notes
- §6 has NO confidence header (per shared contract §2 + guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission row in Feature Utilization.
- Peer benchmark cache files (Q-CI-*) NOT read/referenced.
- No section-level what-this-means (per guide).
- EVERY table wrapped in `<thead>`/`<tbody>` (regeneration fixes prior bare-header bug).
