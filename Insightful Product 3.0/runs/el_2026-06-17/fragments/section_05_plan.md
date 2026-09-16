# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = **FULL** → template §5-FULL, label "FULL PICTURE".
ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (50 reps in Q-01 Step 2; Q-18 absent → source from Q-01 Step 2 GMV/orders/AOV/customers) | YES |
| How Reps' Orders Come In (1b, Rep eCat Adoption vs Total Business) | MANDATORY when gate met | MET (PORTAL_REP_DATA_PRESENT=true, Q-51 has 25 rows, all run entirely off eCat) — DIGITAL-ENABLEMENT framing, never capture-rate/adoption-gap | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true; ORDER_TRACKING_GAP=false) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 rows; 6 reps with 50+ presentations) | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md = 0 candidates above $50K floor) | NO (skip entirely, no rollup) |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | MET (HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-62 rows) | YES |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | MET (MIXPANEL+HAS_PORTAL_ORDERS, Q-64 rows) | YES |
| Selling vs Admin Time (8) | CONDITIONAL | MET (spread 74.7%−47.8% = 26.9pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET (Q-43 absent, Q-43-S2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET (Q-70 = 0 rows) | NO |

Render order (narrative arc): Leaderboard → 1b → Behavioral Archetypes → Presentation-to-Close → Engagement Trajectory → New Item Velocity [collapse] → Rep Engagement vs Revenue [collapse] → Selling vs Admin → section-level what-this-means.
(Coaching skipped; Territory + Inactive skipped.)
