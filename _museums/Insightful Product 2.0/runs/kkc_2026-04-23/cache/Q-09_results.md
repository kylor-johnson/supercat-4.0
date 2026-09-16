# Q-09: Import Health & Sync Reliability — Kindel Karges Furniture (kkc, org_id=99)
- **Query ID**: Q-09
- **VM**: VM-09
- **Run date**: 2026-04-23
- **Period**: Last 6 months
- **Rows returned**: 2 (monthly trend) + 10 (recent imports)

## Monthly Import Trend

| Month | Import Count |
|-------|-------------|
| 2026-04 | 41 |
| 2025-10 | 1 |

**Note**: No import activity from November 2025 through March 2026 (5-month gap). Activity resumed strongly in April 2026 with 41 imports.

## Recent Imports (Last 10)

| Created At | Type | Status |
|-----------|------|--------|
| 2026-04-22 23:54 | Images | Warning (sRGB colorspace) + 1 image imported |
| 2026-04-22 23:48 | Images | Clean — 1 image imported |
| 2026-04-22 22:02 | Products | Clean — no errors |
| 2026-04-22 21:58 | Matrix Options | Clean — no errors |
| 2026-04-22 21:56 | Products | Clean — no errors |
| 2026-04-22 21:48 | Matrix Options | Warnings — missing matrix option records for multiple items |
| 2026-04-22 21:43 | Products | Clean — no errors |
| 2026-04-22 21:36 | Matrix Options | Warnings — multiple products missing OptionSet/COM configurations |
| 2026-04-22 21:29 | Products | Clean — no errors |
| 2026-04-22 21:27 | Images | Clean — 1 image imported |

**Error Assessment**:
- No `:error` or `:fatal` entries in recent imports.
- Multiple `:warning` entries related to missing matrix option records and COM option group configurations.
- One sRGB colorspace warning on an image import.
- Import pipeline is active and functional — no failures detected.
