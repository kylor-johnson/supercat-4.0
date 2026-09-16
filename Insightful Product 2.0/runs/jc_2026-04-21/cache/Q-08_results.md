# Q-08: Data Freshness Monitor
- **Org**: Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Period**: Current snapshot
- **Run date**: 2026-04-21
- **Rows returned**: 22

| Entity Type | Last Updated | Days Since Update | Status |
|------------|-------------|-------------------|--------|
| contract_prices | 2025-08-07 | 256 | Stale |
| kit_items | 2025-08-07 | 256 | Stale |
| commitment_reports | 2025-08-07 | 256 | Stale |
| placement_reports | 2025-08-07 | 256 | Stale |
| riser_prices | 2025-08-07 | 256 | Stale |
| customer_payment_informations | 2025-08-07 | 256 | Stale |
| sales_quotas | 2025-08-07 | 256 | Stale |
| price_levels | 2025-11-10 | 162 | Monitor |
| customers | 2026-03-17 | 35 | Monitor |
| portal_orders | 2026-03-17 | 35 | Monitor |
| portal_invoices | 2026-03-17 | 35 | Monitor |
| customer_favorites | 2026-03-17 | 35 | Monitor |
| options | 2026-04-13 | 8 | Fresh |
| option_groups | 2026-04-13 | 8 | Fresh |
| inventories | 2026-04-20 | 1 | Fresh |
| matrix_options | 2026-04-20 | 1 | Fresh |
| products | 2026-04-20 | 1 | Fresh |
| smart_stacks | 2026-04-20 | 1 | Fresh |
| categories | 2026-04-20 | 1 | Fresh |
| collections | 2026-04-20 | 1 | Fresh |
| groups | 2026-04-20 | 1 | Fresh |
| trade_names | 2026-04-20 | 1 | Fresh |

**Summary**: 10 Fresh, 4 Monitor, 8 Stale (but 7 of the Stale entities are ancillary: contract_prices, kit_items, commitment_reports, placement_reports, riser_prices, customer_payment_informations, sales_quotas — all last updated 2025-08-07). Core entities (products, inventories, customers) are Fresh or Monitor.
