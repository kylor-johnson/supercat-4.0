-- Q017 | LINE C: what share of the BUYER population sits behind each gate?
-- Run: 2026-08-31
-- Result: 18,764 active buyers in 37 orgs.
--   at orgs with an invoice feed  : 17,599 (93.8%) in 27 orgs
--   at orgs with Cart on          : 18,057 (96.2%) in 31 orgs
--   at orgs with Sales Portal on  : 17,526 (93.4%) in 25 orgs
-- Org-count framing badly overstates buyer impact of every gap.
WITH ab AS (SELECT organization_id, count(*) AS buyers FROM org_users
  WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
feed AS (SELECT DISTINCT organization_id FROM portal_invoices),
feed12 AS (SELECT DISTINCT organization_id FROM portal_invoices WHERE invoice_date >= (now()-interval '12 months')::date),
cart AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_online_ordering),
sp AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_sales_portal)
SELECT sum(buyers) AS active_buyers, count(*) AS orgs,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM feed)) AS buyers_at_feed_orgs,
 count(*) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM feed)) AS orgs_feed,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM feed12)) AS buyers_live_feed,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM cart)) AS buyers_cart_on,
 count(*) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM cart)) AS orgs_cart,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM sp)) AS buyers_sales_portal_on,
 count(*) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM sp)) AS orgs_sp
FROM ab;
