# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **FULL** → template `§3-FULL`, label "FULL PICTURE"

Render order (narrative arc): Intelligence (Catalog) → Opportunity (New Intro Adoption) → Risk (Backorder Exposure).
Note: STRENGTH subsections (Top Sellers, Category/Collection) are gated on HAS_SALES_DATA=false and their cache files are absent, so they do not render. Surviving subsections render in arc order: intelligence → opportunity → risk.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true AND Q-61 has 30 rows). Part A Q-42 absent → use new_item_count=556 from gate flags for total; no Q-ORG-NEWITEM so no collection cross-reference | YES (Part B) |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true AND Q-59 has 16 ITEM rows). No ORG_SUMMARY row → no org fill-rate metric cards; render Part B backorder exposure table only | YES (Part B) |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST absent) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=false; Q-37 absent) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT absent) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a 0 rows) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=false; Q-39 absent) | NO |

## Derived metrics for subsection 6
- total_new_items = 556 (new_item_count from gate flags; Q-42 absent)
- adopted_items = 30 (Q-61 row count)
- adoption_rate = 30/556 = 5.4%
- zero_traction_count = 556 - 30 = 526
- adopted_revenue = sum of Q-61 revenue column ≈ $652K LTM

## Subsection 1 (Q-59) note
- No ORG_SUMMARY row present; all fill_rate_pct / total_unfilled = "—". Skip Part A metric cards and fill-rate badge. Render Part B backorder exposure table + risk callout + what-this-means framed on backorder exposure, not org fill rate.
- Top exposure item: Hudson LED Wall/Vanity (WS3313), $121,753.60 exposure.

## Catalog completeness (Q-07) note
- completeness_pct = 0 (missing_price = 6,381 for all visible products). Below 90% → render alert callout. Single visibility row (visible). Cross-reference platform section per guide.
