# Q-10: Feature Enablement Gap Analysis
- **Org:** Magnussen Home (mh, org_id=184)
- **Period:** Current snapshot
- **Rows:** 10
- **Run date:** 2026-04-20

Note: mobile_sites table returned 0 rows for organization_id=184. Feature enablement flags derived from BigQuery org_summary instead.

| Feature | Status |
|---|---|
| enable_sales_portal | — (no mobile_sites row) |
| enable_online_catalog | — (no mobile_sites row) |
| enable_online_ordering | — (no mobile_sites row) |
| kit_items | 1,348 (from BigQuery: view_kit=172, order_kit=92) |
| contract_prices | Present (data_versions shows fresh) |
| smart_stacks | 14 |
| shared_resources | 19 (directories) |
| portal_orders | 0 |
| feature_depth (from org_summary) | 4 |
| order_configured_item (Mixpanel) | 0 |
