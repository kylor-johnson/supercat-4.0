-- Q002 | Cart / catalog / portal flags live on mobile_sites, sites vs orgs
-- Run: 2026-08-31. CALIBRATION: register says "Cart in 58 orgs" -- WRONG.
-- Result: ordering 58 sites / 55 orgs | catalog 95/92 | sales_portal 52/50 | 102 sites / 98 orgs
SELECT
  count(*) FILTER (WHERE enable_online_ordering) AS sites_ordering,
  count(DISTINCT organization_id) FILTER (WHERE enable_online_ordering) AS orgs_ordering,
  count(*) FILTER (WHERE enable_online_catalog) AS sites_catalog,
  count(DISTINCT organization_id) FILTER (WHERE enable_online_catalog) AS orgs_catalog,
  count(*) FILTER (WHERE enable_sales_portal) AS sites_portal,
  count(DISTINCT organization_id) FILTER (WHERE enable_sales_portal) AS orgs_portal,
  count(*) AS sites_total, count(DISTINCT organization_id) AS orgs_with_site
FROM mobile_sites;
