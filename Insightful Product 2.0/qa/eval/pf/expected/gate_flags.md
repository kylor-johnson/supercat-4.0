# Expected Gate Flags — Palecek (pf)

Structural gate booleans only. Numeric evidence may drift between runs.

## Primary Gates

| Flag | Expected |
|------|----------|
| HAS_CLICKY | false |
| HAS_CART | false |
| HAS_PORTAL_ORDERS | false |
| HAS_INVENTORY | true |
| HAS_SALES_DATA | false |
| HAS_SALES_SECTION | true |
| HAS_PEER_DATA | true |
| BENCHMARK_ELIGIBLE | true |

## Derived Gates

| Flag | Expected |
|------|----------|
| VM45_RENDER | false |
| MIXPANEL_USER_DATA_PRESENT | true |
| PORTAL_REP_DATA_PRESENT | false |
| PORTAL_CUSTOMER_DATA_PRESENT | false |
