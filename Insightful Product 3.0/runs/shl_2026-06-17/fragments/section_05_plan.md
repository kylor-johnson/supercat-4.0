# Section 05 Build Plan — Team Intelligence

Client: Savoy House Lighting (shl) · Run date 2026-06-17
Mode: ORDERS (SALES_SECTION_MODE = orders, 18 qualifying reps)
Confidence: SECTION_CONFIDENCE_5 = STRONG → template §5-STRONG, label "STRONG VIEW"
ADMIN_REPS_IN_LEADERBOARD = true (Jessica Romero) → admin disclosure REQUIRED in confidence header.
coaching_candidates.md = 0 candidates → Coaching Opportunities subsection SKIPPED entirely.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET (18 reps; Q-18 absent → source Q-01 Step 2 order data) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (coaching_candidates.md = 0 candidates) | NO (skip whole subsection) |
| How Much Business Goes Through eCat (Rep eCat Adoption 1b) | MANDATORY when PORTAL_REP_DATA_PRESENT | NOT MET (PORTAL_REP_DATA_PRESENT=False; Q-51 not present) | NO |
| Behavioral Archetypes | CONDITIONAL (MIXPANEL_USER_DATA_PRESENT) | MET (true; Q-01 S1/S2 present) | YES |
| Presentation-to-Close Conversion | CONDITIONAL (behavioral + order + Q-63 rows) | MET (Q-63 = 20 rows) — note: eCat order-conversion not tracked (all submit_order=0); framed as presentation effort | YES |
| Engagement Trajectory | CONDITIONAL (Q-06 QoQ data) | MET (Q-06 = 60 rows) | YES |
| New Item Launch Velocity | CONDITIONAL (HAS_PORTAL_ORDERS + HAS_NEW_ITEMS + rows) | NOT MET (Q-62 = 0 rows) | NO |
| Rep Engagement vs Account Revenue | CONDITIONAL (MIXPANEL + HAS_PORTAL_ORDERS + rows) | MET (Q-64 = 20 rows) | YES (collapsed) |
| Selling vs Admin Time | CONDITIONAL (MIXPANEL + rows + spread >20pp) | MET (Q-65 = 20 rows; spread 84.7–36.3 = 48.4pp > 20pp) | YES |
| Territory Coverage | CONDITIONAL (Q-43 + dormant accounts) | NOT MET (Q-43 absent; Q-43-S2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue | CONDITIONAL (HAS_PORTAL_ORDERS + PORTAL_REP_DATA_PRESENT + rows) | NOT MET (PORTAL_REP_DATA_PRESENT=False; Q-70 not present) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Rendering order (narrative arc)
1. Rep Leaderboard
2. Behavioral Archetypes
3. Presentation-to-Close Conversion
4. Engagement Trajectory
5. Rep Engagement vs Account Revenue (collapsed)
6. Selling vs Admin Time
7. Section-level what-this-means

## Leaderboard roster (18 qualifying reps, by eCat GMV LTM; operational "Customer Support" + "Grillo Customer Service" excluded)
Top 5: Mary McKey, Rob Azimi, Tom Wright, Dakota Duffield, Alton Mckey
Middle (6–13): Keeley - Luxeco Jackson, Matt Rowland, Kathy Phelps, Todd Tuchfarber, Shelly Meshwork, Jessica Romero, Jeff Brose, Adams Smith
Bottom 5: Cheryl LaRosa, Martin Blackley, Wayne Falk, Steven Shneer, Brittain Cherry

## Username → display name (Q-63/64/65 cross-ref via Q-01 S2 / Q-04)
shellym=Shelly Meshwork; bbuntz=Brad Buntz; marym=Mary McKey; wfalk1=Wayne Falk; kelley=Keeley - Luxeco Jackson; dakotaluxeco=Dakota Duffield; larosa=Cheryl LaRosa; trevl=Trevor Lindsay; kgrillo=Ken Grillo; bdobson=Brad Dobson; rjazimi=Rob Azimi; lbelesky=Lisa Belesky; stevens=Steven Shneer; jgannon=Julie Gannon; toddt=Todd Tuchfarber; gpassmore=Garrett Passmore; bgrillo=Beto Grillo; martinb=Martin Blackley; jerrysharp=Jerry Sharp; aminkhan=Amin Khan; charliek=Charlie Kissel; cmagana=Cynthia Magana.
Operational/support (EXCLUDE from behavioral tables): grillocs (Grillo Customer Service), starrylightssupport (Customer Support), sourceltg, zrapp, lbellanti, gsharp1.
