# Section 03 Build Plan — Product Intelligence

Confidence tier (SECTION_CONFIDENCE_3): **FULL** → template `§3-FULL`, label "FULL PICTURE".

Rendering order: strength → intelligence → opportunity → risk.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=12 rows, col=25 rows) | YES |
| Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 1 row, 99.30% complete) | YES |
| New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows) | YES |
| Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a returned 0 rows; <3 products with velocity data) | NO (omit silently) |
| Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 ORG_SUMMARY row present, fill_rate=92.9%) | YES (Part A only — no ITEM rows) |
| Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | MET (20 ghost SKUs; top $60K > $5K threshold) | YES |
| Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (SIG-ANOMALY-02 fired; 16 top sellers at 0 availability) | YES |

Notes:
- Q-59 has only the ORG_SUMMARY row (no ITEM/backorder rows) → render Part A metrics only; fill rate 92.9% ≥ 85% so no `.callout.alert` and no "below target" framing.
- Q-ORG-NEWITEM: all 30 rows have customers_purchased=0 and should_buy_customers="—" → no populated customer cross-reference; render zero-traction callout only, skip cross-reference tables.
- Q-42 per-collection revenue is all $0; new-item revenue metric uses the adopted-item revenue from Q-61 (~$118.7K trailing 12 months).
- Derived: total_new_items=856, adopted_items=30, adoption_rate=3.5%, zero_traction=826.
