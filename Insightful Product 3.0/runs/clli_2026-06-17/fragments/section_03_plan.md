# Section 03 Build Plan — Product Intelligence

Client: Craftmade (clli) · Run date: 2026-06-17 · Confidence tier (§3): **STRONG**

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=54 rows, col=25 rows) | YES |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row, 93.6% complete) | YES |
| 6. New Introduction Performance + Adoption Gap | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows) | YES |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a returns org-level monthly totals only — no item_code, no per-item QoQ; <3 real products with velocity data) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY | PARTIAL (HAS_PORTAL_ORDERS=true AND Q-59 has 16 ITEM rows → renders. BUT no ORG_SUMMARY row and fill_rate_pct="—" for all rows → render Part B backorder table only; org fill-rate metric cards omitted, gap noted) | YES |
| 2. Ghost SKU Registry | CONDITIONAL | MET (Q-ORG-GHOST has 20 rows; top item C102L = $1.23M LTM >> $5K threshold; SIG-ANOMALY-01 family present) | YES |
| 4. Stock-Out Impact Board | CONDITIONAL | MET (Q-ORG-STOCKOUT has 7 rows; SIG-ANOMALY-02 fired, top sellers at 0 available) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
5. Fill Rate & Revenue Impact (RISK)
6. Ghost SKU Registry (RISK)
7. Stock-Out Impact Board (RISK)

## Data-quality notes affecting rendering
- **Q-37**: category_code/collection_code/item_description are "—" for all rows except BW414AG3 and BW321AG3; values are coded (CAT24, COL53). Per Data Presentation Rules, suppress the all-dash Category column; render Item code + description where present. Inventory is 0 available / 0 backorder for nearly all top sellers (these are also the ghost SKUs) — frame as "selling strong, zero catalogued stock position."
- **Q-59**: No ORG_SUMMARY row; fill_rate_pct blank. Cannot state an org fill-rate %. Render the backorder-exposure table (Part B) only; omit Part A metric cards and the "1 in N" ratio claim. Note the org-rate gap in prose, not as a fabricated number.
- **Category/Collection codes** (CAT24, COL234, etc.) are internal codes with no friendly label in the data. Present as "Category CAT24" style sparingly; lead with the descriptive item names that ARE present. Codes are not banned terms but are low-value — keep tables focused on what's legible.
- **Q-ORG-NEWITEM**: only the CAST collection carries should-buy customer data; render a single cross-reference table for CAST.
