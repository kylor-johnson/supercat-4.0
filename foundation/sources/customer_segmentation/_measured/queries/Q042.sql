-- Q042 | LINE B (JTBD-044): are the failure reasons classifiable?
-- Run: 2026-08-31
-- Result: '[]' (no error) 17,141 in 16 orgs -- excluded from the real count. Real classes:
--   transport/integration : '401 Unauthorized' 1,003 | '502 Bad Gateway' 52 | timeouts 40
--                           TCP connect failures 28 | 500/503 errors ~28
--   order-content defects : 'Customer number is blank...' 523 | 'customer_num is required' 18
--                           'invalid order_type' 32 | 'Invalid ECAT order' 9
-- Preventable-at-entry class is roughly 580 orders. Most failures are integration transport,
-- not order content -- which is a different fix from the one JTBD-044 describes.
SELECT left(btrim(export_errors),60) AS err_prefix, count(*) AS n, count(DISTINCT organization_id) AS orgs
FROM orders WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months'
  AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE
  AND btrim(COALESCE(export_errors,'')) <> ''
GROUP BY 1 ORDER BY 2 DESC LIMIT 15;
