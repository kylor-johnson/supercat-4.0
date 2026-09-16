# Q-05: Seat Utilization — Buster & Punch (bp, org_id=250)
- **Query**: Q-05 (VM-05)
- **Period**: Rolling 90 days
- **Run date**: 2026-04-21
- **Rows returned**: 1

| metric | value |
|--------|-------|
| active_org_users | 81 |
| logged_in_90d | 48 |
| ordering_users_90d | 3 |

**Derived**:
- Login utilization (90d): 59.3% (48 of 81 active users logged in)
- Ordering utilization (90d): 3.7% (3 of 81 active users submitted orders)
- Login-to-order gap: 45 users logged in but did not submit orders in last 90 days
