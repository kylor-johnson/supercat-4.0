# Section 04 Build Plan — Commerce Patterns

**Client**: Buster & Punch (bp, org_id=250) · Run date: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4)**: STRONG
**Header template**: §4-STRONG requires `{{LAST_PORTAL_ORDER_DATE}}`, which cannot resolve because `HAS_PORTAL_ORDERS = false`. Per guide variable-resolution rule, **fall back to §4-PARTIAL** (label "PARTIAL VIEW").

## Key gates
- `HAS_PORTAL_ORDERS = false` → skip subsections 1, 2B, 3-share-overlay, 9, 10. No mention of total business / all-channel anywhere.
- `HAS_CART = false` → no iPad-vs-Online channel split (and all 12 orders are iPad).
- `HAS_COMMITMENT_DATA = false` → skip 11 (and Q-58/Q-58b absent).
- `PORTAL_CUSTOMER_DATA_PRESENT = false`, Q-52 absent → Top Buyers renders Q-13-only (no Total Business / eCat Share columns).
- `PORTAL_REP_DATA_PRESENT = false` → skip 9B.

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY | MET (Q-18-A has 7 monthly rows) | YES |
| eCat Order Trend (Part B share) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; single channel — 100% iPad) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 8 rows) | YES (base, no Q-52 enrichment) |
| Quote Economics | CONDITIONAL | NOT MET (0 quote orders in Q-20) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has data; 100% Confirmed, no quotes) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month monthly revenue series; Q-21 single row) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data; Q-18 absent) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 monthly, Mar 2025–Jun 2026 ≥6mo) | YES (aggregate only — no account-level trajectory data) |

## Rendered order (strength → intelligence → opportunity → risk)
1. eCat Order Trend (STRENGTH)
2. Top Buyers & Concentration (INTELLIGENCE)
3. Order Type & Workflow (INTELLIGENCE)
4. New Buyer Acquisition & Growth (INTELLIGENCE/pipeline)

## Notes
- §6 (data staleness) owns all the staleness signals; §4 owns SIG-RISK-01 (revenue concentration — top 5 = 98% of eCat GMV). That is the lead intelligence finding for the concentration callout.
- Q-41 has no account-level trajectory; per guide, state the gap explicitly and request customer-level first-order dates.
- All dollar figures carry "trailing 12 months" / "LTM" qualifiers. No total-business language.
