# Operator: Run the golden-set eval

> Paste into a fresh agent. Pick a mode and an org. Produces a PASS/FAIL result file. Do not modify anything outside the eval run dir.

## Inputs
- **Org**: `clm` or `wwjc` (see `qa/eval/<org>/input.md` for params)
- **Mode**: `static` (no MCP) or `full` (MCP required)
- Base path: `Insightful Product 2.0/`

---

## Mode: STATIC (no MCP)

Use after changes to the HTML template, section guides, `shared_rules.md`, or `stage4_assembly.md` — i.e. anything that changes rendering but not gating/queries. No MCP needed because Stage 1 is not re-run; you rebuild only Stage 2-4 against a frozen cache.

**Rebuild fixture**: `qa/eval/clm/fixture-cache/` is a complete frozen Stage-1 cache (all `Q-*_results.md` + `gate_flags.md` + `section_manifest.md`) captured from a GREEN FULL run. It lets you rebuild the report without touching the database.

1. Read `qa/eval/<org>/expected/assertions.md` to get the expected section count.
2. **Rebuild** (no MCP): run `prompts/stage2_through_4_build_and_assemble.md` with the org's Stage 2-4 params, pointing it at the frozen cache `qa/eval/clm/fixture-cache/` (copy it into a scratch run dir's `cache/` if the prompt expects a run path). This produces an output HTML. Prose will vary run-to-run — that is expected; the static checks below are what matter.
3. Run:
   ```
   qa/eval/check_static.sh <path-to-output.html> <expected_section_count>
   ```
4. Cross-contamination check: confirm the output contains only the target org's name/shortname (grep for it; grep that no other client shortname appears).
5. Record PASS/FAIL to `qa/eval/<org>/results/{YYYY-MM-DD}_static.md`.

---

## Mode: FULL (MCP required: Postgres + BigQuery)

Use after changes to `query_library.md`, `stage1_preflight_and_queries.md`, `external_report_blueprint.md`, `external_vm_index.md`, `value_moment_catalog.md`, or the prompts.

1. **Read** `qa/eval/<org>/input.md` for the run params. Use **today's date** for the run so you do not overwrite anything; run dir = `runs/<shortname>_<today>/`.
2. **Stage 1** — execute `prompts/stage1_data_gathering.md` with the org params. If MCP/VPN is unavailable, STOP and report `BLOCKED: MCP unavailable`.
3. **Gate + manifest parity** — compare `runs/<shortname>_<today>/cache/gate_flags.md` and `cache/section_manifest.md` against `qa/eval/<org>/expected/`. Assert (per `expected/assertions.md`):
   - report **mode** matches
   - every **HAS_*** / BENCHMARK_ELIGIBLE **boolean** matches (numeric evidence may differ — not asserted)
   - the **INCLUDE/SKIP** section set matches
   Flag any boolean flip with the likely data reason.
4. **Stage 2–4** — execute `prompts/stage2_through_4_build_and_assemble.md` with the org params to produce the output HTML.
5. **Static checks** — run `qa/eval/check_static.sh <output.html> <expected_section_count>` and the cross-contamination check.
6. **Verdict** — GREEN (all pass), YELLOW (only acceptable numeric drift differs, noted), RED (any structural/gate/forbidden failure).
7. Record to `qa/eval/<org>/results/{YYYY-MM-DD}_full.md`.

---

## Result file template

```markdown
# Eval result — <org> — <date> — <mode>
Verdict: GREEN | YELLOW | RED

| Check | Expected | Observed | Result |
|---|---|---|---|
| Report mode | ... | ... | PASS/FAIL |
| Gate booleans | ... | ... | PASS/FAIL |
| INCLUDE set | ... | ... | PASS/FAIL |
| check_static.sh | PASS | ... | PASS/FAIL |
| Cross-contamination | none | ... | PASS/FAIL |

Acceptable drift (notes): ...
Regressions (if any): ...
Output: runs/<shortname>_<date>/output/<file>.html (<size>)
```
