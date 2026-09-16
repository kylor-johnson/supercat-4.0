# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status (Dashboard) | MANDATORY when any data available | MET (Q-08, Q-09, Q-22, Q-10 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (12 entities stale >90d in Q-08/Q-11; 11 at 301d Critical, price_levels 156d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, ≥3 distinct features; MIXPANEL_ORDER_TRACKING_GAP=False) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | excluded | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | excluded | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (Q-09 avg ~1,024 imports/mo, healthy & consistent — no stall/irregularity) | NO |

## Notes
- §6 does NOT use a data-confidence header (per shared contract §2).
- §6 has NO section-level what-this-means; each subsection carries its own.
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- Health Dashboard cards: Core Pipeline (Healthy), Data Freshness (danger — >3 stale), Feature Adoption (ok — ≥5 active), Smart Stacks (ok — 40 published). Catalog card omitted (no Q-07 data).
- Entity-specific staleness overrides applied: options/option_groups/matrix_options at 301d = Critical (danger); price_levels at 156d = Stale (warn).
