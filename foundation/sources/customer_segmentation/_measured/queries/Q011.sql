-- Q011 | LINE A: do primary_rep_group (agency) reps behave differently?
-- Run: 2026-08-31
-- Result: NOT prg: 3,436 reps, 71.3% zero-order, avg 7.46 orders, $142.2M
--         prg:     590 reps, 60.3% zero-order, avg 11.67 orders, $24.7M
--         Agency reps are measurably MORE productive. PER-02 is behaviourally real.
WITH reps AS (
  SELECT ou.id, COALESCE(ut.primary_rep_group,false) AS prg
  FROM org_users ou LEFT JOIN user_types ut ON ut.id=ou.user_type_id
  WHERE btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
    AND ou.last_ipad_login_at >= now()-interval '90 days'),
oo AS (SELECT org_user_id, count(*) AS n_orders, sum(COALESCE(total,0)) AS val FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '90 days'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1)
SELECT reps.prg, count(*) AS reps,
 count(*) FILTER (WHERE COALESCE(oo.n_orders,0)=0) AS zero_order,
 round(100.0*count(*) FILTER (WHERE COALESCE(oo.n_orders,0)=0)/count(*),1) AS pct_zero,
 round(avg(COALESCE(oo.n_orders,0)),2) AS avg_orders,
 round(sum(COALESCE(oo.val,0))) AS value
FROM reps LEFT JOIN oo ON oo.org_user_id = reps.id GROUP BY 1;
