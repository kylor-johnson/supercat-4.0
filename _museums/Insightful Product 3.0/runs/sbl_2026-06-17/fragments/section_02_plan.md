# Section 02 Build Plan — Account Intelligence

**Client**: Schonbek Lighting (sbl) · Run date 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_2)**: STRONG → label "STRONG VIEW". No portal-order date available (HAS_PORTAL_ORDERS=false), so confidence text uses the non-portal STRONG variant.

## Gate Inputs
- HAS_PORTAL_ORDERS = **False** → 3b, 8b, 9, 10, 11, 12 all SKIP
- PORTAL_CUSTOMER_DATA_PRESENT = False → 3b, 9, 11, 12 SKIP
- HAS_BUYER_DATA = False → 10 SKIP
- top_accounts.md = EMPTY (0 rows) → mini-briefs constructed from Q-14 (reorder) + Q-17-atrisk (GMV/state/days) joined by eCat GMV rank
- Q-ORG-VELOCITY / CONTRACTION / NBP / DECAY / STOCKOUT = empty → no trajectory/companion/decay/stockout/displacement callouts inside mini-briefs
- Q-53/Q-54/Q-52/Q-57/Q-66/Q-67/Q-68 = absent

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built from Q-14/Q-17 by eCat GMV; top_accounts empty) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; file absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 25 rows, SIG-RISK-02 threshold $15K+/90d+) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (clear cluster: KY $328K from 2 customers; rendered compact) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (0 rows) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 6 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; file absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (gates false; absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (gates false; absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (gates false; absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

**Rendered subsections (narrative arc order)**: Header Metrics → Confidence Header → Top Mini-Briefs → Geographic Distribution (intelligence) → Reorder Velocity (early warning) → Dormant High-Value (risk).
