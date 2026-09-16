# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status Dashboard | MANDATORY | MET (Q-08, Q-09, Q-22 all present with data) | YES |
| Operational Alerts (Action Required) | CONDITIONAL | MET (Q-08: 6 entities at 301d Critical; price_levels at 121d Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 16 tracked features; MIXPANEL_ORDER_TRACKING_GAP=False so Order Submission retained) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | CONDITIONAL | PERMANENTLY EXCLUDED (peer benchmark data unreliable) | NO |
| Peer Benchmarking Summary | CONDITIONAL | PERMANENTLY EXCLUDED (peer benchmark data unreliable) | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (Q-09 shows healthy consistent cadence 227–500/mo, no stall or irregularity) | NO |

## Notes
- §6 uses NO data confidence header (per shared contract §2) and NO section-level what-this-means (per guide).
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- Peer cache files (Q-CI-02/03) present in bundle but EXCLUDED — not read or referenced.
- Freshness: 6 entities at 301d = Critical (.badge.danger / row-danger); price_levels at 121d, price-level entity override (stale >30d) → Stale (.badge.warn / row-warn).
- Feature Utilization order-tracking gap is FALSE → submit_order (Order Submission) retained in table.
