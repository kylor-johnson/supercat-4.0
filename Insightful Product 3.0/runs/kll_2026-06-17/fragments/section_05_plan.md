# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=4 < 5; ENGAGEMENT_REP_COUNT=72). Leaderboard built from app selling-activity in Q-01 Step 1, ranked by Total Events — NOT order GMV (~0 here).
**Confidence §5**: FULL → `FULL PICTURE` label.
**ADMIN_REPS_IN_LEADERBOARD = true** → admin disclosure in confidence header (Katy Tipton, Kuzco Showroom).
**Showroom exclusion**: Kuzco Showroom (kuzcoshowroom) excluded from leaderboard/archetypes/conversion (1 account, $112,926).
**MIXPANEL_ORDER_TRACKING_GAP = false**.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, engagement mode) | MET (72 engagement reps; Q-01 S1 data) | YES |
| Coaching Opportunities | CONDITIONAL (≥1 candidate) | NOT MET (coaching_candidates lists 0 — below $50K floor) | NO |
| How Much Business Goes Through eCat (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has rows; 6 reps ≥50 presentations) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (Q-62 0 rows) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | MET (MIXPANEL=true, HAS_PORTAL_ORDERS=true, Q-64 rows) | YES (collapsed) |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (spread 79.5%−48.5% = 31pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-70 not present) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

**Render order (narrative arc):** Leaderboard → Behavioral Archetypes → Presentation-to-Close → Engagement Trajectory → Rep Engagement vs Revenue (collapsed) → Selling vs Admin Time → section what-this-means.
