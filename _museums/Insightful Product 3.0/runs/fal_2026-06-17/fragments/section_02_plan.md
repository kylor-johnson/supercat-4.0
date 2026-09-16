# Section 02 Build Plan — Account Intelligence

Confidence tier: SECTION_CONFIDENCE_2 = **STRONG** (template §2-STRONG, label "STRONG VIEW")

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (always; 4,752 total / 1,848 eCat-ever / 250 active 12mo / 137 active 90d) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (10 accounts in top_accounts.md) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (gate met but Q-57 row count = 0) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL (SIG-OPP-02) | MET (SIG-OPP-02 fired; 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | MET (Wayfair 5,013 orders, Kathy Kuo Home 540 orders — 500+ orders, 0 eCat, HAS_CART=false) | YES |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (no single state >30% of eCat GMV; TX leads at ~14%) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 20 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL (SIG-RISK-02) | MET (Q-17-atrisk 20 rows, $15K+ / 90d+) | YES |
| 7. Accounts Contracting YoY (Q-ORG-CONTRACTION) | CONDITIONAL (SIG-DECAY-04) | MET (Antique Purveyor -68.1% on $214K prior; competitive hypotheses required) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 20 rows) | YES |
| Section-level what-this-means | MANDATORY | MET | YES |

Render order (narrative arc INTELLIGENCE → OPPORTUNITY → RISK):
Header → Confidence → Top-10 Mini-briefs → 3b eCat Penetration → 11 Geo Trends → 5 Unactivated + 5b Enterprise Channel → 8 Reorder Velocity + 8b Deceleration → 4 Dormant → 7 Contracting YoY → 12 Spending Contraction (collapsed) → section what-this-means.

Engagement Score note: org active-12mo count = 250; avg LTM eCat rev per active ≈ $10.4K. 90th-pctile frequency ≈ 12 eCat orders, 90th-pctile monetary ≈ $55K eCat LTM (from Q-14 distribution). Scores computed per mini-brief account from recency/frequency/monetary/trajectory.
