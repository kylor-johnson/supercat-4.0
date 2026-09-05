-- Q004 | Rep territory scopeability. territory_codes is json: cast ::text to test emptiness.
-- Run: 2026-08-31
-- Result: active_reps=4,026 | no codes=938 | with codes=3,088 | scopeable=655 in 20 orgs
WITH reps AS (
  SELECT id, organization_id, territory_codes::text AS tc FROM org_users
  WHERE btrim(COALESCE(customer_number,''))='' AND disabled IS NOT TRUE
    AND last_ipad_login_at >= now()-interval '90 days'),
r2 AS (SELECT id, organization_id, (tc IS NULL OR tc IN ('null','[]','{}','""','')) AS no_codes FROM reps),
terr AS (SELECT DISTINCT organization_id FROM territories)
SELECT count(*) AS active_reps,
 count(*) FILTER (WHERE no_codes) AS reps_no_codes,
 count(*) FILTER (WHERE NOT no_codes) AS reps_with_codes,
 count(*) FILTER (WHERE NOT no_codes AND organization_id IN (SELECT organization_id FROM terr)) AS scopeable,
 count(DISTINCT organization_id) FILTER (WHERE NOT no_codes AND organization_id IN (SELECT organization_id FROM terr)) AS scopeable_orgs
FROM r2;
