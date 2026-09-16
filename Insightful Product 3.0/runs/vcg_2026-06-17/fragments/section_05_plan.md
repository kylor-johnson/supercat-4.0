# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = **PARTIAL** → §5-PARTIAL template / PARTIAL VIEW label.
Admin disclosure: ADMIN_REPS_IN_LEADERBOARD = true → disclosure appended to confidence header (Beth Miller, Becky Reizner, Lenora McIntosh).
Showroom exclusions: 3 operational accounts excluded from leaderboard (Visual Comfort1/2/6, $54,138 aggregate).
Leaderboard source: Q-18 absent → fall back to Q-01 Step 2 order-outcome data (rep GMV/orders/AOV/customers). 37 reps after exclusions.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ reps) | MET (37 active reps, Q-01 S2 order data) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md = 0 above $50K floor) | NO (skip entirely) |
| How Much Business Goes Through eCat (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=false, Q-51 absent) | NO |
| Behavioral Archetypes | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion | CONDITIONAL | MET (Q-63 has 20 rows, MIXPANEL=true) | YES |
| Engagement Trajectory | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| Territory Coverage | CONDITIONAL | NOT MET (Q-43 absent, Q-43-S2=0 rows) | NO |
| New Item Launch Velocity | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Rep Engagement vs Account Revenue | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-64 absent) | NO |
| How Reps Spend Their Time in the App (Selling vs Admin) | CONDITIONAL (spread >20pp) | MET (Q-65 rows, spread 30.5pp: 82.6%–52.1%) | YES |
| Inactive Reps with Territory Revenue | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-70 absent) | NO |
| Section-level what-this-means | MANDATORY | — | YES |
