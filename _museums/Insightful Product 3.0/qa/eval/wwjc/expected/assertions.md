# wwjc — acceptance criteria

Baseline: `2026-04-17` snapshot. **Refresh `expected/` on the next clean wwjc run** for tighter parity (this snapshot predates ~2 months of data drift).

## Mode
- Report mode: **Mode 1** (Standard Intelligence Report)

## Structural gate booleans (must match; numeric evidence may drift)
| Gate | Expected |
|---|---|
| HAS_CLICKY | false |
| HAS_CART | true |
| HAS_PORTAL_ORDERS | true |
| HAS_INVENTORY | true |
| HAS_SALES_DATA | true |
| HAS_SALES_SECTION | true |
| HAS_PEER_DATA | true |
| BENCHMARK_ELIGIBLE | true |
| VM45_RENDER | true (both gates pass) |

## INCLUDE section set
- Content sections: **2, 3, 4, 5, 7, 8** → **count = 6**
- (§6 Portal SKIPPED because HAS_CLICKY=false)

## Static checks (`check_static.sh <output> 6`)
- hard-forbidden tokens = 0 (note: HAS_CLICKY=false → "Clicky"/portal-analytics must be entirely absent)
- unsubstituted `{{` = 0
- `<details class="section-collapse">` blocks = 6
- `<details>` balanced

## Cross-contamination
- Only `Wildwood`/`Chelsea House` / `wwjc`; no other org name or shortname.

## Known-acceptable drift (NOT failures)
- Numeric metrics; rep roster (22 qualifying reps at baseline); cohort membership.
