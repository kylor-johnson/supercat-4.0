# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = PARTIAL → §5-PARTIAL template, "PARTIAL VIEW" label.
ADMIN_REPS_IN_LEADERBOARD = true (Magnus Marsons) → admin disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps; 14 reps in Q-01 S2) | MET | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET (3 candidates, combined $1,281,975) | YES |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has rows; reps with 50+ presentations exist) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data, 33 rows) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 = 0 rows) | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET (Q-65 rows; spread 92%−28.2% = 63.8pp > 20pp) | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; PORTAL_REP_DATA_PRESENT=false; Q-70 not present) | NO |

Section-level what-this-means: YES (mandatory).

Notes:
- MIXPANEL_ORDER_TRACKING_GAP = false → normal funnel analysis applies.
- Leaderboard source: Q-18 absent → use Q-01 Step 2 order outcomes (orders, GMV, AOV, unique customers). Columns match guide's original leaderboard template, not gold's eCat/all-channel split (no all-channel feed for this org).
- Coaching cards rendered EXACTLY as coaching_candidates.md: Kim Quelch $956,448; Hilary Springate $167,069; Stephen Inglehart $158,458. Combined $1,281,975.
