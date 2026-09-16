# Q-43: Territory Coverage & Dormancy — Charleston Forge (cfg, org_id=83)
- **Run date**: 2026-04-20
- **Territory format**: JSON array (rep last names as territory codes)
- **Note**: territories table has no matching rows. Territory codes are rep last names, not geographic codes. Case varies (e.g., "swanson" vs "Swanson" vs "SWANSON").

## Step 1 — Customer Base by Territory (top 20)

| Territory Code | Territory Name | Assigned Customers |
|---------------|---------------|-------------------|
| Harrison | — | 233 |
| Linker | — | 174 |
| Gardner | — | 142 |
| Hayes | — | 142 |
| Reece | — | 137 |
| swanson | — | 135 |
| Bowles | — | 128 |
| Swanson | — | 109 |
| Wells | — | 106 |
| Green | — | 105 |
| CFH | — | 97 |
| Feizy | — | 95 |
| Gould | — | 93 |
| hornby | — | 79 |
| HAYES | — | 79 |
| House | — | 71 |
| GREEN | — | 65 |
| Lamb | — | 62 |
| North | — | 56 |
| Broderson | — | 51 |

## Step 3 — Territory Gap Summary (top 30)

| Territory Code | Assigned | eCat Active | Never/Lapsed via eCat |
|---------------|----------|-------------|----------------------|
| Harrison | 233 | 17 | 216 |
| Linker | 174 | 9 | 165 |
| Gardner | 142 | 5 | 137 |
| Hayes | 142 | 10 | 132 |
| swanson | 135 | 12 | 123 |
| Bowles | 128 | 6 | 122 |
| Reece | 137 | 25 | 112 |
| Wells | 106 | 7 | 99 |
| Swanson | 109 | 12 | 97 |
| CFH | 97 | 0 | 97 |
| Green | 105 | 11 | 94 |
| Feizy | 95 | 3 | 92 |
| Gould | 93 | 11 | 82 |
| HAYES | 79 | 5 | 74 |
| House | 71 | 2 | 69 |
| hornby | 79 | 12 | 67 |
| Lamb | 62 | 5 | 57 |
| GREEN | 65 | 9 | 56 |
| North | 56 | 2 | 54 |
| Broderson | 51 | 1 | 50 |
| LINKER | 44 | 4 | 40 |
| WELLS | 48 | 10 | 38 |
| Gerber | 38 | 1 | 37 |
| GARDNER | 34 | 1 | 33 |
| BOWLES | 38 | 8 | 30 |
| KG | 29 | 0 | 29 |
| HOUSE | 29 | 3 | 26 |
| north | 25 | 2 | 23 |
| Hornby | 17 | 0 | 17 |
| house | 17 | 0 | 17 |

**Note**: Territory codes have significant case inconsistency (e.g., "Swanson" / "swanson", "Harrison" / "harrison", "Bowles" / "BOWLES" / "BoWLES"). Case-insensitive deduplication is recommended for Stage 2 analysis.
