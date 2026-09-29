---
name: ecat-client-email
description: Draft eCat onboarding and support emails to clients in Kylor's voice — numbered point-by-point replies, demo-vs-final scoping, "what we have vs what we need", FTP/Admin next steps. Use when drafting or replying to an onboarding client email, support follow-up, or status update. NOT for pricing-migration notices (those follow Pricing Migration/_root/04).
---

# eCat Client Email (onboarding & support)

Scope: onboarding/implementation/support emails. For pricing-migration notices use
the rules in `Pricing Migration/_root/04_communication_posture.md` instead.

## Voice

- Warm, professional, declarative. Peer-to-principal, not service-rep cheerful.
- **Mirror the client's structure** — if they sent 6 numbered questions, answer
  1. to 6. in order, as plain numbered lines.
- **Own genuine mistakes briefly and specifically**, then state the fix. ("My
  apologies for the confusion — I had prepared the updated file but hadn't uploaded
  it yet. It's live now.") Do not over-apologize and never apologize for the product.
- **Scope demos honestly**: "this is an initial demo to confirm layout and mapping
  direction — not the final approved setup."
- **Concrete next steps**: exact FTP folders, Admin Console paths, upload order,
  "please sync your iPad on Wi-Fi and let me know."
- Be honest about limits ("grid view always shows the item code — that's fixed; we
  can surface the name in Quick View instead. Would that work?").
- Match the client's technical level (non-technical principal vs file-savvy ops
  contact). Avoid eCat jargon for non-technical readers.
- Sign off: **"Best, Kylor"**.

**Tone rules (hard):**
- **No em-dashes.** Use a comma, period, or parentheses instead.
- **Plain text that pastes into Gmail.** No markdown tables, no bold, no headers; lists are plain lines.
- **Do not force in irrelevant numbered points.** Mirror the client's structure only
  where it's genuinely responsive — don't manufacture a point just to match their count.
- **Do not re-explain something already fixed.** If it's done, say it's done and move on;
  don't re-narrate the whole diagnosis.
- **Avoid generic "AI slop" phrasing** (e.g. "I hope this email finds you well,"
  "please don't hesitate to reach out," "as per our discussion," "leverage," "seamless").
  Write plainly and specifically.

## Reusable structures

**Point-by-point reply** — acknowledge → answer each numbered item with fix +
one-line why → next steps → offer a call.

**"What we have vs what we need"** (e.g. missing current price list, missing
addresses): two short lists + the one concrete ask to unblock.

**Source-of-truth / correction** (client pushed back on data lineage): acknowledge,
adopt their correction as the decision, summarize the rebuild plan, confirm the load.

**Self-service handoff with guardrails**: what they can safely manage (NetPrice edits,
Admin Option Mappings) vs what breaks things (re-uploading an old option_groups.csv).
Always include: **download the current file from FTP `/data` before editing.**

## Pre-send checklist

This checklist is the one home of the copy-truth rules; `ecat-support-triage` and
`ecat-correspondence` point here rather than restating them.

```
- [ ] No past-tense action that hasn't happened ("uploaded", "fixed", "enabled", "I've passed that to product", "I've raised it"). Re-query anything claimed changed; old value → future tense ("I'll…") plus an Owner action
- [ ] Anything I claimed "configured" is verified on the device (or Admin field, for price-level / group auth)
- [ ] Every exclusive or comparative claim ("the only one", "the rest of your team", "all", "never") is backed by a count over the whole population, shown in VERIFY
- [ ] Every example the client is told to try (an item, a customer, a login, a URL) is one the person trying it can actually see: check it against their user group's trade-name / collection / price authorisations
- [ ] No release or date promised for a fix unless the fix commit is on the branch that ships in that build (check the release/* branch, not the ticket status)
- [ ] No promise to edit a value the client's own import file controls (it comes back on their next upload); name the file and column they change instead, or say we change it and they must change their export too
- [ ] Relative time words ("today", "yesterday", "this morning") match the send date in the client's time zone; otherwise write the date
- [ ] Named record and import-error record are the same code, or the email treats them as two problems
- [ ] Draft has no truncated/garbled sentences and no duplicated paragraphs
- [ ] Stated UI limits honestly (grid item code, etc.)
- [ ] /images vs /option_images vs /data stated where relevant
- [ ] Clear next action + who does it
- [ ] Internal-only context (China CDN, support tickets, health scores, `*.html.erb` paths) NOT in client copy
- [ ] Every person named in the copy checked against `users.first_name` / `last_name`, never inferred from a username; a first name shared by a SuperCat person and a client contact is written in full
- [ ] Every "shows" or "displays" claim names the surface: Admin Console page, Admin CSV export, eOL order page, eOL invoice page, Orders/Invoices list, or iPad
- [ ] Anyone the draft invites, merges or resets is looked up in `users` across all orgs by email, domain and name first; use an existing login, and put any spelling mismatch with the client's address in the reply
- [ ] Every commitment lifted from a meeting summary checked against live state before it is written as done
- [ ] Owner actions section present (below)
```

## Owner actions (required on every onboarding and support draft)

The draft is not finished until the owner knows exactly what he does before the copy
is true. A numbered list, one step per line, each naming:

- the Admin Console path, or the file and column, or the script (dry-run first,
  per `supercat-mcp-access`), or the query;
- the check that proves it landed (File Import Status `- []`, the Postgres row
  and its `updated_at`, the Admin field);
- who owns it if not the owner (the support lead, the client, engineering with the Jira key).

If the copy promises the client something ("I will send screenshots", "the
links come by Friday"), this section says how that thing gets made. Measured
2026-09-25: a draft promised a configuration change on two SKUs with no steps
behind it, and the first step turned out to be an org-level prerequisite nobody
would have guessed. Read the org's setup for the thing you promise before
writing the steps.

The High Point Market follow-up email skill (`hpmkt-follow-up-email`) covers
post-market recaps in the same voice family.
