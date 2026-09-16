# Section 06 Build Plan — Platform Context

Client: Arabela Lighting (arl) · Run date: 2026-06-17 · Render mode: collapsed `<details>` · NO confidence header (§6 exempt).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (any of Q-07/08/09/22 has data) | MET — Q-07, Q-08, Q-09, Q-22 all present | YES |
| Operational Alerts (Action Required) | CONDITIONAL (any entity >90d stale OR config drift) | MET — 13 entities stale (12 @ 313d Critical, inventories @ 188d Critical) | YES |
| Feature Utilization | CONDITIONAL (Q-22 has ≥3 features) | MET — Q-22 present, 11 active features | YES |
| Catalog Remediation | CONDITIONAL (completeness <95% OR >50 items missing assets) | NOT MET — Q-07 completeness 99.5%, only 1 item missing image | NO |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL (pipeline stalled OR irregular) | MET — cadence highly irregular (54→7→3→1→22, missing months) | YES |

## Health Dashboard badge decisions
- Core Pipeline: avg ~17/mo (<50) → `.badge.warn` "Low Volume" (recent month=22, not stalled)
- Data Freshness: 13 entities >90d stale (>3) → `.badge.danger` "Critical"
- Catalog: 99.5% (≥95%) → `.badge.ok` "Healthy"
- Feature Adoption: 11 active features (≥5) → `.badge.ok` "Active"
- Smart Stacks card: OMITTED — Q-10 returned 0 rows; no published count available to render honestly.

## Data handling notes
- MIXPANEL_ORDER_TRACKING_GAP = true → "Order Submission" (submit_order=0) removed from Feature Utilization table.
- Peer benchmark cache (Q-CI-*) NOT read/referenced.
- Freshness labels: only Stale/Critical rendered. portal_orders/portal_invoices (96d) and customers (85d) are Monitor → NOT rendered in alerts.
- Feature % denominator = sum of named features (6,389), since total_events (15,214) includes untracked navigation/system events.
