-- Q014 | LINE B/F: order channel split. order_source distinguishes iPad from web (buyer) orders.
-- Run: 2026-08-31, trailing 12 months, submitted and not deleted.
-- Result: ipad 139,513 orders / 110 orgs / $732.8M | server(web) 39,422 / 32 orgs / $66.6M
--         Buyer-initiated web = 22.0% of orders but 8.3% of value. Avg $1,689 vs $5,253.
SELECT COALESCE(order_source,'(null)') AS order_source, count(*) AS n,
 count(DISTINCT organization_id) AS orgs, round(sum(COALESCE(total,0))) AS value
FROM orders WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months'
  AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE
GROUP BY 1 ORDER BY 2 DESC;
