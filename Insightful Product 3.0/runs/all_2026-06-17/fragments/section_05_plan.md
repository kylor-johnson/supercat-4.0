# Section 05 Build Plan — Team Intelligence

**Mode**: `engagement` (order_reps=1, engagement_reps=31). Leaderboard ranks by APP ACTIVITY (Total Events), not order GMV.
**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → template `§5-PARTIAL`, label "PARTIAL VIEW".
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` (Adrian Fernandes) → disclosure text REQUIRED in confidence header.
**Coaching**: `coaching_candidates.md` lists 0 candidates → coaching subsection SKIPPED entirely (no rollup, no cards).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET — engagement mode, Q-01 S1 has 71 rows; rank by Total Events | YES (no what-this-means) |
| How Much Business Goes Through eCat (1b) | CONDITIONAL | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-51 absent | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | NOT MET (effectively) — Q-63 has rows but only 1 rep ≥50 presentations; thin → skip, note in header | NO |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET — 0 candidates | NO |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has 55 rows of QoQ data | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 absent / Q-43-S2 = 0 rows | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-62 absent | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-64 absent | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET — Q-65 has rows, spread 66.7pp > 20pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — HAS_PORTAL_ORDERS=false, Q-70 absent | NO |

**Rendered subsections**: Rep Leaderboard, Behavioral Archetypes, Engagement Trajectory, How Reps Spend Their Time in the App (Selling vs Admin) + section-level what-this-means.
