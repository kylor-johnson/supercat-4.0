-- Q021 | LINE D: the invoice-feed TARGET LIST -- largest no-feed clients by order value
-- Run: 2026-08-31. Full result set saved to ../data/Q021.csv (top 25).
-- Result (top 6): uhc $21.8M | wag $16.2M | mpc $15.6M | kii $13.6M | wac $7.3M | ah $6.8M
WITH univ AS (SELECT DISTINCT organization_id FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months' AND is_marked_deleted IS NOT TRUE),
feed AS (SELECT DISTINCT organization_id FROM portal_invoices),
terr AS (SELECT DISTINCT organization_id FROM territories),
ord AS (SELECT organization_id, count(*) AS n_orders, sum(COALESCE(total,0)) AS val FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1),
reps AS (SELECT organization_id, count(*) AS n FROM org_users
  WHERE btrim(COALESCE(customer_number,''))='' AND disabled IS NOT TRUE
    AND last_ipad_login_at >= now()-interval '90 days' GROUP BY 1),
buy AS (SELECT organization_id, count(*) AS n FROM org_users
  WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1)
SELECT g.shortname, g.name, COALESCE(ord.n_orders,0) AS orders_12m,
 round(COALESCE(ord.val,0)) AS order_value_12m, COALESCE(reps.n,0) AS active_reps,
 COALESCE(buy.n,0) AS active_buyers,
 (univ.organization_id IN (SELECT organization_id FROM terr)) AS has_territory_master
FROM univ JOIN organizations g ON g.id=univ.organization_id
LEFT JOIN ord USING(organization_id) LEFT JOIN reps USING(organization_id) LEFT JOIN buy USING(organization_id)
WHERE univ.organization_id NOT IN (SELECT organization_id FROM feed)
ORDER BY order_value_12m DESC LIMIT 25;
