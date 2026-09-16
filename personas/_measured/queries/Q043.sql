-- Q043 | LINE B (JTBD-034): nightly import failure volume
-- Run: 2026-08-31, trailing 30 days. import_events is (id, created_at, organization_id, data).
-- Result: 42,575 events across 107 orgs.
--         6,092 events carry error text, across 71 orgs (66% of importing orgs hit an error in 30d)
--         10,157 carry warning text.
-- Two-thirds of active orgs saw an import error last month and nothing pushes a notification.
SELECT count(*) AS events_30d, count(DISTINCT organization_id) AS orgs,
 count(*) FILTER (WHERE data::text ILIKE '%error%') AS with_error_text,
 count(DISTINCT organization_id) FILTER (WHERE data::text ILIKE '%error%') AS orgs_with_error,
 count(*) FILTER (WHERE data::text ILIKE '%warn%') AS with_warn_text
FROM import_events WHERE created_at >= now()-interval '30 days';
