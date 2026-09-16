-- Q053 | LINE A: buyer RECORDS vs distinct PEOPLE
-- Run: 2026-08-31
-- Result: 18,764 active buyer records = 12,972 distinct people (1.45 memberships each).
-- Buyer:internal ratio in PEOPLE is 12,972 : 2,141 = 6.1:1, not the 7.5:1 record-based figure.
SELECT count(*) AS active_buyer_rows, count(DISTINCT user_id) AS distinct_people,
 round(count(*)::numeric/NULLIF(count(DISTINCT user_id),0),2) AS memberships_per_person
FROM org_users WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
  AND last_ecat_online_login_at >= now()-interval '90 days';
