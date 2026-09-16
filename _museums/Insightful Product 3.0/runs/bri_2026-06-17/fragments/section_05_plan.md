# Section 05 Build Plan — Team Intelligence

- **Client**: Bulbrite (bri, org_id=222)
- **Section**: §5 Team Intelligence
- **Confidence tier**: SECTION_CONFIDENCE_5 = **STRONG** → template `§5-STRONG`, label "Strong View"
- **Admin disclosure**: ADMIN_REPS_IN_LEADERBOARD = False → no admin disclosure text
- **Showroom exclusions**: 0 flagged (mgoffice / "Martha Graham & Associates Office" treated as a non-person office entity and excluded from rep behavioral tables per Pass-1b agent review)

## Gate / Subsection Decisions

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate: 5+ active reps) | MET (Q-01 Step 2 has 15 reps with eCat orders; Q-18 absent, so Q-01 S2 is the rep-order source) | YES |
| Coaching Opportunities | CONDITIONAL (≥1 candidate) | NOT MET (coaching_candidates.md lists 0 candidates above $50K floor) | NO |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT = False; Q-51 not present) | NO |
| Behavioral Archetypes | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT = True; Q-01 S1/S2 data rows) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT = True; Q-63 has data; 5 reps with 50+ presentations) | YES |
| Engagement Trajectory | CONDITIONAL | MET (Q-06 has QoQ order/login data, 78 rows) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (Q-62 returned 0 rows) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL `[COLLAPSE]` | MET (MIXPANEL + HAS_PORTAL_ORDERS = True; Q-64 has 20 rows) | YES |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 spread = 76.9% − 35.1% = 41.8pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL `[COLLAPSE]` | NOT MET (Q-43 absent; Q-43-S2 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL `[COLLAPSE]` | NOT MET (PORTAL_REP_DATA_PRESENT = False; Q-70 not present) | NO |

## Render Order (narrative arc)

1. Rep Leaderboard (STRENGTH) — no what-this-means (pure ranking table)
2. Behavioral Archetypes (INTELLIGENCE) — what-this-means
3. Presentation-to-Close Conversion (INTELLIGENCE+OPPORTUNITY) — what-this-means
4. Engagement Trajectory (INTELLIGENCE) — gold form: Accelerating/Declining callouts with bulleted narrative, no separate what-this-means (per TARGET STRUCTURE)
5. Engagement Depth by Rep (INTELLIGENCE, collapsed) — what-this-means
6. How Reps Spend Their Time in the App (OPPORTUNITY) — gold form: metric cards, what-this-means
7. Section-level what-this-means + "With Connected Data" note

## Form notes (TARGET STRUCTURE governs)

- Leaderboard columns adapted to available data: # / Rep / Orders (LTM) / eCat Sales LTM / AOV / Customers. Gold's All-Channel/Digital Share/YoY columns require rep-level total-business data (PORTAL_REP_DATA_PRESENT = False) — not rendered.
- Structure: Top 5 (row-highlight + bold) → collapsed middle (reps 6–10) → Bottom 5 (reps 11–15).
- Behavioral Archetypes rendered as aggregated archetype distribution table (gold form) using guide archetype names.
- Engagement Trajectory rendered as two callouts with `<ul>` bullets (gold form), no table.
- Selling vs Admin rendered as 4 metric cards (gold form), no per-rep table.
- Engagement Depth wrapped in `<details class="inner-collapse">`.
- Confidence header: gold form (label span + plain text).
