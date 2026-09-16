# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL (any entity >90d stale OR config drift) | MET (Q-08 shows 11 entities 285–313d Stale) | YES |
| Feature Utilization | CONDITIONAL (Q-22 ≥3 features) | MET (Q-22 has 17 tracked features, MIXPANEL_ORDER_TRACKING_GAP=False) | YES |
| Catalog Remediation | CONDITIONAL (Q-07 completeness <95% OR >50 items missing assets) | NOT MET (Q-07 not present in bundle — no data) | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL (pipeline stalled OR irregular) | NOT MET (Q-09 consistent 27–76/mo, recent month >0, no stall) | NO |

## Notes
- §6 uses NO data-confidence header (per shared contract §2 and guide).
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- TARGET STRUCTURE anchored: thead/tbody, row-warn/row-danger highlight rows, per-subsection what-this-means.
- Q-10 empty (0 rows) → no smart stack data; smart_stacks entity exists in Q-08 (Monitor, 50d) so org HAS configured smart stacks → Smart Stacks badge = ok.
- Entity-specific staleness overrides applied: products stale after 30d (products=50d → Monitor, not stale per general; but products override = Stale after 30d → flagged), price_levels (285d) Critical.
- MIXPANEL_ORDER_TRACKING_GAP=False → keep order submission in feature table (no removal).
