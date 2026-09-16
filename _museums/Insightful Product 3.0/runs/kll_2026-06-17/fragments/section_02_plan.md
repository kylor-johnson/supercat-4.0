# Section 02 Build Plan — Account Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics | MANDATORY | MET (Q-12 present) | YES |
| Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| Top 10 Mini-Briefs | MANDATORY | MET (top_accounts.md 10 rows) | YES |
| eCat Penetration of Total Business (3b) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 30 rows) | YES |
| Geographic Revenue Trends (11) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-67 25 rows) | YES |
| Buyer-Within-Account Intelligence (10) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| Untapped Category Opportunities (9) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| Unactivated High-Value Accounts (5) | CONDITIONAL | MET (SIG-OPP-02 fired; Q-53 20 rows) | YES |
| Enterprise Channel Accounts (5b) | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set; HAS_CART=true) | NO |
| Geographic Distribution (6) | CONDITIONAL | NOT MET (eCat distribution not >30% single-state; QC ~16%) | NO |
| Reorder Velocity & Early Warning (8) | MANDATORY | MET (Q-14 17 rows) | YES |
| Account Velocity Deceleration Alert (8b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b 15 rows) | YES |
| Dormant High-Value Accounts (4) | CONDITIONAL | MET (SIG-RISK-02 dormant set; Q-17 25 rows) | YES |
| Accounts Contracting Year-Over-Year (7) | CONDITIONAL | MET (SIG-DECAY-04 fired; Q-ORG-CONTRACTION CONTRACTING rows) | YES |
| Spending Contraction Detection (12) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-68 20 rows) | YES |
| Section-Level What-This-Means | MANDATORY | MET | YES |

## Render order (narrative arc)
1. Header Metrics
2. Data Confidence Header (STRONG VIEW)
3. Top 10 Mini-Briefs (5 visible + 6–10 collapsed)
4. eCat Penetration (3b) — INTELLIGENCE
5. Geographic Revenue Trends (11) — INTELLIGENCE
6. Unactivated High-Value Accounts (5) — OPPORTUNITY
7. Reorder Velocity & Early Warning + Deceleration Alert (8/8b)
8. Dormant High-Value Accounts (4) — RISK
9. Accounts Contracting YoY (7) — RISK
10. Spending Contraction (12) — RISK, collapsed
11. Section What-This-Means

## Mini-brief mapping (top_accounts.md → available data)
1. FLUX LIGHTING — CONTRACTING -46.5% YoY ($390,259→$208,941); Q-68 contraction; competitive hypotheses (M-rule, >$50K, >25%)
2. SUPREME LIGHTING AND ELEC SUPPLIES — CONTRACTING -28.2% YoY ($249,337→$179,045); Q-68 contraction
3. REXEL — CONTRACTING -39.2% YoY ($176,784→$107,488); Q-14b deceleration 3.18x; competitive hypotheses
4. KENDALL ELECTRIC INC. — CONTRACTING -35.9% YoY ($165,833→$106,301); competitive hypotheses
5. BA ROBINSON CO LTD — COMPETITIVE_DISPLACEMENT total +85.1% eCat -100%; Q-52 wallet $1.3M total, 0 eCat
6. ROBINSON LIGHTING LTD — displacement total +108.9% eCat -100%
7. DHILLON LIGHTING CALGARY — displacement total +115% eCat -100%
8. ECLAIRAGE UNION MONTREAL — displacement total +241.7% eCat -100% ($71,699→$0)
9. MCLAREN LIGHTING — displacement total +158.9% eCat -100%
10. MONTREAL LIGHTING AND HARDWARE — displacement total +116.3% eCat -100%
