# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **LIMITED** → header template §3-STRONG with `.limited` class, label "LIMITED VIEW".

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | NOT MET (HAS_SALES_DATA & HAS_INVENTORY true, but Q-37 returned 0 rows — no data) | NO |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | NOT MET (HAS_SALES_DATA true, but Q-39 category & collection both returned 0 rows — no data) | NO |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 data row) | YES |
| 6. New Introduction Performance & Adoption | MANDATORY (Part B) / Part A | Part A MET (HAS_SALES_DATA true, Q-42 has 25 rows). Part B NOT MET (HAS_PORTAL_ORDERS false, Q-61 absent) | YES (Part A only) |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a absent; HAS_PORTAL_ORDERS false) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY | NOT MET (HAS_PORTAL_ORDERS false AND Q-59 absent) | NO |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT 0 rows) | NO |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Catalog Completeness (INTELLIGENCE — operational health)
2. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)

## Notes
- Most data sources empty (no portal orders, sales/category/inventory queries returned 0 rows). LIMITED tier is correct.
- Subsection 6 renders Part A launch metrics only; Part B (Q-61 adoption table) skipped — gate not met. Q-ORG-NEWITEM (30 rows) used for the zero-traction / adoption-gap framing, which is the section's one positive opportunity signal (SIG-OPP-04).
- Catalog completeness = 84% (< 90%) → alert callout fires.
