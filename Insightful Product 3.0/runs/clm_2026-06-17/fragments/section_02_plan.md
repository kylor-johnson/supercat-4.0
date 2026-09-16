# Section 02 Build Plan — Account Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics | MANDATORY | MET (Q-12 row present) | YES |
| Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| Top 10 Mini-Briefs | MANDATORY | MET (top_accounts.md = 10 rows) | YES |
| eCat Penetration (3b) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 30 rows) | YES |
| Geographic Revenue Trends (11) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-67 25 rows) | YES |
| Buyer-Within-Account (10) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false, Q-66 not present) | NO |
| Untapped Category Opportunities (9) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| Unactivated High-Value Accounts (5) | CONDITIONAL | MET (SIG-OPP-02 fired, Q-53 20 rows) | YES |
| Enterprise Channel Accounts (5b) | CONDITIONAL | NOT MET (no enumerated ENTERPRISE_CHANNEL exclusion set provided) | NO |
| Geographic Distribution (6) | CONDITIONAL | NOT MET (no state >30% of revenue; distribution diffuse) | NO |
| Reorder Velocity & Early Warning (8) | MANDATORY | MET (Q-14 11 rows) | YES |
| Account Velocity Deceleration Alert (8b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b 15 rows) | YES |
| Dormant High-Value Accounts (4) | CONDITIONAL | MET (SIG-RISK-02, Q-17 25 rows) | YES |
| Velocity Deceleration / Contracting YoY (7) | CONDITIONAL | MET (SIG-DECAY-04, Q-ORG-CONTRACTION 25 rows) | YES |
| Spending Contraction (12) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-68 20 rows) | YES |

## Confidence Header
- Tier: STRONG → template `§2-STRONG`, label "STRONG VIEW"
- ACCOUNT_COUNT = 4,815

## Render order (narrative arc)
1. Header Metrics → 2. Confidence Header → 3. Mini-Briefs (top 5 + 6–10 collapsed)
→ 3b eCat Penetration → 11 Geographic Revenue Trends → 9 (skip) → 5 Unactivated
→ 6 (skip) → 8 Reorder Velocity + 8b Deceleration → 4 Dormant → 7 Contracting YoY
→ 12 Spending Contraction (collapsed) → section-level what-this-means
