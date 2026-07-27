# Stage 2 — Validation Layer (Fathom + HelpScout)

**Purpose:** Add qualitative validation to the quantitative stage results. Detect blockers, sentiment, and recency that DB metrics can't see, and either confirm or challenge the Stage 1 readiness read.
**Runs after:** `Stage_Gated_Data_Collection.md`. Uses each client's `client_domains` from Step 0 of `RUN_PROMPT.md`.
**Next step:** `Output_Format.md`.

**Sources (BigQuery, `user-bigquery-admin`):**
- `onboarding_assessment.fathom_recent_meetings` — call summaries, attendees pre-parsed into `invitee_emails[]` / `external_domains[]`.
- `onboarding_assessment.helpscout_tickets` — tickets denormalized to ticket×thread with `thread_created_at`, `thread_created_by_type`, HTML-stripped `thread_body`, `primary_customer_domain`, `tags`.

> Anti-hallucination rules apply (see `README.md`). Match strictly on the resolved `client_domains` — never on company-name guesses. No quote/summary without a row to back it.
>
> **Verifiable-quote rule (non-negotiable):** every quote in a validation flag must appear **verbatim in the retrieved `summary` / `thread_body` text of that query result** — never reconstructed from memory, prior runs, or surrounding context. If you remember a detail (e.g. "Silvio leaves June 19") but it is not in the returned text, do not quote it; fall back to what the row actually says (e.g. "goal is to be live for the June Dallas market") or drop the claim. Paraphrases must be traceable to the row; the underlying fact can still hold even when a specific quote can't be verified.

---

## STEP 1 — Fathom call validation

Match meetings where any client domain appears in `external_domains` or an invitee email. Run per client (or `IN (...)` the domain list and group later).

```sql
SELECT meeting_title, meeting_start, duration_minutes, fathom_user,
  has_external_invitees, external_domains, invitee_emails,
  section_titles, recording_url, summary
FROM `supercat-data-pipeline.onboarding_assessment.fathom_recent_meetings`
WHERE meeting_start >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND (
    EXISTS (SELECT 1 FROM UNNEST(external_domains) d WHERE d IN ('[CLIENT_DOMAIN_1]','[CLIENT_DOMAIN_2]'))
    OR EXISTS (SELECT 1 FROM UNNEST(invitee_emails) e
               WHERE SPLIT(e,'@')[SAFE_OFFSET(1)] IN ('[CLIENT_DOMAIN_1]','[CLIENT_DOMAIN_2]'))
  )
ORDER BY meeting_start DESC
```

**Read the `summary` (and `section_titles`) for:**

| Signal | Keywords / cues |
|---|---|
| Blocker | "waiting on", "blocked", "stuck", "can't", "issue with", "not working", "haven't", "still need" |
| Data readiness | "export", "ERP", "data file", "products", "pricing", "customer list", "images", "spreadsheet" |
| Timeline | "go live", "launch", "by [date]", "next week", "deadline", "market", "show" |
| Risk / sentiment | "frustrated", "confused", "concerned", "disappointed", "love", "great", "excited", "perfect" |
| Decision / commitment | "approved", "signed off", "decided", "agreed", "will send", "action item" |

Capture, per relevant meeting: date, title, the most load-bearing 1–2 quotes/paraphrases, and the `recording_url`.

## STEP 2 — HelpScout ticket validation

### 2a — Ticket summary per client
```sql
SELECT primary_customer_domain,
  COUNT(DISTINCT conversation_id) AS total_tickets,
  COUNT(DISTINCT IF(ticket_status = 'active', conversation_id, NULL)) AS open_tickets,
  CAST(MAX(thread_created_at) AS STRING) AS last_thread_activity,
  STRING_AGG(DISTINCT tags, ' | ') AS all_tags
FROM `supercat-data-pipeline.onboarding_assessment.helpscout_tickets`
WHERE primary_customer_domain IN ('[CLIENT_DOMAIN_1]','[CLIENT_DOMAIN_2]')
GROUP BY primary_customer_domain
```

### 2b — Recent threads (sentiment + topic)
```sql
SELECT ticket_number, ticket_subject, ticket_status, ticket_created_at,
  thread_created_at, thread_type, thread_created_by_type, thread_author_email,
  tags, thread_body
FROM `supercat-data-pipeline.onboarding_assessment.helpscout_tickets`
WHERE primary_customer_domain IN ('[CLIENT_DOMAIN_1]','[CLIENT_DOMAIN_2]')
  AND thread_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 120 DAY)
ORDER BY thread_created_at DESC
LIMIT 50
```

**Interpretation notes:**
- `thread_created_at` is true last activity — prefer it over `ticket_created_at` for recency.
- `thread_created_by_type = 'customer'` = client wrote in (signal of engagement or friction); `'user'` = SuperCat agent reply.
- Open tickets touching catalog/pricing/import topics that map to a failing stage are **strong confirmation** of that blocker.
- `tags` may carry severity/escalation markers (`l3`/`l4`/`s1`/`s2`); treat those as fire-flags if present.

## STEP 3 — Mandatory "no activity" certification

Before stating a client has **no** Fathom or HelpScout activity, you must have run the matching queries and gotten **zero rows**. "No recent calls" / "no support tickets" is a claim that requires an empty result set, not an assumption. If a domain looks wrong (e.g. the org uses a parent-company domain), note it rather than silently reporting "none."

---

## VALIDATION FLAGS — emit per client

For each client, reconcile Stage 1 against the qualitative signal:

| Flag | Meaning | Trigger |
|---|---|---|
| ✅ CONFIRMED | Calls/tickets corroborate the stage status | Activity aligns with metrics |
| ⚠️ BLOCKER CONFIRMED | A blocker DB metrics implied is verified in a call/ticket | Quote/ticket matches a 🔴/🟡 stage |
| 🔺 HIDDEN BLOCKER | Friction the metrics didn't show | Negative signal with no metric counterpart |
| 🔻 OVER-STATED | Metrics look better than reality | Healthy metrics but client expresses being stuck/frustrated |
| 🔄 STALE | No client touchpoint recently | No Fathom + no inbound HelpScout in window |
| ❓ UNVERIFIED | Couldn't validate | Domain unresolved or zero matchable activity |

### Output of this stage (per client, appended to Stage 1 block)

```markdown
### Validation (Fathom + HelpScout)
**Confidence:** [✅/⚠️/🔺/🔻/🔄/❓] [one-line read]

**Recent Calls:** [N in 90d] — last [date]
- [date] "[title]": [key quote/paraphrase] ([recording_url])

**Support:** [N total tickets, M open] — last activity [date]
- #[ticket_number] "[subject]" [status]: [what it tells us]

**Flags:**
- [⚠️ BLOCKER CONFIRMED: ...] / [🔺 HIDDEN BLOCKER: ...] / [🔄 STALE: ...]

**Net effect on readiness:** [confirms Stage X / drops confidence / no change]
```

---

**Next:** `Output_Format.md` — assemble the full assessment and write the dated file.
