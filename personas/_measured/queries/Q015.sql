-- Q015 | LINE A: do buyers at large programs behave differently from the long tail?
-- Run: 2026-08-31
-- Result: top6 orgs -- 21,576 orders from 6,769 distinct buyers (54.3% of 12,473 active), avg $1,700
--         tail orgs -- 17,710 orders from 2,309 distinct buyers (36.7% of 6,291 active), avg $1,674
--         BASKET SIZE IS THE SAME. Penetration and frequency are not:
--         large programs = more buyers ordering less often; tail = fewer buyers ordering 2x as often.
WITH b AS (SELECT organization_id, count(*) AS buyers FROM org_users
  WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
rk AS (SELECT organization_id, buyers, row_number() OVER (ORDER BY buyers DESC) AS r FROM b),
o AS (SELECT o.organization_id, o.org_user_id, o.total, ou.customer_number
  FROM orders o JOIN org_users ou ON ou.id=o.org_user_id
  WHERE o.order_source='server' AND COALESCE(o.submit_date,o.created_at) >= now()-interval '12 months'
    AND o.is_marked_deleted IS NOT TRUE AND o.is_submitted IS TRUE)
SELECT CASE WHEN rk.r<=6 THEN 'top6_orgs' WHEN rk.r IS NULL THEN 'no_active_buyers' ELSE 'tail_orgs' END AS grp,
 count(*) AS server_orders,
 count(*) FILTER (WHERE btrim(COALESCE(o.customer_number,''))<>'') AS buyer_placed,
 count(DISTINCT o.org_user_id) FILTER (WHERE btrim(COALESCE(o.customer_number,''))<>'') AS distinct_buyers_ordering,
 round(sum(o.total)) AS value, round(avg(o.total)) AS avg_order
FROM o LEFT JOIN rk ON rk.organization_id=o.organization_id GROUP BY 1 ORDER BY 1;
