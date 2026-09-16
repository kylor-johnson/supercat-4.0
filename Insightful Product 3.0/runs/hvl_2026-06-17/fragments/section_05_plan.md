# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=0, ENGAGEMENT_REP_COUNT=35). Leaderboard built from app selling-activity in Q-01 Step 1, ranked by Total Events. Order-GMV leaderboard suppressed (eCat order GMV ≈ $0).
**Confidence tier**: SECTION_CONFIDENCE_5 = PARTIAL → §5-PARTIAL template, "PARTIAL VIEW" label.
**Admin disclosure**: ADMIN_REPS_IN_LEADERBOARD = False → not appended.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET (35 active reps, Q-01 S1 selling-activity present) | YES |
| Coaching Opportunities | CONDITIONAL → MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0 — no rep ≥50 presentations) | NO |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=False; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=True) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | NOT MET (Q-63 present but no rep ≥50 presentations; max=37) | NO |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has 53 rows of QoQ session data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 19 rows; spread 85.7%–19.4% = 66.3pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-70 not present) | NO |

**Rendered subsections (narrative arc order)**: Rep Leaderboard → Behavioral Archetypes → Engagement Trajectory → Selling vs Admin Time → section-level what-this-means.
