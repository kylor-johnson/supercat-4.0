# Section 04 Build Plan — Commerce Patterns

Section: §4 Commerce | id=commerce | Coleto Brands | Progress Lighting (prog)
Confidence tier (SECTION_CONFIDENCE_4): **PARTIAL** → template `§4-PARTIAL`, label `PARTIAL VIEW`

Key gates: HAS_PORTAL_ORDERS=False, HAS_CART=False, HAS_COMMITMENT_DATA=False,
HAS_INVENTORY=False, PORTAL_CUSTOMER_DATA_PRESENT=False, PORTAL_REP_DATA_PRESENT=False,
VM45_RENDER=False. eCat-only section — no total business / all-channel anywhere.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; VM45_RENDER=False) | NO |
| eCat Order Trend (Part A) | MANDATORY | MET (Q-18-A has 4 monthly rows) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=False; Q-18-A shows iPad only, single channel, 4 mo) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows) | YES |
| Top Buyers enrichment (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 shows 0 quote orders) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 3 types) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-69 empty; Q-18-A only 4 sparse months, <12mo) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 absent) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=False; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 4 monthly rows, no account trajectory) | YES |

Rendering order (narrative arc, gated): eCat Order Trend → Top Buyers & Concentration →
Order Type & Workflow → New Buyer Acquisition & Growth.

Notes:
- Q-13 `pct_of_ecat_gmv` is stored dollar-prefixed but is a percentage (e.g. "$17" = 17%).
- Top buyer name "ROYAUME LUMINAIRE" appears across multiple bill-to numbers; render each row as listed.
- New Buyer Acquisition: only aggregate counts available, no account-level trajectory — must state the gap explicitly per guide.
