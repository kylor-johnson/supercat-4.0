# Section 03 Build Plan — Product Intelligence

Section: §3 Product Intelligence (id: product)
Confidence Tier: SECTION_CONFIDENCE_3 = PARTIAL → §3-PARTIAL header, "PARTIAL VIEW" label

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=14 rows, col=25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has data, 96.30% complete) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | Part A CONDITIONAL / Part B MANDATORY-when-gate-met | Part A MET (HAS_SALES_DATA=true; Q-42 has 19 rows). Part B NOT MET (HAS_PORTAL_ORDERS=false AND Q-61 not present). Q-ORG-NEWITEM cross-ref MET (30 rows) | YES (Part A + customer cross-ref only) |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-38a not present) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=false AND Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST = 0 rows) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (SIG-ANOMALY-02 P0 fired; Q-ORG-STOCKOUT=11 rows; top sellers at zero availability) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE — operational health)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY, Part A + cross-ref)
5. Stock-Out Impact Board (RISK)

## Notes
- Confidence header MANDATORY at top → §3-PARTIAL.
- No YoY/prior-share data in Q-39 → Part C "Significant Mix Shifts" NOT rendered (gate not met).
- Category/collection identifiers are opaque internal codes (CAT11, COL83) with no name map in cache; rendered as provided.
- Section-level what-this-means MANDATORY after all subsections.
