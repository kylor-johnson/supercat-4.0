# Section 03 Build Plan — Product Intelligence

Confidence tier: **FULL** (SECTION_CONFIDENCE_3) → §3-FULL template, "FULL PICTURE" label.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA + HAS_INVENTORY true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA true; Q-39 cat=23 rows, col=25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row, completeness 0%) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS + HAS_NEW_ITEMS true; Q-61 has 30 rows) | YES |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a returned 0 rows) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS true; Q-59 ORG_SUMMARY row present) | YES (Part A only — fill rate 100%, no backorder items) |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST returned 0 rows) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT returned 0 rows) | NO |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE — operational health)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK — but fill rate is 100%, rendered as healthy)

## Key derived numbers
- Total new items (Q-42 sum new_item_count) = 115; adopted (Q-61 rows) = 30; adoption rate = 26%; zero-traction = 85; adopted revenue = $120,494 LTM
- Q-37 top 10 LTM revenue = $646,461; ALL top sellers at zero qty available
- Fill rate = 100%, 0 units unfilled
- Catalog completeness = 0% (1,112 visible products, all missing price level)
- Dominant category: OW (Outdoor Wall) and CL tied at ~$2.6M

## Notes
- Q-37 / Q-39 / Q-42 use category & collection CODES with no name mapping in cache. Codes shown as-is in Category column; item descriptions title-cased where present, item code used as identifier where description is "—".
- Suppress Category/Collection columns in Q-37 where every visible top-10 row is "—".
- Catalog completeness: do NOT recommend operational "upload price" steps — cross-reference Platform section per guide.
