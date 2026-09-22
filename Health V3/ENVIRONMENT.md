# Health V3 — environment of record

The scoring math is deterministic **given an interpreter**. It is not
deterministic across interpreters. Both must be recorded with every canonical.

## Current environment of record

| Component | Version | Notes |
|---|---|---|
| Python | 3.9.6 | `/usr/bin/python3` (macOS system) |
| pandas | 2.3.3 | |
| numpy | 2.0.2 | |

Canonicals produced under this environment:

| Run | Engine / weights | SHA-256 | Status |
|---|---|---|---|
| 2026-09-21 | V3.6.0, equal | `2850025e…` | **the live canonical** |
| 2026-05-13 | V3.5.1, equal | `a797e959…` | prior canonical, demoted to `runs/historical/` |
| 2026-05-13 | V3.5.0, equal | `a5d8cb28…` | superseded |
| 2026-05-13 | V3.4.1, equal (28-col) | `6a2f1d9f…` | superseded. Also the output of `_archive/health_operator_v3.2.x_unweighted.py` on this interpreter — one SHA, two roles |
| 2026-09-21 | V3.4.1 / V3.4.0 | `592c1bdb…` / `6dc304ea…` | superseded; `6dc304ea…` was never committed and is unrecoverable |
| 2026-05-13 | `--weights v330` | `e98f11a4…` | the v330 *scheme* still reproduces all 104 V3.3.2 composites and bands. **`e34552ab…` is NOT reproducible here** — it predates the 30-column schema and needs a V3.4.x checkout |

> **This table goes stale on every version bump and has done so twice.** At V3.5.0
> all three of its rows were wrong, in the one file whose purpose is preventing SHA
> confusion. `check_consistency.py` Invariant 9 now pins the live-canonical row
> against the actual file, so the failure mode is caught rather than discovered.

## Setup

```bash
cd "Health V3"
/usr/bin/python3 -m venv .venv --system-site-packages
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 -c "import pandas,numpy,sys; print(sys.version, pandas.__version__, numpy.__version__)"
```

Expect `3.9.6 … 2.3.3 2.0.2`. If any differ, **stop** — re-run the historical
months and republish their SHAs before treating a new run as canonical.

## The cross-interpreter drift, documented

`runs/_engine_baseline_v3.2.13/` holds the V3.2.13 canonical at SHA
`b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`.

Re-running the **original** unweighted operator
(`_archive/health_operator_v3.2.x_unweighted.py`) against its own immutable
cache (`cache/2026-05-13/`) under the current interpreter yields
`6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff`.

Three composites move by 0.1 — `all` 61.4→61.3, `bsc` 77.2→77.1,
`gblx` 69.2→69.1. Zero band changes, zero narrative changes. The cause is
float summation order at a `.x5` rounding boundary, not a code change.

**Implication for §6.6:** the determinism contract is
*same cache + same `--score-date` + same interpreter* → byte-identical.
A SHA without its interpreter is not a reproducibility claim.

## The cross-machine match, confirmed

Confirmed 2026-09-22 on a second macOS machine — fresh `git clone`, fresh
`.venv`, same interpreter triple (`3.9.6 / 2.3.3 / 2.0.2`):

| Check | Result |
|---|---|
| `runs/2026-09-21/` rescored from `cache/2026-09-21/` | `2850025e…` — byte-identical |
| `check_consistency.py` | 9 pass / 0 fail |
| `trigger_engine_v1.py` | 155 triggers, byte-identical to `trigger_reports/` |

This is the other half of the contract stated above. The drift section records a
*different* interpreter producing a *different* SHA; this records the *same*
interpreter on different hardware producing the *same* one. Until now the
determinism claim had only ever been exercised by re-running on the machine that
produced the canonical — which cannot distinguish "deterministic" from "stable on
one box."

## Prior environment (broken, do not restore)

The `.venv` that produced the V3.2.x and V3.3.x canonicals targeted a Homebrew
`python@3.14` that no longer exists on this machine. It was already recorded as
broken in `runs/cohort/2026-08-26/run_metadata.md`. That interpreter is the one
under which `b48e3a5f…` is exactly reproducible; it is not recoverable here.
