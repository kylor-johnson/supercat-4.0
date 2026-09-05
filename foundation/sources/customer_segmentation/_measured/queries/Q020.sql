-- Q020 | LINE D: size the invoice-feed gap in commercial terms
-- Run: 2026-08-31. Universe = 112 orgs with any order in trailing 12 months.
-- Result:  HAS FEED (48 orgs): 145,358 orders, $672.5M, 1,947 active reps, 17,599 active buyers,
--                              456,237 customer records, 22 also have a territory master
--          NO FEED  (64 orgs):  33,578 orders, $126.9M, 1,893 active reps,  1,164 active buyers,
--                              211,841 customer records,  2 also have a territory master
-- The feed gap is REP-shaped: 49% of the rep base, but only 6% of buyers and 16% of order value.
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
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
cust AS (SELECT organization_id, count(*) AS n FROM customers GROUP BY 1)
SELECT CASE WHEN univ.organization_id IN (SELECT organization_id FROM feed) THEN 'has_feed' ELSE 'no_feed' END AS grp,
 count(*) AS orgs, sum(COALESCE(ord.n_orders,0)) AS orders_12m,
 round(sum(COALESCE(ord.val,0))) AS order_value_12m,
 sum(COALESCE(reps.n,0)) AS active_reps, sum(COALESCE(buy.n,0)) AS active_buyers,
 sum(COALESCE(cust.n,0)) AS customer_records,
 count(*) FILTER (WHERE univ.organization_id IN (SELECT organization_id FROM terr)) AS also_has_territory
FROM univ LEFT JOIN ord USING(organization_id) LEFT JOIN reps USING(organization_id)
LEFT JOIN buy USING(organization_id) LEFT JOIN cust USING(organization_id)
GROUP BY 1 ORDER BY 1;
