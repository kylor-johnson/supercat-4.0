# Q-50 — Library / Document Engagement Effectiveness (Postgres metadata)
- **Query**: Q-50 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `shared_resources` (parent_id IS NULL) | **Run date**: 2026-06-12
- **Top-level resources**: 5 (all directories) | **Stale (no update 90d+)**: 5 | **Total shared_resources incl. children**: 36
- Per-document view/email engagement is Mixpanel-side (aggregate: `view_library_entry`, library emails — see Q-22/Q-01).

| resource_id | document_name | resource_type | created_at | days_since_update |
|---|---|---|---|---|
| 26947 | — | directory | 2024-01-12 | 703 |
| 353 | — | directory | 2015-06-17 | 1,976 |
| 328 | — | directory | 2015-06-17 | 1,976 |
| 346 | — | directory | 2015-06-17 | 1,976 |
| 333 | — | directory | 2015-06-17 | 1,976 |

**Note**: Top-level shared resources are 5 directory containers (all stale at the folder level — folder metadata rarely changes). 36 total shared resources including child documents. Document-level engagement counts require Mixpanel coverage; Postgres provides the stale-metadata signal only. Never attribute sales outcomes to document views.
