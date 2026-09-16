# Section 02 Build Plan — Account Intelligence

Confidence tier (SECTION_CONFIDENCE_2): **STRONG** → label "STRONG VIEW".
Template note: `{{LAST_PORTAL_ORDER_DATE}}` cannot be resolved (HAS_PORTAL_ORDERS=False),
so per guide the header text falls back to the §2-PARTIAL body while keeping the STRONG label.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics | MANDATORY | MET (Q-12 present, 1 row) | YES |
| Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| Top 10 Accounts by Signal Density (Mini-Briefs) | MANDATORY | MET (top_accounts.md empty → built from Q-14 top eCat accounts) | YES |
| eCat Penetration (3b, Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| Dormant High-Value Accounts (4, Q-17) | CONDITIONAL | MET (Q-17 has 25 rows; $15K+ / 90+ days silent) | YES |
| Unactivated High-Value Accounts (5, Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| Enterprise Channel Accounts (5b) | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set) | NO |
| Geographic Distribution (6, Q-40) | CONDITIONAL | MET (FL $1.0M dominates; non-uniform) | YES |
| Velocity Deceleration (7, Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (0 rows) | NO |
| Reorder Velocity & Early Warning (8, Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| Account Velocity Deceleration Alert (8b, Q-14b) | CONDITIONAL | NOT MET (Q-14b absent; HAS_PORTAL_ORDERS=False) | NO |
| Untapped Category Opportunities (9, Q-57) | CONDITIONAL | NOT MET (gates false; Q-57 absent) | NO |
| Buyer-Within-Account Intelligence (10, Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| Geographic Revenue Trends (11, Q-67) | CONDITIONAL | NOT MET (gates false; Q-67 absent) | NO |
| Spending Contraction (12, Q-68) | CONDITIONAL | NOT MET (gates false; Q-68 absent) | NO |
| Section-Level What-This-Means | MANDATORY | MET | YES |

## Mini-brief account selection (top_accounts.md returned 0 rows)
Built from Q-14 ranked by eCat GMV (strongest available account signal):
1. Wilson Fans & Lighting ($133,514 LTM, 7 orders, 39d cadence)
2. Platinum Imports Inc ($112,746 LTM, 6 orders, 47d cadence)
3. Dans Fan City ($76,044 LTM, 10 orders, 34.2d cadence)
4. Lighting First ($57,515 LTM, 5 orders, 51.3d cadence)
5. Krichel Inc DBA Fan And Lighting World ($54,536 LTM, 10 orders, 24.2d cadence)
Accounts 6–10 (collapsed): Metro Electric Supply, Valencia Lighting & Fans,
North Valley Fans And Blinds, Lightstyle Of Orlando, Mclaren Lighting.

Engagement Score: computed from Recency / Frequency / Monetary / Trajectory per guide.
Trajectory dimension is conservative (no Q-ORG-VELOCITY/CONTRACTION data → treated as neutral/0).
