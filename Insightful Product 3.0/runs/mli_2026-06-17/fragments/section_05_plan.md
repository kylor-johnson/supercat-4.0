# Section 05 Build Plan — Team Intelligence

**Mode**: `SALES_SECTION_MODE = engagement` (order_reps=1, engagement_reps=68).
Leaderboard built from app selling-activity (Q-01 Step 1), ranked by Total Events.
GMV/order leaderboard suppressed (eCat order volume ~0).

**Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → template `§5-PARTIAL`, label "PARTIAL VIEW".
**Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` (Nathen Bliss) → disclosure appended to confidence header.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate, 68 engagement reps) | MET (engagement mode, Q-01 Step 1) | YES |
| How Much Business Goes Through eCat (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 absent) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 20 rows) | YES |
| Coaching Opportunities (3) | MANDATORY when ≥1 candidate | MET (1 candidate: Mike Elford, $72,509) | YES |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 has QoQ data) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-62 absent) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 absent) | NO |
| How Reps Spend Their Time in the App (8) | CONDITIONAL (spread >20pp) | MET (spread 95.5−60.1 = 35.4pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-70 absent) | NO |

**Section-level what-this-means**: YES (mandatory).

## Engagement Leaderboard derivation (Q-01 Step 1, rank by Total Events desc)
Presentations = create_pdf_catalog + email_item_info + share_my_list.
Username → display name via Q-01 Step 2 / Q-06 cross-reference.

Top 5: Kyra Gregory (kgregory5), Steve Ricci (steven), Brad Krieger (bkrieger),
Cathy/Chad Teiber (cathychad), Tim Green (greent).
