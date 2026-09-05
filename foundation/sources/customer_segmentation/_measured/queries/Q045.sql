-- Q045 | LINE B/C (JTBD-053): catalog completeness broken out per org and per CHECK
-- Run: 2026-08-31. Top 20 by failing_any -> ../data/Q045.csv
-- Two things this reveals that the aggregate hides:
--  1. TEST/STAGING ORGS are in the headline number: ctest (9,267), tam-staging (7,870),
--     ahtest (5,630) contribute ~24,700 "failures" that are not real catalogs.
--  2. no_net_price is ALL-OR-NOTHING per org: wac 28,528/28,528, cf 6,847/6,847,
--     kll 6,381/6,381, mh 6,213/6,213, mfc 5,467/5,467. Those orgs simply do not use the
--     net_price field -- they price through price levels. Counting them as "incomplete" is a
--     false positive on an entire catalog. See Q046.
SELECT g.shortname, count(*) AS active_items,
 count(*) FILTER (WHERE p.image_exists IS NOT TRUE) AS no_image,
 count(*) FILTER (WHERE p.net_price IS NULL OR p.net_price=0) AS no_net_price,
 count(*) FILTER (WHERE p.prices_json IS NULL OR btrim(p.prices_json) IN ('','{}','[]','null')) AS no_prices_json,
 count(*) FILTER (WHERE btrim(COALESCE(p.category_code,''))='' AND btrim(COALESCE(p.category_codes,''))='') AS no_category,
 count(*) FILTER (WHERE p.image_exists IS NOT TRUE OR p.net_price IS NULL OR p.net_price=0) AS failing_any
FROM products p JOIN organizations g ON g.id=p.organization_id
WHERE p.deleted IS NOT TRUE AND p.hideable IS NOT TRUE
GROUP BY 1 HAVING count(*) FILTER (WHERE p.image_exists IS NOT TRUE OR p.net_price IS NULL OR p.net_price=0) > 0
ORDER BY failing_any DESC LIMIT 20;
