-- Q006 | Organization-level boolean feature flags actually present in Postgres
-- Run: 2026-08-31. CALIBRATION: enable_rep_activity = 7 of 258 (register said 7 of 257) CONFIRMED.
-- Result: orgs=258 rep_activity=7 sales_data=174 stats=155 enrollment=90 mobile=123
--         contract_pricing=71 import_active=0 sandboxes=0
SELECT count(*) AS orgs_total,
 count(*) FILTER (WHERE enable_rep_activity) AS rep_activity_on,
 count(*) FILTER (WHERE enable_sales_data) AS sales_data_on,
 count(*) FILTER (WHERE stats_enabled) AS stats_on,
 count(*) FILTER (WHERE enrollment_enabled) AS enrollment_on,
 count(*) FILTER (WHERE mobile_enabled) AS mobile_on,
 count(*) FILTER (WHERE contract_pricing_enabled) AS contract_pricing_on,
 count(*) FILTER (WHERE import_active) AS import_active,
 count(*) FILTER (WHERE sandbox_of_id IS NOT NULL) AS sandboxes
FROM organizations;
