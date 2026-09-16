# Section 02 Build Plan — Account Intelligence

Section: §2 accounts — Account Intelligence
Confidence tier (SECTION_CONFIDENCE_2): **FULL** → template `§2-FULL`, label `FULL PICTURE`

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=FULL) | YES |
| 3. Top 10 Mini-Briefs (top_accounts) | MANDATORY | MET (10 accounts) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET gate but THIN DATA (1 row, state=Unknown) → render as inline callout per Data Presentation thin-data rule, not full multi-state table | YES (degraded) |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| 5. Unactivated High-Value Accounts (Q-53) | CONDITIONAL | MET (SIG-OPP-02 fired; Q-53 = 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set surfaced; HAS_CART=false but no flagged set provided) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (FL=$6.2M of eCat, concentration > 30% of top states; non-uniform) | YES |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 = 20 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b = 15 rows) | YES |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | MET (SIG-RISK-02; Q-17/Q-17-atrisk rows exist) | YES |
| 7. Velocity Deceleration / Contracting YoY (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04; 25 rows) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT; 20 rows). State col all "Unknown" → suppress State column | YES (collapsed) |

## Mini-brief component map (top 10)

1. Graybar Electric — DECAY-01 (3.0x) + DECAY-04/contraction (total -59.4% YoY $186K→$75.8K). Header + Reorder Decay + Competitive Displacement (eCat -14.8%, total -59.4%; >25% decline & >$50K prior → hypotheses required) + Priority.
2. Lighting Design Center — DECAY-04 (contraction, total -39.2% YoY) + MOM-01 (accel). Header + Spending Trajectory + Priority. (>25%? 39.2% yes, prior $247K>$50K → hypotheses.)
3. Fan & Lighting World — DECAY-04 (total -28.6% YoY $193.6K→$138.2K) + MOM-01. Header + Spending Trajectory + Priority. (28.6%>25%, prior>$50K → hypotheses.)
4. The Hotel Design Group — DECAY-01 (30.7x). Header + Reorder Decay + Priority.
5. Tode Rubenstein — DECAY-01 (4.1x), $411K. Header + Reorder Decay + Priority.
6. ILC Studios — DECAY-01 (8.1x), $159K. Header + Reorder Decay + Priority.
7. Beyer Brown — DECAY-01 (2.7x), $470.8K. Header + Reorder Decay + Priority.
8. Value Lighting Inc. — DECAY-01 (3.5x), $168K. Header + Reorder Decay + Priority.
9. Burk Design Group — DECAY-01 (11.5x), $45.4K. Header + Reorder Decay + Priority.
10. Main Electric Supply Co. — DECAY-01 (3.0x), $155.4K. Header + Reorder Decay + Priority.

NBP (Q-ORG-NBP): top-10 accounts not present in NBP customer list → omit companion-products component for all mini-briefs (no NBP row matches Graybar/Hotel Design/etc.).
Stock-out (Q-ORG-STOCKOUT): not present → omit Stock-Out component everywhere.

Engagement scores computed per guide formula (Recency/Frequency/Monetary/Trajectory). Org 90th-pctile frequency ~ top Q-14 (133 orders); monetary 90th-pctile ~ high-$ accounts. Scores assigned conservatively from available LTM revenue, last-order recency, YoY trajectory.

## Forbidden-term check
No ERP / portal orders / health score / segment labels / platform(standalone) / customer_code in output. State="Unknown" columns suppressed.
