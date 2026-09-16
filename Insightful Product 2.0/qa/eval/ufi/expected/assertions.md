# ufi — acceptance criteria

Baseline: derived from the most recent clean run.

## Mode
- Report mode: **Mode 1** (Standard Intelligence Report)

## Structural gate booleans (must match; numeric evidence may drift)
| Gate | Expected |
|------|----------|
| HAS_CLICKY | false |
| HAS_CART | false |
| HAS_PORTAL_ORDERS | true |
| HAS_INVENTORY | true |
| HAS_SALES_DATA | true |
| HAS_SALES_SECTION | true |
| HAS_PEER_DATA | true |
| BENCHMARK_ELIGIBLE | true |
| VM45_RENDER | true |
| MIXPANEL_USER_DATA_PRESENT | true |
| PORTAL_REP_DATA_PRESENT | true |
| PORTAL_CUSTOMER_DATA_PRESENT | true |

## INCLUDE section set
- Content sections §2–§8: **2, 3, 4, 5, 7, 8** → **count = 6**
- (§6 Portal excluded because HAS_CLICKY=false)

## Static checks (`check_static.sh <output> 6`)
- hard-forbidden tokens = 0
- unsubstituted `{{` = 0
- `<details class="section-collapse">` blocks = 6
- `<details>` balanced

## ERP enrichment assertions
- §2 must include Q-51 subsection (PORTAL_REP_DATA_PRESENT=true)
- §3 must include Q-52 penetration subsection (PORTAL_CUSTOMER_DATA_PRESENT=true)
- §3 must include Q-53 unactivated accounts subsection
- §3 must include Q-54 geographic enrichment columns
- §5 must include Q-52 enrichment on top-buyer table

## Elite insight assertions
- §3 must include Q-14b deceleration alert (HAS_PORTAL_ORDERS=true)
- §4 must include Q-59 fill rate subsection (HAS_PORTAL_ORDERS=true)
- §4 must include Q-61 adoption gap subsection (HAS_NEW_ITEMS=true)
- §2 must include Q-63 conversion subsection (MIXPANEL_USER_DATA_PRESENT=true)
- §2 must include Q-65 selling time subsection (MIXPANEL_USER_DATA_PRESENT=true)

## Cross-contamination
- Only `Universal Forest Industries` / `ufi`; no other org name or shortname in delivered HTML.

## Known-acceptable drift (NOT failures)
- Numeric metrics (orders, GMV, user counts, inventory rows).
- Rep roster composition (new hires, departures).
- Peer benchmark standing (peer CSV refresh cycle).
