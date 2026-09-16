-- Q003 | Live active-client universe and coverage of the two client-data gaps
-- Run: 2026-08-31
-- Result: orgs_orders_12m=112 | any invoice feed=56 orgs, live (12m) feed=44 orgs
--         portal_orders=55 | territory master=26 | orgs with active reps=144
--         active universe with any feed=48, with live feed=44 | rep orgs with territory=23
WITH orders_12 AS (
  SELECT DISTINCT organization_id FROM orders
  WHERE COALESCE(submit_date, created_at) >= now()-interval '12 months' AND is_marked_deleted IS NOT TRUE),
inv_orgs AS (SELECT DISTINCT organization_id FROM portal_invoices),
inv_orgs_12 AS (SELECT DISTINCT organization_id FROM portal_invoices WHERE invoice_date >= (now()-interval '12 months')::date),
porder_orgs AS (SELECT DISTINCT organization_id FROM portal_orders),
terr_orgs AS (SELECT DISTINCT organization_id FROM territories),
rep_orgs AS (SELECT DISTINCT organization_id FROM org_users
   WHERE btrim(COALESCE(customer_number,''))='' AND disabled IS NOT TRUE AND last_ipad_login_at >= now()-interval '90 days')
SELECT (SELECT count(*) FROM orders_12) AS orgs_orders_12m,
 (SELECT count(*) FROM inv_orgs) AS orgs_any_invoice,
 (SELECT count(*) FROM inv_orgs_12) AS orgs_invoice_12m,
 (SELECT count(*) FROM porder_orgs) AS orgs_portal_orders,
 (SELECT count(*) FROM terr_orgs) AS orgs_territory_master,
 (SELECT count(*) FROM rep_orgs) AS orgs_active_reps,
 (SELECT count(*) FROM orders_12 JOIN inv_orgs USING(organization_id)) AS active_with_any_feed,
 (SELECT count(*) FROM orders_12 JOIN inv_orgs_12 USING(organization_id)) AS active_with_live_feed,
 (SELECT count(*) FROM rep_orgs JOIN terr_orgs USING(organization_id)) AS repbase_with_territory;
