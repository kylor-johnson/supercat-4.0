-- Q013 | LINE A: buyer concentration by org
-- Run: 2026-08-31. Reproduces readout's "top 6 orgs hold 12,473 of 18,763".
-- Result: 37 orgs hold 18,764 active buyers. top1=3,954 top6=12,473 top10=14,948 tail(31)=6,291
WITH b AS (SELECT organization_id, count(*) AS buyers FROM org_users
  WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
    AND last_ecat_online_login_at >= now()-interval '90 days' GROUP BY 1),
r AS (SELECT organization_id, buyers, row_number() OVER (ORDER BY buyers DESC) AS rk FROM b)
SELECT count(*) AS orgs_with_active_buyers, sum(buyers) AS total_active_buyers,
 sum(buyers) FILTER (WHERE rk<=1) AS top1, sum(buyers) FILTER (WHERE rk<=6) AS top6,
 sum(buyers) FILTER (WHERE rk<=10) AS top10, sum(buyers) FILTER (WHERE rk>6) AS tail,
 max(buyers) AS max_org
FROM r;
