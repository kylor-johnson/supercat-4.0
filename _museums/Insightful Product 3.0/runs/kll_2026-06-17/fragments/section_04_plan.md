# Section 04 Build Plan — Commerce Patterns

**Client**: Kuzco Lighting Inc. (kll) · Run date: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4)**: STRONG → template `§4-STRONG`, label "STRONG VIEW"

## Key gates
- HAS_PORTAL_ORDERS = true · PORTAL_CUSTOMER_DATA_PRESENT = true · HAS_CART = true · HAS_INVENTORY = true
- VM45_RENDER = false → no eCat-ordering-share % calc (denominator gate failed); total-business context only
- Q-CHANNEL-MIX has DATA NOTE (100% Rep/ERP-entered) → Order Channel Mix renders as honest prose paragraph, NOT a table
- HAS_COMMITMENT_DATA = false → §11 skipped
- PORTAL_REP_DATA_PRESENT = false → §9 Part B skipped; §8 AOV-by-rep has no rep data
- Q-55 displacement: NO row has total_growth>0 AND ecat_share_change<0 (all eCat shares = 0/0) → §9 skipped silently (no false alarm)
- Q-60: 20 rows → §10 Price Erosion MANDATORY
- Q-52: 30 rows → §4 enrichment MANDATORY

## Subsection render decisions (narrative-arc order, per updated §4 guide)

| Subsection (exact name from guide) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL (render FIRST) | MET but Q-CHANNEL-MIX has DATA NOTE → render honest prose paragraph (no table) | YES (prose) |
| eCat Footprint | CONDITIONAL | MET — HAS_PORTAL_ORDERS=true; VM45_RENDER=false so render eCat standalone volume + data-sync line, NO adoption-stage ladder, NO "each point worth $Z" | YES |
| eCat Order Trend | MANDATORY (always) | MET — Q-18 partA 13 months; Part B total-business via Q-18-B | YES (Part A + B) |
| Top Buyers & Concentration | MANDATORY (always) | MET — Q-13 15 rows; Q-52 enrichment MANDATORY (PORTAL_CUSTOMER_DATA_PRESENT=true) | YES (enriched) |
| Order Type & Workflow | MANDATORY (always) | MET — Q-21 4 types incl Quote, HFC | YES |
| Channel Migration | CONDITIONAL | MET — HAS_CART=true, iPad vs eCat Online from Q-18/Q-20; no share-of-total overlay (thin origin data) | YES |
| Market Commitment Attribution | CONDITIONAL — MANDATORY when gate met | NOT MET — HAS_COMMITMENT_DATA=false, Q-58 absent | NO |
| Quote Economics | CONDITIONAL | MET — Q-20: 23 quotes (≥10) + confirmed orders | YES |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET — no rep-level AOV (PORTAL_REP_DATA_PRESENT=false; Q-18 is monthly/channel only) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET — Q-41 spans Mar 2025–Jun 2026 (>6mo); named accounts from Q-ORG-VELOCITY | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET — guide source Q-21 has no monthly time series (order-type rollup only) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL — MANDATORY when gate met | NOT MET — Q-55 has no row where total grew AND eCat share shrank (all eCat shares 0/0) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL — MANDATORY when gate met | MET — HAS_PORTAL_ORDERS=true + Q-60 20 rows. Part B omit (no Q-39 category data) | YES (Part A) |

## Rendered count: 8 subsections (narrative-arc order)
1. Order Channel Mix (context — prose, DATA NOTE path)
2. eCat Footprint (context — eCat as a tool in the mix; enablement thesis, NOT share-to-grow; VM45 fallback)
3. eCat Order Trend (strength — Part A + B)
4. Top Buyers & Concentration — enriched (intelligence)
5. Order Type & Workflow (intelligence)
6. Channel Migration (intelligence)
7. Quote Economics (opportunity)
8. New Buyer Acquisition & Growth (intelligence)
9. Product Mix & Pricing Trends — Price Erosion (risk, last)
