-- Q012 | LINE A: the three rep bands confirmed on a SECOND axis (days active, not orders)
-- Run: 2026-08-31. login_events joins users.id via org_users.user_id + organization_id.
-- Result: A zero-order  2,806 reps, avg 12.4 active days/90 (1,324 on 1-5 days; 368 on 30+)
--         B 1-19 orders    867 reps, avg 26.5 active days
--         C 20+ orders     353 reps, avg 54.2 active days (NONE below 6 days)
--         The order-writing split is not an artefact: engagement tracks it independently.
WITH reps AS (
  SELECT ou.id, ou.user_id, ou.organization_id FROM org_users ou
  WHERE btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
    AND ou.last_ipad_login_at >= now()-interval '90 days'),
oo AS (SELECT org_user_id, count(*) AS n_orders FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '90 days'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1),
le AS (SELECT user_id, organization_id, count(DISTINCT created_at::date) AS n_days
  FROM login_events WHERE created_at >= now()-interval '90 days' GROUP BY 1,2)
SELECT CASE WHEN COALESCE(oo.n_orders,0)=0 THEN 'A_zero_orders'
            WHEN oo.n_orders<20 THEN 'B_low_1_19' ELSE 'C_producer_20plus' END AS band,
 count(*) AS reps,
 count(*) FILTER (WHERE le.n_days IS NULL) AS no_login_events_90d,
 round(avg(COALESCE(le.n_days,0)),1) AS avg_active_days_90d,
 count(*) FILTER (WHERE COALESCE(le.n_days,0) >= 30) AS days30plus,
 count(*) FILTER (WHERE COALESCE(le.n_days,0) BETWEEN 1 AND 5) AS days1to5
FROM reps LEFT JOIN oo ON oo.org_user_id=reps.id
LEFT JOIN le ON le.user_id = reps.user_id AND le.organization_id = reps.organization_id
GROUP BY 1 ORDER BY 1;
