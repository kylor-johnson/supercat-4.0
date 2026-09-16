# Q-50: Library / Document Engagement Effectiveness — Buster & Punch (bp, org_id=250)
- **Query**: Q-50 (VM-50) — Postgres metadata only
- **Period**: Current snapshot
- **Run date**: 2026-04-21
- **Rows returned**: 5

| resource_id | document_name | resource_type | shared_document_file_name | created_at | updated_at | days_since_update |
|------------|--------------|---------------|--------------------------|------------|------------|------------------|
| 33085 | — | directory | — | 2025-06-05 | 2025-06-05 | 320 |
| 33082 | — | directory | — | 2025-06-05 | 2025-06-05 | 320 |
| 32245 | — | directory | — | 2025-04-11 | 2025-04-11 | 374 |
| 30632 | — | directory | — | 2024-12-04 | 2025-02-14 | 431 |
| 30651 | — | directory | — | 2024-12-05 | 2024-12-10 | 497 |

**Notes**:
- 5 top-level shared resources, all directory-type (folders, not individual documents)
- No document labels populated (all null)
- All resources are stale: 320–497 days since last update
- Despite stale metadata, Mixpanel shows 891 all-time library views and 35 email shares — library content is being accessed
- Per-document engagement breakdown not available without event-level Mixpanel query
