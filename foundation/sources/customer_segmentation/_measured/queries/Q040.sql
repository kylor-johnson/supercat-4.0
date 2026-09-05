-- Q040 | LINE E: per-org structural metrics joined to the stamped v4 segment label
-- Run: 2026-08-31. Segment labels come from _working/data/orgs.csv (109 roster orgs); the
--      structural measures are all live Postgres. Full result -> ../data/Q040.csv (109 rows).
-- Purpose: retest "4 of 31 jobs vary by segment" from the database rather than the roster CSV.
-- Headline: segment explains 1.7%-10.9% of variance in EVERY structural driver (see 06-SEGMENT-VARIATION.md).
-- NOTE: the VALUES list is abbreviated here for readability; the full 109-row list is in ../data/Q040.csv
--       (columns short,segment) and can be pasted back in verbatim to re-run.
WITH seg(short,segment) AS (VALUES
  ('abol','2. Premium Trade Brand'),('afx','3. Mid-Market Multi-Channel') /* ...107 more, see ../data/Q040.csv... */ )
SELECT seg.short, seg.segment, o.id AS org_id,
 (SELECT count(*) FROM price_levels pl WHERE pl.organization_id=o.id AND pl.hidden IS NOT TRUE) AS price_codes,
 (SELECT count(*) FROM products p WHERE p.organization_id=o.id AND p.deleted IS NOT TRUE AND p.hideable IS NOT TRUE) AS active_products,
 (SELECT count(*) FROM taxonomies t WHERE t.organization_id=o.id AND t.type='Collection') AS collections,
 (SELECT count(*) FROM territories t WHERE t.organization_id=o.id) AS territories,
 (SELECT count(*) FROM customers c WHERE c.organization_id=o.id) AS customers,
 (SELECT count(DISTINCT NULLIF(btrim(COALESCE(c.default_price_code,'')),'')) FROM customers c WHERE c.organization_id=o.id) AS cust_price_codes,
 (SELECT count(*) FROM orders od WHERE od.organization_id=o.id AND COALESCE(od.submit_date,od.created_at)>=now()-interval '12 months' AND od.is_marked_deleted IS NOT TRUE AND od.is_submitted IS TRUE) AS orders_12m,
 (SELECT count(*) FROM org_users ou WHERE ou.organization_id=o.id AND btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE AND ou.last_ipad_login_at>=now()-interval '90 days') AS active_reps,
 (SELECT count(*) FROM org_users ou WHERE ou.organization_id=o.id AND btrim(COALESCE(ou.customer_number,''))<>'' AND ou.disabled IS NOT TRUE AND ou.last_ecat_online_login_at>=now()-interval '90 days') AS active_buyers,
 (SELECT count(*) FROM option_groups og WHERE og.organization_id=o.id) AS option_groups,
 EXISTS(SELECT 1 FROM portal_invoices pi WHERE pi.organization_id=o.id) AS has_feed
FROM seg JOIN organizations o ON o.shortname=seg.short
ORDER BY seg.segment, seg.short;
