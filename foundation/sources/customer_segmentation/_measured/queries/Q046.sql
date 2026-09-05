-- Q046 | LINE B (JTBD-053): separating configuration from defect in the completeness counts
-- Run: 2026-08-31
-- Result across 241 orgs holding active items:
--   net_price:  25 orgs never populate it at all -> 91,030 items (CONFIGURATION, not a defect)
--               82 orgs always populate it
--              134 orgs partially populate it   -> 98,441 items (GENUINE missing price)
--   prices_json: 54 orgs never use it
--   images:     179,623 items lack an image, but 26,539 sit in orgs where NO item has one
--              (catalogs that do not use images) -> 153,084 genuine image gaps
-- CORRECTED PROBLEM SIZE FOR JTBD-053:
--   153,084 items missing an image  (not 179,623)
--    98,441 items missing a price   (not 189,471)
--         8 items missing a category, 196 missing a collection -> DROP these checks from the spec
-- The completeness rule must be org-relative, or the view reports ~118,000 false positives.
WITH o AS (SELECT organization_id, count(*) AS items,
    count(*) FILTER (WHERE net_price IS NULL OR net_price=0) AS no_np,
    count(*) FILTER (WHERE prices_json IS NULL OR btrim(prices_json) IN ('','{}','[]','null')) AS no_pj,
    count(*) FILTER (WHERE image_exists IS NOT TRUE) AS no_img
  FROM products WHERE deleted IS NOT TRUE AND hideable IS NOT TRUE GROUP BY 1)
SELECT count(*) AS orgs,
 count(*) FILTER (WHERE no_np = items) AS orgs_never_use_net_price,
 sum(no_np) FILTER (WHERE no_np = items) AS items_in_those_orgs,
 count(*) FILTER (WHERE no_np = 0) AS orgs_always_net_price,
 count(*) FILTER (WHERE no_np > 0 AND no_np < items) AS orgs_partial_net_price,
 sum(no_np) FILTER (WHERE no_np > 0 AND no_np < items) AS genuine_missing_price_items,
 count(*) FILTER (WHERE no_pj = items) AS orgs_never_use_prices_json,
 sum(no_img) AS total_no_image,
 sum(no_img) FILTER (WHERE no_img < items) AS no_image_excl_alldark
FROM o;
