# Section 05 Build Plan — Team Intelligence

- **Client**: Coleto Brands | Progress Lighting (prog), run 2026-06-17
- **Mode**: ENGAGEMENT (`SALES_SECTION_MODE = engagement`; order_reps=0, engagement_reps=14)
- **Confidence tier**: `SECTION_CONFIDENCE_5 = PARTIAL` → §5-PARTIAL / "PARTIAL VIEW"
- **Leaderboard basis**: ranked by **Total Events (app activity)**, NOT order GMV
- **Admin disclosure**: `ADMIN_REPS_IN_LEADERBOARD = true` (Michelle Miller) → disclosure appended to confidence header
- **Showroom exclusions**: 0 flagged
- **MIXPANEL_ORDER_TRACKING_GAP**: false (do not claim "zero ordering")

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard (engagement-mode, by Total Events) | MANDATORY (section gate, 14 engagement reps) | MET | YES |
| Coaching Opportunities (subsection 3) | CONDITIONAL | NOT MET (coaching_candidates.md lists 0 candidates) | NO |
| Rep eCat Adoption vs Total Business (1b) | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-51 absent) | NO |
| Behavioral Archetypes (2) | CONDITIONAL | MET (MIXPANEL_USER_DATA_PRESENT=true) | YES |
| Presentation-to-Close Conversion (2b) | CONDITIONAL | MET (Q-63 has 4 rows; behavioral data present) — but qualifying gate is 50+ presentations; 0 reps qualify | NO (note in confidence header) |
| Engagement Trajectory (4) | CONDITIONAL | MET (Q-06 QoQ data present) | YES |
| New Item Launch Velocity (6) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, HAS_NEW_ITEMS=false; Q-62 absent) | NO |
| Rep Engagement vs Account Revenue (7) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-64 absent) | NO |
| Selling vs Admin Time (8) | CONDITIONAL | MET (Q-65 11 rows; spread 77.1%–19.4% = 57.7pp > 20pp) | YES |
| Territory Coverage (5) | CONDITIONAL | NOT MET (Q-43 absent; Q-43-S2 returned 0 rows) | NO |
| Inactive Reps with Territory Revenue (9) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, PORTAL_REP_DATA_PRESENT=false; Q-70 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Notes
- Presentation-to-Close (2b): Q-63 shows only 4 reps with presentation activity, max 46 presentations (Dunn Lighting), all with 0 orders. The guide hard-requires **50+ presentations** to qualify. Zero reps clear that bar → subsection skipped; gap noted in confidence header. The presentation-activity signal is folded into the Behavioral Archetypes narrative instead.
- Engagement-mode leaderboard columns: # · Rep · Days Active · Customer Selections · Product Searches · Presentations · Total Events. Order/GMV/AOV/Unique-Customers columns dropped.
- Presentations = create_pdf_catalog + email_item_info + share_my_list.
