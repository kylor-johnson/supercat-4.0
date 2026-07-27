# onboarding-models — Archive

This folder preserves prior work that is no longer part of the live weekly run.
Nothing here is deleted; it is kept for provenance and rollback.

## `baseline_pre-bq-migration_2026-06-03/`

A **frozen, self-contained snapshot** of the working weekly assessment as it
existed on 2026-06-03, immediately before migrating its data plumbing from the
stale Weld views to the native `supercat-data-pipeline` BigQuery datasets.

Captured because the three live prompts will be rewritten in place (Phase 3);
this is the last known-good version of the *old* generation.

| File | What it is |
|---|---|
| `Stage_Gated_Data_Collection.md` | Stage 1 — PostgreSQL + BigQuery (Weld) metric collection |
| `Validation_Layer_Fathom_HelpScout.md` | Stage 2 — Fathom + HelpScout qualitative validation (Weld views) |
| `Notion_Output_Format.md` | Stage 3 — output formatting (V11 labels, Notion target) |
| `BIGQUERY_WINDMILL_MCP_REFERENCE.md` | Copy of the root-level Weld/MCP reference these prompts depended on |
| `EXAMPLE_OUTPUT_2026-06-03-assessment.md` | The actual assessment these prompts produced on 2026-06-03 (4-client cohort: TCS, PEBL, LIBCO, DRF) |

This run is the **labeled baseline** — the substance the rebuilt workflow must
reproduce (the formatting/emoji/Notion specifics are intentionally not binding).

## `superseded_versions/`

Older FRDs, playbooks, checklists, and a point-in-time assessment that the
weekly run no longer references. Moved out of the live folder to remove version
sprawl; retained for history.

- `FRD_V10_Stage_Gated_Onboarding.md`
- `FRD_V11_Fast_Stage_Gated_Onboarding.md`
- `FRD_V12_Accuracy_Stage_Gated_Onboarding.md`
- `Stage_Gated_Onboarding_Playbook_V12.md`
- `Stage_Gated_Onboarding_Playbook_V14.md`
- `V10_Stage_Gated_Checklist.md`
- `V10_Pipeline_Assessment_January_2026.md`
- `V8 - Full Suite 2e8231dbcd7080d79066e3b61f57b9c4.md`
