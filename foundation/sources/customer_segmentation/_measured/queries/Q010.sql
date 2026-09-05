-- Q010 | LINE A: order-writing distribution across the "active" rep base
-- Run: 2026-08-31
-- Result: 4,026 active reps. zero orders in 90d = 2,806 (69.7%). 1-4=514, 5-19=353,
--         20-99=268, 100+=85 (max 424). Total 32,534 orders / $166.9M.
--         The 353 reps writing 20+ produced 28,087 orders (86.3%) and $143.4M (85.9%).
WITH reps AS (
  SELECT id FROM org_users WHERE btrim(COALESCE(customer_number,''))='' AND disabled IS NOT TRUE
    AND last_ipad_login_at >= now()-interval '90 days'),
oo AS (
  SELECT org_user_id, count(*) AS n_orders,
         count(DISTINCT NULLIF(btrim(COALESCE(customer_num,'')),'')) AS n_custs,
         sum(COALESCE(total,0)) AS val
  FROM orders WHERE COALESCE(submit_date,created_at) >= now()-interval '90 days'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1)
SELECT count(*) AS active_reps,
 count(*) FILTER (WHERE COALESCE(oo.n_orders,0)=0) AS n_zero,
 count(*) FILTER (WHERE oo.n_orders BETWEEN 1 AND 4) AS n_1_4,
 count(*) FILTER (WHERE oo.n_orders BETWEEN 5 AND 19) AS n_5_19,
 count(*) FILTER (WHERE oo.n_orders BETWEEN 20 AND 99) AS n_20_99,
 count(*) FILTER (WHERE oo.n_orders >= 100) AS n_100plus,
 max(oo.n_orders) AS max_orders, sum(oo.n_orders) AS total_orders,
 sum(oo.n_orders) FILTER (WHERE oo.n_orders >= 20) AS orders_from_20plus,
 count(*) FILTER (WHERE COALESCE(oo.n_custs,0)=0) AS custs_zero, max(oo.n_custs) AS max_custs,
 round(sum(COALESCE(oo.val,0))) AS total_value,
 round(sum(oo.val) FILTER (WHERE oo.n_orders >= 20)) AS value_from_20plus
FROM reps LEFT JOIN oo ON oo.org_user_id = reps.id;
