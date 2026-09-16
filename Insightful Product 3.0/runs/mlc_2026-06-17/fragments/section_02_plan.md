# Section 02 Build Plan — Account Intelligence

Run: mlc_2026-06-17 · Confidence tier (SECTION_CONFIDENCE_2): **STRONG**

## Key gate states
- HAS_PORTAL_ORDERS = **False** → 3b, 8b, 9, 11, 12 NOT rendered
- PORTAL_CUSTOMER_DATA_PRESENT = **False** → 3b, 9, 11, 12 NOT rendered
- HAS_BUYER_DATA = **False** → 10 NOT rendered
- top_accounts.md = **EMPTY** (0 rows); Q-ORG-VELOCITY/CONTRACTION/NBP/STOCKOUT/DECAY all 0 rows
  → mini-briefs built from strongest available account data (Q-14 active eCat buyers + Q-17 dormant context). No trajectory/companion/decay/displacement components (signals did not fire).
- QC = 35.9% of eCat GMV (>30%) → Geographic Distribution (6) renders.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has data) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built from Q-14/Q-17; top_accounts empty) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (gate false + file absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (gate false + file absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (gate false + file absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (gate false + file absent) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (file absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (QC 35.9% > 30%) | YES |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 5 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (gate false + file absent) | NO |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | MET (Q-17/Q-17-atrisk have rows) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (0 rows) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (gate false + file absent) | NO |

## Render order (narrative arc)
Header Metrics → Confidence Header → Mini-Briefs (3) → Geographic Distribution (6, intelligence) → Reorder Velocity (8) → Dormant High-Value (4, risk) → Section what-this-means.
