# Section 04 Build Plan — Commerce Patterns

Section: §4 Commerce Patterns (id: commerce)
Confidence tier: SECTION_CONFIDENCE_4 = PARTIAL → template §4-PARTIAL, label "PARTIAL VIEW"

Key gates: HAS_PORTAL_ORDERS=False, HAS_CART=False, HAS_COMMITMENT_DATA=False,
HAS_INVENTORY=False, PORTAL_CUSTOMER_DATA_PRESENT=False, PORTAL_REP_DATA_PRESENT=False,
VM45_RENDER=False. eCat-only data — no total-business / all-channel content anywhere.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; VM45_RENDER=False) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18 Part A has 9 monthly rows) | YES |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 has 15 rows; no Q-52 enrichment, PORTAL_CUSTOMER_DATA_PRESENT=False) | YES |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 3 type rows) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=False; Q-18 shows only iPad channel, 0 Online) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=False; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (only 4 quotes; threshold 10+) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (Q-18 rep-level not present) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 has monthly new-buyer rows spanning Jun 2025–Apr 2026) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 has no 12-month monthly time series) | NO |
| Competitive Displacement | CONDITIONAL (MANDATORY when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-55 absent) | NO |
| Price Erosion / Product Mix | CONDITIONAL (MANDATORY when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-60 absent) | NO |

Rendered subsections (narrative arc order): eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth.
Confidence header: PARTIAL VIEW, positioned immediately after first subsection-title open / before content per shared contract (top of section).
Section-level what-this-means: present.

Data note: Q-13 `pct_of_ecat_gmv` column is the percent value (dollar-sign is a formatting artifact). Top-5 share = 22.4+14.9+11.1+8.0+6.8 ≈ 63.2% → drives SIG-RISK-01 concentration callout.
