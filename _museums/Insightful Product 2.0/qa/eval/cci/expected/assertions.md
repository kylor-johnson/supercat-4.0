# cci — acceptance criteria

Baseline: derived from CCI v3 hardening run (2026-06-16).

## Mode
- Report mode: **Mode 1** (Standard Intelligence Report)

## Structural gate booleans (must match; numeric evidence may drift)
| Gate | Expected |
|------|----------|
| HAS_CLICKY | true |
| HAS_CART | true |
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
- Content sections §2–§8: **2, 3, 4, 5, 6, 7, 8** → **count = 7**
- (All sections included — full-bundle org with Clicky)

## Static checks (`check_static.sh <output> 7`)
- hard-forbidden tokens = 0
- unsubstituted `{{` = 0
- `<details class="section-collapse">` blocks = 7
- `<details>` balanced

## Full-bundle assertions
- §2 must include Q-51 subsection (PORTAL_REP_DATA_PRESENT=true)
- §3 must include Q-52 penetration subsection (PORTAL_CUSTOMER_DATA_PRESENT=true)
- §5 must include channel mix subsection (HAS_CART=true — iPad vs eCat Online split)
- §5 must include capture rate subsection (VM45_RENDER=true)
- §6 must include all 4 Portal subsections (HAS_CLICKY=true): Traffic Health, Monthly Trend, Geographic, Sources
- §6 must NOT contain the word "Clicky" in delivered HTML

## Elite insight assertions
- §3 must include Q-14b deceleration alert (HAS_PORTAL_ORDERS=true)
- §4 must include Q-59 fill rate subsection (HAS_PORTAL_ORDERS=true)
- §4 must include Q-61 adoption gap subsection (HAS_NEW_ITEMS=true)
- §2 must include Q-63 conversion subsection (MIXPANEL_USER_DATA_PRESENT=true)
- §2 must include Q-65 selling time subsection (MIXPANEL_USER_DATA_PRESENT=true)
- §5 must include Q-55 displacement subsection (HAS_PORTAL_ORDERS=true, if displacement rows exist)
- §5 must include Q-60 price erosion subsection (HAS_PORTAL_ORDERS=true, if data rows exist)

## Cross-contamination
- Only `Currey & Company` / `cci`; no other org name or shortname in delivered HTML.

## Known-acceptable drift (NOT failures)
- Numeric metrics (orders, GMV, user counts, inventory rows).
- Portal traffic trends (rolling Clicky window).
- Displacement categories (quarterly shifts).
- Rep roster composition.
