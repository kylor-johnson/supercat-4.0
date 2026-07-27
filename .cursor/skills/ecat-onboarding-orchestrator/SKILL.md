---
name: ecat-onboarding-orchestrator
description: Drive an eCat iPad client onboarding end to end — read the client's state, figure out the current lifecycle phase, route to the correct ecat-* skill, enforce the phase gate, and persist state. Use to start or resume any client onboarding, when asked "what's next" for a client, or when you have a client source file but aren't sure which skill applies.
---

# eCat Onboarding Orchestrator

This is the **controller** for an eCat iPad onboarding. It does not do the build work
itself — it loads client state, determines the phase, hands off to the right `ecat-*`
skill, and refuses to advance a phase until that phase's gate passes.

Always-on rules still apply (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`).
This skill orchestrates; those rules constrain.

## The loop (run this every session)

```
1. LOAD STATE   → read eCat_Onboarding/<Client>/CLIENT_PROFILE.md + HANDOFF.md
2. RECONCILE    → for any client past kickoff, ground the profile against the LIVE DB
                  via ecat-postgres-audit (counts + most-recent import_events). Trust the
                  DB over the markdown; flag and correct any mismatch before proceeding.
3. LOCATE PHASE → match RECONCILED state against the 7 phases below
4. CONFIRM      → state the client, phase, source-of-truth file, and today's task
5. ROUTE        → invoke the skill(s) for this phase (table below)
6. GATE         → run the phase gate (see PHASE_GATES.md). Do NOT advance until it passes.
7. PERSIST      → update CLIENT_PROFILE.md (with reconciled state) + write HANDOFF.md via
                  ecat-session-handoff
```

All client state lives under `eCat_Onboarding/<Client>/` in the **SuperCat 4.0** root
(one repo, one roof). When you invoke `ecat-session-handoff`, point it at this path —
its own doc text may still say `02_Implementation/`; this orchestrator's path wins.

Never skip step 6. The whole point of the orchestrator is that a phase is "done" only
when its gate passes — not when the CSV "looks right."

## Reconcile before you act (the profile lies)

`CLIENT_PROFILE.md` is backfilled by hand and **drifts**. Verified case: Terracotta's
profile said "go-live blocked, 0 customers imported," but the live DB had 346 customers —
the blocker was fixed in a later session that never updated the markdown.

So for any non-new client, before locating the phase:
- Resolve the org and pull live counts + the **most-recent `import_events`** with
  `ecat-postgres-audit`. There is no stored "status" field — derive stage from reality.
- **The live system is the source of truth, not local files.** A client may have run a
  NEWER FTP/Admin import than the last CSV we sent (or after we sent one back), so a local
  `Ready_For_Import/` file can be stale. Check `import_events` (= Admin "File Import
  Status") for what actually loaded and when, then reconcile the profile.
- If the DB and profile disagree, correct the profile as part of PERSIST.

## Source of truth (non-negotiable)

Two different "sources of truth" — don't conflate them:
- **For what we BUILD:** the **latest file the client sent** (older files are reference).
  Working outputs live in `eCat_Onboarding/<Client>/00_Import_Files/Ready_For_Import/`.
- **For what is actually LIVE:** the **database + most-recent `import_events`** (Admin
  "File Import Status"). The client may have imported something newer than our last file,
  so never assume a local CSV reflects the live catalog — verify via `ecat-postgres-audit`.
- Don't invent backup files; keep one `CLIENT_PROFILE.md` and one `HANDOFF.md`.

## New client?

Bootstrap before routing:
1. Copy `eCat_Onboarding/_Template/` → `eCat_Onboarding/<Client>/`.
2. Fill `CLIENT_PROFILE.md` (identity, systems, taxonomy method, pricing, images).
3. Read `<Client>/LESSONS_LEARNED.md` before building — it prevents repeat mistakes.
4. Start at Phase 1.

## Phase → skill routing

| Phase | What it covers | Route to | Gate (see PHASE_GATES.md) |
|---|---|---|---|
| 1. Discovery / Kickoff | shortname, contacts, ERP/PIM, pricing model, go-live date | `ecat-client-email` (intake) | G1 |
| 2. Admin pre-flight | tradenames/collections, groups→categories, custom fields, price levels, option types, FTP, flags | `ecat-pricing-levels`, `ecat-options-and-mapping` | G2 |
| 3. Build | products → stories → inventory → customers; options; pricing columns; image naming | `ecat-core-files`, `ecat-customers-build`, `ecat-pricing-levels`, `ecat-options-and-mapping`, `ecat-images-ftp` | G3 |
| 4. Import | correct order, via Tools/Upload or FTP `/data`, File Import Status error-free | `ecat-import-ops` (rule), `ecat-images-ftp` | G4 |
| 5. iPad review | hero images, visible counts, pricing per customer type, related/options/smartlists | `ecat-images-ftp`, `ecat-smartlists`, `ecat-postgres-audit` | G5 |
| 6. Go-live | user groups, price-level visibility, reps + territories, order email, PDF formats | `ecat-go-live` | G6 |
| 7. Maintenance | recurring feeds, image two-step, health/state audits | `ecat-images-ftp`, `ecat-postgres-audit`, `ecat-session-handoff` | G7 |

Sub-task overrides (use even mid-phase when the user asks for one thing):

| Ask | Skill |
|---|---|
| products / stories / inventory build | `ecat-core-files` |
| customers | `ecat-customers-build` |
| pricing / price levels / divisions | `ecat-pricing-levels` |
| options + Option Mapping | `ecat-options-and-mapping` |
| images / FTP / missing images | `ecat-images-ftp` |
| smartlists | `ecat-smartlists` |
| users / reps / territories / go-live | `ecat-go-live` |
| client email / reply | `ecat-client-email` |
| live DB audit | `ecat-postgres-audit` |
| end of session | `ecat-session-handoff` |

## Import order (Phase 4 — enforce, don't reorder)

`options.csv → option_groups.csv → products.csv → stories.csv → inventory.csv → customers.csv`

Re-send `option_groups.csv` after `options.csv` (importing options nulls group membership).
Deletes only run on a clean (warnings-only) import; an `Error` row skips all deletes. Send
full files — customers/inventory/options HARD-delete omitted records.

## Verification tools (run before each gate; details in PHASE_GATES.md)

```bash
# Data quality + code inventory (Phase 3 → G3)
python scripts/validate_products.py <Ready_For_Import/products.csv>

# Image integrity (Phase 3/5 → G3/G5) — only if images staged locally
python scripts/audit_images.py <Ready_For_Import/products.csv> <image_dir> [--max 12]

# Customer file: required fields + the DefaultPriceCode blocker (Phase 3 → G3)
python scripts/validate_customers.py <Ready_For_Import/customers.csv> --price-levels <codes-from-DB>
```

Both exit non-zero when issues exist, so the gate can branch on the result. The validator
also prints every unique `CollectionCodes`/`CategoryCodes` value — under the Standard
taxonomy method, create each one in Admin before import (Auto-Create orgs skip this).

## End every session

Update `CLIENT_PROFILE.md` (import history row, open items, current source-of-truth) and
regenerate `HANDOFF.md` via `ecat-session-handoff` so the next session resumes cold.

## Additional resources

- Phase gates / definition-of-done per phase: [PHASE_GATES.md](PHASE_GATES.md)
