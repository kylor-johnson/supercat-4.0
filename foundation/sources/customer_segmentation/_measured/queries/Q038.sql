-- Q038 | LINE B (JTBD-012): blast radius of a naive whole-org territory fallback
-- Run: 2026-08-31
-- Result: 3,371 of 4,026 active reps (83.7%) cannot be territory-scoped, across 143 orgs.
--         Under a naive whole-org fallback those reps would collectively be exposed to
--         27,258,121 rep x customer-record pairs.
--         The 655 scopeable reps sit against 4,787,430 such pairs.
-- This is what the mandatory fail-closed rule is buying, expressed as a number.
WITH reps AS (SELECT ou.id, ou.organization_id,
    (ou.territory_codes::text IS NULL OR ou.territory_codes::text IN ('null','[]','{}','""','')) AS no_codes
  FROM org_users ou WHERE btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
    AND ou.last_ipad_login_at >= now()-interval '90 days'),
terr AS (SELECT DISTINCT organization_id FROM territories),
cust AS (SELECT organization_id, count(*) AS n FROM customers GROUP BY 1)
SELECT count(*) AS active_reps,
 count(*) FILTER (WHERE reps.no_codes OR reps.organization_id NOT IN (SELECT organization_id FROM terr)) AS unscopeable,
 sum(COALESCE(cust.n,0)) FILTER (WHERE reps.no_codes OR reps.organization_id NOT IN (SELECT organization_id FROM terr)) AS cust_records_exposed_naive,
 count(DISTINCT reps.organization_id) FILTER (WHERE reps.no_codes OR reps.organization_id NOT IN (SELECT organization_id FROM terr)) AS orgs_affected,
 count(*) FILTER (WHERE NOT reps.no_codes AND reps.organization_id IN (SELECT organization_id FROM terr)) AS scopeable,
 sum(COALESCE(cust.n,0)) FILTER (WHERE NOT reps.no_codes AND reps.organization_id IN (SELECT organization_id FROM terr)) AS cust_records_at_scopeable
FROM reps LEFT JOIN cust ON cust.organization_id=reps.organization_id;
