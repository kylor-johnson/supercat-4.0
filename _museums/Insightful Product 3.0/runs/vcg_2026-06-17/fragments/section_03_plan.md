# Section 03 Build Plan — Product Intelligence

Client: Visual Comfort Signature (vcg) · Run date 2026-06-17
Section confidence (SECTION_CONFIDENCE_3): **PARTIAL**

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST row_count=0) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=True AND HAS_INVENTORY=True; 20 rows) | YES |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (20 rows; top sellers at zero availability) | YES |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a not present; HAS_PORTAL_ORDERS=False) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | Part B MANDATORY when gate met | Part A MET (HAS_SALES_DATA=True); Part B NOT MET (HAS_PORTAL_ORDERS=False; Q-61 not present) | YES (Part A only) |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=True; category + collection data present) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; 1 row) | YES |

## Render order (narrative arc: strength → intelligence → opportunity → risk)
1. Top Sellers & Inventory Position (STRENGTH)
2. What's Selling — Category & Collection Breakdown (INTELLIGENCE)
3. Catalog Completeness (INTELLIGENCE)
4. New Introduction Performance & Adoption — Part A only (INTELLIGENCE)
5. Stock-Out Impact Board (RISK — render late, customer-relationship lens)

## Data notes
- Confidence tier PARTIAL: no all-channel/digital order data (HAS_PORTAL_ORDERS=False); customer data 49d stale. Header reflects PARTIAL VIEW.
- Q-37: query returns OOS top sellers — all 20 rows show qty_available=0 with scheduled receipt dates. Qty Available rendered with .badge.danger.
- Q-ORG-STOCKOUT: ltm_revenue / ltm_units / qty_on_backorder are "—" for all rows (no dollar exposure available). Customer names present (revenue=None). Alternatives present with availability. Board framed through customer lens per STRATEGIC FRAMING MANDATE; per-customer dollar exposure unavailable → stated in prose note.
- Q-42: 21 collection rows; new_item totals derived. Several collections (COL65, COL44, COL69, COL39, COL74, COL59, COL63, "—") have new items with $0 sales → flagged.
- Q-61 / Q-ORG-NEWITEM not present → Part B (adoption gap) and customer cross-reference omitted.
- Category/collection identifiers are taxonomy codes (CAT#/COL#) with no name map supplied except AERIN; rendered as provided.
