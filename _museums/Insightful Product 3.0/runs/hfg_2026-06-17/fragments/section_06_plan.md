# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY when any data available | MET (Q-08/Q-09/Q-22/Q-10 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (9 entities at 300d stale in Q-08, >3 Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, 15 features tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | n/a (peer data unreliable) | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | n/a (peer data unreliable) | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 healthy + consistent: 72–104/mo, June partial at 33; not stalled/irregular) | NO |

## Notes
- §6 does NOT use a data-confidence header (per shared contract).
- §6 renders as a collapsed `<details class="section-collapse">`.
- No section-level what-this-means (per guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → Order Submission stays in the Feature Utilization table.
- Smart Stacks card: smart_stack_count=7 (>0) → `.badge.ok`, card included.
- Catalog card omitted from health dashboard (no Q-07 data).
- Health dashboard cards: Core Pipeline (Healthy, avg 72/mo), Data Freshness (danger, 9 stale), Feature Adoption (ok, 15 active), Smart Stacks (ok, 7 published).
- Staleness >180d (300d) → priority-action-worthy per guide → 1 highlight.
