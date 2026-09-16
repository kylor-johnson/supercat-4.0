# Section 04 Build Plan — Commerce Patterns

Confidence tier: SECTION_CONFIDENCE_4 = **LIMITED** → `§4-PARTIAL` template with `.limited` class, label "LIMITED VIEW".

Key gates: HAS_PORTAL_ORDERS=false, HAS_CART=false, HAS_COMMITMENT_DATA=false, PORTAL_CUSTOMER_DATA_PRESENT=false, PORTAL_REP_DATA_PRESENT=false, HAS_INVENTORY=true. eCat-only client, very thin volume (7 eCat orders LTM).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18_partA has 3 rows). Part B NOT MET (HAS_PORTAL_ORDERS=false) | YES (Part A only) |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; all orders iPad, 0 eCat Online — single channel, no migration) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 2 rows). Q-52 enrichment NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false) | YES (base table) |
| Quote Economics | CONDITIONAL | NOT MET (0 quote orders; needs 10+ quotes) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 1 row: Confirmed 100%). No quotes → lead with dominant workflow pattern | YES |
| Seasonal Timing | CONDITIONAL | NOT MET (only 3 months of order data; needs 12+) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data in Q-18) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 not present) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 not present) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 not present) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | NOT MET (Q-41 spans only 2 distinct months over the window, not 6+ months of monthly data) | NO |

Rendered subsections: eCat Order Trend, Top Buyers & Concentration, Order Type & Workflow (3 total). Plus mandatory data-confidence header (LIMITED) and section-level what-this-means.

Note: thin-data handling — Top Buyers has only 2 rows; render as a small table (acceptable, both are named buyers with GMV/share). Order Type has a single type (Confirmed 100%) — render quote-premium callout fallback (dominant workflow pattern) + collapsed type table per guide.
