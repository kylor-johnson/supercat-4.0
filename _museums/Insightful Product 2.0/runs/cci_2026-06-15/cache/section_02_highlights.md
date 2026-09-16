# Section 2 Highlights — Sales Team Performance
- **Client**: Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-15
- **Confidence tier**: PARTIAL

## Key Metrics
- **iPad GMV (trailing 12 months)**: $8.6M across 3,983 orders
- **Average Order Value**: $2,159
- **Active reps (last 90 days)**: 37
- **Total reps in leaderboard**: 40 (after excluding 3 showroom accounts)

## Top Performers
1. **Stacie Baker** — $765K GMV, 284 orders, broadest reach (131 customers)
2. **Rip Nance** — $557K GMV, highest order volume (327 orders)
3. **Lesley Blair** — $471K GMV, strong AOV ($2,631), 95 customers
4. **Sandy Glosson** — $434K GMV, 237 orders
5. **Carrie Haymore** — $404K GMV, 187 orders

## Accelerating Reps (quarter-over-quarter)
- **Shephalli Jain**: +140% orders (15→36), $196K current-quarter GMV
- **Stacey Chiavetta**: +135% orders (26→61), $118K current-quarter GMV
- **Lee Kram**: +233% orders (3→10), emerging contributor
- **Patty Miller**: +100% orders (14→28), $61K current-quarter GMV
- **Joanie Martin**: +82% orders (22→40), $73K current-quarter GMV

## Declining Reps (quarter-over-quarter)
- **Jodie Veeder**: −60% (20→8 orders), $30K current GMV — sharpest decline
- **Carrie Haymore**: −42% (50→29 orders), still producing $88K current GMV
- **Rip Nance**: −33% (84→56 orders), still top-3 by total GMV — likely seasonal
- **Sandy Glosson**: −33% (72→48 orders)
- **Betty Robbins**: −33% (27→18 orders)

## Showroom Exclusions
- 3 confirmed operational accounts excluded from leaderboard: CC Dallas Showroom ($728K), Atlanta Showroom ($401K), Highpoint Showroom ($84K)
- Aggregate showroom GMV: $1.2M (included in org-wide total)
- Allan Otto retained in leaderboard (admin-flagged but not confirmed operational in scan)

## Subsections Rendered
- §2.1 Rep Activity Ladder — rendered (Q-01 Step 2)
- §2.1b Rep eCat Adoption vs. Total Business — skipped (Q-51 returned 0 rows; name-matching produced no joins)
- §2.2 Behavioral Scorecard — skipped (MIXPANEL_USER_DATA_PRESENT = False)
- §2.3 Selling Archetypes — skipped (MIXPANEL_USER_DATA_PRESENT = False)
- §2.4 Coaching Opportunities — skipped (MIXPANEL_USER_DATA_PRESENT = False)
- §2.5 Rep Engagement Trajectory — rendered (Q-06)
- §2.6 Territory Coverage — skipped (Q-43 returned 0 rows)

## Data Gaps & Notes
- **Behavioral analytics unavailable**: Q-01 Step 1 returned 76 rows but MIXPANEL_USER_DATA_PRESENT gate is False (set by Stage 1 based on 0-row determination). Archetypes, funnel gaps, and coaching cards cannot be generated.
- **Q-51 name-matching failure**: PORTAL_REP_DATA_PRESENT is True (53 distinct rep names in portal_orders) but the LEFT JOIN on LOWER(TRIM(rep_name)) produced 0 matches, indicating portal_orders.rep_name formatting diverges from orders.rep_first_name + rep_last_name. This is a data-quality gap, not a missing-data gap.
- **Territory data absent**: Q-43 returned 0 rows — territories not configured for this org.
- **Admin disclosure appended**: Allan Otto (1 order, $594) is the only admin/internal user remaining in the leaderboard after showroom exclusions.

## Hypothetical Upside Opportunities
- [HYPOTHETICAL] If Jodie Veeder returns to prior-period pace (20 orders/quarter at $2,050 AOV), that represents +$25K potential quarterly GMV recovery.
- [HYPOTHETICAL] If Carrie Haymore returns to prior-period pace (50 orders/quarter at $2,160 AOV), that represents +$45K potential quarterly GMV recovery.
