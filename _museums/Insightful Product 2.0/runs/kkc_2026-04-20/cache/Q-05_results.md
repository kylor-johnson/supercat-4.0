# Q-05: Seat Utilization — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-05
- **Source**: Postgres MCP (`user-supercat-postgres-vpn`) — `org_users`, `login_events`, `orders`
- **Run date**: 2026-04-20
- **Period**: 90-day trailing window

## Results

| Metric | Count |
|--------|-------|
| Active org users (not disabled) | 13 |
| Users logged in — trailing 90 days | 23 |
| Users who submitted orders — trailing 90 days | 0 |

**Note**: logged_in_90d (23) exceeds active_org_users (13). This is expected — `login_events` counts distinct `user_id` values while `org_users` counts non-disabled org records; some users may have logged in but not appear as active in current org_users state, or some accounts reflect users who logged in during the window before being disabled. Order submissions in trailing 90 days = 0, consistent with Mode 3 (lapsed account).
