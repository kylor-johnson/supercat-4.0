# handoffs/exec — worker briefs and evidence

One task = one brief + one branch + one evidence file.

```
<TASK-ID>_brief.md      written by the reviewer BEFORE work starts
<TASK-ID>_evidence.md   written by the worker BEFORE review
STAMPS.md               append-only verdict log
```

A brief is **self-contained** — a worker session has none of the audit context.
It states: problem, evidence (file:line), files in scope, files explicitly **out**
of scope, Definition of Done, and the exact verification commands.

Evidence must paste **real command output**, never claims. Minimum:

```bash
make check                     # pytest + golden + cohort diff
./tools/cohort_diff.sh --full  # per-org visible-text delta
```

Plus one line of justification per changed golden checksum.

**A worker may never** re-stamp the golden set, edit `config/golden_set.json`,
change LIVE SQL bodies, or touch files outside its scope list.
