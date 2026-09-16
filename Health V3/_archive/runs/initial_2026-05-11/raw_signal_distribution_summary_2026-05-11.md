# Health V3 Raw Signal Distribution Summary - 2026-05-11

- Raw signal CSV: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Health V3/runs/2026-05-11/raw_signal_extract_2026-05-11.csv`
- MAL used: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Health V2/inputs/master_account_list_2026-04-14_canonical.csv` (the exact `master_account_list.csv` file was not present)
- Cache used: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Health V3/cache/2026-05-11`
- As-of timestamp for recency/freshness math: `2026-05-12 00:00:00`
- Portfolio rows: 104
- Distribution denominator: 104 scored orgs (excluding `new_org_excluded = true`)

## Percentile Distribution

| Signal | Min | 10th pct | 25th pct | Median | 75th pct | 90th pct | Max | N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logins_90d | 7 | 97.10 | 313.75 | 926.50 | 2102.25 | 3619.90 | 15719 | 104 |
| active_user_ratio | 0 | 0.02 | 0.06 | 0.37 | 0.65 | 0.85 | 1.50 | 104 |
| days_since_last_login | 0 | 0 | 0 | 0 | 0 | 0 | 66 | 104 |
| catalog_pct | 0 | 0.60 | 0.81 | 0.96 | 0.99 | 1 | 1 | 104 |
| freshness_avg_staleness_ratio | 0.17 | 0.76 | 1.25 | 3.25 | 10.48 | 40.06 | 94.38 | 100 |
| features_used / features_applicable | 0.25 | 0.57 | 0.70 | 0.88 | 1 | 1 | 1 | 104 |
| channels_achieved / channels_applicable | 0 | 0.33 | 0.50 | 0.67 | 1 | 1 | 1 | 104 |

## Additional Rates

| Metric | Value | Denominator |
| --- | --- | --- |
| % of orgs with logins_90d = 0 | 0.0% | 104 |
| % of orgs with ipad_orders_90d = 0 | 22.1% | 104 |
| % of orgs with portal_orders_90d = 0 (among portal-configured orgs) | 31.4% | 51 |
| % of orgs with catalog_pct >= 0.85 | 72.1% | 104 |
| % of orgs with at least one import error | 49.0% | 104 |
