# Showroom / Operational Account Scan — Interlude Home (ih, org_id=164)
- **Run date**: 2026-04-17
- **Total flagged accounts**: 3
- **Total confirmed exclusions**: 3
- **Aggregate excluded GMV**: $2,627,665.55

## Flagged Accounts

| Rep Name | Order Count | GMV | Classification | Evidence |
|----------|-------------|-----|----------------|----------|
| MIASR2 Miami Showroom | 169 | $1,046,847.07 | Confirmed showroom | "Showroom" in rep_last_name; "Miami" location in name |
| NYSR New York | 243 | $969,641.40 | Confirmed showroom | "NYSR" = New York Showroom abbreviation; "New York" city in rep_last_name; no individual contact name |
| NYSR2 New York | 176 | $611,177.08 | Confirmed showroom | "NYSR2" = second New York Showroom account; "New York" city in rep_last_name; no individual contact name |

## Notes

- Pass 1 (keyword scan) caught: MIASR2 Miami Showroom
- Pass 2 (brand-name scan for "Interlude"): No results
- NYSR and NYSR2 identified from rep leaderboard review — abbreviated showroom names with city in last_name field
- All three accounts are included in total org eCat GMV but excluded from individual rep leaderboard and archetype analysis
- Customer account "Interlude Home Showroom - Miami" (code 146193) also appears in Q-17 dormant list — this is the customer-side record, not the rep-side
