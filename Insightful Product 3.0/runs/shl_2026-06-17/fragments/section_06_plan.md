# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-07, Q-08, Q-09, Q-10, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08 shows 11 entities at 301d stale; Q-11 surfaces price-code config drift) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has >3 distinct features tracked; MIXPANEL_ORDER_TRACKING_GAP=False so submit_order retained) | YES |
| Catalog Remediation | CONDITIONAL | MET (Q-07 shows 56 items missing images > 50 threshold, even though completeness 98.9% ≥95%) | YES |
| Feature Adoption vs Peers | n/a | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | n/a | PERMANENTLY EXCLUDED | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (pipeline healthy & consistent: avg ~126/mo, recent month 75, no stall) | NO |

## Badge logic resolved
- Core Pipeline: avg ~126/mo (≥50) → `.badge.ok` "Healthy"
- Data Freshness: 11 entities >90d stale (>3) → `.badge.danger` "Needs Attention"
- Catalog: 98.9% (≥95%) → `.badge.ok` "Complete"
- Feature Adoption: many active features (≥5) → `.badge.ok` "Active"
- Smart Stacks: 9 published (>0) → `.badge.ok` "Configured"

## Notes
- §6 has NO confidence header (per shared contract §2).
- §6 has NO section-level what-this-means (per guide).
- Freshness labels: 301d = Critical → `.badge.danger`.
- Entity names rendered human-friendly (no snake_case).
- Peer benchmark cache files NOT read/referenced.
