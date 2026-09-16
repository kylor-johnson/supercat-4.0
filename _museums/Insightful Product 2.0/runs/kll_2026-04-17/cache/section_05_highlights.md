# §5 Commerce Analytics — Highlights
**Client**: Kuzco Lighting Inc. (kll, org_id=166)
**Run date**: 2026-04-17

## Key Metrics (LTM)
- **268 eCat orders**, $887K GMV, $3,310 AOV
- **91,708 all-channel orders**, $70.6M GMV (from business system)
- eCat = **1.3% of total business GMV** (below 5% threshold — capture rate subsection skipped)

## Top Findings

1. **January 2026 breakout**: 78 orders / $403K GMV in a single month — 59 of those were iPad, suggesting a trade show or seasonal ordering event. This one month accounts for 45% of all LTM eCat GMV.

2. **iPad dominates GMV despite near-even order split**: iPad is 48.1% of orders but 83.0% of GMV ($736K). eCat Online leads by count (139 vs 129) but carries only 17% of GMV. iPad AOV ($5,708) is 5.3× eCat Online AOV ($1,085).

3. **HFC + Quote carry half the GMV**: Hold for Confirmation (37 orders) and Quote (28 orders) are just 24.3% of volume but 52.3% of total eCat GMV. HFC AOV is $8,456 — 4.1× the Confirmed average.

4. **Moderate buyer concentration**: Top 5 = 30.7%, Top 10 = 44.6% of eCat GMV. Most top buyers placed 1–4 orders at very high values — concentration is transaction-driven, not repeat-driven.

5. **Massive headroom**: eCat's $887K is 1.3% of the $70.6M total business — significant room for digital channel growth, especially via B2B cart adoption.

## Subsections Rendered
1. eCat Order Trend (Q-18 Part A + Part B total business callout)
2. AOV by Order Segment (Q-20)
3. Ordering Channel Breakdown (Q-18/Q-19 derived, HAS_CART=true)
4. Top Buyers & Concentration (Q-13, with concentration callout — top 5 > 25%)
5. Order Type & Workflow (Q-21)
6. Total Business Context (Q-16, HAS_PORTAL_ORDERS=true)

## Subsections Skipped
- eCat Capture Rate (Q-45) — VM45_RENDER = false; eCat is 1.3% of total business, below 5% interpretability threshold

## Data Notes
- order_origin = 'ECAT' returns 0 for all months — business system does not tag eCat-originated orders
- 1 showroom exclusion ("Kuzco Showroom", 11 orders, $113K) — included in org totals, excluded from rep analysis only
- Q-16 data available through Feb 2026 only (portal_orders sync lag)
