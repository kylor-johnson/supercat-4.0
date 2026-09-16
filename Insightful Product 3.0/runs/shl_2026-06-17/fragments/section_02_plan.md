# Section 02 Build Plan — Account Intelligence

Client: Savoy House Lighting (shl) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_2): **STRONG** → label "STRONG VIEW".
LAST_PORTAL_ORDER_DATE unresolvable (PORTAL_ORDERS_FRESH=False, days_since=9999) → use §2-PARTIAL template text body; keep STRONG label per tier value.
ACCOUNT_COUNT = 1,353 total accounts (Q-12).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12: 1,353 total / 320 active 12mo / 48 active 3mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG) | YES |
| 3. Top 10 Mini-Briefs (top_accounts) | MANDATORY | MET (10 accounts) | YES (top 5 open, 6–10 collapsed) |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true + PORTAL_CUSTOMER_DATA_PRESENT=true, 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL (SIG-OPP-02) | MET (Q-53: 20 rows; SIG-OPP-02 rank #1) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set provided) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL (non-uniform) | NOT MET (TX top state = $562K of ~$2.7M eCat ≈ 21%, < 30%; no single dominant state) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14: 20 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) | YES (nested in 8) |
| 4. Dormant High-Value (Q-17) | CONDITIONAL (SIG-RISK-02) | MET (Q-17: 25 rows ≥ $15K + 90d+ silent) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL (SIG-DECAY-04) | MET (25 rows, multiple >20% YoY decline >$50K) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true + PORTAL_CUSTOMER_DATA_PRESENT=true, 20 rows) | YES (collapsed, last) |
| Section-level what-this-means | MANDATORY | — | YES |

## Render order (narrative arc): 1 → 2 → 3 (+3b) → 11 → 5 → 8 (+8b) → 4 → 7 → 12 → section what-this-means

## Notes
- Q-57 (subsection 9) and Q-66 (subsection 10) correctly skipped: 0 rows / not present.
- Subsection 6 skipped: distribution is not non-uniform enough (no state > 30% of eCat GMV).
- Mini-briefs use TARGET STRUCTURE form (.metrics/.metric/.metric-value, .sub-label, .callout) — gold wins over prose-guide metric set.
- Mini-brief accounts (top_accounts.md): 1 Dement Lighting, 2 Shades Of Light, 3 Hermitage Lighting Gallery, 4 Elements, 5 Lighting Connection Lp, 6 Plumbing Distributors Inc dba PDI, 7 Lamps.com, 8 Graham's Lighting Inc, 9 The Brecher Co. Inc, 10 Aztec Lighting Inc.
- Competitive Hypothesis (Section M) required for: Shades Of Light (-40.8% YoY, $1.7M), Lighting Connection Lp (-64.0% YoY, $334K) — both >25% decline & >$50K.
