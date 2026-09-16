# Q-08: Data Freshness Monitor
- **Org**: Currey & Company (cci), org_id=161
- **Source**: Postgres MCP (data_versions)
- **Row count**: 22 entity types
- **Run date**: 2026-04-17

| entity_type | last_updated | days_since_update | status |
|-------------|-------------|-------------------|--------|
| price_levels | 2025-08-20 | 240 | Stale |
| collections | 2025-08-20 | 240 | Stale |
| trade_names | 2025-08-20 | 240 | Stale |
| contract_prices | 2025-08-20 | 240 | Stale |
| kit_items | 2025-08-20 | 240 | Stale |
| matrix_options | 2025-08-20 | 240 | Stale |
| option_groups | 2025-08-20 | 240 | Stale |
| options | 2025-08-20 | 240 | Stale |
| commitment_reports | 2025-08-20 | 240 | Stale |
| riser_prices | 2025-08-20 | 240 | Stale |
| sales_quotas | 2025-08-20 | 240 | Stale |
| categories | 2026-04-08 | 9 | Fresh |
| groups | 2026-04-08 | 9 | Fresh |
| placement_reports | 2026-04-15 | 2 | Fresh |
| customer_payment_informations | 2026-04-17 | 0 | Fresh |
| customers | 2026-04-17 | 0 | Fresh |
| customer_favorites | 2026-04-17 | 0 | Fresh |
| portal_orders | 2026-04-17 | 0 | Fresh |
| portal_invoices | 2026-04-17 | 0 | Fresh |
| products | 2026-04-17 | 0 | Fresh |
| smart_stacks | 2026-04-17 | 0 | Fresh |
| inventories | 2026-04-17 | 0 | Fresh |

**Summary**: 11 entities Stale (>180 days — all from 2025-08-20 batch), 0 Monitor, 11 entities Fresh (≤30 days). Core commerce entities (products, customers, inventories, portal_orders) are all Fresh (updated today).
