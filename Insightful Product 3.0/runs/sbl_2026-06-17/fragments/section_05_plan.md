# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=1, ENGAGEMENT_REP_COUNT=69).
Rep Leaderboard built from app selling-activity in Q-01 Step 1, ranked by Total Events.
**Confidence tier**: SECTION_CONFIDENCE_5 = PARTIAL → §5-PARTIAL, label "PARTIAL VIEW".
**ADMIN_REPS_IN_LEADERBOARD** = False → no admin disclosure in header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — engagement mode, Q-01 Step 1 has 118 rows | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET — coaching_candidates.md lists 1 (Brad Krieger, $128,469) | YES |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET — PORTAL_REP_DATA_PRESENT=False, Q-51 absent | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=True | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has 20 data rows | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has 96 rows w/ QoQ data | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 empty (0 rows), no dormant value | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=False, Q-62 absent | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=False, Q-64 absent | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 spread 83.9%−61.3% = 22.6pp > 20pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=False, Q-70 absent | NO |

**Rendered subsections (in narrative-arc order)**: Rep Leaderboard → Coaching Opportunities → Behavioral Archetypes → Presentation-to-Close Conversion → Engagement Trajectory → How Reps Spend Their Time in the App → section-level what-this-means.
