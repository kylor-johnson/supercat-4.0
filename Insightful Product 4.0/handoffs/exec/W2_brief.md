# W2 — Phase 3: characterization tests on the renderer

> **Open a FRESH Claude Code session in `~/repos/supercat-4.0` with this prompt:**
>
> `Read "Insightful Product 4.0/handoffs/exec/W2_brief.md" and execute it. Work on branch exec/W2. Do not touch anything outside the scope list.`

**Read first:** `AUDIT_FINDINGS.md` (esp. §4, §9) · `EXECUTION_PLAN.md` (stamp protocol).

**No VPN, no Postgres, no API key.** Everything runs from `pipeline/cache/` in ~10s.
Runs must pin `--date`; `tools/cohort.conf` holds the org→date map.

```bash
cd "Insightful Product 4.0"
make check          # pytest + golden (11/11) + cohort diff — ALL GREEN today
```

---

## Why this phase exists, in one paragraph

Phases 4–8 rewrite rep identity, every signal threshold, the materiality gates
and the voice gates — across `sections.py` (1,641 lines), `step10_check.py`,
`smoke_check.py` and `md_parse.py`, **all of which have zero test coverage**.
That is not hypothetical risk: **P0-3 and P0-4 both lived in exactly that
uncovered renderer code, and both shipped to clients for months.** P0-4 put a
duplicated heading in 8 of 11 reports. Nothing caught either one. Build the net
before the refactors, not after.

## The job

Write **characterization tests** — tests that pin *current* behaviour, correct
or not, so a refactor surfaces unintended change. You are not fixing bugs.

Priority order (highest risk first):

1. **`report_render/sections.py`** — hero assembly, the `_build_hero` /
   hero-sub-paragraph branch (where P0-4 lived), callout-card triggering,
   metric-card table detection, priorities detection, collapse-section wrapping.
2. **`report_render/step10_check.py`** — every §P forbidden pattern needs a test
   that it fires on a positive case **and** one that it does not fire on its
   allow-listed context. This list is rewritten in Phase 8; it must not silently
   loosen.
3. **`report_render/md_parse.py`** — table parsing and block splitting. P0-3
   lived here. Include the lazy-continuation case: a paragraph directly abutting
   a table row.
4. **`pipeline/smoke_check.py`** — especially the §Q sensitivity-hedge gate,
   which W1 just made load-bearing at PARTIAL.
5. **`report_render/naming.py`** — display-name derivation for all 11 orgs.

## Rules

- **Pin behaviour, do not change it.** If you find a bug, write a **failing test
  marked `xfail` with a one-line reason** and report it in the evidence. Do not
  fix it — that is a later phase, and an unreviewed fix inside a test PR is how
  regressions get laundered.
- **No production-code changes**, with one exception: if a function is literally
  untestable without a seam (e.g. it reads a module-level path directly), you may
  add the seam — but call it out separately in the evidence with the reason.
- **Use the real cohort as fixtures** where practical. The 11 cached orgs are the
  best corpus available and they exercise STRONG / PARTIAL / NONE, Tier 0/1/2,
  SHIP / REDIRECT, and both the current and stale `S1` schemas.
- **`make check` must stay green.** Golden is `PASS (11/11)` as of v12 — if it
  goes red, you changed behaviour, which this phase must not do.

## DoD

- ≥70% line coverage on `sections.py` **and** `step10_check.py`
  (`pytest --cov` — add `pytest-cov` to `requirements-pipeline.txt` if needed).
- Every §P forbidden pattern has both a fires-on and a does-not-fire-on test.
- `md_parse` has a test for the lazy-continuation case that caused P0-3.
- `make check` green: pytest all-pass, `GOLDEN SET: PASS (11/11)`, cohort no-change.
- Any bug found is an `xfail` + an evidence entry, **not** a fix.
- Coverage before/after numbers pasted in the evidence.

## Scope

**In:** `tests/**`, `requirements-pipeline.txt` (test deps only),
`handoffs/exec/W2_evidence.md`, plus narrowly-justified testability seams.

**Out:** `config/golden_set.json` (reviewer-only), LIVE SQL in `foundation/**` /
`operators/**`, `pipeline/cache/**`, `outputs/*_prose_*.json` (authored client
inputs), anything outside `Insightful Product 4.0/`, and **any behaviour change**.

**Do not enable `validate_slot` on the prose-file path** — tried and backed out;
it rejects `$1` from the phrase "for every $1". That is Phase 8. See
`AUDIT_FINDINGS.md` §7.

## Evidence

`handoffs/exec/W2_evidence.md`: files added; coverage before/after per module;
every verification command with **real pasted output**; each `xfail` with its
reason; and a self-assessment against each DoD line.
