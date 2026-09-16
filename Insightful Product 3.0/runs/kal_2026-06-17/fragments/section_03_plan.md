# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **FULL** → template `§3-FULL`, label "FULL PICTURE".

Rendered in narrative-arc order (strength → intelligence → opportunity → risk).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 collection + category data present) | YES |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 2 rows) | YES |
| 6. New Introduction Performance + Adoption Gap | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows; Q-ORG-NEWITEM has 30 rows) | YES |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a provides only raw monthly units; no precomputed QoQ deltas or customer attribution; omission rule — silently omit) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has 16 ITEM rows). NOTE: no ORG_SUMMARY row and fill_rate_pct is "—"; render backorder-exposure table + handle missing org fill rate gracefully | YES |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST = 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | MET (Q-ORG-STOCKOUT has 8 rows; top sellers at zero availability) | YES |

Notes:
- Category codes (CAT1, CAT2, …) are internal codes with no name mapping in the bundle → forbidden as bare internal IDs. §7 is built on the Collection breakdown (real product-line names: Flint, Roxy, Samal, Glacier-line, etc.); category-code-only table suppressed.
- Q-59 has no fill_rate_pct value, so the Part A fill-rate metric card / <85% callout cannot be populated; subsection focuses on the backorder-exposure table with a graceful note. The confidence header notes order-level fill-rate detail was not returned.
- Section-level what-this-means rendered after all subsections.
