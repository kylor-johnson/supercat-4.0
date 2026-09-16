# Section 05 Build Plan — Team Intelligence

**Mode:** `SALES_SECTION_MODE = engagement` (order_reps=0, ENGAGEMENT_REP_COUNT=10). Leaderboard built from app selling-activity in Q-01 Step 1, ranked by Total Events — NOT order GMV (~$0).
**Confidence tier:** `SECTION_CONFIDENCE_5 = FULL` → `§5-FULL` / FULL PICTURE.
**ADMIN_REPS_IN_LEADERBOARD = false** → no admin disclosure line required.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, engagement variant) | MET — Q-01 Step 1 has 32 rows, ENGAGEMENT_REP_COUNT=10 | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 (no reps ≥50 presentations) | NO (skip entirely) |
| How Much Business Goes Through eCat (1b) | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-51 absent | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | NOT MET — Q-63 max presentations=10; no rep ≥50 presentations | NO |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has 23 QoQ rows (login-based; orders blank) | YES |
| New Item Launch Velocity (6) | CONDITIONAL `[COLLAPSE]` | NOT MET — Q-62 has 0 rows | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL `[COLLAPSE]` | MET — MIXPANEL=true, HAS_PORTAL_ORDERS=true, Q-64 has 12 rows | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 has 14 rows, spread 82.8%−1.8% = 81pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL `[COLLAPSE]` | NOT MET — Q-43 absent; Q-43-S2 has 0 rows | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL `[COLLAPSE]` | NOT MET — PORTAL_REP_DATA_PRESENT=false, Q-70 absent | NO |

**Render order (narrative arc):** Leaderboard → Behavioral Archetypes → Rep Engagement vs Account Revenue (collapsed) → Selling vs Admin Time → Engagement Trajectory → section-level what-this-means.

**Username → display name map (Q-06):** mgutman=Marvin Gutman, tfarnik=Tamara Farnik, rreindl=Ron Reindl, chardy=Clint Hardy, steveknighten=Steve Knighten, mpawlak=Mike Pawlak, johnsont=Tom Johnson, megany=Megan Young, perezdorothy77=Dorothy Perez, rcarlton=Ryan Carlton, jacksilverman=Jack Silverman, mcarlton=Matt Carlton, mclemetsen=Michele Clemetsen, joemiotto=Joe Miotto, mxsil=Mili Hysa. Unmapped (lszypura, sophie_p, low-event noise users) → anonymized "Rep A/B…".
