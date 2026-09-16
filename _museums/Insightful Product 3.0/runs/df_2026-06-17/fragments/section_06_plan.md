# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (16 entities >90d stale; 12 at 313d Critical) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, 11+ distinct features tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | MET (Q-09 Low Volume avg ~18/mo, Jun drop to 12, Dec dip to 11 — irregular/low) | YES |

## Notes
- §6 does NOT use a confidence header (per shared contract §2 + guide).
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- No section-level what-this-means (guide: not required for §6).
- MIXPANEL_ORDER_TRACKING_GAP=False → keep order data neutral; submit_order=30 is real, low.
- Smart Stacks card omitted (Q-10 returned 0 rows; never configured).
- Inventory is Fresh (0d) — excluded from stale alerts per 7d override (last sync today).
- Freshness labels in client HTML: Stale (91–180d warn), Critical (181+ danger). Monitor/Fresh not rendered as alerts.
