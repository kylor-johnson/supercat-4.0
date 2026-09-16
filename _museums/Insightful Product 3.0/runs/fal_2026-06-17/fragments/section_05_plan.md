# Section 05 Build Plan — Team Intelligence

Confidence tier (SECTION_CONFIDENCE_5): **STRONG** → template `§5-STRONG`, label "STRONG VIEW"
ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure (Matthew Eatmon) appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 12+ qualifying reps) | MET — Q-01 Step 2 has 37 rep rows (Q-18 absent; fall back to rep order data per guide template columns) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 candidates above $50K floor | NO (skip entirely, no rollup) |
| How Reps' Orders Come In (Rep eCat Adoption, 1b) | MANDATORY when PORTAL_REP_DATA_PRESENT | MET — PORTAL_REP_DATA_PRESENT=true, Q-51 has 25 rows | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has rows; reps with 50+ presentations exist | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data | YES |
| New Item Launch Velocity (6) | CONDITIONAL [COLLAPSE] | MET — HAS_PORTAL_ORDERS=true, HAS_NEW_ITEMS=true, Q-62 has 18 rows | YES |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL [COLLAPSE] | MET — MIXPANEL_USER_DATA_PRESENT=true, HAS_PORTAL_ORDERS=true, Q-64 has 20 rows | YES |
| How Reps Spend Their Time in the App (8) | CONDITIONAL (spread >20pp) | MET — selling_pct range 87.7%–57.3% = 30.4pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL [COLLAPSE] | NOT MET — Q-43 absent, Q-43-S2 = 0 rows | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL [COLLAPSE] | NOT MET — Q-70 = 0 rows | NO |
| Section-level what-this-means | MANDATORY | — | YES |

Notes:
- Leaderboard ranked by eCat GMV using Q-01 Step 2 (Orders/GMV/AOV/Unique Customers) — these are eCat orders. Q-18 not present; guide's prose-template column set matches Q-01 S2 exactly.
- 1b reframed to DIGITAL ENABLEMENT per updated guide: reps off eCat = enablement opportunity (streamline rep-assisted/manual order entry), NOT "capture rate / activation target / adoption gap." 8 reps run $0 through eCat; SIG-TEAM-01 headline pair = Charles Hoffman ($6.1M) + Deborah Klien ($1.5M) = $7.6M off-eCat.
- Username→display-name cross-ref for Q-63/64/65 via Q-01 S2 + Q-51; unmatched slugs anonymized.
