# Section Guide: §5 — Commerce Analytics
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `commerce`
- **title**: Commerce Analytics
- **section number**: 5
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-13_results.md` — Customer concentration risk (top-buyer eCat GMV share)
- `cache/Q-16_results.md` — ERP total business visibility
- `cache/Q-18_results.md` — eCat order trend and channel breakdown
- `cache/Q-20_results.md` — AOV by order segment
- `cache/Q-21_results.md` — Order type & workflow
- `cache/Q-45_results.md` — eCat capture rate
- `cache/gate_flags.md` — for `HAS_CART`, `HAS_PORTAL_ORDERS`, `VM45_RENDER`

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. eCat Order Trend (Q-18)

**Part A** (always): eCat order trend — eCat-originated orders only.

**Part B** (only if `HAS_PORTAL_ORDERS = true`): Add eCat share of total business trend alongside Part A.

### 2. AOV by Order Segment (Q-20)

Build from `Q-20_results.md`. Surface average order value broken down by order segment.

### 3. eCat Ordering Channel Breakdown (Q-18)

**Gate**: `HAS_CART = true`

Build from Q-18 data. Show iPad vs. eCat Online channel split.

### 4. Top Buyers & Concentration (Q-13)

Build from `Q-13_results.md`. Show top 10 buyers by eCat GMV with these exact columns:

| Column | Content |
|--------|---------|
| Customer | Buyer name |
| Orders | eCat order count |
| GMV | eCat GMV |
| % of eCat GMV | Buyer's share of total eCat GMV |

Include a concentration callout if top-5 buyers exceed 25% of total eCat GMV.

### 5. Order Type & Workflow (Q-21)

Build from `Q-21_results.md`. Surface order type and workflow distribution.

### 6. ERP Total Business Context (Q-16)

**Gate**: `HAS_PORTAL_ORDERS = true`

Build from `Q-16_results.md`. Use ERP framing only — present as total all-channel business context.

### 7. eCat Capture Rate (Q-45)

**Gate**: `HAS_PORTAL_ORDERS = true` AND `VM45_RENDER = true` (read from `gate_flags.md`)

Build from `Q-45_results.md`. No denominator-less fallback — if `VM45_RENDER = false`, skip this subsection silently.

## Section-Specific Rules

**VM-45 denominator gate**: The section agent reads `VM45_RENDER` from `gate_flags.md`. Stage 1 pre-computes the two-gate validity check (Gate 1: `portal_orders_gmv > ecat_gmv`; Gate 2: `ecat_gmv >= 5% of portal_orders_gmv`). If `VM45_RENDER = false`, skip subsection 7 silently. Do not re-derive the gate. Do not render a fallback capture rate without a valid denominator.

**If `HAS_PORTAL_ORDERS = false`**: Commerce Analytics shows eCat-only data. Do not mention ERP, total business, or `portal_orders` at all in this section. Subsections 1 Part B, 6, and 7 are all skipped.

**Channel attribution statement** (required in section body when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.
