# W2 evidence — Phase 3, characterization tests on the renderer

Branch `exec/W2`, off `main` (`aa307ed`). Worker session, 2026-09-18.
Brief: [`W2_brief.md`](W2_brief.md). Everything below ran offline from
`pipeline/cache/` — no VPN, no Postgres, no `ANTHROPIC_API_KEY`. Full suite is
~1.5s; `make check` is ~25s.

**Headline:** 675 new tests across 7 files. Coverage on the two DoD modules went
`sections.py` **0% → 99%** and `step10_check.py` **13% → 95%** (DoD floor: 70%).
All 83 §P forbidden patterns have a fires-on and a does-not-fire-on test.
**Zero production-code changes** — no testability seam was needed. `make check`
green, `GOLDEN SET: PASS (11/11)`, cohort no-change. Six latent defects found;
all six are `xfail`, none fixed.

---

## Files added / changed

| File | Kind | Tests |
|---|---|---|
| `tests/test_sections_summary.py` | new | 100 + 2 xfail — §1 hero, metric cards, CEO callouts, priorities |
| `tests/test_sections_render.py` | new | 116 + 1 xfail — §2-§11, Gate-STOP, tables, row tints, cell cleanup |
| `tests/test_step10_forbidden_vocab.py` | new | 203 + 2 xfail — the 83-pattern §P matrix + the six §P.2 allow-lists |
| `tests/test_step10_checks.py` | new | 50 + 1 xfail — checks [8] [9] [11] [12] + the CLI |
| `tests/test_md_parse_characterization.py` | new | 67 + 1 xfail — parsing, classification, footers, **P0-3 lazy continuation** |
| `tests/test_smoke_check_characterization.py` | new | 86 — §Q / §R / §S, section profiles, topline parity, CLI |
| `tests/test_naming_characterization.py` | new | 53 — display names + filenames for all 11 orgs |
| `requirements-pipeline.txt` | edit | `pytest-cov>=5.0` (test dep only) |
| `handoffs/exec/W2_evidence.md` | new | this file |

**No production code was changed.** The brief allowed a narrowly-justified
testability seam; none was required. Every target function is importable and
pure enough to drive directly, and the two path-reading functions
(`step10_check.run_checks`, `smoke_check.smoke`) already take `Path` arguments,
so `tmp_path` is the seam.

**Nothing outside the scope list was touched.** `git diff --stat main...exec/W2`
is 9 files: 7 new test files, `requirements-pipeline.txt`, this evidence file.

---

## Coverage before / after

Both runs are the same command against the same venv; "before" simply ignores
the seven new files.

### Before

```
$ .venv-renderer/bin/python -m pytest tests/ -q \
    --ignore=tests/test_naming_characterization.py \
    --ignore=tests/test_md_parse_characterization.py \
    --ignore=tests/test_smoke_check_characterization.py \
    --ignore=tests/test_step10_forbidden_vocab.py \
    --ignore=tests/test_step10_checks.py \
    --ignore=tests/test_sections_summary.py \
    --ignore=tests/test_sections_render.py \
    --cov=report_render --cov=pipeline.smoke_check --cov-report=term

================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.2-final-0 _______________

Name                             Stmts   Miss  Cover
----------------------------------------------------
pipeline/smoke_check.py            145    106    27%
report_render/__init__.py            1      0   100%
report_render/html_renderer.py     172    172     0%
report_render/md_parse.py           96     96     0%
report_render/md_render.py          15     15     0%
report_render/naming.py             26      7    73%
report_render/sections.py          798    798     0%
report_render/step10_check.py      209    182    13%
----------------------------------------------------
TOTAL                             1462   1376     6%
150 passed, 6 skipped in 0.99s
```

### After

```
$ .venv-renderer/bin/python -m pytest tests/ -q \
    --cov=report_render --cov=pipeline.smoke_check --cov-report=term

================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.2-final-0 _______________

Name                             Stmts   Miss  Cover
----------------------------------------------------
pipeline/smoke_check.py            145      4    97%
report_render/__init__.py            1      0   100%
report_render/html_renderer.py     172    172     0%
report_render/md_parse.py           96      0   100%
report_render/md_render.py          15      0   100%
report_render/naming.py             26      0   100%
report_render/sections.py          798     11    99%
report_render/step10_check.py      209     10    95%
----------------------------------------------------
TOTAL                             1462    197    87%
825 passed, 6 skipped, 7 xfailed in 1.67s
```

| Module | Before | After | DoD |
|---|---|---|---|
| `report_render/sections.py` | **0%** | **99%** | ≥70% ✅ |
| `report_render/step10_check.py` | **13%** | **95%** | ≥70% ✅ |
| `report_render/md_parse.py` | 0% | 100% | — |
| `report_render/naming.py` | 73% | 100% | — |
| `pipeline/smoke_check.py` | 27% | 97% | — |
| `report_render/md_render.py` | 0% | 100% | — |

`report_render/html_renderer.py` stays at 0% — it is not on the brief's priority
list and it is the one module whose behavior Phase 4 (T1-3) rewrites wholesale.
The golden set already pins it end to end.

Residual misses are defensive branches with no reachable input from the cohort
(`sections.py` 270-272, 603, 892-893, 1114, 1198, 1242, 1250, 1254 —
list-shape fallbacks; `step10_check.py` 148, 155-156, 211, 215, 230-231,
284-285 — `AttributeError` guards and the `__main__` block).

---

## `make check` — green

```
$ make check
.venv-renderer/bin/python -m pytest tests/ -q
825 passed, 6 skipped, 7 xfailed in 1.47s
./regression.sh --verify

══════════════════════════════════════════════════════════════
  GOLDEN SET: PASS (11/11)
./tools/cohort_diff.sh

ORG      TEXT       CORE-SHA  OUTCOME    NOTE
----------------------------------------------------------------------
sarreid  same       same      SHIP
cci      same       same      SHIP
da       same       same      SHIP
clc      same       same      SHIP
hfg      same       same      SHIP
kal      same       same      SHIP
ali      same       same      SHIP
sca      same       same      SHIP
bsc      same       same      REDIRECT
bmc      same       same      SHIP
bri      same       same      SHIP
----------------------------------------------------------------------
COHORT: no change vs baseline

$ echo $?
0
```

Cohort delta: **none, on any org.** Golden-core checksum delta: **none.** That
is the expected result — this phase adds tests and changes no behavior, so
there is no per-org justification to write.

---

## §P coverage — 83 patterns, 166 tests

```
$ .venv-renderer/bin/python -m pytest tests/test_step10_forbidden_vocab.py -q
203 passed, 2 xfailed in 0.28s
```

The matrix lives in one `CASES` table of `(regex source, fires-on prose,
does-not-fire-on prose)`, driving two parametrized tests. A third test,
`test_every_forbidden_pattern_is_covered`, asserts

```python
assert {p for p, _ in _FORBIDDEN_PATTERNS} == {p for p, _, _ in CASES}
assert len(CASES) == len(_FORBIDDEN_PATTERNS) == 83
```

so Phase 8 cannot add, drop or reword a pattern without the suite saying so.

A does-not-fire-on case asserts only that *that* pattern stays quiet (the prose
may legitimately trip a different rule). On top of that, the six §P.2
allow-listed contexts get whole-sweep-clean assertions:

| allow-list | covered by |
|---|---|
| `yoy-acronym` | number adjacency, `<th>` ancestor, and the two xfails below |
| `ecat` | all 5 allowed section ids clean; 6 disallowed ids fire |
| `cohort` | `buyer cohort` / `design cohort` clean; bare `cohort` fires |
| `supercat` | `About SuperCat` clean; elsewhere fires |
| `product` | `CEO Brief` / `Customer Intelligence` window clean |
| `version` | bare `v4.0` clean; `product v4.0` fires; `$15.64M` never reads as a version |

Plus the three document-level skips: Gate-STOP relaxation, `#appendix`, and
`.footer-ledger`.

---

## P0-3 — the lazy-continuation case

`tests/test_md_parse_characterization.py` pins all four states of the shape that
produced the client-visible `---` cell:

1. **blank lines intact** (what the Phase-1 template fix produces) — three
   blocks, two tables, no `---`.
2. **one blank line lost** — the paragraph is swallowed as a table *cell*; the
   second table still survives.
3. **both blank lines lost** (the original `{%-` chomp) — `_split_paragraphs`
   returns **one** block, `_parse_md_table` returns `None`, the caller falls
   back to the raw markdown-it render, and the two tables collapse into one with
   5 body rows.
4. **xfail** — the renderer still emits `<td>---</td>` for state 3.

That last one is the finding: **P0-3 was fixed in the Jinja templates only.** The
renderer has no defense, so any future template that loses a blank line
reproduces the defect. Reported, not fixed (Phase 4+).

---

## Findings — six latent defects, all `xfail`, none fixed

Every one is a **strict** xfail: if a later phase fixes it, the xfail turns
XPASS and the suite goes red, which is the signal the fix landed.

```
$ .venv-renderer/bin/python -m pytest tests/ -q -rx
XFAIL tests/test_md_parse_characterization.py::test_renderer_should_not_leak_a_separator_row_as_a_cell
XFAIL tests/test_step10_forbidden_vocab.py::test_a_bare_full_stop_should_not_satisfy_the_yoy_proximity_test
XFAIL tests/test_step10_forbidden_vocab.py::test_yoy_is_allowed_when_the_number_is_in_the_surrounding_block
XFAIL tests/test_step10_checks.py::test_check_9_should_catch_a_verbatim_duplicate
XFAIL tests/test_sections_summary.py::test_an_unbolded_hero_should_keep_the_whole_dollar_figure
XFAIL tests/test_sections_summary.py::test_a_list_directly_after_the_hero_should_still_reach_its_detector
XFAIL tests/test_sections_render.py::test_the_render_time_titlecaser_diverges_from_gather
825 passed, 6 skipped, 7 xfailed in 1.43s
```

### P0-3 residual — the renderer still leaks `---`
`report_render/md_parse.py` / `sections.py:_split_paragraphs`. See above. Owner
for the fix: Phase 4+.

### F-1 — §P's number-proximity test accepts a full stop
`step10_check._yoy_allowed:143` — `re.search(r"[\d\.%]", window)`. The `.` is
inside the character class, so it matches a literal period. Any sentence-ending
`YoY` / `MoM` / `QoQ` therefore passes:

```
_violations("The YoY view is noisy")   →  1 violation
_violations("The YoY view is noisy.")  →  0 violations
```

The rule is effectively unenforced in prose. **Phase 8.**

### F-2 — the yoy allow-list cannot see past the immediate parent
Same function, lines 145-148. The docstring says the check allows
`"+82.5% <strong>YoY</strong>"`, but `parent_text` is the `<strong>`, whose text
is just `YoY`. The documented shape fires. (The `<th>` ancestor walk on
lines 149-157 does climb the tree — only the number-proximity branch does not.)
**Phase 8.**

### F-3 — check [9] cannot see a verbatim duplicate
`step10_check._check_phrase_echo:380-381` requires **≥2 distinct fragment
texts**, so the most obvious echo — byte-identical copy in two places — reports
nothing. Only partially-overlapping fragments are caught. Given that **P0-4 was a
duplicated heading**, this is the check that should have caught it and could not.
**Phase 8.**

### F-4 — an unbolded hero truncates its own dollar figure
`sections._build_hero:439` — `headline_md = lead_match.group(1) if lead_match
else first_para.split(".")[0]`. The fallback splits on the first `.`, which is
inside the number: `$9.9M invoiced this year.` → `<div class="hero-num">$9</div>`.
No current cohort org renders an unbolded hero paragraph, so this is latent, not
shipped. **Phase 4 (T1-3) rewrites this function.**

### F-5 — a list directly after the hero is swallowed by the hero sub
`sections.render_summary:226-232`. The hero-sub branch excludes a table and the
two lead-ins (the P0-4 guard) but **not a list**. A callout or priority list that
follows the hero with no lead-in — the shape the sanitizer produces when it
collapses the lead — is absorbed as hero prose, and the three CEO cards or the
priority rows never render. This is the same class of bug as P0-4, one branch
over. **Phase 4 (T1-3).**

### F-6 — two title-casers, two answers
`sections._smart_titlecase:107` keeps a leading 3-letter ALL-CAPS word as an
initialism, so `THE SWAN'S NEST INC` → `THE Swan's Nest Inc`, while
`gather.normalize_account_name` (which AUDIT §9 records as fixing exactly this on
sarreid) returns `The Swan's Nest Inc`. Whichever path a name arrives by decides
how it is cased. Not client-visible today — the data layer normalizes first — but
it is a second source of truth for display names. **Phase 6.**

---

## Test-design notes for the reviewer

**Hermetic by default.** `outputs/` and `pipeline/cache/*/` are gitignored
(client data), so every test that reads them calls `pytest.skip` when absent —
the convention `test_deterministic_fallback.py` already set. 6 skips in this
tree are the pre-existing `test_product_descriptions.py` ones; the new
cohort-fixture tests find their files here and pass. On a clean checkout they
skip rather than fail. `profiles/*.md` and `tools/cohort.conf` **are** tracked,
so `test_naming_characterization.py` covers all 11 orgs hermetically.

**Real cohort used where it earns its place.** Cohort fixtures cover the shapes
synthetic MD cannot fake: the invoiced vs behavior-only layouts (sarreid vs da),
the Gate-STOP filename carrying a Mode-1 body (bsc), and four shipped HTML files
run end to end through all five Step-10 checks. Everything else is synthetic,
because a characterization test that depends on a client's exact revenue figure
is a test that breaks when the cache is re-populated.

**Cohort drift guards.** `test_cohort_and_expectations_cover_the_same_orgs` fails
if `tools/cohort.conf` gains an org without a display-name expectation;
`test_every_forbidden_pattern_is_covered` fails if `_FORBIDDEN_PATTERNS` changes
shape. Both exist so the suite cannot go quietly vacuous.

**Pinned, not endorsed.** Every file's module docstring says so. Several tests
assert behavior that is plainly wrong (`THE Swan's Nest`, `$9`, the swallowed
list). They are there so Phases 4-8 produce a loud, readable diff — the same
argument Phase 2 made for freezing HFG in its current state.

---

## Self-assessment against the DoD

| DoD line | Status | Evidence |
|---|---|---|
| ≥70% line coverage on `sections.py` **and** `step10_check.py` | ✅ | 99% and 95%; before/after tables above |
| `pytest-cov` added to `requirements-pipeline.txt` if needed | ✅ | `pytest-cov>=5.0`, test dep only |
| Every §P forbidden pattern has both a fires-on and a does-not-fire-on test | ✅ | 83 patterns × 2, plus a completeness guard that fails if the list changes |
| `md_parse` has a test for the lazy-continuation case that caused P0-3 | ✅ | four tests covering all four blank-line states |
| `make check` green: pytest all-pass, `GOLDEN SET: PASS (11/11)`, cohort no-change | ✅ | full output pasted above, exit 0 |
| Any bug found is an `xfail` + an evidence entry, **not** a fix | ✅ | 6 findings, 7 strict xfails, zero production-code changes |
| Coverage before/after numbers pasted in the evidence | ✅ | above |
| Scope respected — `tests/**`, `requirements-pipeline.txt`, this file | ✅ | 9 files in `git diff --stat main...exec/W2`; no seam was needed |
| `validate_slot` NOT enabled on the prose-file path | ✅ | untouched; `tests/test_slot_validator.py` unchanged |

**One thing for the reviewer:** `pytest --cov` drops a `.coverage` data file in
the project root, and `.gitignore` does not yet cover it. `.gitignore` is not on
this brief's scope list, so I deleted the file rather than edit it — a one-line
`.coverage` entry is a reviewer call.

**Not done, deliberately:** `html_renderer.py` has no unit coverage. It is not on
the brief's priority list, it is the module T1-3 rewrites, and the golden set
already pins its output byte for byte. Flagging it rather than silently scoping
it in.
