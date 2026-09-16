# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY when any data available | MET (Q-08, Q-09, Q-22, Q-10 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (18 entities >90d stale; 13 at 313d Critical) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 17 tracked features, multiple active) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no completeness data) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | — | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | — | NO |
| Import Pipeline | CONDITIONAL | MET (Q-09 irregular: 12/25/3/3/3 — cadence collapse story) | YES |

## Notes
- §6 uses NO confidence header (per shared contract §2).
- §6 has NO section-level what-this-means (per guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → keep order-submission data; submit_order=683 (non-zero), so no artifact suppression needed.
- Health badges: Core Pipeline = danger (recent month 12 <50, prior months as low as 3 = Stalled-ish; avg <50 → Low Volume; recent dip → flag Low Volume warn). Data Freshness = danger (>3 Stale). Feature Adoption = ok (>=5 active features). Smart Stacks = ok (16 published per Q-10).
- Health label normalization: 313d/264d/246d all >180d → Critical (.badge.danger). Entity overrides: inventories stale after 7d, price/products after 30d — all far exceed → Critical.
- Catalog card omitted from health grid (no Q-07 data).
