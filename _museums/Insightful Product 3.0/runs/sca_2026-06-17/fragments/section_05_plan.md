# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=3 < 5; ENGAGEMENT_REP_COUNT=15).
Rep Leaderboard built from Q-01 Step 1 app selling-activity, ranked by Total Events.
**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → §5-PARTIAL template, "Partial View" label.
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` → disclosure text appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 15 engagement reps) | MET (Q-01 Step 1 = 31 rows; engagement mode) | YES |
| Coaching Opportunities | MANDATORY-when-≥1 | NOT MET (coaching_candidates.md lists 0 candidates) | NO (skip entirely) |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY-when-gate-met | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 absent) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 6 data rows) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has 24 rows QoQ) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 absent) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 absent) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 13 rows; spread 95.0%−4.1% = 90.9pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 step2 = 0 rows; no dormant territory value) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-70 absent) | NO |

**Section-level what-this-means**: YES (mandatory).

## Username → Display Name map (Q-01 S2 / Q-06 cross-ref)
marydavis=Mary Davis · kevinp=Kevin Phillips · sheilac=Sheila Chamberlin · dcandee=Dawn Candee ·
sharrison=Stacy Harrison · timdavis=Tim Davis · lhorry=Leslie Horry · barbaral=Barbara Lankford ·
nmcelwee=Nate McElwee · katiep=Katie Pokorski · seth=Seth Neumann · sknaak=Steve Knaak ·
lloydc=Lloyd Chapman · erikam=Erika McBee · doughall=Douglas Hall · ehorry=Eric Horry ·
carrieturelli=Carrie Turelli · torih=Tori Howard · gracec=Grace Cooper · corym=Cory Munro ·
djuneau=Dana Juneau · foliveira=Flavia Oliveira · kerif=Keri Feeney · swilliamson=Scott Williamson ·
brentsanders=Brent Sanders
