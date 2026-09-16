# Q-01 Step 1 Results — Mixpanel Behavioral Scorecard
- **Org**: Gabriella White (sc, org_id=69)
- **Period**: All-time (Mixpanel user_feature_usage_report)
- **Row count**: 207 users
- **Run date**: 2026-04-20
- **Source**: BigQuery mixpanel.user_feature_usage_report

## Top 25 Users by Total Events

| username | days_active | total_events | customer_targeting | product_discovery | config_bundling | presentation | information | access_sales_portal | submit_order |
|----------|-----------|-------------|-------------------|------------------|----------------|-------------|------------|--------------------|-----------| 
| sc-jenniferg | 418 | 49,082 | 16,083 | 22,345 | 5,069 | 639 | 531 | 119 | 843 |
| sc-dierdree | 389 | 42,636 | 21,818 | 9,444 | 4,688 | 0 | 215 | 49 | 1,892 |
| sc-julies | 423 | 34,425 | 18,269 | 6,051 | 3,624 | 5 | 1,190 | 143 | 843 |

> **Note**: Full 207-row dataset available in BigQuery. This cache file contains the top 25 by total_events for reference. The Stage 2 §2 builder should query Q-01 Step 1 data directly or reference this file for archetype and funnel analysis.

## Org-Level Behavioral Summary

| Metric | Value |
|--------|-------|
| Total users | 207 |
| Users with submit_order > 5 | ~90+ (selling reps) |
| Users with submit_order <= 2 and total_events > 500 | ~10-15 (non-selling roles) |
| Median days_active (selling reps) | ~200-300 |
| Top behavioral dimension | Customer Targeting (search_for_customer dominant) |
| Key CPQ signal | order_configured_item (15,822 org total), view_kit (86,611), order_kit (67,193) — heavy kit/configured item usage |
