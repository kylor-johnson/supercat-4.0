# Q-22 — Feature Usage Depth

- **Org:** Sarreid · org_id = 1
- **Period:** All-time (Mixpanel) / LTM where applicable
- **Row count:** 3 aggregate categories; detailed breakdown below
- **Run date:** 2026-04-17
- **Exclusions:** None

> **Note:** Direct query against org_feature_usage_report failed — column "product_search" does not exist in that table. Feature-level data sourced from Q-46 Mixpanel org-level query and aggregated Q-01 Step 1 user data instead.

---

## Aggregate Feature Categories (from Q-46 Mixpanel)

| feature | event_count |
|---------|------------|
| customer_targeting_events (select_a_customer + search_for_customer) | 15,295 |
| product_discovery_events (search_products + filter_products) | 35,849 |
| presentation_events (create_pdf_catalog + email_item_info + share_my_list) | 2,167 |

## Detailed Breakdown (from Q-01 Step 1 / org_summary)

| metric | value |
|--------|-------|
| access_sales_portal | 10,318 |
| submit_order | 891 |
| search_products | high activity across multiple users |
| create_pdf_catalog | significant usage |
| view_library_entry | active |
