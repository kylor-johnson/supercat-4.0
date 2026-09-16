# Q-43: Territory Coverage & Dormancy — Crystorama (clm, org_id=64)
- **Query**: Q-43 (Postgres — territory_codes format: JSON array)
- **Period**: Current snapshot
- **Row count**: 60 territories
- **Run date**: 2026-04-20
- **Format detected**: JSON array (used jsonb_array_elements_text)

## Territory-to-Customer Mapping (Top 40)

| territory_code | territory_name | total_assigned_customers |
|---------------|---------------|------------------------|
| C-14 | — | 401 |
| C-18 | — | 387 |
| C-99 | — | 383 |
| C-129 | — | 270 |
| C-155 | — | 243 |
| C-07 | — | 217 |
| C-57 | — | 206 |
| C-26 | — | 188 |
| C-119 | — | 182 |
| C-02 | — | 171 |
| C-55 | — | 168 |
| C-78 | — | 157 |
| C-150 | — | 151 |
| C-32 | — | 145 |
| C-15 | — | 141 |
| C-04 | — | 140 |
| C-25 | — | 127 |
| C-82 | — | 124 |
| C-75 | — | 117 |
| C-95 | — | 90 |
| C-01 | — | 82 |
| C-10 | — | 81 |
| C-60 | — | 71 |
| C-05 | — | 67 |
| C-123 | — | 67 |
| C-83 | — | 65 |
| C-29 | — | 59 |
| C-50 | — | 59 |
| C-54 | — | 46 |
| C-108 | — | 39 |
| C-109 | — | 29 |
| C-98 | — | 8 |
| C-46 | — | 4 |
| C-71 | — | 3 |
| C-08 | — | 3 |
| C-127 | — | 2 |
| C-121 | — | 2 |
| C-126 | — | 2 |
| C- | — | 2 |
| 95 | — | 3 |

**Note**: Territory names are all null — the territories lookup table is not populated for this org. Territory codes are used as identifiers only. Some codes lack the "C-" prefix (e.g., "95", "10") — these appear to be legacy format entries.
