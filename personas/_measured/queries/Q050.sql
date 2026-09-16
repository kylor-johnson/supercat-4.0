-- Q050 | LINE F: iPad login activity by quarter, trailing 24 months
-- Run: 2026-08-31. login_events records iPad logins (buyers barely appear: 57-91/qtr).
-- Result (distinct internal user_id per quarter):
--   2025Q1 1,994 | 2025Q2 2,530 | 2025Q3 2,316 | 2025Q4 2,294 | 2026Q1 2,348 | 2026Q2 2,301
-- The internal/rep population is FLAT to slightly declining since 2025Q2.
SELECT date_trunc('quarter', created_at)::date AS qtr,
 count(DISTINCT user_id) FILTER (WHERE btrim(COALESCE(customer_number,''))<>'') AS active_buyers,
 count(DISTINCT user_id) FILTER (WHERE btrim(COALESCE(customer_number,''))='') AS active_internal,
 count(DISTINCT organization_id) AS orgs, count(*) AS login_events
FROM login_events
WHERE created_at >= date_trunc('quarter', now()) - interval '24 months'
  AND created_at < date_trunc('quarter', now())
GROUP BY 1 ORDER BY 1;
