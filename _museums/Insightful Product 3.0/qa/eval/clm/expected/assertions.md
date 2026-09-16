# clm — acceptance criteria

Baseline: fresh GREEN reproduction `2026-06-12` (Track A verification run).

## Mode
- Report mode: **Mode 1** (Standard Intelligence Report)

## Structural gate booleans (must match; numeric evidence may drift)
| Gate | Expected |
|---|---|
| HAS_CLICKY | true |
| HAS_CART | false |
| HAS_PORTAL_ORDERS | true |
| HAS_INVENTORY | true |
| HAS_SALES_DATA | true |
| HAS_SALES_SECTION | true |
| HAS_PEER_DATA | true |
| BENCHMARK_ELIGIBLE | true |
| VM45_RENDER | false (Gate 2 fail — eCat GMV < 5% of all-channel) |

## INCLUDE section set
- Content sections §2–§8: **2, 3, 4, 5, 6, 7, 8** → **count = 7**
- (§6 Portal included because HAS_CLICKY=true)

## Static checks (`check_static.sh <output> 7`)
- hard-forbidden tokens = 0
- unsubstituted `{{` = 0
- `<details class="section-collapse">` blocks = 7
- `<details>` balanced

## Cross-contamination
- Only `Crystorama` / `clm`; no other org name or shortname in delivered HTML.

## Known-acceptable drift (NOT failures)
- Numeric metrics (orders, GMV, user counts, inventory rows).
- `new_item=true` product count (prod catalog re-flags; was 44 in Apr, 929 on 2026-06-12).
- Portal traffic trend label (rolling window moves).
- Quiet-rep / cohort membership (seasonal).
