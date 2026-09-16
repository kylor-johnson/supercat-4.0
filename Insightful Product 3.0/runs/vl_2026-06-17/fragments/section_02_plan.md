# Section 02 Build Plan — Account Intelligence

**Client**: Ciana Varaluz LLC (vl) · Run date 2026-06-17
**Confidence tier**: SECTION_CONFIDENCE_2 = `FULL` → template `§2-FULL`, label `FULL PICTURE`

## Pre-Build Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row: 1,851 customers, 66 active 12mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2=FULL) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (account-level signals across Q-14/Q-17/Q-ORG-VELOCITY/NBP/STOCKOUT) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS+PORTAL_CUSTOMER_DATA_PRESENT, Q-67 20 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | MET (HAS_PORTAL_ORDERS+HAS_BUYER_DATA, Q-66 20 rows) | YES |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows → omit per "zero rows" exception) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (Q-53 20 rows, $50K threshold loose — render top unactivated) | YES |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (TX+AZ+FL concentration; TX 17%, top 5 states ~62%) | YES |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (Q-14 6 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b 15 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 25 rows ≥ $15K, 90d+ silent) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION = 0 rows) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS+PORTAL_CUSTOMER_DATA_PRESENT, Q-68 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set provided) | NO |

## Notes
- `top_accounts.md` is degenerate (1 row = NBP item code 557P08HG, not an account). Mini-briefs built from strongest account-level signals across Q-14 (eCat leaders), Q-17 (dormant high-value), Q-ORG-VELOCITY (trajectory), Q-ORG-NBP (companion), Q-ORG-STOCKOUT (fulfillment gap), Q-14b (deceleration).
- Reorder Decay mini-brief component skipped: Q-ORG-DECAY = 0 rows.
- Competitive Displacement mini-brief component skipped: Q-ORG-CONTRACTION = 0 rows.
- Render order per narrative arc: metrics → confidence → mini-briefs → 3b → 11 → 10 → 5 → 6 → 8(+8b) → 4 → 12.
