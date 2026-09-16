# Section 05 Build Plan — Team Intelligence

Section: §5 · id=`team` · Title: Team Intelligence
Confidence tier (SECTION_CONFIDENCE_5): **FULL** → template `§5-FULL`, label "FULL PICTURE"
ADMIN_REPS_IN_LEADERBOARD = true → admin disclosure REQUIRED in confidence header.
Showroom excluded: 1 (HighPoint Showroom, $8,084) — excluded from leaderboard + behavioral subsections.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (5+ active reps) | MET — Q-18 absent, fallback Q-01 Step 2 has 30 order rows (29 after showroom exclusion) | YES |
| How Much Business Goes Through eCat (1b) | MANDATORY when gate met | NOT MET — PORTAL_REP_DATA_PRESENT=False AND Q-51 not present | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — MIXPANEL_USER_DATA_PRESENT=true | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has 20 rows; 6 reps ≥50 presentations | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET — coaching_candidates.md lists 0 candidates above floor | NO (skip entirely, no rollup) |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has QoQ data | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — Q-43 absent; Q-43-S2 returns 0 rows | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — Q-62 returns 0 rows | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | MET — Q-64 has 20 rows, MIXPANEL+HAS_PORTAL_ORDERS true | YES (collapsed) |
| Selling vs Admin Time (8) | CONDITIONAL | MET — Q-65 rows; spread 96.3%−39.6%=56.7pp > 20pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — Q-70 absent, PORTAL_REP_DATA_PRESENT=False | NO |

Section-level what-this-means: YES (mandatory).

## Notes
- Leaderboard uses Q-01 Step 2 columns (Orders/GMV/AOV/Unique Customers) — the data source the guide specifies; gold's eCat-share/all-channel columns require Q-51 data not available for clm.
- Username→display-name cross-ref (Q-63/64/65 → Q-01 Step 2 / Q-04 / Q-06):
  chardy=Clint Hardy, steven=Steven (no order-name match → "Steve Ricci"? ambiguous; steven has 109 accounts touched and is a Content/Library Manager non-selling role) — handle via Q-04 role context.
  kcavanagh=Kristen Cavanagh, megany=Megan Young, ptheos=Pauline Theos, zrapp=Zachary Rapp,
  bkrieger=Brad Krieger, bdobson2=Brad Dobson, smicheal=Stacey Micheal, ktaylor=Kevin Taylor,
  asharma=Amit Sharma (admin), robantonecchia=Rob Antonecchia, dunnlighting=Dunn Lighting,
  jpnich=Jeff Nicholson, katymccully=Katy McCully, mattsullivan=Matt Sullivan, jessicam=Jessica Mason,
  sebastianc=Sebastian Castrillon, sourceltg=Source Lighting (operational-ish), eduardoa=Eduardo Armenta,
  nickbrown=Nick Brown, vinceh=Vince Hall, mlieb=Melissa Leib, cframburg=Collin Framburg,
  philcook=Phil Cook, brucekremer=Bruce Kremer, eric_m=Eric Manzo, donporter=Don Porter, rmckillen=Ryan Mckillen,
  stephencaplight=Stephen Capitummino, amymatteson=Amy Matteson.
- MIXPANEL_ORDER_TRACKING_GAP = False per gate flags, BUT all Q-63 conversions are 0 and Q-01 submit_order all 0 → Mixpanel is not capturing iPad submit events; frame presentations as effort, do not claim "zero ordering" (Postgres shows real orders). Use Postgres orders (Q-01 S2) as the real signal.
