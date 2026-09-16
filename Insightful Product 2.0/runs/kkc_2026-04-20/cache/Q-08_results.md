# Q-08: Data Freshness Monitor — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-08
- **Source**: Postgres MCP (`user-supercat-postgres-vpn`) — `data_versions` table
- **Run date**: 2026-04-20
- **Rows**: 22

## Results

| Entity Type | Last Updated | Days Since Update | Status |
|-------------|-------------|-------------------|--------|
| matrix_options | 2025-08-07 | 255 | Stale |
| option_groups | 2025-08-07 | 255 | Stale |
| options | 2025-08-07 | 255 | Stale |
| price_levels | 2025-08-07 | 255 | Stale |
| customer_favorites | 2025-08-07 | 255 | Stale |
| contract_prices | 2025-08-07 | 255 | Stale |
| inventories | 2025-08-07 | 255 | Stale |
| kit_items | 2025-08-07 | 255 | Stale |
| commitment_reports | 2025-08-07 | 255 | Stale |
| placement_reports | 2025-08-07 | 255 | Stale |
| riser_prices | 2025-08-07 | 255 | Stale |
| customer_payment_informations | 2025-08-07 | 255 | Stale |
| sales_quotas | 2025-08-07 | 255 | Stale |
| smart_stacks | 2025-10-23 | 179 | Monitor |
| collections | 2025-10-23 | 179 | Monitor |
| groups | 2025-10-23 | 179 | Monitor |
| trade_names | 2025-10-23 | 179 | Monitor |
| portal_orders | 2026-03-13 | 38 | Monitor |
| portal_invoices | 2026-03-13 | 38 | Monitor |
| customers | 2026-03-31 | 20 | Fresh |
| categories | 2026-04-14 | 6 | Fresh |
| products | 2026-04-14 | 6 | Fresh |

**Summary by status**:
- Fresh (≤30 days): 3 entities — products, categories, customers
- Monitor (31–180 days): 6 entities — smart_stacks, collections, groups, trade_names, portal_orders, portal_invoices
- Stale (>180 days): 13 entities — includes inventories, options, price_levels, contract_prices, kit_items, sales_quotas, and others

**Key reactivation flag**: `inventories` is Stale at 255 days. Per Mode 3 rules, this blocks §4 Product & Inventory section even if HAS_INVENTORY were true.
