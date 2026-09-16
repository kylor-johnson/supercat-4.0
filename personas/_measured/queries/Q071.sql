-- Q071 | PER-02: scoping the "11,880 free-text company names" decision figure
-- Run: 2026-08-31
-- Result: distinct non-blank company_name among INTERNAL users = 11,799
--           -> reproduces the register's 11,873 / readout's 11,880 within drift. CONFIRMED.
--         among BUYERS = 59,601 (which is why the all-users figure is 67,470)
--         case-insensitive dedup of internal names = 11,612 (casing is NOT the problem)
--         among CURRENTLY ACTIVE reps = 353 distinct names
-- BUT: only 868 of 4,026 active reps (21.6%) have company_name populated AT ALL.
--      Among primary_rep_group active reps, only 125 of 590 (21.2%) have a name, 81 distinct.
-- The register's DECISION is right and its STATED REASON is wrong. The blocker for PER-02 is
-- not that 11,880 names need normalising -- it is that the field is EMPTY for 78% of active
-- reps. Normalisation cannot fix absence. See 02-PERSONA-EVIDENCE.md.
SELECT count(DISTINCT btrim(company_name)) FILTER (WHERE btrim(COALESCE(customer_number,''))='') AS internal_distinct_names,
 count(DISTINCT btrim(company_name)) FILTER (WHERE btrim(COALESCE(customer_number,''))<>'') AS buyer_distinct_names,
 count(DISTINCT btrim(lower(company_name))) FILTER (WHERE btrim(COALESCE(customer_number,''))='') AS internal_distinct_names_ci
FROM org_users WHERE btrim(COALESCE(company_name,''))<>'';

WITH r AS (SELECT ou.id, btrim(COALESCE(ou.company_name,'')) AS cn, COALESCE(ut.primary_rep_group,false) AS prg
  FROM org_users ou LEFT JOIN user_types ut ON ut.id=ou.user_type_id
  WHERE btrim(COALESCE(ou.customer_number,''))='' AND ou.disabled IS NOT TRUE
    AND ou.last_ipad_login_at >= now()-interval '90 days')
SELECT count(*) AS active_reps, count(*) FILTER (WHERE cn<>'') AS with_company_name,
 count(DISTINCT cn) FILTER (WHERE cn<>'') AS distinct_names,
 count(*) FILTER (WHERE prg) AS prg_reps, count(*) FILTER (WHERE prg AND cn<>'') AS prg_with_name,
 count(DISTINCT cn) FILTER (WHERE prg AND cn<>'') AS prg_distinct_names
FROM r;
