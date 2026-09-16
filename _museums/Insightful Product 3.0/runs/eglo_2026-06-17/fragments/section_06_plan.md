# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08: 10 entities at 313d Critical, 2 entities at 96d Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 13 active tracked features) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no completeness data) | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 pipeline healthy & consistent: 103–164/mo, recent 70 — no stall, no irregular cadence) | NO |

## Notes
- §6 does NOT use a data confidence header (per shared contract §2).
- §6 renders as a collapsed `<details>`.
- No section-level what-this-means (per guide).
- Health Dashboard cards: Core Pipeline (Healthy), Data Freshness (12 Stale → danger), Feature Adoption (Healthy). Catalog card omitted (no Q-07). Smart Stacks card omitted (no published-count source).
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in Feature Utilization.
- Peer/Q-CI cache files NOT read or referenced.
