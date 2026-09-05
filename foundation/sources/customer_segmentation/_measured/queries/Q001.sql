-- Q001 | Population baseline: internal vs buyer, active on each surface
-- Run: 2026-08-31 against supercatprod (read-only)
-- Result: internal=25,801 buyers=88,037 (86,768 enabled) | ipad_active_reps=4,026
--         eol_active_buyers=18,763 eol_active_internal=2,490 active_both=600
--         admin_records=2,460 orgs_with_active_ipad_reps=144
WITH u AS (
  SELECT ou.*, NULLIF(btrim(ou.customer_number),'') AS cust, (ou.disabled IS NOT TRUE) AS enabled
  FROM org_users ou
)
SELECT
  count(*) FILTER (WHERE cust IS NULL) AS internal_all,
  count(*) FILTER (WHERE cust IS NOT NULL) AS buyers_all,
  count(*) FILTER (WHERE cust IS NOT NULL AND enabled) AS buyers_enabled,
  count(*) FILTER (WHERE cust IS NULL AND enabled AND last_ipad_login_at >= now()-interval '90 days') AS ipad_active_reps,
  count(*) FILTER (WHERE cust IS NOT NULL AND enabled AND last_ecat_online_login_at >= now()-interval '90 days') AS eol_active_buyers,
  count(*) FILTER (WHERE cust IS NULL AND enabled AND last_ecat_online_login_at >= now()-interval '90 days') AS eol_active_internal,
  count(*) FILTER (WHERE enabled AND last_ecat_online_login_at >= now()-interval '90 days' AND last_ipad_login_at >= now()-interval '90 days') AS active_both,
  count(*) FILTER (WHERE is_admin) AS admin_records,
  count(DISTINCT organization_id) FILTER (WHERE cust IS NULL AND enabled AND last_ipad_login_at >= now()-interval '90 days') AS orgs_with_active_ipad_reps
FROM u;
