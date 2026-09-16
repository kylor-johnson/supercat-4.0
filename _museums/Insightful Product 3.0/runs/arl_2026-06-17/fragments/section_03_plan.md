# Section 03 Build Plan — Product Intelligence

**Client**: Arabela Lighting (arl) · Run date: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_3)**: PARTIAL → `§3-PARTIAL` template, label `PARTIAL VIEW`

## Gate inputs
- HAS_PORTAL_ORDERS = False
- HAS_SALES_DATA = False
- HAS_INVENTORY = True
- HAS_NEW_ITEMS = True
- Data present: Q-07 only (196 visible products, 1 missing image, 0 missing price, 99.50% complete)
- All other Q-files (Q-37, Q-38a, Q-39, Q-42, Q-59, Q-61, Q-ORG-GHOST, Q-ORG-STOCKOUT, Q-ORG-NEWITEM) = not present
- No P0/P1 product signals fired (Product not in signal density table)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | NOT MET (HAS_PORTAL_ORDERS=false; Q-59 absent) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (SIG-ANOMALY-01 not fired; Q-ORG-GHOST absent) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=false; Q-37 absent) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (SIG-ANOMALY-02 not fired; Q-ORG-STOCKOUT absent) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-38a absent) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY when Q-61 gate met | NOT MET (HAS_PORTAL_ORDERS=false; HAS_SALES_DATA=false; Q-42/Q-61 absent) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=false; Q-39 absent) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 data row) | YES |

## Render summary
- Confidence header (PARTIAL VIEW) — MANDATORY, at top
- 1 subsection renders: **Catalog Completeness**
- Section-level what-this-means — MANDATORY
- section-contents middot list = "Catalog completeness" only
