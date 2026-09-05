-- Q034 | LINE B/C (JTBD-084): the same staleness, weighted by BUYERS who actually see it
-- Run: 2026-08-31, restricted to Cart-enabled orgs holding inventory.
-- Result: 48 orgs / 17,550 active buyers. 23 orgs fresh(<=2d) but they hold 15,837 buyers (90.2%).
--         20 orgs stale >30d hold only 205 buyers. 11 orgs stale >1y hold 84 buyers.
-- Staleness is severe by ORG COUNT and negligible by BUYER REACH. Same pattern as the feed gap.
WITH inv AS (SELECT organization_id, max(updated_at) AS last_upd FROM inventories GROUP BY 1),
buy AS (SELECT organization_id, count(*) AS buyers FROM org_users
  WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
cart AS (SELECT DISTINCT organization_id FROM mobile_sites WHERE enable_online_ordering)
SELECT count(*) AS orgs_cart_on_with_inventory, sum(buy.buyers) AS active_buyers_covered,
 count(*) FILTER (WHERE inv.last_upd >= now()-interval '2 days') AS orgs_fresh,
 sum(buy.buyers) FILTER (WHERE inv.last_upd >= now()-interval '2 days') AS buyers_seeing_fresh,
 count(*) FILTER (WHERE inv.last_upd < now()-interval '30 days') AS orgs_stale30,
 sum(buy.buyers) FILTER (WHERE inv.last_upd < now()-interval '30 days') AS buyers_seeing_stale30,
 count(*) FILTER (WHERE inv.last_upd < now()-interval '365 days') AS orgs_stale1y,
 sum(buy.buyers) FILTER (WHERE inv.last_upd < now()-interval '365 days') AS buyers_seeing_stale1y
FROM inv JOIN cart ON cart.organization_id=inv.organization_id
LEFT JOIN buy ON buy.organization_id=inv.organization_id;
