-- Q056 | DATA QUALITY: isolating the 2025Q2 value anomaly
-- Run: 2026-08-31
-- Result: org 'shl' shows 147 orders worth $464,936,100 in 2025Q2 -- of which a SINGLE order
--         is $464,039,002. That one row is the entire quarterly anomaly.
--         Next largest org in the quarter: sccon $58.1M across 2,124 orders (max order $6.7M).
-- Excluding that single order, 24-month recorded order value is ~$1.584B rather than $2.048B.
SELECT o.organization_id, g.shortname, count(*) AS n, round(sum(COALESCE(o.total,0))) AS value,
 round(max(o.total)) AS max_order
FROM orders o JOIN organizations g ON g.id=o.organization_id
WHERE COALESCE(o.submit_date,o.created_at) >= '2025-04-01'
  AND COALESCE(o.submit_date,o.created_at) < '2025-07-01'
  AND o.is_marked_deleted IS NOT TRUE AND o.is_submitted IS TRUE
GROUP BY 1,2 ORDER BY value DESC LIMIT 5;
