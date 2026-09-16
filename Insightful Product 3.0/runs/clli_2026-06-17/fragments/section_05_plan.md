# Section 05 Build Plan — Team Intelligence

Client: Craftmade (clli) · Run date: 2026-06-17 · SECTION_CONFIDENCE_5 = STRONG (§5-STRONG, "STRONG VIEW")
ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure REQUIRED in confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ reps; 9+ ordering reps) | MET — Q-01 Step 2 has 34 reps with eCat orders (Q-18 absent → order-GMV fallback per order-mode) | YES |
| How Much Business Goes Through eCat (1b) | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-51 not present | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=True | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has 20 rows; 7 reps with 50+ presentations | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 candidates above $50K floor → SKIP ENTIRELY (no rollup, no cards, no what-this-means) | NO |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data (70 rows) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 not present; Q-43-S2 = 0 rows | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — Q-62 = 0 rows | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL `[COLLAPSE]` | MET — Q-64 has 20 rows; MIXPANEL+HAS_PORTAL_ORDERS true | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 spread 89.9%→36.0% = 53.9pp > 20pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — Q-70 not present; PORTAL_REP_DATA_PRESENT=False | NO |
| Section-level what-this-means | MANDATORY | — | YES |

## Render order (narrative arc)
1. Rep Leaderboard (top 5 / collapsed middle / bottom 5) — no what-this-means
2. Behavioral Archetypes
3. Presentation-to-Close Conversion
4. Engagement Trajectory
5. How Reps Spend Their Time in the App (Selling vs Admin)
6. Rep Engagement vs Account Revenue [COLLAPSE]
7. Section-level what-this-means + connected-data note

## Key data
- Total eCat GMV LTM = $881,334 across 34 ordering reps (Q-01 Step 2)
- Top rep Shayna Petty = $261,427 = 29.7% of eCat GMV (just under 30% concentration threshold; SIG-RISK-04 not flagged)
- AOV spread: $20,110 (Shayna Petty) vs $430 (David Raushchuber) = 47x
- Admin/showroom users in leaderboard: David Raushchuber, Kevin Ailara, Andrew Rivera, Shayna Petty → disclosed in header
- MIXPANEL_ORDER_TRACKING_GAP = False (Postgres order data is the qualifying signal)
- Coaching: benchmark conversion 1.3%, 0 candidates clear $50K floor → coaching subsection skipped
