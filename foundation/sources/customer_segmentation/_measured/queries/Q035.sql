-- Q035 | LINE B (JTBD-054): is there ANY launch date? products has no created_at/updated_at at all.
-- Run: 2026-08-31. Confirms the register's A1 ("one nullable column") is genuinely needed.
-- Result: products columns matching created_at/updated_at = NONE. Only 'id'.
--         taxonomies (Collection) DOES have created_at -- 65,910 collections, 19,197 created in the
--         last 12 months across 119 orgs. That is a candidate collection-level launch date.
SELECT column_name FROM information_schema.columns
WHERE table_schema='public' AND table_name='products' AND column_name IN ('created_at','updated_at','id');

SELECT count(*) FILTER (WHERE type='Collection') AS collections_total,
 count(*) FILTER (WHERE type='Collection' AND created_at >= now()-interval '12 months') AS new_12m,
 count(DISTINCT organization_id) FILTER (WHERE type='Collection' AND created_at >= now()-interval '12 months') AS orgs_with_new_collection_12m,
 count(*) FILTER (WHERE type='Collection' AND created_at >= now()-interval '6 months') AS new_6m,
 count(DISTINCT organization_id) FILTER (WHERE type='Collection') AS orgs_with_collections,
 min(created_at) FILTER (WHERE type='Collection') AS earliest,
 max(created_at) FILTER (WHERE type='Collection') AS latest
FROM taxonomies;
