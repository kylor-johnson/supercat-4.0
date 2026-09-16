# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = **STRONG** → template `§5-STRONG`, label "STRONG VIEW".
ADMIN_REPS_IN_LEADERBOARD = **true** → admin disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (38 qualifying reps; Q-01 Step 2 has 48 rep rows of eCat order data) | YES |
| How Reps' Orders Come In (1b — Rep eCat Adoption vs Total Business, Q-51, digital-enablement framing) | MANDATORY | MET (PORTAL_REP_DATA_PRESENT=true; Q-51 has 25 data rows) | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true; Q-01 Step 1 = 95 rows) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 20 rows; reps with 50+ presentations exist) | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | MET (coaching_candidates.md lists 1: Rob Robinson, $248,901) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has 64 rows of QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-62=10 rows) | YES (collapsed) |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true, HAS_PORTAL_ORDERS=true, Q-64=20 rows) | YES (collapsed) |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | NOT MET (Q-65 spread = 84.3% − 69.8% = 14.5pp ≤ 20pp) | NO |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (Q-70 returned 0 rows) | NO |

Section-level what-this-means: YES (mandatory).

Notes:
- Q-18 file absent → leaderboard built from Q-01 Step 2 (eCat orders by rep: orders, GMV, AOV, unique customers).
- Q-63/64/65 usernames cross-referenced to display names via Q-01 Step 2 / Q-04 / Q-06.
- Showroom scan: 0 flagged, 0 excluded → no exclusion note in section-sub.
- Q-65 skipped silently per spread gate (14.5pp).
