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
  `**1.**`–`**6.**` in order.
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

```
- [ ] Files actually uploaded (not "Done!" before upload confirmed)
- [ ] If the draft says "I've already changed X", re-query X live. Old value → do not send that sentence
- [ ] Anything I claimed "configured" is verified on the device (or Admin field, for price-level / group auth)
- [ ] Named record and import-error record are the same code, or the email treats them as two problems
- [ ] Draft has no truncated/garbled sentences and no duplicated paragraphs
- [ ] Stated UI limits honestly (grid item code, etc.)
- [ ] /images vs /option_images vs /data stated where relevant
- [ ] Clear next action + who does it
- [ ] Internal-only context (China CDN, support tickets, health scores, `*.html.erb` paths) NOT in client copy
```

The High Point Market follow-up email skill (`hpmkt-follow-up-email`) covers
post-market recaps in the same voice family.
