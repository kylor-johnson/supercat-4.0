# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = STRONG → template §5-STRONG, label "STRONG VIEW"
ADMIN_REPS_IN_LEADERBOARD = false → no admin disclosure.
MIXPANEL_ORDER_TRACKING_GAP = false.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (Q-01 Step 2 has 15 eCat-active reps; Q-18 absent → S2 fallback) | YES |
| Coaching Cards | MANDATORY when MIXPANEL data + any rep >$50K upside | MET (MIXPANEL_USER_DATA_PRESENT=true; high-presentation / zero-conversion reps exceed $50K estimated upside) | YES |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Scorecard | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 20 rows; 5 reps with 50+ presentations) | YES |
| Engagement Trajectory | CONDITIONAL | MET (Q-06 has QoQ data, 78 rows) | YES |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | NOT MET (Q-62 has 0 rows) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | MET (MIXPANEL + HAS_PORTAL_ORDERS true; Q-64 has 20 rows) | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 spread = 76.9% − 35.1% = 41.8pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET (Q-43 absent; Q-43_step2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET (Q-70 absent; PORTAL_REP_DATA_PRESENT=false) | NO |

## Render order (narrative arc)
1. Rep Leaderboard (STRENGTH)
2. Coaching Cards (OPPORTUNITY)
3. Behavioral Scorecard (INTELLIGENCE)
4. Presentation-to-Close Conversion (INTELLIGENCE + OPPORTUNITY)
5. Engagement Trajectory (INTELLIGENCE)
6. Rep Engagement vs Account Revenue (INTELLIGENCE — collapsed)
7. Selling vs Admin Time (OPPORTUNITY)
+ Section-level what-this-means + "With Connected Data" note

## Leaderboard data (Q-01 Step 2 — eCat orders LTM)
Columns adapted to available data: #, Rep, Orders (LTM), GMV (LTM), AOV, Unique Customers.
Top 5: Jason Burns ($420,246), Dave Kapalka ($23,016), Ruben Vargas ($18,083), Tami Stauffacher ($6,023), Pat Debarber ($3,369).
Bottom 5: Beth Peel ($36), Brittain Cherry ($110), Vincent Ingato ($591), Jon McMahan ($739), Allison Stauffacher ($813).
Middle (6–10): Kevin Gannon, Melissa Schultheis, Pepper Carlson, Aaron Moscowicz, Allison Stauffacher — collapse reps 6–10.
DEDUP: 15 distinct rep_name values, no duplicates.
