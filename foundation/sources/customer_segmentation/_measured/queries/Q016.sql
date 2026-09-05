-- Q016 | LINE A: buyer-level ordering distribution and ship-to multiplicity
-- Run: 2026-08-31
-- Result: 18,764 active buyers. 11,868 (63.2%) placed NO order in 12 months.
--         1 order=2,769 | 2-5=2,873 | 6-20=1,013 | >20=241 (max 835)
--         The 241 heaviest buyers drove $23.6M of $59.9M (39.4%).
--         Ship-to: of 3,987 buyers with a resolvable ship_to_code, only 75 (1.9%) use more than one.
WITH ab AS (SELECT id FROM org_users WHERE btrim(COALESCE(customer_number,''))<>'' AND disabled IS NOT TRUE
  AND last_ecat_online_login_at >= now()-interval '90 days'),
o AS (SELECT org_user_id, count(*) AS n, sum(COALESCE(total,0)) AS v,
      count(DISTINCT NULLIF(btrim(COALESCE(ship_to_code,'')),'')) AS shipto
  FROM orders WHERE order_source='server'
    AND COALESCE(submit_date,created_at) >= now()-interval '12 months'
    AND is_marked_deleted IS NOT TRUE AND is_submitted IS TRUE GROUP BY 1)
SELECT count(*) AS active_buyers,
 count(*) FILTER (WHERE o.n IS NULL) AS never_ordered_12m,
 count(*) FILTER (WHERE o.n=1) AS one_order,
 count(*) FILTER (WHERE o.n BETWEEN 2 AND 5) AS o2_5,
 count(*) FILTER (WHERE o.n BETWEEN 6 AND 20) AS o6_20,
 count(*) FILTER (WHERE o.n > 20) AS o20plus, max(o.n) AS max_orders,
 round(sum(o.v) FILTER (WHERE o.n > 20)) AS value_from_20plus,
 round(sum(COALESCE(o.v,0))) AS total_value,
 count(*) FILTER (WHERE o.shipto > 1) AS multi_shipto,
 count(*) FILTER (WHERE o.shipto = 1) AS single_shipto
FROM ab LEFT JOIN o ON o.org_user_id = ab.id;
