# Q-09: Import Health & Sync Reliability — Buster & Punch (bp, org_id=250)
- **Query**: Q-09 (VM-09)
- **Period**: Last 6 months
- **Run date**: 2026-04-21
- **Rows returned**: 7 (monthly trend) + 10 (recent imports)

## Monthly Import Trend

| month | import_count |
|-------|-------------|
| 2026-04 | 15 |
| 2026-03 | 60 |
| 2026-02 | 87 |
| 2026-01 | 99 |
| 2025-12 | 72 |
| 2025-11 | 61 |
| 2025-10 | 20 |

## Recent Imports (Last 10)

| created_at | entity | status |
|------------|--------|--------|
| 2026-04-21 10:31 | Inventory | :warning — Product not found for multiple items (100727, BB-TD-B22-D-GO-B, BB-TD-B22-D-SM-B, BB-TD-B22-ND-GO-B, etc.) |
| 2026-04-20 23:11 | Customers | :warning + :error — Unknown field names (id, recordType, Price Level, Primary Currency, partner_id). Validation error: Shipping address fields blank |
| 2026-04-20 10:11 | Inventory | :warning — Product not found for multiple items (same pattern as above) |
| 2026-04-19 23:10 | Customers | :warning + :error — Same unknown field + validation error pattern |
| 2026-04-19 10:12 | Inventory | :warning — Product not found pattern |
| 2026-04-18 23:13 | Customers | :warning + :error — Same pattern |
| 2026-04-18 10:48 | Inventory | :warning — Product not found pattern |
| 2026-04-17 10:14 | Inventory | :warning — Product not found pattern |
| 2026-04-16 23:16 | Customers | :warning + :error — Same pattern |
| 2026-04-16 10:13 | Inventory | :warning — Product not found pattern |

**Notes**:
- Import cadence: Daily automated imports running (inventory ~daily AM, customers ~daily PM)
- Inventory imports: Recurring :warning — multiple product codes not found in catalog (items exist in ERP but not in eCat product table)
- Customer imports: Recurring :error — validation failures (missing shipping address fields) + :warning for unknown field names in import mapping
- April count (15 so far) is on pace with recent months when extrapolated
