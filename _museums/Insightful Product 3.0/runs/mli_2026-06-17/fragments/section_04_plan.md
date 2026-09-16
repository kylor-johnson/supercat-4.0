# Section 04 Build Plan — Commerce Patterns

**Confidence tier:** SECTION_CONFIDENCE_4 = STRONG → but §4-STRONG requires
`{{LAST_PORTAL_ORDER_DATE}}` and `HAS_PORTAL_ORDERS = false` so it cannot be
resolved → fall back to §4-PARTIAL template (label "PARTIAL VIEW") per guide.

**Section-wide constraint:** `HAS_PORTAL_ORDERS = false` → eCat-only data. No
total-business / all-channel language anywhere. Subsections 1, 2B, 3 (share
overlay), 9, 10 skipped. `HAS_CART = false`, `HAS_COMMITMENT_DATA = false`,
`PORTAL_CUSTOMER_DATA_PRESENT = false`, `PORTAL_REP_DATA_PRESENT = false`.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18 partA, 9 months) | YES |
| Channel Migration | CONDITIONAL | NOT MET (1 channel only — 100% iPad, 0 online; HAS_CART=false) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13, 15 rows). Q-52 enrichment NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false / Q-52 absent) → base table | YES |
| Quote Economics | CONDITIONAL | NOT MET (only 3 quotes; gate needs 10+) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21, 3 types) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month monthly time series in Q-21; Q-18 partA only 9 months) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data; QUALIFYING_REP_COUNT=1) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41, 8 months). Account-level trajectory unavailable → state explicitly | YES |

**Rendered subsections (narrative arc order):**
eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth
