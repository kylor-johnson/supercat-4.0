# Section 03 Build Plan — Product Intelligence

Confidence tier (SECTION_CONFIDENCE_3): **PARTIAL** → template `§3-PARTIAL`, label "PARTIAL VIEW"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-37 not present) | NO |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-39 not present) | NO |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| 6. New Introduction Performance & Adoption | CONDITIONAL (Part B MANDATORY when gate met) | NOT MET (HAS_PORTAL_ORDERS=False, HAS_NEW_ITEMS=False, HAS_SALES_DATA=False; Q-42/Q-61 not present) | NO |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST not present; SIG-ANOMALY-01 not fired) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present; SIG-ANOMALY-02 not fired) | NO |

## Notes

- Data availability is thin: only Q-07 (catalog completeness) has data rows. All
  order-history and inventory-detail queries (Q-37, Q-38a, Q-39, Q-42, Q-59, Q-61,
  Q-ORG-*) are not present because HAS_SALES_DATA and HAS_PORTAL_ORDERS are both False.
- Only ONE subsection (Catalog Completeness) renders. Confidence header carries the
  explanation of the limited view.
- Catalog completeness = 99.80% (2,091 visible products; 5 missing images, 0 missing
  price). ≥95% → positive what-this-means branch; ≥90% → no alert callout.
- Section-level what-this-means is MANDATORY and renders after the subsection.
