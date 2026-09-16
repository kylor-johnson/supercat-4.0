# Section 03 Build Plan — Product Intelligence

Client: Crystorama (clm) · Run date: 2026-06-17 · Section confidence (§3): **FULL** → `§3-FULL` / "FULL PICTURE"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; 20 rows) | YES |
| What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; 9 category + 25 collection rows) | YES |
| Catalog Completeness (Q-07) | MANDATORY | MET (always; 1 row, 100% complete) | YES |
| New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B when gate met) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true AND Q-61 has 30 rows) | YES |
| Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (all Q-38a rows have blank item_code / "—" descriptions and corrupt future-dated months; <3 real products after filtering) | NO (omit silently) |
| Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true AND Q-59 has 4 rows; ORG_SUMMARY fill_rate=95.70%) | YES |
| Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST row count = 0) | NO |
| Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (10 rows, top sellers at 0 available with customer + alternative data) | YES |

## Narrative arc render order (strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE — operational health)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK — render after positive context)
6. Stock-Out Impact Board (RISK — render late)

## Key derived values
- Fill rate (ORG_SUMMARY): 95.70% → `.badge.ok` (≥95%); units unfilled 7,855; NO <85% alert callout
- Top 10 sellers cumulative LTM revenue: $2.47M; all top 10 at 0 qty_available
- Dominant category CAT1 (Chandeliers): $39.6M, 59.4% of $66.6M category sales, 781 items
- New items launched (Q-42 sum of new_item_count): 919; adopted (Q-61 rows): 30 → 3.3% adoption; zero-traction: 889; adopted revenue (Q-61 sum): ~$151K
- Stock-out board: 10 top sellers at 0 available, top 5 cumulative LTM ~$1.58M; customer + alternative data present
- Catalog: 100% complete (no <90% / <95% callout)
