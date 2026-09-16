# Section Guide: §3 — Customer & Buyer Intelligence
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `customers`
- **title**: Customer & Buyer Intelligence
- **section number**: 3
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-12_results.md` — Customer activation & network health
- `cache/Q-14_results.md` — Reorder velocity & early warning
- `cache/Q-17_results.md` — Dormant high-value accounts
- `cache/Q-40_results.md` — Geographic distribution of eCat orders
- `cache/Q-41_results.md` — New eCat buyer acquisition
- `cache/gate_flags.md` — for `HAS_CART`

## Subsection Order (do not reorder — render in the order below)

### 1. Customer Activation & Network Health (Q-12)

Build from `Q-12_results.md`. Surface total account base size, active vs. inactive customer counts, and activation rates.

### 2. Dormant High-Value Accounts (Q-17)

Build from `Q-17_results.md`. Surface accounts that were previously active but have gone dormant, prioritized by historical value.

**Extrapolation tag rule**: Include prior GMV figure only when the `[ESTIMATED]` tag is appropriate (extrapolated annualized GMV). Exact LTM GMV does not require a tag.

Show top 5 dormant accounts by historical value. Remaining in collapsed `<details>`.

### 3. Geographic Distribution (Q-40)

Build from `Q-40_results.md`. Surface geographic distribution of eCat ordering activity. `[COLLAPSE]`

### 4. Reorder Velocity & Early Warning (Q-14)

Build from `Q-14_results.md`. Surface reorder frequency patterns and flag accounts showing declining reorder velocity as early churn warnings.

Show top 5 high-frequency buyers and flagged decelerating accounts only.

### 5. New eCat Buyer Acquisition (Q-41)

Build from `Q-41_results.md`. Surface newly acquired buyers on the eCat platform.

**Column rule**: The iPad column is always present. The eCat Online column is included only if `HAS_CART = true` (check `gate_flags.md`). If `HAS_CART = false`, render iPad acquisition data only — do not include an empty eCat Online column.

`[COLLAPSE]`

## Section-Specific Rules

**ERP label prohibition — applies to every HTML slot in this section:**

The VM-12 data source (`customers` table, synced from the client's ERP) contains total account counts including non-eCat accounts. When displaying metric cards or `metric-note` slots in this section:

- **`metric-note` text**: use "total account records" or "your full account base" — NEVER "all-time ERP records"
- **Percentage notes**: use "% of your full account base" or "% of total accounts" — NEVER "% of ERP base"
- **Inline prose**: use "accounts in your system" or "in your account base" — NEVER "ERP accounts"

These are the three most common ERP label leakage points in the Customer section. All three are forbidden in client-facing HTML.
