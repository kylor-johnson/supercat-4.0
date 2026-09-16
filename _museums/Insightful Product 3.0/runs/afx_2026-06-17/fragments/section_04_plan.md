# Section 04 Build Plan — Commerce Patterns

- **Client**: AFX, Inc. (afx, org_id=185)
- **Run date**: 2026-06-17
- **Section confidence (SECTION_CONFIDENCE_4)**: STRONG
- **Confidence header template**: §4-STRONG requires `{{LAST_PORTAL_ORDER_DATE}}`, which is unresolvable (HAS_PORTAL_ORDERS=false). Per guide variable-resolution rule, fall back to §4-PARTIAL template (label "Partial View").

## Key gates
- HAS_PORTAL_ORDERS = **false** → subsections 1, 2B, 3 share-overlay, 9, 10 skipped; no total-business language anywhere.
- HAS_CART = **false** → channel split not rendered.
- HAS_COMMITMENT_DATA = **false** → subsection 11 + 11B skipped.
- PORTAL_CUSTOMER_DATA_PRESENT = **false** → no Q-52 enrichment on Top Buyers.
- PORTAL_REP_DATA_PRESENT = **false** → no 9B.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A) | MET (Q-18 Part A has 3 monthly rows) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows) | YES |
| Top Buyers enrichment (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 absent) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 3 rows) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel — iPad) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-20: 37 quotes ≥ 10; confirmed orders exist) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data; Q-18 rep file absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 spans Jun 2025–Jan 2026) — account-level trajectory unavailable, noted in prose | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month monthly time series) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |

## Render order (narrative arc)
1. eCat Order Trend (strength)
2. Top Buyers & Concentration (intelligence)
3. Order Type & Workflow (intelligence)
4. Quote Economics (opportunity)
5. New Buyer Acquisition & Growth (intelligence)

5 subsections render + confidence header + section-level what-this-means.
