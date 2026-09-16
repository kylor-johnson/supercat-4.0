# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET — Q-08, Q-09, Q-22 all have data | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET — Q-08 shows 14 entities @ 313d (Critical) + 6 @ 153d (incl. products, override 30d) | YES |
| Feature Utilization | CONDITIONAL | MET — Q-22 has 12+ distinct features tracked; MIXPANEL_ORDER_TRACKING_GAP=False (keep submit_order) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET — Q-07 results not present in bundle (no data block) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | n/a | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | n/a | NO |
| Import Pipeline | CONDITIONAL | MET — Q-09 stalled: only 1 month (Jan 2026, 7 imports), recent months = 0 | YES |

## Notes
- §6 uses NO data-confidence header (per shared contract §2).
- Smart Stacks health card OMITTED — Q-10 returned 0 rows (never configured).
- Catalog health card OMITTED from dashboard — Q-07 not present (no completeness %).
- Peer benchmark cache files (Q-CI-02/03) present in bundle but EXCLUDED — not read/referenced.
- Freshness badges: 181+d = `.badge.danger` (Critical); products at 153d = Critical (30d override).
- Render order: Health Dashboard → Action Required → Feature Utilization → Import Pipeline.
- Section is collapsed `<details>`. Every rendered subsection ends with `.what-this-means`. No section-level what-this-means.
