# Golden-set eval

The regression safety net for the external Customer Intelligence Report. It replaces the in-agent QC that was removed after the early clean runs, and it is what makes it **safe** to keep runs lean and to harden the runtime authority files (template, blueprint, vm_index, section guides).

## What it proves

For a frozen org, a fresh run still produces a **structurally correct, leak-free** report: the same gate decisions, the same INCLUDE/SKIP section set, no forbidden phrases, no broken HTML, and no cross-contamination. Numeric data is allowed to drift (live prod); structure and gating are not.

## Two modes (matched to blast radius)

| Mode | Needs MCP? | Run it after a change to… | How |
|---|---|---|---|
| **Static** | No | `html_report_template.html`, `section_0N_*.md`, `shared_rules.md`, `stage4_assembly.md` | rebuild Stage 2-4 on `clm/fixture-cache/`, then `./check_static.sh <output.html> <expected_section_count>` |
| **Full** | Yes | `query_library.md`, `stage1_preflight_and_queries.md`, `external_report_blueprint.md`, `external_vm_index.md`, `value_moment_catalog.md`, the prompts | follow `run_eval.md` (re-runs Stage 1, checks gate/manifest parity, then runs Static on the new output) |

## Frozen orgs

| Org | Shortname / id | Coverage profile | Expected snapshot |
|---|---|---|---|
| Crystorama | `clm` / 64 | HAS_CLICKY=true, HAS_CART=false, VM45 not rendered → 7 INCLUDE sections | fresh `2026-06-12` (GREEN reproduction) |
| Wildwood/Chelsea House | `wwjc` / 8 | HAS_CLICKY=false (§6 skipped), HAS_CART=true, VM45 rendered → 6 INCLUDE sections | `2026-04-17` baseline — **refresh on next clean wwjc run** |

Each org folder: `input.md` (run params) + `expected/{gate_flags.md, section_manifest.md, assertions.md}`.

## Acceptance threshold (assert these)

1. Report **mode** == expected.
2. Structural **gate booleans** == expected (HAS_*). Numeric evidence may differ.
3. **INCLUDE/SKIP** section set == expected.
4. `check_static.sh` = **PASS** (hard-forbidden=0, `{{`=0, section count == expected, `<details>` balanced).
5. **No cross-contamination** — only the target org's name/shortname in the output.

A run is **GREEN** if all five hold. **YELLOW** if only acceptable numeric drift differs (with a note). **RED** on any structural/gate/forbidden failure → do not ship the change that caused it.

## When to run (regression trigger)

Before accepting any change to `operators/external/*`, `operators/external/guides/*`, `authority/*`, or `authority/value_moment_catalog.md`. This is the gate for the Phase H de-profiling work.
