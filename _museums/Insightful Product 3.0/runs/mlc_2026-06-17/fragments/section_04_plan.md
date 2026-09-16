# Section 04 Build Plan — Commerce Patterns

Confidence tier: `SECTION_CONFIDENCE_4 = STRONG` → §4-STRONG / "STRONG VIEW".
Key gates: `HAS_PORTAL_ORDERS=false`, `HAS_CART=false`, `PORTAL_CUSTOMER_DATA_PRESENT=false`, `HAS_COMMITMENT_DATA=false`, `HAS_INVENTORY=true`.
eCat-only mode: no total-business / all-channel language anywhere.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18_partA has 13 monthly rows) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; eCat_online=0 all months → single channel) | NO |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 has 15 rows); enrichment NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false, Q-52 absent) | YES |
| Quote Economics | CONDITIONAL | NOT MET (only 3 quotes; gate needs 10+) | NO |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 3 type rows) | YES |
| Seasonal Timing | CONDITIONAL | NOT MET (Q-21 has no 12-month monthly revenue series) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (Q-18_partA has no rep-level AOV dimension) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-55 absent) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-60 absent) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false, Q-58 absent) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 has 9 monthly rows, Mar 2025–Mar 2026 > 6mo); account-level trajectory unavailable (counts only) | YES |

Rendered subsections (narrative arc order): eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth.
Total rendering: 4 subsections + section-level what-this-means.
