-- Q055 | DATA QUALITY (JTBD-031, 061): outliers in orders.total
-- Run: 2026-08-31, trailing 24 months, submitted and not deleted.
-- Result: 357,317 orders totalling $2,048,128,996.
--         15 orders exceed $1M and account for $496,085,960 -- 24.2% of ALL recorded order value.
--         1 order exceeds $100M (see Q056). 11,925 orders (3.3%) have a zero total. No negatives.
-- Any topline computed off orders.total without outlier handling is materially wrong.
-- This is a concrete mechanism behind the register's "eCat runs 0.22-3.10x invoiced truth".
SELECT count(*) FILTER (WHERE total > 1000000) AS over_1m,
 count(*) FILTER (WHERE total > 10000000) AS over_10m,
 count(*) FILTER (WHERE total > 100000000) AS over_100m,
 count(DISTINCT organization_id) FILTER (WHERE total > 1000000) AS orgs_over_1m,
 round(sum(total) FILTER (WHERE total > 1000000)) AS value_over_1m,
 count(*) FILTER (WHERE total < 0) AS negative_total,
 count(*) FILTER (WHERE COALESCE(total,0) = 0) AS zero_total,
 count(*) AS all_orders_24m, round(sum(COALESCE(total,0))) AS all_value_24m
FROM orders WHERE COALESCE(submit_date,created_at) >= now()-interval '24 months'
  AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE;
