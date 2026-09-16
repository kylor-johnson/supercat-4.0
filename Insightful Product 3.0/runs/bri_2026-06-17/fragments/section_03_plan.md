# Section 03 Build Plan — Product Intelligence

**Client:** Bulbrite (bri, org_id 222) · **Run date:** 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_3):** STRONG → template `§3-STRONG`, label "Strong View"

## Gate inputs
- HAS_PORTAL_ORDERS = True
- HAS_SALES_DATA = True
- HAS_INVENTORY = True
- HAS_NEW_ITEMS = True (new_item_count = 179)

## Subsection manifest (rendered in narrative-arc order: Strength → Intelligence → Opportunity → Risk)

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Top Sellers & Inventory Position | CONDITIONAL | MET (HAS_SALES_DATA + HAS_INVENTORY both true; Q-37 has 20 rows) | YES |
| What's Selling — Category & Collection Breakdown | CONDITIONAL | MET (HAS_SALES_DATA true; Q-39 has 31 category + 6 collection rows) | YES |
| Catalog Completeness | MANDATORY | MET (always; Q-07 has 1 row) | YES |
| New Introduction Performance & Adoption | MANDATORY (Part B) | MET (HAS_PORTAL_ORDERS + HAS_NEW_ITEMS true; Q-61 has 30 rows) | YES |
| Item Velocity Signals | CONDITIONAL | NOT MET (Q-38a has 0 rows; <3 products with velocity data → omit silently) | NO |
| Fill Rate & Revenue Impact | MANDATORY | MET (HAS_PORTAL_ORDERS true; Q-59 has 1 ORG_SUMMARY row, fill rate 99.4%) | YES |
| Ghost SKU Registry | CONDITIONAL | NOT MET (Q-ORG-GHOST has 0 rows) | NO |
| Stock-Out Impact Board | CONDITIONAL | MET (SIG-ANOMALY-02 fired; Q-ORG-STOCKOUT has 6 rows, top sellers at zero availability) | YES |

## Rendered subsection order (final)
1. Top Sellers & Inventory Position (Q-37) — STRENGTH
2. What's Selling — Category & Collection Breakdown (Q-39) — INTELLIGENCE
3. Catalog Completeness (Q-07) — INTELLIGENCE
4. New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) — INTELLIGENCE + OPPORTUNITY
5. Fill Rate & Revenue Impact (Q-59) — RISK
6. Stock-Out Impact Board (Q-ORG-STOCKOUT) — RISK
+ Section-level what-this-means

## Key data decisions
- **Total new items = 179** (gate flag `new_item_count`). Q-42's `new_item_count` column (1,115 / 3,523) is implausible vs. an 896-product catalog and conflicts with the gate flag — treated as corrupted; gate flag used.
- **New-item revenue = $1.48M** (sum of Q-61 `revenue`, the only verifiable figure; zero-traction items generate $0).
- Adoption: 30 adopted / 179 total = **17%**; **149 zero-traction**.
- Q-37 returns OOS top sellers — every row has qty_available = 0; Backorder column suppressed (all 0).
- Stock-Out alternatives column dropped (no in-stock substitute data in cache) → prose note instead. Customer impact populated from `top_customers`.
- Fill rate 99.4% ≥ 95% → badge ok, no alert callout, no Part B item table (Q-59 has no ITEM rows).
- Catalog completeness 99.2% ≥ 95% → positive what-this-means, no alert.
- Next-receipt date `2040-4-4` and `—` treated as "Unknown" (badge warn).
