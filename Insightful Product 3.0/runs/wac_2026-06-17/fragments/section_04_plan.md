# Section 04 Build Plan — Commerce Patterns

Section: §4 Commerce Patterns (id: commerce)
Confidence tier (SECTION_CONFIDENCE_4): STRONG → §4-STRONG / "STRONG VIEW"

Key gates: HAS_PORTAL_ORDERS=false, HAS_CART=false, HAS_COMMITMENT_DATA=false,
PORTAL_CUSTOMER_DATA_PRESENT=false, PORTAL_REP_DATA_PRESENT=false, VM45_RENDER=false,
HAS_INVENTORY=true.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18-A has 13 monthly rows) | YES |
| eCat Order Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 has 15 rows) | YES |
| Top Buyers Q-52 enrichment | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false, Q-52 absent) | NO |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 3 type rows) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel — iPad, ecat_online=0 all months) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false, Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (only 6 quotes, threshold 10+) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 rep file absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 16 monthly rows) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 has no monthly time series) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-60 absent) | NO |

Rendered (narrative arc order): eCat Order Trend → Top Buyers & Concentration →
Order Type & Workflow → New Buyer Acquisition & Growth.

Notes:
- HAS_PORTAL_ORDERS=false: eCat-only data. No mention of total business / all-channel.
- Quote premium framing inverted (quotes $3,331 AOV < confirmed $4,228) — §6 leads
  with dominant Confirmed workflow pattern, per guide fallback.
- Q-41 has aggregate monthly counts only (no account-level); state the gap explicitly.
