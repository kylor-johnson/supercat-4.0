# Section 05 Build Plan — Team Intelligence

Section: §5 · id=`team` · Bulbrite (bri) · Run date 2026-06-17
Confidence tier: SECTION_CONFIDENCE_5 = **STRONG** → template `§5-STRONG`, label "Strong View"
ADMIN_REPS_IN_LEADERBOARD = False → no admin disclosure in confidence header
MIXPANEL_ORDER_TRACKING_GAP = False → use Postgres order counts; do not skip Presentation→Orders ratio

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate: 5+ active reps) | MET — Q-01 Step 2 has 15 reps with eCat orders (Q-18 absent; Step 2 is the order-outcome source) | YES |
| Rep eCat Adoption vs Total Business | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-51 not present | NO |
| Behavioral Scorecard | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=True | YES |
| Presentation-to-Close Conversion | CONDITIONAL | MET — Q-63 has 20 rows; 5 reps with 50+ presentations | YES |
| Coaching Cards | MANDATORY when Mixpanel + any rep >$50K upside | MET — Anita Laidlaw ~$63K estimated upside (133 presentations, 0 conversions) | YES |
| Engagement Trajectory | CONDITIONAL | MET — Q-06 has QoQ login + order change data | YES |
| New Item Launch Velocity | CONDITIONAL | NOT MET — Q-62 returned 0 rows | NO |
| Rep Engagement vs Account Revenue | CONDITIONAL (collapsed) | MET — Q-64 has 20 rows; MIXPANEL + HAS_PORTAL_ORDERS True | YES |
| Selling vs Admin Time | CONDITIONAL (spread >20pp) | MET — Q-65 spread 76.9%−35.1% = 41.8pp > 20pp | YES |
| Territory Coverage | CONDITIONAL (collapsed) | NOT MET — Q-43 absent, Q-43_step2 returned 0 rows | NO |
| Inactive Reps with Territory Revenue | CONDITIONAL (collapsed) | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-70 not present | NO |

Plus MANDATORY: Data Confidence Header (top) and Section-level what-this-means (bottom).

Render order (narrative arc): Confidence Header → Rep Leaderboard → Coaching Cards → Behavioral Scorecard → Presentation-to-Close → Engagement Trajectory → Rep Engagement vs Revenue [collapsed] → Selling vs Admin Time → Section what-this-means.
