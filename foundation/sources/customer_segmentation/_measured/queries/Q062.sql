-- Q062 | LINE G (JTBD-086): bounding the "~13,800 additional buyers" claim
-- Run: 2026-08-31. Replaces a point estimate with a measured denominator and a range.
-- Result: 18,764 active buyer records total.
--         17,637 sit at the 24 Portal-PLAN orgs that have any active buyers
--         17,526 sit at orgs with the Portal FLAG on
--         17,522 sit at orgs that are BOTH on the Portal plan AND have an invoice feed
--                (JTBD-086 needs invoiced history, so this is the true ceiling)
-- CEILING for JTBD-086 = 17,522 active buyer records (~12,100 people at 1.45 records/person).
-- FLOOR depends on which 6 orgs already run :advanced_reports -- UNVERIFIABLE-FROM-DB.
--   If those 6 are the 6 largest (12,473 buyers), incremental reach ~= 5,100.
--   If they are 6 small orgs, incremental reach approaches ~17,000.
-- DEFENSIBLE RANGE: ~5,100 to ~17,500 buyer records. The register's 13,800 sits inside it
-- but is not pinned. Naming the 6 orgs collapses the range to a single number.
WITH ab AS (SELECT organization_id, count(*) AS buyers, count(DISTINCT user_id) AS people
  FROM org_users WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
psub AS (SELECT DISTINCT organization_id FROM subscriptions WHERE subscription_plan_id=6),
spf AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_sales_portal),
feed AS (SELECT DISTINCT organization_id FROM portal_invoices)
SELECT sum(buyers) AS all_active_buyers,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM psub)) AS buyers_at_portal_plan_orgs,
 count(*) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM psub)) AS portal_plan_orgs_with_buyers,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM spf)) AS buyers_at_portal_flag_orgs,
 sum(buyers) FILTER (WHERE ab.organization_id IN (SELECT organization_id FROM psub)
                       AND ab.organization_id IN (SELECT organization_id FROM feed)) AS buyers_portal_plan_and_feed
FROM ab;
