# Q-09 — Import Health

- **Org:** Braxton Culler (bcf, org_id=171)
- **Period:** Last 6 months (trend) + last 10 imports (error check)
- **Rows returned:** 7 (trend) + 10 (recent)
- **Run date:** 2026-04-17

## Monthly Import Trend

| month | import_count |
|---|---|
| 2026-04 | 108 |
| 2026-03 | 151 |
| 2026-02 | 98 |
| 2026-01 | 119 |
| 2025-12 | 111 |
| 2025-11 | 175 |
| 2025-10 | 152 |

## Recent Imports (Error Check)

| created_at | data |
|---|---|
| 2026-04-17 17:11:13 | Sales Data — no errors |
| 2026-04-17 16:10:32 | Portal Invoices — no errors |
| 2026-04-17 16:09:38 | Inventory — **warning: Line 615: Product not found, record ignored., BaseItemCode=0370-61**; Customers — no errors; Portal Orders — no errors |
| 2026-04-16 23:11:13 | Sales Data — no errors |
| 2026-04-16 22:10:27 | Portal Invoices — no errors |
| 2026-04-16 22:09:36 | Inventory — **warning: Line 615: Product not found, record ignored., BaseItemCode=0370-61**; Customers — no errors; Portal Orders — no errors |
| 2026-04-16 17:11:12 | Sales Data — no errors |
| 2026-04-16 16:10:31 | Portal Invoices — no errors |
| 2026-04-16 16:09:10 | Portal Orders — no errors |
| 2026-04-16 16:08:34 | Inventory — no errors; Customers — no errors |
