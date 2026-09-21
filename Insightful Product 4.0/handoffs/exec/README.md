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

---

## Remaining work and who does it (2026-09-21)

State at this point: 26 of 111 library queries wired, `make check` green
(895 tests, `GOLDEN SET: PASS (11/11)`, golden v24), 43 commits on `main`,
all 11 cohort orgs SHIP/REDIRECT.

| Brief | Phase | Needs VPN | Priority |
|---|---|---|---|
| `W11_brief.md` | 11 — clean company repo | no | **highest — this is the actual goal** |
| `W7_brief.md` | 9 — remaining 7 backlog queries | yes | medium, diminishing returns |
| — | 8 — voice gates | no | low, mechanical |
| — | 10 — thin data (da/sca/bsc ~1,100 words) | no | low, design-heavy |
| — | 12 — doctrine reconciliation | no | do last, after code settles |

**Read `TRAPS.md` before any of them.** It records sixteen failure modes this
programme already paid for, including four that shipped wrong numbers or
template text into client reports. None of it is inferable from the code.

### Review protocol (unchanged)

The reviewer re-runs; the reviewer never reads claims. `make check` exit 0,
`cohort_diff.sh --full` read line by line, and the worker's verification
aggregates re-executed against the database. STAMP / REWORK / REJECT logged
in `STAMPS.md` with the evidence that decided it.
