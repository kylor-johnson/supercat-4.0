# Section 04 Build Plan — Commerce Patterns

Section ID: commerce · §4 · Confidence tier: STRONG (§4-STRONG / "STRONG VIEW")
Client: Gabby (gh) · Run date: 2026-06-17

Key data facts driving decisions:
- HAS_PORTAL_ORDERS = True; VM45_RENDER = False (Gate1 FAIL: erp_gmv $41.6M < ecat_gmv $50.2M) → render total-business context only for Ordering Share, NO eCat-share-of-total % calc.
- Q-CHANNEL-MIX has channel rows. eCat appears as $0 in the order_origin feed because eCat orders are NOT separately tagged there (they fall into the Rep/ERP-entered bucket). MUST NOT say eCat = $0 or imply non-eCat = manual/offline/non-digital. Render the channel table; position eCat honestly as a channel the origin feed can't yet isolate.
- HAS_CART = False → NO "iPad (rep-submitted) / eCat Online (buyer self-service)" attribution statement. But Q-18-A carries iPad + eCat Online columns over 13 months → Channel Migration renders as an eCat channel split (no share-of-total overlay).
- Q-55: every row ecat_share_change_ppts = 0 (shares ≥100%, partial ERP feed) → NO displacement category → §9 skipped silently (§9B with it).
- Q-60: 20 rows → §10 MANDATORY render. No Q-39 category granularity in this bundle → §10 Part B skipped silently.
- Q-58/Q-58b absent, HAS_COMMITMENT_DATA = False → §11 skipped silently.
- Q-52 present (30 rows), PORTAL_CUSTOMER_DATA_PRESENT = True → §4 Top Buyers enrichment MANDATORY (Total Business + eCat Share columns).
- Q-21 has no monthly time series (only 3 order-type rows); §7 source is Q-21 → §7 Seasonality skipped silently.
- No rep-level AOV / order-count data (Q-18-A is monthly totals; Q-56 has rep GMV but no order counts) → §8 AOV Spread by Rep skipped silently.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true + Q-CHANNEL-MIX rows, no DATA NOTE) | YES |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS). REFRAMED: footprint-as-a-tool, NOT a share-to-grow. VM45_RENDER=false → eCat standalone scale + data-sync prose line; NO adoption-stage ladder | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18-A, 13 months). Part B share suppressed (VM45 denominator invalid) | YES (Part A) |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 + Q-52 enrichment) | YES (enriched) |
| Order Type & Workflow | MANDATORY | MET (Q-21: Confirmed + Quote) | YES |
| Channel Migration | CONDITIONAL | MET (iPad + Online split, 13 months, Q-18-A) | YES |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false, Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-20: 2,954 quotes + 11,504 confirmed) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV/order data) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41: 16 months by channel) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 has no monthly series) | NO |
| Channel Share Opportunity (Displacement) | CONDITIONAL — MANDATORY when gate met | NOT MET (Q-55: no row with total growth + share decline) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL — MANDATORY when gate met | MET (Q-60 rows) | YES |

## Render order (strength → intelligence → opportunity → risk)
0. Order Channel Mix
1. eCat Footprint (footprint-as-a-tool; NOT a share-to-grow)
2. eCat Order Trend
4. Top Buyers & Concentration (enriched)
6. Order Type & Workflow
3. Channel Migration
5. Quote Economics
12. New Buyer Acquisition & Growth
10. Product Mix & Pricing Trends (last, RISK)

## Notes
- VM45_RENDER=false because the all-channel/total-business feed is stale (PORTAL_ORDERS_FRESH=false) and reads lower than eCat. Ordering Share renders total-business context only with the data-synchronization prose line; no share % computed.
- TEST order type (16 orders, $46,758) suppressed as noise; show Confirmed + Quote only.
- WAYFAIR appears twice in Q-60; keep both rows are distinct price-band rows — dedupe to the largest current-quarter row ($608,261) per "one row per account" rule.
- All-caps entity names title-cased per Data Presentation Rules.
- Channel Mix: never state eCat=$0; explain the origin feed doesn't isolate eCat from the rep/back-office bucket.
