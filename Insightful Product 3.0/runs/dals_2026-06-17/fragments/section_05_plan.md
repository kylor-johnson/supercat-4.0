# Section 05 Build Plan — Team Intelligence

**Mode:** `SALES_SECTION_MODE = engagement` (order_reps=0, engagement_reps=17). Leaderboard built from app selling-activity (Q-01 Step 1), ranked by Total Events. Order-GMV columns dropped.

**Confidence tier:** `SECTION_CONFIDENCE_5 = PARTIAL` → template §5-PARTIAL, label "PARTIAL VIEW".

**Admin disclosure:** `ADMIN_REPS_IN_LEADERBOARD = false` → no admin disclosure text needed.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_5=PARTIAL) | YES |
| Rep Leaderboard | MANDATORY (section gate, 5+ reps) | MET (engagement mode, 35 app users / 17 engaged) | YES |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | NOT MET (Q-63 row_count=0; no rep with 50+ presentations) | NO |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0) | NO (skip entirely) |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has 23 rows QoQ) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 4 rows; spread 61.1%−21.7% = 39.4pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-70 not present) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

**Rendered subsections:** Confidence header, Rep Leaderboard, Behavioral Archetypes, Engagement Trajectory, Selling vs Admin Time, section-level what-this-means.
