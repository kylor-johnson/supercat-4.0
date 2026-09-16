# Q-05: Seat Utilization
- **Query ID**: Q-05 (VM-05)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Period**: Trailing 90 days
- **Row count**: 1
- **Run date**: 2026-04-16
- **Exclusions**: None

| Metric | Value |
|--------|-------|
| active_org_users | 310 |
| logged_in_90d | 49 |
| ordering_users_90d | 831 |

Note: ordering_users_90d (831) exceeds active_org_users (310) because ordering_users counts distinct org_user_id values from orders — this includes eCat Online (server) orders which may be placed by buyers who are not in org_users (they have org_user_id from session). The 49 logged_in_90d represents iPad/direct login users only. The 310 active_org_users is the configured seat count.
