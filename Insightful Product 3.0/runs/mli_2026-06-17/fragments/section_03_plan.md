# Section 03 Build Plan — Product Intelligence

Run: mli (Maxim Lighting), 2026-06-17
SECTION_CONFIDENCE_3 = PARTIAL → header template §3-PARTIAL, label "PARTIAL VIEW"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 collection has 25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | Part A conditional / Part B MANDATORY-when-met | Part A MET (HAS_SALES_DATA=true; Q-42 has data). Part B NOT MET (HAS_PORTAL_ORDERS=false AND Q-61 not present) | YES (Part A only) |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (SIG-ANOMALY-02 fired; Q-ORG-STOCKOUT has 9 rows, top sellers at 0 available) | YES |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY-when-gate-met | NOT MET (HAS_PORTAL_ORDERS=false AND Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST has 0 rows) | NO |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a not present; HAS_PORTAL_ORDERS=false) | NO |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE — operational health)
4. New Introduction Performance (INTELLIGENCE/OPPORTUNITY — Part A only, Q-61 gate not met)
5. Stock-Out Impact Board (RISK — render late)

## Notes
- HAS_PORTAL_ORDERS=false suppresses fill-rate, velocity, and adoption-gap (Q-61) arcs → confidence tier PARTIAL.
- Category codes (CAT2…) are internal IDs (banned). Subsection 7 renders the collection breakdown (CHIP/TRIM/RAIL/SPEC/etc. are product-line names) as the primary table; opaque category-code table suppressed.
- Subsection 6 Part B (adoption gap table) NOT rendered — Q-61 absent. Part A self-contained what-this-means.
- Stock-out top_customers populated from Q-ORG-STOCKOUT; no in-collection alternatives available in cache → alternatives column shows "None in cache" badge.
