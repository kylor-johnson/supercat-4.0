# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (Q-08 shows 10 entities at 313d, Critical) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 13 active features; ≥3 tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present — completeness cannot be evaluated) | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 healthy/consistent 87–166/mo, no stalled month) | NO |

## Notes
- §6 uses NO data-confidence header (per shared contract §2 and §3).
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- Health cards: Core Pipeline (avg ~105/mo → Healthy/ok); Data Freshness (10 entities >180d → danger); Feature Adoption (13 active → ok); Smart Stacks (Q-10 returned 0 rows → muted "Not configured").
- Catalog card omitted from dashboard — Q-07 (catalog completeness) not present in bundle.
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in feature table.
- Peer benchmark cache files (Q-CI-*) deliberately NOT used.
