# Section 05 Build Plan — Team Intelligence

**Mode:** ENGAGEMENT (`SALES_SECTION_MODE = engagement`; order_reps=3, engagement_reps=38)
**Confidence tier:** `SECTION_CONFIDENCE_5 = FULL` → template §5-FULL, label "FULL PICTURE"
**Admin disclosure:** `ADMIN_REPS_IN_LEADERBOARD = true` → MUST appear in confidence header
**Leaderboard basis:** Q-01 Step 1, ranked by Total Events (app selling activity LTM), engagement column set
**Mixpanel order-tracking gap:** False (Postgres orders real; do not skip funnel)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 38 engagement reps) | MET — engagement mode, Q-01 S1 has 95 rows | YES (ranked by Total Events; no what-this-means) |
| Coaching Opportunities | MANDATORY when ≥1 candidate | MET — `coaching_candidates.md` lists 1 (Garrett Passmore, $52,474) | YES (1 card, verbatim upside; no what-this-means) |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when `PORTAL_REP_DATA_PRESENT=true` + Q-51 rows | NOT MET for engagement display — Q-51 shows agency-level rows, only 1 rep (Dean Coxworth) has any eCat capture; all others 0%. Engagement-mode guidance §3 says skip 1b (no portal/order data at rep level). | NO — skipped; noted in confidence header |
| Behavioral Archetypes (2) | CONDITIONAL — `MIXPANEL_USER_DATA_PRESENT=true` | MET | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL — Q-63 rows + 50+ presentations | MET — 2 reps with ≥50 presentations (gpassmore 59, jhoward 57) | YES |
| Engagement Trajectory (4) | CONDITIONAL — Q-06 QoQ data | MET — Q-06 has 76 rows | YES |
| New Item Launch Velocity (6) | CONDITIONAL — HAS_PORTAL_ORDERS + HAS_NEW_ITEMS + Q-62 rows | MET — but Q-62 is agency/rep-firm level (not individual app reps); engagement mode leads on app activity. Order-channel data near-empty per mode. | NO — skipped (agency-level, not individual reps; noted) |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL — Q-64 rows + gates | MET — Q-64 has 20 rows | YES (collapsed) |
| Selling vs Admin Time (8) | CONDITIONAL — Q-65 rows + spread >20pp | MET — spread 77.3% to 20.6% = 56.7pp > 20pp | YES |
| Territory Coverage (5) | CONDITIONAL — Q-43 territory + dormant accounts | NOT MET — Q-43 not present; Q-43-S2 returned 0 rows | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL — Q-70 rows | NOT MET — Q-70 returned 0 rows | NO |
| Section-level what-this-means | MANDATORY | — | YES |

## Skipped subsections (noted in confidence header)
- 1b Rep eCat Adoption — engagement mode (rep-level eCat ordering still ramping; only 1 rep has eCat capture)
- 5 Territory Coverage — no territory/dormant data (Q-43 empty)
- 6 New Item Launch Velocity — data is agency-level, not individual app reps
- 9 Inactive Reps with Territory Revenue — Q-70 empty
