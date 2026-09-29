-- Replay packet, threads cut at T. Parameters: @conv (INT64), @t (TIMESTAMP), @domains (ARRAY<STRING>)
WITH base AS (
  SELECT h.*
  FROM `onboarding_assessment.helpscout_tickets` h
  WHERE h.thread_type NOT IN ('lineitem')
    AND h.thread_created_at <= @t
    AND (h.conversation_id = @conv
         OR (LOWER(h.thread_author_domain) IN UNNEST(@domains)
             AND h.thread_created_at >= TIMESTAMP_SUB(@t, INTERVAL 30 DAY)))
),
convs AS (SELECT DISTINCT conversation_id FROM base),
all_threads AS (
  SELECT h.* FROM `onboarding_assessment.helpscout_tickets` h JOIN convs USING (conversation_id)
  WHERE h.thread_type NOT IN ('lineitem') AND h.thread_created_at <= @t
),
dd AS (
  SELECT * EXCEPT(rn) FROM (
    SELECT *, ROW_NUMBER() OVER (
      -- Dedupe inside one conversation group (same subject minus Re:/Fw:), not across the
      -- client's conversations: a client who re-sends an ask on a new ticket keeps both.
      PARTITION BY REGEXP_REPLACE(LOWER(ticket_subject), r'^\s*((re|fw|fwd)\s*:\s*)+', ''),
                   LOWER(thread_author_email), LEFT(LOWER(REGEXP_REPLACE(thread_body, r'\s+', ' ')), 200)
      -- A twin capture (same email in both inboxes) keeps THIS ticket's copy, not the lower
      -- conversation_id; otherwise the T message leaves the "← THIS TICKET" section
      -- (measured: 8 of 20 packets in one batch).
      ORDER BY IF(conversation_id = @conv, 0, 1), thread_created_at, conversation_id) rn
    FROM all_threads) WHERE rn = 1
)
SELECT conversation_id, ticket_number, ticket_subject, mailbox_id, assignee_id, assignee_email, tags,
       thread_type, thread_created_at, thread_author_email, LOWER(thread_author_domain) AS dom,
       thread_attachment_count, thread_body
FROM dd ORDER BY conversation_id, thread_created_at;

-- Leak check: anything on these conversations after T (metadata only, never shown to the agent)
-- SELECT conversation_id, thread_type, thread_created_at, LOWER(thread_author_domain) FROM `onboarding_assessment.helpscout_tickets`
-- WHERE conversation_id IN (SELECT conversation_id FROM convs) AND thread_created_at > @t ORDER BY thread_created_at;
