-- Q032 | LINE B: size the ERP order-status normalisation problem
-- Run: 2026-08-31
-- Result: 125 distinct status values across 43 orgs over 1,280,046 rows in 12 months.
--         12 are single/double-character codes covering 574,621 rows (44.9%).
--         18 are date-shaped strings (94 rows) -- a field-mapping defect.
-- This is the actual blocker for JTBD-015/043, not the absence of the data.
WITH s AS (SELECT organization_id, COALESCE(status::text,'(null)') AS st, count(*) AS n
  FROM portal_orders WHERE order_date >= (now()-interval '12 months')::date GROUP BY 1,2)
SELECT count(DISTINCT st) AS distinct_status_values, count(DISTINCT organization_id) AS orgs,
 sum(n) AS rows_12m,
 count(DISTINCT st) FILTER (WHERE st ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$') AS date_shaped_statuses,
 sum(n) FILTER (WHERE st ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$') AS rows_with_date_status,
 count(DISTINCT st) FILTER (WHERE length(st)<=2) AS single_char_codes,
 sum(n) FILTER (WHERE length(st)<=2) AS rows_single_char
FROM s;
