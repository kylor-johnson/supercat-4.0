-- Scope at T: the ticket's assignee and inbox as they were at the cut time, not today.
-- The view's assignee_id / mailbox_id are current values; a reassigned or moved ticket
-- reports the wrong scope. Assignment and move events are lineitems whose detail is in the
-- raw helpscout.conversation_threads row (assignedTo, action.text).
-- Parameters: conv (INT64), t (TIMESTAMP). Run through the bigquery-admin MCP only.
--
-- Reading the result:
--   assign_events_before_t > 0  -> assignee at T = last_assignee_before_t
--   none before T, some after   -> at T the ticket was unassigned (or held by a
--                                  first assignee HelpScout didn't log): say "unassigned or unknown"
--   none at all                 -> the current assignee held since creation
--   a "moved ... from the <X> inbox" event after T -> the inbox at T was <X>
DECLARE conv INT64 DEFAULT @conv;
DECLARE t TIMESTAMP DEFAULT @t;
WITH cur AS (
  SELECT ANY_VALUE(mailbox_id) mailbox_now, ANY_VALUE(assignee_id) assignee_now, ANY_VALUE(assignee_email) assignee_email_now
  FROM `onboarding_assessment.helpscout_tickets` WHERE conversation_id = conv
),
li AS (
  SELECT v.thread_created_at ts,
         JSON_VALUE(TO_JSON_STRING(r.assignedTo), '$.id')    aid,
         JSON_VALUE(TO_JSON_STRING(r.assignedTo), '$.email') aemail,
         JSON_VALUE(TO_JSON_STRING(r.action), '$.text')      txt
  FROM `onboarding_assessment.helpscout_tickets` v
  JOIN `helpscout.conversation_threads` r ON CAST(r.id AS STRING) = CAST(v.thread_id AS STRING)
  WHERE v.conversation_id = conv AND v.thread_type = 'lineitem'
)
SELECT
  cur.*,
  (SELECT COUNTIF(ts <= t AND txt LIKE '%assigned to%') FROM li) AS assign_events_before_t,
  (SELECT COUNTIF(ts >  t AND txt LIKE '%assigned to%') FROM li) AS assign_events_after_t,
  (SELECT ARRAY_AGG(STRUCT(aid, aemail, ts) ORDER BY ts DESC LIMIT 1)[SAFE_OFFSET(0)]
     FROM li WHERE ts <= t AND txt LIKE '%assigned to%') AS last_assignee_before_t,
  (SELECT ARRAY_AGG(STRUCT(txt, ts) ORDER BY ts)
     FROM li WHERE ts > t AND txt LIKE '%moved this conversation from%') AS moves_after_t
FROM cur;
