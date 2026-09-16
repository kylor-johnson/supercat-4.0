# Section 02 Build Plan — Account Intelligence

Client: Vaxcel International Corporation (vic) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_2): **STRONG** → template `§2-STRONG`, label `STRONG VIEW`

## Gate inputs
- HAS_PORTAL_ORDERS = True
- PORTAL_CUSTOMER_DATA_PRESENT = True
- HAS_BUYER_DATA = False
- PORTAL_REP_DATA_PRESENT = False

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG tier) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (named accounts available) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false, Q-66 absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (SIG-OPP-02, 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; HAS_CART=true) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (eCat distribution thin, no >30% single-state concentration worth a table; Q-67 covers geography) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (10 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS, 15 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02, 6 rows) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04, 6 rows) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 20 rows) | YES |

## Mini-brief accounts (signal-density order, real named accounts only)
top_accounts.md rows 5 ("C0281", an item) and 6 ("20 accounts", an aggregate) are NOT account
entities → excluded from mini-briefs (covered by 3b/5/9 instead). Real named accounts:
1. HomeDepot.com (DECAY-04 contraction; item-level decay; NBP not present for HD)
2. Menards DC DIST #3039 (DECAY-04 -78.4%; deceleration; contraction-vs-peak)
3. Ace Hardware Corporation (MOM-01 acceleration — LEAD positive)
4. Walmart.com (MOM-01 acceleration; NBP companion)
5. Belami, Inc. (DECAY-04 -25.1%)
Accounts 6-10 (collapsed): Lighting New York (DECAY-04 -25.5%), Cast Antlers (-25%), The Cabin Place (-20.5%).

## Render order (narrative arc)
Header → Confidence → Mini-briefs → 3b Penetration (INTEL) → 11 Geo Trends (INTEL) →
5 Unactivated (OPP) → 8 Reorder Velocity + 8b Deceleration → 4 Dormant (RISK) →
7 Contracting YoY (RISK) → 12 Spending Contraction (RISK, collapsed) → section what-this-means.
