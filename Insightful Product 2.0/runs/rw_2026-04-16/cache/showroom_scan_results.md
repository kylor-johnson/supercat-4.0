# Showroom / Operational Account Scan
- **Org**: RENWIL (rw, org_id=248)
- **Run date**: 2026-04-16
- **Total excluded accounts**: 1
- **Aggregate excluded GMV**: $313.19

## Pass 1 — Keyword Scan (showroom, admin, marketing, training, test, demo)

| Rep Name | Order Count | GMV | Classification | Evidence |
|----------|-----------|-----|----------------|---------|
| Test Sales Portal | 1 | $313.19 | **Confirmed test account — EXCLUDE** | Name contains "Test"; single order; zero unique customers |

## Pass 2 — Brand-Name Scan ("RENWIL")

No results returned for `rep_first_name ILIKE '%RENWIL%'`.

## Flagged for CSM Review (not excluded from org totals)

| Account | Type | Evidence | Action |
|---------|------|---------|--------|
| torontoshowroom (Mixpanel) | Internal/Showroom user | 293 days_active, 9,387 total_events, 693 submit_order events — 4th highest event volume in org | Flagged — orders remain in total org GMV; high behavioral activity for showroom account |
| TORONTOSHOWROOM / Renwil Showroom (customers table) | Showroom customer record | $296,541 GMV, 17 orders (from Q-13 concentration data) | Flagged — orders remain in total org GMV; significant revenue from internal showroom |

## Exclusion Rules Applied

- "Test Sales Portal" excluded from rep leaderboard (§2) based on: keyword match + zero unique customers + single order pattern
- "torontoshowroom" NOT excluded from rep leaderboard — high activity suggests operational account that genuinely processes customer orders through the showroom; however, its GMV is flagged for CSM awareness
- All flagged accounts' orders remain in total org eCat GMV calculations
