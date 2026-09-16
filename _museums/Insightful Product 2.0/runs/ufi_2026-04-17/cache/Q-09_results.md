# Q-09: Import Health & Sync Reliability — Universal Furniture (ufi, org_id=18)
- **Period**: Last 6 months
- **Run date**: 2026-04-17

## Monthly Import Trend

| Month | Import Count |
|-------|-------------|
| 2026-04 | 85 |
| 2026-03 | 159 |
| 2026-02 | 94 |
| 2026-01 | 104 |
| 2025-12 | 110 |
| 2025-11 | 102 |
| 2025-10 | 61 |

## Recent Imports — Error Check (Last 10)

| Date | Entity | Status |
|------|--------|--------|
| 2026-04-17 11:18 | Products, Inventory, Product Stories | :warning — Products has recurring warnings for unknown price fields (Price_BBD, Price_BBW, Price_BLD, Price_BLW) and missing custom fields (Wood_Finish, Nail_Trim, Cushion_Up, Contrast_Welt, Contrast_Out, Contrast_Seat, Base_Opt, Pillows, Features1, Features2, PlainYardage, POIntroDate). Inventory and Product Stories clean. |
| 2026-04-17 11:17 | Customers | Clean |
| 2026-04-17 08:02 | Sales Data | Clean |
| 2026-04-17 05:09 | Portal Invoices | Clean |
| 2026-04-17 05:08 | Portal Orders | Clean |
| 2026-04-16 11:18 | Products, Inventory, Product Stories | Same warnings as above |
| 2026-04-16 11:17 | Customers | Clean |
| 2026-04-16 08:06 | Images | :information — 4 images imported |
| 2026-04-16 08:04 | Images | :information — 35+ images imported |
| 2026-04-16 08:01 | Sales Data | Clean |

**Interpretation**: Active daily import cadence across all core entities (products, customers, inventory, portal orders, sales data). Recurring product import warnings are cosmetic config issues (unrecognized price fields and missing custom fields) — not data loss errors. No :error or :fatal entries found. Pipeline is healthy.
