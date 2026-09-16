# VM Runtime Index — Insightful Product 4.0 (v4.2-complete)

> ## ⚠️ CAPABILITY / ROADMAP — not executed by `./run.sh`
> **Location:** `foundation/capability/` (shelved 2026-07-13 re-anchor). Despite
> the name, this index is **not** the pipeline's runtime manifest. Runtime:
> **14** detectors / **24** query IDs. Ground truth:
> [`../WHAT_ACTUALLY_RUNS.md`](../WHAT_ACTUALLY_RUNS.md) — **wins on any conflict.**
> Treat every "runtime status" row here as future capability, not a live gate.

> **What this is.** The **operational menu** for the value-moment catalog: one row per VM across **all 13 domains**,
> with the run/don't-run decision (`runtime status`), the audience flag, the section it lands in, its binding gate,
> query-readiness, and **live coverage** (stamped 2026-06-30). This is the runnable derivative the report operator
> (and a human picking VMs for a client) reads — the v4.2 successor to the retired `external_vm_index.md` (which
> only ever covered the original 51 VMs).
>
> **Derived from — catalog wins.** Semantic authority is [`value_moment_catalog.md`](value_moment_catalog.md)
> (its [Unified Stack Rank](value_moment_catalog.md#unified-stack-rank-v41) + [Master gate table](value_moment_catalog.md#master-gate-table-machine-readable-live-coverage-stamped)
> carry tier · ceiling · gate · `Lib` · coverage). Gating truth is [`../provenance_spine.md`](../provenance_spine.md). **If any row
> here conflicts with the catalog or the Spine, they win** — fix this index. Allowed/Forbidden claims are **not**
> duplicated here (that's where drift lives); read them from the catalog VM body before rendering.
>
> **Status:** built 2026-06-30 from the v4.2 catalog + the 2026-06-30 data-grounding probe
> ([`build_notes/vm_org_coverage_matrix_2026-06-30.md`](../build_notes/vm_org_coverage_matrix_2026-06-30.md)).

---

## How to use this menu (per client)

This menu is **static** (the universe of VMs); a client's **live menu** is produced by running the binding-gate
preflight once, then reading each VM's gate against it.

1. **Preflight the client** (read-only, once):
   - **Commerce** — `Q-PROV-00` → `TOTAL_BUSINESS_SOURCE`, `COMMERCE_CONFIDENCE`, `FEED_COMPLETENESS`, returns-in-feed, staleness.
   - **Rep identity** — name-bridge match rate → Tier 2 named / Tier 1 number-only / behavior-only (Spine §7.1).
   - **Behavioral** — Mixpanel coverage present? active users > 0? (degrade to login/order effort if absent).
   - **Sub-feed booleans** — `has_clicky`, `smart_stacks>0`, `shared_resources>0`, `enrollment_applicants>0`, HubSpot mapped.
2. **Walk the menu.** For each VM, in order:
   - **Skip** if `runtime status` = `internal_only` (never external), `non_runtime` (reference/redirect), `pending_query` or `pending_data` (no audited SQL / no feed).
   - Otherwise read the **binding gate** against the preflight → decide **🟢 FIRE** (present normally) · **🟡 DEGRADE** (fire with the mandatory caveat/clamp, or absolute-$ only) · **🔴 SUPPRESS** (do not present; the gap *is* the finding).
   - The **live coverage** column is your prior — what this VM did across the 6-org grounding cohort / population.
3. **Render** only FIRE/DEGRADE VMs, pulling Allowed/Forbidden + the Decision line from the catalog body. Internal-only VMs feed CS/Sales, never the client report.

> The full report assembly (reading contract → preflight → gather → signal rank → render) is
> [`../operators/report_operator.md`](../operators/report_operator.md). This index is the **VM-selection layer** it sits on.

---

## Runtime status — definitions

| Status | Meaning | Operator action |
|---|---|---|
| `active` | External-safe, audited SQL exists, no special feed gate beyond commerce/behavioral preflight | Run |
| `conditional` | External-safe but gated by a data flag / feature / feed completeness | Run **only** when the gate is met (else degrade or suppress) |
| `pending_query` | External-safe, schema confirmed, but SQL not yet authored/audited in `query_library_v2.md` | Do not run until authored |
| `pending_data` | Blocked on a feed/column that does not exist yet (hard-gap / cost-gated / pending-engineering) | Do not run; it's a "what to ask the client for" item |
| `internal_only` | CS/Sales/health use; **must never appear in a client report in any form** | Never in the external read path |
| `non_runtime` | Reference/redirect/frozen — exists in the catalog as governance, not a runnable VM | Operator does not call it |

---

## Hard rules (non-negotiable)

- **Never external, ever:** VM-27 (Health Score), VM-28 (Expansion), VM-29 (Churn), VM-30 (Support Burden), VM-36 (Traffic-Decline churn input), VM-48 (HubSpot), VM-K-HEALTH (capped composite), VM-R-FUSION (coached-dollar), VM-C-POOL (margin pool). Health score / churn risk / expansion score do not surface in client output in any form.
- **All Domain 8 (VM-31–36)** are a binary `has_clicky=true` gate. If false: the VMs **do not exist** in the report — no placeholder, no mention.
- **Segment labels** (`Platform-Embedded`, `Commerce-Active`, etc.) and **fit scores** never appear in client-facing prose, including Peer Benchmarking (Spine §8). Cohort framing is plain-language only.
- **`FULL` is unreachable for economics** — every money VM caps at **STRONG** by Option A even when `Q-PROV-00` returns `COMMERCE_CONFIDENCE=FULL` (see catalog ceiling note / delta D2).
- **Rep dollar-attribution** is gated on rep-identity Tier (Spine §7.1): Tier 2 → names; Tier 1 → `rep_number` only; behavior-only → suppress rep revenue, ship behavior VMs. **Never silently drop unmapped reps** (fabricates a leaderboard).
- **Redirect stubs (not VMs):** VM-16 → VM-C1 · VM-45 → VM-C14/CHAN-1 · VM-38b → VM-38a.

---

## Coverage keys (stamped 2026-06-30)

`COMMERCE` = 6-org probe cohort `cci`(FULL) · `bcf`/`sarreid`(STRONG-gross) · `mhc`(PARTIAL-stale) · `sc`(PARTIAL-incomplete) · `da`(NONE) → headline economics **3 fire / 2 degrade / 1 dark**. `MIXPANEL` = **187/252 (74%)** any behavioral, **146/252 (58%)** active; cohort 5/6 rich, `mhc` dormant. `IDENTITY` = rep-naming tier (cohort 4 Tier-2 / 1 number-only / 1 behavior-only). `OWNED` = MCP/cross-instance, always-on (100%). `CLICKY` = 48 portals. `STACKS` 185/252 · `RESOURCES` 164/252 · `HUBSPOT` 157/252 · `ENROLL` 68/252. `HARD-GAP` = 0/252 (no cost feed). Audience codes: **E** external-safe · **D** dual · **I** internal-only · **C** conditional framing.

---

## Domain 1 — Sales Team Performance (the behavioral moat)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-01 | Rep Behavioral Scorecard | D | A | Mixpanel-coverage; eCat-outcome owned | Q-01 ✅ | active | MIXPANEL |
| VM-03 | Behavioral Funnel Gap | D | A | Mixpanel-coverage | Q-01-derived ✅ | active | MIXPANEL |
| VM-02 | Selling Archetype Classification | D | C | Mixpanel + VM-01 first | Q-01-derived ✅ | active | MIXPANEL |
| VM-04 | Non-Selling User Role Classification | D | D | Mixpanel-coverage | Q-04 ✅ | active | MIXPANEL |
| VM-05 | Seat Utilization | D | C | active-seat roster proxy | Q-05 ✅ | active | MIXPANEL / OWNED |
| VM-06 | Rep Engagement Trajectory | D | C | owned | Q-06 ✅ | active | OWNED |
| VM-43 | Territory Coverage & Dormancy | D | C | territory-format preflight + active-seat | Q-43 ✅ | conditional | OWNED + IDENTITY |
| VM-46 | eCat Selling Workflow Maturity | D | C | Mixpanel-coverage | Q-46 ✅ | conditional | MIXPANEL |

## Domain 2 — Platform & Feature Utilization (instance-health check-engine lights)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-07 | Catalog Completeness Score | D | D | owned (`products`) | Q-07 ✅ | active | OWNED |
| VM-08 | Data Freshness Monitor | D | D | owned (`data_versions`) | Q-08 ✅ | active | OWNED |
| VM-09 | Import Health & Sync Reliability | D | D | owned (`import_events`); N/A Admin-only | Q-09 ✅ | active | OWNED |
| VM-10 | Feature Enablement Gap Analysis | D | D | owned + cross-instance; bundle-aware | Q-10 ✅ | active | OWNED |
| VM-11 | Configuration Completeness | D | D | owned | Q-11 ✅ | active | OWNED |
| VM-47 | Smart Stack Effectiveness | D | D | `smart_stacks>0` + Mixpanel stack events | Q-47 ✅ | conditional | MIXPANEL + STACKS |
| VM-50 | Library / Document Engagement | D–C | D | Mixpanel `view/email_document` present | Q-50 ✅ | conditional | MIXPANEL + RESOURCES |

## Domain 3 — Customer & Buyer Intelligence (eCat-activity cousins + activation)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-12 | eCat Customer Activation & ERP Penetration | D | C | `FEED_COMPLETENESS` + billing-entity | Q-12 ✅ | conditional | COMMERCE 3🟢/2🟡/1🔴 |
| VM-41 | First-Time eCat Orderers | D | C | owned (eCat) | Q-41 ✅ | active | OWNED |
| VM-13 | Customer Concentration Risk (eCat cousin) | D | Cousin | `orders`; twin VM-C3/K2 leads outcome | Q-13 ✅ | active | OWNED (cousin) |
| VM-14 | Customer Reorder Frequency (eCat cousin) | D | Cousin | `orders`; twin K-cadence leads | Q-14 ✅ | active | OWNED (cousin) |
| VM-17 | Dormant eCat Customer (cousin) | D | Cousin | `orders`; twin VM-K8/S1 leads $-at-risk | Q-17 ✅ | active | OWNED (cousin) |
| VM-49 | Buyer-Level Repeat Purchase | D | C | `portal_orders` buyer attribution | Q-49 ✅ | conditional | OWNED (eCat) |
| VM-15 | Enrollment Funnel Analysis | I | D | enrollment enabled | Q-15 ✅ | internal_only | ENROLL |
| VM-44 | Onboarding Velocity | I | D | enrollment; internal-only scope | Q-44 ✅ | internal_only | ENROLL |

## Domain 4 — eCat Commerce Analytics (cousins) + Feature Depth

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-22 | Feature Usage Depth (Behavioral) | D | D | Mixpanel-coverage | Q-22 ✅ | active | MIXPANEL |
| VM-18 | eCat Order Velocity & Trend (cousin) | D | Cousin | `orders`; Part B total is labeled fallback | Q-18 ✅ | active | OWNED (cousin) |
| VM-20 | eCat AOV Analysis (cousin) | D | Cousin | `orders`; never "average deal size" | Q-20 ✅ | active | OWNED (cousin) |
| VM-21 | eCat Order Type & Workflow (cousin) | D | Cousin | `orders`; twin VM-C24 leads | Q-21 ✅ | active | OWNED (cousin) |
| VM-19 | eCat Channel Mix Evolution (cousin) | D | Cousin | `has_cart=true` + server orders | Q-19 ✅ | conditional | OWNED (cousin) |
| VM-45 | eCat Capture Rate vs Total — ⛔ SUPERSEDED | — | — | redirect → VM-C14 / VM-CHAN-1 | — | non_runtime | n/a |

## Domain 5 — Product & Inventory Intelligence

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-40 | Regional Product Intelligence | D | C | `billing_state` (owned) | Q-40 ✅ | active | OWNED |
| VM-37 | Inventory × Sales Intelligence | D | B | `sales_data` + `inventories` | Q-37 ✅ | conditional | OWNED (fires even on NONE org) |
| VM-39 | Line Analysis by Category & Collection | D | C | `sales_data`; per-org category interp | Q-39 ✅ | conditional | OWNED |
| VM-42 | New Item Performance | D | C | `new_item` + `sales_data` | Q-42 ✅ | conditional | OWNED |
| VM-38a | Product Velocity Trend (eCat Orders) | D | C | `portal_order_items` (~52 orgs) | Q-38a ✅ | conditional | OWNED (eCat) |
| VM-38b | Product Velocity Trend (Full) — ⏳ | D | — | needs `invoice_date` on `sales_data` | pending | pending_data | HARD-GAP (pending eng) |

## Domain 6 — Peer Benchmarking (cross-instance, owned)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-23 | Peer Comparison Dashboard | D | C | cross-instance (owned) | Q-CI-02 ✅ | active | OWNED |
| VM-24 | Feature Adoption Benchmarking | D | C | owned | Q-CI-03 ✅ | active | OWNED |
| VM-26 | Best Practice Identification | D | C | owned | Q-CI-05/06 ✅ | active | OWNED |
| VM-25 | Growth Trajectory Comparison | D | C | ≥2 monthly snapshots | Q-CI-02/04 ✅ | conditional | OWNED (≥2 snapshots) |

## Domain 7 — SuperCat Internal Intelligence (all internal-only)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-27 | Account Health Score (Health V2) | I | D | Health V2 operator (authoritative) | operator ✅ | internal_only | OWNED (internal) |
| VM-28 | Expansion Readiness Signals | I | D | BigQuery `insightful_product` | Q-CI-07 ✅ | internal_only | OWNED (internal) |
| VM-29 | Churn Risk (composite) | I | D | composite (lowest input) | Q-CI-01/08 ✅ | internal_only | OWNED (internal) |
| VM-30 | Support Burden Analysis | I | D | HelpScout (~80% match) | Q-HS-01..06 ✅ | internal_only | HelpScout |
| VM-48 | HubSpot Expansion Signals | I | D | HubSpot mapped (`org_id` = shortname) | Q-48 ✅ | internal_only | HUBSPOT (internal-only) |

## Domain 8 — Portal Engagement (Clicky demand-side; `has_clicky=true` binary gate)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-31 | Portal Traffic Health | D | D | `has_clicky=true` | Q-CL-01 ✅ | conditional | CLICKY (48 portals) |
| VM-33 | Geographic Demand Map | D | D | `has_clicky=true` | Q-CL-03 ✅ | conditional | CLICKY |
| VM-35 | Traffic Source Intelligence | D | D | `has_clicky=true` | Q-CL-05 ✅ | conditional | CLICKY |
| VM-32 | Portal Content Performance | D–C | D | `has_clicky` + page-level data | Q-CL-02 ✅ | conditional | CLICKY |
| VM-34 | Visitor Organization Identification | D–C | D | `has_clicky`; corporate-network dependent | Q-CL-04 ✅ | conditional | CLICKY |
| VM-36 | Portal Traffic Decline Signal | I | D | `has_clicky`; churn input → VM-29 | Q-CL-01/CI-08 ✅ | internal_only | CLICKY (internal) |

## Domain 9 — Commerce Economics (the "Money Map," Layer 1)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-C1 | True Topline *(the anchor)* | D | S | `FEED_COMPLETENESS` (suppress incomplete/dead; clamp stale) | Q-PROV-00/ECON-00 ✅ | active | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C2 | Net Realization & Discount Leakage | D | A | `FEED_COMPLETENESS` + tier-aware dispersion + gut-check | Q-ECON-LEAK ✅ | active | COMMERCE 1🟢/3🟡/2🔴 |
| VM-C4 | Booked→Invoiced Conversion & Fill Leakage | D | B | within-line only (no header join) | Q-ECON-FILL ✅ | active | COMMERCE |
| VM-C5 | Returns & Credit-Memo Drag | D | B | `RETURNS_IN_FEED` (suppress silent 0%) | Q-ECON-RETURNS ✅ | conditional | COMMERCE — `bcf`/`sarreid` 🔴 no returns |
| VM-C3 | Revenue Concentration & Single-Account Risk (HHI) | D | A | `FEED_COMPLETENESS` + billing-entity | Q-ECON-CONC ✅ | conditional | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C10 | Comparable-Window Momentum (staleness-proof YoY) | D | A | equal windows ending at `report_through_date` | Q-ECON-MOMENTUM ✅ | conditional | COMMERCE 2🟢/1🟡/3🔴 |
| VM-C7 | Revenue Quality — Recurring vs One-Time | D | B | ≥2 comparable windows | Q-ECON-QUALITY ✅ | conditional | COMMERCE (≥2 windows) |
| VM-C9 | Run-Rate Pacing (a range) | D | B | ≥24 months; band never a point | Q-ECON-PACE ✅ | conditional | COMMERCE (≥24mo) |
| VM-C11 | Revenue Lumpiness / Big-Deal Dependence *(honesty guard)* | D | S | invoice grain | Q-ECON-LUMP ✅ | conditional | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C17 | Net Revenue Retention ($-based) | D | B | ≥2 yrs, stable keys (band if reconciling) | Q-ECON-NRR ✅ | conditional | COMMERCE (≥2yr) |
| VM-C20 | Customer Contribution & Margin Tiering | D | B | inherits C2/C5/C18; "contribution proxy" (no cost) | Q-ECON-CONTRIB ✅ | conditional | COMMERCE (true-margin 🔴 HARD-GAP) |
| VM-C8 | Seasonality & Market-Month Calendar | D | C | ≥2–3 yrs | Q-ECON-SEASON ✅ | conditional | COMMERCE (≥2–3yr) |
| VM-C12 | Price Realization by Account & Off-List | D | C | `net_price` is a meaningful reference | Q-ECON-OFFLIST ✅ | conditional | COMMERCE (cond. on list ref) |
| VM-C13 | Price-Increase Pass-Through | D | C | known increase date + stable item identity | Q-ECON-PASSTHRU ✅ | conditional | COMMERCE (cond.) |
| VM-C14 | eCat Capture / Platform Footprint | D–C | B | rate only at `CORROBORATED`; else absolute $ | Q-45/PROV-00 ✅ | conditional | COMMERCE — abs-$; `sc`🔴 (126%) |
| VM-C16 | Revenue Composition Strip-Out | D | C | itemized freight/tax/discount | Q-ECON-COMPOSITION ✅ | conditional | COMMERCE (`freight_amount` present) |
| VM-C18 | Freight & Small-Order Recovery | D | C | itemized `freight_amount` (recovery % cost-gated) | Q-ECON-FREIGHT ✅ | conditional | COMMERCE (recovery % ⏳) |
| VM-C22 | Geographic Profit Map | D | C | ship-to geo; "contribution" label (no cost) | Q-ECON-GEO ✅ | conditional | COMMERCE (true-margin 🔴) |
| VM-C23 | New-Introduction Revenue Vitality | D | C | derived first-sale date (not stale `new_item`) | Q-ECON-NEWINTRO ✅ | conditional | COMMERCE |
| VM-C24 | Quote-to-Cash Pipeline Value *(pipeline, never sales)* | D | C | per-org `order_type` map | Q-ECON-PIPELINE ✅ | conditional | COMMERCE (cond. on order_type) |
| VM-C15 | Working Capital — Backlog / Lead-Time / Terms | D | C | cohort/distributional lag only | Q-ECON-LEADTIME / Q-ECON-TERMS ✅ *(backlog-aging WCAP 🟡)* | conditional | COMMERCE (distributional) |
| VM-C-POOL | Recoverable Margin Pool (composite) | I | — | deferred until C2/C4/C5/C18 trusted | composite ⏳ | internal_only | COMMERCE (partly HARD-GAP) |
| VM-C19 | Margin Pool & Mix (PVM bridge) — ⏳ | D | Hard-gap | landed `unit_cost` (absent) | ⏳ | pending_data | HARD-GAP 0/252 |
| VM-C21 | Margin-Weighted Concentration — ⏳ | D | Hard-gap | `unit_cost` (absent) | ⏳ | pending_data | HARD-GAP 0/252 |
| VM-C25 | Market & Trade-Show $ ROI — ⏳ | D | Hard-gap | market-coded `order_origin` + client show cost | ⏳ | pending_data | HARD-GAP (no source) |

## Domain 10 — Channel / "Where You Sell"

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-CHAN-1 | eCat vs non-eCat Split (the Headline) | D | B | rate only at `CORROBORATED`; else absolute $ | Q-CHAN-00 ✅ | conditional | COMMERCE — abs-$; `sc`🔴 |
| VM-CHAN-2 | Non-eCat Sub-Channel Decomposition | D | C | `CHANNEL_CONFIDENCE≠NONE` + per-org map | Q-CHAN-DECOMP ✅ | conditional | COMMERCE (cond. on channel map) |
| VM-CHAN-3 | Channel Cannibalization / Conflict | D (internal-lead) | C | CHAN-2 reliability + ≥2 windows; correlational | Q-CHAN-CONFLICT ✅ | conditional | COMMERCE (internal-lead) |

## Domain 11 — Customer Economics (Layer 3, the K-series)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-K8 / S1 | Account-Health $-at-Risk | D | A | `FEED_COMPLETENESS` + equal-window decay | Q-K-RISK ✅ | active | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K-HEADLINE | Revenue-at-Risk / Competitive-Loss Banner | D | B | suppress on PROVABLY-INCOMPLETE topline | Q-K-HEADLINE ✅ | conditional | COMMERCE (`sc`🔴) |
| VM-K1 | Customer Value Ranking | D | B | `FEED_COMPLETENESS` + billing-entity | Q-K1 ✅ | active | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K3 | Account Decline / Churn-Risk | D | B | ≥2 periods | Q-K3 ✅ | active | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K2 | Concentration (customer grain) | D | C | billing-entity | Q-K2 ✅ | conditional | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K4 | New vs Reactivated vs Lapsed | D | C | dated invoice feed | Q-K4 ✅ | active | COMMERCE |
| VM-K6 | Parent / Corporate-Family Roll-Up | D | C | derived "estimated family"; suppress degenerate names | Q-K6 ✅ | conditional | COMMERCE (derived family) |
| VM-K7 | Price-Realization Leakage (customer grain) | D | C | `leakage_dispersion_ok` (≥60% priced lines) + gut-check | Q-K7 ✅ | conditional | COMMERCE (cond. on priced-line %) |
| VM-K-HEALTH | Composite Account Health (capped) | I | — | lowest-input cap; never external | composite ✅ | internal_only | COMMERCE + MIXPANEL |
| VM-K5 | Segment Composition of the Book — 🧊 FROZEN | — | Frozen | segmentation frozen (Spine §8) | Q-SEG-DERIVE ⏳ | non_runtime | n/a — do not ship |

## Domain 12 — Rep Outcome & Copilot (Layer 2, the R-series)

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-R1–R4 | The Behavior Floor (always-on, ERP-optional) | D | B | owned / Mixpanel-coverage — never dark | Q-63/64/65 ✅ | active | MIXPANEL / OWNED |
| VM-R5 | Rep → Revenue Outcome | D | C | rep-identity Tier (2 named / 1 number / 0 suppress) | Q-R5 ✅ | conditional | IDENTITY |
| VM-R6 | Book-of-Business Health by Rep | D | C | rep-identity Tier + billing-entity | Q-R6 ✅ | conditional | IDENTITY + COMMERCE |
| VM-R-PROMPTS | Six Packaged Copilot Prompts | D | C | consumes gated data; identity Tier on rep naming | operator ✅ | conditional | IDENTITY |
| VM-R-FUSION | Coached-Dollar (Tier-2 only, NOT built) | I | — | approved (Option A); juxtapose-not-fuse | ⏳ | internal_only | IDENTITY (not built) |

## Domain 13 — Exception Push ("answers, not dashboards")

| VM | Name | Aud | Tier | Binding gate | Query (readiness) | Runtime status | Live coverage |
|---|---|---|---|---|---|---|---|
| VM-S1 | Account-Health $-at-Risk (the "Quietly-Dying" Alarm) | D | A | `FEED_COMPLETENESS` + equal-window decay *(= VM-K8)* | Q-K-RISK ✅ | active | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C2-rep | Leakage-by-Rep (the "Rogue Discounting" Alarm) | D (internal-lead) | B | rep-identity Tier + dispersion + gut-check | Q-ECON-LEAK + RS-01 ✅ | conditional | IDENTITY + COMMERCE |
| VM-S/C-ROADMAP | Next Exception Types (designed / candidate) | — | — | designed, not built | — | non_runtime | n/a |

---

## Status counts (v4.2, all 13 domains)

96 menu rows total (some VMs appear in two domains by design — VM-K8 and VM-S1 are the same alarm surfaced in both the K-series and the Exception-Push layer).

| Status | Count | VMs |
|---|---|---|
| `active` | 32 | VM-01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 13, 14, 17, 18, 20, 21, 22, 23, 24, 26, 40, 41; VM-C1, C2, C4; VM-K8/S1, K1, K3, K4; VM-R1–R4 *(grouped)*; VM-S1 *(Exception row)* |
| `conditional` | 46 | VM-12, 19, 25, 31, 32, 33, 34, 35, 37, 38a, 39, 42, 43, 46, 47, 49, 50; VM-C3, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C20, C22, C23, C24; VM-CHAN-1, CHAN-2, CHAN-3; VM-K-HEADLINE, K2, K6, K7; VM-R5, R6, R-PROMPTS; VM-C2-rep |
| `pending_query` | 0 | — *(the economics set VM-C3/C7/C8/C9/C10/C11/C17/C20 was authored + live-validated 2026-06-30; see [`query_library_v2.md`](query_library_v2.md) Domain 10)* |
| `pending_data` | 4 | VM-38b (`invoice_date`), VM-C19, C21, C25 (landed `unit_cost` / market cost) |
| `internal_only` | 11 | VM-15, 44, 27, 28, 29, 30, 36, 48; VM-C-POOL, K-HEALTH, R-FUSION |
| `non_runtime` | 3 | VM-45 (redirect → C14), VM-K5 (🧊 frozen), VM-S/C-ROADMAP (designed, not built) |

*(Redirect stubs VM-16 → C1 and VM-38b → 38a are not counted as separate menu rows. `active` + `conditional` = 78 runnable rows; the rest are gated-out, internal, or roadmap.)*

> **As of 2026-06-30 every external economics VM has audited SQL** — the previously-pending set
> (`Q-ECON-CONC/QUALITY/SEASON/PACE/MOMENTUM/LUMP/NRR/CONTRIB`) and `Q-48` (HubSpot, internal-only) were
> authored and live-smoke-tested on cci (org 161) / cfg, so `pending_query` is now empty.
> `pending_data` rows are blocked on a feed that does not exist (the `unit_cost` "one ask" + `invoice_date`
> on `sales_data`) — they are the client/engineering roadmap, not a backlog.
