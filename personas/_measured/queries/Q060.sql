-- Q060 | LINE G: does anything in Postgres encode plan-level entitlement? YES.
-- Run: 2026-08-31. The register/readout assert feature gates live only in application YAML.
--      That is true of FINE-GRAINED gates. It is FALSE of plan-level commercial entitlement.
-- Result -- subscription_plans with live subscription counts (orgs):
--   1  eCat iPad                          $725   97 orgs
--   3  eCat (iPad) Service with CPQ       $795   17 orgs
--   4  eCat Online - B2B Cart             $295   31 orgs
--   5  eCat Online - Closed Site          $100   47 orgs
--   6  eCat Online - Portal               $395   37 orgs  <-- "Sales Portal service with
--                                                              enhanced sales reporting"
--   7  eCat Online Service                $295   53 orgs
--   9  eCat (iPad) CPQ                    $195    3 orgs
--  12  eCat (iPad) Product Configuration  $195    1 org
--  16  T1 - Catalog Essentials            $749    2 orgs
--  17  T2 - Commerce Professional        $1295    2 orgs
--  18  T3 - Commerce Enterprise          $2295    1 org
-- CPQ entitlement (plans 3+9+12) = 21 orgs; register's "16 CPQ orgs" is close on plan 3 alone (17).
-- T1/T2/T3 exist but only 5 orgs are on the new tiering.
SELECT sp.id, sp.name, sp.description, sp.base_price, sp.user_limit, sp.per_user_price, sp.active,
 (SELECT count(*) FROM subscriptions s WHERE s.subscription_plan_id=sp.id) AS subs,
 (SELECT count(DISTINCT s.organization_id) FROM subscriptions s WHERE s.subscription_plan_id=sp.id) AS orgs
FROM subscription_plans sp ORDER BY sp.id;
