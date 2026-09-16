# Section 04 Build Plan — Commerce Patterns

**Confidence tier (SECTION_CONFIDENCE_4):** LIMITED → template `§4-PARTIAL` with `.limited` class, label "LIMITED VIEW"

**Key gates:** HAS_PORTAL_ORDERS=false · HAS_CART=false · HAS_COMMITMENT_DATA=false · PORTAL_CUSTOMER_DATA_PRESENT=false · HAS_INVENTORY=true · VM45_RENDER=false

**Data reality:** Only 1 eCat order in LTM ($6,333, iPad, Confirmed, Jan 2026). Q-13 top buyers = 0 rows; Q-41 new buyers = 0 rows; Q-69 = 0 rows; no quote orders.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY | MET (Q-18-A has 1 row) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel, 1 month) | NO |
| Top Buyers & Concentration | MANDATORY (always) | Q-13 = 0 rows → thin-data: inline note, no empty table | YES (degraded) |
| Quote Economics | CONDITIONAL | NOT MET (0 quotes) | NO |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 1 row: Confirmed) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (1 month of data, need 12+) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV / single order) | NO |
| Channel Share Opportunity (Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | NOT MET (Q-41 = 0 rows, no 6+ mo trend) | NO |

**Rendered subsections (narrative arc order):** eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow

**Confidence header:** MANDATORY, at top, LIMITED VIEW (`.data-confidence limited`).
**Section-level what-this-means:** MANDATORY at end.
