-- Q022 | LINE D: how concentrated is the invoice-feed gap?
-- Run: 2026-08-31
-- Result: 64 no-feed orgs hold $126.9M of order value.
--         Top 6 = $81.4M (64.1%) | Top 10 = $94.7M (74.6%) | Top 20 = $112.7M (88.8%)
--         Ten conversations recover three-quarters of the gap.
WITH univ AS (SELECT DISTINCT organization_id FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months' AND is_marked_deleted IS NOT TRUE),
feed AS (SELECT DISTINCT organization_id FROM portal_invoices),
ord AS (SELECT organization_id, sum(COALESCE(total,0)) AS val FROM orders
  WHERE COALESCE(submit_date,created_at) >= now()-interval '12 months'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1),
nf AS (SELECT univ.organization_id, COALESCE(ord.val,0) AS val,
   row_number() OVER (ORDER BY COALESCE(ord.val,0) DESC) AS r
   FROM univ LEFT JOIN ord USING(organization_id)
   WHERE univ.organization_id NOT IN (SELECT organization_id FROM feed))
SELECT count(*) AS no_feed_orgs, round(sum(val)) AS total_val,
 round(sum(val) FILTER (WHERE r<=6)) AS top6_val, round(sum(val) FILTER (WHERE r<=10)) AS top10_val,
 round(sum(val) FILTER (WHERE r<=20)) AS top20_val,
 round(100.0*sum(val) FILTER (WHERE r<=6)/NULLIF(sum(val),0),1) AS pct_top6,
 round(100.0*sum(val) FILTER (WHERE r<=10)/NULLIF(sum(val),0),1) AS pct_top10
FROM nf;
