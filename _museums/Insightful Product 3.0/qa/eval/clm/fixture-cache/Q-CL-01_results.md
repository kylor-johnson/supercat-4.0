# Q-CL-01 — Portal Traffic Health (Clicky daily_metrics, dedup)
- **Query**: Q-CL-01 | **Org**: Crystorama (clm, org_id=64) | **Source**: BigQuery `clicky_analytics.crystorama_clm_ecat_online_daily_metrics` | **Run date**: 2026-06-12
- Dedup guard applied (GROUP BY date, MAX()). 6-month window. `bounce_rate` excluded per policy.

| month | avg_daily_unique_visitors | total_pageviews | avg_session_seconds |
|---|---|---|---|
| 2026-06 | 49.1 | 2,627 | 443.6 |
| 2026-05 | 42.7 | 4,800 | 330.6 |
| 2026-04 | 44.1 | 5,552 | 392.5 |
| 2026-03 | 38.5 | 6,032 | 462.5 |
| 2026-02 | 41.2 | 6,856 | 468.3 |
| 2026-01 | 38.7 | 6,976 | 469.0 |
| 2025-12 | 25.6 | 3,180 | 497.9 |

**Note**: Steady portal traffic (~38–49 avg daily unique visitors), with long avg session times (~5.5–8 min) indicating engaged catalog browsing. Pageviews peaked Jan–Feb 2026 (aligns with order peak). June 2026 is a partial month.
