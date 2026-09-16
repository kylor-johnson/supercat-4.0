# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (9 entities stale 313d — Critical >90d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 14 distinct active features) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (no Q-07 catalog completeness data in bundle) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Import Pipeline | CONDITIONAL | MET (cadence irregular + declining 131→19/mo) | YES |

## Notes
- No data confidence header — §6 is exempt per shared contract §2.
- Render as collapsed `<details class="section-collapse" id="platform">`.
- MIXPANEL_ORDER_TRACKING_GAP = False → keep Order Submission in feature table (do not strip).
- Freshness: 9 config/pricing entities at 313d = Critical (181+, `.badge.danger`). 2 entities at 95d = Monitor → DO NOT RENDER. products/inventory fresh (0d).
- Health cards: Core Pipeline (avg 60/mo ≥50 = Healthy w/ slowdown note), Data Freshness (9 stale = danger), Feature Adoption (14 active = ok), Smart Stacks (smart_stacks fresh 0d = ok). No Catalog card (no Q-07).
- Forbidden terms: no ERP, Mixpanel, portal_orders, health score, platform (standalone), segment labels. Use human-friendly entity names.
