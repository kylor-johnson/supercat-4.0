# Section 04 Build Plan — Commerce Patterns

**Confidence tier (SECTION_CONFIDENCE_4):** STRONG → template §4-STRONG, label "STRONG VIEW"

**Key gates:** HAS_PORTAL_ORDERS=False · HAS_CART=False · HAS_COMMITMENT_DATA=False · PORTAL_CUSTOMER_DATA_PRESENT=False · HAS_INVENTORY=True · SALES_DATA=True

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| 2. eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18-A has 10 monthly rows) | YES |
| 2B. eCat Share of Total Trend | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| 3. Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel — 100% iPad, 0 eCat Online) | NO |
| 4. Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 has 15 rows); no Q-52 enrichment (gate false) | YES |
| 5. Quote Economics | CONDITIONAL | NOT MET (only 3 quotes; need 10+) | NO |
| 6. Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 4 rows) | YES |
| 7. Seasonal Timing | CONDITIONAL | NOT MET (no Q-21 monthly time series spanning 12mo) | NO |
| 8. AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data; Q-18-A is monthly only) | NO |
| 9. Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| 10. Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| 11. Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| 12. First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 has 10 monthly rows, 6+ months) — aggregate only, no account trajectory | YES |

**Rendering (narrative arc):** eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth → section-level what-this-means.

**Notes:**
- All eCat orders are iPad (0 eCat Online) — section is eCat-only; no total-business/all-channel language anywhere.
- Q-41 is aggregate counts only (no account-level first-order GMV). Per §12 CRITICAL FRAMING, state the account-trajectory data gap explicitly rather than rendering vanity counts.
- Top-5 concentration = $126,661 of $260,143 (48.7% ≈ 49%, matches SIG-RISK-01).
