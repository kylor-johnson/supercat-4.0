# Stage 3 — Output Format

**Purpose:** Assemble the collected metrics (Stage 1) and validation (Stage 2) into the final assessment markdown and write it to the output folder.
**Runs after:** `Stage_Gated_Data_Collection.md` and `Validation_Layer_Fathom_HelpScout.md`.

## The contract

Write **one file** per run:

```
onboarding-models/output/{YYYY-MM-DD}-assessment.md
```

`{YYYY-MM-DD}` = the run date from Step 0 (`date -u +%F`). This markdown file **is** the deliverable. Do not push to Notion. (A prettier HTML "WoW" view is a planned later layer built from this same content — not part of this run.)

Substance over styling: the sections, ordering, and evidence below are required; exact emoji/spacing is not. Every fact must trace to a Stage 1 or Stage 2 tool result.

## Required structure

Reproduce this layout (proven in `output/2026-06-03-assessment.md`):

### 1. Title
```markdown
# {Month D, YYYY} — Onboarding Assessment
```

### 2. Pipeline Overview (table)
One row per client:

```markdown
## Pipeline Overview

| Client | Product | Owner | Stage | Readiness | Biggest Blocker | Validation | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TCS** | eCat iPad | Kylor | 2 / 7 | 30% | 0 price levels; Catsy export stalled | ⚠️ 2 flags | ~44 |
```

### 3. Pipeline View — least ready → most ready (ASCII bar)
```
TCS   ██████░░░░░░░░░░░░░░ 30%  Stage 3 - Pricing          ⚠️ ACTIVE ENGAGEMENT
PEBL  ███████████░░░░░░░░░ 55%  Stage 5 - Customer Setup   ⚠️ ACTIVE ENGAGEMENT
```
Bar = 20 chars; filled = `round(readiness/5)`. Status tag from validation confidence (`ACTIVE ENGAGEMENT` / `FLAGGED` / `STALE`).

### 4. Per-client section (one per client, sorted by readiness ascending)
For each client:

```markdown
## {SHORTNAME} ({Company Name})

**Assessment:** Stage {X} | {Y}% Ready | Products: {eCat iPad / eCat Online / Sales Portal}

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | {metric evidence} |
| ... | ... | ... |
| 7 | 🔴 | {metric evidence} |

🎯 **Next Action:** {the single most important next step, blocker-driven}

{⚠️/🔴} **Validation Flags ({N})**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 3 | ⚠️ {FLAG} | {Fathom date / HelpScout #ticket / Import date} | "{quote or specific fact}" |

**Validation Summary:** {2–5 sentences reconciling metrics with calls/tickets — what changed, what's blocking, what to do.}
```

Rules for the per-client section:
- **Status legend:** 🟢 ready · 🟡 partial · 🔴 blocker · ⚫ N/A. Mark a 🔴 stage **BLOCKER** in the evidence cell when it gates progression.
- **Out-of-sequence completion** (e.g. options done while pricing is blocked) — note it in the evidence cell.
- Every validation-flag row needs a real **source** (Fathom date / HelpScout ticket # / import-event date) and a verbatim quote or specific fact. No source → no flag.

### 5. Validation Flags Summary (cohort roll-up)
```markdown
## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)
| Client | Stage | Issue | Evidence | Action |

### ⚠️ Review Flags (Need Clarification)
| Client | Stage | Issue | Evidence | Action |

### ✅ Confirmed (No Flags)
| Client | Stage | Readiness | Status |
```

## Computing the two headline numbers

- **Stages Passed / Current Stage:** apply the gating in `Stage_Gated_Data_Collection.md`. Current Stage = the first non-🟢 required stage (⚫ N/A stages are skipped, not counted as failures).
- **Readiness %:** `round(green_required_stages / total_required_stages * 100)`. Required stages depend on the product (see the Products-supported table in Stage 1). 🟡 counts as half a stage if you want finer granularity, but be consistent across the cohort.

## Final checks before writing

- Clients sorted by readiness ascending (least ready first) in the Pipeline View and per-client sections.
- Every client from the run's shortname list is present (or explicitly flagged unresolved).
- No metric without a backing tool result; no flag without a source.
- File written to `onboarding-models/output/{RUN_DATE}-assessment.md`.
