# Section 05 Build Plan — Team Intelligence

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (29 reps with eCat orders in Q-01 Step 2; Q-18 absent → Q-01 Step 2 fallback) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md = 0 candidates above $50K floor) | NO |
| How Much Business Goes Through eCat (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT = false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT = true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has data rows; reps with 50+ presentations exist) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ order data for active reps) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 absent; Q-43-S2 = 0 rows; no dormant territory data) | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS = false; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS = false; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 rows; spread 73.0%−47.2% = 25.8pp > 20pp) | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS = false; PORTAL_REP_DATA_PRESENT = false; Q-70 not present) | NO |

## Confidence Header
- SECTION_CONFIDENCE_5 = PARTIAL → template §5-PARTIAL, label "PARTIAL VIEW"
- ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure appended (My Dang, John Pugh appear in leaderboard)

## Render order (narrative arc)
1. Rep Leaderboard (top 5 / collapsed middle / bottom 5) — no what-this-means
2. Behavioral Archetypes
3. Presentation-to-Close Conversion
4. Engagement Trajectory
5. How Reps Spend Their Time in the App (Selling vs Admin)
6. Section-level what-this-means
