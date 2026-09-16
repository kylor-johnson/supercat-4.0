# Q-22: Feature Usage Depth — Buster & Punch (bp, org_id=250)
- **Query**: Q-22 (VM-22)
- **Source**: BigQuery mixpanel.org_feature_usage_report
- **Period**: All-time cumulative
- **Run date**: 2026-04-21
- **Rows returned**: 1

| feature | event_count |
|---------|------------|
| total_events | 12,041 |
| total_users | 76 |
| active_users | 48 |
| total_logins | 2,411 |
| search_products | 2,244 |
| search_for_customer | 1,586 |
| select_a_customer | 890 |
| view_library_entry | 891 |
| pdf_searches | 215 |
| filter_products | 126 |
| view_my_list | 81 |
| view_ipad_orders | 73 |
| submit_order | 66 |
| change_catalog_sort | 54 |
| view_placements | 46 |
| create_pdf_catalog | 29 |
| email_single_library_entry | 28 |
| email_item_info | 20 |
| search_collections | 9 |
| email_multiple_library_entries | 7 |
| share_my_list | 5 |
| edit_my_list | 3 |
| view_cust_favorites | 2 |
| view_smartpicks | 1 |
| access_sales_portal | 0 |
| create_my_list | 0 |
| create_customer_product_list | 0 |
| view_cust_product_list | 0 |
| create_maybe_list | 0 |
| export_data_to_csv | 0 |
| export_data_to_excel | 0 |
| show_sales_in_catalog | 0 |
| view_cust_backorders | 0 |
| view_kit | 0 |
| order_kit | 0 |
| order_configured_item | 0 |
| order_from_maybe_list | 0 |
| scan_item_with_camera | 0 |
| view_commitments | 0 |
| view_flipbook | 0 |
| add_to_list_from_flipbook | 0 |
| order_from_flipbook | 0 |

**Notes**:
- Top features by usage: Product Search (2,244), Customer Search (1,586), Customer Selection (890), Library (891)
- Order submission (66) reflects all-time cumulative — 19 orders exist in Postgres, so Mixpanel captured ~66 submit events (multiple submissions per order possible)
- Zero usage: Sales Portal, CSV/Excel export, CPQ (kits, configured items), camera scanning, flipbook
- Library engagement present: 891 views + 35 email shares
- My List: modest usage (81 views, 5 shares, 3 edits)
