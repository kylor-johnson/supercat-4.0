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

| Run | Weights | SHA-256 |
|---|---|---|
| 2026-05-13 | equal (default) | `6a2f1d9f…` — **the live canonical** |
| 2026-09-21 | equal (default) | `6dc304ea…` (V3.4.0) / see CHANGELOG for the V3.4.1 rescore |
| 2026-05-13 | `--weights v330` | `e34552ab…` — the retired V3.3.x canonical, still reproducible here |

> Corrected 2026-09-21. This line previously named `e34552ab… --weights v330`
> as *the* canonical for this environment. That was written before the V3.4.0
> weight flip and never updated — it is reproducible here, but it is not the
> live canonical, which is exactly the confusion this file exists to prevent.

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

## Prior environment (broken, do not restore)

The `.venv` that produced the V3.2.x and V3.3.x canonicals targeted a Homebrew
`python@3.14` that no longer exists on this machine. It was already recorded as
broken in `runs/cohort/2026-08-26/run_metadata.md`. That interpreter is the one
under which `b48e3a5f…` is exactly reproducible; it is not recoverable here.
