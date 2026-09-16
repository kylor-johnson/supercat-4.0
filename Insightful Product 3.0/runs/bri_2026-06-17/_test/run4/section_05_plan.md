# Section 05 Build Plan — Team Intelligence

Confidence tier: SECTION_CONFIDENCE_5 = STRONG → template §5-STRONG, label "STRONG VIEW".
ADMIN_REPS_IN_LEADERBOARD = False → no admin disclosure in confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — section gate passes (qualifying_reps=5); Q-18 absent, fall back to Q-01 Step 2 order outcomes (15 reps) | YES |
| How Much Business Goes Through eCat (Q-51) | CONDITIONAL (MANDATORY when gate met) | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-51 not present | NO |
| Behavioral Archetypes (Q-01 + Q-03) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=True; MIXPANEL_ORDER_TRACKING_GAP=False (submit_order usable) | YES |
| Presentation-to-Close Conversion (Q-63) | CONDITIONAL | MET — Q-63 has rows; 3 reps with 50+ presentations (jasonburns 209, alaid 133, tstauffacher 98) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate; skip when 0 | NOT MET — coaching_candidates.md lists 0 candidates above $50K floor | NO |
| Engagement Trajectory (Q-06) | CONDITIONAL | MET — Q-06 has QoQ order/login change data | YES |
| New Item Launch Velocity (Q-62) | CONDITIONAL [COLLAPSE] | NOT MET — Q-62 returned 0 rows | NO |
| Rep Engagement vs Account Revenue (Q-64) | CONDITIONAL [COLLAPSE] | MET — MIXPANEL_USER_DATA_PRESENT=True + HAS_PORTAL_ORDERS=True + Q-64 has 20 rows | YES |
| How Reps Spend Their Time in the App (Q-65) | CONDITIONAL (spread >20pp) | MET — selling_pct spread 76.9%−35.1% = 41.8pp > 20pp | YES |
| Territory Coverage Gaps (Q-43) | CONDITIONAL [COLLAPSE] | NOT MET — Q-43 absent; Q-43-S2 returned 0 rows | NO |
| Platform Adoption Gap / Inactive Reps (Q-70) | CONDITIONAL [COLLAPSE] | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-70 not present | NO |

## Rendered subsections (narrative arc order)
1. Rep Leaderboard
2. Behavioral Archetypes
3. Presentation-to-Close Conversion
4. Engagement Trajectory
5. Rep Engagement vs Account Revenue (collapsed)
6. How Reps Spend Their Time in the App
+ Section-level what-this-means

## Coaching cards: 0 (subsection skipped entirely per coaching_candidates.md)

## Notes
- Username→display-name resolved via Q-01 Step 2 / Q-06 / Q-04.
- "mgoffice" = "Martha Graham & Associates Office" — operational/non-person entity, excluded from Presentation-to-Close and Engagement-depth tables and summary stats.
- Q-18 absent → leaderboard columns use Q-01 Step 2 order outcomes (Orders / GMV / AOV / Unique Customers) rather than gold's eCat/all-channel columns (no source data for those).
