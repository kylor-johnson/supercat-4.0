-- Q051 | LINE A/F: rep RECORDS vs distinct PEOPLE
-- Run: 2026-08-31
-- Result: 4,026 active rep records = 2,141 distinct people across 144 orgs.
--         1.88 org memberships per person.
-- Every rep-facing headcount in the register is inflated ~1.9x when read as people.
-- The typical SuperCat rep carries about two manufacturers on the same iPad.
SELECT count(*) AS active_rep_org_user_rows, count(DISTINCT user_id) AS distinct_people,
 round(count(*)::numeric/NULLIF(count(DISTINCT user_id),0),2) AS memberships_per_person,
 count(DISTINCT organization_id) AS orgs
FROM org_users WHERE btrim(COALESCE(customer_number,''))='' AND disabled IS NOT TRUE
  AND last_ipad_login_at >= now()-interval '90 days';
