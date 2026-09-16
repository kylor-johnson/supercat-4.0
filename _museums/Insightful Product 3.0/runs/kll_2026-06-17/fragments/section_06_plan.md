# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (any data available) | MET (Q-08, Q-09, Q-22 all present) | YES |
| Action Required (Operational Alerts) | CONDITIONAL (entity stale OR config drift) | MET (11 entities at 313d Critical, price_levels 160d Stale) | YES |
| Feature Utilization | CONDITIONAL (Q-22 ≥3 features) | MET (Q-22 present, 14+ tracked features) | YES |
| Catalog Remediation | CONDITIONAL (Q-07 completeness <95% OR >50 items missing assets) | NOT MET (Q-07 not present in bundle — no completeness data) | NO |
| Feature Adoption vs Peers | PERMANENTLY EXCLUDED | EXCLUDED | NO |
| Peer Benchmarking Summary | PERMANENTLY EXCLUDED | EXCLUDED | NO |
| Import Pipeline | CONDITIONAL (pipeline stalled OR irregular) | NOT MET (Q-09 avg ~107/mo, recent month 95, no stall/irregularity) | NO |

## Notes
- §6 uses NO confidence header (per shared contract §2).
- §6 renders as collapsed `<details>` (user must click to expand).
- No section-level what-this-means (guide says not required).
- Catalog card omitted from Health Dashboard: Q-07 absent → no completeness %.
- Smart Stacks: Q-10 smart_stack_count=21, Q-08 smart_stacks Fresh (4d) → `.badge.ok` "Configured".
- Health cards rendered: Core Pipeline, Data Freshness, Feature Adoption, Smart Stacks (4 cards).
- MIXPANEL_ORDER_TRACKING_GAP=False → keep order submission data, no neutral replacement.

## Freshness classification (Q-08, entity overrides applied)
- Critical (181+, .badge.danger): kit_items, contract_prices, customer_favorites, matrix_options, option_groups, options, commitment_reports, placement_reports, riser_prices, customer_payment_informations, sales_quotas — all 313d.
- Stale (91–180, .badge.warn): price_levels 160d.
- Products override (Stale after 30d): products 4d = Fresh → not shown.
- Inventory override (Stale after 7d): inventories 0d = Fresh → not shown.
- Grouped for Action Required: Options/Option Groups/Matrix Options; Pricing (Contract Prices, Riser Prices, Price Levels); Reports (Commitment, Placement); Kit Items; Customer Favorites; Payment Info; Sales Quotas.
