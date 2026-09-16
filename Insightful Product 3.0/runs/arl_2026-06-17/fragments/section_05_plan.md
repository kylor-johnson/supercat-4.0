# Section 05 Build Plan — Team Intelligence

**Mode**: ENGAGEMENT (`SALES_SECTION_MODE = engagement`) — few eCat order reps (4), many active app users (17). Leaderboard ranked by **app activity (Total Events)** from Q-01 Step 1, NOT order GMV.
**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → §5-PARTIAL template, "PARTIAL VIEW" label.
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` → Lee Nemeth, Nadia Quintero, Sophia Wang flagged in confidence header.
**Order-tracking gap**: `MIXPANEL_ORDER_TRACKING_GAP = true` → all `submit_order = 0` in Mixpanel; do NOT claim reps have zero ordering. Use Postgres orders (Q-01 Step 2) where order context is needed.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, engagement basis) | MET (17 engagement reps ≥ 5; Q-01 S1 = 64 rows) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md lists 0 — "No coaching cards for this client") | NO (skip entirely) |
| Rep eCat Adoption vs Total Business (1b) | MANDATORY when gate met | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 not present) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 10 data rows; Q-01 behavioral present) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data, 57 rows) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 not present / Q-43-S2 = 0 rows) | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 not present) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 not present) | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET (Q-65 has 20 rows; spread 73.7pp > 20pp) | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-70 not present) | NO |

## Leaderboard basis (engagement columns)
Columns: # · Rep · Days Active · Customer Selections (`select_a_customer`) · Product Searches (`search_products`) · Presentations (`create_pdf_catalog` + `email_item_info` + `share_my_list`) · Total Events. Sorted by Total Events desc. Top 5 visible / collapsed middle / bottom 5 visible.

Username → display name (Q-01 S2 / Q-06 cross-ref): nadia=Nadia Quintero, sophiawang=Sophia Wang, lee=Lee Nemeth, nicole=Nicole Bretzing, cindyvackar=Cindy Vackar, steveknighten=Steve Knighten, salesra=Sales Arabela, petercs=Peter Saiolla, eric_m=Eric Manzo, forrestdenbow=Forrest Denbow, libbyh=Libby Hancock, timiek=Timie Kozaryn, donporter=Don Porter, hreyes=Hector Reyes, karl=Karl Prekaski, bellawang=Bella Wang, kirk_johnson=Kirk Johnson, markrottner=Mark Rottner, cynthiazeidler=Cynthia Zeidler, rjohnson1=Rita Johnson, daveb=Dave Bock, jgannon=Julie Gannon, tlascari=Ted Lascari, broche=Brian Roche, adams=Adams Smith, jonmcmahan=Jon McMahan, jonv=Jon Vanderberg, jackh=Jack Helbert, thel70=Larry Jenkins, dpatruno=Dino Patruno, rubenv=Ruben Vargas, astauffacher=Allison Stauffacher, chuckvienna=Chuck Vienna, jasonburns=Jason Burns, tstauffacher=Tami Stauffacher, donnaallen=Donna Allen, larryjmich, kgannon=Kevin Gannon, terrencet=Terence Timlin.

Admin/support users (per Q-04 classification) Nadia, Sophia, Lee retained in leaderboard per gold-standard practice; admin disclosure noted in header.
