# Q-22: Feature Usage Depth — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-22
- **Source**: BigQuery `mixpanel.org_feature_usage_report`
- **Period**: All-time cumulative
- **Rows**: 1

| Feature | Event Count |
|---------|------------|
| total_users | 42 |
| active_users | 24 |
| total_logins | 1,261 |
| total_events | 4,563 |
| search_products | 607 |
| filter_products | 15 |
| change_catalog_sort | 12 |
| search_collections | 19 |
| create_my_list | 0 |
| edit_my_list | 7 |
| view_my_list | 120 |
| share_my_list | 1 |
| create_customer_product_list | 0 |
| view_cust_product_list | 0 |
| create_maybe_list | 0 |
| email_item_info | 22 |
| create_pdf_catalog | 253 |
| export_data_to_csv | 0 |
| export_data_to_excel | 0 |
| view_library_entry | 834 |
| email_single_library_entry | 12 |
| email_multiple_library_entries | 17 |
| pdf_searches | 114 |
| select_a_customer | 10 |
| search_for_customer | 31 |
| show_sales_in_catalog | 0 |
| view_cust_favorites | 0 |
| view_cust_backorders | 0 |
| view_smartpicks | 0 |
| access_sales_portal | 0 |
| view_ipad_orders | 2 |
| view_kit | 0 |
| order_kit | 0 |
| order_configured_item | 20 |
| order_from_maybe_list | 0 |
| scan_item_with_camera | 0 |
| submit_order | 0 |
| view_placements | 0 |
| view_commitments | 0 |
| view_flipbook | 0 |
| add_to_list_from_flipbook | 0 |
| order_from_flipbook | 0 |

**MIXPANEL_ORDER_TRACKING_GAP note**: submit_order = 0 in Mixpanel while Postgres shows 41 all-time eCat orders. Mixpanel is not tracking iPad order submissions for this org.
