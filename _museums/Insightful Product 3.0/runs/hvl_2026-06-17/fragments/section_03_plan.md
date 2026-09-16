# Section 03 Build Plan — Product Intelligence

Confidence tier: SECTION_CONFIDENCE_3 = **LIMITED** → §3-STRONG template with `.limited` class, label "LIMITED VIEW".

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 category 12 rows + collection 25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 1 row, 91.9% complete) | YES |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B when gate met) | Part A MET (HAS_SALES_DATA=true, Q-42 108 rows). Part B NOT MET (HAS_PORTAL_ORDERS=false, Q-61 not present) → Part A only | YES (Part A only) |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-38a not present) | NO |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=false; Q-59 not present) | NO (correctly skipped) |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | MET (Q-ORG-GHOST 20 rows; top ghost $134,794 > $5K) | YES |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (Q-ORG-STOCKOUT 20 rows; top sellers at zero inventory per Q-37). Framed via customer lens; ltm_revenue/units blank in cache | YES |

## Narrative arc render order
3 (STRENGTH) → 7 (INTELLIGENCE) → 8 (INTELLIGENCE) → 6 Part A (OPPORTUNITY) → 2 Ghost SKU (RISK) → 4 Stock-Out (RISK)

## Data notes
- All Q-37 items have qty_available=0 and stale receipt dates (2023) — the whole top-seller list is in a stockout posture. Render qty_available=0 with `.badge.danger`, Next Receipt 2023 dates surfaced as overdue/Unknown.
- Category codes (CAT1, CAT8...) and collection codes (COL622, PAIGE...) are raw codes; no human-readable names in cache. Render as given (these are HVL's own internal collection labels, not banned internal IDs like org_id/query IDs).
- Q-ORG-NEWITEM `should_buy_customers` all "—" → no customer cross-reference tables (subsection 6 (iii) omitted).
- Q-ORG-STOCKOUT ltm_revenue/units/qty_on_backorder all "—"; customer revenue all None → render customer names only, no per-customer dollars; alternatives rendered where present.
