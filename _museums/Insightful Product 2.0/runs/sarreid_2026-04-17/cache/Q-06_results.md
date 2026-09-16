# Q-06 — Rep Engagement Trajectory (VM-06)

- **Org:** SARREID (sarreid, org_id=1)
- **Period:** 180-day rolling window (current 90d vs. prior 90d)
- **Row count:** ~63 (selling reps + login-only users)
- **Run date:** 2026-04-17
- **Exclusions:** "Sarreid Showroom" excluded per showroom scan

---

**Key selling rep trajectories:**

| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
|----------|----------------|-------------------|-----------------|----------------|-------------------|-----------------|----------------|
| Clyde Barnard | — | — | +11.4% | — | — | -31.3% | $71,059 |
| John Anhut | — | — | -11.9% | — | — | -16.7% | $59,420 |
| Charity Queen | — | — | +39.6% | — | — | +60.0% | $57,570 |
| Stan Terry | — | — | +19.4% | — | — | +57.1% | $53,930 |
| Deborah Klein | — | — | +8.0% | — | — | +7.1% | $39,965 |
| Rip Nance | — | — | +70.0% | — | — | -47.4% | $23,607 |
| Ryan McWilliams | — | — | +24.0% | — | — | -66.7% | $19,224 |
| Danielle Green | — | — | +39.5% | — | — | -71.4% | $10,893 |
| Joan Harrison | — | — | +61.8% | — | — | -50.0% | $10,255 |

**Disengaged reps (prev 90d active → current 0 orders):**

| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
|----------|----------------|-------------------|-----------------|----------------|-------------------|-----------------|----------------|
| Jenny Bowers | — | — | +531.4% | — | 0 | -100.0% | $0 |
| Rip Nance | — | — | +70.0% | — | — | -47.4% | $23,607 |
| Hannah Hoxworth | — | — | -92.7% | — | 0 | -100.0% | $0 |
| April Davis | — | — | -30.3% | — | 0 | -100.0% | $0 |
| Carmy Muller | — | — | -92.3% | — | 0 | -100.0% | $0 |
| Bert Wood | 0 | 0 | -100.0% | — | 0 | -100.0% | $0 |
| Beth Sartore | 0 | 0 | -100.0% | — | 0 | -100.0% | $0 |
| Bridget Delaney | 0 | 0 | -100.0% | — | 0 | -100.0% | $0 |

> Full query returned ~63 rows including login-only users (those with login activity but no LTM orders in the 180-day window). Absolute login/order counts (logins_prev_90d, logins_current_90d, orders_prev_90d, orders_current_90d) available in source query results. This cache captures the key trend percentages and GMV dictated during Stage 1 data gathering. Reps with -100.0% logins have fully disengaged (logins_current_90d = 0). Jenny Bowers shows +531.4% login growth but -100% orders — logged in but not ordering.
