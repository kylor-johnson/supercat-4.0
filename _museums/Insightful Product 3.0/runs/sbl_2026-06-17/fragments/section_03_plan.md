# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **PARTIAL** → template `§3-PARTIAL`, label "PARTIAL VIEW".

Key gates: HAS_PORTAL_ORDERS=False, HAS_SALES_DATA=True, HAS_INVENTORY=True, HAS_NEW_ITEMS=True.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | NOT MET (Q-37 returned 0 rows — no item×inventory intersection) | NO |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | NOT MET (Q-39 category + collection both 0 rows) | NO |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| 6. New Introduction Performance & Adoption | MANDATORY (Part B when gate met) | Part A MET (HAS_SALES_DATA=true, Q-42 has 39 rows). Part B NOT MET (HAS_PORTAL_ORDERS=false, Q-61 absent) → Part A only + Q-ORG-NEWITEM cross-ref | YES (Part A) |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a absent, HAS_PORTAL_ORDERS=false) | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=false, Q-59 absent) | NO |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT 0 rows) | NO |

Render order (narrative arc, only those that render): 6 (New Intro — intelligence/opportunity) → 8 (Catalog Completeness — operational health/risk).

Note: Subsections 1 and 6-Part-B are MANDATORY only "when gate met". HAS_PORTAL_ORDERS=false means neither portal-gated subsection renders — correctly skipped, not a defect. Subsection 8 is the only unconditionally-mandatory block and it renders.
