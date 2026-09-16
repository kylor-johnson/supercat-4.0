# Section 06 Build Plan — Platform Context

Render mode: collapsed `<details id="platform">`. No data-confidence header (§6 exempt per shared contract). No section-level what-this-means (guide exempts §6).

TARGET STRUCTURE (gold) collapses this section to two data-backed subsections, each a thead/tbody table closing with a what-this-means. Guide governs which content renders; gold governs form. Peer benchmarking (Q-CI-*) is permanently excluded.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status (Health Status Dashboard) | MANDATORY when any data available | MET (Q-08, Q-09, Q-10, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL — any entity >90d stale OR config drift | MET (11 config entities 313d stale = Critical) | YES |
| Feature Utilization | CONDITIONAL — Q-22 ≥3 features tracked | MET (Q-22 present, 10+ features with events) | YES |
| Catalog Remediation | CONDITIONAL — Q-07 completeness <95% OR >50 items missing assets | NOT MET (Q-07 not in bundle; cannot evaluate) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | — | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | — | NO |
| Import Pipeline Detail | CONDITIONAL — stalled or irregular | NOT MET (Q-09 healthy: 51–105/mo, consistent; not stalled) | NO |

## Notes on gold reconciliation
- Gold shows two subsection titles: "Data Freshness" and "Feature Adoption Gaps". The guide's data-backed equivalents are the Health Dashboard + Operational Alerts (freshness) and Feature Utilization. I render the guide's named, data-backed subsections in narrative order (health → alerts → utilization), each matching gold FORM: thead/tbody tables, row-warn/row-danger, what-this-means close.
- MIXPANEL_ORDER_TRACKING_GAP = False → do NOT remove Order Submission from Feature Utilization; the 6,235 submit_order events are real.
- Freshness labels: 313d = Critical (`.badge.danger` / `row-danger`); 95d entities (portal_orders/invoices) = Monitor → DO NOT RENDER.
- Q-10: 40 smart stacks published → Smart Stacks card = `.badge.ok`. Sales portal / online ordering not enabled → not surfaced as a gap (feature-gaps prohibition).
