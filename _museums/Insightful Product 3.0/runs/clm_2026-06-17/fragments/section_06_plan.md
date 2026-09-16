# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-10, Q-22 all have data) | YES |
| Action Required | CONDITIONAL | MET (Q-08 shows 9 entities >90d stale: 8 at 301d, price_levels 219d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 15+ tracked features with usage) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 healthy & consistent: 160–5,584/mo, recent month 205 — not stalled/irregular) | NO |

## Notes
- §6 uses NO confidence header and NO section-level what-this-means (per shared contract §2/§5 and guide).
- Rendered as collapsed `<details class="section-collapse" id="platform">`.
- Q-08 freshness with entity-specific overrides:
  - price_levels (219d) → Critical (.badge.danger) — Products/price-levels stale after 30d
  - options/option_groups/matrix_options (301d) → Critical (.badge.danger)
  - kit_items, contract_prices, sales_quotas (301d) → Critical (.badge.danger, >180d general)
  - riser_prices, commitment_reports, customer_payment_informations (301d) → Critical
  - placement_reports (43d) = Monitor → DO NOT RENDER
  - All inventory/products/customers FRESH (0d) → do not render
- Health dashboard cards (4): Core Pipeline (OK, ~1,046/mo avg), Data Freshness (danger, >3 stale),
  Feature Adoption (OK, ≥5 active), Smart Stacks (OK, 21 published). Catalog card omitted (no Q-07).
- Feature Utilization: submit_order=2 is a tracking artifact (gate note shows order tracking handled
  outside behavioral layer) — remove Order Submission row, do not characterize as non-transactional.
