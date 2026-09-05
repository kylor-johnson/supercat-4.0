-- Q007 | rep_activities access probe
-- Run: 2026-08-31
-- Result: ERROR "permission denied for table rep_activities". Table exists (pg_class est. 635 rows)
--         but is not readable by this role, and is absent from information_schema.columns for us.
--         The enable_rep_activity pilot's contents are therefore UNVERIFIABLE-FROM-DB at this grant.
SELECT count(*) AS rep_activity_rows, count(DISTINCT organization_id) AS orgs FROM rep_activities;
