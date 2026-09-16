# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-10, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08: 9 entities >90d stale; price_levels 225d, 8 entities 300d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 present, >3 distinct features tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not included in bundle Cache Data — no completeness data available) | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | MET (Q-09 cadence irregular: Feb dip to 40; recurring "product not found" import errors every cycle) | YES |

## Notes
- §6 does NOT use a data-confidence header (per shared contract §2).
- §6 renders as collapsed `<details class="section-collapse" id="platform">`.
- No section-level what-this-means (per guide).
- Health badges:
  - Core Pipeline: avg ~176/mo imports (≥50) → `.badge.ok` Healthy
  - Data Freshness: 9 entities >90d stale → `.badge.danger` Stalled/Stale
  - Feature Adoption: ≥5 active features → `.badge.ok`
  - Smart Stacks: 14 published (Q-10) → `.badge.ok`
  - Catalog card OMITTED (no Q-07 data in bundle)
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in feature table.
- Entity-specific freshness overrides: products 1d (Fresh), inventory 0d (Fresh) — both OK, not alerted.
