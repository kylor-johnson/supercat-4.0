# Customer Intelligence Brief — Org Readiness Profiler

> **Status**: Production v4 — updated 2026-06-16 (added G-10, G-11)
> **Purpose**: Pre-flight check that runs before generating any Customer Intelligence Brief.
> Determines which sections will render, sets expectations, and prevents wasted queries.

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `{{ORG_ID}}` | Organization ID (integer) |
| `{{ORG_SHORTNAME}}` | Organization shortname for BigQuery (e.g., `ufi`, `cci`, `sc`) |

---

## Workflow

### Step 1 — Run Gate Queries

Execute all 11 gate queries from [customer_gate_rules.md](../authority/customer_gate_rules.md) against the target org.

**Postgres gates** (run via `user-supercat-postgres-vpn`, `execute_sql`):

Run these 9 queries in sequence (they're fast — each returns a single row):

1. **G-01 `HAS_PORTAL_INVOICES`**: `portal_invoice_items` count > 0
2. **G-02 `HAS_COMMITMENT_REPORTS`**: `commitment_reports` count > 0
3. **G-03 `HAS_PLACEMENT_REPORTS`**: `placement_reports` count > 0
4. **G-05 `HAS_ECAT_ORDERS`**: `orders` submitted in LTM > 0
5. **G-06 `HAS_RMA`**: `rma_requests` via `org_users` join > 0
6. **G-07 `HAS_BUYER_NAMES`**: `portal_orders` buyer_name > 5% populated
7. **G-08 `COLLECTION_COVERAGE`**: `products` collection_code >= 50%
8. **G-09 `HAS_SHIP_TO_DATA`**: `portal_orders` ship_to_number > 10% populated
9. **G-10 `FILL_RATE_POPULATION`** (v4): `portal_order_items` quantity_invoiced > 0 for >= 50% of LTM items. When false, §20 Fulfillment is suppressed and health score H6 is skipped.
10. **G-11 `HAS_NEW_ITEMS`** (v4): `products` with `new_item = true AND deleted = false` count > 0. When false, §5 New Introduction Adoption is skipped entirely (no empty placeholder).

**BigQuery gate** (run via `user-bigquery-admin`, `sql`):

11. **G-04 `HAS_MIXPANEL_CUSTOMER`**: `mixpanel.events` with `selected_bill_to_code IS NOT NULL` in LTM > 0

### Step 2 — Compute Gate Flags

For each gate, apply the threshold rule from `customer_gate_rules.md` and record `true` or `false`.

### Step 3 — Compute Data Richness Score

Count the number of `true` gates (0–11):
- **8–11**: Rich — full brief with all conditional sections
- **5–7**: Standard — core sections strong, some conditional sections skip
- **2–4**: Lean — orders-only mode likely
- **0–1**: Insufficient — cannot produce a meaningful brief

### Step 4 — Build Section Manifest

Determine which sections will render based on gate flags:

| Section | Gate Required | Status |
|---------|--------------|--------|
| Header | — | ALWAYS |
| Account at a Glance | — (eCat portion conditional on `HAS_ECAT_ORDERS`) | ALWAYS |
| Purchase DNA: Categories | `HAS_PORTAL_INVOICES` | conditional |
| Purchase DNA: Top Items | `HAS_PORTAL_INVOICES` | conditional |
| New Introduction Adoption | `HAS_PORTAL_INVOICES` + `HAS_NEW_ITEMS` (G-11) | conditional |
| Spend Trajectory | — | ALWAYS |
| Buying Rhythm | — | ALWAYS |
| Channel Mix | — | ALWAYS |
| Wallet Share | — | ALWAYS |
| Price & Discount | `HAS_PORTAL_INVOICES` | conditional |
| Fulfillment / Fill Rate | `HAS_PORTAL_INVOICES` + `FILL_RATE_POPULATION` (G-10) | conditional |
| Market Commitments | `HAS_COMMITMENT_REPORTS` | conditional |
| Showroom Placements | `HAS_PLACEMENT_REPORTS` | conditional |
| Rep Engagement | `HAS_MIXPANEL_CUSTOMER` | conditional |
| Buyer Intelligence | `HAS_BUYER_NAMES` | conditional |
| Returns | `HAS_RMA` | conditional |
| Collection Mix | `COLLECTION_COVERAGE` (standalone vs. folded) | conditional |
| Same-Store Comps | `HAS_SHIP_TO_DATA` | conditional |
| Account Lifecycle | — | ALWAYS |
| Strategic Summary | — | ALWAYS |

### Step 5 — Output

Report to chat:

```
## Org Readiness Profile: {{ORG_SHORTNAME}} (ID {{ORG_ID}})

### Gate Flags
| Gate | Value | Raw Metric |
|------|-------|------------|
| HAS_PORTAL_INVOICES | true/false | N items |
| HAS_COMMITMENT_REPORTS | true/false | N reports |
| HAS_PLACEMENT_REPORTS | true/false | N reports |
| HAS_MIXPANEL_CUSTOMER | true/false | N events |
| HAS_ECAT_ORDERS | true/false | N orders |
| HAS_RMA | true/false | N requests |
| HAS_BUYER_NAMES | true/false | N% populated |
| COLLECTION_COVERAGE | true/false | N% with code |
| HAS_SHIP_TO_DATA | true/false | N% populated |
| FILL_RATE_POPULATION | true/false | N% with qty_invoiced > 0 |
| HAS_NEW_ITEMS | true/false | N products with new_item=true |

### Data Richness Score: X/11 (Rich/Standard/Lean/Insufficient)

### Section Manifest
- INCLUDE: [list of sections that will render]
- SKIP: [list of sections that will not render]
- CONDITIONAL NOTE: [any sections with special rendering modes]

### Brief Quality Prediction
[1-2 sentence assessment of expected brief quality for this org]
```

---

## Hard Constraints

- **Read-only MCP posture.** Every query is a SELECT. Never write, update, or delete.
- **If a gate query fails, flag it** — do not assume true or false. Report the error and let the operator decide.
- **Do not run customer-level queries in the profiler.** This is an org-level diagnostic only.
