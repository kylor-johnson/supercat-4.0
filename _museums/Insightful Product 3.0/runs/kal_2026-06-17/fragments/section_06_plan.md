# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-10, Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (Q-08 shows 10 entities at 300d Critical, price_levels 106d Stale, products 43d > 30d override Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 13+ distinct features with usage; >3 tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — cannot evaluate completeness) | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 avg ~101/mo, recent month 61 — healthy and consistent, no story) | NO |

## Notes
- §6 does NOT use a data-confidence header (per shared contract).
- §6 renders as collapsed `<details>`.
- No section-level what-this-means (per guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → submit_order (266) stays in feature table.
- Smart Stacks: 8 published (Q-10) → Health card badge.ok.
- Entity-specific freshness overrides applied: products/price_levels stale after 30d; inventory after 7d (inventory is 0d = Fresh, not rendered).
