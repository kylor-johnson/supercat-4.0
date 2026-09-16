# Health V3 — Folder Audit Prompt

> **What this is:** A copy-paste prompt for an agent to audit the entire Health V3 folder and operator code for complexity, drift, redundancy, stale references, and operationalization risk. Run this before any major version bump or when the system feels "too heavy."

---

## The prompt

Everything below is the prompt body. Copy from this line to the end of the file and hand it to the agent.

---

You are auditing the Health V3 folder and operator for complexity, drift risk, and redundancy. This is a read-only audit — you will produce a structured report. Do not make any changes. Read this entire prompt before starting.

## What you are auditing

The system lives at `Health V3/`. The goal of the audit is to answer one question honestly: **Is this system simple and stable enough that a new person could run it monthly without introducing drift or hallucinations?**

You are looking for three categories of problems:

1. **Drift risk** — places where inconsistency between files could cause an agent or human to make a wrong decision or produce incorrect output
2. **Complexity** — code or documentation that is more complex than the problem requires; things that could be simplified or eliminated without losing capability
3. **Cruft** — stale content, dead code, version references that no longer apply, redundant files, or documentation that no longer matches reality

---

## Audit targets

Work through each target below in order. For each, apply the relevant checks and record findings.

---

### 1. File inventory audit

List every file and folder in `Health V3/` (recursive). For each file, state:
- What it is for (one sentence)
- Whether it is **active** (needed for current operation), **reference** (useful context but not required to run), or **cruft** (can be deleted or archived)
- Any red flags

Files to pay particular attention to:
- Any `.md` file that references a version number (V3.2.0, V3.2.1, V3.2.2, etc.) — flag any that are stale relative to current version V3.3.2
- Any prompt files (`RUN_PROMPT.md`, `DASHBOARD_POLISH_PROMPT.md`, `FRESH_RUN_GUIDE.md`) — confirm they are internally consistent with each other and with the operator
- `roadmap/outcomes.csv` — flag if it is still empty/header-only; it is inert until populated
- `_archive/` contents — confirm they are genuinely archived and not referenced by active files

---

### 2. Cross-file consistency check

Read these four files in full and cross-check them against each other:

- `README.md`
- `METHODOLOGY.md`
- `CHANGELOG.md`
- `RUN_PROMPT.md`

For each inconsistency found, report:
- File A says: [exact quote]
- File B says: [exact quote]
- Verdict: which is correct, or are both stale?

Specific things to check:
- Version numbers: do all four agree on the current version (V3.3.2)?
- Canonical SHA: does every file that mentions a SHA agree on `e34552abe2232c630b088465a067c77a39d598cd6979e912717626598edafce9`?
- Column names: the operator writes the canonical CSV (28 cols, all fields) and the formatted CSV (20 cols, executive subset in stakeholder order). Both files use the same column names. Confirm the canonical header matches what README.md §6 documents and the formatted header matches the _fmt_cols list at the bottom of main() in health_operator_v3.py.
- Band count: does every file that lists health bands list exactly 5 (Thriving, Healthy, Watch, At Risk, Critical)?
- Floor logic: do all files describe the behavioral floor consistently — composite capped at 40 when `engagement_score < 55 AND value_delivery_score < 40`?
- `exec_narrative`: confirm this field is mentioned nowhere in active files. It was removed in V3.2.4. Any mention is stale.

---

### 3. Operator code audit (`health_operator_v3.py`)

Read the full operator file. Check for:

**Dead code:**
- Any function that is defined but never called
- Any import that is unused
- Any commented-out block that is more than 5 lines (flag for removal consideration)
- Any variable assigned but never read

**Hardcoded values that should be parameters:**
- Any date, threshold, weight, or file path hardcoded in the function body rather than a named constant or argument
- If found, state: where it is, what the current value is, and what the risk of it drifting is

**Drift-prone logic:**
- Any place where the scoring output could differ between runs with identical inputs (non-determinism)
- Any place where a narrative is constructed using a variable that could change meaning between versions (e.g., a threshold constant that's used in both scoring logic AND narrative text — if the threshold changes for scoring but not for the narrative copy, the narrative will lie)

**Narrative engine:**
- Read all composite narrative template strings. For each shape, confirm: does the narrative text match what the shape is actually detecting in the data? Flag any where the template says X but the condition checks Y.
- Flag any shape where two different data profiles would produce identical output text (these are ambiguity bugs)

**Complexity assessment:**
- How many lines is the operator? How many functions? How many distinct scoring paths?
- State honestly: is any part of this over-engineered for 104 accounts? What could be simplified?

---

### 4. Dashboard HTML audit (`dashboards/health_dashboard_{date}.html`)

You do not need to read the full HTML. Use targeted searches.

Check for:
- Any hardcoded count, SHA, or date that should be computed from `DATA` at render time
- Any reference to `exec_narrative` (should not exist as of V3.2.4)
- Any reference to `composite_narrative` going through `translateNarrative()` (should not — as of V3.2.4, composite_narrative is rendered raw)
- Any version string — confirm it reads V3.3.2
- Any external network requests (script tags, link tags, img tags pointing to external URLs)

---

### 5. Prompt file operationalization check

For each prompt file (`RUN_PROMPT.md`, `DASHBOARD_POLISH_PROMPT.md`, `FRESH_RUN_GUIDE.md`), answer:

1. **Can a new agent follow this prompt without reading any other file?** If not, what context is missing?
2. **Are there any steps that require judgment calls not defined in the prompt?** (e.g., "populate the cache" without specifying the exact SQL queries)
3. **Are there any steps that are ambiguous about which tool to use?** (e.g., MCP vs. direct shell command)
4. **Does the prompt contain any instructions that contradict the current operator behavior?**

For `RUN_PROMPT.md` specifically: read the embedded SQL queries. For each query, state whether you can verify (from operator source or README) that the query maps to the correct cache file.

---

### 6. End-to-end drift risk assessment

Having read all of the above, answer these questions directly:

1. **How many distinct files does an agent need to read to successfully run a fresh monthly scorecard end-to-end?** List them.
2. **What is the most likely single point of failure for a future run?** Be specific.
3. **What is the most likely source of a hallucinated or incorrect narrative?** Be specific.
4. **Is there any part of the system where a version bump (changing a threshold, adding a column, renaming a field) would NOT automatically propagate to all dependent files?** List each gap.
5. **Overall verdict:** On a scale of 1–5 (1 = runs cleanly, 5 = will break or drift within 2 months), what is your operationalization score? Justify with the 2–3 highest-risk issues found.

---

## Report format

Produce the report in this structure:

```
## File Inventory
[table: file, status, notes]

## Cross-File Inconsistencies
[numbered list of findings, or "None found"]

## Operator Code Issues
[subsections: Dead Code / Hardcoded Values / Drift-Prone Logic / Narrative Engine / Complexity]

## Dashboard Issues
[bulleted list, or "None found"]

## Prompt File Issues
[per-file findings]

## End-to-End Drift Risk
[answers to the 6 questions above]

## Recommended Actions (priority order)
[numbered list: what to fix first, what can wait, what can be deleted]
```

Be blunt. This system is used to make decisions about customer relationships. If something is fragile, say so clearly.
