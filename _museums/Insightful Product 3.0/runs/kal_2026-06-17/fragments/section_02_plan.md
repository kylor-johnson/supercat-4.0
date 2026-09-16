# Section 02 Build Plan — Account Intelligence

Section: §2 Account Intelligence (id: accounts)
Confidence tier: SECTION_CONFIDENCE_2 = FULL → label "Full Picture", template §2-FULL

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=FULL) | YES |
| 3. Top 10 Mini-Briefs (top_accounts) | MANDATORY | MET (10 accounts) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS+PORTAL_CUSTOMER_DATA_PRESENT, 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | MET (HAS_PORTAL_ORDERS+HAS_BUYER_DATA, 20 rows) | YES |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (SIG-OPP-02 fired, 20 rows) | YES |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | NOT MET (no single state >30% of eCat GMV; distribution spread — skipped per uniform rule) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (17 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02 / at-risk rows exist) | YES |
| 7. Velocity Deceleration / Contracting YoY (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04 fired) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS+PORTAL_CUSTOMER_DATA_PRESENT, 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (HAS_CART=true → ENTERPRISE_CHANNEL gate requires HAS_CART=false; set empty) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Render order (narrative arc: intelligence → opportunity → risk)
1. Header Metrics
2. Data Confidence Header (FULL)
3. Top 10 Mini-Briefs (top 5 open, 6–10 collapsed)
4. 3b eCat Penetration (INTELLIGENCE)
5. 11 Geographic Revenue Trends (INTELLIGENCE)
6. 10 Buyer-Within-Account (INTELLIGENCE)
7. 5 Unactivated High-Value (OPPORTUNITY)
8. 8 Reorder Velocity + 8b Deceleration Alert (early warning)
9. 4 Dormant High-Value (RISK)
10. 7 Contracting YoY (RISK)
11. 12 Spending Contraction (RISK, collapsed)
12. Section what-this-means

## Mini-brief account mapping (from top_accounts.md, signal density order)
1. LUX LIGHTING LTD — MOM-01 (accel, peak $56,060 +650.6% QoQ) + DECAY-04 (contraction -57.9% YoY) + Q-14b decel 3.29x. Lead positive (trajectory), then contraction recovery.
2. DESIGNER LIGHTING & FAN/DECOR — MOM-01 (accel, peak $55,467) + ANOMALY-03 competitive displacement (total +58.1% YoY, eCat -100%).
3. SPACIAL EFX — DECAY-01 (3.7x gap, 111d) + item-level decay rows. Reorder pattern change.
4. DOLAN NORTHWEST LLC PORTLAND — DECAY-04 (-77.1% YoY, $401,733 gap) — competitive hypothesis required (>25%, >$50K).
5. SHADES OF LIGHT — DECAY-04 (-50.9% YoY, $204,290 gap) — competitive hypothesis required.
6-10 (collapsed): LAMPS PLUS (DECAY-04 -27.9%), LIGHTING NEW YORK INTERNET (DECAY-04 -23%), LIGHTING WORLD DECORATOR (DECAY-04 -26.3%), CAPITOL LIGHTING--E. HANOVER (DECAY-04 -34.5%), LIGHTSTYLE OF ORLANDO (DECAY-04 -35.6%).
