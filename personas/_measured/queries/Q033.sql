-- Q033 | LINE B (JTBD-084): inventory snapshot age across orgs
-- Run: 2026-08-31. max(inventories.updated_at) per org is an exact snapshot age.
-- Result: 187 orgs hold inventory (687,455 rows). Fresh (<=2d)=68 | 2-7d=4 | 7-30d=6
--         30-365d=26 | OLDER THAN A YEAR=83. Mean age 1,071 days; max 5,530 days.
--         335,571 of 687,455 rows (48.8%) are more than 30 days stale.
WITH inv AS (SELECT organization_id, max(updated_at) AS last_upd, count(*) AS rows FROM inventories GROUP BY 1)
SELECT count(*) AS orgs_with_inventory, sum(rows) AS inventory_rows,
 count(*) FILTER (WHERE last_upd >= now()-interval '2 days') AS fresh_le2d,
 count(*) FILTER (WHERE last_upd >= now()-interval '7 days' AND last_upd < now()-interval '2 days') AS d2_7,
 count(*) FILTER (WHERE last_upd >= now()-interval '30 days' AND last_upd < now()-interval '7 days') AS d7_30,
 count(*) FILTER (WHERE last_upd >= now()-interval '365 days' AND last_upd < now()-interval '30 days') AS d30_365,
 count(*) FILTER (WHERE last_upd < now()-interval '365 days') AS older_than_1y,
 sum(rows) FILTER (WHERE last_upd < now()-interval '30 days') AS rows_stale_30d,
 round(avg(EXTRACT(day FROM now()-last_upd))) AS avg_age_days,
 round(max(EXTRACT(day FROM now()-last_upd))) AS max_age_days
FROM inv;
