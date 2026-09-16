# Q-22: Feature Usage Depth
- **Org**: Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Period**: All-time cumulative (Mixpanel)
- **Run date**: 2026-04-21
- **Source**: BigQuery mixpanel.org_feature_usage_report
- **Rows returned**: 1

| Feature | Event Count |
|---------|-----------|
| search_products | 967 |
| filter_products | 683 |
| scan_item_with_camera | 895 |
| view_library_entry | 688 |
| select_a_customer | 263 |
| order_configured_item | 235 |
| search_collections | 160 |
| view_ipad_orders | 112 |
| view_cust_favorites | 103 |
| view_cust_backorders | 70 |
| view_cust_product_list | 70 |
| pdf_searches | 59 |
| view_my_list | 51 |
| submit_order | 50 |
| view_smartpicks | 40 |
| change_catalog_sort | 37 |
| search_for_customer | 38 |
| access_sales_portal | 30 |
| show_sales_in_catalog | 23 |
| email_item_info | 14 |
| view_placements | 8 |
| share_my_list | 8 |
| email_single_library_entry | 7 |
| create_pdf_catalog | 7 |
| order_from_maybe_list | 2 |

**Zero-count features**: create_my_list, edit_my_list, create_customer_product_list, create_maybe_list, export_data_to_csv, export_data_to_excel, email_multiple_library_entries, view_kit, order_kit, view_commitments, view_flipbook, add_to_list_from_flipbook, order_from_flipbook

**Totals**: total_events = 7,234; total_users = 22; active_users = 11; total_logins = 716

**Notable patterns**: Camera scanning (895 events) is the 2nd most-used feature — unusual and suggests field-based product identification workflow. Configured item ordering (235 events) indicates CPQ usage. Library viewing (688) is active. PDF catalog creation (7) and data exports (0) are nearly unused.
