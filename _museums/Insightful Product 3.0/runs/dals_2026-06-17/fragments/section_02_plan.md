# Section 02 Build Plan — Account Intelligence

Tier: **SECTION_CONFIDENCE_2 = STRONG** (label "STRONG VIEW"). Template falls back
to §2-PARTIAL text because `{{LAST_PORTAL_ORDER_DATE}}` is unresolvable
(HAS_PORTAL_ORDERS=False); tier label remains STRONG per shared contract §2.

Key data posture: engagement-mode client, **0 portal orders**, top_accounts.md is
EMPTY (0 rows), Q-14 / Q-ORG-DECAY / Q-ORG-VELOCITY / Q-ORG-CONTRACTION /
Q-ORG-STOCKOUT all 0 rows or absent. The only account-level data with rows:
Q-12 (header metrics), Q-17 (2 dormant accounts), Q-40 (2-state geography).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| 3. Top 10 Mini-Briefs (top_accounts.md) | MANDATORY | NOT MET (top_accounts.md has 0 rows; Q-14/Q-ORG-* empty) | NO — render explanatory note in place |
| 3b. eCat Penetration (Q-52) | CONDITIONAL (mandatory when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 2 rows) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | NOT MET (only 2 rows, 1 customer each — thin; render as inline stat per Data Presentation Rules) | NO (skip table; folded into confidence/section note) |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY (always) | NOT MET (Q-14 has 0 rows; Q-14b absent) | NO — render explanatory note (no data) |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; file absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

Notes:
- Subsection 3 (mini-briefs) is normally MANDATORY, but its sole source
  (top_accounts.md) returned zero rows and every account-level signal query
  (Q-14, Q-ORG-DECAY, Q-ORG-VELOCITY, Q-ORG-CONTRACTION, Q-ORG-STOCKOUT) is empty.
  No mini-brief can be constructed without inventing data. Render a transparent
  no-data note in place rather than fabricating accounts.
- Subsection 8 (Reorder Velocity) is normally always-render, but Q-14 has 0 rows.
  Render a no-data note.
- Geographic data (Q-40) is 2 rows of 1 customer each → thin data per Data
  Presentation Rules; not rendered as a standalone table.
- Q-17 (Dormant) is the one account-level subsection with usable rows → renders.
