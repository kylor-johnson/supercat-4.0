# Gabby — Generation Notes
**Generated:** March 04, 2026 | **Script:** build_intelligence_deepdive.py
**Data range:** 2025-03-01 → 2026-03-01

---

## 1. Data Sources

| Source | Type | Query / Table | Records |
|--------|------|--------------|---------|
| Revenue KPIs | Postgres `orders` + line-item `extended_price` | org_id=55, dedup by order_number | 13048 orders |
| Feature adoption | BigQuery `mixpanel__events` | `current_organization_shortname = 'gh'` | 188750 events |
| Rep names | Postgres `orders.rep_first_name + rep_last_name` | Per-order attribution | 13048 rows |
| Customer names | Postgres `orders.bill_to_company_name` | Revenue aggregated per customer | 3016 customers |
| Licensed users | Postgres `org_users` + `user_types` | `allow_ipad_logins = true`, `disabled = false` | 54 users |
| Active users | BigQuery `mixpanel__events` `selected_org` | Users with login events in period | 78 active |
| Revenue KPIs | Postgres `orders` + line-item `extended_price` | org_id=69, dedup by order_number | 22526 orders |
| Feature adoption | BigQuery `mixpanel__events` | `current_organization_shortname = 'sc'` | 721011 events |
| Rep names | Postgres `orders.rep_first_name + rep_last_name` | Per-order attribution | 22526 rows |
| Customer names | Postgres `orders.bill_to_company_name` | Revenue aggregated per customer | 13182 customers |
| Licensed users | Postgres `org_users` + `user_types` | `allow_ipad_logins = true`, `disabled = false` | 122 users |
| Active users | BigQuery `mixpanel__events` `selected_org` | Users with login events in period | 172 active |
| Revenue KPIs | Postgres `orders` + line-item `extended_price` | org_id=87, dedup by order_number | 11580 orders |
| Feature adoption | BigQuery `mixpanel__events` | `current_organization_shortname = 'scw'` | 213212 events |
| Rep names | Postgres `orders.rep_first_name + rep_last_name` | Per-order attribution | 11580 rows |
| Customer names | Postgres `orders.bill_to_company_name` | Revenue aggregated per customer | 2367 customers |
| Licensed users | Postgres `org_users` + `user_types` | `allow_ipad_logins = true`, `disabled = false` | 90 users |
| Active users | BigQuery `mixpanel__events` `selected_org` | Users with login events in period | 85 active |
| Revenue KPIs | Postgres `orders` + line-item `extended_price` | org_id=88, dedup by order_number | 4225 orders |
| Feature adoption | BigQuery `mixpanel__events` | `current_organization_shortname = 'sccon'` | 83939 events |
| Rep names | Postgres `orders.rep_first_name + rep_last_name` | Per-order attribution | 4225 rows |
| Customer names | Postgres `orders.bill_to_company_name` | Revenue aggregated per customer | 1094 customers |
| Licensed users | Postgres `org_users` + `user_types` | `allow_ipad_logins = true`, `disabled = false` | 29 users |
| Active users | BigQuery `mixpanel__events` `selected_org` | Users with login events in period | 46 active |

**No CSV files were read during this run.**

---

## 2. Computed Metrics

| Metric | Method | Notes |
|--------|--------|-------|
| Revenue | `SUM(order_items[].extended_price)` from Postgres | Deduped orders; excludes shipping/tax |
| AOV | `Revenue / Order Count` | Full denominator including $0 orders |
| Active Users | Users with `selected_org` events in BigQuery | Unique usernames with login activity |
| Licensed Users | Postgres `org_users` + `user_types.allow_ipad_logins` | Excludes disabled and internal |
| Self-Service % | `order_source = 'server'` / total orders | Postgres `orders.order_source` |
| Feature Totals | `COUNT(*)` per `event_name` from BigQuery | Mapped via BQ_EVENT_MAP |
| Rep Concentration | Top rep `order_submitted` / total entity `order_submitted` | From BigQuery |
| Customer Concentration | Top customer revenue / total entity revenue | From Postgres |
| MoM Growth | `(month2 - month1) / month1 * 100` | Requires 2+ months |
| Cross-Entity Reps | Users in 2+ entity user lists | Matched by full name |

---

## 3. Feature Gaps Detected

| Entity | Feature | Event Count | Status |
|--------|---------|------------|--------|
| SC Contract | Camera Scan | 0 | Gap |
| SC Contract | Submit Order | 0 | Gap |
| SC Contract | Cust. Favorites | 0 | Gap |
| SC Contract | Cust. Backorders | 0 | Gap |
| SC Contract | SmartPicks | 0 | Gap |

---

## 4. Data Quality Notes

| Observation | Detail |
|-------------|--------|
| Cross-entity reps | 0 users found in 2+ entity CLMs — headline 'active users' (381) includes duplicates |
| SC Wholesale self-service | 0% — expected for POS/project workflow |
| SC Contract customer concentration | 6.9% — top customer DIRECT SUPPLY ELDERCARE INT |

---

## 5. Output Files

- **Deck:** `EBR_Gabby_SC_2026-03.html`
- **Snapshot:** `Snapshot_Gabby_SC_2026-03.md`
- **Generation Notes:** this file

---

*Generated: March 04, 2026 | Author: build_intelligence_deepdive.py*
