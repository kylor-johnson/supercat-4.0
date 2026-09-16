# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=1, ENGAGEMENT_REP_COUNT=28).
Leaderboard built from app selling-activity in Q-01 Step 1 (ranked by Total Events),
NOT order GMV (~$131K eCat across 11 reps, would be empty/misleading).

**Confidence tier**: `SECTION_CONFIDENCE_5 = FULL` → `§5-FULL` / "Full Picture".
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` → disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 28 engagement reps) | MET — engagement mode, Q-01 Step 1 present (51 rows) | YES |
| Coaching Opportunities | CONDITIONAL (≥1 candidate) | NOT MET — coaching_candidates.md lists 0 candidates (0 converting) | NO |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-51 absent | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has 8 rows; MIXPANEL_USER_DATA_PRESENT=true | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data (37 rows) | YES |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | NOT MET — Q-62 has 0 rows | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | MET — Q-64 has 20 rows; HAS_PORTAL_ORDERS=true | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 spread 0%–59.4% = 59.4pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET — Q-43 absent / Q-43-S2 0 rows; PORTAL_REP_DATA_PRESENT=false | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET — Q-70 absent; PORTAL_REP_DATA_PRESENT=false | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

**Username→display-name** resolved via Q-01 Step 2 / Q-06 / Q-04. Raw usernames never rendered.
Admin/support accounts (Customer Support, Sholeh Duncan) included in app-activity counts per
showroom scan (0 flagged) but disclosed in confidence header.
