# Section 02 Build Plan — Account Intelligence (Bulbrite, bri)

Run date: 2026-06-17 · Confidence tier (SECTION_CONFIDENCE_2): **STRONG**
(LAST_PORTAL_ORDER_DATE unresolvable → §2-PARTIAL template wording, STRONG label per exact tier value)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12: 3,226 accounts, 334 active 12mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| 3. Top 10 Mini-Briefs (top_accounts.md) | MANDATORY | MET (10 accounts) | YES |
| 3b. eCat Penetration of Total Business (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (gates true, 1 row — thin data, rendered as inline national stat) | YES |
| 10. Buyer-Within-Account Intelligence (Q-66) | CONDITIONAL | NOT MET (Q-66 not present + HAS_BUYER_DATA=false) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 row count=0) | NO |
| 5. Unactivated High-Value Accounts (Q-53) | CONDITIONAL | MET (SIG-OPP-02 fired, 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (HAS_CART=true → exclusion set empty) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (no state >30%; UT top at ~18%) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14: 20 rows) | YES |
| 8b. Account Velocity Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) | YES |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | MET (5 accounts ≥$15K, 90+ days silent) | YES |
| 7. Accounts Contracting Year-Over-Year (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04 fired, 17+ accounts >$50K & >20% decline) | YES |
| 12. Spending Contraction Detection (Q-68) | MANDATORY when gate met | MET (gates true, 20 rows) | YES — [COLLAPSE] |

## Mini-brief accounts (signal density order, top_accounts.md)
1. Shades of Light — MOM-01 (eCat accel, 3 qtrs) + DECAY-04 (all-channel −28.7%) → LEAD positive
2. James & Company Lighting — MOM-01 + DECAY-04
3. Lumens Light & Living — DECAY-04 (−52.7%, $443K gap) — hypotheses
4. Progressive — DECAY-04 (−71.3%) + deceleration — hypotheses
5. Wayfair, LLC -Castlegate — DECAY-04 (−31.6%) — hypotheses
(6–10 collapsed) Lighting Design LLC, M & M Lighting-Houston (stock-out 773166), Wayfair LLC ***, Low Country Lighting, Coffman Home Decor

## Component availability notes
- Companion Products (Q-ORG-NBP): row count 0 → omit from all briefs
- Reorder Decay item table (Q-ORG-DECAY): row count 0 → omit
- Stock-Out Impact (Q-ORG-STOCKOUT): M&M Lighting (773166, $229,999), Lighting Design (773166, $20,735), Lumens (776869, $5,289)
- Competitive/decline hypotheses (Section M): rendered for accounts with >25% YoY decline AND >$50K
- Engagement Score: omitted (gold TARGET STRUCTURE uses data metric cards, not a score; org-percentile inputs unavailable)

## Suppressed columns (all-dashes / Unknown)
- State column suppressed in Q-52, Q-53, Q-ORG-CONTRACTION, Q-68 tables (all "—"/"Unknown")
- Q-67 state="Unknown" → rendered as national inline stat, not a state table
