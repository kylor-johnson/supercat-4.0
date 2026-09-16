# Q-09: Import Health & Sync Reliability
- **Query ID**: Q-09 (VM-09)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Period**: Trailing 6 months
- **Row count**: 7 (monthly trend) + 10 (recent imports)
- **Run date**: 2026-04-16
- **Exclusions**: None

## Monthly Import Trend

| Month | Import Count |
|-------|-------------|
| 2026-04 | 233 |
| 2026-03 | 448 |
| 2026-02 | 357 |
| 2026-01 | 361 |
| 2025-12 | 589 |
| 2025-11 | 403 |
| 2025-10 | 259 |

## Recent Imports (Latest 10)

| Date | Entity | Errors |
|------|--------|--------|
| 2026-04-17 02:10 | Product Stories | None |
| 2026-04-17 02:09 | Portal Invoices | None |
| 2026-04-17 01:16 | Inventory | Warnings only — ~200+ "Product not found, record ignored" entries (item codes in inventory file not matching products table). No :error or :fatal. |
| 2026-04-16 23:36 | Portal Orders | None |
| 2026-04-16 20:13 | Customers | None |
| 2026-04-16 18:16 | Customers | None |
| 2026-04-16 17:10 | Sales Data | None |
| 2026-04-16 16:12 | Customers | None |
| 2026-04-16 14:20 | Customers | None |
| 2026-04-16 13:45 | Portal Orders | None |
