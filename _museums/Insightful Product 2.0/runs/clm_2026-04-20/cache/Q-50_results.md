# Q-50: Library / Document Engagement Effectiveness — Crystorama (clm, org_id=64)
- **Query**: Q-50 (Postgres — shared_resources inventory)
- **Period**: Current snapshot
- **Row count**: 5 (root-level directories)
- **Run date**: 2026-04-20

## Document Inventory (Root Level)

| resource_id | document_name | resource_type | shared_document_file_name | created_at | updated_at | days_since_update |
|------------|-------------|--------------|--------------------------|-----------|-----------|------------------|
| 26947 | — | directory | — | 2024-01-12 | 2024-07-09 | 650 |
| 353 | — | directory | — | 2015-06-17 | 2021-01-13 | 1,923 |
| 328 | — | directory | — | 2015-06-17 | 2021-01-13 | 1,923 |
| 346 | — | directory | — | 2015-06-17 | 2021-01-13 | 1,923 |
| 333 | — | directory | — | 2015-06-17 | 2021-01-13 | 1,923 |

## Mixpanel Engagement (from org_feature_usage_report)

| metric | count |
|--------|-------|
| view_library_entry | 7,832 |
| email_single_library_entry | 499 |
| email_multiple_library_entries | 83 |
| pdf_searches | 1,366 |

**Note**: Root-level shared_resources are all directories with null labels. Subdocuments exist under these directories. Library engagement is active (7,832 views, 582 email shares) despite the stale directory metadata.
