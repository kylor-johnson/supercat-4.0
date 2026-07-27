---
name: ecat-support-triage
description: Triage a one-off eCat support request — a HelpScout ticket or a client email — diagnose it, route to the right ecat-* skill, ground it in live client state, and draft a reply in Kylor's voice. Use for ad-hoc issues outside a net-new build (missing images on iPad, wrong price, "everyone disappeared from my customer list", a mid-project question), or whenever a ticket/email needs a diagnosed answer rather than a full onboarding pass.
---

# eCat Support Triage (reactive mode)

The **reactive** entry point to onboarding work. Where `ecat-onboarding-orchestrator`
walks a net-new client through phases, this handles a single inbound signal — a HelpScout
ticket or a client email — and turns it into a diagnosed fix plus a drafted reply.

Always-on rules apply (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`). The
dangerous delete semantics in `ecat-ground-truth` are the most common root cause here.

## The loop

```
1. INGEST    → take the pasted ticket/email (or pull it from BigQuery HelpScout tables)
2. IDENTIFY  → which client/org? known onboarding client or net-new?
3. CLASSIFY  → map the problem to a domain (table below)
4. GROUND    → read eCat_Onboarding/<Client>/CLIENT_PROFILE.md; if unknown or unsure,
               run ecat-postgres-audit by org shortname to get REAL state, not a guess
5. DIAGNOSE  → route to the domain skill, confirm root cause against ground truth
6. REPLY     → draft the response with ecat-client-email (draft only — never auto-send)
7. LOG       → append a dated line to eCat_Onboarding/<Client>/HANDOFF.md
```

Do not answer from assumption. If the fix depends on current state (counts, what
imported, what's visible), GROUND first — step 4 is not optional for state-dependent
questions.

## Ingesting from HelpScout

If the ticket isn't pasted, pull it from the BigQuery HelpScout tables via the
bigquery MCP. Confirm the current table/column names with a `list_tables` /
`get_table_schema` call before querying — the warehouse schema changes and the static
docs can lag. Capture: subject, body, customer email/company, and the thread so far.

## Classify → route

| Symptom in the ticket/email | Likely domain | Route to |
|---|---|---|
| Images missing / wrong hero / won't show on iPad | image pipeline / FTP | `ecat-images-ftp` |
| Price wrong, blank, $0.00, or wrong per customer | pricing / price levels | `ecat-pricing-levels` |
| Customers or ship-tos missing after an upload | **HARD-delete on omission** | `ecat-ground-truth` → `ecat-customers-build` |
| Inventory/options wiped after a partial file | **HARD-delete on omission** | `ecat-ground-truth` → `ecat-core-files` / `ecat-options-and-mapping` |
| Expected deletes didn't happen | an `Error` row blocked deletes | `ecat-import-ops` |
| New/updated product file to load | core files build | `ecat-core-files` |
| Option swatches / cascading filters wrong | options + mapping | `ecat-options-and-mapping` |
| SmartList not appearing / wrong items | smartlists | `ecat-smartlists` |
| Rep can't see catalog / wrong customers / login | users, groups, territories | `ecat-go-live` |
| "Why is the item code showing instead of the name" | known UI limit | answer honestly (see `ecat-client-email`) |
| Anything needing live counts/state to answer | live DB audit | `ecat-postgres-audit` |

When in doubt between two domains, GROUND with `ecat-postgres-audit` first — the real
state usually disambiguates.

## Reply posture

Draft with `ecat-client-email` (warm, declarative, point-by-point, **"Best, Kylor"**).
Carry its discipline:
- Don't claim something is fixed/uploaded until it actually is.
- State UI limits honestly rather than overpromising.
- Give the exact next action and who owns it (FTP folder, Admin path, "sync on Wi-Fi").
- Keep internal context (health scores, support history, CDN) out of client copy.

Drafts only. This skill never sends; you paste/approve.

## Existing vs net-new client

- **Existing onboarding client:** read their `CLIENT_PROFILE.md` for taxonomy method,
  pricing model, and snowflake quirks before diagnosing. Log the outcome to `HANDOFF.md`.
- **Net-new / unknown:** if the ticket is really the start of an onboarding, hand off to
  `ecat-onboarding-orchestrator` and bootstrap a client folder instead of one-off patching.

## Capture the lesson

If the root cause is generalizable (not client-specific), note it so it can be promoted
to `eCat_Onboarding/<Client>/LESSONS_LEARNED.md` and, eventually, a test fixture. Repeat
tickets with the same root cause are a signal to harden the build, not just reply faster.
