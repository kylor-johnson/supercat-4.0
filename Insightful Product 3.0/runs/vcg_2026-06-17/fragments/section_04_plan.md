# Section 04 Build Plan — Commerce Patterns

Confidence tier: SECTION_CONFIDENCE_4 = STRONG. Header variable {{LAST_PORTAL_ORDER_DATE}}
cannot resolve (HAS_PORTAL_ORDERS=false) → fall back to §4-PARTIAL template ("PARTIAL VIEW")
per guide variable-resolution rule.

Key gates: HAS_PORTAL_ORDERS=false (skip 1, 2B, 3-overlay, 9, 10), HAS_CART=false,
HAS_COMMITMENT_DATA=false (skip 11), PORTAL_CUSTOMER_DATA_PRESENT=false (no Q-52 enrichment),
PORTAL_REP_DATA_PRESENT=false (no 9B). eCat is 100% iPad (online orders = 0).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY | MET (Q-18-A has 13 months) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows); enrichment NOT MET (no Q-52) | YES (base only) |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 3 types incl. quotes) | YES |
| Channel Migration | CONDITIONAL | NOT MET (only iPad channel; online=0; HAS_CART=false) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false, Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-20: 20 quotes + confirmed orders) | YES |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 rep file absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 15 months) | YES (aggregate; no trajectory data) |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 has no monthly time series) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-55 absent) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-60 absent) | NO |

Rendered (5): eCat Order Trend, Top Buyers & Concentration, Order Type & Workflow,
Quote Economics, New Buyer Acquisition & Growth. Plus section-level what-this-means.
