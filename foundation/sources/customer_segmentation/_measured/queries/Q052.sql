-- Q052 | LINE A/C: the rep-component launch population expressed in PEOPLE
-- Run: 2026-08-31
-- Result: 2,141 people. 559 are scopeable at >=1 of their orgs; 1,808 are unscopeable at >=1.
--         559 + 1,808 = 2,367 > 2,141, so 226 people are scopeable at one manufacturer and
--         NOT at another -- the same human sees their book at org A and nothing at org B.
-- The launch population for the rep component is 559 PEOPLE, not 655/664 records.
WITH reps AS (SELECT ou.user_id, ou.organization_id,
    (ou.territory_codes::text IS NULL OR ou.territory_codes::text IN ('null','[]','{}','""','')) AS no_codes
  FROM org_users ou WHERE btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
    AND ou.last_ipad_login_at >= now()-interval '90 days'),
terr AS (SELECT DISTINCT organization_id FROM territories)
SELECT count(DISTINCT user_id) AS people,
 count(DISTINCT user_id) FILTER (WHERE NOT no_codes AND organization_id IN (SELECT organization_id FROM terr)) AS people_scopeable_somewhere,
 count(DISTINCT user_id) FILTER (WHERE no_codes OR organization_id NOT IN (SELECT organization_id FROM terr)) AS people_unscopeable_somewhere,
 count(*) FILTER (WHERE NOT no_codes AND organization_id IN (SELECT organization_id FROM terr)) AS scopeable_rows
FROM reps;
