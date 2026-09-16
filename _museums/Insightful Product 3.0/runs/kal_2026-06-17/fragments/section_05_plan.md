# Section 05 Build Plan — Team Intelligence

Client: Kalco Lighting / Allegri Crystal (kal) · Run 2026-06-17
Mode: ORDERS · SECTION_CONFIDENCE_5 = FULL → `§5-FULL` / label "Full Picture".
Admin disclosure REQUIRED (ADMIN_REPS_IN_LEADERBOARD = true: Bob Ross, Claudia Carrillo, Snehal Shah).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — 25 reps with eCat orders (Q-01 Step 2; Q-18 absent, use Step 2 order data) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 above $50K floor | NO (skip entirely) |
| How Reps' Orders Come In (1b) | MANDATORY | MET — PORTAL_REP_DATA_PRESENT=true, Q-51 has 25 rows | YES |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true (ORDER_TRACKING_GAP=False) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 rows; 4 reps with 50+ presentations (larosa 95, bob_ross 85, kirk_johnson 62, rparker2 54) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 QoQ data, 56 reps | YES |
| New Item Launch Velocity (6) [COLLAPSE] | CONDITIONAL | MET — HAS_PORTAL_ORDERS + HAS_NEW_ITEMS + Q-62 rows | YES |
| Rep Engagement vs Account Revenue (7) [COLLAPSE] | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT + HAS_PORTAL_ORDERS + Q-64 rows | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — spread 41.9pp (78.3% bob_ross → 36.4% jackh) | YES |
| Territory Coverage (5) [COLLAPSE] | CONDITIONAL | NOT MET — Q-43 absent, Q-43-S2 0 rows | NO |
| Inactive Reps with Territory Revenue (9) [COLLAPSE] | CONDITIONAL | NOT MET — Q-70 0 rows | NO |
| Section-level what-this-means | MANDATORY | — | YES |

## Build notes
- Leaderboard columns: # · Rep · Orders (LTM) · GMV (LTM) · AOV · Unique Customers (guide order-template; Q-18 absent → source Q-01 Step 2). Top 5 / collapsed middle (6–20) / bottom 5. No what-this-means (exempt). Dedup: one row per rep.
- 1b reframed DIGITAL ENABLEMENT. No "capture rate / activation target / untapped / adoption gap." Off-eCat books = other channels (web/EDI/phone/email/rep entry). Q-51 keyed to sales-agency rows; only DBA Associates has eCat orders ($194,108 / 11 orders LTM). Top off-eCat books: House Account $1.8M, Pacific Liteforce $1.3M, Cheryl La Rosa & Assoc $1.3M, Grillo Group $1.1M, Pacific Ltfrce North $790K.
- Coaching SKIPPED — no rollup, no cards (correct for low-AOV/low-conversion org).

Username→display map (Q-63/64/65): larosa=Cheryl LaRosa, bob_ross=Bob Ross,
kirk_johnson=Kirk Johnson, rparker2=Robert Parker, ccarrillo=Claudia Carrillo,
grillocs=Grillo Customer Service, kgrillo=Ken Grillo, jsteele1=Jason Steele,
cgecowets=Carole Gecowets, doerenc=Doeren Carsten, rjazimi=Rob Azimi,
zrapp=Zachary Rapp, bnorthway=Bill Northway, gpassmore=Garrett Passmore,
bgrillo=Beto Grillo, jenmccarty=Jenifer McCarty, charliek=Charlie Kissel,
jackh=Jack Helbert, rjohnson1=Rita Johnson, trevl=Trevor Lindsay, albert=Albert Maldonado.
