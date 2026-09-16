# Section 03 Build Plan — Product Intelligence

Client: Savoy House Lighting (shl) · Run date: 2026-06-17 · Confidence tier: STRONG

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=33 rows, col=25 rows) | YES |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row, 98.90% complete) | YES |
| 6. New Introduction Performance + Adoption Gap | MANDATORY (Part B when gate met) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows; Q-42 199 rows; Q-ORG-NEWITEM 30 rows) | YES |
| 5. Velocity Signals | CONDITIONAL | NOT MET (Q-38a returned 0 rows) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 ORG_SUMMARY present; no ITEM rows so no backorder table) | YES |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST returned 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | MET (Q-ORG-STOCKOUT has 9 rows, top sellers at 0 available, customer + alternatives populated) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK)
6. Stock-Out Impact Board (RISK)

## Notes
- Confidence tier STRONG → template §3-STRONG, label "STRONG VIEW".
- Fill rate 95.8% → `.badge.ok` (≥95%). No `.callout.alert` (not below 85%). Q-59 has only ORG_SUMMARY row, no ITEM rows → omit Part B backorder table per guide ("Omit ONLY when the file ... contains zero rows").
- Q-37 is the OOS-top-sellers query; all 20 rows show qty_available=0 → render Qty Available as `.badge.danger`.
- New-item total count = 827 (HAS_NEW_ITEMS / new_item_count from gate_flags). Adopted = 30 (Q-61). Adoption ≈ 3.6%. Zero-traction = 797.
- Entity names title-cased; warehouse-channel buyers (Wayfair, Ferguson, Build.com) kept as proper names.
