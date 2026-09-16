# Section 05 Build Plan — Team Intelligence

- **Section**: §5 Team Intelligence (id: `team`)
- **Client**: Capital Lighting Fixture Co. (clc, org_id=40)
- **Confidence tier**: `SECTION_CONFIDENCE_5 = STRONG` → label **STRONG VIEW**, template `§5-STRONG`
- **Admin disclosure required**: YES (`ADMIN_REPS_IN_LEADERBOARD = true` → Liz Townsend, Tim Pirkl)
- **Showroom exclusions**: 1 (Capital Lighting, $19,218 — confirmed operational; excluded from leaderboard & archetypes)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Rep Leaderboard | MANDATORY (section gate) | MET (Q-01 Step 2 = 40 order rows, 5+ active reps) | YES |
| Rep eCat Adoption vs Total Business | MANDATORY | MET (`PORTAL_REP_DATA_PRESENT = true`; Q-51 = 25 rows) | YES |
| Behavioral Scorecard Spotlight | CONDITIONAL | MET (`MIXPANEL_USER_DATA_PRESENT = true`; Q-01 data present) | YES |
| Presentation-to-Close Conversion | CONDITIONAL | MET (Q-63 = 20 rows; 7 reps with 50+ presentations after exclusions) | YES |
| Coaching Opportunities | MANDATORY when ≥1 candidate | NOT MET (`coaching_candidates.md` = 0 candidates above $50K floor) | NO (skip entirely — no rollup, no cards) |
| Engagement Trajectory | CONDITIONAL | MET (Q-06 = 75 rows QoQ login/order change) | YES |
| New Item Launch Velocity by Rep `[COLLAPSE]` | CONDITIONAL | MET (`HAS_PORTAL_ORDERS=true` + `HAS_NEW_ITEMS=true`; Q-62 = 20 rows) | YES (collapsed) |
| Rep Engagement vs Account Revenue `[COLLAPSE]` | CONDITIONAL | MET (`MIXPANEL_USER_DATA_PRESENT=true` + `HAS_PORTAL_ORDERS=true`; Q-64 = 20 rows) | YES (collapsed) |
| Selling vs Admin Time | CONDITIONAL (spread >20pp) | MET (Q-65 = 20 rows; spread 31.8pp after operational exclusion) | YES |
| Territory Coverage `[COLLAPSE]` | CONDITIONAL | NOT MET (Q-43 not present; Q-43-S2 = 0 rows) | NO |
| Inactive Reps with Territory Revenue `[COLLAPSE]` | CONDITIONAL | NOT MET (Q-70 = 0 rows) | NO |

## Render order (narrative arc; collapses clustered before section close)

1. Rep Leaderboard (STRENGTH) — Top 5 / collapsed middle / Bottom 5
2. How Reps' Orders Come In (1b — INTELLIGENCE; DIGITAL ENABLEMENT framing)
3. Behavioral Archetypes (2 — INTELLIGENCE)
4. Presentation-to-Close Conversion (2b — INTELLIGENCE/OPPORTUNITY)
5. Engagement Trajectory (4 — INTELLIGENCE)
6. How Reps Spend Their Time in the App (8 — OPPORTUNITY)
7. New Item Launch Velocity `[COLLAPSE]` (6)
8. Rep Engagement vs Account Revenue `[COLLAPSE]` (7)
9. Section-level what-this-means + "With Connected Data" note

## Build notes

- **Leaderboard source**: Q-18 absent → use Q-01 Step 2 (rep order outcomes: orders, GMV, AOV, unique customers — same shape). ORDERS-mode columns per guide: #, Rep, Orders (LTM), GMV (LTM), AOV, Unique Customers. Form per guide: Top 5 row-highlight visible → `<details>` collapsed middle → Bottom 5 visible. No what-this-means.
- **Exclusions**: Capital Lighting (brand/operational, $19,218, confirmed by showroom scan) and the clearly-operational entities Customer Support / Capital Lighting Fixture excluded from individual leaderboard & archetypes. starrylightssupport / capcan excluded from behavioral tables (operational). Admins Liz Townsend & Tim Pirkl kept in leaderboard, disclosed in confidence header.
- **1b — DIGITAL ENABLEMENT reframe**: title is "How Reps' Orders Come In". All 25 Q-51 rows run entirely off eCat → enablement opportunity (streamline rep-assisted/manual portion), NOT capture/activation/untapped/adoption-gap. Metric cards: eCat share of team business (~2%), top/bottom quartile eCat use, top-to-bottom range. Callout names 5 highest-volume off-eCat agency books. Acknowledge much volume legitimately belongs on web/EDI.
- **Banned-term substitutions**: NEVER "capture rate / activation target / untapped / adoption gap". "platform"→"app/eCat"; "ERP"→"total business"; time-card title "How Reps Spend Their Time in the App".
- **2b reps with 50+ presentations** (post-exclusion of starrylightssupport): Timie Kozaryn 270, Anita Laidlaw 186, Clint Hardy 106, Shelly Orban 61, Dunn Lighting 58, Jeff Nicholson 58, Cody Adler 55. Only Jeff Nicholson converts (3.4%).
- **Q-65 spread**: 94.7% (capcan, operational — excluded) → with capcan excluded, top = Mitchell Winston 81.3%, bottom = Scott Connell 49.5% → 31.8pp > 20pp gate passes.
- what-this-means on every rendered subsection except Rep Leaderboard. Coaching skipped (0 candidates).
