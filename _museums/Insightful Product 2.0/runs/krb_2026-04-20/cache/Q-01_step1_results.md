# Q-01 Step 1: Rep Behavioral Scorecard (Mixpanel)
- **Org**: Kaleen Rugs & Broadloom (krb, org_id=244)
- **Source**: BigQuery mixpanel.user_feature_usage_report
- **Period**: All-time cumulative
- **Rows returned**: 8
- **Run date**: 2026-04-20
- **Note**: Run as part of Mixpanel User Data Check (derived gate). Q-01 Step 2 (Postgres orders) skipped — HAS_SALES_SECTION = false.

| username | days_active | total_events | first_event | last_event | customer_targeting | product_discovery | config_bundling | presentation | information | submit_order |
|----------|------------|-------------|-------------|------------|-------------------|------------------|----------------|-------------|-------------|-------------|
| tandtmillerfam | 31 | 623 | 2025-02-02 | 2025-03-31 | 39 | 164 | 0 | 0 | 63 | 1 |
| colelewis | 10 | 66 | 2025-02-17 | 2026-04-08 | 13 | 2 | 0 | 0 | 4 | 0 |
| chuck-user | 9 | 11 | 2024-12-04 | 2025-12-03 | 0 | 0 | 0 | 0 | 0 | 0 |
| jonv | 3 | 5 | 2024-11-22 | 2024-12-10 | 0 | 0 | 0 | 0 | 0 | 0 |
| kylor_johnson | 1 | 4 | 2026-02-04 | 2026-02-04 | 0 | 0 | 0 | 0 | 0 | 0 |
| swt | 1 | 4 | 2024-12-04 | 2024-12-04 | 0 | 0 | 0 | 0 | 0 | 0 |
| timbrunson | 1 | 3 | 2025-08-21 | 2025-08-21 | 0 | 0 | 0 | 0 | 0 | 0 |
| cwiebe | 1 | 1 | 2025-08-20 | 2025-08-20 | 0 | 0 | 0 | 0 | 0 | 0 |

Note: Only 1 user (tandtmillerfam) has meaningful behavioral depth (623 events, 31 active days). Only 1 submit_order event across all 8 users. 6 of 8 users have minimal activity (≤11 events).
