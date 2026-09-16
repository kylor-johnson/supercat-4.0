# Section 02 Build Plan — Account Intelligence

**Confidence tier (SECTION_CONFIDENCE_2):** STRONG → template `§2-STRONG`, label "STRONG VIEW"

## Gate-driven subsection check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row: 787 total / 73 ever / 37 active 12mo / 31 active 6mo / 2 active 3mo) | YES |
| Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| Top 10 Mini-Briefs | MANDATORY | MET — note: `top_accounts.md` returned ZERO rows; org's account-level signals are dormancy (SIG-RISK-02 via Q-17/Q-17-atrisk) + stock-out impact (Q-ORG-STOCKOUT). Mini-briefs built from highest-value dormant accounts cross-referenced with stock-out exposure. | YES (5 full + 5 collapsed) |
| 3b eCat Penetration (Q-52) | CONDITIONAL (MUST when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 not present) | NO |
| 4 Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02; Q-17 has 25 rows, Q-17-atrisk has 20 rows) | YES |
| 5 Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (SIG-OPP-02 absent; Q-53 not present) | NO |
| 5b Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set; SHOWROOM_EXCLUSIONS=0) | NO |
| 6 Geographic Distribution (Q-40) | CONDITIONAL | MET (QC = $193,560 of $325,171 = 59% > 30% concentration; Q-40 has 6 rows) | YES |
| 7 Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (SIG-DECAY-04 absent; Q-ORG-CONTRACTION not present) | NO |
| 8 Reorder Velocity & Early Warning (Q-14) | MANDATORY ("Always render from Q-14") | Q-14 = 0 rows. Per Data Presentation thin-data rule, render gap note rather than empty table. Treated as data-gap; not forced into empty table. | NO (data gap noted in confidence header) |
| 8b Deceleration Alert (Q-14b) | CONDITIONAL (MUST when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-14b not present) | NO |
| 9 Untapped Category Opportunities (Q-57) | CONDITIONAL (MUST when gate met) | NOT MET (HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False; Q-57 not present) | NO |
| 10 Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False, HAS_BUYER_DATA=False; Q-66 not present) | NO |
| 11 Geographic Revenue Trends (Q-67) | CONDITIONAL (MUST when gate met) | NOT MET (HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False; Q-67 not present) | NO |
| 12 Spending Contraction (Q-68) | CONDITIONAL (MUST when gate met) | NOT MET (HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False; Q-68 not present) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Narrative render order (intelligence → opportunity → risk)
1. Header Metrics
2. Data Confidence Header (STRONG VIEW)
3. Top 10 Mini-Briefs (5 full + Accounts 6–10 collapsed)
6. Geographic Distribution (QC concentration)
4. Dormant High-Value Accounts (RISK, render late)
- Section-level what-this-means

## Notes
- No PORTAL_ORDERS data → all eCat-penetration / total-business / buyer / QoQ-geo subsections correctly skipped.
- top_accounts.md empty → mini-briefs sourced from Q-17-atrisk (dormancy) + Q-ORG-STOCKOUT (fulfillment exposure), the only account-level signals present. Each mini-brief renders the components whose signal fired (Reorder Pattern Change for dormancy; Fulfillment Gap where the account buys a stocked-out item).
- All dollar figures carry LTM/12mo qualifiers. All findings name specific accounts.
