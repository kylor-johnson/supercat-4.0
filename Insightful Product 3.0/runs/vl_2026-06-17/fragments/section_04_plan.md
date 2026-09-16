# Section 04 Build Plan — Commerce Patterns

Client: Ciana Varaluz LLC (vl) · Run 2026-06-17
SECTION_CONFIDENCE_4 = **STRONG** → template §4-STRONG, label "STRONG VIEW"

Thesis (reframed): **DIGITAL ENABLEMENT, not eCat share.** eCat already carries
~93.6% of total-business GMV (Q-45) — it is vl's dominant channel. Frame eCat as
a strength; the opportunity = the small remaining rep-/back-office-entered volume.
NEVER "grow eCat X→Y / each point worth $Z / capture rate / adoption stage."
vl feed = thin order-origin → Q-CHANNEL-MIX carries a DATA NOTE → channel-mix
table is SKIPPED in favor of one honest paragraph.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET — HAS_PORTAL_ORDERS=T, Q-CHANNEL-MIX exists w/ DATA NOTE | YES (honest paragraph, no table — DATA NOTE path) |
| eCat Footprint | CONDITIONAL | MET — HAS_PORTAL_ORDERS=T, VM45_RENDER=T | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET — Q-18 Part A has 12 months; Part B (HAS_PORTAL_ORDERS=T) via Q-18 Part B ERP totals | YES (Part A + Part B share columns) |
| Top Buyers & Concentration | MANDATORY (always) | MET — Q-13 has 15 rows; Q-52 enrichment MET (PORTAL_CUSTOMER_DATA_PRESENT=T) | YES + Total Business / eCat Share enrichment columns |
| Order Type & Workflow | MANDATORY (always) | MET — Q-21 has 3 types | YES |
| Channel Migration | CONDITIONAL | NOT MET — HAS_CART=F and only 1 channel populated (100% iPad, eCat Online=0) | NO (skip silently) |
| Market Commitment Attribution | CONDITIONAL | NOT MET — HAS_COMMITMENT_DATA=F, Q-58/Q-58b not present | NO (skip silently) |
| Quote Economics | CONDITIONAL | MET — Q-20/Q-21 show 10 Quote orders (threshold 10+) + 47 Confirmed | YES |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET — Q-18 has no per-rep AOV data this run | NO (skip silently) |
| New Buyer Acquisition & Growth | CONDITIONAL | MET — Q-41 spans 6+ months (Mar 2025–Jun 2026) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET — Q-21 has no monthly series; eCat monthly (Q-18-A) too lumpy/thin for honest seasonality | NO (skip silently) |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (mandatory when gate met) | NOT MET — Q-55: every row total_growth<0 AND share_change=0; ZERO displacement rows | NO (skip silently — no false alarm) |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL (mandatory when gate met) | MET — HAS_PORTAL_ORDERS=T, Q-60 has 3 rows | YES |

## Render order (strength → intelligence → opportunity → risk)
1. Order Channel Mix (context, DATA NOTE paragraph)
2. eCat Footprint (context)
3. eCat Order Trend (strength)
4. Top Buyers & Concentration (intelligence) + Q-52 enrichment
5. Order Type & Workflow (intelligence)
6. Quote Economics (opportunity)
7. New Buyer Acquisition & Growth (intelligence)
8. Product Mix & Pricing Trends (risk — last)

## Key figures
- eCat LTM GMV $1.3M; total business LTM $1.4M; eCat = 93.6% of GMV (Q-45 "Primary transaction system")
- Top 5 buyers = 64% of eCat GMV ($419,032) — SIG-RISK-01
- Quote AOV $10,901 (10 quotes) vs Confirmed AOV $7,900 (47) → quotes ~1.4x; Wish List AOV $13,849 (59)
- Q-60 price erosion: Fort Worth Lighting -24.8%, Valley Light Gallery -24.0%, Southern Lights -44.9%
- Q-41 first-time buyers: Jan 2026 spike of 10; ~2.7/mo over 10 active months
