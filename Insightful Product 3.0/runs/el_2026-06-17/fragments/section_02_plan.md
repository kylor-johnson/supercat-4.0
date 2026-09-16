# Section 02 Build Plan — Account Intelligence

Confidence tier: **SECTION_CONFIDENCE_2 = FULL** → template `§2-FULL`, label `FULL PICTURE`.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present: 1,985 total / 144 active 12mo / 12 active 3mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2=FULL) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (top_accounts.md has 6 real signal accounts) | YES (5 standalone briefs from real accounts: Ferguson, La Cie d'Eclairage Union, Litemode, Luminaire & Cie, Ocean Pacific) |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 has 30 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02 set: Q-17 25 rows, $15K+ / 90d+) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (SIG-OPP-02: Q-53 20 rows, $50K+ zero eCat) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set surfaced; HAS_CART=false but no 500+ order zero-eCat accounts flagged) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (ON = $1.3M total business, dominant concentration) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04: Litemode -47.5% YoY, LTM $409K) | YES |
| 8. Reorder Velocity (Q-14) | MANDATORY (always) | Q-14 has 0 rows AND Q-14b has 0 rows → no data to render; per Data Presentation Rules "handle thin data gracefully" the empty-table subsection is skipped (chrome with no content), gap noted here | NO |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | NOT MET (Q-14b has 0 rows) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 has 0 rows) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT; Q-67 20 rows) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (Q-68 3 rows) | YES (collapsed) |
| Section-level what-this-means | MANDATORY | MET | YES |

## Mini-brief account reconciliation

top_accounts.md lists 6 rows but two are not real accounts ("46818-034" is an item code from the NBP signal; "9 accounts" is the SIG-OPP-02 aggregate). Real signal accounts with usable data:

1. **Ferguson Enterprises** (VA) — SIG-MOM-01 acceleration (lead/positive). Velocity + NBP + displacement data.
2. **La Cie d'Eclairage Union-Showroom** (QC) — SIG-MOM-01 acceleration (positive). Velocity + NBP + displacement.
3. **Litemode Ltd** (ON) — SIG-DECAY-04 contraction (risk). Contraction + NBP. >25% decline + >$50K → competitive hypotheses required.
4. **Luminaire & Cie - Showroom** (QC) — SIG-ANOMALY-03 displacement (risk). NBP + displacement.
5. **Ocean Pacific Lighting** (BC) — SIG-ANOMALY-03 displacement (risk). Displacement.

Accounts 6–10: no further distinct signal accounts exist (only 6 in manifest, 2 non-accounts). Collapsed 6–10 block omitted — fewer than 6 real accounts. Render the 5 real mini-briefs standalone.
