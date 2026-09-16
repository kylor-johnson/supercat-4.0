# Section 04 Build Plan — Commerce Patterns

Confidence tier: SECTION_CONFIDENCE_4 = STRONG. However, `{{LAST_PORTAL_ORDER_DATE}}`
cannot be resolved (HAS_PORTAL_ORDERS = false), so per the guide's confidence-header
variable-resolution rule, the header falls back to **§4-PARTIAL** (label "PARTIAL VIEW").

Gate summary:
- HAS_PORTAL_ORDERS = false → subsections 1, 3 (share overlay), 9, 10 skipped; eCat-only data, no total-business mentions.
- HAS_CART = false → no iPad-vs-Online channel attribution statement.
- HAS_COMMITMENT_DATA = false → subsection 11 skipped.
- PORTAL_CUSTOMER_DATA_PRESENT = false + Q-52 absent → subsection 4 renders Q-13-only (no enrichment columns).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A) | MET (Q-18-A has 11 monthly rows; Part B skipped, HAS_PORTAL_ORDERS=false) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel — all iPad, 0 Online) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows; no Q-52 enrichment) | YES |
| Quote Economics | CONDITIONAL | NOT MET (only 3 quotes; threshold 10+) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 4 rows) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (only 11 months of order data; threshold 12+) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (Q-18 rep-level data absent) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 spans Apr 2025–Jun 2026, 6+ months) | YES |

Rendered subsections (narrative-arc order): eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth.
