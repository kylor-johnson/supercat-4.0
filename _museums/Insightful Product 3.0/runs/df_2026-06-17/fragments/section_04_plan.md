# Section 04 Build Plan — Commerce Patterns

Confidence tier: SECTION_CONFIDENCE_4 = STRONG → §4-STRONG template, label "STRONG VIEW".

Key gates: HAS_PORTAL_ORDERS=False, HAS_CART=False, HAS_COMMITMENT_DATA=False,
PORTAL_CUSTOMER_DATA_PRESENT=False, VM45_RENDER=False. eCat-only client, thin data.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18 partA has 8 monthly rows) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=False; only iPad channel, eCat Online=0) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 4 rows); no Q-52 enrichment (PORTAL_CUSTOMER_DATA_PRESENT=False) | YES |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 shows 0 quote orders) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has Confirmed + HFC rows) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month monthly revenue series; Q-18 spans 8 partial months) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV in Q-18; cannot test >2x spread) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=False; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | NOT MET (Q-41 has only 3 sparse monthly rows, not 6+ months of data) | NO |

Rendered subsections: eCat Order Trend, Top Buyers & Concentration, Order Type & Workflow (3).

Notes:
- No total-business / all-channel language anywhere (HAS_PORTAL_ORDERS=False).
- Order Type subsection: no quotes exist → lead with dominant workflow pattern (Confirmed vs HFC), not quote premium.
- Top Buyers: Q-13 pct_of_ecat_gmv column is malformed ($78/$10/$9/$3 — these are integer percents rendered with $). Treat as % values: 78%, 10%, 9%, 3%.
