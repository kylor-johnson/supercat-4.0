# Q-06 — Rep Engagement Trajectory (90d current vs prior 90d)
- **Query**: Q-06 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `login_events` + `orders`
- **Period**: trailing 180 days, split into current 90d vs prior 90d | **Run date**: 2026-06-12
- Names normalized (double-spaces collapsed). Sorted by current-90d orders desc.

| rep_name | logins_prev_90d | logins_curr_90d | login_chg_% | orders_prev_90d | orders_curr_90d | order_chg_% | gmv_curr_90d |
|---|---|---|---|---|---|---|---|
| Katy McCully | 62 | 39 | −37.1 | 17 | 8 | −52.9 | $7,797.83 |
| Jeff Nicholson | 108 | 43 | −60.2 | 14 | 6 | −57.1 | $15,092.00 |
| Vince Hall | 65 | 18 | −72.3 | 6 | 2 | −66.7 | $5,064.40 |
| Zachary Rapp | 172 | 151 | −12.2 | 4 | 1 | −75.0 | $560.00 |
| Sebastian Castrillon | 13 | 1 | −92.3 | 0 | 1 | — | $2,649.60 |
| Matt Sullivan | 21 | 2 | −90.5 | 6 | 1 | −83.3 | $904.50 |
| Kristen Cavanagh | 38 | 27 | −28.9 | 0 | 1 | — | $3,361.95 |
| Steve Linder | 48 | 29 | −39.6 | 6 | 0 | −100.0 | $0.00 |
| Mike Hemsarth | 12 | 0 | −100.0 | 5 | 0 | −100.0 | $0.00 |
| Kevin Taylor | 86 | 64 | −25.6 | 2 | 0 | −100.0 | $0.00 |
| Megan Trosclair | 32 | 0 | −100.0 | 5 | 0 | −100.0 | $0.00 |
| Pauline Theos | 56 | 50 | −10.7 | 1 | 0 | −100.0 | $0.00 |
| Rob Hailpern | 20 | 2 | −90.0 | 1 | 0 | −100.0 | $0.00 |
| Forrest Denbow | 56 | 22 | −60.7 | 2 | 0 | −100.0 | $0.00 |
| Cindy Vackar | 82 | 44 | −46.3 | 1 | 0 | −100.0 | $0.00 |
| Kelly York | 66 | 16 | −75.8 | 2 | 0 | −100.0 | $0.00 |
| HighPoint Showroom | 1 | 0 | −100.0 | 1 | 0 | −100.0 | $0.00 |
| Steve Jones | 42 | 34 | −19.0 | 1 | 0 | −100.0 | $0.00 |
| Nick Brown | 47 | 21 | −55.3 | 2 | 0 | −100.0 | $0.00 |
| Collin Framburg | 51 | 13 | −74.5 | 2 | 0 | −100.0 | $0.00 |
| Brad Krieger | 324 | 267 | −17.6 | 2 | 0 | −100.0 | $0.00 |
| Shelly Orban | 71 | 27 | −62.0 | 3 | 0 | −100.0 | $0.00 |
| Chas Lassoff | 46 | 8 | −82.6 | 11 | 0 | −100.0 | $0.00 |
| Cindy Rogers | 88 | 52 | −40.9 | 1 | 0 | −100.0 | $0.00 |
| Jeff Izower | 24 | 2 | −91.7 | 1 | 0 | −100.0 | $0.00 |
| Brad Dobson | 28 | 4 | −85.7 | 4 | 0 | −100.0 | $0.00 |

**Note**: Seasonal trough — Q1 (Jan) was the order peak; current 90d (Mar–Jun) is the seasonal low. Login activity is broad-based but declining across the board. Login-only rows (no LTM orders) omitted from this excerpt; full FULL OUTER JOIN returned additional login-only names (Robin Boyd, Caleb Reiss, Stacey Micheal, Melissa Leib).
