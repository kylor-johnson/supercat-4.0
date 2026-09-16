# Validation Runbook — Insightful Product 2.0

**External Customer Intelligence Report — QA Runbook**
Last updated: 2026-06-12
Evidence basis: 13-org Phase 1 validation set

This is the standard QA checklist for every external intelligence report run. Work through it in stage order alongside the external run prompts (`prompts/stage1_data_gathering.md` → `prompts/stage2_through_4_build_and_assemble.md`). Fill out `org_validation_log_template.md` as you go.

This document is **not** a runtime input. It is a human-facing QA reference.

> **Profiles retired.** There is a single report form. Earlier versions supported `deep_intelligence` / `executive_intelligence` profiles; that branch has been removed and every check below applies to the one report form.

---

## Caveat vs. blocker — quick reference

Understanding the difference prevents unnecessary escalation and prevents shipping bad reports.

> **Delivered Appendix vs. validation log**: The delivered report Appendix contains data source attribution only (see `report-system/external_report_blueprint.md §6`). Findings from this runbook — omission reasons, anomaly flags, deduplication notes, staleness details, VM-45 rationale, showroom exclusions — are recorded in the **validation log** (`org_validation_log_template.md`), not in the delivered Appendix. Report mode, gating explanations, partial-sync disclosures, standing caveat blocks, and [ESTIMATED] explanation rows are also forbidden from the Appendix.
>
> **HTML comment leakage**: The template file contains `<!-- ... -->` authoring comments. None of these comments may remain in the delivered HTML. A clean delivered HTML has zero HTML comment nodes — search `<!--` in the output file before delivery.

| Type | Definition | Action |
|------|-----------|--------|
| **Log disclosure** | Known, stable data pattern with no impact on the report's core claims | Record in the validation log. No note in delivered report. No escalation. |
| **Section caveat** | Data is present but limited in a way that affects one section's reliability | Degrade or omit the affected section. Record the reason in the validation log. Continue the rest of the report. |
| **Run caveat** | A data issue that affects the overall reliability of the report but does not block delivery | Complete the report. Add a caveat to the Executive Summary if client-relevant. Flag for CSM review before client delivery. Record in validation log. |
| **Blocker** | The data state makes the report undeliverable or fundamentally misleading | Abort the run. Document the block in the validation log. Escalate before proceeding. |

When to escalate: if a data issue does not match any known limitation in `known_limitations.md`, is new, and is large enough to affect a core claim in the report — escalate rather than improvise.

---

## Stage 1 — Identity and dependency checks

Run before any data queries.

### 1.1 Org identity

- [ ] Confirm org name, shortname, and `org_id` from `organizations` table
- [ ] If the shortname lookup returns no result or is ambiguous: **STOP** — resolve before proceeding

### 1.2 Peer benchmark availability

- [ ] Check for org's shortname in the current `peer_benchmark_{date}.csv` in `Peer Benchmark/runs/`
- [ ] If found: note `benchmark_eligible`, `confidence` (high/medium/low), and peer count — **internal working notes only**; none of these values appear in the client-facing report output
- [ ] `benchmark_eligible = True` AND found in file → `HAS_PEER_DATA = true`
- [ ] Not found or `benchmark_eligible = False` → `HAS_PEER_DATA = false`; §7 will be omitted

### 1.3 Clicky availability

- [ ] Check `org_summary.has_clicky_portal` for the org
- [ ] If true: list tables in `clicky_analytics` with `LIKE '%_daily_metrics'` and identify the prefix for this org (prefix is not always the same as the org shortname — match by org name pattern). Set `CLICKY_PREFIX`.
- [ ] Confirm the `{clicky_prefix}_daily_metrics` table exists and has rows
- [ ] If false, or table missing or prefix unresolvable: `HAS_CLICKY = false` — §6 is absent entirely; Clicky not mentioned anywhere in report
- [ ] Record the resolved `CLICKY_PREFIX` value in the validation log (§3 Preflight Gates)

---

## Stage 2 — Minimum-commerce gate

Run before generating sections.

### 2.1 Zero-commerce check

- [ ] Query LTM eCat order count (`orders`, submitted, last 12 months)
- [ ] Query LTM `portal_orders` count
- [ ] **If both are zero**: route to activation / reactivation summary mode
  - Zero all-time orders → "Platform Activation Report" framing
  - Historical orders exist but none LTM → "Platform Reactivation Report" framing
  - Exclude all commerce-dependent sections (§2 Sales Team, §3 Customer, §4 Product, §5 Commerce, VM-45)

### 2.2 Core data staleness gate

- [ ] Query `data_versions` for `products`, `inventories`, `customers` staleness
- [ ] If any of these are **> 180 days stale**: exclude §4 Product & Inventory Intelligence; add staleness warning to Executive Summary
- [ ] Record staleness of all entities in the validation log

---

## Stage 3 — Preflight gates

Determine which sections and VMs are active. Resolve every flag before querying data.

### 3.1 Bundle and config detection

- [ ] Read `org_summary.recurring_services` for the org
- [ ] `HAS_CART` = true **only if** B2B Cart is in `recurring_services` **AND** confirmed server order count > 0
  - "eCat Online - Catalog" and "eCat Online - Portal" are read-only products — do not set `HAS_CART = true` from their presence alone
- [ ] `HAS_PORTAL_ORDERS` = true only if `portal_orders` row count > 0 **AND** GMV > 0

### 3.2 Section availability gates

- [ ] `HAS_INVENTORY` = true if `inventories` row count > 0
- [ ] `HAS_SALES_DATA` = true if `sales_data` row count > 0
- [ ] **Catalog visibility sanity check**: compare `COUNT(*) WHERE deleted = false AND hideable = false` vs. total active products. If explicit-`false` count is dramatically lower (< 5% of active products), the org uses `hideable = NULL` as default. Use `(hideable = false OR hideable IS NULL)` for all catalog visibility queries. Do not report near-zero visible product counts without checking this first.
- [ ] `HAS_SALES_SECTION` = true only if qualifying iPad rep count ≥ 5 (run the count query; threshold is 10+ orders LTM per rep; do not assume from roster size)

> **Enrollment**: VM-15 and VM-44 (enrollment funnel and onboarding velocity) are intentionally excluded from the external report system. Do not check `enrollment_applicants` as part of this runbook. No `HAS_ENROLLMENT` or `HAS_VM44` gate is required.

---

## Stage 4 — Denominator sanity check (VM-45)

Only run if `HAS_PORTAL_ORDERS = true`.

- [ ] Compute LTM eCat GMV from `orders` (submitted, not deleted, last 12 months)
- [ ] Compute LTM ERP GMV from `portal_orders` (last 12 months)
- [ ] **Gate 1** — `portal_orders_gmv > ecat_gmv`
  - Fail → partial ERP sync; skip VM-45; record gate result in validation log
- [ ] **Gate 2** — `ecat_gmv ≥ 5% of portal_orders_gmv`
  - Fail → eCat share too small to interpret as an activation signal; skip VM-45; record gate result in validation log
- [ ] Both gates pass → render VM-45; record denominator ratio in validation log
- [ ] **Never** substitute a denominator-less GMV commentary if VM-45 is skipped

---

## Stage 5 — Buyer, rep, and non-selling user checks

Run before generating §2 Sales Team and §3 Customer sections.

### 5.1 B2B Cart buyer orders

- [ ] Server orders with `rep_first_name IS NULL` and numeric `org_user_id` = B2B buyers — **expected behavior**
- [ ] Include in commerce analytics as server-sourced; do not flag as anomalous

### 5.2 Showroom and operational account check

- [ ] Scan rep name fields for: `showroom`, `admin`, `marketing`, `training`, `test`, `demo`, or the org's own company name
- [ ] A name match is a flag for review — it is **not sufficient evidence on its own** to exclude an account from the rep leaderboard. Look for corroborating signals: location/city string in last name, no individual contact name, pattern consistent with a shared/physical-location account.
- [ ] If corroborating signals confirm operational/shared-location account: include in total org GMV; exclude from rep leaderboard; record in validation log with the specific evidence (not just the name pattern)
- [ ] If no corroborating signal beyond the name: classify as "ambiguous — flagged for CSM review" rather than auto-excluding. Do not exclude any account on name alone.
- [ ] Showroom/operational exclusions are recorded in the **validation log**, not in the delivered Appendix

### 5.3 NULL customer_number on high-value orders

- [ ] Check for orders where `customer_num IS NULL` and `total > $5,000`
- [ ] These are real orders but cannot be ERP-matched — flag in validation log for account record cleanup

---

## Stage 6 — Duplicate and data-quality checks

### 6.1 Zero-dollar orders

- [ ] Count orders with `total = 0`
- [ ] ≤ 1% of total → log in validation log; no further action
- [ ] > 1% → investigate before surfacing GMV figures; may be marketing supply, sample requests, or import artifacts

### 6.2 Duplicate quote clusters

- [ ] Query: same `customer_num`, same `total`, same calendar day, count ≥ 2
- [ ] Classify each cluster:
  - Count 2 → incidental pair; log in validation log, no exclusion
  - Count 3–5 → potential duplicate; flag for review
  - 4+ orders within a 10-minute window → likely resubmission; flag as high-confidence duplicate
- [ ] Do not auto-exclude. Record in validation log for human confirmation.

### 6.3 Monthly GMV distribution check

- [ ] If any single month exceeds 50% of LTM GMV → investigate for trade show / market week context or data anomaly
- [ ] If context confirmed → note in Commerce Analytics; do not normalize without documentation

### 6.4 OOS × ERP join quality check

- [ ] When surfacing OOS items: confirm each item has non-NULL `amount_invoiced` in `sales_data`
- [ ] NULL ERP join → item has no confirmed sales history; do not label it "best sellers you can't sell"
- [ ] Surface separately as "out of stock with no recent ERP sales history" or omit

---

## Stage 7 — Clicky-specific checks

Only run if `HAS_CLICKY = true`.

- [ ] Confirm `{clicky_prefix}_daily_metrics` table exists and has rows
- [ ] **Deduplication check**: if any date has `COUNT(*) > 1`, use `MAX()` aggregation per date for all daily_metrics queries — never raw SUM across dates without deduplication
- [ ] **Exclude `bounce_rate`**: returns unconfirmed large integer values — omit from all report outputs
- [ ] Use deduplicated `visitors_unique`, `actions_pageviews`, and `time_average_seconds`
- [ ] Record in validation log whether date-level deduplication was applied and which dates had multiple rows
- [ ] **Cross-account gap check**: if a Clicky data gap appears (stretch of days with no rows or anomalously low traffic), check whether the same date window appears on at least one other Clicky-enabled org before classifying it as account-specific. If the gap appears on multiple orgs in the same window, record it as a pipeline-level outage in the validation log — not an account data issue.

---

## Stage 8 — Section-rendering checks

Confirm which sections are active before assembly.

### Section rendering

| Section | Render when | Omit when |
|---------|------------|-----------|
| §1 Executive Summary | Always — written last; 5–6 highlights + 2–4 priority actions | — |
| §2 Sales Team Performance | ≥ 5 qualifying iPad reps (≥ 10 orders LTM each) | Fewer than 5 qualifying reps |
| §3 Customer & Buyer Intelligence | Minimum-commerce gate passed | Pre/lapsed account mode |
| §4 Product & Inventory Intelligence | `HAS_INVENTORY = true` AND core data ≤ 180d stale | No inventory data, or data stale > 180 days |
| §5 Commerce Analytics | Minimum-commerce gate passed | Pre/lapsed account mode |
| §5 VM-45 (eCat Capture Rate) | Both denominator gates pass | Either gate fails |
| §5 VM-19 (Channel Mix) | `HAS_CART = true` AND confirmed server orders > 0 | iPad-only, read-only catalog, or no server orders |
| §6 Portal Engagement | `HAS_CLICKY = true` AND table exists | `has_clicky_portal = false` — absent entirely, no soft references |
| §7 Peer Benchmarking | `HAS_PEER_DATA = true` AND `benchmark_eligible = True` | Not in peer file or not eligible |
| §8 Platform & Feature Utilization | Always (if minimum-commerce gate passed) | Pre/lapsed account mode — limited version |
| §9 Appendix | Always — attribution only | — |

### Summary rules (enforced — not editorial guidance)

- [ ] Executive Summary contains 5–6 highlights — not fewer than 5, not more than 6
- [ ] No `<p class="prose">` before the highlights list — zero prose before the list
- [ ] Priority Actions: 2–4 actions; lower-priority may be in collapsed `<details>`

**§1 Executive Summary is always written last.** It synthesizes the other sections — do not draft it until all other sections are assembled.

---

## Stage 9 — Output-claim checks

Review the generated report before delivery.

### 9.1 Semantic guardrails

- [ ] `portal_orders` described only as "ERP-synced total business" or "all-channel business" — never as buyer activity or portal ordering
- [ ] `Sales Portal` not described as a buyer ordering channel
- [ ] `self-service` used only for B2B Cart / eCat Online (`order_source = 'server'`)
- [ ] Health score absent from the report in any form
- [ ] Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) do not appear anywhere — these are internal-only terms. §7 Peer Benchmarking uses plain-language cohort framing derived from `peer_group_id_effective` — not the raw label or tier labels.
- [ ] Clicky not mentioned anywhere if `HAS_CLICKY = false`

### 9.2a Direct HTML inspection — forbidden strings (search the delivered HTML file before delivery)

These are the confirmed regression leakage points. Search the final HTML output for each of the following strings. **Any hit is a blocker — do not deliver until resolved.**

| String to search | Why it's forbidden | Required replacement |
|---|---|---|
| `<!--` | **HTML COMMENT LEAKAGE** — No HTML comment nodes may remain in delivered HTML. The template contains authoring comments (`<!-- Operator: ... -->`, `<!-- BEGIN/END ... GATE -->`, `<!-- HAS_* -->`, `<!-- EXAMPLE ROW -->`, section banners) that must all be stripped before delivery. | Strip every `<!-- ... -->` node from the delivered file |
| `HAS_CLICKY` | Gating flag — must not appear in delivered HTML source even inside a comment | Strip the containing comment node |
| `HAS_CART` | Gating flag — same prohibition | Strip the containing comment node |
| `HAS_INVENTORY` | Gating flag — same prohibition | Strip the containing comment node |
| `HAS_SALES_SECTION` | Gating flag — same prohibition | Strip the containing comment node |
| `HAS_PORTAL_ORDERS` | Gating flag — same prohibition | Strip the containing comment node |
| `HAS_PEER_DATA` | Gating flag — same prohibition | Strip the containing comment node |
| `ERP` | Forbidden in all client-facing HTML elements (§1–§8 prose, metric labels, metric-note slots, table footnotes, callouts, section descriptions) — Appendix attribution row is the only exception | "total business," "all-channel sales," "your account base," "your business system," etc. |
| `Operational Health Score` | Internal Health V2 vocabulary — client-facing peer benchmark metric label must never use this phrase | Use `peer-metric-title` = "Data & Operational Health" |
| `operational_health_score` | Internal metric key name — must never appear in delivered HTML | Use display label "Data & Operational Health" |
| `health score` | Covers sentence-level leakage in the `operational_health_score` row and top-performer prose — "import health score at X" and "lower operational health scores" are both violations | Rewrite as "catalog freshness and import health at X" / "accounts with lower data freshness" |
| `health scores` | Plural form — same prohibition, same locations | Rewrite without "health scores" wording |
| `health_score` | Internal metric key — excluded from all external output | Suppress entirely |
| `Health Score` | Capitalized form of internal label | Suppress entirely |
| `Health Scores` | Capitalized plural | Suppress entirely |
| `benchmark_confidence` | Internal rendering signal — never in client-facing HTML | Remove; use calibrated plain-language framing |
| `peer_group_level` | Internal gating signal — never externally | Remove |
| `peer_group_n` | Internal count — never as a literal number externally | Remove or replace with approved plain-language framing |
| `Platform-Embedded` | Internal segment label | Remove entirely |
| `Commerce-Active` | Internal segment label | Remove entirely |
| `Catalog-Focused` | Internal segment label | Remove entirely |
| `Mixpanel` | Internal tool name | Use "platform engagement data" |
| `Clicky` | Internal tool name | Remove or use "portal analytics" only if HAS_CLICKY = true; never mention if false |

**How to run this check**: Open the final HTML file in a text editor or use a browser's View Source. Search for each string. A clean HTML has zero hits on every row above except `ERP` in the Appendix attribution row (if `HAS_PORTAL_ORDERS = true`). The `<!--` search must return zero hits — a delivered report has no HTML comment nodes of any kind.

### 9.2 Claim validity

- [ ] Every metric has a time qualifier ("in the trailing 12 months," "as of April 2026," etc.)
- [ ] Projections labeled `[HYPOTHETICAL]`; extrapolations labeled `[ESTIMATED]`
- [ ] No forbidden claims appear (health score, churn risk, exact competitor comparisons, internal-only VM content)

### 9.3 Section order

Verify the final section order (Mode 1 Standard):

- [ ] Final order: Executive Summary → [Sales Team] → Customer & Buyer → [Product & Inventory] → Commerce → [Portal Engagement] → [Peer Benchmarking] → Platform & Feature → Appendix
- [ ] Portal Engagement and Platform & Feature Utilization appear as separate core sections
- [ ] Executive Summary is first in the deliverable but was written last during assembly

---

## Stage 10 — Pre-delivery completeness check

Before marking the report done, verify both the validation log and the delivered Appendix are correct.

**Validation log** — confirm the following are recorded:
- [ ] Omitted sections and the specific reason for each omission
- [ ] VM-45 gate result and denominator ratio (if applicable)
- [ ] `sales_quotas` staleness (standing pipeline disclosure)
- [ ] Any other stale entities affecting accuracy
- [ ] Duplicate clusters or anomaly flags
- [ ] NULL customer_number high-value orders (if applicable)
- [ ] Clicky deduplication — whether applied, and which dates had multiple rows
- [ ] Peer benchmark: `benchmark_confidence` value and `peer_group_n` (internal calibration; never in delivered report)
- [ ] Showroom/operational account exclusions from rep leaderboard — account name, corroborating evidence, and exclusion rationale (none of this appears in delivered Appendix)

**Delivered Appendix** — confirm it contains data source attribution only (every item below is a blocker if present):
- [ ] One attribution row per data source used — plain-language name, time period or "as of [date]"
- [ ] No report mode (standard / activation / reactivation) stated in the Appendix
- [ ] No run parameters, generation metadata, or platform bundle metadata
- [ ] No omitted-sections table or rationale — absent sections are omitted silently; no explanation in the Appendix
- [ ] No gating explanations (e.g., "HAS_CLICKY = false — Portal Engagement omitted," "VM-45 skipped — Gate 2 failed")
- [ ] No partial-sync disclosure blocks or ERP-sync caveats
- [ ] No standing caveat blocks or data-quality disclaimers
- [ ] No [ESTIMATED] explanation rows — the inline tag in the section is the complete disclosure
- [ ] No methodology notes, VM-45 rationale, gate flags, or deduplication notes
- [ ] No internal identifiers: no org IDs, table names, VM codes, query IDs, row counts, dataset paths
- [ ] No Clicky deduplication disclosure, no pipeline outage notes, no validation commentary
- [ ] Peer benchmark row (if section included): "Anonymized median and percentile data from [PEER_GROUP_LABEL] accounts. No individual account data is disclosed." — no confidence label, no raw `peer_group_n` count
- [ ] Plain-language peer context note added (if `benchmark_confidence` is `low` or `medium`) per `dependencies/PEER_BENCHMARK.md §7`

---

## Report delivery gate

When Stage 10 is complete and the report is ready to send, run through `report_delivery_checklist.md` before delivering to the client. The checklist is the final go/no-go gate and takes less than 5 minutes for a clean run. It is separate from this runbook — the runbook governs the generation process; the checklist governs the delivery decision.

---

## When to escalate

Stop the run and escalate if any of the following are true:

- The org identity cannot be confirmed from the database
- LTM eCat and ERP order counts are both zero for an account that should be active
- Core data (products, inventories, customers) is > 180 days stale for an account currently in active use
- A query returns results that cannot be explained by any known limitation in `known_limitations.md` and would materially affect a core claim
- A new anomaly class appears that does not fit the existing taxonomy and the right handling is unclear

When escalating: document the exact issue in the validation log, note what was checked, and describe what would be needed to resolve it. Do not guess or improvise around an unfamiliar data state.

---

## Appendix: Recurring patterns — standing disclosures

These patterns are stable across the 13-org validation set. They do not require per-run investigation — just consistent disclosure.

| Pattern | Treatment |
|---------|-----------|
| `sales_quotas` stale 229–242+ days | Log in validation log as standing disclosure; not an anomaly to investigate per org |
| Numeric buyer-ID server orders on B2B Cart accounts | Expected behavior; include in commerce analytics, no flag needed |
| `order_origin = 'ECAT'` in `portal_orders` returns 0 | Platform-wide pipeline gap; do not use this field |
| No `invoice_date` on `sales_data` | VM-38b remains pending engineering; do not promote to active |
| `hideable = NULL` on most active products | Default visible state; use `(hideable = false OR hideable IS NULL)` as visibility filter |
| Clicky `bounce_rate` large integer values | Excluded; column scale unconfirmed |
| Clicky date-gap affecting multiple orgs in same window | Pipeline-level outage; record in validation log, do not classify as account-specific |

---

*This runbook is updated after each significant new finding or validation cohort.*
*It is a QA reference, not a runtime authority source.*
