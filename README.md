# eCat Onboarding Automation

Personal staging repo for SuperCat's eCat iPad onboarding automation IP —
Cursor agent skills, import rules, onboarding models, and orchestration tooling.

## Status

**Personal staging** — parked here until the company repo situation (SuperCatSolutionsLLC/agentic_operations) is resolved and a clean separation is established.

This repo holds only onboarding-related intellectual property. It does not contain client data, secrets, or the broader SuperCat 4.0 workspace.

## What's in here

| Path | Description |
|---|---|
| `.cursor/skills/ecat-*/` | Cursor agent skills for each onboarding phase |
| `.cursor/rules/ecat-*.mdc` | Import ground truth and data model rules |
| `eCat_Onboarding/` | Per-client onboarding workspaces |
| `onboarding-models/` | Phase framework, output contracts, templates, and rendering pipeline |
| `IMPLEMENTATION_PLAN.md` | Full automation implementation plan (2026-07-27) |

## Implementation Plan

See [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md) for the complete roadmap
covering the loop architecture, phase-gate model, agent skill structure, and
build-out sequence.

## What's excluded

- Client data files (`customers.csv`, `Ready_For_Import/*.csv`)
- Transcript archives (`*transcript*.zip`, `ecat-onboarding-transcripts-MERGED-*`)
- Secrets (`.env`, `*service-account*.json`)
- Frozen legacy folders (`Insightful Product 2.0/`, `3.0/`)
- Other SuperCat 4.0 workspace folders not relevant to onboarding
