# Q-11: Configuration Completeness — Kindel Karges Furniture (kkc, org_id=99)
- **Query ID**: Q-11
- **VM**: VM-11
- **Run date**: 2026-04-23
- **Period**: Entities stale >30 days
- **Rows returned**: 14

| Entity Type | Last Updated | Days Stale | Related Record Count |
|-------------|-------------|------------|---------------------|
| option_groups | 2025-08-07 | 258 | — |
| options | 2025-08-07 | 258 | — |
| price_levels | 2025-08-07 | 258 | — |
| customer_favorites | 2025-08-07 | 258 | — |
| contract_prices | 2025-08-07 | 258 | 0 |
| inventories | 2025-08-07 | 258 | — |
| kit_items | 2025-08-07 | 258 | 0 |
| commitment_reports | 2025-08-07 | 258 | — |
| placement_reports | 2025-08-07 | 258 | — |
| riser_prices | 2025-08-07 | 258 | — |
| customer_payment_informations | 2025-08-07 | 258 | — |
| sales_quotas | 2025-08-07 | 258 | 0 |
| portal_orders | 2026-03-13 | 40 | — |
| portal_invoices | 2026-03-13 | 40 | — |

**Notes**:
- 12 entities share the same last-updated timestamp of 2025-08-07, all 258 days stale.
- contract_prices, kit_items, and sales_quotas all show 0 related records — these are empty/unconfigured entities.
- portal_orders and portal_invoices at 40 days stale (Monitor status) but contain 0 data rows.
