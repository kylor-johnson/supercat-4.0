# Customer Intelligence v4 — Planning Handoff

> **Purpose**: Plan and implement changes to the Customer Intelligence Brief generator based on the v3 pilot audit findings.
> **Created**: 2026-06-16

---

## Your Task

Read the pilot audit report, understand the current brief generation architecture, and produce an implementation plan that addresses the audit findings in priority order. Then implement the changes to the authority files and generation specs.

---

## Start Here

### 1. The Audit Report (read first)

`Customer Intelligence/runs/pilot_audit_report.md`

This is a comprehensive audit of the 40-brief v3 pilot batch. It evaluates goal achievement (4/5), accuracy (15/15 spot-checks pass), and quality. It ends with prioritized recommendations:

- **3 must-fix** items (blocks production)
- **5 should-fix** items (significant quality improvement)
- **4 nice-to-have** items (polish)
- **4 strategic** items (next-version capabilities)

### 2. The Authority Files (these are what you'll modify)

| File | What it governs |
|------|----------------|
| `Customer Intelligence/authority/health_score_spec.md` | Health score formula — has a confirmed arithmetic bug |
| `Customer Intelligence/authority/customer_gate_rules.md` | Gate logic for conditional sections — needs new gates |
| `Customer Intelligence/authority/customer_brief_sections.md` | Section rendering specifications |
| `Customer Intelligence/authority/customer_query_library.md` | Every CQ query used to generate briefs |

### 3. The Design Docs (the measuring stick)

| File | What it contains |
|------|----------------|
| `Customer Intelligence/00_product_concept.md` | Product concept and value proposition |
| `Customer Intelligence/02_brief_sections.md` | Original 12-section design |
| `Customer Intelligence/03_advanced_insights.md` | 11 advanced insights (Next Best Product, Wallet Share, etc.) |
| `Customer Intelligence/04_example_brief.md` | Gold standard Magnolia example |
| `Customer Intelligence/07_prototype_findings.md` | v1→v2 iteration findings |

### 4. The Pilot Briefs (for reference/testing)

All 40 briefs live under: `Customer Intelligence/runs/{shortname}/{customer_code}/brief.md`

Manifest: `Customer Intelligence/runs/pilot_manifest.md`

### 5. MCP Access (for validation queries)

- **Postgres**: `user-supercat-postgres-vpn` → tool: `execute_sql`, param: `sql`
- **BigQuery**: `user-bigquery-admin` → tool: `query`, param: `sql`

---

## What Needs to Happen

### Phase 1: Must-Fix (do these first)

1. **Health score arithmetic bug** — The normalization in `health_score_spec.md` produces wrong results. Confirmed case: wwjc/21762 scores 84/90 raw points but displays 91 instead of 93. Additionally, signal H6 (fill rate) used a proxy ("replacement order %") instead of the spec-defined CQ-15 formula when fill rate data was missing. Fix the spec to clarify: (a) the exact normalization formula, (b) what to do when CQ-15 can't be computed for a specific customer.

2. **Fill rate = 0% false alarm** — Three orgs (fsf, jyc, ril) show 0% fill rate because `portal_order_items.quantity_invoiced` is not populated. The briefs present this as critical fulfillment failure. Add a new gate or pre-check: if the org's invoice item population rate is below a threshold (e.g., <50% of `quantity_invoiced` values are non-zero), SKIP the fill rate section rather than displaying 0%.

3. **Ghost SKU vs. real stock-out disambiguation** — In the §4 Top Items section, ghost SKUs (no catalog record) appear identically to real stock-outs (item exists but qty=0). Update `customer_brief_sections.md` to require distinct formatting: "⚠ STOCK OUT — [item] — 0 available, next receipt [date]" vs. "⚠ GHOST SKU — [item] — no catalog record, cannot verify stock status."

### Phase 2: Should-Fix

4. **Next Best Product volume gate** — V-01 in `customer_gate_rules.md` blocks CQ-06 at >10,000 orders. The pilot's most important accounts all exceed this. Options: (a) raise threshold, (b) sample recent orders only, (c) compute on most-recent 12 months only, (d) pre-compute item co-occurrence matrix.

5. **Cross-sell cohort definition** — State-level cohorts produce absurd results when target account dwarfs peers. Add alternative cohort logic to the query library.

6. **Expand Strategic Summary** — Update `customer_brief_sections.md` §23 spec to require 5-6 talking points (currently produces 3) with priority sequencing.

7. **Seasonality visualization** — Add ASCII bar chart format spec for monthly revenue (per the Magnolia example).

8. **Active months cap** — Cosmetic: cap displayed value at 12, note "all months active" when true.

### Phase 3: Nice-to-Have

9. Normalize section numbering (sequential, no gaps)
10. Add rep name to header (territory → rep lookup)
11. Wallet share minimum cohort size (N >= 5 required)
12. Standardize "Uncategorized" callout format

### Phase 4: Strategic (design only, don't implement yet)

13. Multi-account customer grouping
14. Anomaly-first brief reordering
15. Revenue at Risk / Opportunity quantification
16. Competitive loss signal as primary alert banner

---

## Output Expected

1. Updated `health_score_spec.md` with bug fixes
2. Updated `customer_gate_rules.md` with new gates (fill rate population check, ghost SKU handling)
3. Updated `customer_brief_sections.md` with formatting changes
4. A `Customer Intelligence/CHANGELOG.md` documenting what changed and why
5. For Phase 4 items: design notes only (append to existing design docs or create `Customer Intelligence/09_v4_design.md`)

---

## Constraints

- **Read-only MCP posture** — you can query the database to validate your changes but do not modify data.
- **Preserve backward compatibility** — existing gate definitions that work correctly should not change behavior. Add new gates, don't remove working ones.
- **Reference the audit** — every change should cite which audit finding it addresses.

---

*Handoff created: 2026-06-16 | Source: Customer Intelligence v3 Pilot Audit*
