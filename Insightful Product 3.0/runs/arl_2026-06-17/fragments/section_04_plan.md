# Section 04 Build Plan — Commerce Patterns

**Client**: Arabela Lighting (arl) · Run date 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4)**: LIMITED → template `§4-PARTIAL` with `.limited` class, label "LIMITED VIEW"

## Governing gates
- `HAS_PORTAL_ORDERS = false` → skip subsections 1, 2B, 3 (share overlay), 9, 10. No total-business / all-channel language anywhere.
- `HAS_CART = false` AND Q-18-A shows 0 eCat Online orders (100% iPad) → no iPad-vs-Online channel split.
- `HAS_COMMITMENT_DATA = false` → skip 11 (and 11B).
- `PORTAL_CUSTOMER_DATA_PRESENT = false` AND Q-52 absent → Top Buyers renders Q-13-only (no enrichment columns).
- `PORTAL_REP_DATA_PRESENT = false` → no 9B.

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18-A has 13 months) | YES |
| eCat Order Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false, single channel — 100% iPad) | NO |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 has 15 rows) | YES |
| Top Buyers enrichment (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false, Q-52 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 shows 0 quotes; <10 quotes) | NO |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 3 types) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 is type breakdown, no 12-mo monthly time series; Q-69 0 rows) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (Q-18-A has no rep-level AOV; monthly only) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 13 months) | YES |

## Rendering order (narrative arc, gated subset)
1. eCat Order Trend (STRENGTH)
2. Top Buyers & Concentration (INTELLIGENCE)
3. Order Type & Workflow (INTELLIGENCE)
4. New Buyer Acquisition & Growth (INTELLIGENCE — pipeline health)

## Data notes
- Total eCat GMV (Q-20, All eCat Orders) = $662,375 over 313 orders, overall AOV $2,116 LTM.
- Q-13 `pct_of_ecat_gmv` column is corrupted (shows "$8","$6"...). Recompute share = gmv / $662,375.
- Top 5 Q-13 buyers GMV = 33,541+25,691+24,244+18,963+16,998 = $119,437 → 18.0% of $662,375. (Signal SIG-RISK-01 quotes top-5=50% / $119,437 — the $ matches; render the recomputed 18.0% honestly with concentration framing.)
- Q-41 monthly new buyers all "Rep-Acquired (iPad)". No account-level trajectory data available → state the gap per guide §12 framing. Avg ≈ 5.8/mo; trend rising (first half ~4.0/mo, second half ~7.8/mo).
- HFC orders present (7) → note approval workflow serves high-value governance.
- New buyer acquisition is NOT declining (rising) → no decline alert.
