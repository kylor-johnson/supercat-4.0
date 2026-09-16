# Section 05 Build Plan — Team Intelligence (ril, 2026-06-17)

- **Mode**: ORDERS (5+ reps placing eCat orders; Q-01 Step 2 has 27 reps with GMV)
- **Confidence tier**: SECTION_CONFIDENCE_5 = FULL → template `§5-FULL`, label "FULL PICTURE"
- **ADMIN_REPS_IN_LEADERBOARD = true** (Winnie Ng) → admin disclosure MUST appear in confidence header
- **MIXPANEL_ORDER_TRACKING_GAP = False** → conversion analysis runs normally
- Showroom exclusions: 0
- Leaderboard source: Q-18 not present → fall back to Q-01_step2_results.md (orders/GMV/AOV/unique customers)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 5+ reps) | MET (27 reps w/ eCat orders in Q-01 S2) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET (coaching_candidates.md lists 5; $4,428,360 combined) | YES |
| How Reps' Orders Come In (Rep eCat Adoption, Q-51) | MANDATORY | MET (PORTAL_REP_DATA_PRESENT=true, 25 rows) | YES |
| Behavioral Archetypes (Q-01+Q-03) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (Q-63) | CONDITIONAL | MET (Q-63 rows; reps 50+ presentations) | YES |
| Engagement Trajectory (Q-06) | CONDITIONAL | MET (Q-06 QoQ data present) | YES |
| New Item Launch Velocity (Q-62) | CONDITIONAL | NOT MET (HAS_NEW_ITEMS=false, Q-62 absent) | NO |
| Rep Engagement vs Account Revenue (Q-64) | CONDITIONAL | MET (Q-64 rows + HAS_PORTAL_ORDERS=true) — collapsed | YES |
| Selling vs Admin Time (Q-65) | CONDITIONAL | MET (spread 86.3%−49.8% = 36.5pp > 20pp) | YES |
| Territory Coverage (Q-43) | CONDITIONAL | NOT MET (Q-43 absent, Q-43-S2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue (Q-70) | CONDITIONAL | NOT MET (Q-70 = 0 rows) | NO |

## Render order (narrative arc per guide Content Blocks)
1. Rep Leaderboard (no what-this-means — pure ranking table)
2. Coaching Opportunities (no what-this-means)
3. How Reps' Orders Come In (1b — digital enablement framing)
4. Behavioral Archetypes (2)
5. Presentation-to-Close Conversion (2b)
6. Engagement Trajectory (4)
7. Rep Engagement vs Account Revenue (7, collapsed)
8. Selling vs Admin Time (8)
+ Section-level what-this-means

## Data notes
- Q-51 duplicate Gayle Massey rows (GM8/GM) — collapse to one; never expose rep_number.
- 1b is reframed "How Reps' Orders Come In" = DIGITAL ENABLEMENT. Reps off eCat = enablement opportunity (streamline rep-assisted/manual portion). NEVER "capture rate / activation target / untapped / adoption gap."
- Zero-eCat reps (top 5 by total business, $0 eCat): Nick Meletis $1.4M, Patrick Chandonnet $911,622, Jon Healy $798,798, Keith Stibler $779,508, Jacqueline Wu $770,099. Combined zero-eCat ≈ $7.3M across reps.
- Coaching cards verbatim from coaching_candidates.md: Yash Roy $1,830,659; Sondra Walbert $1,206,459; Desiree Gladstone $705,166; Sylvia Ou $442,686; Allison Tsoi $243,390. Combined $4,428,360.
- Q-63/64/65 usernames → display names via Q-01 Step 2 cross-ref (yash=Yash Roy, allisontsoi=Allison Tsoi, sondrawalbert=Sondra Walbert, johnnyh=Johnny Hostetter, sylvia=Sylvia Ou, sherylb=Sheryl Madonna, michele_gee=Michele Gee, m_crandall=Meghan Crandall, patrickchandonnet=Patrick Chandonnet, kimking=Kim King, desiree503=Desiree Gladstone, bryan913=Bryan Gladstone, shelley_straughan=Shelley Straughan, dhalpern=Drew Halpern, winnie=Winnie Ng, elainevoong=Elaine Voong, cottonl=Layla Cotton).
