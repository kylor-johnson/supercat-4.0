# Section 05 Build Plan — Team Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 17 qualifying reps) | MET (Q-01 Step 2 has per-rep eCat order data; Q-18 absent, fallback used) | YES |
| How Reps' Orders Come In (1b — digital enablement, NOT capture rate) | MANDATORY | MET (PORTAL_REP_DATA_PRESENT=true, Q-51 has 25 rows) | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 20 rows, ≥1 rep with 50+ presentations) | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | MET (coaching_candidates.md lists 4) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | MET (Q-64 has 20 rows; MIXPANEL + HAS_PORTAL_ORDERS true) | YES |
| How Reps Spend Their Time in the App (8) | CONDITIONAL (spread >20pp) | MET (Q-65 spread 91.9%−64.4% = 27.5pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET (Q-43 absent; Q-43-S2 = 0 rows) | NO |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | NOT MET (Q-62 = 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET (Q-70 = 0 rows) | NO |

## Confidence
- SECTION_CONFIDENCE_5 = FULL → template §5-FULL, label "FULL PICTURE"
- ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure appended to confidence header (Shannon Rose, Retha Boles)

## Data handling notes
- Leaderboard source Q-18 absent → use Q-01 Step 2 eCat order data (GMV/AOV/orders/customers).
- DEDUP: "Lynn  Ross" + "Lynn Ross" merged → 324 orders, $2,117,369 GMV, $6,535 AOV, 47 customers.
- Showroom exclusion: "Martha Graham & Associates Office" ($20,656, confirmed_operational) excluded from leaderboard.
- Coaching cards: 4 reps verbatim from coaching_candidates.md (Brad Krieger $373,740; Amy Matteson $86,449; Randy Gould $81,634; Dunn Lighting $53,680). Combined $595,503.
- Q-63/64/65 username→display-name cross-ref via Q-01 Step 2.
