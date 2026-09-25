# Handoff: first real HelpScout inbox test

Written 2026-09-25 for a fresh Claude Code session on this Mac. Read this whole
file before touching anything. It says where the agent lives, what each file
means, what is already known to be wrong, and exactly how to run the test.

Canonical tree: `~/repos/supercat-4.0`, branch `main`. If something seems
missing you are in the wrong directory. `onboarding-models/`, iCloud
`SuperCat 4.0`, and `~/supercat-4.0` are all stale. Never write into them.

## 1. What the HelpScout agent is

Agent 3 is three skills that run as drafts only. There is no HelpScout write
credential anywhere, and v1 never sends even if one appears.

| Skill | Path | Job |
|---|---|---|
| `ecat-correspondence` | `onboarding-agents/3-helpscout/ecat-correspondence/SKILL.md` | The loop and the gate. Reads the inbox mirror, decides which conversations need a reply, categorises each draft SEND-SAFE / DRAFT-AND-PING / ESCALATE. 578 lines, every number in it was measured. |
| `ecat-support-triage` | `onboarding-agents/3-helpscout/ecat-support-triage/SKILL.md` | Diagnoses one ticket. Classify table, identity proof, login URL shapes, reply posture. |
| `ecat-client-email` | `onboarding-agents/3-helpscout/ecat-client-email/SKILL.md` | Writes the reply in Kylor's voice. Tone rules, pre-send checklist, "Best, Kylor". |

`onboarding-agents/3-helpscout/FINDINGS_agent4.md` is the build log from
2026-09-05 (its filename uses the old numbering). Read sections C, D and F.
The relative paths in it are a known nit; ignore them.

`~/.claude/skills/<name>` and `.cursor/skills/<name>` are symlinks into that
folder, so `/ecat-correspondence` loads the live file.

Always-on rules (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`,
`jira-read-only`) are Cursor rules inlined into `CLAUDE.md`. They load
automatically. The delete-on-omission semantics in ground-truth are the most
common root cause in tickets.

## 2. Inputs, verified 2026-09-25

**BigQuery, required.** `onboarding_assessment.helpscout_tickets` via the
`bigquery-admin` MCP. Columns: `ticket_number`, `conversation_id`,
`ticket_subject`, `ticket_status`, `ticket_created_at`,
`ticket_last_updated_at`, `mailbox_id`, `primary_customer_email`,
`primary_customer_domain`, `tags`, `thread_id`, `thread_type`,
`thread_created_at`, `thread_created_by_type`, `thread_author_email`,
`thread_author_domain`, `thread_body`. One row per thread.

State of the mirror at 16:18 UTC today:

| | |
|---|---|
| newest thread | 2026-09-25 16:18 UTC |
| conversations with any thread in the last 14 days | 118 |
| of those, with at least one non-staff, non-note, non-lineitem thread | 92 |

The mirror is a batch about six hours behind. State its age in the run header.
A missing SuperCat reply in the warehouse is not proof nobody replied.

**Postgres, optional.** `supercat-postgres-vpn` MCP, VPN must be up. Without
it the run still drafts, but nothing may be marked SEND-SAFE and every state
claim is `unverified`. Check whether the MCP's tools are listed before
starting; if they are not, say so in the header and proceed.

**Client profiles.** `~/repos/ecat-onboarding-workspace/02_Implementation/<Client Name>/CLIENT_PROFILE.md`.
Seven exist: Dorell, Lib & Co Onboarding, Magic Lite, Pebl, Teracotta,
The CopperSmith, and `_Template`. Use full names, not shortnames.
`eCat_Onboarding/` in this repo is pointers and a registry only.

**Org attribution.** `onboarding_assessment.org_domains` has six rows. A
sender domain does not identify an org (correspondence § 5). Refuse to guess.

## 3. What is already known to be wrong

Fixed today and pushed:

- Triage classify row for missing customers now says a `customers.csv` with an
  `Error` row skipped its deletes.
- `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` now says only bad-code rows are rejected.
- Triage GROUND step now points at the workspace client profiles.

Established and **not yet in the skills**. Apply them by hand while drafting:

3. Acceptance A2 misses an all-zero catalog when no price code has more than
   half the customers, or when `prices_json` is empty. Do not cite A2 as proof
   prices are fine.
4. A product soft-delete does not change `last_modified_at`. A clean Products
   import is proved by an empty error log plus every live row stamped at that
   import. Never date a delete from `last_modified_at`.
5. Never invent a collection's display name from `min(long_description)`.
6. HelpScout in BigQuery lags about six hours. Absence of a reply is not proof.
7. User-group `trade_names_auth` is a second gate. The product file can be right
   and a custom group still hides brands. Admin Products is not filtered that way.
8. A product supplement cannot add new item numbers and does not undelete.

Kylor has candidate rule lists from other chats on another machine. Do not
edit the skills to add 3 through 8 in this session; note where each one would
have changed a draft instead. That evidence decides the edits.

## 4. How to run the test

Work in `onboarding-agents/3-helpscout/runs/2026-09-25/` (gitignored, holds
client email text). One `INBOX_RUN.md` plus one file per draft.

1. Load `/ecat-correspondence`. Confirm the table schema with
   `get_table_schema` before the first query.
2. Window: last 14 days. Follow § 4 exactly: drop `lineitem` and `note` from
   "did we reply" but read the notes; dedupe threads on
   `(thread_author_email, LEFT(body,200))` then conversations on normalised
   subject; derive openness from `thread_author_domain`, never from
   `ticket_status` or `thread_created_by_type` or `primary_customer_domain`.
3. Run the acknowledgment pass. Report the counts:
   classified / attributed / suppressed / needs reply. Expect most of the
   structurally open set to be thank-yous.
4. Cap the needs-reply list at about 12, ranked by age of the oldest unanswered
   client message. Say what was held back.
5. For each needs-reply conversation: attribute the org or mark
   `unattributed`; diagnose with `/ecat-support-triage`; ground in Postgres if
   up; draft with `/ecat-client-email`; categorise and name the clause; record
   "would have sent under the gate: yes/no"; include the deep link
   `https://secure.helpscout.net/conversation/<conversation_id>`.
6. Hunt specifically for these three shapes, because they exercise the
   known-wrong rules. Flag any you find in the header:
   - missing products after a Products upload with an empty error log
   - $0 or blank prices for a whole rep or price level
   - a customer import error that names an account which is still live
7. End with a section `## Where the eight rules mattered`: for each of rules
   3 through 8, the ticket where it changed or would have changed the draft,
   or "did not arise".

Success is not coverage. It is whether Kylor sends the draft unedited. Say
that in the output and ask him to mark each draft sent-as-is / edited / not
sent, so the fortnight comparison in correspondence § 9 has its first data.

## 5. Hard rules for this session

- Nothing is sent. Nothing is written to HelpScout, Jira, Postgres, or Admin.
- No org from a sender domain alone. Free-mail senders are real clients.
- Every quote dated and attributed. Every count names its table. Every
  judgement prefixed `Conclusion:`. No consequence stated as a measurement.
- If the draft says something is fixed or uploaded, re-query it first.
- Internal context (notes, health scores, ticket history, CDN) stays out of
  client copy.
- Do not build a fifth agent, do not propose hosting, do not touch agents 1,
  2 or 4.

## 6. Open items you may hit but must not fix here

- The 2026-09-16 profiler patch (`norm_token`, `field_in_target`) is missing
  from git; its review packet is in `1-ingestion/profiler/`. Agent 1, not yours.
- `ecat-session-prep` drops free-mail domains and excludes only `note`. Agent 4.
- `IMPORT_VS_HELPSCOUT_DRIFT` keys on `thread_created_by_type`. Agent 1.
- The dead local `onboarding-models/` folder still exists; Kylor removes it.
