# Section 02 Build Plan — Account Intelligence

Confidence tier: SECTION_CONFIDENCE_2 = **FULL** → `§2-FULL` / label "FULL PICTURE"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row: 4,423 total / 310 active 12mo / 132 active 3mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2 = FULL) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (top_accounts.md has 10 rows) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 has 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true + PORTAL_CUSTOMER_DATA_PRESENT=true, Q-67 has 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true + HAS_BUYER_DATA=true, Q-66 has 20 rows) | YES |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 row count = 0, no data) | NO |
| 5. Unactivated High-Value Accounts (Q-53) | CONDITIONAL | MET (SIG-OPP-02 fired, Q-53 has 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; HAS_CART=true) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (BC = $5.8M of ~$17.6M eCat ≈ 33% > 30% concentration) | YES |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-14b has 11 rows) | YES |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | MET (SIG-RISK-02; Q-17-atrisk has 20 rows ≥$15K, 90+ days) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04; CONTRACTING rows, LTM>$50K) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true + PORTAL_CUSTOMER_DATA_PRESENT=true, Q-68 has 10 rows) | YES |
| Section-level what-this-means | MANDATORY | MET | YES |

## Render order (narrative arc):
Header Metrics → Confidence Header → Top 10 Mini-Briefs → 3b eCat Penetration (INTEL) → 11 Geographic Revenue Trends (INTEL) → 10 Buyer-Within-Account (INTEL) → 5 Unactivated High-Value (OPP) → 6 Geographic Distribution (neutral) → 8 Reorder Velocity + 8b Deceleration → 4 Dormant High-Value (RISK) → 7 Velocity Deceleration (RISK) → 12 Spending Contraction (RISK, collapsed) → section what-this-means.

## Notes
- §9 (Q-57) SKIPPED: 0 rows. Gate condition "data rows exist" not met.
- Mini-brief form follows TARGET STRUCTURE gold shape (metrics: All-Channel LTM / eCat LTM / Reorder Velocity / Engagement Score; companion products; trajectory/decay/displacement callouts; Pre-Meeting Priority).
- Competitive Hypothesis (Shared Rules M) triggers for accounts with >25% YoY decline AND >$50K: applied in §7 (Stevans, Harp Team, KM-Associates, Clutch) and mini-briefs where displacement fired.
