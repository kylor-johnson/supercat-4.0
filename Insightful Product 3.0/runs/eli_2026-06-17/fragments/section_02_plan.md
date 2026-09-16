# Section 02 Build Plan — Account Intelligence

Confidence tier: SECTION_CONFIDENCE_2 = **STRONG** (label "Strong View"). No portal-order
date resolvable (HAS_PORTAL_ORDERS=False, portal_order_count=0) → confidence text uses
PARTIAL-style coverage content per fallback rule, label remains "Strong View".

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built from Q-14 eCat GMV; top_accounts.md empty, Q-ORG-* empty so arc components skipped silently) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL (mandatory when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-67 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-57 absent) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; HAS_CART=True) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (clear NY/NJ + international cluster; Q-40 has 20 rows) | YES |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | CONDITIONAL (mandatory when gate met) | NOT MET (Q-14b absent; HAS_PORTAL_ORDERS=False) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 25 rows; $15K+ / 90d+ accounts present) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION absent/0 rows) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-68 absent) | NO |

Render order (per guide narrative arc, filtered to rendering subsections):
Header → Confidence → Mini-Briefs (1-10) → Geographic Distribution → Reorder Velocity → Dormant High-Value → section what-this-means.

Notes:
- No YoY data available per account → omit YoY metric-note rather than fabricate.
- No Q-ORG trajectory/NBP/decay/displacement/stockout data → mini-brief arc components skipped silently per spec.
- Engagement Score computed from Recency + Frequency + Monetary; Trajectory dimension unscored (no YoY) → set to 10 (neutral, -10%–0% band) conservatively.
