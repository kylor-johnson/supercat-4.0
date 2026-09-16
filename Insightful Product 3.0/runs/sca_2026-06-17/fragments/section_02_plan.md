# Section 02 Build Plan — Account Intelligence

Tier: SECTION_CONFIDENCE_2 = **STRONG** (no LAST_PORTAL_ORDER_DATE resolvable → §2-PARTIAL template body, STRONG VIEW label per fallback rule).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics | MANDATORY | MET (Q-12 row present: 2,782 total, 100 active 12mo, 46 active 90d) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (top_accounts.md: 1 account — GDC) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY-when-gate | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 25 rows; $15K+/90d+ silent: GDC, Gary Riggs, Bay Design Store) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (AL = $377K = 33% of $1.14M eCat GMV > 30% concentration) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 10 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY-when-gate | NOT MET (HAS_PORTAL_ORDERS=False; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY-when-gate | NOT MET (gates false; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY-when-gate | NOT MET (gates false; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY-when-gate | NOT MET (gates false; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

Rendered subsections: Header Metrics, Confidence Header, Top 10 Mini-Briefs (GDC), Dormant High-Value Accounts, Geographic Distribution, Reorder Velocity & Early Warning, section what-this-means.

Computed values:
- Total eCat GMV (Q-40 sum) = $1,135,183 (~$1.14M)
- Avg LTM revenue per active 12mo account = $1,135,183 / 100 = $11,352
- AL concentration = $377,020 / $1,135,183 = 33.2%
- GDC Engagement Score = Recency 15 + Frequency 20 + Monetary 25 + Trajectory 5 = 65 → .badge.ok "Strong"
