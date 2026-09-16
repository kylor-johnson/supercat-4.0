# Q-22 — Feature Usage Depth (Mixpanel org_feature_usage_report)
- **Query**: Q-22 | **Org**: Crystorama (clm, org_id=64) | **Source**: BigQuery `supercat-data-pipeline.mixpanel.org_feature_usage_report` | **Run date**: 2026-06-12
- All-time cumulative event counts. total_events = 80,813; total_users = 100.

| feature (plain name) | event_count |
|---|---|
| Product Search (search_products) | 20,041 |
| Library/Document Views (view_library_entry) | 8,284 |
| Customer Search (search_for_customer) | 6,255 |
| Customer Selection (select_a_customer) | 4,057 |
| Sales Portal Access (access_sales_portal) | 2,089 |
| Collection Search (search_collections) | 783 |
| PDF Catalog Creation (create_pdf_catalog) | 599 |
| Email Item Info (email_item_info) | 494 |
| Product Filtering (filter_products) | 380 |
| SmartPicks Views (view_smartpicks) | 44 |
| Share My List (share_my_list) | 28 |
| Export to Excel (export_data_to_excel) | 21 |
| Export to CSV (export_data_to_csv) | 8 |
| Order Submission (submit_order) | 2 |
| Configured Item Orders (order_configured_item) | 0 |
| View Kit (view_kit) | 0 |
| Order Kit (order_kit) | 0 |

**Note**: Heavy product-search and library/catalog usage — a discovery/presentation-led platform. Order submission (2) is effectively untracked in Mixpanel for this org (Postgres is authoritative: 166 LTM iPad orders). Kit/CPQ features unused. Render non-zero features only; caveat the submit_order tracking gap in §8.
