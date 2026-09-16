# Section 05 Build Plan — Team Intelligence

Mode: **orders** (SALES_SECTION_MODE=orders, 37 ordering reps, 40 non-showroom order rows). Confidence tier: **SECTION_CONFIDENCE_5 = FULL** → §5-FULL "FULL PICTURE". ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure required in confidence header. Showroom exclusions: 3 (CC Dallas, Atlanta, Highpoint).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 5+ reps) | MET (40 non-showroom order reps; Q-18 empty → sourced from Q-01 Step 2 order data, same shape) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET (coaching_candidates.md lists 5) | YES |
| How Reps' Orders Come In (1b) | MANDATORY when gate met | MET (PORTAL_REP_DATA_PRESENT=true, Q-51 has 25 rows) — DIGITAL ENABLEMENT framing, not capture rate | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true; ORDER_TRACKING_GAP=false) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has rows; reps with 50+ presentations) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data, 58 rows) | YES |
| New Item Launch Velocity (6) `[COLLAPSE]` | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-62 20 rows) | YES |
| Rep Engagement vs Account Revenue (7) `[COLLAPSE]` | CONDITIONAL | MET (MIXPANEL+HAS_PORTAL_ORDERS true, Q-64 20 rows) | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | NOT MET (spread 18.3pp ≤ 20pp) | NO |
| Territory Coverage (5) `[COLLAPSE]` | CONDITIONAL | NOT MET (Q-43 / Q-43-S2 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) `[COLLAPSE]` | CONDITIONAL | NOT MET (Q-70 returned 0 rows) | NO |

What-this-means exemptions: Rep Leaderboard and Coaching Opportunities (per gold + Section D). All other rendered subsections carry a what-this-means; section-level what-this-means at the end.
