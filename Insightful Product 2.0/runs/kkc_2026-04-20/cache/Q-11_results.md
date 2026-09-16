# Q-11: Configuration Completeness — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-11
- **Source**: Postgres MCP (`user-supercat-postgres-vpn`) — `data_versions`
- **Run date**: 2026-04-20
- **Rows**: 19 (entities stale >30 days)

## Results

| Entity Type | Last Updated | Days Stale | Related Record Count |
|-------------|-------------|------------|---------------------|
| matrix_options | 2025-08-07 | 255 | — |
| option_groups | 2025-08-07 | 255 | — |
| options | 2025-08-07 | 255 | — |
| price_levels | 2025-08-07 | 255 | — |
| customer_favorites | 2025-08-07 | 255 | — |
| contract_prices | 2025-08-07 | 255 | 0 |
| inventories | 2025-08-07 | 255 | — |
| kit_items | 2025-08-07 | 255 | 0 |
| commitment_reports | 2025-08-07 | 255 | — |
| placement_reports | 2025-08-07 | 255 | — |
| riser_prices | 2025-08-07 | 255 | — |
| customer_payment_informations | 2025-08-07 | 255 | — |
| sales_quotas | 2025-08-07 | 255 | 0 |
| smart_stacks | 2025-10-23 | 179 | — |
| collections | 2025-10-23 | 179 | — |
| groups | 2025-10-23 | 179 | — |
| trade_names | 2025-10-23 | 179 | — |
| portal_orders | 2026-03-13 | 38 | — |
| portal_invoices | 2026-03-13 | 38 | — |

**Key findings**:
- sales_quotas: 0 records (no quota configuration)
- kit_items: 0 records (no kits configured)
- contract_prices: 0 records (no contract pricing configured)
- Most configuration entities last updated Aug 7 2025 — 255 days stale (aligned with last active commerce period of Jul 2024 approximately; likely reflects last full data import)
