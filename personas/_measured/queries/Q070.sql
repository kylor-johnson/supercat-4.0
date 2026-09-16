-- Q070 | PER-02: user_types, primary_rep_group, and the free-text company_name count
-- Run: 2026-08-31
-- Result: 1,986 user types | primary_rep_group on 142 of them across 42 orgs
--         (register: "142 of 1,983 across 39 orgs" -- CONFIRMED within drift)
--         590 active reps sit on a primary_rep_group user type (readout said 617; window drift)
--         distinct non-blank company_name across ALL org_users = 67,470
--         boolean toggle columns: user_types 12, organizations 35
--           -> the register's "134 toggles / 39 flags / 6 layers" [F10] is a CODE-AUDIT figure and
--              is NOT reproducible from column counts alone. Marked UNVERIFIABLE-FROM-DB.
SELECT (SELECT count(*) FROM user_types) AS user_types,
 (SELECT count(*) FROM user_types WHERE primary_rep_group) AS primary_rep_group_types,
 (SELECT count(DISTINCT organization_id) FROM user_types WHERE primary_rep_group) AS prg_orgs,
 (SELECT count(DISTINCT btrim(company_name)) FROM org_users WHERE btrim(COALESCE(company_name,''))<>'') AS distinct_company_names,
 (SELECT count(*) FROM information_schema.columns WHERE table_schema='public' AND table_name='user_types' AND data_type='boolean') AS user_type_boolean_toggles,
 (SELECT count(*) FROM information_schema.columns WHERE table_schema='public' AND table_name='organizations' AND data_type='boolean') AS org_boolean_toggles,
 (SELECT count(*) FROM org_users ou JOIN user_types ut ON ut.id=ou.user_type_id
   WHERE ut.primary_rep_group AND btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
     AND ou.last_ipad_login_at >= now()-interval '90 days') AS prg_active_reps;
