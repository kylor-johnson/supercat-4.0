# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-07, Q-08, Q-09, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL (any entity >90d stale OR config drift) | MET (Q-08: 11 entities at 301 days stale) | YES |
| Feature Utilization | CONDITIONAL (Q-22 has ≥3 features) | MET (Q-22 has 12+ tracked features, 76 users) | YES |
| Catalog Remediation | CONDITIONAL (completeness <95% OR >50 items missing assets) | MET (visible 144 missing images, hidden 89.9% complete) | YES |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Import Pipeline Detail | CONDITIONAL (pipeline stalled OR irregular) | NOT MET (pipeline healthy & consistent: 189–530/mo, avg ~398/mo) | NO |

## Notes
- §6 uses NO data-confidence header (per shared contract).
- §6 renders as collapsed `<details>` (user must click to expand).
- No section-level what-this-means (per guide).
- MIXPANEL_ORDER_TRACKING_GAP = False → order submission events are real, retained in Feature Utilization.
- Peer benchmark cache files (Q-CI-02/03/05) present in bundle but MUST NOT be read/referenced.

## Badge logic
- Core Pipeline: avg ~398 imports/mo ≥50 → `.badge.ok` "Healthy"
- Data Freshness: 11 entities >90d stale (all at 301d) → >3 Stale → `.badge.danger` "Stale Configs"
- Catalog: visible completeness 95.8% ≥95% → `.badge.ok` (note: 144 visible items missing images)
- Feature Adoption: 12+ active features ≥5 → `.badge.ok` "Active"
- Smart Stacks: count = 5 (>0) → `.badge.ok` "Configured"
