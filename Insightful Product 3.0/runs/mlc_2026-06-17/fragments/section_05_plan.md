# Section 05 Build Plan — Team Intelligence

**Mode:** ENGAGEMENT (`SALES_SECTION_MODE = engagement`; order_reps=4 < 5, ENGAGEMENT_REP_COUNT=33).
Leaderboard built from app selling-activity (Q-01 Step 1), ranked by Total Events.

**Confidence tier:** SECTION_CONFIDENCE_5 = PARTIAL → template `§5-PARTIAL`, label "PARTIAL VIEW".
**Admin disclosure:** ADMIN_REPS_IN_LEADERBOARD = true (Kevin Chang) → disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — ENGAGEMENT mode, Q-01 S1 has 53 rows | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 candidates | NO (skip entirely) |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-51 not present | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close (2b) | CONDITIONAL | MET — Q-63 has rows (2 reps with 50+ presentations) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, HAS_NEW_ITEMS=false, Q-62 absent | NO |
| Rep Engagement vs Revenue (7) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-64 absent | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET — Q-65 has 19 rows, spread 84.8%−14.3%=70.5pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43/Q-43-S2 returned 0 rows | NO |
| Inactive Reps w/ Territory Revenue (9) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-70 absent | NO |
| Section-level what-this-means | MANDATORY | — | YES |

**Rendered subsections:** Rep Leaderboard, Behavioral Archetypes, Presentation-to-Close Conversion, Engagement Trajectory, How Reps Spend Their Time in the App.
