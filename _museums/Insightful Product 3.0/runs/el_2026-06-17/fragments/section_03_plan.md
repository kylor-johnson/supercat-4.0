# Section 03 Build Plan — Product Intelligence

Client: Eurofase Inc. (el) · Run date: 2026-06-17 · Confidence tier: FULL

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3. Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA=true AND HAS_INVENTORY=true; Q-37 has 20 rows) | YES |
| 7. What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA=true; Q-39 cat=18 rows, col=25 rows) | YES |
| 8. Catalog Completeness | MANDATORY | MET (always; Q-07 has data) | YES |
| 6. New Introduction Performance & Adoption | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS=true AND HAS_NEW_ITEMS=true; Q-61 has 30 rows) | YES |
| 5. Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a has no item-level rows — all item_code blank, <3 real products) | NO (omit silently) |
| 1. Fill Rate & Revenue Impact | MANDATORY | MET (HAS_PORTAL_ORDERS=true; Q-59 has 16 ITEM rows). No ORG_SUMMARY row → render backorder table + risk framing, no fill-rate badge | YES |
| 2. Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST = 0 rows) | NO |
| 4. Stock-Out Impact Board | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT = 0 rows) | NO |

**Confidence header**: SECTION_CONFIDENCE_3 = FULL → template §3-FULL, label "FULL PICTURE". Positioned at top, after summary, before first subsection.

**Render order (narrative arc)**: §3 → §7 → §8 → §6 → [§5 omitted] → §1 → [§2 omitted] → [§4 omitted]

**Derived metrics (New Intro)**: total_new_items=235 (gate_flags HAS_NEW_ITEMS), adopted_items=30 (Q-61), adoption_rate=12.8%, zero_traction=205, adopted_revenue=$288K LTM.

**Notes**:
- Q-59 has no ORG_SUMMARY row and fill_rate_pct is "—" for all items → cannot show a fill-rate %. Render backorder exposure table + risk callout/what-this-means without inventing a fill-rate number.
- Category/collection codes title-cased to readable names (e.g., DECCHANDELIER → Chandeliers).
