# Section 02 Build Plan — Account Intelligence

Client: Geo Contemporary (gcl), run 2026-06-17.
Confidence: `SECTION_CONFIDENCE_2` = "—" (no tier resolved). FULL/STRONG require
`{{LAST_PORTAL_ORDER_DATE}}`, which cannot be resolved (HAS_PORTAL_ORDERS=False).
Per guide fallback rule → use `§2-PARTIAL` template, label **PARTIAL VIEW**.

Key gates: HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False,
HAS_BUYER_DATA=False. All portal/ERP-enriched subsections gate OUT. Only
eCat-native cache files (Q-12, Q-14, Q-17, Q-40) carry data. All Q-ORG-* files
are empty/zero → mini-briefs reduce to header + priority (no trajectory, NBP,
decay, stock-out, displacement components fired). top_accounts.md is empty →
mini-brief accounts selected by eCat GMV from Q-14 (signal-density manifest blank).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has data) | YES |
| 2. Data Confidence Header | MANDATORY | MET (PARTIAL fallback) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (Q-14 substitutes for empty top_accounts) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17/Q-17-atrisk have data) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (Canadian cluster ~45% of eCat GMV) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has data) | YES |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (Q-14b absent; HAS_PORTAL_ORDERS=False) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (gates False; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (gates False; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (gates False; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

Rendered: Header Metrics, Confidence Header, Top 10 Mini-Briefs (5 + collapsed 6-10),
Dormant High-Value Accounts, Geographic Distribution, Reorder Velocity & Early Warning,
section-level what-this-means.
