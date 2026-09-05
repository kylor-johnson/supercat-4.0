# Gabby — Generation Notes
**Generated:** March 04, 2026 | **Script:** build_intelligence_deepdive.py
**Data range:** 2026-01-01 → 2026-03-04

---

## 1. Data Sources

| Source | Type | Query / Table | Records |
|--------|------|--------------|---------|
| Revenue KPIs | Postgres `orders` + line-item `extended_price` | org_id=55, dedup by order_number | 2270 orders |
| Feature adoption | BigQuery `mixpanel__events` | `current_organization_shortname = 'gh'` | 35240 events |
| Rep names | Postgres `orders.rep_first_name + rep_last_name` | Per-order attribution | 2270 rows |
| Customer names | Postgres `orders.bill_to_company_name` | Revenue aggregated per customer | 1128 customers |
| Licensed users | Postgres `org_users` + `user_types` | `allow_ipad_logins = true`, `disabled = false` | 114 users |
| Active users | BigQuery `mixpanel__events` `selected_org` | Users with login events in period | 54 active |

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
| Gabby | Flipbook Order | 0 | Gap |

---

## 4. Data Quality Notes

| Observation | Detail |
|-------------|--------|
| Cross-entity reps | 0 users found in 2+ entity CLMs — headline 'active users' (54) includes duplicates |

---

## 5. Output Files

- **Deck:** `EBR_Gabby_2026-03.html`
- **Snapshot:** `Snapshot_Gabby_2026-03.md`
- **Generation Notes:** this file

---

*Generated: March 04, 2026 | Author: build_intelligence_deepdive.py*
