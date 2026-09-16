# Section 02 Build Plan — Account Intelligence

- **Client**: AFX, Inc. (afx, org_id=185)
- **Run date**: 2026-06-17
- **Section confidence (SECTION_CONFIDENCE_2)**: STRONG → falls back to §2-PARTIAL template (LAST_PORTAL_ORDER_DATE unresolved; HAS_PORTAL_ORDERS=false)
- **Key gates**: HAS_PORTAL_ORDERS=false, PORTAL_CUSTOMER_DATA_PRESENT=false, HAS_BUYER_DATA=false, HAS_INVENTORY=true, HAS_SALES_DATA=false

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row: 3,534 accounts, 49 active 12mo) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG → §2-PARTIAL fallback, no all-channel date) | YES |
| 3. Top 10 Accounts by Signal Density (mini-briefs) | MANDATORY | MET (top_accounts.md empty → built from highest-value eCat accounts via Q-17 / Q-17-atrisk) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 absent) | NO |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | NOT MET (SIG-RISK-02 did not fire; only 1 account ≥$15K — folded into mini-briefs) | NO |
| 5. Unactivated High-Value Accounts (Q-53) | CONDITIONAL | NOT MET (SIG-OPP-02 not fired; Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (Q-40 has 20 states; rendered for intelligence value) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION empty) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 1 row: Valley Lights) | YES |
| 8b. Account Velocity Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (Q-14b absent; HAS_PORTAL_ORDERS=false) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, PORTAL_CUSTOMER_DATA_PRESENT=false; Q-57 absent) | NO |
| 10. Buyer-Within-Account Intelligence (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, PORTAL_CUSTOMER_DATA_PRESENT=false; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, PORTAL_CUSTOMER_DATA_PRESENT=false; Q-68 absent) | NO |

## Build notes
- `top_accounts.md` returned 0 ranked rows (no multi-signal accounts; Q-ORG-DECAY/VELOCITY/CONTRACTION/NBP/STOCKOUT all empty). Mini-briefs built from the highest-value eCat accounts available (Q-17 dormant + Q-17-atrisk gmv_12mo / days_since), which is the only account-level revenue signal present.
- No YoY available (eCat ordering effectively began Jan 2026), so account headers omit YoY notes and show scope/recency instead. Trajectory dimension of Engagement Score scored neutral where no prior-year exists.
- Engagement Score computed per guide (Recency + Frequency + Monetary + Trajectory), labeled per badge table.
- Geographic table excludes the malformed "." state row (A.G. Electric, no state on file) and notes it in what-this-means.
- Positive narrative lead (43 new eCat buyers in Jan 2026, rep Emily Carpenter +18) carried in section-level what-this-means and highlights, since no momentum subsection gate is met.
