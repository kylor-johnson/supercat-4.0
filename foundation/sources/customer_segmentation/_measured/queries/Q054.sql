-- Q054 | LINE F: order volume and channel mix by quarter, trailing 24 months
-- Run: 2026-08-31
-- Result: orders 42,454 (2024Q3) -> 48,387 (2026Q2), +14.0%
--         buyer web orders 8,441 -> 10,907, +29.2%   <-- fastest-growing channel
--         iPad orders     34,013 -> 37,480, +10.2%
--         web share of orders 19.9% -> 22.5% | distinct writers 4,336 -> 5,528 (+27.5%)
--         orgs 85 -> 94
-- WARNING: the 2025Q2 value ($705.6M) is a single bad order, not growth. See Q055/Q056.
SELECT date_trunc('quarter', COALESCE(submit_date,created_at))::date AS qtr, count(*) AS orders,
 count(*) FILTER (WHERE order_source='server') AS buyer_web_orders,
 count(*) FILTER (WHERE order_source='ipad') AS ipad_orders,
 count(DISTINCT organization_id) AS orgs, count(DISTINCT org_user_id) AS distinct_writers,
 round(sum(COALESCE(total,0))) AS value
FROM orders WHERE COALESCE(submit_date,created_at) >= date_trunc('quarter', now()) - interval '24 months'
  AND COALESCE(submit_date,created_at) < date_trunc('quarter', now())
  AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE
GROUP BY 1 ORDER BY 1;
