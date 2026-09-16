# Section 03 Build Plan — Product Intelligence

**Client:** Capital Lighting Fixture Co. (clc) · **Confidence tier (SECTION_CONFIDENCE_3):** STRONG → label "STRONG VIEW"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 has 17 category + 25 collection rows) | YES |
| Catalog Completeness | MANDATORY | MET (always; Q-07 has data — 1,793 visible, 100% complete) | YES |
| New Introduction Performance & Adoption | MANDATORY (Part B when gate met) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows; Q-42 present) | YES |
| Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a returned 0 rows — omit silently) | NO |
| Fill Rate & Revenue Impact | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has ORG_SUMMARY row — fill_rate 92%, 40,270 unfilled). No ITEM rows → Part A only | YES |
| Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST returned 0 rows) | NO |
| Stock-Out Impact Board | CONDITIONAL | MET (SIG-ANOMALY-02 fired ×19; Q-ORG-STOCKOUT has 20 rows; top sellers at 0 avail) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK)
6. Stock-Out Impact Board (RISK)

## Build notes
- Confidence header at top, label "STRONG VIEW" (exact tier from section_confidence).
- Cryptic category/collection codes (CAT3, COL410) are mapped to readable product-type/collection names inferred from item descriptions (Pendants, Chandeliers, Bradford, Delaney, etc.); unmappable minor codes rolled into "Other categories"/"Other collections" per the no-cryptic-codes rule. Category code column dropped from item tables.
- Q-ORG-NEWITEM has 1 row with empty should_buy_customers → no usable customer cross-reference; cross-reference tables omitted.
- Catalog Completeness rendered as a metric block (single data point) per thin-data rule, not a 1-row table.
- total_new_items=186 (gate flag); adopted_items=30 (Q-61); adoption_rate≈16%; zero_traction=156; adopted_revenue≈$1.6M (sum Q-61 revenue) used as new-item revenue (zero-traction items contribute $0).
- Every dollar figure carries a time qualifier (LTM / trailing 12 months). Banned terms avoided.
