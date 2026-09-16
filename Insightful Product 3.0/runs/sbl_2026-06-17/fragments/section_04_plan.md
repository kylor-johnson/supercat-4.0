# Section 04 Build Plan — Commerce Patterns

**Client:** Schonbek Lighting (sbl) · Run date 2026-06-17
**Section confidence (SECTION_CONFIDENCE_4):** STRONG → rendered as §4-PARTIAL template (`{{LAST_PORTAL_ORDER_DATE}}` unresolvable because HAS_PORTAL_ORDERS=false; per variable-resolution fallback, use §4-PARTIAL / PARTIAL VIEW).

**Governing gates:**
- HAS_PORTAL_ORDERS = False → subsections 1, 2B, 3-overlay, 9, 10 skipped; no "total business" anywhere.
- HAS_CART = False AND only one active eCat channel (iPad; eCat Online = 0 orders) → Channel Migration skipped.
- HAS_COMMITMENT_DATA = False → subsection 11 skipped.
- PORTAL_CUSTOMER_DATA_PRESENT = False, Q-52 absent → Top Buyers renders Q-13-only (no enrichment columns).
- Only 4 quotes (< 10 threshold) → Quote Economics skipped.
- No rep-level AOV data in Q-18_partA → AOV Spread by Rep skipped.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18_partA, 12 months) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; single channel — 0 eCat Online orders) | NO |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13, 15 rows) | YES |
| Top Buyers enrichment | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (only 4 quotes; threshold 10+) | NO |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21, 3 types) | YES |
| Ordering Seasonality | CONDITIONAL | MET (Q-18_partA, 12 months of monthly eCat sales) | YES |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data available) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41, 13 months) — aggregate only; account-level trajectory gap stated explicitly | YES |

**Rendering order (narrative arc):** eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth → Ordering Seasonality.

**Subsections rendered: 5.**
