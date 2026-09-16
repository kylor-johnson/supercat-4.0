# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status Dashboard | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Operational Alerts (Action Required) | CONDITIONAL | MET (12 entities >90d stale: 10 config entities @313d, all-channel orders/invoices @96d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 14 active features tracked, ≥3) | YES |
| Catalog Operational Recommendations | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (Q-09 pipeline healthy & consistent: avg ~263/mo, recent month 352, no stall) | NO |

## Notes
- §6 does NOT use a data-confidence header (per shared contract §2).
- Rendered as collapsed `<details class="section-collapse" id="platform">`.
- MIXPANEL_ORDER_TRACKING_GAP = False → Order Submission (273 events) retained in Feature Utilization table.
- Peer benchmark cache files (Q-CI-02, Q-CI-03, Q-CI-03-bench) NOT read/referenced per exclusion.
- Forbidden terms: portal_orders → "All-Channel Orders"; access_sales_portal feature → "Sales App Access"; no "Mixpanel"/"platform"/"ERP".

## Health Dashboard cards (4)
| Indicator | Source | Badge | Note |
|---|---|---|---|
| Core Pipeline | Q-09 avg ~263 imports/mo | ok "Healthy" | consistent monthly imports |
| Data Freshness | Q-08 12 entities >90d stale | danger | config + pricing data 10mo old |
| Feature Adoption | Q-22 14 active features | ok "Strong" | broad feature usage |
| Catalog Sync | Q-08 products/inventory fresh 0d | ok "Current" | core catalog imported today |
