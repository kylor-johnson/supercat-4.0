# Staged Report Generation — Orchestrator

> Execution reference for the external intelligence report. The **canonical path is the 2-prompt flow** below. The multi-stage validator swarm is retained as an **optional QA mode** (appendix) — it is not run by default.

---

## Canonical flow (default)

| Step | Prompt | Writes | Checkpoint |
|---|---|---|---|
| Stage 1 — Data gathering | `prompts/stage1_data_gathering.md` | `runs/{shortname}_{date}/cache/*` | Review `cache/gate_flags.md` + `cache/section_manifest.md` |
| Stages 2–4 — Build & assemble | `prompts/stage2_through_4_build_and_assemble.md` | `fragments/section_NN.html`, `output/{shortname}_{date}_intelligence_report.html` | Forbidden-phrase grep + browser review (see `RUNBOOK.md`) |

- **MCP required (Stage 1 only)**: `user-supercat-postgres-vpn` + `user-bigquery-admin`.
- **Mode 2/3 note**: if Stage 0 (inside Stage 1) selects Mode 2 (Activation) or Mode 3 (Reactivation), the report completes entirely within Stage 1; Stages 2–4 are Mode 1 only.

---

## Optional QA mode — validator swarm (off by default)

The original design ran section building and a per-section validation swarm as separate parallel agents. In-agent QC was removed after 10 clean runs (`RUNBOOK.md` Phase History); the current default is the 2-prompt flow with post-build grep + browser review.

Re-enable the validator swarm only when making non-trivial changes to the prompts/guides and you want extra assurance before the golden-set eval exists:

- **Stage 2 (parallel builders)**: one Task per INCLUDE section — reads `shared_rules.md` + `section_NN_*.md` + relevant cache; writes `fragments/section_NN.html` + `cache/section_NN_highlights.md`.
- **Stage 3 (parallel validators)**: one Task per built section — reads `shared_rules.md` + `section_NN_*.md` + `stage3_validator.md` + the fragment; writes `cache/validation_section_NN.md`; aggregate to `cache/validation_checklist.md`.
  - Re-dispatch = full regeneration (not targeted edit), max 2 per section, then flag for human review.
- **Stage 4 (assembly)**: `stage4_assembly.md` — assembles fragments + highlights into the final HTML.
