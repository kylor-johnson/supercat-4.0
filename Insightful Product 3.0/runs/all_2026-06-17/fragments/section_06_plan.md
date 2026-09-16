# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08/Q-09/Q-07/Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (14 entities Stale at 313d, customers 291d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, >3 features tracked; MIXPANEL_ORDER_TRACKING_GAP=False) | YES |
| Catalog Remediation | CONDITIONAL | MET (completeness 3.8% < 95%; 700 items missing images) | YES |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | MET (cadence notably irregular: 48/2/1/26/6 — near-stalled Mar/Apr) | YES |

## Notes
- §6 does NOT use a data-confidence header.
- Renders as collapsed `<details class="section-collapse" id="platform">`.
- Smart Stacks card: Q-10 returned 0 rows; smart_stacks entity is Fresh (4d) in Q-08 — org has smart stacks. Render an OK card.
- Badge logic:
  - Core Pipeline: avg monthly imports (48+2+1+26+6)/5 = 16.6/mo → <50 → `.badge.warn` "Low Volume" (not <10 stalled overall; recent month=48 healthy).
  - Data Freshness: 14 Stale (>3) → `.badge.danger`.
  - Catalog: 3.8% < 80% → `.badge.danger`.
  - Feature Adoption: 11+ active features (>5) → `.badge.ok`.
  - Smart Stacks: present/fresh → `.badge.ok`.
- MIXPANEL_ORDER_TRACKING_GAP=False, so Order Submission (submit_order=45) stays in feature table.
- Forbidden-term substitutions: use human-friendly entity names (Price Levels, Option Groups, etc.), "the app"/"eCat", no Mixpanel/ERP/portal_orders raw names.
