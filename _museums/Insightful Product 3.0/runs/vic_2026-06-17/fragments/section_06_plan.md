# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data available) | MET (Q-08, Q-09, Q-10, Q-22 all present) | YES |
| Action Required | CONDITIONAL (any entity stale OR config drift) | MET (12 entities >90d stale in Q-08; 0 related records for kit_items/contract_prices/sales_quotas in Q-11) | YES |
| Feature Utilization | CONDITIONAL (Q-22 ≥3 features) | MET (Q-22 has 10+ active features tracked) | YES |
| Catalog Remediation | CONDITIONAL (Q-07 completeness <95% OR >50 missing assets) | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL (stalled OR irregular pattern) | MET (recurring "Product not found" inventory import errors — ~80 SKUs rejected every inventory import; Dec dip to 12) | YES |

## Notes
- §6 does NOT carry a data-confidence header (per shared contract §2 and section guide).
- Badge logic:
  - Core Pipeline: avg ≈33 imports/mo (231/7) → `.badge.warn` "Low Volume" (<50/mo, recent month=37 so not Stalled)
  - Data Freshness: 12 entities >90d stale → `.badge.danger`
  - Feature Adoption: 10+ active features → `.badge.ok`
  - Smart Stacks: Q-10 smart_stack_count=6 → `.badge.ok` "Published"
  - Catalog card OMITTED (no Q-07 data)
- MIXPANEL_ORDER_TRACKING_GAP = False → handle Feature Utilization normally (no order-row suppression rule triggered).
- Peer benchmark cache (Q-CI-02/03/05) present in bundle but EXCLUDED — not read, referenced, or rendered.
