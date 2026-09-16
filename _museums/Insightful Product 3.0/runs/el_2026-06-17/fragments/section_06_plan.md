# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08/Q-09/Q-10/Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (10 entities stale 301d > 90d in Q-08/Q-11) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 14 active features, ≥3 tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (avg ~2,042 imports/mo, not stalled; recent month partial, not 0) | NO |

## Notes
- §6 uses NO data-confidence header (shared contract §2).
- §6 has NO section-level what-this-means (guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission row in Feature Utilization.
- Health dashboard cards: Core Pipeline (Healthy), Data Freshness (danger, 10 stale), Feature Adoption (ok), Smart Stacks (ok, 11 published). Catalog card omitted (no Q-07).
- SmartPicks opportunity callout: 67 events vs 27,031 product searches.
