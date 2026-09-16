# pf — acceptance criteria

Baseline: derived from the most recent clean run.

## Mode
- Report mode: **Mode 1** (Standard Intelligence Report)

## Structural gate booleans (must match; numeric evidence may drift)
| Gate | Expected |
|------|----------|
| HAS_CLICKY | false |
| HAS_CART | false |
| HAS_PORTAL_ORDERS | false |
| HAS_INVENTORY | true |
| HAS_SALES_DATA | false |
| HAS_SALES_SECTION | true |
| HAS_PEER_DATA | true |
| BENCHMARK_ELIGIBLE | true |
| VM45_RENDER | false |
| PORTAL_REP_DATA_PRESENT | false |
| PORTAL_CUSTOMER_DATA_PRESENT | false |

## INCLUDE section set
- Content sections §2–§8: **2, 3, 4, 5, 7, 8** → **count = 6**
- (§6 Portal excluded because HAS_CLICKY=false)

## Static checks (`check_static.sh <output> 6`)
- hard-forbidden tokens = 0
- unsubstituted `{{` = 0
- `<details class="section-collapse">` blocks = 6
- `<details>` balanced

## Graceful degradation assertions (iPad-only path)
- §2 must NOT include Q-51 subsection (PORTAL_REP_DATA_PRESENT=false)
- §3 must NOT include Q-52 penetration subsection (PORTAL_CUSTOMER_DATA_PRESENT=false)
- §3 must NOT include Q-53 unactivated accounts subsection
- §5 must NOT include "total business" or "all-channel" language (HAS_PORTAL_ORDERS=false)
- §5 must NOT include capture rate subsection (VM45_RENDER=false)
- §5 must NOT include Q-55 displacement subsection
- No "ERP" in delivered HTML
- Confidence tiers: §2 PARTIAL or STRONG (no ERP), §3 PARTIAL, §5 PARTIAL

## Cross-contamination
- Only `Palecek` / `pf`; no other org name or shortname in delivered HTML.

## Known-acceptable drift (NOT failures)
- Numeric metrics (orders, GMV, user counts).
- Rep roster composition (seasonal shifts, new hires).
- Peer benchmark standing (peer CSV refresh cycle).
