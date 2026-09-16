# Section 03 Build Plan — Product Intelligence

Confidence tier (SECTION_CONFIDENCE_3): **PARTIAL** → template `§3-PARTIAL`, label `PARTIAL VIEW`

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST not present; no ghost SKU >$5K) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-37 not present) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B when gate met) | NOT MET (HAS_SALES_DATA=False; HAS_PORTAL_ORDERS=False; Q-42/Q-61 not present) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-39 not present) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 data row, 11,342 visible products, 96.50% complete) | YES |

## Notes
- HAS_SALES_DATA=False and HAS_PORTAL_ORDERS=False suppress every sales/order-dependent subsection. All Q-37/Q-38a/Q-39/Q-42/Q-59/Q-61/Q-ORG-* cache files are "(not present)".
- Mandatory subsections 1 and 6 are correctly skipped: their gates require HAS_PORTAL_ORDERS=true, which is False.
- Only subsection 8 (Catalog Completeness) qualifies. Catalog is 96.50% complete (≥95%), so the "below 90%" alert is suppressed and the strong-shape what-this-means branch applies.
- Confidence header reflects PARTIAL tier — inventory/catalog present, but sales and all-channel order data absent.
- Section-contents middot list lists ONLY Catalog Completeness.
