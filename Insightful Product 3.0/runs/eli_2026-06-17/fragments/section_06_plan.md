# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08: 14 entities >90d stale, 11 at 313d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 present, 12 active features tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (no Q-07 catalog completeness data in bundle) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED (unreliable peer data) | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED (unreliable peer data) | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 consistent 41–116/mo, no stall, no zero month) | NO |

## Notes
- §6 uses NO data-confidence header (per shared contract §2).
- §6 renders as collapsed `<details class="section-collapse">`.
- No section-level what-this-means (per guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → keep order submission in Feature Utilization.
- Health dashboard cards: Core Pipeline (Healthy, ~74/mo), Data Freshness (Stalled/danger, 14 stale), Feature Adoption (Healthy, 12 active), Smart Stacks (16 published, ok). Catalog card omitted (no Q-07).
- Peer benchmark cache files (Q-CI-*) present in bundle but NOT read/referenced/rendered.
- access_sales_portal excluded from Feature Utilization (enable_sales_portal=0 — client lacks this feature).

## Health dashboard computations
- Core Pipeline: avg (41+63+106+61+61+116+68)/7 = 73.7/mo → ≥50 → ok "Healthy"
- Data Freshness: 14 entities >90d (11 @ 313d, price_levels @103d, portal_orders/invoices @96d) → >3 stale → danger "Stalled"
- Feature Adoption: 12 features with >0 LTM events (excl. access_sales_portal) → ≥5 → ok "Healthy"
- Smart Stacks: 16 published → >0 → ok "Active"
