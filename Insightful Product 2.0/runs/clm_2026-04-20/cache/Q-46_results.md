# Q-46: eCat Selling Workflow Maturity — Crystorama (clm, org_id=64)
- **Query**: Q-46 (Postgres + BigQuery Mixpanel)
- **Period**: LTM (Postgres), all-time (Mixpanel)
- **Run date**: 2026-04-20

## Postgres Side — eCat Order Outcomes

- **LTM eCat submitted orders**: 168
- **LTM iPad orders**: 168
- **LTM eCat Online orders**: 0

## Mixpanel Side — Behavioral Feature Usage (from org_feature_usage_report)

| feature | event_count |
|---------|------------|
| submit_order | 2 |
| select_a_customer | 3,757 |
| search_for_customer | 5,683 |
| search_products | 19,067 |
| filter_products | 367 |
| create_pdf_catalog | 566 |
| email_item_info | 471 |
| share_my_list | 25 |
| view_library_entry | 7,832 |
| view_kit | 0 |
| order_kit | 0 |
| order_configured_item | 0 |
| access_sales_portal | 1,875 |
| export_data_to_csv | 8 |
| export_data_to_excel | 21 |
| scan_item_with_camera | 2,484 |
| view_smartpicks | 44 |
| view_cust_favorites | 87 |
| view_cust_backorders | 56 |
| show_sales_in_catalog | 22 |
| view_flipbook | 0 |
| total_events | 75,788 |
| total_users | 99 |
| active_users | 69 |
| total_logins | 7,707 |

**Note**: submit_order from Mixpanel (2) ≪ submitted orders from Postgres (168). This discrepancy is expected — Mixpanel tracks the in-app "Submit Order" button tap, while Postgres counts all submitted orders including those submitted via batch/sync workflows.
