# Section 03 Build Plan — Product Intelligence

**Client**: Buster & Punch (bp, org_id=250) · **Run date**: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_3)**: PARTIAL → template `§3-PARTIAL`, label "Partial View"

## Gate Inputs (from gate_flags.md)
- HAS_INVENTORY = True
- HAS_SALES_DATA = False
- HAS_PORTAL_ORDERS = False
- HAS_NEW_ITEMS = False
- HAS_CART = False

## Cache Data Availability
- Q-07 (Catalog Completeness): PRESENT — 1 row (visible: 2,362 products; 495 missing images; 1,237 missing price; 43.80% complete)
- Q-37, Q-38a, Q-39 (cat/coll), Q-42, Q-59, Q-61, Q-ORG-GHOST, Q-ORG-STOCKOUT, Q-ORG-NEWITEM: ALL not present

## Subsection Gate Table

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=False AND Q-59 absent) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST absent) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False, Q-37 absent) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT absent) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False, Q-38a absent) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B when gate met) | NOT MET (HAS_SALES_DATA=False, HAS_PORTAL_ORDERS=False, HAS_NEW_ITEMS=False, Q-42/Q-61 absent) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False, Q-39 absent) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY (always) | MET (Q-07 present, 1 row) | YES |

## Render Decision
Only **Catalog Completeness (Q-07)** renders. Sales-dependent and portal-order-dependent
subsections are correctly skipped — this org has inventory + catalog data but no sales/
portal-order data (engagement-mode org). The PARTIAL confidence header explains the scope.

Completeness is 43.80% (< 90%) → the `.callout.alert` "Catalog Below 90% Complete" fires,
and the `< 95%` branch of the what-this-means copy is used.

Section-level `.what-this-means` (MANDATORY) closes the section.
