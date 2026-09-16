# Section 03 Build Plan — Product Intelligence

**Client**: EGLO Canada (eglo_can) · **Run date**: 2026-06-17
**Section confidence (SECTION_CONFIDENCE_3)**: PARTIAL → template `§3-PARTIAL` / label "PARTIAL VIEW"

## Gate Inputs
- HAS_SALES_DATA = True
- HAS_INVENTORY = True
- HAS_PORTAL_ORDERS = False
- HAS_NEW_ITEMS = True
- SIG-ANOMALY-01 (Ghost SKU) = not fired (Q-ORG-GHOST 0 rows)
- SIG-ANOMALY-02 (Stock-Out) = fired (12 P0 stock-out signals; Q-ORG-STOCKOUT 20 rows)

## Subsection Render Decisions (narrative arc order)

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA AND HAS_INVENTORY both true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA true; Q-39 cat+col present) | YES |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has data) | YES |
| 6. New Introduction Performance & Adoption (Part A only) | Part A CONDITIONAL / Part B MANDATORY-when-gate | Part A MET (HAS_SALES_DATA; Q-42 present). Part B NOT MET (HAS_PORTAL_ORDERS=false AND Q-61 absent) | YES (Part A only) |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-38a not present) — omit silently | NO |
| 1. Fill Rate & Revenue Impact | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=false; Q-59 absent) | NO |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST 0 rows; SIG-ANOMALY-01 not fired) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | MET (SIG-ANOMALY-02 fired; Q-ORG-STOCKOUT 20 rows; top sellers at 0 avail) | YES |

## Render order in fragment (strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption (INTELLIGENCE + OPPORTUNITY, Part A only)
5. Stock-Out Impact Board (RISK)

## Notes
- Confidence header: PARTIAL VIEW, placed at top before first subsection.
- Q-37: all 20 rows have qty_available=0 (OOS-top-sellers query) — render with `.badge.danger` on Qty Available, "Unknown" on Next Receipt.
- Q-ORG-NEWITEM (30 rows) cross-reference requires Q-61 gate (not met). Part B and its collection cross-reference tables are correctly skipped.
- Category/Collection codes are raw (CAT12, COL804) — no name mapping in bundle; render codes as labels, descriptions title-cased.
- Section-level what-this-means present at end.
