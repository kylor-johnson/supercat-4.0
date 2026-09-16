# Q-08 — Data Freshness Monitor
- **Query**: Q-08 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `data_versions` | **Run date**: 2026-06-12
- **Row count**: 22 | Labels: Fresh (≤30d), Monitor (31–180d), Stale (>180d)

| entity_type | last_updated | days_since_update | status |
|---|---|---|---|
| sales_quotas | 2025-08-20 | 296 | Stale |
| customer_payment_informations | 2025-08-20 | 296 | Stale |
| riser_prices | 2025-08-20 | 296 | Stale |
| commitment_reports | 2025-08-20 | 296 | Stale |
| kit_items | 2025-08-20 | 296 | Stale |
| contract_prices | 2025-08-20 | 296 | Stale |
| matrix_options | 2025-08-20 | 296 | Stale |
| option_groups | 2025-08-20 | 296 | Stale |
| options | 2025-08-20 | 296 | Stale |
| price_levels | 2025-11-10 | 214 | Stale |
| placement_reports | 2026-05-05 | 38 | Monitor |
| customers | 2026-06-12 | 0 | Fresh |
| products | 2026-06-12 | 0 | Fresh |
| smart_stacks | 2026-06-12 | 0 | Fresh |
| categories | 2026-06-12 | 0 | Fresh |
| collections | 2026-06-12 | 0 | Fresh |
| groups | 2026-06-12 | 0 | Fresh |
| trade_names | 2026-06-12 | 0 | Fresh |
| customer_favorites | 2026-06-12 | 0 | Fresh |
| portal_orders | 2026-06-12 | 0 | Fresh |
| portal_invoices | 2026-06-12 | 0 | Fresh |
| inventories | 2026-06-12 | 0 | Fresh |

**Note**: Core commerce entities (products, customers, inventories, portal_orders) all Fresh (synced 2026-06-12). Stale entities are unused config tables (kit_items=0, contract_prices=0, options, etc.).
