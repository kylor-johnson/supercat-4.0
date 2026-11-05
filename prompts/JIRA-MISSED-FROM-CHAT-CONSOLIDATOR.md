# Jira missed-from-chat consolidator

> **Last updated**: 2026-10-13
> **Canonical path**: `prompts/JIRA-MISSED-FROM-CHAT-CONSOLIDATOR.md`
> **Operator**: Kylor Johnson

## How to invoke

In a fresh agent session, on any device, in Cursor or Claude Code:

```
Read prompts/JIRA-MISSED-FROM-CHAT-CONSOLIDATOR.md and execute it.
Swarm outputs: <paste, @-mention, or say "find them">
```

That is the whole brief. The file below is the prompt. Do not wait for more instructions. Do not re-prompt Kylor to confirm scope.

This file is meant to be run in **several places at once** (Cursor + Claude Code, Mac Mini + MacBook). Each run writes its **own** output file. Do not overwrite another run's file.

---

# CONSOLIDATOR — missed Jira tickets from onboarding / support chat history

You are the **independent consolidator** for a multi-device agent swarm.

Four surfaces already ran the same hunt in parallel:

| Surface | Device |
|---|---|
| Cursor | Mac Mini |
| Cursor | MacBook |
| Claude Code | Mac Mini |
| Claude Code | MacBook |

Each swarm’s job was: review recent chat history and produce a POV on **onboarding and support tickets I received and forgot to log in Jira**.

Your job is **not** to re-scan all chat history. Your job is to **inventory every swarm output you can reach, reconcile them, independently verify the Jira half, and hand me one ranked summary I can act on**.

Finish the whole job in one pass. Do not stop to ask whether to continue. Ask at most one question, and only if a missing input would make the rest of the work unsafe or wasted.

---

## 0. Hard rules (non-negotiable)

1. **Jira is read-only.** Do not create, edit, comment, transition, link, or worklog. Draft tickets in chat / a PM markdown file only. Kylor will file them himself.
2. **Do not send email, HelpScout replies, or Slack.** Internal summary only.
3. **Swarm outputs are hypotheses, not findings.** A claim of “no ticket exists” is false until *you* have run a Phase 1 Jira duplicate search. A claim of “this needs a ticket” is false until you have classified it as engineering work (not ops).
4. **Suppress rather than guess.** If evidence is too thin, put it in INSUFFICIENT EVIDENCE. Do not promote a maybe into a file-this.
5. **Do not invent org shortnames, HelpScout IDs, or Jira keys.** If a swarm omitted them, try to recover them from the cited source. If you cannot, leave them blank and downgrade confidence.
6. **Consult these skills before you conclude anything:**
   - `.cursor/skills/supercat-jira/SKILL.md` — Phase 1 duplicate search is a gate
   - `.cursor/skills/supercat-data-routing/SKILL.md` — HelpScout lives in BigQuery (`helpscout.conversations` / `helpscout.conversation_threads`), not Postgres
   - `.cursor/skills/ecat-support-triage/SKILL.md` — what is support/ops vs engineering
   - `.cursor/rules/jira-read-only.mdc` — no Jira writes, no hygiene comments
   - `.cursor/skills/truth-discipline/SKILL.md` — no bare counts; label completeness
   - `.cursor/skills/finish-the-job/SKILL.md` — do the whole pass
7. **Cloud ID for Jira:** `3aea3e61-c30d-422a-9b0e-b5bab9b4c92a` (`supercatsolutions.atlassian.net`).
8. **HelpScout in BigQuery is a once-daily batch**, not live. If you use it to recover a conversation ID, stamp the lag. Do not treat a missing BQ row as “no ticket existed.”
9. **Do not create a canvas.** Results go in chat + one markdown file.

---

## 1. Inventory first (do this before judging anyone’s POV)

Find **every** swarm output you can reach on this machine and anything Kylor pasted / attached / @-mentioned in this chat.

Search, in this order:

1. **This conversation** — pasted reports, attached files, @-mentioned paths.
2. **Obvious drop locations on this machine**
   - `~/Downloads/`
   - `~/Desktop/`
   - `~/repos/supercat-4.0/PM/` (any new `*jira*`, `*missed*`, `*unlogged*`, `*swarm*`, `*pov*` files from the last few days)
   - `~/repos/supercat-4.0/scratch/` if it exists
   - anything left in the working tree that is clearly a swarm write-up
3. **Cursor transcripts on this machine**
   - `~/.cursor/projects/Users-kylorjohnson-repos-supercat-4-0/agent-transcripts/`
   - sibling `~/.cursor/projects/*supercat*/agent-transcripts/`
   - look for recent transcripts whose first user turn is about forgotten / missing / unlogged Jira tickets, chat history, onboarding, or support
4. **Claude Code transcripts on this machine**
   - `~/.claude/projects/`
   - any project-local `.claude/` conversation dumps
5. **iCloud / other-device sync, if present**
   - do **not** open the iCloud `SuperCat 4.0` working-tree trap for product work
   - you **may** read transcript / export folders if that is where the other device dropped swarm output

For each source you find, record a provenance row **before** you merge anything:

| # | Surface | Device (if known) | Path or chat id | Date written | Window they claimed to cover | Item count they claimed | Notes (complete / truncated / still running) |

**Coverage rule.** You are on one device. The other device’s local transcripts may be invisible. Proceed with what you have. In the summary, state coverage as `N of 4 surfaces found`, name the missing ones, and do not pretend the union is complete.

If Kylor already pasted the swarm write-ups, those are the primary corpus. Transcript hunting is only to recover outputs he did not paste.

---

## 2. What you are consolidating

Each swarm item is a candidate of the form:

> In recent onboarding or support chat history, client X raised problem Y, and it looks like we never logged a Jira ticket.

You are answering one question:

**Which of those candidates are real, distinct, engineering-trackable misses — and which are noise, ops, or already in Jira?**

Out of scope (drop or file under NOT A MISS):

- Password resets, new users, territory/user-group assignment, invitation emails
- Import / FTP / image / `customers.csv` / `products.csv` build work
- “Client asked a how-to and we answered from KB / Admin”
- Sales / pricing-migration / CEO-system / Insightful work unless it is a product defect a client hit
- Anything the swarm flagged only because the words “bug” or “ticket” appeared
- Duplicate restatements of a ticket that already exists (`SERV` / `ECAT` / `EBR` / `CSP`)

In scope (keep and verify):

- A diagnosed product defect or missing capability a client hit
- A client feature request that was never scoped into EBR
- A workaround we told a client to live with, with no engineering record
- The same defect hitting multiple orgs (that is one ticket, many org citations)

---

## 3. Identity key — this is how you dedupe

Do **not** dedupe on wording. Four swarms will describe the same miss four ways.

Build one row per distinct issue using this key, in order of strength:

1. HelpScout conversation ID or `#number` (best)
2. Org shortname + surface + engineering-shaped defect (good)
3. Client name + date + symptom (weak — only if 1 and 2 are missing)

Surface vocabulary (pick one): `iPad` · `eOL` · `Sales Portal` · `Admin` · `Importer` · `Enrollment` · `Sandbox` · `unknown`

If two rows share a HelpScout ID, they are the same issue even if the swarms named different bugs. If they share org + surface + the same mechanism, they are the same issue. If they only share a vague symptom (“inventory wrong”), they are **not** the same until you prove it.

When swarms disagree (one says file, one says already tracked, one says ops), **do not average**. Re-verify and pick a verdict. Record the dissent in a one-line note.

---

## 4. Independent Jira verification (mandatory, per surviving candidate)

Read `.cursor/skills/supercat-jira/SKILL.md` and run Phase 1 for every candidate that is still standing after classification.

`text ~` is fuzzy word matching, not semantic. One query proves nothing. For each candidate:

**Pass 1 — summary scan, per relevant project**

```
project = SERV AND (summary ~ "<domain noun>" OR summary ~ "<surface>") ORDER BY created DESC
```

Repeat for `ECAT` and `EBR` when the surface could live there. Include `CSP` only if the swarm claimed a client-engagement umbrella.

**Pass 2 — full text, 4–6 phrasings** covering the client’s words *and* the engineering words.

**Pass 3 — open near misses** with `getJiraIssue` and read the description. Titles lie. The useful hit is often the ticket that *created* the behavior now being complained about.

Search mechanics:

- Narrow `fields`: `["key","summary","status","resolution","created"]`
- Never request `description` in a multi-row search
- If JQL overflows to a file, `jq` it; do not read the dump linearly

Status vocabulary you must not flatten:

`To Do` · `In Progress` · `Ready to Accept` · `Done` · `Closed` · `Hold` · `Back Burner` · `Triaging` · `Submitted` · `Pending SuperCat` · `Already Implemented` · **`Archieved`** (sic — match that spelling)

Interpretation:

- `Done` / `Closed` / `Already Implemented` = tracked and treated as solved. Still say so. A new ticket is only justified if the live complaint is a **regression** or a **different** defect.
- `Archieved` / `Back Burner` = dropped, not fixed. Do **not** say a fix is coming. Flag as “dropped; client still hitting it” if the chat evidence is recent.
- `Submitted` / `Triaging` on EBR = raw ask already captured. Not a miss.

Never say “I searched Jira and found nothing.” Say what you searched and name the nearest neighbors.

---

## 5. Classification — pick exactly one verdict per unique issue

| Verdict | Meaning | What Kylor will do |
|---|---|---|
| **FILE** | Net-new engineering work. Phase 1 found no real ticket. Evidence is strong enough to draft. | File it |
| **ALREADY TRACKED** | Swarm miss. A live ticket covers it. | Cite it / ignore |
| **DROPPED BUT ALIVE** | Nearest ticket is `Archieved` / `Back Burner` and the client is still hitting it. | Decide reopen vs new vs leave |
| **OPS / NOT JIRA** | Import, config, users, invitations, FTP, file-build, how-to. | No ticket |
| **ANSWERED IN PLACE** | Support thread resolved; no product gap remains. | No ticket |
| **INSUFFICIENT EVIDENCE** | Swarm named a smell, not a defect. Cannot recover org / symptom / source. | Park |
| **CONFLICT UNRESOLVED** | Swarms disagree and your verification could not settle it. | Look |

Project guess if FILE (do not guess silently):

- Diagnosed server-side defect or missing control with AC → **SERV**
- iPad client / sync / on-device rendering → **ECAT**
- Raw customer ask, not yet scoped → **EBR**
- Unsure → say so, do not pick

Priority guess: `High` if a client was forced into a damaging workaround or data was exposed; `Medium` if cosmetic or one-org annoyance; leave `Unprioritized` if you do not know.

---

## 6. Confidence on every FILE / DROPPED BUT ALIVE row

Use these tiers. A composite inherits the lowest input.

| Tier | Meaning |
|---|---|
| **STRONG** | HelpScout ID (or pasted ticket) + org shortname + Phase 1 Jira search with named near-misses + a specific mechanism or ask |
| **PARTIAL** | Org + symptom + Jira search, but no HelpScout ID or the chat excerpt is second-hand |
| **LIMITED** | Only a swarm paraphrase; you could not recover the source |

Do not put LIMITED rows in the “file these today” list. They go under INSUFFICIENT EVIDENCE.

---

## 7. Output — this is the only deliverable

Write the summary in **this chat**. Also save one markdown file. Because this prompt is run in parallel, **never overwrite another run**.

1. Detect this run: `hostname`, and whether you are Cursor or Claude Code (from the environment / `CLAUDE.md` vs Cursor rules).
2. Write to:

```
PM/JIRA-MISSED-FROM-CHAT-CONSOLIDATED-YYYY-MM-DD-<host>-<app>.md
```

Examples:

- `PM/JIRA-MISSED-FROM-CHAT-CONSOLIDATED-2026-10-13-kylors-mac-mini-cursor.md`
- `PM/JIRA-MISSED-FROM-CHAT-CONSOLIDATED-2026-10-13-kylors-macbook-claude.md`

3. If that exact path already exists, append `-2`, `-3`, … Do not clobber.
4. Do **not** write the unsuffixed `PM/JIRA-MISSED-FROM-CHAT-CONSOLIDATED-YYYY-MM-DD.md` — that name is reserved for a later human / designated merge.

Put this YAML block at the top of the output file:

```yaml
---
title: Jira missed-from-chat consolidation
date: YYYY-MM-DD
host: <hostname>
app: cursor | claude-code
surfaces_found: N
unique_issues: N
file_count: N
already_tracked: N
---
```

### Required shape

#### A. Coverage
- Surfaces found vs expected (N of 4)
- Date window the union actually covers (not what the swarms claimed)
- How many raw swarm items you ingested, how many unique issues after dedupe
- What you could not see (other device, still-running swarm, truncated transcript)

#### B. Decision list — file these
A numbered table, ranked by (priority, then evidence strength, then recency):

| # | Org | Surface | One-line defect / ask (engineering terms) | HelpScout | Nearest Jira (or “none — searched X”) | Project / type | Priority | Confidence | Why this is a miss | Swarm agreement (e.g. 3/4) |

Under the table, for each FILE row, a **draft ticket Kylor can paste**. Use the Story or Bug template from `supercat-jira`. Include:

- HelpScout link if you have the id
- Verbatim client ask if the swarm quoted it
- Background in engineering terms
- Related: nearest Jira keys and why they are not this
- Open question only if you are not entitled to settle it

Do **not** file them. Do **not** add labels, assignee, or components.

#### C. Already tracked (swarm false positives)
Table: org, symptom, the Jira key, status, why the swarm missed it (wording / project / closed-as-done). Needed so Kylor does not double-file.

#### D. Dropped but still alive
Ticket key, status (`Archieved` / `Back Burner`), org still hitting it, one-line recommendation: reopen vs new ticket vs leave it.

#### E. Not a miss
Counts only, plus 3–5 examples so the sort can be checked: OPS / NOT JIRA, ANSWERED IN PLACE.

#### F. Insufficient / conflicts
Short list. What would unblock each (HelpScout #, org shortname, a pasted thread).

#### G. Patterns, not a sermon
At most five bullets. Only if a pattern is evidenced by ≥3 unique issues (e.g. “eOL inventory visibility asked three times, never ticketed”). No strategy lecture.

#### H. What you did not do
One short list: surfaces you never saw, Jira projects you did not search, HelpScout recovery you skipped because BQ was stale / unavailable.

---

## 8. Working method

1. Inventory and provenance table.
2. Normalize every swarm item onto the identity key. Do not drop items you cannot classify — park them.
3. Classify ops vs engineering **before** spending Jira budget. Ops rows do not get Phase 1.
4. Phase 1 on every remaining engineering candidate. Batch Jira searches where the same domain noun serves several orgs, but still open near-misses per candidate.
5. Dedupe again after Jira (two “net-new” rows often collapse onto one existing SERV).
6. Draft only the FILE tickets.
7. Write the chat summary and this run’s PM file (suffixed path from § 7).
8. Stop. Do not start a second hunt through chat history. Do not “also quickly check HelpScout for anything the swarms missed” unless asked.

---

## 9. Tone

Lead with the decision list. Numbers over adjectives. “14 unique issues from 61 swarm rows; 5 FILE, 6 ALREADY TRACKED, 2 OPS, 1 INSUFFICIENT” is the right opening. Do not narrate your process. Do not congratulate the swarms. Do not soften a miss that should be filed.

If the honest answer is “the write-ups I could see do not support a FILE list,” that is a valid deliverable. Say so, show the already-tracked and ops buckets, and stop.
