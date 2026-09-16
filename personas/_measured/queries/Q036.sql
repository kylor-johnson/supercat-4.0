-- Q036 | LINE B (JTBD-054): is taxonomies.created_at a real launch date, or import churn?
-- Run: 2026-08-31. VERDICT: mostly churn -- do NOT substitute it for a launch date.
-- Result: 239 orgs with collections. 149 (62%) have >=50% of their collections created on a SINGLE
--         day; 64 orgs have >=90% on one day. Only 56 orgs spread creation over 20+ distinct days.
--         Mean distinct creation days per org = 14.6.
-- The obvious shortcut for JTBD-054 fails. The register's A1 stands, now with evidence why.
WITH c AS (SELECT organization_id, created_at::date AS d, count(*) AS n
  FROM taxonomies WHERE type='Collection' GROUP BY 1,2),
t AS (SELECT organization_id, sum(n) AS total, max(n) AS biggest_day, count(*) AS distinct_days FROM c GROUP BY 1)
SELECT count(*) AS orgs,
 count(*) FILTER (WHERE biggest_day::numeric/total >= 0.9) AS orgs_90pct_one_day,
 count(*) FILTER (WHERE biggest_day::numeric/total >= 0.5) AS orgs_50pct_one_day,
 count(*) FILTER (WHERE distinct_days >= 20) AS orgs_spread_20plus_days,
 round(avg(distinct_days),1) AS avg_distinct_days
FROM t;
