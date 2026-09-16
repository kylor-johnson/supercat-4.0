# Section 04 Build Plan — Commerce Patterns

**Client**: Millennium Lighting (ml) · Run date 2026-06-17
**Section confidence (SECTION_CONFIDENCE_4)**: STRONG → label "STRONG VIEW".
`{{LAST_PORTAL_ORDER_DATE}}` cannot resolve (HAS_PORTAL_ORDERS=false), so confidence-header TEXT uses the eCat-only (PARTIAL-style) framing per the guide's fallback rule.

## Key gates
- HAS_PORTAL_ORDERS = **False** → skip subsections 1, 2B, 3 share-overlay, 9, 10. No total-business / all-channel language anywhere.
- HAS_CART = **False** → no cart channel split.
- HAS_COMMITMENT_DATA = **False** → skip subsection 11.
- PORTAL_CUSTOMER_DATA_PRESENT = **False** → Top Buyers base table (Q-13) only, no enrichment columns.
- Q-18-A: all orders iPad (eCat_online = 0 every month) → single channel, Channel Migration skipped.
- Q-20: Quote Orders = 0 → Quote Economics skipped; Order Type subsection leads with workflow pattern, not quote premium.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18-A, 8 rows) | YES |
| eCat Share of Total (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; single channel, 0 eCat Online) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13, 3 rows) | YES |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 Quote Orders=0) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21, Confirmed + HFC) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month monthly revenue series; Q-21 has no monthly breakdown) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level Q-18 data) | NO |
| Channel Share Opportunity (Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | NOT MET (Q-41 has only 2 monthly points, not 6+ months) | NO |

**Rendering (narrative arc order):** eCat Order Trend (STRENGTH) → Top Buyers & Concentration (INTELLIGENCE) → Order Type & Workflow (INTELLIGENCE).

3 subsections render → meets the ≥3-subsection include gate.
