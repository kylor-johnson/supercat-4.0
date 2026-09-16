# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08, Q-09, Q-22, Q-10 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08 shows 15 entities >90d stale: 9 Critical at 254–301d, 6 Stale at 117d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 present, 13+ distinct features tracked; MIXPANEL_ORDER_TRACKING_GAP=False so Order Submission retained) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 cadence steady 17–47/mo, no stall; current month partial — no story worth telling) | NO |

## Notes
- Section renders as collapsed `<details class="section-collapse" id="platform">`.
- §6 does NOT use a data-confidence header (per shared contract §2).
- No section-level what-this-means (per guide).
- Health dashboard cards: Core Pipeline (warn/Low Volume, ~37/mo avg), Data Freshness (danger, 15 stale >90d), Feature Adoption (ok/Healthy, 13+ active), Smart Stacks (ok, 1 published). Catalog card omitted — no Q-07 data.
- Operational Alerts: entity-specific overrides applied (products 5d=fresh, inventory 0d=fresh, smart_stacks 54d=Monitor → not rendered). Stale rows grouped by impact.
