# STAMPS — Insightful 4.0 remediation

Append-only. One row per stamped task. Protocol: [`../../EXECUTION_PLAN.md`](../../EXECUTION_PLAN.md).

| Date | Task | Branch | Verdict | Reviewer note |
|---|---|---|---|---|
| 2026-09-16 | PHASE-0 | (direct to main) | **STAMP** | Baseline 11 orgs / 9.7s; harness green; 58 client reports untracked; audit + plan committed |
| 2026-09-16 | P0-9, P0-1 | `48dc0ec` | **STAMP** | kal exit1→SHIP; "went dark" reconciled on hfg/cci/bmc |
| 2026-09-16 | P0-2, P0-3 | `fd02e2b` | **STAMP** | behavior-only hero label; 3 chomp sites; prose inputs re-tracked |
| 2026-09-16 | P0-4, P0-5, P0-11 | `a9c2df0` | **STAMP** | double heading on 8/11; account+rep+prose names; zero-base target |
| 2026-09-16 | P0-6 | — | **BLOCKED** | stale S1 cache on 5 orgs; needs VPN + Postgres |
| 2026-09-17 | P0-7, P0-8, P0-10 | `exec/W1` `687414f` | **STAMP** | all DoD met, verified by re-running; cohort 8/1/2 → **10 SHIP / 1 REDIRECT / 0 fail** |


---

| 2026-09-17 | PHASE-2 golden re-freeze | `main` | **STAMP** | v11 (4 orgs) → v12 (11 orgs); `GOLDEN SET: PASS (11/11)`; `make check` green |

---

## Reviewer note — W1 (2026-09-17)

Verified by re-running, not by reading the evidence. Independent checks:

| claim | how I checked | result |
|---|---|---|
| bmc ships | `./run.sh bmc --date 2026-07-09` | `smoke_check: PASS · step10: PASS · SHIP` |
| smoke_check not weakened | `git diff` on `smoke_check.py`, `golden_set.json` | untouched — structurally true, not asserted |
| escape hatch works | `--no-narrative` across all 11 orgs | **11/11** ship deterministically |
| P0-8 introduces no SKU collisions | normalised every hfg catalog row, grouped by output label | **0 new**; the 3 duplicate labels were already identical in source |
| P0-8 leaves odd catalogs alone | normalised all 8 catalogs | ali 0/25, bri 0/25, clc 0/25 changed — `FLMNT RND` intact |
| P0-7 no false positives | grepped the fired signal across all 11 reports | fires on **hfg only** |
| cohort delta | captured `_ref` at `exec/phase-0-baseline`, `_w1` at `exec/W1`, diffed | matches the evidence |

**One discrepancy, in W1's favour.** I counted 7 orgs visible-text-identical, the
evidence says 6. `sarreid` changed a double space to a single space, which
`html_to_text` collapses but the HTML does not — so the deterministic core moved
with zero visible-text delta. W1 measured by core SHA, the stricter test, and
disclosed it. My measure was the looser one.

**Scope deviation, accepted.** `run.sh` was not on the brief's In list. The DoD
explicitly offered the choice between adding the flag and documenting the module
form, W1 chose the flag, flagged it prominently, and the result is that the
escape hatch README documents is now reachable through the entrypoint README
names. Correct call.

**Quality notes.** The `sensitivity_hedge()` macro branches on `is_stale` and
names the uncertainty class rather than stamping a bracket — *"A refreshed feed
moves the size of these numbers, not their direction; pressure-test the size
before you plan against it."* That satisfies communication_guideline FM4 ("the
prose must carry the confidence, not just the tag"), which the §Q gate alone
does not enforce. The P0-7 lead does the interpretive work without inventing
causation: *"that is one project, not a line the field can reorder."*

Two disclosures I would have had to find myself, and did not have to:
`hfg`'s §3 play title is still the raw field because `looks_like_code` reads it
pre-normalisation; and `kal`'s `Sphere 36 in Pendant` → `36 IN` is a *fix* to a
pre-existing render-time caser bug, not a P0-8 change.

**Golden stays red (0/4).** It was red before W1, `golden_set.json` is
worker-forbidden, and re-freezing is Phase 2 — after the P0 defects are closed,
so known-defective output is never enshrined as the baseline.


---

## Phase 2 — golden re-freeze (2026-09-17)

`config/golden_set.json` **v11 (4 orgs) → v12 (11 orgs)**. First freeze since
2026-07-20, and the first that can detect Sarreid overfit — V11 contained only
orgs that behave like Sarreid. `hfg`, `kal`, `ali`, `sca` were dropped from V11
rather than reviewed; `bsc`, `bmc`, `bri` were never frozen at all.

**`bsc` is now the only regression coverage of the correct-refusal path.**

Every entry was generated from a real run, not hand-edited. Each carries
`known_defects` — the design debt frozen alongside it, so the manifest
*documents* debt instead of blessing it. Phases 4–10 tick those off. Nothing in
`known_defects` is endorsed by being frozen.

```
GOLDEN SET: PASS (11/11)        # incl. prose conformance, Gate 2
pytest                          150 passed, 6 skipped
cohort_diff                     no change vs baseline
```

`_baseline/` re-captured at the same moment as the freeze, so the two agree.

**The rule from here: red means red.** *"Expected-red is accepted"* — the
2026-09-16 changelog line that let the harness rot for two months — is not
written again.
