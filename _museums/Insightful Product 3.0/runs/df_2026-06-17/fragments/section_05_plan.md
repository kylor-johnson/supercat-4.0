# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=0, engagement_reps=13). Leaderboard built from app selling-activity (Q-01 Step 1), ranked by Total Events — NOT order GMV (~$0).
**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → template `§5-PARTIAL`, label "PARTIAL VIEW".
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = False` → not appended.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY | MET (13 engagement reps, Q-01 Step 1 has rows) | YES (engagement column set) |
| How Much Business Goes Through eCat (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=False; Q-51 absent) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=True) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | NOT MET (0 reps with 50+ presentations; max=24) | NO |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0) | NO (skip entirely) |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has 31 rows of QoQ session data) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43/Q-43-S2 = 0 rows) | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-62 absent) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-64 absent) | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET (Q-65 has 9 rows; spread 73.3%−7.9% = 65.4pp > 20pp) | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-70 absent) | NO |

**Rendered subsections (4)**: Rep Leaderboard · Behavioral Archetypes · Engagement Trajectory · How Reps Spend Their Time in the App. Plus mandatory confidence header (top) and section-level what-this-means (bottom).
