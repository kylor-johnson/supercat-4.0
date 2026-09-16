# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=2, engagement_reps=28). Leaderboard built from app selling-activity in Q-01 Step 1, ranked by Total Events. Order-GMV leaderboard suppressed (GMV ~0).

**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → `§5-PARTIAL` template, label "PARTIAL VIEW".

**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` (Greg Knudsen, Sarah Chandler) → admin disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — 28 engagement reps; ranked by Total Events (Q-01 S1) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 candidates above $50K floor | NO (skip entirely) |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-51 not present | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has data rows (reps with 50+ presentations) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 has 0 rows, no portal data | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-62 not present | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-64 not present | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 spread 78.7%→30.4% = 48.3pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-70 not present | NO |

**Rendered subsections (narrative arc order)**: Rep Leaderboard → Behavioral Archetypes → Presentation-to-Close → Engagement Trajectory → Selling vs Admin Time → section-level what-this-means.

**Note**: Coaching subsection (the OPPORTUNITY slot right after leaderboard) is correctly skipped per engagement-mode + 0-candidate rule. No rollup callout, no cards.
