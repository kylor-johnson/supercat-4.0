# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-07, Q-08, Q-09, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (price_levels 183d Critical; products/smart_stacks/categories/collections/groups/trade_names 126d Stale; portal/invoices 96d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 12+ tracked features with usage; MIXPANEL_ORDER_TRACKING_GAP=False so keep Order Submission) | YES |
| Catalog Remediation | CONDITIONAL | MET (98.6% complete is ≥95%, BUT 58 items missing images > 50 threshold) | YES |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | n/a | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | n/a | NO |
| Import Pipeline | CONDITIONAL | MET (cadence irregular — 125 imports Dec 2025 collapsed to 5/3/4/11/5 since; notable story) | YES |

## Notes
- §6 does NOT use a data-confidence header (per shared contract §2).
- §6 renders as collapsed `<details>`.
- No section-level what-this-means (per guide).
- Smart Stacks health card OMITTED: Q-10 (Feature Enablement) returned 0 rows; no published smart-stack count available.
- Badge logic:
  - Core Pipeline: recent months avg < 10/mo (5,3,4,11,5) → Stalled / danger.
  - Data Freshness: >3 stale entities (>90d) → danger.
  - Catalog: 98.6% ≥95% → ok.
  - Feature Adoption: ≥5 active features → ok.
- Q-CI-* peer files EXCLUDED — not read/referenced.
