# Report Generation — Orchestrator

> Execution reference for the external intelligence report. The **canonical path is the single unified prompt** below. The multi-stage validator swarm is retained as an **optional QA mode** (appendix) — it is not run by default.

---

## Canonical flow (default)

| Step | Prompt | Writes | Checkpoint |
|---|---|---|---|
| Full run (Steps 1–4) | `operators/external/run_prompt.md` | `runs/{shortname}_{date}/cache/*`, `fragments/section_NN.html`, `output/{shortname}_{date}_intelligence_report.html` | Agent reports gate/manifest summary after data gathering; runs static check after assembly |

- **MCP required (Step 1 only)**: `user-supercat-postgres-vpn` + `user-bigquery-admin`.
- **Mode 2/3 note**: if Step 1 selects Mode 2 (Activation) or Mode 3 (Reactivation), the report completes within Step 1; Steps 2–3 are Mode 1 only.

---

## Optional QA mode — validator swarm (off by default)

The original design ran section building and a per-section validation swarm as separate parallel agents. In-agent QC was removed after 10 clean runs (`RUNBOOK.md` Phase History); the current default is the single-prompt flow with a built-in static check + browser review.

Re-enable the validator swarm only when making non-trivial changes to the prompts/guides and you want extra assurance before the golden-set eval exists:

- **Parallel builders**: one Task per INCLUDE section — reads `shared_rules.md` + `section_NN_*.md` + relevant cache; writes `fragments/section_NN.html` + `cache/section_NN_highlights.md`.
- **Parallel validators**: one Task per built section — reads `shared_rules.md` + `section_NN_*.md` + `stage3_validator.md` + the fragment; writes `cache/validation_section_NN.md`; aggregate to `cache/validation_checklist.md`.
  - Re-dispatch = full regeneration (not targeted edit), max 2 per section, then flag for human review.
- **Assembly**: `stage4_assembly.md` — assembles fragments + highlights into the final HTML.
