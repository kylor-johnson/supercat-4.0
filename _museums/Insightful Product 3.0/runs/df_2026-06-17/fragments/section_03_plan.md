# Section 03 Build Plan — Product Intelligence

Run: Designer's Fountain (df), 2026-06-17
Confidence tier (SECTION_CONFIDENCE_3): **PARTIAL** → `§3-PARTIAL` template, label "PARTIAL VIEW"

## Gate evaluation

Data files present: only `Q-07_results.md` (Catalog Completeness). All other Q files report "(not present)".
Key flags: HAS_SALES_DATA=False, HAS_PORTAL_ORDERS=False, HAS_INVENTORY=True, HAS_NEW_ITEMS=True.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST not present) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-37 not present) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY Part B when gate met | NOT MET (HAS_SALES_DATA=False; HAS_PORTAL_ORDERS=False; Q-42/Q-61 not present) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-39 not present) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (Always; Q-07 has 1 data row, 98.70% complete) | YES |

## Rendering notes

- Only subsection 8 (Catalog Completeness) renders. All MANDATORY-when-gate-met
  subsections (1, 6) have unmet gates because HAS_SALES_DATA and HAS_PORTAL_ORDERS
  are both False and the underlying Q files are absent.
- Q-07: visible=1,496 products, missing_images=10, missing_price=9, completeness=98.70%.
  98.70% ≥ 95% → NO `.callout.alert`; positive-toned what-this-means.
- State/Region-style empty columns: none in Q-07.
- Confidence header: PARTIAL VIEW, positioned immediately after section open, before subsection.
- Section-level what-this-means required (max 3 sentences).
- section-contents middot list: only "Catalog completeness".
