-- Q039 | LINE B (JTBD-052): the real option / CPQ footprint, and whether selections are captured
-- Run: 2026-08-31. Register says "only 16 CPQ orgs".
-- Result: option_groups in 93 orgs (12,541 groups) | options in 92 orgs (46,432 values)
--         matrix_options in 53 orgs (4,865,103 rows) | option_mappings in 7 orgs | option_forms in 10
--         organizations.imports_options = 66
-- Option DATA reaches 92 orgs; the configurator CASCADE reaches 7. "16" sits between two
-- different definitions. Reporting reach for JTBD-052 is ~4x what the register assumes.
SELECT
 (SELECT count(DISTINCT organization_id) FROM option_groups) AS orgs_with_option_groups,
 (SELECT count(*) FROM option_groups) AS option_groups,
 (SELECT count(DISTINCT organization_id) FROM options) AS orgs_with_options,
 (SELECT count(*) FROM options) AS options_rows,
 (SELECT count(DISTINCT organization_id) FROM matrix_options) AS orgs_with_matrix,
 (SELECT count(*) FROM matrix_options) AS matrix_rows,
 (SELECT count(DISTINCT organization_id) FROM option_mappings) AS orgs_with_option_mappings,
 (SELECT count(DISTINCT organization_id) FROM option_forms) AS orgs_with_option_forms,
 (SELECT count(*) FROM organizations WHERE imports_options) AS orgs_imports_options;

-- Are chosen option VALUES recorded per order line? Sampled 30,000 non-empty custom_data blobs:
-- the only key present is 'item'. Option selections are NOT queryable. A13 confirmed necessary.
SELECT k, count(*) AS n FROM (
  SELECT jsonb_object_keys(custom_data) AS k FROM (
    SELECT custom_data FROM portal_order_items
    WHERE custom_data IS NOT NULL AND custom_data::text NOT IN ('{}','null') LIMIT 30000) s
) t GROUP BY 1 ORDER BY 2 DESC LIMIT 25;
