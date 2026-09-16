# Section 03 Build Plan — Product Intelligence

Run: da (Dainolite Ltd.), 2026-06-17
Confidence tier (SECTION_CONFIDENCE_3): **PARTIAL**

Key gate facts: HAS_PORTAL_ORDERS=False, HAS_SALES_DATA=True, HAS_INVENTORY=True,
HAS_NEW_ITEMS=True (new_item_count=220).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | NOT MET (Q-37_results has 0 rows — no data to render) | NO |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | NOT MET (Q-39 category & collection both 0 rows) | NO |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row, 2,244 visible products, 100% complete) | YES |
| 6. New Introduction Performance + Adoption Gap | MANDATORY (Part B) / CONDITIONAL | Part A MET (HAS_SALES_DATA); Part B NOT MET (HAS_PORTAL_ORDERS=false, Q-61 not present) → Part A only | YES (Part A) |
| 5. Velocity Signals | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-38a not present) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=false, Q-59 not present) | NO |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | MET (Q-ORG-STOCKOUT has 20 rows; top sellers at zero availability) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Confidence header (PARTIAL)
2. §8 Catalog Completeness (INTELLIGENCE — operational health, strong: 100%)
3. §6 New Introduction Performance (INTELLIGENCE + OPPORTUNITY — Part A only)
4. §4 Stock-Out Impact Board (RISK — render late)
5. Section-level what-this-means

## Data notes
- Q-ORG-STOCKOUT: ltm_revenue = "—" for ALL 20 rows → suppress Revenue column.
  qty_on_backorder = "—" for ALL rows → suppress Backorder column.
  Customer per-customer revenue all None → list customer names only, no dollars.
  Alternatives (in-stock) populated for most rows → render up to 3.
- Q-42: 220 new items across 7 collections, $0 LTM sales (zero traction).
- Q-ORG-NEWITEM: 30 zero-traction new items (all customers_purchased=0); no
  should_buy_customers data → customer cross-reference table cannot be built.
- Catalog 100% complete → no "below 90%" alert callout.
