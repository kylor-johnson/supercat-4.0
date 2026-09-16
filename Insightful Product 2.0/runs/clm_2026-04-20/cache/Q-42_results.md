# Q-42: New Item Performance — Crystorama (clm, org_id=64)
- **Query**: Q-42 (Postgres — products flagged new_item = true)
- **Period**: Current snapshot
- **Row count**: 1 (summary)
- **Run date**: 2026-04-20

## Summary

| new_item_count | catalog_ready |
|---------------|--------------|
| 44 | 44 |

**Note**: All 44 new items have images and prices (100% catalog-ready). Per-item eCat order attribution requires order_items JSON parsing which was not executed in this run. ERP-level new item sales can be derived from Q-39 collection data where new collections are identified.
