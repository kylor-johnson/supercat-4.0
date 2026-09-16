# Section 03 Build Plan — Product Intelligence

Confidence tier (SECTION_CONFIDENCE_3): **FULL** → §3-FULL template, "FULL PICTURE" label.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=35 rows, col=25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row, 98.2% complete) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | CONDITIONAL (Part B MANDATORY when gate met) | NOT MET (HAS_NEW_ITEMS=False; Q-42=0 rows; Q-61 not present) | NO |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a descriptions blank; <3 real products with meaningful QoQ velocity + attribution after filtering fee items — omit silently) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has 16 ITEM rows). NOTE: no ORG_SUMMARY row, fill_rate_pct="—" → Part A org-rate metrics unavailable; render Part B backordered-items table with relationship framing. Filter fee item "DSC — Tariff Prepaid". | YES |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST=0 rows) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (Q-ORG-STOCKOUT=20 rows; top sellers at 0 available; SIG-ANOMALY-02 fired P0 x20) | YES |

Render order (strength → intelligence → opportunity → risk):
1. Top Sellers & Inventory Position
2. What's Selling — Category & Collection Breakdown
3. Catalog Completeness
4. Fill Rate & Revenue Impact
5. Stock-Out Impact Board
