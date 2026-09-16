# Q-09: Import Health & Sync Reliability
- **Org**: Kaleen Rugs & Broadloom (krb, org_id=244)
- **Period**: Last 6 months
- **Run date**: 2026-04-20

## Monthly Import Trend

| month | import_count |
|-------|-------------|
| 2025-12-01 | 4 |

Note: Only 1 month with imports in the last 6 months. No imports since December 2025 (4+ month gap).

## Recent Imports — Error Check (last 10 events)

Most recent import events are from 2025-12-03. Error analysis:

| created_at | entity | status |
|-----------|--------|--------|
| 2025-12-03 14:48 | Products | Clean (no errors) |
| 2025-12-03 14:26 | Taxonomies | Clean (no errors) |
| 2025-12-03 14:07 | Taxonomies | **ERRORS**: "Line 31: We could not find a Parent with Code: HNB of expected Type: TradeName" |
| 2025-12-03 13:46 | Products | **ERRORS**: Multiple invalid trade name codes ("HAB") — errors on lines 2–6+ |

Import cadence: Imports are not regular. Only 4 imports observed in the last 6 months, all clustered on a single day (2025-12-03). Prior import history exists (345 total import events). Current cadence suggests the data pipeline is dormant.
