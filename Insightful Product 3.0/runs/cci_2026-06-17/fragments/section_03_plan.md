# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **FULL** → template `§3-FULL` / label "FULL PICTURE"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=37 rows, col=12 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 2 rows) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows) | YES |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a is raw monthly time-series with no computed QoQ acceleration/deceleration; <3 real products with meaningful pre-computed velocity signal — omission rule applies) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 ORG_SUMMARY row present, fill_rate=81.7%) — Part A only; no ITEM rows so backorder table omitted | YES |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST has 0 rows) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (Q-ORG-STOCKOUT has 20 rows; top sellers at zero availability) | YES |

## Narrative arc render order
3 (STRENGTH) → 7 (INTELLIGENCE) → 8 (INTELLIGENCE) → 6 (INTELLIGENCE+OPPORTUNITY) → 1 (RISK) → 4 (RISK)

## Notes
- Q-59 has only an ORG_SUMMARY row (no ITEM backorder rows) → render Part A metrics + alert callout; skip Part B backorder table.
- Q-37: all 20 rows show qty_available=0 (OOS top sellers) — render with danger badges on Qty Available.
- Q-ORG-STOCKOUT: customer revenue is null; alternatives present for one item only. Frame through customer-relationship lens.
- Q-ORG-NEWITEM: Bunny Williams collection has 3 unadopted Wander cordless table lamps with deep collection buyers — cross-reference table.
