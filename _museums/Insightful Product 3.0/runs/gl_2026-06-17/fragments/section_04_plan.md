# Section 04 Build Plan — Commerce Patterns

**Client**: Golden Lighting (gl) · Run date 2026-06-17
**Section confidence (SECTION_CONFIDENCE_4)**: STRONG → template `§4-STRONG`, label `STRONG VIEW`
**Thesis**: DIGITAL ENABLEMENT, not eCat share. eCat = footprint/tool in the order mix. NO "grow eCat X%→Y%", NO "capture rate", NO "each point worth $Z", NO "adoption stage". gl feed = thin order-origin → Q-CHANNEL-MIX has DATA NOTE → channel table SKIPPED, honest enablement paragraph rendered first.

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET but Q-CHANNEL-MIX has DATA NOTE (100% Rep/ERP-entered) → DATA NOTE path: skip table, render honest enablement paragraph FIRST | YES (paragraph) |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true) — footprint, NOT share-to-grow, NO adoption ladder | YES |
| eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18-A, 13 months) | YES |
| eCat Order Trend (Part B) | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, Q-18-B total business) — share column framed as "more orders digitized" not "share captured" | YES |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13, 15 rows) | YES |
| Top Buyers enrichment (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 30 rows) → Total Business + eCat Share cols | YES |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21; Draft for Quote AOV $2,488 = 4.8x Confirmed $514) | YES |
| Channel Migration / Channel Split | CONDITIONAL | MET (HAS_CART=true → iPad vs eCat Online from Q-18-A) | YES |
| Market Commitment Attribution | CONDITIONAL (MANDATORY when met) | NOT MET (HAS_COMMITMENT_DATA=false; Q-58/Q-58b absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (only 4 Draft-for-Quote; <10 threshold; Q-20 Quote Orders=0) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; PORTAL_REP_DATA_PRESENT=false) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 spans Mar 2025–May 2026; trajectories from Q-ORG-VELOCITY) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 has no 12-month monthly series; only 2 order-type rows) | NO |
| Channel Share Opportunity (Competitive Displacement 9A) | CONDITIONAL (MANDATORY when met) | NOT MET (Q-55: every eCat share = 0/0; no row with total_growth>0 AND share_change<0) | NO |
| Rep Capture Rate Trend (9B) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-56 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion 10) | CONDITIONAL (MANDATORY when met) | MET (HAS_PORTAL_ORDERS=true, Q-60 20 rows) | YES |
| Category-Level AOV Trends (10B) | CONDITIONAL | NOT MET (Q-60 not broken out by category; no Q-39 in bundle) | NO |

**Render order (narrative arc strength→intelligence→opportunity→risk):**
Order Channel Mix (context paragraph) → eCat Footprint → eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → Channel Split: iPad vs eCat Online → New Buyer Acquisition & Growth → Product Mix & Pricing Trends.

**Confidence header:** STRONG → label "Strong View". {{LAST_PORTAL_ORDER_DATE}} = 2026-06-15 (days_since_last_erp_order=2).

**Data normalization:** title-case ALL-CAPS customer names; recompute Top-Buyer % from gmv / $131,151 (Q-13 pct column is dollar-junk); suppress empty State column in Q-52.
