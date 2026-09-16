# Section 02 Build Plan — Account Intelligence

Confidence tier (SECTION_CONFIDENCE_2): **STRONG** → template `§2-STRONG`, label "STRONG VIEW".

## Pre-Build Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2=STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (account signals from Q-ORG-VELOCITY + top_accounts) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=True, 30 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02; Q-17 has 25 rows) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (SIG-OPP-02; Q-53 has 20 rows, $50K+ candidates) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (HAS_CART=True → no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (top state FL $12.3K ≈ 9% of eCat; uniform, <30%) | NO |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION = 0 rows) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=True, 15 rows) | YES |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 not present) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | DEGENERATE (1 row, state="Unknown") → rendered as single inline stat per thin-data rule | YES (minimal) |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | NOT MET (Q-68 = 0 rows) | NO |
| Section-level What-This-Means | MANDATORY | MET | YES |

## Mini-Brief account selection

top_accounts.md lists 3 rows but #1 ("3164-FM BCB-HWG") is an item code (NBP anchor), not a customer.
Real account-level signals: MOM-01 accelerators (THE LIGHTING DESIGN CO., THE WELL APPOINTED HOUSE)
and the Q-ORG-VELOCITY trajectory set. Built 5 standalone mini-briefs from the strongest
accelerating accounts + 5 in collapsed 6–10 block, all from Q-ORG-VELOCITY (2-quarter accelerators),
enriched with NBP (Q-ORG-NBP), reorder decay (Q-ORG-DECAY-items), and stock-out (Q-ORG-STOCKOUT) where present.

## Notes
- Q-67 has a single "Unknown" state row — the QoQ breakout-vs-contracting headline cannot be built;
  rendered as one inline insight stat (total eCat QoQ movement) to honor the mandate while avoiding a
  degenerate 1-row table.
- No competitive-hypothesis blocks required: no account meets >25% YoY decline + >$50K LTM (contraction queries empty).
