# Section 05 Build Plan — Team Intelligence

**Mode**: SALES_SECTION_MODE = engagement (order_reps=2, ENGAGEMENT_REP_COUNT=46).
Rep Leaderboard built from Q-01 Step 1 app selling-activity, ranked by Total Events.
Order-GMV leaderboard suppressed (eCat order GMV ~$0 across team).

**Confidence tier**: SECTION_CONFIDENCE_5 = PARTIAL → §5-PARTIAL, label "PARTIAL VIEW".
ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure appended to confidence header
(Caitlin McGinnis, Ron Devorsky).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET — 46 engagement reps, Q-01 S1 data present | YES |
| Coaching Opportunities | CONDITIONAL | NOT MET — coaching_candidates.md lists 0 candidates | NO |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET — PORTAL_REP_DATA_PRESENT=false; Q-51 absent | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true (order-tracking gap=false) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has rows; 5 reps with 50+ presentations | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data (67 rows) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false; Q-62 absent | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false; Q-64 absent | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET — Q-65 rows; spread 96.3%→57.0% = ~39pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 empty; no dormant territory $ | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false; Q-70 absent | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

**Render order (narrative arc)**: Rep Leaderboard → Behavioral Archetypes →
Presentation-to-Close → Engagement Trajectory → Selling vs Admin Time → section what-this-means.
