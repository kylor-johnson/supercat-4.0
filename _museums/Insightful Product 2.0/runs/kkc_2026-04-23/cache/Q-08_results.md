# Q-08: Data Freshness Monitor — Kindel Karges Furniture (kkc, org_id=99)
- **Query ID**: Q-08
- **VM**: VM-08
- **Run date**: 2026-04-23
- **Period**: Current snapshot
- **Rows returned**: 22

| Entity Type | Last Updated | Days Since Update | Status |
|-------------|-------------|-------------------|--------|
| option_groups | 2025-08-07 | 258 | Stale |
| options | 2025-08-07 | 258 | Stale |
| price_levels | 2025-08-07 | 258 | Stale |
| customer_favorites | 2025-08-07 | 258 | Stale |
| contract_prices | 2025-08-07 | 258 | Stale |
| inventories | 2025-08-07 | 258 | Stale |
| kit_items | 2025-08-07 | 258 | Stale |
| commitment_reports | 2025-08-07 | 258 | Stale |
| placement_reports | 2025-08-07 | 258 | Stale |
| riser_prices | 2025-08-07 | 258 | Stale |
| customer_payment_informations | 2025-08-07 | 258 | Stale |
| sales_quotas | 2025-08-07 | 258 | Stale |
| portal_orders | 2026-03-13 | 40 | Monitor |
| portal_invoices | 2026-03-13 | 40 | Monitor |
| customers | 2026-03-31 | 22 | Fresh |
| matrix_options | 2026-04-22 | 0 | Fresh |
| products | 2026-04-22 | 0 | Fresh |
| collections | 2026-04-22 | 0 | Fresh |
| trade_names | 2026-04-22 | 0 | Fresh |
| categories | 2026-04-22 | 0 | Fresh |
| groups | 2026-04-22 | 0 | Fresh |
| smart_stacks | 2026-04-22 | 0 | Fresh |

**Freshness Summary**:
- **Fresh** (≤30 days): 8 entities — customers, matrix_options, products, collections, trade_names, categories, groups, smart_stacks
- **Monitor** (31–180 days): 2 entities — portal_orders, portal_invoices
- **Stale** (>180 days): 12 entities — option_groups, options, price_levels, customer_favorites, contract_prices, inventories, kit_items, commitment_reports, placement_reports, riser_prices, customer_payment_informations, sales_quotas

**Mode 3 staleness note**: 12 of 22 entities are Stale (>180 days), all last updated on 2025-08-07. This is consistent with a lapsed account — ERP-side configuration data stopped syncing approximately 9 months ago, around the same time as last eCat order activity (July 2024). Product catalog data remains actively maintained (updated today).
