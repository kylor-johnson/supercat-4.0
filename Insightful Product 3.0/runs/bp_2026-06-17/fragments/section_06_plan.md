# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status Dashboard | MANDATORY | MET (Q-07, Q-08, Q-09, Q-10, Q-22 all have data) | YES |
| Operational Alerts | CONDITIONAL | MET (11 entities at 313d stale + price_levels 118d + 2 entities 96d — far beyond 90d threshold) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, >3 distinct features tracked: search_products 2,800, search_for_customer 1,746, etc.) | YES |
| Catalog Operational Recommendations | CONDITIONAL | MET (Q-07 completeness 43.8% < 95%; 495 missing images, 1,237 missing price > 50) | YES |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (pipeline healthy & consistent: 35–99/mo, recent month June=34 active, no stall) | NO |

## Confidence header
§6 (Platform Context) does NOT use a confidence header (per shared contract §2). No header rendered.

## Notes
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in feature table (submit_order=72).
- Entity-specific staleness overrides applied: Inventory fresh (0d), Products fresh (8d) → not in alerts. price_levels 118d → Stale per >30d products/price override → warn. portal_orders/portal_invoices 96d → general 90d threshold → warn.
- Section renders as collapsed `<details>`.
- No section-level what-this-means (per guide).
