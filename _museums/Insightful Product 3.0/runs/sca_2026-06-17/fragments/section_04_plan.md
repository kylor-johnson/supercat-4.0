# Section 04 Build Plan — Commerce Patterns

Confidence tier: **SECTION_CONFIDENCE_4 = LIMITED** → template `§4-PARTIAL` with `.limited` class, label "LIMITED VIEW".

Key gates: `HAS_PORTAL_ORDERS=false`, `HAS_CART=false`, `HAS_COMMITMENT_DATA=false`, `PORTAL_CUSTOMER_DATA_PRESENT=false`, `HAS_INVENTORY=true`. eCat data shows 100% iPad, 0 eCat Online every month. No "total business" anywhere in section.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A) | MET (Q-18-A has 12 months) | YES (Part A only; Part B skipped, HAS_PORTAL_ORDERS=false) |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; Q-18-A is 100% iPad, single channel) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows) | YES (Q-13-only; no Q-52 enrichment, PORTAL_CUSTOMER_DATA_PRESENT=false) |
| Quote Economics | CONDITIONAL | NOT MET (only 9 quotes; threshold 10+) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has data) | YES |
| Ordering Seasonality | CONDITIONAL | MET (Q-18-A has 12 months of monthly GMV) | YES |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 absent, Q-18-A has no rep dimension) | NO |
| Channel Share Opportunity (Displacement) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-55 absent) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 9 months, Mar 2025–Jun 2026) | YES (aggregate only; account-level trajectory unavailable, stated explicitly) |

Rendered subsections (narrative arc order): eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth → Ordering Seasonality.

Data notes:
- Q-13 `pct_of_ecat_gmv` column is malformed ("$30" etc.); shares recomputed from GMV. Top 5 = 80.2% of eCat GMV ($653,938 of $815,887). Top buyer "Shadow Catchers, Inc." rendered as-is.
- eCat LTM: $2.07M GMV, 411 orders, AOV $5,044, 100% iPad.
- Order type: HFC averages $10,660 — 3.5x Confirmed AOV ($3,015). 9 quotes only → leading §6 with the HFC high-value workflow premium, not quote premium.
- Seasonality from Q-18-A monthly GMV (avg month $172,761). Peaks: Oct 2025 (idx 263), Jul 2025 (idx 242). Trough: Aug 2025 (idx 1).
- Q-41: 19 first-time eCat buyers over window, all Rep-Acquired (iPad). ~1–2/month.
