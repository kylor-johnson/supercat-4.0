---
name: ecat-session-handoff
description: Generate an end-of-session handoff prompt for an eCat client so the next chat starts with full context and no reloading. Use when wrapping up work on a client, the user asks for a handoff, or context should be persisted for the next session.
---

# eCat Session Handoff

At the end of a working session, generate a single self-contained markdown block the
next chat can be started from. Save it to the client's
`eCat_Onboarding/<Client>/` folder (e.g. `HANDOFF.md`) and update `CLIENT_PROFILE.md`.

A good handoff lets a fresh agent (no prior chat) resume correctly. Include:

```markdown
# <Client> (<org shortname>) — Handoff Prompt

## Context
One paragraph: who the client is, what stage, what we're doing now.

## Source of truth
- Current source file: <path> (everything else is reference only)
- Working files: eCat_Onboarding/<Client>/00_Import_Files/Ready_For_Import/

## Field mapping decisions
| Source column | eCat field | Notes |

## Rules in effect
- Taxonomy method (Standard / Auto-Create); TradeNameCode
- Image rules (which rows get images / `-`); RelatedItems policy
- Pricing model; price levels; division split if any
- Option group pattern / Option Mapping connections if any

## Current state
- Row counts (products / collections / categories), images matched, etc.
- Last import date + result; any known-bad passes to avoid repeating

## Validation checklist (must pass before import)
- [ ] 0 duplicate BaseItemCode
- [ ] 0 blank required fields
- [ ] lengths OK (BaseItemCode<=40 enforced, 20 advisory; option codes/groups<=15)
- [ ] image/RelatedItems policy applied
- [ ] File Import Status error-free

## Open items / client confirmations
- ...
```

Rules: a NEW source file the client sends becomes the source of truth (old files are
reference). Don't create random backup files. Keep the handoff to one file.
