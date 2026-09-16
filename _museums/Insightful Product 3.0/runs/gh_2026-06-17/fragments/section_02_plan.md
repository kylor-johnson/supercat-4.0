# Section 02 Build Plan — Account Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| Top 10 Accounts by Signal Density (mini-briefs) | MANDATORY | MET (top_accounts.md has 10 rows) | YES |
| eCat Penetration of Total Business (3b, Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 = 30 rows) | YES |
| Geographic Revenue Trends (11, Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-67 = 25 rows) | YES |
| Buyer-Within-Account Intelligence (10, Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| Untapped Category Opportunities (9, Q-57) | MANDATORY when gate met | NOT MET (Q-57 row count = 0, no data) | NO |
| Unactivated High-Value Accounts (5, Q-53) | CONDITIONAL | MET (SIG-OPP-02 fired; Q-53 = 20 rows) | YES |
| Enterprise Channel Accounts (5b) | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set; SHOWROOM_EXCLUSIONS=0) | NO |
| Geographic Distribution (6, Q-40/Q-54) | CONDITIONAL | NOT MET (distribution broad; TX top at ~17% of GMV < 30% threshold) | NO |
| Reorder Velocity & Early Warning (8, Q-14) | MANDATORY | MET (Q-14 = 20 rows) | YES |
| Account Velocity Deceleration Alert (8b, Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b = 15 rows) | YES |
| Dormant High-Value Accounts (4, Q-17) | CONDITIONAL | MET (SIG-RISK-02 / Q-17-atrisk = 20 rows) | YES |
| Velocity Deceleration / Contracting YoY (7, Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04 fired; 25 rows) | YES |
| Spending Contraction Detection (12, Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, Q-68 = 20 rows) | YES |
| Section-Level What-This-Means | MANDATORY | MET | YES |

## Mini-brief components fired per account
- Green Front (Champion 87): Trajectory (contraction -37.6% total / +8.2% eCat), Companion (Alexandra Dresser SCH-166295, 164 cust), Reorder Decay (2.9x), Stock-Out ($80.6K across 14 items), Priority.
- Walter E. Smithe (Strong 61): Trajectory (-43.8% total), Reorder Decay (3.1x), Stock-Out ($17.9K), Priority.
- Elle Design (Strong 64): Trajectory ACCELERATING lead (+965.8% QoQ, 2 accel quarters), Reorder Decay (2.7x), Stock-Out ($7.4K), Priority.
- Gadsden Lighting (Moderate 45): Trajectory (-24.4% total), Reorder Decay (2.8x), Stock-Out ($10.1K), Priority.
- HCD Design (Moderate 59): Reorder Decay LEAD (20.9x — top org decay signal), Priority.
- Cultivated (Moderate 45): Reorder Decay (9.9x), Priority.
- Hollace Clare (Moderate 45): Reorder Decay (5.7x), Priority.
- Littman Bros (At Risk 10): Trajectory contraction LEAD (-72.3% total, $629,568 gap) + competitive hypotheses (M requirement met), Priority.
- Donna's Homefurniture (At Risk 18): Trajectory contraction (-77% total) + hypotheses, Priority.
- Cara Brock (Cooling 22): Trajectory contraction (-79.5% total) + hypotheses, Priority.

## Notes
- Stock-out table: suppress `qty_on_backorder` and `next_scheduled_receipt_date` columns (both "—" for every row).
- Q-66 absent + HAS_BUYER_DATA=false → subsection 10 correctly skipped.
- Q-57 zero rows → subsection 9 correctly skipped (gate condition: data rows must exist).
- Geographic Distribution (6) skipped: no single state ≥30% of GMV. Q-67 (11) covers geographic intelligence.
