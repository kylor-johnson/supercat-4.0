-- Q061 | LINE G: entitlement (billed) vs enablement (flag) -- where do they disagree?
-- Run: 2026-08-31
-- Result:
--   Sales Portal : 37 orgs on the Portal plan (35 status='active'); 50 orgs have
--                  mobile_sites.enable_sales_portal = true.
--                  36 paying AND enabled | 1 paying NOT enabled | 14 ENABLED NOT PAYING
--                  36 of 37 paying Portal orgs also have an invoice feed.
--   Cart         : 32 orgs on a Cart plan (4 or 10); 55 orgs have enable_online_ordering = true.
--                  25 orgs run Cart with NO Cart subscription.
-- 25 orgs x $295/mo is roughly $88,500/yr of un-billed Cart entitlement. Commercial, not technical.
WITH portal_sub AS (SELECT DISTINCT organization_id FROM subscriptions WHERE subscription_plan_id=6 AND status='active'),
portal_sub_any AS (SELECT DISTINCT organization_id FROM subscriptions WHERE subscription_plan_id=6),
cart_sub AS (SELECT DISTINCT organization_id FROM subscriptions WHERE subscription_plan_id IN (4,10)),
sp_flag AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_sales_portal),
cart_flag AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_online_ordering),
feed AS (SELECT DISTINCT organization_id FROM portal_invoices)
SELECT (SELECT count(*) FROM portal_sub_any) AS portal_plan_orgs_any_status,
 (SELECT count(*) FROM portal_sub) AS portal_plan_orgs_active,
 (SELECT count(*) FROM sp_flag) AS orgs_sales_portal_flag_on,
 (SELECT count(*) FROM portal_sub_any JOIN sp_flag USING(organization_id)) AS paying_and_enabled,
 (SELECT count(*) FROM portal_sub_any WHERE organization_id NOT IN (SELECT organization_id FROM sp_flag)) AS paying_not_enabled,
 (SELECT count(*) FROM sp_flag WHERE organization_id NOT IN (SELECT organization_id FROM portal_sub_any)) AS enabled_not_paying,
 (SELECT count(*) FROM portal_sub_any WHERE organization_id NOT IN (SELECT organization_id FROM feed)) AS paying_portal_but_no_feed,
 (SELECT count(*) FROM cart_sub) AS cart_plan_orgs,
 (SELECT count(*) FROM cart_flag) AS cart_flag_orgs,
 (SELECT count(*) FROM cart_flag WHERE organization_id NOT IN (SELECT organization_id FROM cart_sub)) AS cart_enabled_not_paying;
