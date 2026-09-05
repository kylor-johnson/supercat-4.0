-- Q005 | Catalog completeness, all active items (deleted IS NOT TRUE AND hideable IS NOT TRUE)
-- Run: 2026-08-31. Reproduces roadmap's 179,577/938,394 within drift.
-- Result: 938,893 active items / 241 orgs | no_image=179,623 | no_net_price=189,471
--         no_prices_json=210,652 | no_category=8 | no_collection=196 | new_item flag true=69,659
SELECT count(*) AS active_items, count(DISTINCT organization_id) AS orgs,
 count(*) FILTER (WHERE image_exists IS NOT TRUE) AS no_image,
 count(*) FILTER (WHERE net_price IS NULL OR net_price=0) AS no_net_price,
 count(*) FILTER (WHERE prices_json IS NULL OR btrim(prices_json) IN ('','{}','[]','null')) AS no_prices_json,
 count(*) FILTER (WHERE btrim(COALESCE(category_code,''))='' AND btrim(COALESCE(category_codes,''))='') AS no_category,
 count(*) FILTER (WHERE btrim(COALESCE(collection_code,''))='' AND btrim(COALESCE(collection_codes,''))='') AS no_collection,
 count(*) FILTER (WHERE new_item) AS new_item_true
FROM products WHERE deleted IS NOT TRUE AND hideable IS NOT TRUE;
