# Section 03 Build Plan — Product Intelligence

Section: §3 Product Intelligence (id: product)
Confidence tier (SECTION_CONFIDENCE_3): PARTIAL → §3-PARTIAL / "PARTIAL VIEW"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (gate flags HAS_SALES_DATA+HAS_INVENTORY true, but Q-37 row count = 0 — no data rows) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (Q-39 category and collection both row count = 0 — no data rows) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (Always; Q-07 has 1 data row) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | CONDITIONAL (Part B MANDATORY when gate met) | NOT MET (Part A: Q-42 row count = 0, HAS_NEW_ITEMS=False; Part B: HAS_PORTAL_ORDERS=False, Q-61 not present) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST row count = 0) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT row count = 0) | NO |

## Notes
- Only Catalog Completeness (Q-07) has renderable data this cycle.
- Q-37/Q-39 gates technically met at the flag level but returned zero data rows — no table can be built; skipped per Data Presentation "handle thin data gracefully" and noted in the confidence header.
- Confidence header: §3-PARTIAL (PARTIAL VIEW). PRODUCT_COUNT = 28,833 visible products (from Q-07).
- Catalog completeness = 0% (every visible product missing a price); fires the <90% alert callout.
- Section-level what-this-means: MANDATORY, present.
