# Section 02 Build Plan — Account Intelligence

Client: Currey & Company (cci) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_2): **FULL** → template `§2-FULL`, label "Full Picture"
Account count: 38,964 total ERP customers · Last portal order: 2026-06-15 (2 days ago)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has data) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=FULL) | YES |
| 3. Top 10 Mini-Briefs (top_accounts) | MANDATORY | MET (10 rows) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (SIG-RISK-02, Q-17 25 rows) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | MET (SIG-OPP-02, Q-53 20 rows) | YES |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set surfaced) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (FL leads; non-uniform; Q-40/Q-54 data) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | MET (SIG-DECAY-04, contraction rows) | YES |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (Q-14 20 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) | YES |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 = 0 rows / no data) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | MET (HAS_PORTAL_ORDERS + HAS_BUYER_DATA, 20 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 25 rows) | YES |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 20 rows) | YES |

## Render order (narrative arc)
Header → Confidence → Mini-Briefs → 3b eCat Penetration → 11 Geo Trends → 10 Buyer-Within → 5 Unactivated → 6 Geo Distribution → 8/8b Reorder Velocity + Deceleration → 4 Dormant → 7 Velocity Deceleration → 12 Spending Contraction (collapsed). Section-level what-this-means last.

## Note
- Subsection 9 (Q-57) SKIPPED: file returned 0 rows. Mandatory-when-gate-met gate is not satisfied (no data rows). Mini-brief B2 Wallet whitespace paragraph also omitted (no Q-57 data); wallet position rendered from Q-52 only.
