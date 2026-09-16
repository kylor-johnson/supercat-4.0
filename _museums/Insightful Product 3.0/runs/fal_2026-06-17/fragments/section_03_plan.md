# Section 03 Build Plan — Product Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true, Q-59 has 16 data rows) | YES |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST has 0 data rows) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true, HAS_INVENTORY=true) | YES |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (Q-ORG-STOCKOUT has 20 data rows, all top sellers at zero inventory, SIG-ANOMALY-02 fired) | YES |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a returns only aggregate monthly totals with blank item_code — no item-level velocity data; fewer than 3 real products with velocity data) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B, when gate met) | MET (HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-61 has 30 data rows) | YES |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always) | YES |

## Rendering Order (narrative arc)

1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK)
6. Stock-Out Impact Board (RISK)

## Notes

- **Confidence tier**: SECTION_CONFIDENCE_3 = STRONG
- **Q-59**: No ORG_SUMMARY row present — Part A (org fill rate metrics grid) cannot be rendered. Part B (backordered items table) renders normally.
- **Q-38a**: Data is aggregate monthly (blank item_code for all 7 rows). No item-level acceleration/deceleration available. Subsection 5 correctly skipped.
- **Q-ORG-GHOST**: Zero rows. Subsection 2 correctly skipped.
- **Q-37**: All 20 top sellers have qty_available = 0. Cumulative LTM revenue ≈ $2.3M.
- **Q-ORG-STOCKOUT**: All 20 items at zero availability. Customer cross-reference and alternatives data present.
- **Q-ORG-NEWITEM**: 30 rows across collections U (21 items), 3 (6 items), 3-INV (1 item), O (2 items). Customer cross-reference available.
