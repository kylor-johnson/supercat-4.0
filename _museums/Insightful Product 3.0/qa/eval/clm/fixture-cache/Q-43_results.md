# Q-43 — Territory Coverage & Dormancy (JSON path, Step 3 gap summary)
- **Query**: Q-43 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `customers` + `orders`
- **Period**: trailing 12 months eCat activity | **Run date**: 2026-06-12
- **Format**: territory_codes stored as JSON array (`["C-14"]`) → JSON path used. `territories` lookup table = 0 rows → territory_name NULL throughout (Step 1 name-join skipped; Step 3 gap summary used).
- Top 25 territories by `never_or_lapsed_via_ecat`.

| territory_code | assigned_customers | ecat_active_customers | never_or_lapsed_via_ecat |
|---|---|---|---|
| C-14 | 407 | 1 | 406 |
| C-18 | 399 | 10 | 389 |
| C-99 | 388 | 0 | 388 |
| C-129 | 272 | 0 | 272 |
| C-155 | 253 | 0 | 253 |
| C-07 | 221 | 0 | 221 |
| C-57 | 210 | 1 | 209 |
| C-26 | 190 | 10 | 180 |
| C-55 | 174 | 0 | 174 |
| C-02 | 173 | 2 | 171 |
| C-119 | 186 | 26 | 160 |
| C-78 | 159 | 3 | 156 |
| C-150 | 157 | 5 | 152 |
| C-32 | 145 | 0 | 145 |
| C-15 | 145 | 3 | 142 |
| C-04 | 138 | 1 | 137 |
| C-25 | 128 | 0 | 128 |
| C-75 | 118 | 3 | 115 |
| C-82 | 128 | 18 | 110 |
| C-95 | 92 | 0 | 92 |
| C-01 | 86 | 3 | 83 |
| C-10 | 83 | 5 | 78 |
| C-123 | 68 | 0 | 68 |
| C-05 | 67 | 0 | 67 |
| C-83 | 66 | 1 | 65 |

**Interpretation**: Very large assigned-but-not-eCat-active gap across territories — customers are assigned to territory codes but order overwhelmingly via non-eCat channels. Territory names unavailable (lookup table empty). Frame as eCat territory activation opportunity, never "these accounts don't buy from you."
