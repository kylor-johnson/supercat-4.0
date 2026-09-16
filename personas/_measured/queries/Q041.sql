-- Q041 | LINE B (JTBD-044): do order-failure reason codes exist? Register says no.
-- Run: 2026-08-31, trailing 12 months, submitted and not deleted.
-- Result: 178,944 orders / 111 orgs.
--         num_failures > 0 .............. 1,862 orders across 16 orgs (max 17 failures)
--         export_errors non-blank ....... 19,003 -- BUT 17,141 of those are the literal '[]'
--                                          i.e. an empty JSON array = NO error.
--         => genuine populated errors ... 1,862 orders / 16 orgs (matches num_failures exactly)
--         to_export TRUE + is_exported not TRUE (stuck) ... 5,007 orders
--         retry_count > 0 ............... 1,615
-- The register is WRONG that no failure field exists -- but the volume is 1.0% of orders,
-- so the correction does not by itself move JTBD-044 up the roadmap.
SELECT count(*) AS orders_12m, count(DISTINCT organization_id) AS orgs,
 count(*) FILTER (WHERE COALESCE(num_failures,0) > 0) AS with_failures,
 count(DISTINCT organization_id) FILTER (WHERE COALESCE(num_failures,0) > 0) AS orgs_with_failures,
 count(*) FILTER (WHERE btrim(COALESCE(export_errors,'')) <> '') AS with_export_errors_incl_empty_array,
 count(DISTINCT organization_id) FILTER (WHERE btrim(COALESCE(export_errors,'')) <> '') AS orgs_with_export_errors,
 count(*) FILTER (WHERE to_export IS TRUE AND is_exported IS NOT TRUE) AS stuck_unexported,
 count(*) FILTER (WHERE COALESCE(retry_count,0) > 0) AS with_retries, max(num_failures) AS max_failures
FROM orders WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months'
  AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE;
