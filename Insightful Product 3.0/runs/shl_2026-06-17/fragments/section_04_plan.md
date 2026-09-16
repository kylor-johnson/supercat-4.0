# Section 04 Build Plan — Commerce Patterns

**Client**: Savoy House Lighting (shl) · **Run**: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4)**: STRONG → template `§4-STRONG`, label "STRONG VIEW"
**Thesis (REFRAMED)**: DIGITAL ENABLEMENT, not eCat share. BANNED: "grow eCat X%→Y%", "capture rate",
"adoption stage / Early-Emerging-Dominant", "each point worth $Z". eCat is a TOOL in the order mix,
never a quota; never imply non-eCat orders are "manual/offline" as certainty.
**Data scale**: $3.4M eCat LTM · $50.0M total business LTM (clean data).
**Q-CHANNEL-MIX**: contains a DATA NOTE (100% Unclassified order-origin) → DATA NOTE path: honest
paragraph, NO channel table.

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL (render FIRST) | MET — HAS_PORTAL_ORDERS=T; Q-CHANNEL-MIX has DATA NOTE → honest-paragraph path | YES (paragraph, no table) |
| eCat Footprint | CONDITIONAL | MET — HAS_PORTAL_ORDERS=T, VM45_RENDER=T | YES |
| eCat Order Trend | MANDATORY (Part A); Part B CONDITIONAL | MET — Q-18-A 13 months; Part B MET (HAS_PORTAL_ORDERS=T, Q-18-B total business) | YES (A + B) |
| Top Buyers & Concentration | MANDATORY | MET — Q-13 15 rows; enrichment MET (PORTAL_CUSTOMER_DATA_PRESENT=T, Q-52 30 rows) | YES (+ Total Business + eCat Share) |
| Order Type & Workflow | MANDATORY | MET — Q-21 3 types | YES |
| Channel Migration | CONDITIONAL | MET — Q-18 iPad + eCat Online, 13 months ≥ 6. HAS_CART=F → eCat channel split only, no share-of-total overlay | YES |
| Market Commitment Attribution | CONDITIONAL | NOT MET — HAS_COMMITMENT_DATA=F; Q-58/Q-58b absent | NO |
| Quote Economics | CONDITIONAL | NOT MET — only 2 quotes < 10 threshold | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET — no rep-level AOV data; PORTAL_REP_DATA_PRESENT=F | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET — Q-41 13 months ≥ 6 | YES (+ Q-ORG-VELOCITY named trajectories) |
| Ordering Seasonality | CONDITIONAL | NOT MET — Q-21 has no monthly series; Q-18-A monthly dominated by market-order spikes | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (MANDATORY when gate met) | NOT MET — Q-55: all rows ecat_share_change_ppts = 0; no row total_growth>0 AND ecat_share<0 | NO (skip silently) |
| Product Mix & Pricing Trends (Price Erosion) | MANDATORY when gate met | MET — HAS_PORTAL_ORDERS=T, Q-60 20 rows | YES (Part A; Part B omitted — no Q-39 in bundle) |

**Render order (narrative arc)**: Order Channel Mix → eCat Footprint → eCat Order Trend →
Top Buyers & Concentration → Order Type & Workflow → Channel Migration →
New Buyer Acquisition & Growth → Product Mix & Pricing Trends.

## Notes
- §4-STRONG confidence header positioned immediately after the summary metrics, before subsections.
- eCat Footprint (NOT "eCat Ordering Share"): shows $3.4M eCat as a tool in the mix and 6.9% of total
  business factually — NO badge, NO "Early/grow-the-share" classification, NO capture-rate quota. The
  opportunity is digitizing rep-/back-office-entered order flow, not a bigger eCat number.
- Order Channel Mix renders the required honest DATA-NOTE paragraph (no table): shl's ERP feed has no
  order-origin detail; non-eCat volume is rep-/back-office-entered and must NOT be called manual/offline.
- Subsection 9 (Q-55) skipped silently: every row has prior & current eCat share = 0, so no category
  meets the displacement criteria (total grew AND eCat share shrank). No false alarm.
- Ordering Seasonality skipped: Q-21 (the guide's data source) has no monthly series; Q-18-A monthly is
  dominated by market-order artifacts (Jun-25 $663K, Jan-26 $2.5M, both iPad-heavy).
- Q-60 Part B (category-level) omitted: Q-39 not in bundle → insufficient category granularity.
- Jan-2026 and Jun-2025 eCat spikes are market-order artifacts (iPad-heavy, very high AOV); flagged as
  market/partial periods in the trend narrative, not organic monthly demand.
