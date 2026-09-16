# Section 02 Build Plan — Account Intelligence

**Client:** Coleto Brands | Progress Lighting (prog) · Run 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_2):** STRONG → template `§2-STRONG`, label "STRONG VIEW"

## Key gate facts
- HAS_PORTAL_ORDERS = **False**
- PORTAL_CUSTOMER_DATA_PRESENT = **False**
- HAS_BUYER_DATA = **False**
- `top_accounts.md` has **zero rows** (signal-density pass returned no accounts). Mini-briefs are
  derived from the strongest available account-level data (Q-14 reorder GMV + Q-17 dormant GMV).
- All Q-ORG-* files empty/zero. Q-52/53/54/57/66/67/68 absent.

## Pre-Build Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (derived from Q-14/Q-17 GMV; top_accounts empty) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; file absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 25 rows; ≥$15K, 90+d silent: ROYAUME $34,552, CITY LIGHTZ $19,261) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (file absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (QC $60,018 >30% of eCat GMV — non-uniform) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file empty) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (Q-14 4 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=false; file absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (both gates false; file absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; file absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | NOT MET (both gates false; file absent) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | NOT MET (both gates false; file absent) | NO |

## Render order (narrative arc)
Header Metrics → Confidence Header → Top Mini-Briefs → Geographic Distribution (intelligence/neutral)
→ Reorder Velocity (early warning) → Dormant High-Value (risk) → Section what-this-means.
