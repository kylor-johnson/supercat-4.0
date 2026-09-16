# Section 05 Build Plan — Team Intelligence

**Mode**: ENGAGEMENT (`SALES_SECTION_MODE = engagement`, `ENGAGEMENT_REP_COUNT = 24`, `order_reps = 0`)
**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → template `§5-PARTIAL`, label "PARTIAL VIEW"
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = False` → not appended
**Order-tracking gap**: `MIXPANEL_ORDER_TRACKING_GAP = False` → real orders exist (Postgres LTM = 12); never claim "zero ordering"

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET — engagement mode, rank by Total Events (Q-01 Step 1, 24 active reps) | YES |
| How Much Business Goes Through eCat (1b) | CONDITIONAL | NOT MET — `PORTAL_REP_DATA_PRESENT = False`, Q-51 not present | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET — `MIXPANEL_USER_DATA_PRESENT = True` | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET — Q-63 has 13 data rows | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | NOT MET — `coaching_candidates.md` lists 0 candidates above $50K floor | NO (skip entirely) |
| Engagement Trajectory (4) | CONDITIONAL | MET — Q-06 has 60 rows of QoQ data | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET — `HAS_PORTAL_ORDERS = False`, Q-43 empty | NO |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET — `HAS_PORTAL_ORDERS = False`, `HAS_NEW_ITEMS = False`, Q-62 absent | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET — `HAS_PORTAL_ORDERS = False`, Q-64 absent | NO |
| Selling vs Admin Time (8) | CONDITIONAL (spread >20pp) | MET — Q-65 has 20 rows; spread 80.8%→1.9% ≈ 79pp > 20pp | YES |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET — `HAS_PORTAL_ORDERS = False`, `PORTAL_REP_DATA_PRESENT = False`, Q-70 absent | NO |

**Rendered subsections (5)**: Rep Leaderboard · Behavioral Archetypes · Presentation-to-Close Conversion · Engagement Trajectory · How Reps Spend Their Time in the App
**Plus**: section-level what-this-means.

## Leaderboard basis
Engagement mode — ranked by **Total Events (app selling activity, LTM)** from Q-01 Step 1.
Columns: # · Rep · Days Active · Customer Selections · Product Searches · Presentations · Total Events.
Order/GMV/AOV/Unique-Customers columns dropped (near-zero in engagement mode).
Top 5 visible / collapsed middle / bottom 5 visible, sorted by Total Events desc.
Usernames resolved to display names via Q-01 Step 2 / Q-06 cross-reference.
