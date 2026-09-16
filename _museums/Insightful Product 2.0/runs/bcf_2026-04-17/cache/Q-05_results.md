# Q-05 — Seat Utilization

- **Org:** Braxton Culler (bcf, org_id=171)
- **Period:** 90-day lookback for login/ordering activity
- **Guardrails:** `is_marked_deleted = false OR IS NULL` on orders
- **Rows returned:** 1
- **Run date:** 2026-04-17

| active_org_users | logged_in_90d | ordering_users_90d |
|---|---|---|
| 72 | 53 | 152 |
