# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = FULL → §3-FULL / "Full Picture"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_INVENTORY=false; Q-37 not present) | NO |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat+col data present) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row, 95.6% complete) | YES |
| 6. New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-61 has 30 rows) | YES |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a has only raw monthly qty time-series — no QoQ revenue deltas, no customer attribution; <3 products with the required computed velocity fields) → omit silently | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 ORG_SUMMARY row present, 83.9% fill). No ITEM rows → render Part A only (org metrics + sub-85% alert), no backorder item table | YES |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST 0 rows) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present) | NO |

## Render order (narrative arc strength → intelligence → opportunity → risk)
1. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
2. Catalog Completeness (INTELLIGENCE — operational health)
3. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
4. Fill Rate & Revenue Impact (RISK — fill rate 83.9% < 85% → leads risk block)

## Key data notes
- Q-07: 1,082 visible products, 48 missing images, 0 missing price, 95.6% complete → ≥95%, no sub-90% alert.
- Q-42 (by collection): 954 new items launched, $1.02M LTM sales, 1,382 qty.
- Q-61: 30 high-list-price new items, ALL with 0 buyers / $0 revenue → these are the zero-traction watchlist, NOT top performers. Top-performer table would be all zeros (misleading) → render as high-list-price zero-traction watchlist + count-based zero-traction callout.
- Q-ORG-NEWITEM: 3 real unadopted items (Lilium 10-Light Mobile Pendant COL40; Linea Outdoor Lantern Post Light + Linea Outdoor Flush Mount LINEA) with named collection-active customers (Elegante Interiors, Connecticut Lighting Center, Fadecci Architectural Lighting).
- Q-59: fill rate 83.9% (< 85% → .badge.danger + .callout.alert), 10,506 units unfilled LTM. No ITEM rows.
- Q-39: category codes are internal (CAT1...) → suppress category table; lead with named collections (AXIS, EXOS, HENRY, MASON, AIRIS, ARC, VITRE, CAIRN, LUMA, TORCH, SNAPS). Suppress bare COL### internal codes.
