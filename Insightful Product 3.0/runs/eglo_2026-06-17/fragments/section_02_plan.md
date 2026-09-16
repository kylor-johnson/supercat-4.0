# Section 02 Build Plan — Account Intelligence

**Client**: Eglo USA Inc. (eglo) · Run date 2026-06-17
**Section confidence (SECTION_CONFIDENCE_2)**: STRONG → `§2-STRONG` / "STRONG VIEW"

## Gate snapshot
- HAS_PORTAL_ORDERS = **False**
- PORTAL_CUSTOMER_DATA_PRESENT = **False**
- HAS_BUYER_DATA = **False**
- HAS_INVENTORY = True; HAS_SALES_DATA = True
- top_accounts.md = **0 rows** (no signal-density ranking produced)

## Pre-Build Gate Check (mandatory-conditional table)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built from Q-14/Q-17/Q-ORG-STOCKOUT account data; top_accounts.md empty so accounts selected by available LTM/historical GMV + fired stock-out signal) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL (MUST when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 not present) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 25 rows; SIG-RISK-02 pattern present) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 not present) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (FL = $44.3K = 19% but concentration in top states notable; Q-40 has 18 rows) — render compact | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION not present) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 4 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL (MUST when gate met) | NOT MET (Q-14b not present; HAS_PORTAL_ORDERS=false) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL (MUST when gate met) | NOT MET (Q-57 not present; gates false) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (Q-66 not present; HAS_BUYER_DATA=false) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL (MUST when gate met) | NOT MET (Q-67 not present; gates false) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL (MUST when gate met) | NOT MET (Q-68 not present; gates false) | NO |
| Section-level what-this-means | MANDATORY | — | YES |

## Mini-brief account selection (top_accounts.md empty → derived)
Selected by available account-level signal/value:
1. Gross Electric Inc (OH) — most active eCat reorderer (6 orders, 0.2-day cadence), now 252 days silent (dormant) — reorder-decay + dormancy story
2. Ferguson #555 - Katy, TX (TX) — highest historical eCat GMV ($23,583), 128 days silent — dormant high-value
3. Lights & More, LLC (FL) — $19,038 historical, 158 days silent
4. Lightstyle of Orlando (FL) — $17,904 historical, 157 days silent
5. Grupo ARM Rojas Ochoa SRL — active reorderer ($9,035, 5 orders, 27-day cadence) — still-engaged contrast
6–10: Muska Lighting, Progressive Lighting, Glitz Lighting Gallery, Chic Home Lighting (active, 6 orders), Grand Rapids Lighting Center (active reorderer)

Stock-out impact (Q-ORG-STOCKOUT) woven into briefs where the account appears in a stock-out item's top_customers list (e.g., Pine Tree Lighting on Ayers 207275A; Shades of Light on Maserlo).

## Notes
- No NBP / velocity / org-decay / contraction data → those mini-brief components silently omitted per spec.
- Engagement Score computed per account from recency/frequency/monetary/trajectory; no YoY data available → trajectory scored neutral; YoY metric-note omitted where unknown.
- All $ figures carry LTM / historical time qualifiers. All entity names title-cased.
