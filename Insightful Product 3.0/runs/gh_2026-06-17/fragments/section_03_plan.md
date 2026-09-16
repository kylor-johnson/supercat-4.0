# Section 03 Build Plan — Product Intelligence

Section ID: product · Section Number: §3 · Confidence tier: STRONG (§3-STRONG, "STRONG VIEW")

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row, 6,857 products, 56.7% complete) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 27 rows) | YES |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a item descriptions/collections all blank "—"; <3 real products with usable velocity attribution after filtering) | NO (omitted per omission rule) |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has 16 ITEM rows). NOTE: no ORG_SUMMARY row present — Part A org fill-rate % cannot be populated; render Part B backordered-items table only, exclude freight fee rows | YES (Part B) |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST row count = 0) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (SIG-ANOMALY-02 fired; Q-ORG-STOCKOUT has 20 rows, top sellers at 0 available, named customers + alternatives present) | YES |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET for render (Q-39 dimension is internal CAT_/COL_ codes only — no category/collection NAMES and no YoY column; rendering coded rows would expose banned internal IDs) | NO (omitted; concentration described in section close instead) |

## Narrative arc render order (strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. Catalog Completeness (INTELLIGENCE)
3. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY)
4. Fill Rate & Revenue Impact — Part B (RISK)
5. Stock-Out Impact Board (RISK)

## Derived metrics
- Total new items (Q-42 sum new_item_count): 13+2+1+4+6+1+1+27 = 55
- Adopted items (Q-61 rows with buyers>0): 2 (Gaston Counter Stool, Julian Floor Lamp)
- Adoption rate: 2/55 = 3.6%
- Zero-traction count: 55-2 = 53
- Adopted revenue: $8,662 + $4,317 = $12,979 (trailing 12 months)
- Catalog completeness: 56.7%; 2,968 of 6,857 missing images; 0 missing price
- Stock-out board: top 5 by LTM revenue = Strella Cabinet ($366,883), Leary Sideboard - Gray ($322,414), Fitzgerald Sideboard ($297,241), Andrea Dresser ($235,140), Landon Counter Stool - Gold ($205,351). Top-5 combined LTM ≈ $1.43M.
