# Health V3 — Canonical Run Prompt

Reusable prompt for producing the next monthly canonical Health V3 scorecard. Hand this to any capable agent (Cursor, Codex, etc.) and it will execute the full Path B workflow: MCP-driven cache population → deterministic cache-mode operator run → independent cold-read review → CHANGELOG entry → archive of the prior canonical.

The prompt orchestrates a doc-driven workflow rather than restating logic, so the system stays in sync with `README.md` automatically. If the prompt drifts from the docs, fix the docs first and update this prompt to point at the new sections.

**When to use:** monthly cadence, or any time a fresh canonical is needed.

**Prerequisites:**

- Cursor with the `user-supercat-postgres-vpn` and `user-bigquery-vpn` MCPs enabled.
- VPN active (both MCPs require it).
- Empty target directory at `cache/$SCORE_DATE/` ready to receive 10 CSVs.

**Rough runtime:** 30–60 min cache populate, 1–2 min operator, 5–10 min cold-read review.

**Hard rule:** if anything fails (determinism break, sanity-check fail, cold-read flag), stop and report. Do not attempt to fix scoring logic in the same run — code changes require a separate version bump and review cycle.

---

## The prompt

Everything below the line is the prompt body. Copy from the line break to the end of file and hand it to the agent. Do not include this preamble.

---

You are producing the next canonical Health V3 scorecard. Read the entire prompt before starting.

## Authoritative docs

Before doing anything, read:

1. `Health V3/README.md` §"How to populate the cache" — the 10-file MCP workflow, with execution rules and sanity checks.
2. `Health V3/README.md` §"How to run" — the operator invocation.
3. `Health V3/README.md` §6.6 Determinism and Reproducibility — why the cache is immutable.
4. `Health V3/CHANGELOG.md` most recent entry — the prior canonical's SHA, distribution, and floor cohort, for delta comparison.

The operator code at `Health V3/health_operator_v3.py` is the source of truth for SQL. Do not paraphrase queries — read each loader function verbatim.

## Step 0 — Environment (once per machine)

The determinism contract is interpreter-scoped: the same cache and `--score-date`
reproduce byte-identically only under the same Python. Build the pinned venv
before the first run — see `ENVIRONMENT.md` for why and for the environment of
record.

```bash
cd "Health V3"
/usr/bin/python3 -m venv .venv --system-site-packages
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 -c "import sys,pandas,numpy; print(sys.version.split()[0], pandas.__version__, numpy.__version__)"
# expect: 3.9.6 2.3.3 2.0.2
```

`.venv/` is gitignored. Every command below assumes `.venv/bin/python3`.

---

## Step 1 — Determine the score date

Run `date -u +%F` and use that value for both:

- The cache directory name: `cache/$SCORE_DATE/`
- The `--score-date` argument

Why UTC: PG `NOW()` in the queries is UTC-anchored; aligning the cache name preserves the determinism contract (see README §6.6).

## Step 2 — Populate `cache/$SCORE_DATE/`

Follow README §"How to populate the cache" exactly. All 10 CSVs. MCPs are `user-supercat-postgres-vpn` and `user-bigquery-vpn`.

After population, run the sanity checks listed in that section: 10 files present, all readable by `pandas.read_csv`, row counts within ±50% of the prior cache (compare against the most recent `cache/` directory or the deltas in the latest CHANGELOG entry).

## Step 3 — Run the operator (cache mode)

Follow README §"How to run" exactly, with `--score-date` and `--cache-dir` matching `$SCORE_DATE`.

Then run a second pass with the same arguments and SHA-256 both output CSVs. They MUST be byte-identical. If they aren't, stop and report — do not treat the run as canonical. (See README §6.6 for the determinism contract.)

## Step 4 — Independent cold-read review

Spawn a separate agent (Ask mode is fine) with a small set of spot-checks:

- Distribution table (band counts) vs prior canonical.
- Behavioral floor cohort (`org_shortname` list and count).
- Ghost cohort.
- 5–10 specific orgs spanning all bands, verifying score + narrative consistency.
- Any org that crossed a band boundary, with a one-line driver explanation.

The reviewer must work from the CSV alone, without access to your run report.

## Step 5 — Document and archive

Once the cold-read clears:

1. Add a new entry to `CHANGELOG.md` at the top, following the V3.2.2 entry's structure (the canonical-refresh exemplar — V3.2.3 and V3.2.4 are narrative-only patches and not the right template): canonical SHA, distribution table with delta vs prior, band changes with drivers, composite shifts ≥5pts with drivers, cache deltas, validation summary.
2. Bump the "Version" and "Date" in **both** `README.md` and `METHODOLOGY.md` to match — Invariant 1 checks the two against the top CHANGELOG heading.
3. Archive the prior canonical:
   - `mv runs/{prior-date}/ _archive/runs/v{prior-version}_{prior-date}/`
   - `mv cache/{prior-date}/ _archive/cache/v{prior-version}_{prior-date}/`
4. Verify SHA pre/post archive move (no corruption).
5. Sweep for stale path references in live (non-archive) docs:
   ```
   grep -rn "runs/{prior-date}\|cache/{prior-date}" --exclude-dir=_archive Health\ V3/
   ```
   Any hits in live docs (CHANGELOG entries describing the archive move are expected and fine) should be patched to point at the new archive location.
6. Run `.venv/bin/python3 check_consistency.py` from `Health V3/`. All 8 invariants must pass. If any fail, stop and resolve before declaring the canonical shipped — typical fix is updating the top CHANGELOG entry with the new SHA or regenerating the dashboard against the new canonical.

## Hard constraints

- **Operator code MUST NOT be modified.** This is a routine canonical refresh, not a code change. Any code edit requires a separate version bump and review cycle.
- **The cache is immutable once populated.** To re-run with fresher data, populate a NEW dated cache directory.
- **Every numeric claim in the new CHANGELOG entry must be verified against the actual CSV** before committing the entry. Use `pandas` to recompute distributions, behavioral floor cohort, band changes, and composite shifts directly from the canonical CSV — do not trust your run report.
- **If anything fails, stop and report.** Do not attempt to fix scoring logic, narrative wording, or anything else inside the same run.
