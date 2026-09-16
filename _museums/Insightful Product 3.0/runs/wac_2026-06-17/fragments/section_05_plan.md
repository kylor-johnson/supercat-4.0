# Section 05 Build Plan — Team Intelligence

Confidence tier (SECTION_CONFIDENCE_5): **PARTIAL** → template `§5-PARTIAL`, label "Partial View".
ADMIN_REPS_IN_LEADERBOARD = False → no admin disclosure.
MIXPANEL_ORDER_TRACKING_GAP = False.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (45 ordering reps; Q-01 Step 2 has 77 rep order rows — Q-18 fallback source) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET (coaching_candidates.md lists 2: Sam Schwartz, Ruben Vargas; combined $188,649) | YES |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=False; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=True; Q-01 Step 1 has 139 rows) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (MIXPANEL present + Q-63 has 20 rows) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data, 113 rows) | YES |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | NOT MET (HAS_PORTAL_ORDERS=False, HAS_NEW_ITEMS=False, Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | NOT MET (HAS_PORTAL_ORDERS=False; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | NOT MET (Q-65 present but spread 91.8%−75.5% = 16.3pp ≤ 20pp → skip silently) | NO |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET (Q-43 not present; Q-43_step2 has 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET (HAS_PORTAL_ORDERS=False, PORTAL_REP_DATA_PRESENT=False; Q-70 not present) | NO |

## Render order (narrative arc)
1. Data Confidence Header (Partial View)
2. Rep Leaderboard (no what-this-means — pure ranking table)
3. Coaching Opportunities (2 cards — no what-this-means)
4. Behavioral Archetypes
5. Presentation-to-Close Conversion
6. Engagement Trajectory
7. Section-level what-this-means

## Leaderboard columns
Source = Q-01 Step 2 (only order source; Q-18 absent). Columns per guide template: #, Rep, Orders (LTM), GMV (LTM), AOV, Unique Customers. Top 5 visible, reps 6–10 collapsed, full roster collapsed, bottom 5 visible. Showroom exclusions = 0.
