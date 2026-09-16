# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (12 entities at 313d Critical; customers 148d, portal_orders/invoices 96d Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, >3 distinct features tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle; no completeness data to gate on) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 shows consistent 2-6/mo cadence, no stall, recent month=5 non-zero; low-volume but steady — no story worth telling) | NO |

## Notes
- §6 uses NO data-confidence header (per shared contract §2).
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- MIXPANEL_ORDER_TRACKING_GAP = False → no special order-submission suppression needed; submit_order=232 is real.
- Entity-specific staleness overrides: 313d entities = Critical (.badge.danger); customers 148d, portal_orders/invoices 96d = Stale (.badge.warn).
- Health badges: Core Pipeline = Low Volume (avg ~4.5/mo <50); Data Freshness = Stalled/danger (>3 stale = 14 stale entities); Catalog/Feature = from Q-22 (4 active high-value features → warn). Smart Stacks fresh (1d) → ok.
- Peer/Q-CI cache files NOT read (excluded).
