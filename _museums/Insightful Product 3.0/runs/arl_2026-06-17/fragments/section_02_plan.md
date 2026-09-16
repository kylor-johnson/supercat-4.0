# Section 02 Build Plan — Account Intelligence

- **Client**: Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17
- **SECTION_CONFIDENCE_2**: STRONG → template `§2-STRONG`, label `STRONG VIEW`
- **Key gates**: HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False, HAS_BUYER_DATA=False, HAS_INVENTORY=True (stale 188d), HAS_SALES_DATA=False

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG tier) | YES |
| 3. Top 10 Mini-Briefs (top_accounts.md) | MANDATORY | MET (2 accounts present) | YES (2 briefs — only 2 accounts) |
| 3b. eCat Penetration (Q-52) | CONDITIONAL (mandatory when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 2 rows, SIG-RISK-02 style) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; SHOWROOM_EXCLUSIONS=0) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (only 2 states, thin; Q-54 absent) — render as compact inline stat | YES (compact, not full table) |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL (mandatory when gate met) | NOT MET (gates False; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL (mandatory when gate met) | NOT MET (gates False; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL (mandatory when gate met) | NOT MET (gates False; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Mini-brief components per account (only fired signals)
- **Beautiful Things Lighting & Accessories** (FL): Account header + Reorder Decay (Q-ORG-DECAY: 3.0x, 55d gap vs 18.6d avg) + Pre-Meeting Priority. No NBP/stockout/displacement data present (those Q files absent). Engagement Score ≈ 75 (Strong).
- **WAYFAIR** (MA): Account header + Reorder Decay (Q-ORG-DECAY: 4.6x, 79d gap vs 17.2d avg) + Pre-Meeting Priority. Engagement Score ≈ 73 (Strong).

Note: Spending Trajectory (B), Wallet (B2), Companion (C), Stock-Out (E), Displacement (F) all skipped — no source data (Q-ORG-VELOCITY/CONTRACTION/NBP/STOCKOUT absent, no portal data). Item-level decay table omitted (Q-ORG-DECAY_items absent → only account-level SIG-DECAY-01 fired).
