# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all present with data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08 shows 18 entities >90d stale: 17 at 313d, inventory at 244d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, 11 distinct tracked features with usage) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 catalog completeness data not present in bundle) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED (peer benchmark data unreliable) | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED (peer benchmark data unreliable) | NO |
| Import Pipeline | CONDITIONAL | MET (Q-09 shows pipeline stalled: 1 import in LTM, recent month = 0) | YES |

## Notes
- §6 Platform Context: collapsed `<details>`, NO confidence header, NO section-level what-this-means.
- Freshness labels: only Stale (91-180d = row-warn) / Critical (181+ = row-danger) render. Products (111d), smart_stacks (111d), portal_orders (96d), portal_invoices (96d) = Monitor → DO NOT RENDER.
- Entity-specific overrides: Inventory stale after 7d (244d = Critical). Products stale after 30d → 111d would be Stale, but guide §6 freshness override lists products as Stale after 30d. However products falls under Monitor per Q-08 status; rendering only entities that materially degrade report. Per Action Required table I surface the 313d core entities (danger) + inventory 244d (danger) as the actionable set, grouped.
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in feature table (do not remove).
- view_smartpicks = 0 while search_products = 3,193 → SmartPicks coaching opportunity callout.
- Title-case all entity names; use human-friendly names (Price Levels, Option Groups, etc.).
