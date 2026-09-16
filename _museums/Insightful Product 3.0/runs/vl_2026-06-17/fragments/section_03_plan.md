# Section 03 Build Plan — Product Intelligence

**Client**: Ciana Varaluz LLC (vl, org_id=147) · Run date 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_3)**: FULL → template `§3-FULL` / label `FULL PICTURE`
**Narrative arc render order**: 3 → 7 → 8 → 6 → (5 omitted) → 1 → (2 omitted) → 4

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown (Q-39) | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=14 rows, col=25 rows) | YES |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| 6. New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY (Part B when gate met) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows) | YES |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (Q-38a returns raw per-month order counts only — no precomputed QoQ acceleration/deceleration; cannot derive reliable velocity deltas without fabrication) | NO (omit silently per guide) |
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has 16 ITEM rows) — note: no ORG_SUMMARY row, so org fill-rate % unavailable; render Part B backorder exposure table | YES |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST returns 0 rows; SIG-ANOMALY-01 did not fire) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | MET (SIG-ANOMALY-02 fired; Q-ORG-STOCKOUT has 10 rows, top sellers at 0 availability) | YES |

**Confidence header**: FULL — placed at top, immediately after wrapper, before first subsection.
**Section-level what-this-means**: present at end.
**Forbidden terms check**: no ERP/Mixpanel/Clicky/platform/health-score in HTML; dollar figures carry time qualifiers.

## Subsections rendered (section-contents list, in render order)
Top Sellers & Inventory Position · What's Selling — Category & Collection · Catalog Completeness · New Introduction Performance & Adoption · Fill Rate & Revenue Impact · Stock-Out Impact Board
