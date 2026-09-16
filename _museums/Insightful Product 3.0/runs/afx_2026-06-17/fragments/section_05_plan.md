# Section 05 Build Plan — Team Intelligence

- **Client**: AFX, Inc. (afx, org_id=185)
- **Section**: §5 Team Intelligence (id=`team`)
- **Mode**: `SALES_SECTION_MODE = engagement` (order_reps<5, ENGAGEMENT_REP_COUNT=24) → leaderboard ranked by app activity, not order GMV
- **Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → template `§5-PARTIAL`, label `PARTIAL VIEW`
- **Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` (Ryan Weems) → disclosure appended to confidence header

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET (24 active reps; engagement mode → rank by Total Events from Q-01 Step 1) | YES |
| Rep eCat Adoption vs Total Business | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 absent; engagement mode skips 1b) | NO |
| Behavioral Scorecard Spotlight | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion | CONDITIONAL | NOT MET (Q-63 has 3 rows but 0 reps with 50+ presentations — no qualifying reps) | NO |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0 candidates → skip entire subsection) | NO |
| Engagement Trajectory | CONDITIONAL | MET (Q-06 has QoQ session data for active reps) | YES |
| Territory Coverage | CONDITIONAL | NOT MET (Q-43 main absent; Q-43-S2 = 0 rows) | NO |
| New Item Launch Velocity by Rep | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 absent) | NO |
| Rep Engagement vs Account Revenue | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 absent) | NO |
| Selling vs Admin Time | CONDITIONAL | MET (Q-65 8 rows; selling_pct spread 68.8%−22.6% = 46.2pp > 20pp) | YES |
| Inactive Reps with Territory Revenue | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; PORTAL_REP_DATA_PRESENT=false; Q-70 absent) | NO |

**Rendered subsections (in narrative-arc order):** Rep Leaderboard → Behavioral Archetypes → Engagement Trajectory → How Reps Spend Their Time in the App, followed by section-level what-this-means + "With Connected Data" note.

**Notes:**
- Leaderboard population = 24 most-active app users (Q-01 Step 1, ranked by Total Events). Merged duplicate display names: `clindenborn`+`chris_lindenborn` → Chris Lindenborn; `markhudson`+`mark_hudson` → Mark Hudson.
- Engagement Trajectory uses session (login) trend, not orders/GMV (orders ≈ 0 current 90d in engagement mode).
- Selling vs Admin Time rendered as gold-standard metric cards (TARGET STRUCTURE form wins over guide table).
- Rep Leaderboard exempt from what-this-means (pure ranking table). All other rendered subsections carry a what-this-means.
