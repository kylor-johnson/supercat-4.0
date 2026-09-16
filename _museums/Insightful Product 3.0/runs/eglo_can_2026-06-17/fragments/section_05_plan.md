# Section 05 Build Plan — Team Intelligence

**Mode:** SALES_SECTION_MODE = engagement (order_reps=1, ENGAGEMENT_REP_COUNT=17). Leaderboard built from Q-01 Step 1 app selling-activity, ranked by Total Events — NOT order GMV.

**Confidence tier:** SECTION_CONFIDENCE_5 = PARTIAL → §5-PARTIAL template, label "PARTIAL VIEW".

**Admin disclosure:** ADMIN_REPS_IN_LEADERBOARD = true (Karen Hoffman) → disclosure text appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, engagement mode) | MET (26 Q-01 S1 rows; rank by Total Events) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0 candidates) | NO (skip entirely) |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET-but-EMPTY (Q-63 present but no rep has 50+ presentations except 2 reps with 0% conversion; see note) | YES (renders the two 50+ presentation reps) |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 spread 74.7%–13.1% = 61.6pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; PORTAL_REP_DATA_PRESENT=false; Q-70 not present) | NO |
| Section-level what-this-means | MANDATORY | — | YES |

**Render order (narrative arc):** Rep Leaderboard → Behavioral Archetypes → Presentation-to-Close → Engagement Trajectory → Selling vs Admin Time → section-level what-this-means.

**Showroom exclusions:** 0 (showroom_scan_results.md total flagged=0).
