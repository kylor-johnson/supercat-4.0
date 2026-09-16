# Section 05 Build Plan — Team Intelligence

Confidence tier (SECTION_CONFIDENCE_5): **STRONG** → template `§5-STRONG`, label `STRONG VIEW`
ADMIN_REPS_IN_LEADERBOARD: False → no admin disclosure
MIXPANEL_ORDER_TRACKING_GAP: False

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (15 reps with eCat orders in Q-01 Step 2; Q-18 absent so sourced from Q-01 Step 2) | YES |
| How Much Business Goes Through eCat (1b, Q-51) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=False AND Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=True) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has rows; 3 reps with 50+ presentations) | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0 candidates above $50K floor — skip entirely) | NO |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (Q-62 = 0 rows) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | MET (Q-64 has 20 rows; MIXPANEL_USER_DATA_PRESENT=True; HAS_PORTAL_ORDERS=True) — collapsed | YES |
| How Reps Spend Their Time in the App (8, Selling vs Admin) | CONDITIONAL (spread >20pp) | MET (Q-65 spread 76.9%−35.1% = 41.8pp > 20pp) | YES |
| Territory Coverage Gaps (5) | CONDITIONAL | NOT MET (Q-43 absent, Q-43-S2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=False, Q-70 not present) | NO |

## Render order (narrative arc)
1. Rep Leaderboard
2. Behavioral Archetypes
3. Presentation-to-Close Conversion
4. Engagement Trajectory
5. How Reps Spend Their Time in the App (Selling vs Admin)
6. Rep Engagement vs Account Revenue (collapsed)
7. Section-level what-this-means + With Connected Data note

## Notes
- Leaderboard built from Q-01 Step 2 (Q-18 absent). 15 reps. Top 5 visible, reps 6–10 collapsed, bottom 5 (11–15) visible.
- Username→display mapping via Q-01 Step 2 + Q-06. Operational account `mgoffice` (Martha Graham & Associates Office) excluded from Q-63/64/65 tables.
- Coaching subsection fully skipped per coaching_candidates.md (0 candidates).
