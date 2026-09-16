# Q-08: Data Freshness Monitor — Buster & Punch (bp, org_id=250)
- **Query**: Q-08 (VM-08)
- **Period**: Current snapshot
- **Run date**: 2026-04-21
- **Rows returned**: 22
- **Labels**: Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days)

| entity_type | last_updated | days_since_update | status |
|-------------|-------------|-------------------|--------|
| contract_prices | 2025-08-07 | 256 | Stale |
| customer_favorites | 2025-08-07 | 256 | Stale |
| kit_items | 2025-08-07 | 256 | Stale |
| matrix_options | 2025-08-07 | 256 | Stale |
| option_groups | 2025-08-07 | 256 | Stale |
| options | 2025-08-07 | 256 | Stale |
| commitment_reports | 2025-08-07 | 256 | Stale |
| placement_reports | 2025-08-07 | 256 | Stale |
| riser_prices | 2025-08-07 | 256 | Stale |
| customer_payment_informations | 2025-08-07 | 256 | Stale |
| sales_quotas | 2025-08-07 | 256 | Stale |
| products | 2026-01-08 | 102 | Monitor |
| smart_stacks | 2026-01-08 | 102 | Monitor |
| categories | 2026-01-08 | 102 | Monitor |
| collections | 2026-01-08 | 102 | Monitor |
| groups | 2026-01-08 | 102 | Monitor |
| trade_names | 2026-01-08 | 102 | Monitor |
| price_levels | 2026-02-19 | 61 | Monitor |
| portal_orders | 2026-03-13 | 39 | Monitor |
| portal_invoices | 2026-03-13 | 39 | Monitor |
| customers | 2026-04-20 | 0 | Fresh |
| inventories | 2026-04-21 | 0 | Fresh |

**Summary**:
- Fresh: 2 entities (customers, inventories)
- Monitor: 9 entities (products, smart_stacks, categories, collections, groups, trade_names, price_levels, portal_orders, portal_invoices)
- Stale: 11 entities (contract_prices, customer_favorites, kit_items, matrix_options, option_groups, options, commitment_reports, placement_reports, riser_prices, customer_payment_informations, sales_quotas)
