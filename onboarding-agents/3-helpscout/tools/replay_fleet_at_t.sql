-- Fleet at T: what the rest of the fleet looked like just before the cut time, so a
-- replay drafter (who has no BigQuery) can see a fleet-wide incident. Every window
-- ends AT T; nothing after T goes in the packet.
-- The builder runs these and saves the results as fleet.md in the ticket folder;
-- packet_assemble.py prints it as section 1b.
-- Measured: a replay blamed one client's browser while fleet sessions had dropped
-- from ~500 to 67-86 per 15 minutes and another client had reported the same thing
-- five minutes earlier. Neither was in the packet.

-- A. BigQuery (bigquery-admin MCP only). Other clients' tickets in the 2 hours before T.
--    Subjects and orgs only: no bodies, no staff replies, nothing after T.
--    Parameters: @t (TIMESTAMP), @domains (the client's own domains, excluded).
SELECT ticket_number, ticket_subject, LOWER(thread_author_domain) AS dom, mailbox_id,
       MIN(thread_created_at) AS first_client_msg
FROM `onboarding_assessment.helpscout_tickets`
WHERE thread_type IN ('customer', 'message')
  AND thread_created_at > TIMESTAMP_SUB(@t, INTERVAL 2 HOUR)
  AND thread_created_at <= @t
  AND LOWER(thread_author_domain) != 'supercatsolutions.com'
  AND LOWER(thread_author_domain) NOT IN UNNEST(@domains)
GROUP BY 1, 2, 3, 4
ORDER BY first_client_msg;

-- B. Postgres (supercat-postgres-vpn MCP, SELECT only). Substitute T as a
--    'YYYY-MM-DD HH:MM:SS' UTC string literal; the MCP validator rejects typed
--    timestamp literals and date_bin, so keep the shapes below.

-- B1. Admin/app sessions, 15-minute buckets, T-3h -> T.
SELECT date_trunc('hour', created_at) + floor(extract(minute FROM created_at) / 15) * interval '15 minutes' AS bucket,
       count(*) AS sessions
FROM authenticated_sessions
WHERE created_at > '<T minus 3h>' AND created_at <= '<T>'
GROUP BY 1 ORDER BY 1;

-- B2. Same metric, hourly, T-24h -> T (the baseline).
SELECT date_trunc('hour', created_at) AS hr, count(*) AS sessions
FROM authenticated_sessions
WHERE created_at > '<T minus 24h>' AND created_at <= '<T>'
GROUP BY 1 ORDER BY 1;

-- B3. iPad sign-ins and eOL logins, hourly, T-24h -> T.
SELECT date_trunc('hour', created_at) AS hr, count(*) AS ipad_logins
FROM login_events
WHERE created_at > '<T minus 24h>' AND created_at <= '<T>'
GROUP BY 1 ORDER BY 1;
SELECT date_trunc('hour', created_at) AS hr, count(*) AS eol_logins
FROM audit_log_entries
WHERE event = 'eol_login_successful' AND created_at > '<T minus 24h>' AND created_at <= '<T>'
GROUP BY 1 ORDER BY 1;

-- B4. Import fatals by org, T-24h -> T (a cluster across orgs is ours, not the client's file).
SELECT organization_id, count(*) AS fatal_events, min(created_at) AS first_at
FROM import_events
WHERE data ILIKE '%fatal%' AND created_at > '<T minus 24h>' AND created_at <= '<T>'
GROUP BY 1 ORDER BY 3;
