# Value Moment Catalog v4.2 — Insightful Product 4.0

> ## ⚠️ CAPABILITY / ROADMAP — not executed by `./run.sh`
> **Location:** `foundation/capability/` (shelved 2026-07-13 re-anchor). Do **not**
> load this file to run a report. This 87-VM catalog is a capability/semantic
> roadmap, not a description of what the factory emits. Runtime: **14** signal
> detectors in `pipeline/signals.py`, **24** query IDs in `pipeline/config.py`.
> Ground truth: [`../WHAT_ACTUALLY_RUNS.md`](../WHAT_ACTUALLY_RUNS.md) — **wins on
> any conflict.**

> **Version**: 4.2
> **Status**: Active — **grounded + compressed + uniform** (2026-06-30). Every binding gate is now live-proven against data (not asserted); all 49 Domain 1–8 VMs compressed to the locked Domain-9–13 format; a machine-readable [Master gate table](#master-gate-table-machine-readable-live-coverage-stamped) consolidates tier · ceiling · gate · query-readiness · live coverage. Supersedes v4.1 (in-place evolution; v4.0 snapshot preserved at [`_archive/value_moment_catalog_v4.0_2026-06-29.md`](../_archive/value_moment_catalog_v4.0_2026-06-29.md), v4.2 milestone snapshot at [`_archive/value_moment_catalog_v4.2_2026-06-30.md`](../_archive/value_moment_catalog_v4.2_2026-06-30.md)).
> **Scope**: The original 51 eCat/behavioral VMs (Domains 1–8) **plus** the Intelligence Stack families added in 4.0 — Commerce Economics (Domain 9, C-series), Channel / "Where You Sell" (Domain 10, CHAN-series), Customer Economics (Domain 11, K-series), Rep Outcome & Copilot (Domain 12, R-series + 6 packaged prompts), and the Exception-Push engine (Domain 13, S/C-series). See the Summary Statistics block for current counts.
> **Data readiness**: All VMs queryable or explicitly gated; conditional, cost-gated (`unit_cost`), and pending-engineering variants noted per VM. Economics VMs ride invoiced `net_amount` truth and carry a confidence + completeness stamp or are suppressed.
> **Provenance authority (Tier 0)**: [`../provenance_spine.md`](../provenance_spine.md) governs how truth and confidence are established. Where any VM's denominator, gate, or grain conflicts with the Spine, **the Spine wins**. The 4.0 families also inherit the Tier-1 domain maps ([`../provenance_map_rep.md`](../provenance_map_rep.md), [`../provenance_map_customer.md`](../provenance_map_customer.md)) and the commerce synthesis ([`insights_moneymap_SYNTHESIS.md`](insights_moneymap_SYNTHESIS.md)).
> **The 4.0 through-line (governs every economics/rep/customer VM below)**: a money number ships with a **`COMMERCE_CONFIDENCE` (`Q-ECON-00`/`Q-PROV-00`) + `FEED_COMPLETENESS`** stamp **or it is suppressed**. These VMs are defined as much by **when they refuse to fire** — the FAL case (confidence forcing silence over a wrong number), the `sc` >100%-capture suppression, the WAYFAIR equal-window decay fix — as by what they surface. `FULL` is unreachable for economics (single invoice feed → STRONG ceiling). Rep naming obeys the 3-tier identity gate (Spine §7.1); customer grain is billing-entity (Spine §7.2); segmentation is 🧊 FROZEN (Spine §8).

> ### ✅ v4.2 GROUNDING & COMPRESSION RECONCILIATION (2026-06-30) — read this first
> v4.1 unified the rank and re-gated Domains 1–8, but two gaps remained: the gates were **asserted, not proven**, and Domains 1–8 were still in the long-form pre-4.0 prose while Domains 9–13 were compressed. v4.2 closes both:
> 1. **Every binding gate is live-grounded.** A read-only 2026-06-30 probe reproduced `Q-PROV-00` across a 6-org cohort spanning all five `COMMERCE_CONFIDENCE` states, plus rep-identity tiers, Mixpanel coverage, and a full-population sub-feed census. Evidence: [`build_notes/vm_org_coverage_matrix_2026-06-30.md`](../build_notes/vm_org_coverage_matrix_2026-06-30.md). Headline economics fire on **3 / degrade on 2 / go dark on 1** of the cohort; the behavioral moat (Mixpanel 74% of pop) and eCat cousins are the floor that never goes dark (proven on `da`, a commerce-NONE org).
> 2. **Five claim-accuracy deltas folded in** (none changed a tier or gate): the `CORROBORATED` band carries a coverage guard (a *sparse* second feed can't corroborate); the two different "FULL"s (`COMMERCE_CONFIDENCE` topline vs `FEED_COMPLETENESS` corroboration) are made explicit at the ceiling; `mhc` carries both stale-clamp **and** `DOESNT_CORRELATE`; Register C's `unit_cost` hard-gap is live-re-confirmed (only `freight_amount` exists).
> 3. **Domains 1–8 compressed** to the locked `·`-joined format (punchy Decision line, merged Allowed/Forbidden, one-line examples) — preserving every gate, Forbidden Claim, Health-V2 reconciliation note, Query ID, and the redirect stubs (VM-16/45/38b) verbatim in meaning.
> 4. **One machine-readable [Master gate table](#master-gate-table-machine-readable-live-coverage-stamped)** sits under the Stack Rank: every VM's tier · ceiling · binding gate · `Lib` · **proven live coverage** in a single parse-once block. On any disagreement with a VM body, the rank + gate tables win.
> 5. **The runnable menu is [`vm_runtime_index.md`](vm_runtime_index.md)** — the operational derivative of this catalog: one row per VM (all 13 domains) with `runtime status` (active / conditional / pending_query / pending_data / internal_only / non_runtime), audience, section, gate, and live coverage. The report operator and a human picking VMs for a client read *that*; this catalog stays the capability authority (on conflict, the catalog + Spine win).
> *Scope was format + accuracy + finish-grounding only — no net-new VMs (untapped Mixpanel-depth / HubSpot / Clicky / freight expansion is deferred by owner choice).*

<details>
<summary><strong>📜 Prior-version reconciliation history (v4.1 re-gating + v3 provenance) — click to expand.</strong> Governance trail only; the live rules are the v4.2 note above, the <a href="#unified-stack-rank-v41">Unified Stack Rank</a>, and <a href="provenance_spine.md">provenance_spine.md</a>.</summary>

> ### 🔁 v4.1 STACK-RANK & RE-GATING RECONCILIATION (2026-06-29)
> v4.0 carried two unstated problems: the original **Domains 1–8** (49 eCat/behavioral VMs) were never re-gated against the Spine that Domains 9–13 were born from, and the bottom-of-file **Prioritization Matrix** still listed the **superseded VM-16 and VM-45 as "Tier 1 — Implement Now."** v4.1 closes that seam:
> 1. **One ranking system.** The old Tier-1/2/Conditional **Prioritization Matrix** and the money-map's inline **`Rank N`** tokens are both **superseded by the single [Unified Stack Rank](#unified-stack-rank-v41)** below. It is the authoritative carrier of every VM's **`Stack` tier + `Confidence Ceiling` + binding `Gate`**. Inline `Rank N` tokens in Domains 9–13 are retained only as legacy money-map provenance.
> 2. **The anchor is [VM-C1 True Topline](#vm-c1-true-topline)** — the invoiced-net denominator every money VM inherits confidence from. VM-01 (Rep Behavioral Scorecard) remains a top-tier differentiator but is no longer "the anchor."
> 3. **Domains 1–8 are re-gated** to the Spine's `FEED_COMPLETENESS` / 3-tier rep-identity / billing-entity / returns-in-feed / Mixpanel-coverage rules (see the [Unified Stack Rank](#unified-stack-rank-v41) gate column).
> 4. **Seven eCat VMs are demoted to "intent/activity cousins"** of their invoiced twin (VM-13→C3/K2, VM-14→K-cadence, VM-17→K8/S1, VM-18/19/20/21→Domain-9 economics). **Two-lane rule:** the invoiced twin leads the **commercial-outcome** story (revenue, concentration, decay, realized AOV); the cousin leads the **eCat workflow/adoption** story, and is the only option when no invoice feed exists (see the [Demoted Cousins register](#register-a--demoted-ecat-intent-cousins)). VM-16/VM-45 are pure redirect stubs.
> 5. **Frozen + hard-gap items leave the stack** into non-ranked [Registers](#registers-non-ranked-governance) (segmentation 🧊; margin/AR/claims ⏳) so they stop reading as shippable backlog.

> ### ⚠️ v3 PROVENANCE RECONCILIATION (2026-06-26) — read before running any total/capture VM
> This catalog's original Commerce Ontology equated "total business" with `SUM(portal_orders.total_amount)`. That is **superseded** by [`provenance_spine.md`](provenance_spine.md):
> - **Total business = invoiced net** `SUM(portal_invoices.net_amount)`, source/confidence selected by **`Q-PROV-00`**; `portal_orders` is the **booked/fallback** feed only (Spine §1, §6.1).
> - **Every total carries a `FEED_COMPLETENESS` label** (Spine §6.3). "complete / total business" language is allowed **only when `CORROBORATED`**; otherwise report at STRONG with a completeness caveat. `invoiced ≠ collected` (Spine §6.7).
> - **Capture ≠ attribution** (Spine §4): a capture *rate* (eCat ÷ total) is valid only when `FEED_COMPLETENESS=CORROBORATED` **and** confidence ≥ STRONG; otherwise report **eCat capture in absolute dollars only**.
> - **Rep revenue VMs** are gated on the rep-identity match rate ≥80% (Spine §7.1); **Customer VMs** report at billing-entity grain (Spine §7.2); **no segment labels / fit scores** anywhere external (Spine §8).
> The Commerce Ontology, VM-16, and VM-45 below are reconciled inline; the cross-domain gate addendum follows the Commerce Ontology. The current runnable derivative is [`vm_runtime_index.md`](vm_runtime_index.md) (all 13 domains, with `runtime status`); the legacy [`external_vm_index.md`](../_archive/external_vm_index.md) (original 51 VMs only) is **archived/superseded** and kept for history.

</details>

---

## How to Read This Catalog

Each **value moment** (VM) is a discrete recommendation or insight the Insights Layer can deliver. The schema for each VM is:

| Field | Meaning |
|-------|---------|
| **Audience** | External-safe [E], Internal only [I], Dual [D], or Conditional [C] |
| **Commerce Lens** | eCat transaction / ERP total-business / Comparative capture / Non-commerce |
| **Internal Name** | System/engineering name used in gating and query references |
| **Customer-Facing Name** | Name used in report prose and external claims |
| **Gating** | Feature flags, bundle types, or data conditions required |
| **Signal** | Data sources and query logic |
| **Example** | Real grounding from a validated client account |
| **Action** | What CS or the customer does with this insight |
| **Client value** | Why the customer cares — a one-line decision/benefit, present on every VM |
| **SuperCat value** | Why SuperCat cares — retention / expansion / competitive moat, present on every VM |
| **Segments** | Which bundle types or account profiles benefit |
| **Complexity** | Simple / Moderate / Complex |
| **Data Dependency** | Explicit table names, source system, data readiness |
| **Data Readiness** | Live / Conditional Live / Pending Engineering / Deferred |
| **Bundle Required** | Specific bundle(s) or "All" |
| **Query IDs** | References to query library |
| **Allowed Claims** | What this VM can say — safe for external use if [E] or [D] |
| **Forbidden Claims** | Claims this VM must never make |
| **Portability** | Fully portable / Query portable–interpretation varies / Data-gated |
| **Enhancement Path** | What would expand this VM's capability (where relevant) |
| **Stack** *(v4.1)* | Its tier + position in the [Unified Stack Rank](#unified-stack-rank-v41) (S / A / B / C / D, or a non-ranked register: Cousin / Frozen / Hard-gap) |
| **Confidence Ceiling** *(v4.1)* | The highest tier this VM may claim — **FULL** only for owned behavior with no money number. **Economics VMs cap at STRONG even when `FEED_COMPLETENESS=CORROBORATED`**: booked≈invoiced agreement is *internal* corroboration from one ERP's two tables, not a truly independent second feed, so the catalog deliberately presents one notch below Spine §6.3's "eligible for FULL" (a presentation cap, not a data-state claim — ~14/21 cohort orgs *are* CORROBORATED). Where completeness is unproven the total carries the single-feed caveat; on PROVABLY-INCOMPLETE/DEAD we suppress. **Two distinct signals (don't conflate):** `COMMERCE_CONFIDENCE=FULL` (Q-PROV-00 — the invoiced *topline figure* is clean; reachable, e.g. `cci`) is **not** `FEED_COMPLETENESS=CORROBORATED` (a second feed agrees in-band). A clean topline still presents at **STRONG for economics** because in-band corroboration ≠ an independent feed — so a future reader must not "promote" a `COMMERCE_CONFIDENCE=FULL` org to a FULL economics claim. **Principle: never show a client a number we can't stand behind — caveat or suppress.** |
| **Gate** *(v4.1)* | The single binding gate that decides fire-vs-suppress: `FEED_COMPLETENESS`, rep-identity Tier (Spine §7.1), billing-entity grain (§7.2), `RETURNS_IN_FEED`, Mixpanel-coverage, or "owned / none" |

> **Where the three v4.1 fields live (single definition, everywhere-reference).** `Stack`, `Confidence Ceiling`, and `Gate` are populated **authoritatively, for every VM, in the [Unified Stack Rank](#unified-stack-rank-v41) table** — not duplicated into all 80+ VM bodies. Individual entries carry an inline stamp only where the legacy body text was stale and needed correcting (the re-gated Domain 1–8 VMs and the demoted cousins). When a body and the rank table ever disagree, **the rank table wins.**

**Delivery surface**: Where each VM lives in the product (Admin Console, Sales Portal, Insights Layer, internal CS tooling) is a commercial decision resolved separately from this catalog.

---

## Global Query Guardrail

All queries touching the `orders` table must use the nullable delete guard:

```sql
AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
```

This is not repeated per VM. The `is_marked_deleted` column is nullable — some orgs store `NULL` (meaning "not deleted") rather than `false`. Using `= false` alone silently drops valid orders and understates all eCat metrics.

---

## Commerce Ontology

Every commerce-related VM belongs to one of three lenses. *(v3 reconciled to [`provenance_spine.md`](provenance_spine.md) — the total-business source is now invoiced net, not `portal_orders`.)*

| Lens | Source Table | What It Covers |
|------|-------------|----------------|
| **eCat transaction** | `orders` | iPad + eCat Online orders only. Rep-submitted and buyer self-service eCat orders. *Intent (pre-re-key), not invoiced revenue (Spine §2).* |
| **ERP total-business** | `portal_invoices.net_amount` (**truth**); `portal_orders` (**booked/fallback only**) | The client's total business = **invoiced net** `SUM(portal_invoices.net_amount)`, selected by `Q-PROV-00` (Spine §1/§6.1). `portal_orders` is the *booked* feed across all channels (eCat, phone, EDI, trade shows, showroom) — used only as the fallback (`TOTAL_BUSINESS_SOURCE=ORDERS`) when no invoice feed exists, and then labeled booked-not-invoiced. Never buyer activity. Every figure carries a `FEED_COMPLETENESS` label (Spine §6.3). |
| **Comparative capture** | `orders` (eCat-SALE, Spine §6.5) vs. invoiced total business | eCat share of total business. This is **attribution, not capture** (Spine §4): valid as a *rate* only when `FEED_COMPLETENESS=CORROBORATED` and confidence ≥ STRONG; otherwise report eCat capture in absolute dollars. |

`portal_orders` is never framed as buyer self-service activity. "Self-service" in this catalog means `orders.order_source = 'server'` (B2B Cart / eCat Online ordering) only.

---

## Provenance Gate Addendum (v3) — cross-domain

Inherits from [`provenance_spine.md`](provenance_spine.md) and the Tier-1 domain maps ([`provenance_map_rep.md`](provenance_map_rep.md), [`provenance_map_customer.md`](provenance_map_customer.md)). Applies on top of each VM's own gating.

- **`FEED_COMPLETENESS` (Spine §6.3)** — every total/denominator carries one of CORROBORATED / UNVERIFIED-SINGLE-FEED / PROVABLY-INCOMPLETE / STALE / DEAD. `FULL`/"complete business" language requires CORROBORATED.
- **Rep revenue-attribution gate (Spine §7.1)** — any VM tying a **dollar outcome to a named rep** (e.g. VM-01 per-rep GMV against ERP, VM-05/06/43/46 outcome side) requires rep-identity match ≥80%; 40–80% → `rep_number` only; <40% → suppress rep-level revenue, ship behavior-only. Per-rep eCat GMV from `orders` (owned/behavioral) is always allowed. Never silently drop unmapped reps from a ranking.
- **Mixpanel-coverage gate** — Mixpanel-dependent VMs degrade to login/order effort when coverage is absent; never fabricate engagement.
- **Active-rep roster** — reps = iPad-active seats (`org_users.last_ipad_login_at IS NOT NULL`) ∪ order authors, not raw `org_users` (conflates B2B buyers).
- **Customer grain (Spine §7.2)** — customer VMs report at **billing-entity** grain; no native parent key exists (`mapped_code` ~0%), so parent/family roll-ups are derived + gated and labeled "estimated family."
- **No segment labels / fit scores externally (Spine §8)** — segments are derived from first-party behavior per [`segmentation_derivation.md`](segmentation_derivation.md); the TAM CSV enrichment block (columns BH–BO: `FIT_*`/`Segment_Opus_*`) is excluded as input, validated against only.

---

## Unified Stack Rank (v4.1)

> **This is the single source of priority truth.** It replaces both the legacy "Prioritization Matrix" (Tier 1/2/Conditional/Deferred) and the money-map's inline `Rank N` tokens. Every active VM appears here exactly once, with its **tier**, **Confidence Ceiling**, and **binding Gate**. The detailed VM bodies below are the *spec*; this table is the *rank + gate authority*. On any disagreement, **this table wins.**

### The scoring rubric

Each VM is scored on five factors (1–5). **Confidence-survivability is weighted heaviest (×1.2)** — surviving the Spine's gates across the cohort *is* the product thesis; coverage is ×0.8; the rest ×1.0. Composite is out of 25.

| Factor | Weight | Rewards |
|---|---|---|
| **Action proximity** | ×1.0 | drives a named decision/dollar, not a dashboard |
| **Dollar materiality** | ×1.0 | size of money moved or protected |
| **Confidence survivability** | **×1.2** | how often it survives `FEED_COMPLETENESS` + identity + hard-gaps across the 21–22-org cohort |
| **Coverage / portability** | ×0.8 | how many orgs can actually run it |
| **Differentiation** | ×1.0 | does a competitor have it (behavioral data = moat) |

### Tier definitions

| Tier | Meaning |
|---|---|
| **S** | The spine — run first; every other money VM inherits its confidence. |
| **A** | Headline client value — high $, survives the gates, broad coverage. |
| **B** | Strong, slightly narrower or more gated. |
| **C** | Useful, conditional, or derivative of a higher VM. |
| **D** | Internal / instance-health / ops — real, but not a client headline. |
| *(register)* | **Cousin** / **Frozen** / **Hard-gap** — non-ranked; see [Registers](#registers-non-ranked-governance). |

> **`Lib` = query-readiness** (priority ≠ implementation status; a high tier is the *value* claim, `Lib` is whether the audited SQL exists today): **✅ live** in `query_library_v2.md` · **🟡 pending** (designed; SQL not yet authored/audited — inherits C1's `Q-ECON-00` denominator) · **⏳ gated** on cost/client input. Authority for economics rows is the Domain-9 Query-ID Reconciliation table.

### Tier S — the spine

| VM | Name | Domain | Score | Confidence Ceiling | Binding Gate | Lib |
|---|---|---|---|---|---|---|
| **VM-C1** | **True Topline** *(the anchor)* | 9 | **22.2** | STRONG | `FEED_COMPLETENESS` (suppress PROVABLY-INCOMPLETE/DEAD; clamp STALE) | ✅ |
| **VM-C11** | Revenue Lumpiness / Big-Deal Dependence | 9 | **20.0** | STRONG | `FEED_COMPLETENESS` (invoice grain; the honesty guard — rarely suppressed itself) | 🟡 |

### Tier A — headline value

| VM | Name | Domain | Score | Confidence Ceiling | Binding Gate | Lib |
|---|---|---|---|---|---|---|
| **VM-01** | Rep Behavioral Scorecard *(the moat)* | 1 | 21.8 | FULL (behavior) | Mixpanel-coverage (CORROBORATED 20/21); eCat-outcome owned | ✅ |
| **VM-03** | Behavioral Funnel Gap *(the ROI story)* | 1 | 21.8 | FULL (behavior) | Mixpanel-coverage | ✅ |
| **VM-K8 / S1** | Account-Health $-at-Risk | 11/13 | 21.0 | STRONG | `FEED_COMPLETENESS` + equal-window decay (suppress NONE; floor PARTIAL) | ✅ |
| **VM-C3** | Revenue Concentration & Single-Account Risk (HHI) | 9 | 20.0 | STRONG | `FEED_COMPLETENESS` + billing-entity grain | 🟡 |
| **VM-C2** | Net Realization & Discount Leakage | 9 | 20.0 | STRONG | `FEED_COMPLETENESS` + tier-aware dispersion + human gut-check | ✅ |
| **VM-C10** | Comparable-Window Momentum (staleness-proof YoY) | 9 | 19.0 | STRONG | `FEED_COMPLETENESS` + equal windows ending at `report_through_date` | 🟡 |

### Tier B — strong, narrower or more gated

| VM | Name | Domain | Confidence Ceiling | Binding Gate | Lib |
|---|---|---|---|---|---|
| VM-C7 | Revenue Quality — Recurring vs One-Time | 9 | STRONG | ≥2 comparable windows | 🟡 |
| VM-K-HEADLINE | Revenue-at-Risk / Competitive-Loss Banner | 11 | STRONG | suppress on PROVABLY-INCOMPLETE topline | ✅ |
| VM-C4 | Booked→Invoiced Conversion & Fill Leakage | 9 | STRONG | within-line only (no header join) | ✅ |
| VM-C5 | Returns & Credit-Memo Drag | 9 | STRONG | `RETURNS_IN_FEED` (suppress silent 0%) | ✅ |
| VM-C9 | Run-Rate Pacing (a range) | 9 | STRONG | ≥24 months; band never a point | 🟡 |
| VM-C2-rep | Leakage-by-Rep (exception) | 13 | STRONG | rep-identity Tier + dispersion + gut-check | ✅ |
| VM-CHAN-1 / VM-C14 | eCat vs non-eCat Split / Capture | 10/9 | STRONG | rate only at `FEED_COMPLETENESS=CORROBORATED`; else absolute $ | ✅ |
| VM-K1 | Customer Value Ranking | 11 | STRONG | `FEED_COMPLETENESS` + billing-entity | ✅ |
| VM-K3 | Account Decline / Churn-Risk | 11 | STRONG | ≥2 periods | ✅ |
| VM-37 | Inventory × Sales Intelligence | 5 | STRONG | `sales_data` + `inventories` | ✅ |
| VM-C17 | Net Revenue Retention ($-based) | 9 | STRONG | ≥2 yrs, stable keys (band if reconciling) | 🟡 |
| VM-C20 | Customer Contribution & Margin Tiering | 9 | STRONG | inherits C2/C5/C18; "contribution proxy" label (no cost) | 🟡 |
| VM-R1–R4 | Rep Behavior Floor (always-on) | 12 | FULL (owned) | owned / Mixpanel-coverage — never dark | ✅ |

### Tier C — useful, conditional, or derivative

| VM | Name | Domain | Confidence Ceiling | Binding Gate |
|---|---|---|---|---|
| VM-02 | Selling Archetype Classification | 1 | FULL | Mixpanel + VM-01 first |
| VM-05 | Seat Utilization | 1 | FULL | active-seat roster proxy |
| VM-06 | Rep Engagement Trajectory | 1 | FULL | owned |
| VM-43 | Territory Coverage & Dormancy | 1 | STRONG | territory-format preflight + active-seat |
| VM-46 | eCat Selling Workflow Maturity | 1 | STRONG | Mixpanel-coverage |
| VM-12 | eCat Customer Activation & ERP Penetration | 3 | STRONG | `FEED_COMPLETENESS` + billing-entity |
| VM-41 | First-Time eCat Orderers | 3 | FULL (eCat owned) | owned |
| VM-R5 | Rep → Revenue Outcome | 12 | STRONG | rep-identity Tier (2 named / 1 number / 0 suppress) |
| VM-R6 | Book-of-Business Health by Rep | 12 | STRONG | rep-identity Tier + billing-entity |
| VM-R-PROMPTS | Six Packaged Copilot Prompts | 12 | STRONG | consumes gated data; identity Tier on rep naming |
| VM-C8 | Seasonality & Market-Month Calendar | 9 | STRONG | ≥2–3 yrs |
| VM-C12 | Price Realization by Account & Off-List | 9 | STRONG (cond.) | `net_price` is a meaningful reference |
| VM-C13 | Price-Increase Pass-Through | 9 | STRONG (cond.) | known increase date + stable item identity |
| VM-C16 | Revenue Composition Strip-Out | 9 | STRONG | itemized freight/tax/discount components |
| VM-C18 | Freight & Small-Order Recovery | 9 | STRONG | itemized `freight_amount` (recovery % cost-gated) |
| VM-C22 | Geographic Profit Map | 9 | STRONG | ship-to geo; "contribution" label without cost |
| VM-C23 | New-Introduction Revenue Vitality | 9 | STRONG | derived first-sale date (not stale `new_item` flag) |
| VM-C24 | Quote-to-Cash Pipeline Value | 9 | PARTIAL | per-org `order_type` map; label "pipeline," never sales |
| VM-C15 | Working Capital — Backlog Aging | 9 | PARTIAL | cohort/distributional lag only |
| VM-K2 | Concentration (customer grain) | 11 | STRONG | billing-entity |
| VM-K4 | New vs Reactivated vs Lapsed | 11 | STRONG | dated invoice feed |
| VM-K6 | Parent / Corporate-Family Roll-Up | 11 | PARTIAL | derived "estimated family"; suppress degenerate names |
| VM-K7 | Price-Realization Leakage (customer grain) | 11 | STRONG (directional) | `leakage_dispersion_ok` (≥60% priced lines) + gut-check |
| VM-CHAN-2 | Non-eCat Sub-Channel Decomposition | 10 | STRONG (cond.) | `CHANNEL_CONFIDENCE≠NONE` + maintained per-org map |
| VM-CHAN-3 | Channel Cannibalization / Conflict | 10 | PARTIAL (internal-lead) | CHAN-2 reliability + ≥2 windows; correlational |
| VM-23 | Peer Comparison Dashboard | 6 | STRONG | cross-instance (owned) |
| VM-24 | Feature Adoption Benchmarking | 6 | STRONG | owned |
| VM-25 | Growth Trajectory Comparison | 6 | STRONG | ≥2 snapshots |
| VM-26 | Best Practice Identification | 6 | STRONG | owned |
| VM-40 | Regional Product Intelligence | 5 | STRONG | `billing_state` (owned) |
| VM-42 | New Item Performance | 5 | STRONG (cond.) | `new_item` + `sales_data` |
| VM-39 | Line Analysis by Category & Collection | 5 | STRONG (cond.) | `sales_data`; per-org category interpretation |
| VM-38a | Product Velocity Trend (eCat Orders) | 5 | STRONG (cond.) | `portal_order_items` |
| VM-49 | Buyer-Level Repeat Purchase | 3 | STRONG (cond.) | `portal_orders` buyer attribution |

### Tier D — internal / instance-health / ops

| VM | Name | Domain | Confidence Ceiling | Binding Gate |
|---|---|---|---|---|
| VM-22 | Feature Usage Depth (Behavioral) | 4 | FULL | Mixpanel-coverage |
| VM-07 | Catalog Completeness Score | 2 | FULL | owned (`products`) |
| VM-08 | Data Freshness Monitor | 2 | FULL | owned (`data_versions`) |
| VM-09 | Import Health & Sync Reliability | 2 | FULL | owned (`import_events`) |
| VM-10 | Feature Enablement Gap Analysis | 2 | FULL | owned + cross-instance |
| VM-11 | Configuration Completeness | 2 | FULL | owned |
| VM-47 | Smart Stack Effectiveness | 2 | STRONG | Mixpanel-coverage (per-stack pending) |
| VM-50 | Library / Document Engagement | 2 | STRONG | Mixpanel-coverage (conditional) |
| VM-27 | Account Health Score (Health V2) | 7 | internal | Health V2 operator (authoritative) |
| VM-28 | Expansion Readiness Signals | 7 | internal | BigQuery `insightful_product` |
| VM-29 | Churn Risk (composite) | 7 | internal | composite (lowest input) |
| VM-30 | Support Burden Analysis | 7 | internal | HelpScout |
| VM-48 | HubSpot Expansion Signals | 7 | internal | HubSpot |
| VM-31–36 | Portal & Demand-Side (Clicky) | 8 | STRONG (cond.) | `has_clicky = true` |
| VM-04 | Non-Selling User Role Classification | 1 | FULL | Mixpanel-coverage |
| VM-15 | Enrollment Funnel Analysis | 3 | internal | enrollment enabled |
| VM-44 | Onboarding Velocity | 3 | internal | enrollment |
| VM-C-POOL | Recoverable Margin Pool (composite) | 9 | internal (lowest input) | deferred until C2/C4/C5/C18 trusted |
| VM-K-HEALTH | Composite Account Health (capped) | 11 | internal | lowest-input cap; never external |
| VM-R-FUSION | Coached-Dollar | 12 | internal, Tier-2 only | approved (Option A), NOT built; juxtapose-not-fuse |

> **Query-readiness for Tiers C/D** (not columned to keep the long tail legible): economics rows follow the Domain-9 Query-ID Reconciliation table — as of **2026-06-30** the previously-pending economics set (**VM-C3/C7/C8/C9/C10/C11/C17/C20**) is **✅ authored + live-validated** (`Q-ECON-CONC/QUALITY/SEASON/PACE/MOMENTUM/LUMP/NRR/CONTRIB`, all smoke-tested on cci org 161); the only economics rows still gated are the **cost-gated** VM-C19/C21/C25 (`unit_cost` — a confirmed hard gap). Behavioral, instance-health, benchmarking, and Clicky VMs are **✅ owned/live**; VM-43/44/46/47/49/50 are **live** (VM-44 internal-only scope; VM-46/47/49/50 conditional — per-stack/per-doc Mixpanel or `portal_orders` sub-gates). **VM-48 (HubSpot) is now ✅ live** (`Q-48`, internal-only, validated 2026-06-30). Internal composites (VM-27/28/29, C-POOL, K-HEALTH, R-FUSION) ride their operator/inputs.

### Master gate table (machine-readable, live-coverage-stamped)

> **One parse-once block.** Consolidates every active VM's `tier` · `ceiling` · binding `gate` · `Lib` (query-readiness) from the tier tables above, and adds the **live coverage** proven by the 2026-06-30 grounding probe ([coverage matrix](../build_notes/vm_org_coverage_matrix_2026-06-30.md)). On any disagreement with a VM body, **this table and the tier tables win**. Coverage keys are defined once below; per-org detail is in the matrix.
>
> **Coverage keys** — `COMMERCE` = 6-org probe cohort `cci`(FULL) · `bcf`/`sarreid`(STRONG-gross) · `mhc`(PARTIAL-stale) · `sc`(PARTIAL-incomplete) · `da`(NONE) → headline economics fire **3 / degrade 2 / dark 1**. `MIXPANEL` = **187/252 orgs (74%)** any behavioral, **146/252 (58%)** active; probe cohort 5/6 rich, `mhc` dormant. `IDENTITY` = rep-naming tier; cohort **4 Tier-2 named / 1 number-only (`sc`) / 1 behavior-only (`da`)**. `OWNED` = MCP/cross-instance, **always-on (100%)**. `CLICKY` = 48 portals (eCat-Online subset). `STACKS` 185/252 (73%) · `RESOURCES` 164/252 (65%) · `HUBSPOT` 157/252 (62%) · `ENROLL` 68/252 (27%). `HARD-GAP` = 0/252 (no cost feed).

| VM | Tier | Ceiling | Binding gate | Lib | Live coverage (2026-06-30) |
|---|---|---|---|---|---|
| VM-C1 | S | STRONG | `FEED_COMPLETENESS` (suppress incomplete/dead; clamp stale) | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C11 | S | STRONG | `FEED_COMPLETENESS` (invoice grain; honesty guard) | 🟡 | COMMERCE 3🟢/2🟡/1🔴 |
| VM-01 | A | FULL (behavior) | Mixpanel-coverage (eCat-outcome owned) | ✅ | MIXPANEL |
| VM-03 | A | FULL (behavior) | Mixpanel-coverage | ✅ | MIXPANEL |
| VM-K8/S1 | A | STRONG | `FEED_COMPLETENESS` + equal-window decay | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C3 | A | STRONG | `FEED_COMPLETENESS` + billing-entity grain | 🟡 | COMMERCE 3🟢/2🟡/1🔴 |
| VM-C2 | A | STRONG | `FEED_COMPLETENESS` + tier-aware dispersion + gut-check | ✅ | COMMERCE 1🟢/3🟡/2🔴 |
| VM-C10 | A | STRONG | `FEED_COMPLETENESS` + equal windows ending at `report_through_date` | 🟡 | COMMERCE 2🟢/1🟡/3🔴 (`mhc` stale breaks YoY) |
| VM-C7 | B | STRONG | ≥2 comparable windows | 🟡 | COMMERCE (needs ≥2 windows) |
| VM-K-HEADLINE | B | STRONG | suppress on PROVABLY-INCOMPLETE topline | ✅ | COMMERCE 3🟢/2🟡/1🔴 (`sc`🔴) |
| VM-C4 | B | STRONG | within-line only (no header join) | ✅ | COMMERCE |
| VM-C5 | B | STRONG | `RETURNS_IN_FEED` (suppress silent 0%) | ✅ | COMMERCE — `bcf`/`sarreid` 🔴 no returns in feed |
| VM-C9 | B | STRONG | ≥24 months; band never a point | 🟡 | COMMERCE (≥24mo) |
| VM-C2-rep | B | STRONG | rep-identity Tier + dispersion + gut-check | ✅ | IDENTITY + COMMERCE |
| VM-CHAN-1/C14 | B | STRONG | rate only at `FEED_COMPLETENESS=CORROBORATED`; else absolute $ | ✅ | COMMERCE — abs-$ on all cohort; `sc`🔴 (126%) |
| VM-K1 | B | STRONG | `FEED_COMPLETENESS` + billing-entity | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K3 | B | STRONG | ≥2 periods | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-37 | B | STRONG | `sales_data` + `inventories` | ✅ | OWNED (fires even on `da`/NONE) |
| VM-C17 | B | STRONG | ≥2 yrs, stable keys (band if reconciling) | 🟡 | COMMERCE (≥2yr) |
| VM-C20 | B | STRONG | inherits C2/C5/C18; "contribution proxy" (no cost) | 🟡 | COMMERCE (true-margin half 🔴 HARD-GAP) |
| VM-R1–R4 | B | FULL (owned) | owned / Mixpanel-coverage — never dark | ✅ | MIXPANEL / OWNED (floor) |
| VM-02 | C | FULL | Mixpanel + VM-01 first | ✅ | MIXPANEL |
| VM-05 | C | FULL | active-seat roster proxy | ✅ | MIXPANEL / OWNED |
| VM-06 | C | FULL | owned | ✅ | OWNED |
| VM-43 | C | STRONG | territory-format preflight + active-seat | ✅ | OWNED + IDENTITY |
| VM-46 | C | STRONG | Mixpanel-coverage | ✅ | MIXPANEL |
| VM-12 | C | STRONG | `FEED_COMPLETENESS` + billing-entity | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-41 | C | FULL (eCat owned) | owned | ✅ | OWNED |
| VM-R5 | C | STRONG | rep-identity Tier (2 named / 1 number / 0 suppress) | ✅ | IDENTITY |
| VM-R6 | C | STRONG | rep-identity Tier + billing-entity | ✅ | IDENTITY + COMMERCE |
| VM-R-PROMPTS | C | STRONG | consumes gated data; identity Tier on rep naming | ✅ | IDENTITY |
| VM-C8 | C | STRONG | ≥2–3 yrs | 🟡 | COMMERCE (≥2–3yr) |
| VM-C12 | C | STRONG (cond.) | `net_price` is a meaningful reference | ✅ | COMMERCE (cond. on list ref) |
| VM-C13 | C | STRONG (cond.) | known increase date + stable item identity | ✅ | COMMERCE (cond.) |
| VM-C16 | C | STRONG | itemized freight/tax/discount components | ✅ | COMMERCE (`freight_amount` present) |
| VM-C18 | C | STRONG | itemized `freight_amount` (recovery % cost-gated) | ✅ | COMMERCE (recovery % ⏳ cost-gated) |
| VM-C22 | C | STRONG | ship-to geo; "contribution" label without cost | ✅ | COMMERCE (true-margin half 🔴 HARD-GAP) |
| VM-C23 | C | STRONG | derived first-sale date (not stale `new_item`) | ✅ | COMMERCE |
| VM-C24 | C | PARTIAL | per-org `order_type` map; label "pipeline" | ✅ | COMMERCE (cond. on order_type map) |
| VM-C15 | C | PARTIAL | cohort/distributional lag only | 🟡 | COMMERCE (distributional only) |
| VM-K2 | C | STRONG | billing-entity | ✅ | COMMERCE 3🟢/2🟡/1🔴 |
| VM-K4 | C | STRONG | dated invoice feed | ✅ | COMMERCE |
| VM-K6 | C | PARTIAL | derived "estimated family"; suppress degenerate names | ✅ | COMMERCE (derived family) |
| VM-K7 | C | STRONG (directional) | `leakage_dispersion_ok` (≥60% priced lines) + gut-check | ✅ | COMMERCE (cond. on priced-line %) |
| VM-CHAN-2 | C | STRONG (cond.) | `CHANNEL_CONFIDENCE≠NONE` + per-org map | ✅ | COMMERCE (cond. on channel map) |
| VM-CHAN-3 | C | PARTIAL (internal-lead) | CHAN-2 reliability + ≥2 windows; correlational | ✅ | COMMERCE (internal-lead) |
| VM-23 | C | STRONG | cross-instance (owned) | ✅ | OWNED |
| VM-24 | C | STRONG | owned | ✅ | OWNED |
| VM-25 | C | STRONG | ≥2 snapshots | ✅ | OWNED (≥2 snapshots) |
| VM-26 | C | STRONG | owned | ✅ | OWNED |
| VM-40 | C | STRONG | `billing_state` (owned) | ✅ | OWNED |
| VM-42 | C | STRONG (cond.) | `new_item` + `sales_data` | ✅ | OWNED (cond.) |
| VM-39 | C | STRONG (cond.) | `sales_data`; per-org category interpretation | ✅ | OWNED (cond.) |
| VM-38a | C | STRONG (cond.) | `portal_order_items` | ✅ | OWNED (eCat) |
| VM-49 | C | STRONG (cond.) | `portal_orders` buyer attribution | ✅ | OWNED (eCat, cond.) |
| VM-22 | D | FULL | Mixpanel-coverage | ✅ | MIXPANEL |
| VM-07 | D | FULL | owned (`products`) | ✅ | OWNED |
| VM-08 | D | FULL | owned (`data_versions`) | ✅ | OWNED |
| VM-09 | D | FULL | owned (`import_events`) | ✅ | OWNED |
| VM-10 | D | FULL | owned + cross-instance | ✅ | OWNED |
| VM-11 | D | FULL | owned | ✅ | OWNED |
| VM-47 | D | STRONG | Mixpanel-coverage (per-stack pending) | ✅ | MIXPANEL + STACKS |
| VM-50 | D | STRONG | Mixpanel-coverage (conditional) | ✅ | MIXPANEL + RESOURCES |
| VM-27 | D | internal | Health V2 operator (authoritative) | ✅ | OWNED (internal) |
| VM-28 | D | internal | BigQuery `insightful_product` | ✅ | OWNED (internal) |
| VM-29 | D | internal | composite (lowest input) | ✅ | OWNED (internal) |
| VM-30 | D | internal | HelpScout | ✅ | HelpScout (~80% match) |
| VM-48 | D | internal | HubSpot | 🟡 | HUBSPOT (Q-48 pending) |
| VM-31–36 | D | STRONG (cond.) | `has_clicky = true` | ✅ | CLICKY (48 portals) |
| VM-04 | D | FULL | Mixpanel-coverage | ✅ | MIXPANEL |
| VM-15 | D | internal | enrollment enabled | ✅ | ENROLL |
| VM-44 | D | internal | enrollment | ✅ | ENROLL |
| VM-C-POOL | D | internal (lowest input) | deferred until C2/C4/C5/C18 trusted | ⏳ | COMMERCE (composite; partly HARD-GAP) |
| VM-K-HEALTH | D | internal | lowest-input cap; never external | ✅ | COMMERCE + MIXPANEL (capped) |
| VM-R-FUSION | D | internal, Tier-2 only | approved (Option A), NOT built; juxtapose-not-fuse | ⏳ | IDENTITY (not built) |
| VM-C19 | Hard-gap | — | `unit_cost` (absent) | ⏳ | HARD-GAP 0/252 |
| VM-C21 | Hard-gap | — | `unit_cost` (absent) | ⏳ | HARD-GAP 0/252 |
| VM-C25 | Hard-gap | — | market-coded `order_origin` + client show cost | ⏳ | HARD-GAP (no source) |
| VM-K5 | Frozen 🧊 | — | segmentation frozen (Spine §8) | ⏳ | n/a — do not ship |

> **Cousins (Register A, non-ranked):** VM-13/14/17/18/19/20/21 are eCat-intent activity twins — they **fire wherever `orders` exists (OWNED), and are the sole commercial view on a NONE org like `da`**, but never lead a commercial-outcome number when their invoiced twin is live. **Redirect stubs:** VM-16 → VM-C1; VM-45 → VM-C14/CHAN-1; VM-38b → VM-38a (not VMs).

---

## Registers (non-ranked governance)

*These do not compete in the stack. They are governance/roadmap, not priority.*

### Register A — Demoted eCat-intent cousins

The eCat-order versions of insights that now have a sharper invoiced twin. **They are intent/activity, not invoiced outcome.** **Two-lane rule:** the **invoiced twin leads the commercial-outcome story** (revenue, concentration, decay, realized value); the **cousin leads the eCat workflow/adoption story**, and is the only option when no invoice feed exists. Never let a cousin carry a commercial-outcome number when its invoiced twin is available. Each carries a cousin banner in its body below.

| Cousin (eCat intent) | Invoiced twin (leads commercial outcome) | The cousin's own lane (eCat workflow/adoption) |
|---|---|---|
| **VM-13** Customer Concentration Risk (eCat) | [VM-C3](#vm-c3-revenue-concentration--single-account-risk-hhi) / [VM-K2](#vm-k2-concentration--single-account-risk-customer-grain) | eCat-channel concentration overlay; sole view when no invoice feed |
| **VM-14** Customer Reorder Frequency (eCat) | K-series cadence (CQ-07/08), behind [VM-K3](#vm-k3-account-decline--churn-risk) | eCat reorder velocity / platform engagement; sole view when no invoice feed |
| **VM-17** Dormant eCat Customer | [VM-K8 / S1](#vm-s1-account-health--at-risk-the-quietly-dying-alarm) | eCat reactivation list (useful on its own); $-at-risk is the twin's |
| **VM-18** eCat Order Velocity & Trend | Domain-9 invoiced economics | eCat platform health / adoption trend (Part A); Part B "total" is a labeled fallback |
| **VM-19** eCat Channel Mix Evolution | [VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline) | iPad-vs-eOL mix *within* eCat for `has_cart` orgs tuning self-service |
| **VM-20** eCat AOV Analysis | invoiced AOV (Domain 9) | eCat workflow/quote-vs-confirmed tuning (never "average deal size") |
| **VM-21** eCat Order Type & Workflow | [VM-C24](#vm-c24-quote-to-cash-pipeline-value-ecat-pipeline-never-sales) | eCat workflow-adoption coaching |

**Redirect stubs (not VMs — reference only):** VM-16 → [VM-C1](#vm-c1-true-topline) · VM-45 → [VM-C14](#vm-c14-ecat-capture--platform-footprint) / [VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline).

### Register B — Frozen 🧊

| Item | Why | Rule |
|---|---|---|
| **VM-K5** Segment Composition of the Book | Segmentation is the program's final step (Spine §8, owner directive 2026-06-29) | **Do not advance, cluster, label, or ship.** `Q-SEG-DERIVE` is frozen. Method preserved in [`segmentation_derivation.md`](segmentation_derivation.md), validation-only. |
| Any imposed customer-type label / fit score | Biasing; TAM `FIT_*`/`Segment_Opus_*` excluded as input (Spine §8) | Derive from first-party behavior only, **when unfrozen**. |

### Register C — Hard-gap roadmap ⏳ (never viable until a feed lands)

Schema-confirmed absent (full `information_schema` scan, Spine §6.9; **re-verified live 2026-06-30** — the only cost-adjacent column on any economics table is `portal_invoices.freight_amount`; no `unit_cost`/COGS/landed-cost/margin column exists). **Suppress with a one-line "no source" note — never approximate.** This is the "what to ask the client for" roadmap, not a backlog.

| Wanted insight | Blocked on | The unlock |
|---|---|---|
| **VM-C19** Margin Pool & Mix (PVM bridge) | landed `unit_cost` per item-period | **the one ask** — one column lights up C19/C21 + the true-margin halves of C20/C22 |
| **VM-C21** Margin-Weighted Concentration | `unit_cost` | suppress whenever C19 is suppressed |
| **VM-C25** Market & Trade-Show $ ROI | market-coded `order_origin` **and** client-supplied show cost | suppress without both |
| True / gross net margin | COGS / landed cost, freight cost, claims, rebates | `Q-ECON-NETREV` is net-of-freight, **not** margin |
| AR / DSO / collections / credit risk | an AR / cash-receipt feed (none in schema) | every Total is **invoiced, not collected** (Spine §6.7) |
| Damage / claims by carrier / lane | freight/carrier + claims feeds | carrier analytics = freight $/shipments only |
| Quoted lead-time miss, inventory aging | reliable forward inventory + lead-time feed | — |

---

## Domain 1 — Rep Performance Intelligence

*A top-tier capability of the Insights Layer (the behavioral moat; see [Unified Stack Rank](#unified-stack-rank-v41) — VM-01/VM-03 are Tier A). The menu **anchor** is [VM-C1 True Topline](#vm-c1-true-topline), not this domain. The behavioral correlation model reported **r > 0.96 for customer targeting on the BCF validation org** — a single-account result; cohort-broadening is pending before it is stated as a general claim. Full analysis in `03_rep_performance_intelligence.md`.*

---

### VM-01: Rep Behavioral Scorecard

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: rep_behavioral_scorecard · **Customer-Facing Name**: Sales Team Performance Report

**Client value**: Evidence-based per-rep coaching — see exactly where each rep is strong and where a training dollar has the highest ROI, not intuition. · **SuperCat value**: Highest action-proximity insight and the strongest competitive moat (no competitor ties per-rep behavior to order outcomes); opens CPQ / seat-expansion conversations.

**Decision**: *"Here's exactly how each rep sells — six behavioral dimensions tied to order outcomes — so coaching is evidence-based, not intuition."* The catalog's highest action-proximity insight and the strongest competitive moat (no competitor ties per-rep behavior to outcomes).

**Gating**: Mixpanel behavioral data present (active iPad users; live coverage 187/252 orgs, CORROBORATED 20/21 cohort). Catalog-only orgs → substitute engagement proxies (library views, PDF generation, discovery depth) for order outcomes.

**Signal**: per-rep Mixpanel event counts (38 behavioral counters) mapped to the six-dimension model — Customer Targeting, Product Discovery, Configuration & Bundling, Presentation & Communication, Information & Planning, Engagement Depth — cross-referenced with `orders` outcomes (count, GMV, unique customers, AOV).

**Example** *(BCF — validated)*: **Todd Teague Q4 2025** — Targeting 10.5/order (peer 14.2, efficient), Discovery 98.9/order (peer 85.3, thorough), Presentation 32.0 (peer 8.1, standout); outcome 26 eCat orders, $148K GMV, 10 customers, $5,683 AOV.

**Complexity**: Complex · **Data Dependency**: BigQuery `user_feature_usage_report` + MCP `orders` · **Data Readiness**: Live · **Bundle**: any `eCat iPad` · **Query IDs**: Q-01, Q-18 Part A

**Allowed Claims**: behavioral usage profile; per-rep coaching opportunities; per-rep eCat GMV/order count/AOV/customer count. **Forbidden Claims**: "net-new customers" · total-business GMV attributed to rep behavior · non-eCat order outcomes.

**Who pays**: Sales managers / CS (QBR). **Portability**: fully portable (Mixpanel shortname + `orders` org_id standardized).

---

### VM-02: Selling Archetype Classification

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: selling_archetype_classification · **Customer-Facing Name**: Sales Team Archetype Report

**Client value**: Replaces one-size-fits-all coaching with archetype-specific development (don't train a deep-account specialist on breadth). · **SuperCat value**: Demonstrates platform-intelligence depth; the QBR "aha moment" that justifies the Insights Layer price.

**Decision**: *"Your reps fall into distinct selling styles — coach to the archetype, and model the whole team on the most scalable one."* Creates the QBR "aha" that justifies the Insights Layer.

**Gating**: VM-01 first; ≥3 active selling reps for meaningful clustering.

**Signal** (derived from Q-01): cluster analysis on VM-01's behavioral dimensions vs eCat outcomes → named selling styles.

**Example** *(BCF — validated)*: Deep-Account Specialist (Barbara Harper, 58 orders/$192K at 1 account — concentration risk); Curated Discovery Seller (Todd Teague, $5,683 AOV — model style); Volume Relationship Seller (Sharyn Moss, 624 logins/22 customers); Precision Closer (Steve Billingsley, $8,881 AOV).

**Complexity**: Complex · **Data Dependency**: Mixpanel + MCP `orders` · **Data Readiness**: Live · **Bundle**: any `eCat iPad` with active ordering · **Query IDs**: derived from Q-01

**Allowed Claims**: distinct selling styles; archetype profiles; per-archetype coaching. **Forbidden Claims**: "net-new customers" · implied archetype superiority without data.

**Who pays**: Sales managers. **Portability**: fully portable.

---

### VM-03: Behavioral Funnel Gap Analysis

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: behavioral_funnel_gap · **Customer-Facing Name**: Sales Funnel Coaching Report

**Client value**: Turns behavioral data into a dollar-valued coaching opportunity — close one rep's funnel gap and it's ~$8K/quarter in incremental GMV. · **SuperCat value**: The strongest ROI story for the Insights Layer — "the add-on pays for itself on a single rep."

**Decision & Dollar**: *"This rep does the hard upstream work but stalls at one funnel step — close that gap and it's ~$8K/quarter in incremental GMV."* The strongest ROI story for the Insights Layer (it pays for itself on one rep).

**Gating**: VM-01 required; sufficient rep-level behavioral data for funnel mapping.

**Signal** (Q-01, Q-18 Part A): map each rep to the funnel (Targeting → Discovery → Configuration → Presentation → eCat Orders); flag strong-upstream/weak-downstream conversion.

**Example** *(BCF — validated)*: Katrinka Barnhart — Targeting/Discovery very strong (1,745 events / 2,537 searches), Configuration weak (213), 6 orders/$3,488 AOV. Gap = configuration; train on bundling/CPQ → AOV to peer $4,846 (+39%) ≈ $8K/qtr.

**Complexity**: Moderate · **Data Dependency**: Mixpanel + MCP `orders` · **Data Readiness**: Live · **Bundle**: any `eCat iPad` with ordering · **Query IDs**: derived from Q-01, Q-18 Part A

**Allowed Claims**: per-rep funnel gap with behavioral data; quantified upside vs peer AOV. **Forbidden Claims**: guaranteed revenue improvement.

**Who pays**: Sales managers / CS. **Portability**: fully portable.

---

### VM-04: Non-Selling User Role Classification

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: non_selling_user_classification · **Customer-Facing Name**: Platform User Role Report

**Client value**: Cleaner performance data — stop comparing catalog managers to sales reps, and confirm non-selling seats earn their cost. · **SuperCat value**: Honest value-per-seat conversation under step-declining user pricing.

**Decision**: *"Several of your active seats aren't sellers — they're content/catalog/analytics roles; exclude them from rep benchmarks and confirm they earn their seat."*

**Gating**: org with 10+ active users + Mixpanel.

**Signal** (Q-04): users with significant activity but ~zero eCat orders, classified by behavioral fingerprint (library+PDF = Content Manager; portal-heavy = Analytics; etc.).

**Example** *(BCF — validated)*: 7 of 49 active Q4 users non-selling — Morgan Horwitz (Catalog/Data: 83 PDFs, 15 CSV exports); Paul Camillo (Library: 940 views); Kirsten Seidl (Analytics: 1,084 library + 320 portal views).

**Complexity**: Moderate · **Data Dependency**: Mixpanel + MCP `org_users` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-04

**Allowed Claims**: non-selling role identification with evidence; seat-value assessment. **Forbidden Claims**: "seat count = wasted spend" (framing must be value-neutral).

**Who pays**: CS / Admin. **Portability**: fully portable.

---

### VM-05: Seat Utilization Analysis

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: seat_utilization · **Customer-Facing Name**: Platform Adoption Summary

**Client value**: License hygiene + adoption gaps in one view ("1,321 users have never logged in") — both a security and an activation story. · **SuperCat value**: Trust-building seat conversation — cleanup lowers the bill or activation raises platform value; either way it's transparent.

> **v4.1 gate:** define the rep population as **iPad-active seats** (`org_users.last_ipad_login_at IS NOT NULL`) ∪ order authors — **not** raw `org_users`, which conflates B2B buyers (wwjc 20,740 vs ~40–160 real seats, Spine §7.1/§7.3). Confidence Ceiling **FULL** (owned). [Stack: Tier C](#tier-c--useful-conditional-or-derivative).

**Decision**: *"Of your seats, X% actually sell — clean up dead accounts (security) and decide if the inactive base is untapped adoption or stale ERP records."*

**Gating**: none (apply the active-seat roster proxy above).

**Signal** (Q-05): total `org_users` vs active (90d login), ordering users, role-classified users.

**Example** *(BCF — validated)*: 1,370 org users — 10 active sellers (0.7%), 14 light sellers, 7 non-selling, 18 minimal, 1,321 (96.4%) never logged in.

**Complexity**: Simple · **Data Dependency**: MCP `org_users`/`login_events`/`orders` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-05

**Allowed Claims**: active-vs-inactive breakdown; security-hygiene recommendation. **Forbidden Claims**: "X% of your licenses are wasted" (value-neutral, not accusatory).

**Who pays**: Admin / CS. **Note**: large ERP-imported user bases are common — inactive ≠ a problem.

---

### VM-06: Rep Engagement Trajectory

**Audience**: Dual [D] — input to VM-29 · **Commerce Lens**: eCat transaction · **Internal Name**: rep_engagement_trajectory · **Customer-Facing Name**: Sales Team Engagement Trend

**Client value**: Early warning on rep disengagement before it shows up in numbers. · **SuperCat value**: Leading churn indicator — rep drop-off precedes account-level churn by 60–90 days (feeds VM-29).

**Decision**: *"These reps are disengaging — follow up now; rep disengagement leads account churn by 60–90 days."* Feeds VM-29 (Churn Risk).

**Gating**: active ordering reps in last 180d.

**Signal** (Q-06): per-rep login frequency + eCat order velocity over rolling 90-day windows; surface declines.

**Example** *(BCF — validated)*: Todd Teague logins −12%, orders −27% (prev vs curr 90d); Sharyn Moss flat/+4%.

**Complexity**: Moderate · **Data Dependency**: MCP `login_events`/`orders` · **Data Readiness**: Live · **Bundle**: any `eCat iPad` · **Query IDs**: Q-06

**Allowed Claims**: rolling login + eCat order trend per rep; 90-day decline %. **Forbidden Claims**: "rep is about to leave" (leading indicator) · total-business decline attributed to rep.

**Who pays**: Sales manager / CS. **Portability**: fully portable.

---

### VM-43: Territory Coverage & Dormancy

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: territory_coverage_dormancy · **Customer-Facing Name**: Territory Coverage Report

**Client value**: Shows which territories are actively covered vs going dormant, so coverage and rep assignment follow the map, not habit. · **SuperCat value**: Surfaces under-covered territory revenue at risk — a concrete rep-add / expansion conversation.

> **v4.1 gate:** run the **territory-format preflight** before unnesting (`territory_codes` is CSV in some orgs, JSON in others — Spine §7.3) and use the **active-seat** roster (§7.1), not raw `org_users`. Confidence Ceiling **STRONG**. [Stack: Tier C](#tier-c--useful-conditional-or-derivative).

**Decision**: *"Your Southeast rep owns 247 accounts but 158 have never placed an eCat order — here's the activation list, ranked by historical volume."*

**Gating**: rep territory assignments populated; meaningful at 3+ active territories.

**Signal** (Q-43): cross-reference rep territory vs `customers` (assigned) and `orders` (eCat history) → assigned-never-ordered, assigned-dormant (>90d), and uncovered territories.

**Example** *(illustrative)*: Territory Southeast / Jerry Montini — 247 assigned, 89 (36%) ever ordered eCat, 34 dormant, 158 (64%) never activated; top 10 by `sales_data` volume = highest-ROI targets.

**Complexity**: Moderate · **Data Dependency**: MCP `customers`/`orders`/`org_users` · **Data Readiness**: Live (run the `territory_codes` format pre-flight first) · **Bundle**: any `eCat iPad` with territories · **Query IDs**: Q-43

**Allowed Claims**: assigned-but-no-eCat-history accounts; territory activation rate; dormant-by-rep. **Forbidden Claims**: "these accounts don't buy from you" (may order non-eCat) · "net-new customers".

**Who pays**: Sales managers / CS. *(Pair with VM-17 aggregate + VM-37 revenue context.)*

---

### VM-46: eCat Selling Workflow Maturity

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: ecat_workflow_maturity · **Customer-Facing Name**: eCat Workflow Assessment

**Client value**: Scores how fully the team uses the eCat selling workflow and where deeper adoption would speed selling. · **SuperCat value**: Adoption depth = stickiness; a concrete feature-coaching and expansion hook.

**Decision**: *"High browsing/presentation with low submit-through means your team sells *with* eCat but closes elsewhere — that's a legitimate enablement pattern, not low adoption. Measure presentation-to-close, not order count."*

**Gating**: active Mixpanel data; most useful when submit-through <25%.

**Signal** (Q-46): eCat submit rate as a fraction of behavioral selling signals → four bands — 0% Non-submit-through · <10% Minimal · 10–25% Partial capture · >25% Transactional. High behavioral signal + low submit = enablement layer, a recognized pattern.

**Example** *(illustrative — iPad+Catalog+Portal, 3% submit)*: 12,400 searches / 8,200 customer-selects / 3,100 presentations / 420 PDFs vs 47 submitted orders (90d) → enablement-heavy; orders close via phone/EDI.

**Complexity**: Moderate · **Data Dependency**: Mixpanel `user_feature_usage_report` + MCP `orders` · **Data Readiness**: Live (conditional) · **Bundle**: any `eCat iPad` · **Query IDs**: Q-46

**Allowed Claims**: submit-through rate with band; "uses eCat as a selling layer without full submission"; presentation-depth as the value metric. **Forbidden Claims**: "low submit = low value" · "your team isn't using eCat" when behavioral signals are high.

**Who pays**: CS. **Note**: bands are calibration guides — adjust thresholds to portfolio distribution.

---

## Domain 2 — Instance Health & Data Quality

*Universally applicable "check-engine lights" — they flag problems the customer should fix. All MCP-only except VM-10 (cross-instance). All Tier D in the [Unified Stack Rank](#unified-stack-rank-v41).*

---

### VM-07: Catalog Completeness Score

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: catalog_completeness · **Customer-Facing Name**: Catalog Health Report

**Client value**: Incomplete products slow reps and buyers — a direct hit to the selling experience. · **SuperCat value**: Data quality drives engagement; >90%-complete catalogs correlate with higher order velocity.

**Decision**: *"Of your visible catalog, X% is sale-ready (image + price); the products buyers see that are missing one or both are the fix-first list."* Incomplete visible products slow the selling workflow and depress buyer conversion.

**Gating**: None — any catalog. Split `hideable=false` (visible) from hidden; hidden products are context only, never in the numerator/denominator.

**Signal** (`Q-07`): visible products (`hideable=false`) missing images (`image_exists=false`) and/or prices (`net_price IS NULL`), as a completeness %; compare to platform median (~74%).

**Example** *(BCF — validated)*: 2,980 visible — 82.3% complete, 7.0% missing image, 10.7% missing price; 447 hidden excluded; above the 74% median.

**Complexity**: Simple · **Data Dependency**: MCP `products` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-07

**Allowed Claims**: visible-product completeness %, missing image/price counts, vs platform median. **Forbidden Claims**: flagging hidden-product images as actionable · any score that folds hidden products in without disclosure.

**Who pays**: Admin / CS. **Note**: same calc as Health V2 §4.4 `catalog_completeness`; VM-07 is the per-product breakdown, Health V2 the scored aggregate.

---

### VM-08: Data Freshness Monitor

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: data_freshness · **Customer-Facing Name**: Data Health Report

**Client value**: Catches stale data before it causes order errors (stale kit data + heavy CPQ = mistakes). · **SuperCat value**: Freshness is an account-health proxy; proactive alerting prevents escalations and churn.

**Decision**: *"These entities are stale — re-import them or disable the feature before reps/buyers act on outdated data."* Freshness is a leading proxy for account health.

**Gating**: None.

**Signal** (`Q-08`): per-entity days since last update from `data_versions`, tiered Fresh (≤30d) / Monitor (31–180d) / Stale (>180d); severity-ranked.

**Example** *(BCF — validated)*: `sales_quotas` 7 mo **Stale**; `kit_items` 27d Monitor; `price_levels`/`customers`/`inventories` Fresh.

**Complexity**: Simple · **Data Dependency**: MCP `data_versions` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-08

**Allowed Claims**: entity-level freshness with age + status. **Forbidden Claims**: attributing business impact to staleness without evidence.

**Who pays**: Admin / CS. **Note**: Health V2 §4.4 scores this as `days_since_critical_update` (max across products/customers/inventory); VM-08 is the entity-level detail.

---

### VM-09: Import Health & Sync Reliability

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: import_health · **Customer-Facing Name**: Data Pipeline Health

**Client value**: Early warning on broken data pipelines before they cascade into stale catalogs and pricing. · **SuperCat value**: Import failures are a top-3 support-ticket driver — proactive detection cuts support burden.

**Decision**: *"Your import cadence is steady / slipping — here's the trend before stale data cascades."* Import failure is a top-3 support driver; early detection cuts the ticket.

**Gating**: Automated (FTP/API) imports only. Admin-Console-only orgs → **N/A**, note in output.

**Signal** (`Q-09`): monthly `import_events` frequency + error-array presence; flag declining cadence, gaps, error spikes.

**Example** *(BCF — validated)*: 119→98→74/mo (Jan→Mar 2026), consistent daily imports, no error arrays — healthy.

**Complexity**: Simple · **Data Dependency**: MCP `import_events` · **Data Readiness**: Live · **Bundle**: All (N/A for Admin-only) · **Query IDs**: Q-09

**Allowed Claims**: monthly import-count trend, presence/absence of error arrays. **Forbidden Claims**: specific error root-causes without parsing the `data` YAML.

**Who pays**: CS / Admin. **Note**: Health V2 §4.4 scores this as `import_success_rate`; VM-09 is the per-month trend.

---

### VM-10: Feature Enablement Gap Analysis

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: feature_enablement_gap · **Customer-Facing Name**: Feature Utilization Review

**Client value**: Surfaces features they already pay for (or could access) but aren't using. · **SuperCat value**: Feature activation = stickiness = lower churn; a direct upsell catalyst for add-ons.

**Decision**: *"You're paying for features you aren't using — here's what same-bundle peers run that you don't."* Activation = stickiness = lower churn; the only Domain-2 VM that isn't MCP-only (uses cross-instance benchmarks).

**Gating**: None, but **bundle-aware** — eCat-Online features are NOT "gaps" for iPad-only orgs (they're expansion, not deficiency).

**Signal** (`Q-10`): enabled features (`mobile_sites` flags + `organizations` properties) vs same-bundle peer usage; surface "available-but-unused" + platform adoption rates.

**Example** *(BCF — validated)*: well-used Kit Builder/CPQ/Library/Enrollment; Contract Pricing enabled but 0 prices loaded (18 bundle-peers use it); Quick-Order Grid not enabled.

**Complexity**: Moderate · **Data Dependency**: MCP `mobile_sites`/`organizations`/`kit_items`/`contract_prices`/`enrollment_applicants`/`smart_stacks`/`shared_resources` + BigQuery `segment_benchmarks_monthly` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-10

**Allowed Claims**: "available in your plan, not active"; per-feature adoption across same-bundle accounts. **Forbidden Claims**: listing eCat-Online features as "gaps" for iPad-only · "CPQ gap" without a CPQ subscription · "Full-stack"/"Platform-Embedded" deployment language.

**Who pays**: CS / expansion. **Note**: eCat-Online engagement measurement is an open Health V2 question (OD-5) — don't over-claim Online adoption.

---

### VM-11: Configuration Completeness

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: configuration_completeness · **Customer-Facing Name**: Platform Configuration Health

**Client value**: Prevents half-configured features from adding noise to the platform. · **SuperCat value**: Clean configuration = fewer tickets, plus a QBR adoption-gap CS can close.

**Decision**: *"This feature is on but its data is stale/empty — it's quietly feeding reps bad numbers. Re-import or turn it off."*

**Gating**: None.

**Signal** (`Q-11`): features enabled but stale (>30d) or zero-record (quotas enabled + 7-mo data; enrollment on + no recent applicants; contract pricing on + 0 contracts).

**Example** *(BCF — validated)*: Sales Quotas enabled, 15,950 rows, last import 7 mo ago → budget tracking may show outdated targets; re-import or disable.

**Complexity**: Moderate · **Data Dependency**: MCP `data_versions`/`sales_data`/`kit_items`/`contract_prices` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-11

**Allowed Claims**: feature enabled but data stale/unpopulated + a re-import-or-disable recommendation. **Forbidden Claims**: asserting a feature is "abandoned" without confirming (ask first).

**Who pays**: Admin / CS.

---

### VM-47: Smart Stack Effectiveness

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: smart_stack_effectiveness · **Customer-Facing Name**: Curated List Performance

**Client value**: Shows whether curated Smart Stacks actually drive selling, so merchandising effort pays off. · **SuperCat value**: Proves a premium feature's ROI — an adoption and expansion hook.

**Decision**: *"Your curation investment is/isn't paying off — these stacks drive orders, this 31% is dead weight; archive them and clone the winner."*

**Gating**: `smart_stacks > 0` AND Mixpanel stack-interaction events present. *(Census: 185/252 orgs carry stacks.)*

**Signal** (`Q-47`): per-stack views (`view_smart_stack`), viewing customers, and downstream eCat orders containing stack items; flag high-converting vs stale (no view / >90d).

**Example** *(illustrative)*: BCF 124 stacks; top "High-Velocity Reorders" 67% post-view order rate; 38/124 (31%) stale.

**Complexity**: Moderate · **Data Dependency**: MCP `smart_stacks`/`orders` + BigQuery Mixpanel `user_feature_usage_report` · **Data Readiness**: Live (Postgres metadata live; per-stack Mixpanel pending) · **Bundle**: any `eCat iPad` · **Query IDs**: Q-47

**Allowed Claims**: stack views, post-view eCat order rate, stale-stack list. **Forbidden Claims**: attributing revenue solely to a stack view (correlation) · performance for stacks with <5 views.

**Who pays**: CS / merchandising.

---

### VM-50: Library / Document Engagement Effectiveness

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: Non-commerce · **Internal Name**: library_document_engagement · **Customer-Facing Name**: Digital Library Performance

**Client value**: Shows which library / marketing documents reps and buyers actually open and use. · **SuperCat value**: Demonstrates Library-feature value; low usage flags an enablement gap to coach.

**Decision**: *"Here's what content reps actually use and send — keep it current, archive the 21% that's dead."* Library engagement is one of the strongest per-account stickiness/anti-churn signals.

**Gating**: Mixpanel `view_document`/`email_document` present — some orgs have sparse document-level coverage; validate first. *(Census: 164/252 orgs carry `shared_resources`.)*

**Signal** (`Q-50`): per `shared_resources` doc — views, email shares, days since last activity; flag top performers, under-used, and stale (>90d).

**Example** *(BCF — validated)*: 162 resources, 17,287 views, 444 shares; top "2026 Spring Catalog" 1,840 views/94 emails; 34/162 (21%) stale.

**Complexity**: Moderate · **Data Dependency**: MCP `shared_resources` + BigQuery Mixpanel `user_feature_usage_report` · **Data Readiness**: Conditional Live (per-org Mixpanel doc coverage) · **Bundle**: any `eCat iPad` · **Query IDs**: Q-50

**Allowed Claims**: doc view/email counts where Mixpanel coverage confirmed, stale-doc list, top content by engagement. **Forbidden Claims**: attributing sales to doc views · claims for orgs with incomplete Mixpanel coverage.

**Who pays**: CS / content owner.

---

## Domain 3 — Customer & Buyer Intelligence

*High customer value, strong retention signal. Surfaces patterns in the customer's dealer/buyer network that they often can't see themselves.*

---

### VM-12: eCat Customer Activation & ERP Penetration

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction (primary) + ERP total-business (secondary) · **Internal Name**: ecat_customer_activation · **Customer-Facing Name**: Buyer Network Activation Report

**Client value**: Headline-level — "81% of your dealers are dormant" reshapes growth strategy; most clients don't know their activation rate. · **SuperCat value**: Dormant-buyer activation = more orders = higher GMV and a strong retention/expansion story.

> **v4.1 gate:** the eCat-activation half is **owned** (always reportable); the **ERP-penetration** half is a total/denominator claim → carries `FEED_COMPLETENESS` and reports at **billing-entity** grain (Spine §6.3/§7.2). Suppress the penetration *rate* on PROVABLY-INCOMPLETE/DEAD feeds; show eCat activation regardless. Confidence Ceiling **STRONG**. [Stack: Tier C](#tier-c--useful-conditional-or-derivative).

**Decision**: *"76.7% of your eCat buyers are still active; 113 lapsed in the last 12 months are your highest-ROI reactivation list — separate from the ERP accounts that never used eCat at all."*

**Gating**: active eCat orders (submitted `orders`).

**Signal** (Q-12): primary = eCat retention (`active_12mo` / `total_ever_ordered_via_ecat`); secondary context = ERP penetration (`total_ever_ordered` / `total_erp_customers`). ERP count is context, not the activation denominator (most ERP accounts were never intended for eCat).

**Example** *(BCF — Q-12)*: 12-mo retention 373/486 (76.7%); 113 (23.3%) recently lapsed; ERP penetration 486/1,983 (24.5%), 1,497 never-activated.

**Complexity**: Moderate · **Data Dependency**: MCP `orders`/`customers` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-12

**Allowed Claims**: eCat retention on `total_ever_ordered` denominator; lapsed-buyer segmentation; ERP penetration as secondary context. **Forbidden Claims**: "81% of dealers dormant" using ERP total as denominator · "net-new customers" · treating all ERP accounts as intended eCat users.

**Who pays**: CS / sales. **Portability**: fully portable (corrected `total_ever_ordered` denominator standardized).

---

### VM-13: Customer Concentration Risk (eCat)

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: customer_concentration_ecat · **Customer-Facing Name**: Customer Concentration Analysis

**Client value**: Concentration risk at the rep + customer level most wholesalers don't track. · **SuperCat value**: Retention signal — high-concentration accounts are exposed to a single customer loss (eCat cousin of the invoiced VM-C3 / K2).

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** This is the **eCat-channel** concentration view (intent, not invoiced). The peer-ranked, invoiced-truth twin is **[VM-C3](#vm-c3-revenue-concentration--single-account-risk-hhi)** (org-level HHI, the board/covenant/M&A number) / **[VM-K2](#vm-k2-concentration--single-account-risk-customer-grain)** (customer-grain). VM-13 **leads only for no-ERP / catalog-only orgs**; otherwise lead with C3/K2 and use this as the eCat-share overlay.

**Decision**: *"Your eCat revenue is well-distributed at the account level — but one rep draws 28% of eCat GMV from a single buyer. Watch rep-level concentration, not just account."*

**Gating**: active eCat orders (12 months).

**Signal** (Q-13): eCat GMV concentration across the buyer base (top-1/5/10 share) + rep-level concentration.

**Example** *(BCF — validated)*: top buyer 4.7%, top-5 13.0%, top-10 20.8% (well-distributed); rep-level — Barbara Harper 28% of eCat GMV from one buyer.

**Complexity**: Simple · **Data Dependency**: MCP `orders` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-13

**Allowed Claims**: eCat GMV concentration %, top-buyer/top-5 share. **Forbidden Claims**: total-business concentration (eCat-channel only) · business-risk conclusions without broader ERP context.

**Who pays**: CS / sales. **Portability**: fully portable.

---

### VM-14: Customer Reorder Frequency & Velocity (eCat)

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: customer_reorder_velocity · **Customer-Facing Name**: Buyer Activity Report

**Client value**: Early warning on lapsing buyers — a weekly→monthly cadence slip caught before they disappear. · **SuperCat value**: Velocity is a direct platform-health signal; higher velocity = stickier account (eCat cousin of K-cadence).

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** eCat reorder cadence is **platform activity**, not the invoiced reorder/decay truth. The peer-ranked twin is the K-series cadence/decay (CQ-07/08, behind **[VM-K3](#vm-k3-account-decline--churn-risk)**). Leads only for no-ERP / catalog-only orgs; otherwise it is the eCat-velocity overlay on the invoiced view.

**Decision**: *"Your top buyers reorder via eCat every 4–6 days; anyone slipping past their 14-day baseline carries 3× lapsing risk — reach out before they go quiet."*

**Gating**: active eCat buyers with 3+ orders in trailing 12 months.

**Signal** (Q-14): per active buyer — avg days between eCat orders, frequency trend, declining-velocity flag.

**Example** *(BCF — validated)*: Outer Banks Furniture 89 orders/4.0d/$170K; W.F. Booth 74/4.9d/$116K; Trident 61/6.0d/$303K; <every-14-days = 3× lapsing risk.

**Complexity**: Moderate · **Data Dependency**: MCP `orders` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-14

**Allowed Claims**: eCat reorder frequency/trend per buyer; lapsing-risk flag from frequency decline. **Forbidden Claims**: total-business reorder frequency (eCat-only) · overall buyer-health conclusions without ERP context.

**Who pays**: CS / sales. **Portability**: fully portable.

---

### VM-15: Enrollment Funnel Analysis

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: Non-commerce · **Internal Name**: enrollment_funnel · **Customer-Facing Name**: Buyer Registration Funnel

**Client value**: If accepted dealers don't convert to buyers, enrollment is generating leads but not revenue — this shows the leak. · **SuperCat value**: Enrollment→first-order is a platform-health metric; low conversion = wasted growth investment.

**Decision**: *"Your registration funnel accepts 81% — but are accepted dealers actually placing first eCat orders? The gap is leads-without-revenue."* Feeds VM-44.

**Gating**: `enrollment_applicants > 0` (Buyer Registration enabled; ~68/252 orgs).

**Signal** (Q-15): applicants through applied → accepted/rejected → first eCat login → first eCat order; flag bottlenecks.

**Example** *(BCF — validated)*: 1,508 applicants → 1,218 accepted (80.8%), 288 rejected; open Q: how many accepted placed a first eCat order (join to `orders`; see VM-44).

**Complexity**: Moderate · **Data Dependency**: MCP `enrollment_applicants`/`orders` · **Data Readiness**: Live (gated by enrollment) · **Bundle**: eCat Online Closed Site / Catalog · **Query IDs**: Q-15

**Allowed Claims**: acceptance rate + funnel-stage breakdown; first-eCat-order conversion when joined to `orders`. **Forbidden Claims**: "accepted = new customers" (not buyers until they order) · "net-new customers".

**Who pays**: CS / growth. **Portability**: fully portable (gated by enrollment flag).

---

### VM-16: ERP Total Business Visibility — ⛔ SUPERSEDED → **VM-C1 (True Topline)**

> **SUPERSEDED (4.0, 2026-06-29).** This VM is the eCat-context framing of "total business." Its hardened, board-grade successor is **[VM-C1 True Topline](#vm-c1-true-topline)** in Domain 9 — same invoiced-net spine (`SUM(portal_invoices.net_amount)` via `Q-PROV-00`/`Q-ECON-00`), but with the full `FEED_COMPLETENESS` verdict table (CORROBORATED / UNVERIFIED / PROVABLY-INCOMPLETE / STALE / DEAD), the `report_through_date` clamp, and the `invoiced ≠ collected` rule as first-class fields. **Do not run VM-16 as a separate VM** — run VM-C1 and frame eCat capture against it via **[VM-C14 / VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline)**. The anchor is retained only so existing references resolve.

---

### VM-17: Dormant eCat Customer Identification

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: dormant_ecat_customers · **Customer-Facing Name**: Lapsed Buyer Report

**Client value**: Turns "81% dormant" into a prioritized outreach list; the at-risk high-value cut is sharpest ("your 5th-largest buyer hasn't ordered in 4 months"). · **SuperCat value**: Reactivation = GMV growth and a tangible CS value story (eCat cousin of K8 / S1).

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** This is **eCat-order dormancy** (last eCat order date) — a reactivation list, still useful on its own. The peer-ranked twin for **invoiced** account decay with a dollar-at-risk and who-to-call (catches decline 90 days early on the slope of the real book) is **[VM-K8 / Exception S1](#vm-s1-account-health--at-risk-the-quietly-dying-alarm)**. VM-17 = eCat reactivation list; K8/S1 = invoiced revenue-at-risk alarm.

**Decision**: *"113 buyers ordered via eCat before but not in the last 12 months — and 4 high-value buyers (>$10K) have gone 90+ days silent. Here's the prioritized reactivation list by rep."*

**Gating**: active eCat order history.

**Signal** (Q-17): buyers who ordered in a prior period but not the current; segment by historical eCat value; **at-risk sub-view** = rank by trailing-12mo eCat GMV, flag no eCat order in 90d. Distinguish "dormant" (ordered before) from "never activated" (see VM-12).

**Example** *(BCF — validated)*: of 486 all-time eCat buyers — 373 active, 113 lapsed 7–24 mo (highest reactivation), 76 lapsing 4–12 mo (urgent); 4 buyers >$10K with no order in 90+ days.

**Complexity**: Moderate · **Data Dependency**: MCP `orders`/`customers` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-17

**Allowed Claims**: lapsed eCat buyer count by dormancy window; at-risk high-value list with last order date. **Forbidden Claims**: "dormant" for never-ordered buyers (that's "not yet activated") · "net-new customers".

**Who pays**: CS / sales. **Portability**: fully portable.

---

### VM-41: First-Time eCat Orderers by Channel & Rep

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: first_time_ecat_orderers · **Customer-Facing Name**: New eCat Buyer Acquisition Report

**Client value**: Quantifies new-buyer acquisition by channel and rep; the eOL split measures portal ROI directly ("the portal is winning business on its own"). · **SuperCat value**: Demonstrates platform-driven acquisition; strengthens the Clicky / portal case.

**Decision**: *"You added 167 first-time eCat buyers in 15 months (68% rep-acquired, 32% eCat-Online self-serve) — here's growth by channel and rep, paired with lapsed for net buyer-base change."*

**Gating**: active eCat order history (12+ months for trend).

**Signal** (Q-41): buyers whose first-ever eCat order falls in the period, attributed by channel (`order_source='ipad'` rep-acquired vs `'server'` eCat-Online) and by rep. Keep enrollment pipeline separate (acceptance ≠ ordering).

**Example** *(BCF — validated, Jan 2025–Mar 2026)*: 167 first-time — 113 (68%) rep-acquired, 54 (32%) eCat-Online; top reps Sharyn Moss 20, Katrinka Barnhart 15; enrollment ~30/mo at 80.6% accept (separate).

**Complexity**: Simple · **Data Dependency**: MCP `orders` (+ `enrollment_applicants` for pipeline context) · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-41

**Allowed Claims**: first-time orderer count by channel + rep; enrollment pipeline as leading indicator. **Forbidden Claims**: "net-new customers" · "eCat-Online buyers are net-new accounts" (may have ERP relationships) · enrollment acceptances = proven buyers.

**Who pays**: CS / sales (QBR). *(Pair with VM-17 for net buyer-base change.)*

---

### VM-44: Onboarding Velocity / Time-to-First-eCat-Order

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: eCat transaction · **Internal Name**: onboarding_velocity · **Customer-Facing Name**: Buyer Onboarding Report

**Client value**: Time-to-first-order shows exactly where onboarding stalls (internal-lead framing for CS). · **SuperCat value**: Onboarding speed is a leading retention signal and a CS-playbook prioritization input.

**Decision**: *"Median accepted dealer takes 19 days to first eCat order — but 47% never convert. That's the onboarding gap to close with a first-order sequence."*

**Gating**: accepted `enrollment_applicants` joined to `orders`; enrollment enabled (~68 orgs).

**Signal** (Q-44): cohort distribution of acceptance→first-eCat-order time; median days, 30/60/90-day conversion, never-converted %.

**Example** *(illustrative)*: 412 accepted — 21.6% convert ≤30d, 12.6% 31–60d, 7.5% 61–90d, 46.6% never; median 19 days.

**Complexity**: Moderate · **Data Dependency**: MCP `enrollment_applicants`/`orders`/`customers` · **Data Readiness**: Live (gated by enrollment; internal-only scope) · **Bundle**: Buyer Registration enabled · **Query IDs**: Q-44

**Allowed Claims**: acceptance-to-first-order conversion at 30/60/90d; median time; % with no order. **Forbidden Claims**: acceptance = eCat buyer · "net-new customers".

**Who pays**: CS / growth. **Portability**: fully portable for enrollment-enabled accounts.

---

### VM-49: Buyer-Level Repeat Purchase

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: ERP total-business · **Internal Name**: buyer_repeat_purchase · **Customer-Facing Name**: Buyer Loyalty Report

**Client value**: Buyer-level repeat-purchase within accounts — who's reordering vs one-and-done. · **SuperCat value**: Repeat depth = stickiness; supports buyer-engagement expansion conversations.

**Decision**: *"64% of new buyers reorder within 90 days (80% within 180) — the 20% who never return are your targeted-outreach list, across all channels not just eCat."*

**Gating**: `portal_orders` buyer attribution present (coverage varies by org/ERP sync — validate first).

**Signal** (Q-49): buyer-level repeat rates — first-order cohort returning within 90/180 days; all-channel, not eCat-only.

**Example** *(illustrative)*: 84 first-time buyers Q4 2025 — 64.3% repeat ≤90d, 79.8% ≤180d, 20.2% none.

**Complexity**: Moderate · **Data Dependency**: MCP `portal_orders` (buyer attribution) · **Data Readiness**: Conditional Live (attribution not universal) · **Bundle**: iPad+Catalog+Portal, Full · **Query IDs**: Q-49

**Allowed Claims**: buyer repeat rate where attribution confirmed; cohort return at 90/180d. **Forbidden Claims**: applying to orgs without confirmed buyer attribution · buyer-level claims on aggregate-only `portal_orders`.

**Who pays**: CS / sales. **Portability**: data-gated on buyer attribution.

---

## Domain 4 — eCat Commerce Analytics

*Deepens eCat platform value. Surfaces trends and patterns in eCat-channel behavior that inform strategy and operations.*

---

### VM-18: eCat Order Velocity & Trend (with ERP Context)

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction (primary) + ERP total-business (context) · **Internal Name**: ecat_order_velocity · **Customer-Facing Name**: eCat Order Performance Report

**Client value**: Platform-specific order trend and channel mix the ERP doesn't surface easily. · **SuperCat value**: Order velocity is the fundamental health signal; declining velocity is the earliest churn predictor.

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** Part A (eCat order velocity) is owned platform health and **always leads** for the eCat story. Part B's "total/share" context is superseded by invoiced-truth Domain 9 ([VM-C1](#vm-c1-true-topline), [VM-C10](#vm-c10-comparable-window-momentum-staleness-proof-yoy), [VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline)) — Part B's `portal_orders` booked total is a **labeled fallback only** (Spine §1), never the invoiced topline.

**Decision**: *"Your eCat order volume is stable at ~200–250/month (~52% of total ERP order count); the Oct–Nov market spike in the ERP feed explains the seasonal eCat-share dip — plan capacity and promos around it."*

**Gating**: active eCat orders.

**Signal** (Q-18): Part A — monthly eCat order count/GMV/trend + iPad-vs-eOL split from `orders`. Part B (ERP context) — monthly total order count/GMV from `portal_orders` (labeled booked fallback), eCat share, seasonality.

**Example** *(BCF — Q-18 A+B)*: eCat ~200–250/mo, December dip ~30%; ERP ~400/mo; eCat ~52% of ERP order volume; Oct–Nov market spike explains Nov share decline.

**Complexity**: Simple · **Data Dependency**: MCP `orders` (A), `portal_orders` (B — Sales Portal only) · **Data Readiness**: Live (A all commerce; B gated to `portal_orders`) · **Bundle**: A iPad+Catalog+Cart/Full; B + Portal · **Query IDs**: Q-18

**Allowed Claims**: eCat volume/GMV trend; eCat share of total ERP business (Part B present); seasonality. **Forbidden Claims**: ERP total volume = eCat volume · attributing non-eCat channels to eCat.

**Who pays**: CS / sales ops. **Portability**: Part A portable; Part B gated to `portal_orders`.

---

### VM-19: eCat Channel Mix Evolution

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: eCat transaction · **Internal Name**: ecat_channel_mix · **Customer-Facing Name**: eCat Ordering Channel Report

**Client value**: The iPad vs eOL shift informs where to invest — rep training vs online experience. · **SuperCat value**: Channel mix predicts segment migration and tier-upgrade readiness.

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** This is the **iPad-vs-eOL split *within* eCat** (an internal-to-eCat mix), not the where-you-sell channel headline. The peer-ranked twin for eCat-vs-everything-else is **[VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline)**. Leads only for `has_cart` orgs tuning their own online-vs-rep mix.

**Decision**: *"Buyer self-service has reached near-parity with rep ordering (55% online in Jan) — it's complementary, not cannibalizing; invest in the online catalog experience as it compounds."*

**Gating**: `has_cart=true` AND confirmed `order_source='server'` orders present. Never show "mix" for iPad-only orgs (no mix with one channel).

**Signal** (Q-19): ratio of iPad (`order_source='ipad'`) vs eCat-Online (`'server'`) orders over time within `orders`.

**Example** *(BCF — validated)*: online share 45%→51%→55% (Mar→Jan); near-parity with iPad.

**Complexity**: Simple · **Data Dependency**: MCP `orders` · **Data Readiness**: Live (gated `has_cart` + server orders) · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-19

**Allowed Claims**: iPad-vs-eCat-Online split + trend within `orders`. **Forbidden Claims**: showing eCat-Online as a channel for iPad-only · "100% iPad / 0% eOL" as a mix · referencing `portal_orders` as a channel here.

**Who pays**: CS / digital. **Portability**: data-gated (B2B Cart confirmed + server orders).

---

### VM-20: eCat AOV Analysis

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: ecat_aov · **Customer-Facing Name**: eCat Order Value Analysis

**Client value**: AOV by dimension surfaces concrete selling-workflow optimization. · **SuperCat value**: Quote/config adoption = deeper platform integration = stickier account.

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** eCat AOV is **order-intent** AOV (pre-re-key), not invoiced realized value. Useful for eCat workflow tuning (e.g., quote-vs-confirmed); for realized economics use the invoiced Domain-9 view. Never present eCat AOV as "your average deal size."

**Decision**: *"Quotes carry 19% higher AOV but only 0.9% of your eCat orders use them — train reps to route larger deals through Quote to lift captured GMV."*

**Gating**: active eCat orders (10+ per dimension for meaningful averages).

**Signal** (Q-20): eCat AOV by rep/buyer/channel/order-type over time; surface outliers and trends.

**Example** *(BCF — validated)*: all eCat $2,525; iPad $2,783 vs eOL $2,254; top rep Jack Johnson $5,599; Quotes $2,994 (19% higher) but only 22/2,557 (0.9%).

**Complexity**: Simple · **Data Dependency**: MCP `orders` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-20

**Allowed Claims**: eCat AOV by rep/buyer/channel/order-type; Quote-vs-non-Quote AOV within eCat. **Forbidden Claims**: total-business AOV (eCat-only) · "your average deal size is $X" without the eCat-only qualifier.

**Who pays**: Sales ops / CS. **Portability**: fully portable.

---

### VM-21: eCat Order Type & Workflow Analysis

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction · **Internal Name**: ecat_order_type · **Customer-Facing Name**: eCat Workflow Analysis

**Client value**: Workflow visibility — ensure the platform matches the real selling process. · **SuperCat value**: Quote-workflow adoption pulls SuperCat deeper into the sales process = stickier usage.

> **⤵ Demoted to eCat-intent cousin (v4.1 — [Register A](#register-a--demoted-ecat-intent-cousins)).** Order-type/workflow mix is **eCat adoption**, and its quote→cash value is now owned by **[VM-C24 Quote-to-Cash Pipeline](#vm-c24-quote-to-cash-pipeline-value-ecat-pipeline-never-sales)** (which enforces the eCat-SALE filter — never sum quote $ into sales, the FAL trap). Leads only for eCat workflow-adoption coaching.

**Decision**: *"You run 99% Confirmed orders — if your process involves negotiation/approvals, routing through Quote adds the audit trail and visibility you're missing."*

**Gating**: active eCat orders.

**Signal** (Q-21): eCat orders by `order_type` (Confirmed/Quote/HFC) and `order_source`; flag underutilized workflows.

**Example** *(BCF — validated)*: Confirmed 2,535 (99.1%, $6.40M); Quote 22 (0.9%, $66K, $2,994 avg).

**Complexity**: Simple · **Data Dependency**: MCP `orders` · **Data Readiness**: Live · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-21

**Allowed Claims**: eCat order-type distribution; Quote-vs-Confirmed AOV within eCat. **Forbidden Claims**: total-business workflow analysis (eCat-only).

**Who pays**: Sales ops / CS. **Portability**: fully portable.

---

### VM-22: Feature Usage Depth (Behavioral)

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: feature_usage_depth · **Customer-Facing Name**: Platform Feature Usage Report

**Client value**: Quantifies how the team really uses the platform and which features would save time or drive revenue if adopted. · **SuperCat value**: Feature depth = stickiness — accounts using 5+ features churn far less.

**Decision**: *"Here's what your team actually leans on (CPQ, Library — power usage) vs what's underused (Customer Favorites), plus a 27% PDF-catalog abandonment worth fixing."* Feature depth = stickiness; 5+ features churn far less.

**Gating**: Mixpanel behavioral data present (live coverage 187/252 orgs).

**Signal** (Q-22): per-org Mixpanel iPad event aggregation vs same-bundle averages; heavy-use (validated investment) vs underused (adoption opportunity). Optional Clicky join for `has_clicky` portal accounts.

**Example** *(BCF — validated)*: CPQ 7,173 configured (power user); Library 17,287 views/444 emails (content-heavy); Smart Stacks 2,147 views; PDFs 73% completion (27% abandonment = UX friction); Customer Favorites 227 views (underutilized for a 486-buyer base).

**Complexity**: Moderate · **Data Dependency**: BigQuery `org_feature_usage_report` (+ `clicky_analytics` for `has_clicky`) · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-22

**Allowed Claims**: feature event counts + intensity; same-bundle peer comparison. **Forbidden Claims**: "Platform-Embedded"/"Commerce-Active"/"Catalog-Focused" labels in client-facing text · "you're using eCat Online heavily" where Online measurement isn't validated (Health V2 OD-5).

**Who pays**: CS. **Portability**: fully portable.

---

### VM-45: eCat Capture Rate vs. Total Business — ⛔ SUPERSEDED → **VM-C14 / VM-CHAN-1**

> **SUPERSEDED (4.0, 2026-06-29).** The capture insight now lives as one consolidated VM — **[VM-C14 eCat Capture / Platform Footprint](#vm-c14-ecat-capture--platform-footprint)** (Domain 9) for the dollar/share question and **[VM-CHAN-1 eCat vs non-eCat split](#vm-chan-1-ecat-vs-non-ecat-split-the-headline)** (Domain 10) for the channel headline. All three were the same insight; 4.0 collapses them so the catalog does not ship near-duplicates. The successor VMs carry the full gate verbatim: rate only when `TOTAL_BUSINESS_SOURCE=INVOICES`, `COMMERCE_CONFIDENCE ≥ STRONG`, `FEED_COMPLETENESS=CORROBORATED`, and eCat-SALE GMV ≤ invoiced (the `sc` >100% case → suppress and report the completeness gap); otherwise **absolute captured dollars only**. Capture is a **fact**; attribution ("eCat drove $X") stays a suppressed estimate (Spine §4). Anchor retained for reference resolution.

---

## Domain 5 — Product & Inventory Intelligence

*Manufacturer business intelligence. These are "how is your business performing" insights — not platform analytics.*

---

### VM-37: Inventory × Sales Intelligence

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: inventory_sales_crossref · **Customer-Facing Name**: Inventory & Sales Opportunity Report

**Client value**: "Your best sellers you can't currently sell" — drives purchasing and production; a headline QBR insight. · **SuperCat value**: Business intelligence, not just analytics — the strongest "pays for itself" case ($250K+ if restocking the top 10 captures even 10%).

> **v4.1 gate:** rides `sales_data` (coarse, no dates) + point-in-time `inventories` → magnitude + OOS signal only, never a dated trend; OOS items are "historically high-volume items currently showing zero availability," never "revenue at risk" (Forbidden Claims Register). Confidence Ceiling **STRONG** (conditional). [Stack: Tier B](#tier-b--strong-narrower-or-more-gated).

**Decision**: *"8 of your top-10 revenue products show zero current availability — $2.55M of historical demand you can't fulfill right now. Restock by historical velocity."*

**Gating**: both `sales_data` (ERP-invoiced history) and `inventories` (current stock) present (~81 orgs).

**Signal** (Q-37): cross-reference historical sales per product (`sales_data.amount_invoiced`/`quantity_invoiced`) with current `inventories` (`qty_available`/`qty_on_hand`/`qty_on_backorder`); surface top sellers at zero/critically-low stock. **Snapshot caveat:** `inventories` is point-in-time — no history, so never claim how long an item's been out.

**Example** *(BCF — validated)*: 0510-005 $400K/0 avail; 0728-011 $381K/0; 0635-002 $339K/0; 8 of top-10 at zero = $2.55M historical demand.

**Complexity**: Simple · **Data Dependency**: MCP `sales_data` + `inventories` + `products` · **Data Readiness**: Live · **Bundle**: All (data-dependent) · **Query IDs**: Q-37

**Allowed Claims**: "historically high-volume items currently at zero availability"; top-sellers (historical ERP invoiced) × current stock. **Forbidden Claims**: "revenue at risk" as a precise figure without the snapshot caveat · how long items have been OOS (no inventory history).

**Who pays**: Ops / merchandising / CFO. **Portability**: fully portable (`base_item_code` standardized per org).

---

### VM-38a: Product Velocity Trend (eCat Orders — Current Capability)

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: eCat transaction · **Internal Name**: product_velocity_ecat · **Customer-Facing Name**: Product Sales Velocity Report (eCat Orders)

**Client value**: Product velocity with directional signals ("accelerating — stock up") the ERP doesn't show. · **SuperCat value**: Deepens BI value; paired with VM-37 it's a full product-health view.

**Decision**: *"This item's eCat demand is accelerating +12% — replenish before stockout; these others are declining — clear or reposition."*

**Gating**: `portal_order_items` + `portal_orders` present (~52 orgs).

**Signal** (Q-38a): product-level eCat order velocity over time from `portal_order_items` × `portal_orders` (dated); rising vs falling demand.

**Example** *(illustrative)*: Item 0848-026 (BEDS) — 588 units historically, +12% last 3 months, accelerating.

**Complexity**: Moderate · **Data Dependency**: MCP `portal_order_items` + `portal_orders` · **Data Readiness**: Live (conditional on `portal_order_items`) · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-38a

**Allowed Claims**: eCat product velocity trend; accelerating vs declining by order count. **Forbidden Claims**: full-channel velocity (eCat-only via `portal_order_items`) · total inventory demand.

**Who pays**: Ops / merchandising. **Portability**: data-gated to `portal_order_items` orgs. *(Pairs with VM-37 for full product health.)*

---

### VM-38b: Product Velocity Trend (Full — Pending Engineering)

**Audience**: Dual [D] — **Pending Engineering** · **Commerce Lens**: ERP total-business · **Internal Name**: product_velocity_full · **Customer-Facing Name**: Product Sales Velocity Report (All Channels)

**Client value**: The all-channel version of VM-38a — true product velocity across every channel, not just eCat (pending an invoice-line feed). · **SuperCat value**: Completes the product-health BI story; the upgrade hook once the line-level feed lands.

**Decision**: *"(When unlocked) full-channel product demand direction — accelerating vs declining across ALL ERP sales, not just eCat — covering 81 `sales_data` orgs vs the 52 on VM-38a."*

**Gating**: ⏳ **blocked** — requires an `invoice_date`/`period` column on `sales_data` (not yet available; one-column ERP-import schema change). Until then, run VM-38a (eCat-only).

**Signal**: once dated, product-level sales velocity across all ERP channels by month.

**Complexity**: Moderate · **Data Dependency**: MCP `sales_data` + the pending `invoice_date` column · **Data Readiness**: **Pending Engineering** (high-priority; one-column add) · **Bundle**: All (data-dependent) · **Query IDs**: pending

**Enhancement path**: engineering adds `invoice_date`/`period` to `sales_data` → VM-38b unlocks for all 81 `sales_data` orgs (companion to VM-C23's `introduced_date` ask).

**Who pays**: Product / VP Sales (deepens Domain 5 from eCat-centric to full-business BI).

---

### VM-39: Line Analysis by Category & Collection

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: line_analysis_category · **Customer-Facing Name**: Product Line Performance Report

**Client value**: "Analyze the line by category" — which lines earn their shelf space and which don't, auto-surfaced from data already flowing through the platform. · **SuperCat value**: Positions Insights as a product-strategy tool and engages a new persona (product / merchandising).

**Decision**: *"BEDS return $82K/item on 21 SKUs; CAT23 returns $328/item on 806 — rationalize the bloated low-return lines and invest in the productive ones."*

**Gating**: `sales_data` + `products` with `category_code` populated (~81 orgs).

**Signal** (Q-39): ERP sales aggregated by `category_code`/`collection_code` — revenue, item count, sales/item — catalog investment vs where revenue comes from.

**Example** *(BCF — validated)*: CAT1 $5.79M/150; SOFAS $3.46M/102; BEDS $1.73M/21 ($82,534/item, highest); CAT23 $264K/806 ($328/item, lowest).

**Complexity**: Simple · **Data Dependency**: MCP `sales_data` + `products` · **Data Readiness**: Live · **Bundle**: All (data-dependent) · **Query IDs**: Q-39

**Allowed Claims**: sales by category with per-item productivity; collection-level revenue. **Forbidden Claims**: category conclusions on opaque codes (e.g. "CAT1") without noting the client must interpret their own codes.

**Who pays**: Product / merchandising. **Portability**: query portable; category codes client-configured (a ~10–30-row name map enables self-serve). **Enhancement**: attribute-level (style/color/size) needs `products.custom_fields` structured metadata (Phase 4+).

---

### VM-40: Regional Product Intelligence

**Audience**: Dual [D] · **Commerce Lens**: eCat transaction + ERP total-business · **Internal Name**: regional_product_intelligence · **Customer-Facing Name**: Geographic Sales Intelligence Report

**Client value**: Geographic demand intelligence usually only available from costly market research — built from real transaction data. · **SuperCat value**: "There's demand in regions you don't serve" is a powerful expansion conversation (reps / territory / portal).

**Decision**: *"BEDS over-index in MA ($703K) vs NC ($213K), and your portal draws traffic from 20 states but orders from 8 — here's demand in regions you don't actively serve."*

**Gating**: `customers.billing_state` populated (197 orgs, 81%); category×geography additionally needs `sales_data`.

**Signal** (Q-40): eCat orders / ERP sales × buyer geography (`billing_state`) → regional patterns; optional Clicky (VM-33) overlay for portal-traffic-vs-order geography gap.

**Example** *(BCF — validated)*: top states NC $874K, NJ $746K, FL $658K; BEDS skew MA vs NC; supply×demand gap — traffic from 20 states, orders from 8.

**Complexity**: Moderate · **Data Dependency**: MCP `orders`/`customers` (eCat), `sales_data`/`customers`/`products` (ERP), BigQuery `clicky_analytics` (`has_clicky` enrichment) · **Data Readiness**: Live · **Bundle**: All (data-dependent) · **Query IDs**: Q-40

**Allowed Claims**: geographic distribution of eCat orders/buyers; category×state; portal-traffic-vs-order geography gap (with Clicky). **Forbidden Claims**: single-cause attribution of regional patterns without analysis · international claims from `billing_state` alone.

**Who pays**: Sales leadership / expansion. **Portability**: fully portable (`billing_state` standardized); map viz is a Phase 3/4 decision.

---

### VM-42: New Item Performance

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: new_item_performance · **Customer-Facing Name**: New Introduction Performance Report

**Client value**: Near-real-time new-introduction sell-through by collection — a genuinely new capability vs end-of-season reviews. · **SuperCat value**: Elevates the buyer persona — "how are my new intros doing?" is a CEO / VP-Sales question, not an IT-admin one.

**Decision**: *"Your new intros span a 107× sell-through gap ($1,398/item vs $13/item) — lead with the winners, flag the dead collections for merchandising review."*

**Gating**: `products.new_item=true` (164 orgs, 67%) AND `sales_data` (81 orgs, 33%) — intersection (~81).

**Signal** (Q-42): `new_item` flag × `sales_data`, grouped by `collection_code` → new-product sell-through and per-item productivity.

**Example** *(BCF — validated 2026-03-24)*: 230 new items; COL11 $1,398/item (strongest); COL119 $1,278; CORA $24; COL61 55 items/$13 (near-zero); 107× best-vs-worst spread.

**Complexity**: Simple · **Data Dependency**: MCP `products` (new_item) + `sales_data` · **Data Readiness**: Live · **Bundle**: All (data-dependent) · **Query IDs**: Q-42

**Allowed Claims**: new-item sell-through by collection; per-item productivity; near-zero-sell-through collections. **Forbidden Claims**: attributing poor sell-through to product quality alone (could be rep awareness/timing/pricing) · "these products are failing" without alternatives.

**Who pays**: Product / VP Sales. **Portability**: fully portable (`new_item`/`collection_code` standardized). **Enhancement**: time-cohorted intro performance needs `introduced_date` on `products` (companion to VM-38b's `invoice_date`).

---

## Domain 6 — Cross-Instance Benchmarking

*The long-term moat. Only SuperCat can provide cross-customer comparison because only SuperCat sees data across all instances. Requires anonymization — no product-level best-seller data exposed.*

---

### VM-23: Peer Comparison Dashboard

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce (platform metrics) · **Internal Name**: peer_comparison · **Customer-Facing Name**: Industry Benchmark Report

**Client value**: Context — raw numbers are meaningless without it; "is 1,773 orders good?" the benchmark answers. · **SuperCat value**: Benchmarking is the single strongest differentiator no competitor can provide; creates segment-aware urgency.

**Decision**: *"You're above peer median on engagement and MRR but 41% below on eCat orders — more engaged than peers yet converting less; reactivation (VM-17) is the most direct fix."* Benchmarking is the single strongest Insights-Layer differentiator.

**Gating**: BigQuery `segment_peer_comparison` view (live). Anonymized — no client names.

**Signal** (Q-CI-02): rank client on key platform metrics vs same-bundle peers (`segment_peer_comparison` + `segment_benchmarks_monthly`).

**Example** *(BCF — validated 2026-03-24, 33 Full-bundle peers)*: eCat orders 1,773 vs 2,986 median (−40.6%); logins +23.5%; MRR +35.3%.

**Complexity**: Simple · **Data Dependency**: BigQuery `segment_peer_comparison` + `segment_benchmarks_monthly` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-CI-02

**Allowed Claims**: client metrics vs anonymized peer medians/percentiles; "above/below median for your plan." **Forbidden Claims**: internal segment labels in client-facing text · naming peer clients · comparing across bundle types.

**Who pays**: CS / exec (QBR). **Portability**: fully portable.

---

### VM-24: Feature Adoption Benchmarking

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: feature_adoption_benchmarking · **Customer-Facing Name**: Feature Utilization Benchmark

**Client value**: Validates their platform investment and surfaces the one gap in context. · **SuperCat value**: A natural upsell vehicle — "67% of accounts at your level use portal analytics; you don't yet."

**Decision**: *"You're top-tier on feature breadth for your plan — the expansion conversation is depth (Clicky, Insights Layer), not breadth."*

**Gating**: BigQuery `org_summary` + `segment_benchmarks_monthly`.

**Signal** (Q-CI-03): per-feature adoption rate across same-bundle accounts; where the client sits vs peers and top performers.

**Example** *(BCF — validated 2026-03-24)*: Library/PDF 100% (at norm); CPQ 7,306 items at 36.4% adoption (above peers); Online Ordering 66.7%; Clicky not established (opportunity).

**Complexity**: Simple · **Data Dependency**: BigQuery `org_summary` + `segment_benchmarks_monthly` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-CI-03

**Allowed Claims**: feature adoption % vs same-bundle peers; "X% of accounts on your plan use [feature]." **Forbidden Claims**: internal segment labels in client-facing text · high-certainty eCat-Online adoption claims while Health V2 OD-5 unresolved.

**Who pays**: CS / expansion. **Portability**: fully portable.

---

### VM-25: Growth Trajectory Comparison

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: growth_trajectory_comparison · **Customer-Facing Name**: Growth Trajectory Report

**Client value**: "Are we keeping up?" with percentile specifics ("between p25 and median — here's what moves you to p75"). · **SuperCat value**: Creates urgency and anchors Insights as the tool that monitors trajectory continuously.

**Decision**: *"You sit between p25 and median on orders — here's what moves you to p50–p75, tracked monthly so you can see whether you're closing the gap."*

**Gating**: ≥2 monthly benchmark snapshots for trending (snapshots started March 2026).

**Signal** (Q-CI-02/04): client eCat velocity vs segment cohort trajectory; monthly snapshots enable MoM/YoY trending.

**Example** *(BCF — March 2026 snapshot)*: eCat orders 1,773 (p25 1,205 / median 2,986 / p75 6,109) — between p25 and median; logins between median and p75; first time-series comparison May 2026.

**Complexity**: Simple now; time-series needs 2–3 months · **Data Dependency**: BigQuery `segment_peer_comparison` (now) + `segment_benchmarks_monthly` (accumulating) · **Data Readiness**: Live (snapshot); trending from May 2026 · **Bundle**: iPad+Catalog+Cart, Full · **Query IDs**: Q-CI-02, Q-CI-04

**Allowed Claims**: current-period percentile vs peers; trajectory direction once 2+ snapshots exist. **Forbidden Claims**: definitive trend claims before 2+ monthly snapshots.

**Who pays**: CS / exec. **Portability**: fully portable.

---

### VM-26: Best Practice Identification

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: best_practices · **Customer-Facing Name**: What Top-Performing Accounts Do

**Client value**: Evidence-based recommendations anchored in what top performers actually do — "the top 3 accounts in your segment all do X." · **SuperCat value**: Positions SuperCat as a strategic partner; the cross-instance dataset is the moat that makes it quantifiable.

**Decision**: *"The top-3 accounts on your plan all run max feature depth + Clicky + >5,000 eCat orders — close your specific gaps (Clicky, reactivation) in that order."*

**Gating**: BigQuery `top_performers_by_segment` + `org_master_with_segments`.

**Signal** (Q-CI-05/06): behavioral patterns correlated with high performance across the platform, surfaced as bundle-specific best practices (feature adoption × engagement × outcomes).

**Example** *(BCF — validated 2026-03-24, internal)*: top Full-bundle performers (Gabriella White 38,049 orders, Summer Classics 13,424, Gabby 13,049) share feature depth 8/8 (BCF 7/8, gap = Clicky), established portal analytics, and >5,000 eCat orders (BCF 1,773 — headroom).

**Complexity**: Moderate · **Data Dependency**: BigQuery `org_master_with_segments` + `top_performers_by_segment` + `segment_benchmarks_monthly` · **Data Readiness**: Live (correlation build ongoing) · **Bundle**: All · **Query IDs**: Q-CI-05, Q-CI-06

**Allowed Claims**: "top performers on your plan share these patterns"; anonymized benchmarks only. **Forbidden Claims**: naming specific top-performing clients (client-facing) · internal segment labels in client-facing text.

**Who pays**: CS / exec. **Portability**: fully portable.

---

## Domain 7 — SuperCat Internal Intelligence

*Not customer-facing (except VM-30 which has an external-safe variant). Powers CS playbooks, expansion targeting, and churn prevention.*

---

### VM-27: Account Health Score (Health V2)

**Audience**: Internal [I] · **Commerce Lens**: Non-commerce · **Internal Name**: account_health_score · **Customer-Facing Name**: N/A — internal only

**Client value**: Internal only — the customer benefits indirectly via better-prioritized, proactive CS. · **SuperCat value**: Replaces intuition-driven CS prioritization with data — the core internal health engine (Health V2).

**Decision**: *"One authoritative health band + classification per account → CS knows who to Intervene, Stabilize, Maintain, or Expand, and why."* Health V2 is the **only** authoritative scoring methodology — never maintain a parallel formula.

**Gating**: Health V2 inclusion criteria (§1 of Health V2 README).

**Signal**: surface Health V2 operator outputs — `health_score` (0–100, post-cap), `health_band` (Thriving/Healthy/Watch/At Risk/Critical), `classification` (Expand/Stabilize First/Maintain/Intervene), `churn_risk(+severity)`, `expansion_ready(+type)`, the five component scores (engagement/adoption/value_delivery/operational_health/trajectory), `risk_modifier_applied` (RM-1..4), `score_explanation`. The legacy `org_summary.health_score` (0–1.0) is a precursor for trend continuity only — not co-equal.

**Example** *(BCF)*: run the Health V2 operator for current score/band/classification; engagement+adoption above median, value-delivery constrained by the order gap; no risk modifiers fired.

**Complexity**: Simple (run operator) · **Data Dependency**: Health V2 operator CSV (sources: Mixpanel, MCP orders/login_events/org_users/import_events/products, Clicky, HelpScout) · **Data Readiness**: Live · **Bundle**: All (bundle-aware) · **Query IDs**: Health V2 operator (`operator.py`), `QUERIES.md`

**Allowed Claims**: Health V2 scores/bands as produced by the operator; classification + CS action. **Forbidden Claims**: presenting legacy `org_summary.health_score` as authoritative · recomputing health outside Health V2 · using Health V2 score language with clients (internal only).

**Internal use**: CS prioritization. **Portability**: fully portable (bundle-aware weight redistribution).

---

### VM-28: Expansion Readiness Signals

**Audience**: Internal [I] · **Commerce Lens**: Non-commerce · **Internal Name**: expansion_readiness · **Customer-Facing Name**: N/A — internal only

**Client value**: Internal — CS frames it softly ("your usage is evolving; here's what supports your growth"). · **SuperCat value**: A live, ARR-prioritized expansion pipeline; data-driven upsell targeting that replaces intuition.

**Decision**: *"Here's the ARR-sorted upsell hit-list — accounts whose behavior says 'ready to expand,' with the specific missing bundle/feature."*

**Gating**: Health V2 Growth Score + BigQuery `expansion_candidates`.

**Signal** (Q-CI-07): accounts ready for bundle upgrade / add-on — Health V2 `growth_score`/`expansion_ready`/`expansion_type`/`bundle_upgrade_signal`/`feature_gap_score`/`customer_headroom_score`, the `expansion_candidates` view, and VM-48 CRM context.

**Example** *(live 2026-03-24)*: Craftmade (Cart→Full, missing Kit Builder+CPQ); Geo Contemporary (add Online Ordering — has eOL traffic, no Cart); Designers Fountain/Godinger/Butler (iPad-only → iPad+Catalog).

**Complexity**: Simple · **Data Dependency**: BigQuery `expansion_candidates` + Health V2 CSV + VM-48 · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-CI-07, Health V2 (Growth Score)

**Allowed Claims**: bundle/feature-gap/headroom signals; named candidates from `expansion_candidates`. **Forbidden Claims**: sharing expansion signals with the client · internal segment labels in client-facing text.

**Internal use**: CS / Sales upsell targeting. **Portability**: fully portable.

---

### VM-29: Churn Risk (Composite Output)

**Audience**: Internal [I] · **Commerce Lens**: Non-commerce · **Internal Name**: churn_risk_composite · **Customer-Facing Name**: N/A — internal only

**Client value**: Internal — the customer benefits via earlier, proactive support before problems escalate. · **SuperCat value**: The highest-ROI internal use — saving one at-risk account outweighs many new sales.

**Decision**: *"Paying-but-disengaged accounts, composite-scored — reach out with a diagnostic ('your imports stopped — can we help?'), not a pitch."* Churn prevention is the highest-ROI internal use of the layer.

**Gating**: Health V2 risk modifiers + BigQuery `at_risk_accounts`.

**Signal**: composite of VM-06 (rep engagement decline), VM-36 (portal-traffic decline), Health V2 risk modifiers — **RM-1** ARR>$5K & 0 logins/90d→cap 20; **RM-2** primary metric down >60% & value<20→cap 20; **RM-3** 5+ L3+ escalations→cap 30; **RM-4** `days_since_critical_update`>180 for 2+ entities→cap 30 — plus the `at_risk_accounts` view.

**Example** *(live 2026-03-24)*: Jonathan Charles (risk 125, ARR $27.8K — 0 logins/0 orders, RM-1); Bliss Studio (125, $6.8K); Tomlinson & Interlude (paying, disengaged).

**Complexity**: Simple · **Data Dependency**: BigQuery `at_risk_accounts` + `portal_health_alerts` + Health V2 operator · **Data Readiness**: Live (automated) · **Bundle**: All · **Query IDs**: Q-CI-01, Q-CI-08, Health V2

**Allowed Claims**: at-risk identification with risk factors; Health V2 risk-modifier status. **Forbidden Claims**: sharing churn scores with clients · treating a single signal (login decline alone) as definitive without the composite.

**Internal use**: CS churn prevention. **Portability**: fully portable.

---

### VM-30: Support Burden Analysis

**Audience**: Internal [I] — optional external-safe framing · **Commerce Lens**: Non-commerce · **Internal Name**: support_burden · **Customer-Facing Name**: (Optional) Support Partnership Summary

**Client value**: Indirect — faster issue resolution and proactive prevention. · **SuperCat value**: Cuts support cost per account and targets where product investment most reduces ticket load.

**Decision**: *"This account carries disproportionate support load (162 tickets, 48% S1/S2, eOL-heavy) — deploy proactive monitoring on the top drivers; feeds churn risk."*

**Gating**: HelpScout account matching (~80% exact / ~95% fuzzy; email-domain-based, approximate — Health V2 OD-6).

**Signal** (Q-HS-01..06): per-account HelpScout volume, response time, topic/severity/type/level distribution; flag disproportionate load.

**Example** *(BCF — validated)*: 162 tickets (2nd highest), trend declining (11/qtr); eOL 18% (vs ~7%), bug 39%, S1/S2 48%; primary contact = BCF's Catalog/Data Manager (VM-04).

**Complexity**: Moderate · **Data Dependency**: BigQuery `helpscout.conversations`/`conversation_threads`/`customers` · **Data Readiness**: Live · **Bundle**: All · **Query IDs**: Q-HS-01..06

**Allowed Claims**: internal per-account volume/tags/trend; external-safe — "how your support interactions break down by category" (omit internal severity + cross-account comparisons). **Forbidden Claims**: sharing cross-account comparisons · sharing internal S1/S2 externally without reframing · claiming exact matching where fuzzy may have erred.

**Internal use**: CS health context (feeds VM-29). **Portability**: moderate (~80% exact match).

---

### VM-48: HubSpot Expansion Signals

**Audience**: Internal [I] · **Commerce Lens**: Non-commerce · **Internal Name**: hubspot_expansion_signals · **Customer-Facing Name**: N/A — internal only

**Client value**: Internal only — never client-facing. · **SuperCat value**: CS prep — surfaces open expansion deals + stage so the account team acts on a live opportunity; a CRM-hygiene prompt, not a measured claim.

**Decision**: *"Where the platform says 'ready to expand' AND HubSpot has an open late-stage deal, that's the highest-confidence CS/Sales action — go there first."*

**Gating**: HubSpot BigQuery sync active; `hubspot_company_id` mapping present (157/252 orgs mapped, live 2026-06-30).

**Signal** (Q-48 — **pending authoring**): HubSpot deal stage, lifecycle stage, open-opportunity count, last sales activity per account, combined with VM-28 platform signals.

**Example** *(illustrative)*: Craftmade — Health V2 Expand + bundle upgrade signal + HubSpot Stage 3 "Contract Sent" (45d open) + CS call 12d ago → follow up on contract.

**Complexity**: Simple · **Data Dependency**: BigQuery HubSpot tables + `hubspot_company_id` mapping · **Data Readiness**: Live (data); **Q-48 query pending** in `query_library_v2.md` · **Bundle**: All · **Query IDs**: Q-48 (pending)

**Allowed Claims**: HubSpot deal stage/lifecycle as internal CS context; combined platform+CRM priority list. **Forbidden Claims**: sharing HubSpot deal data with clients · CRM data in client-facing reports.

**Internal use**: CS / Sales expansion. **Portability**: fully portable for HubSpot-mapped accounts.

---

## Domain 8 — Portal & Demand-Side Intelligence

*Powered by Clicky Analytics data in BigQuery — 48 client portals, 22 table types per client. This is the demand-side complement to Mixpanel's supply-side rep behavior. All VMs in this domain are gated to `has_clicky = true`.*

*Do not mention Clicky Analytics in client-facing reports when `has_clicky = false`. For clients without Clicky, Clicky setup is a SuperCat-side action item (noted in internal brief, not surfaced to client).*

*VM-36 appears in this domain because it reads Clicky data, but it feeds Domain 7 (VM-29 Churn Risk). It is an input signal family, not a standalone output.*

---

### VM-31: Portal Traffic Health

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: portal_traffic_health · **Customer-Facing Name**: Online Catalog Traffic Report

**Client value**: Visibility into a channel they can't otherwise see — "how many dealers actually visit our portal?" · **SuperCat value**: Portal engagement is a retention signal and a cross-portal benchmark differentiator (declines feed VM-36).

**Decision**: *"X buyers/day are browsing your online catalog (above the ~170 cross-portal median) — and declining traffic is your earliest churn warning."*

**Gating**: `has_clicky=true`.

**Signal** (Q-CL-01): daily unique visitors, pageviews, bounce, session duration → monthly trend vs cross-portal median.

**Example** *(Gabby — validated)*: ~374 avg daily visitors (median ~170), 14% bounce, 8-min sessions (engaged); December dip mirrors eCat seasonality.

**Complexity**: Simple · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics` · **Data Readiness**: Live (gate `has_clicky`) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-01

**Allowed Claims**: daily visitors/pageviews/bounce/session trend; cross-portal benchmark. **Forbidden Claims**: traffic figures for non-`has_clicky` clients · attributing traffic to specific dealers without visitor-identity confirmation.

**Who pays**: CS / marketing. **Portability**: data-gated (48 portals; BCF not among them — setup pending). *(Feeds VM-36 churn signal.)*

---

### VM-32: Portal Content Performance

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: Non-commerce · **Internal Name**: portal_content_performance · **Customer-Facing Name**: Online Catalog Content Report

**Client value**: Content performance pairing browsing with order data — an insight no single system produces alone. · **SuperCat value**: Proves the supply-side + demand-side data integration that is a core Insights differentiator.

**Decision**: *"SOFAS pull 45% of your browsing but only 22% of GMV — that high-view/low-order gap is a pricing/availability/detail problem worth fixing."*

**Gating**: `has_clicky=true` AND page-level data available (validate date range/coverage first).

**Signal** (Q-CL-02): page-level views (product/category/section), entrance/exit patterns; cross-reference top pages with eCat orders for high-view/low-order gaps.

**Example** *(illustrative)*: SOFAS 45% of pageviews vs 22% of eCat GMV → conversion opportunity.

**Complexity**: Moderate · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_pages` + MCP `orders` · **Data Readiness**: Conditional Live (per-portal data varies) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-02

**Allowed Claims**: top-viewed pages/categories; browse-to-order conversion where data permits. **Forbidden Claims**: conversion conclusions without sufficient page+order data for that portal.

**Who pays**: CS / merchandising. **Portability**: data-gated (page data varies by portal/date).

---

### VM-33: Geographic Demand Map

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: geographic_demand_map · **Customer-Facing Name**: Online Catalog Geographic Demand Report

**Client value**: Demand geography usually only available from market research — built from real portal engagement. · **SuperCat value**: "Demand where you don't have coverage" is a direct expansion conversation (reps / territory / portal).

**Decision**: *"Your portal draws visitors from 20 states but your reps cover 12 — 8+ states have organic demand you're not converting."*

**Gating**: `has_clicky=true`.

**Signal** (Q-CL-03): portal visitors by state/region × visit volume; cross-reference rep territory for demand-supply gaps.

**Example** *(Gabby — validated)*: top states GA 8,568, TX 8,448, AL 7,655, FL 5,316; 20 states with traffic vs 12 covered.

**Complexity**: Simple · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_regions` (+ MCP rep territory) · **Data Readiness**: Live (gate `has_clicky`) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-03

**Allowed Claims**: state-level visitor volume; regions with traffic but no known rep coverage. **Forbidden Claims**: geographic visitor data for non-`has_clicky` clients.

**Who pays**: Sales leadership / expansion. **Portability**: data-gated (international may use `billing_country`).

---

### VM-34: Visitor Organization Identification

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: Non-commerce · **Internal Name**: visitor_org_identification · **Customer-Facing Name**: Portal Visitor Companies Report

**Client value**: "These companies are browsing your catalog" — a lead-gen signal (ISP-limited, but valuable on corporate networks). · **SuperCat value**: A unique capability — no competitor deanonymizes visitors on the manufacturer's catalog portal.

**Decision**: *"Named corporate visitors not in your dealer list are leads — but most traffic resolves to residential ISPs, so this shines only where dealers use corporate networks."*

**Gating**: `has_clicky=true`; value depends on visitor network (B2B/corporate networks identify; residential ISPs don't).

**Signal** (Q-CL-04): reverse-DNS org identification from Clicky `organizations`; "Business" ISP variants + named corporate networks are the actionable subset.

**Example** *(Gabby — validated)*: top orgs iCloud Private Relay 15,221, Comcast 11,996, Spectrum 7,761, Spectrum Business 2,804, Cox Business 2,431 — most residential; "Business" variants = commercial proxy.

**Complexity**: Simple · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_organizations` · **Data Readiness**: Conditional Live (accuracy varies) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-04

**Allowed Claims**: named-org visits where corporate-network ID confirmed; "Business" ISP counts as commercial-visitor proxy. **Forbidden Claims**: claiming company identity from ISP alone · presenting ISP counts as company counts.

**Who pays**: Sales (lead gen). **Portability**: data-gated (depends on visitor network type).

---

### VM-35: Traffic Source Intelligence

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce · **Internal Name**: traffic_source_intelligence · **Customer-Facing Name**: Online Catalog Traffic Source Report

**Client value**: How dealers find the portal — marketing-channel intelligence they usually lack. · **SuperCat value**: Drives portal-adoption conversations (low direct traffic → a dealer-communication campaign).

**Decision**: *"60% direct traffic = strong dealer awareness; if yours is <30% direct, run a dealer-comms campaign to drive portal awareness."*

**Gating**: `has_clicky=true`.

**Signal** (Q-CL-05): source distribution (Direct/Referral/Search/Social/Email/Ads) → dealer awareness, SEO, marketing-channel performance.

**Example** *(Gabby — validated)*: Direct 44,996 (59.7%), Referral 28,112 (37.3%), Organic Search 1,779 (2.4%) — strong recall, weak SEO.

**Complexity**: Simple · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_traffic_sources` · **Data Readiness**: Live (gate `has_clicky`) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-05

**Allowed Claims**: traffic-source distribution + trend; direct-% as dealer-awareness proxy. **Forbidden Claims**: traffic-source data for non-`has_clicky` clients.

**Who pays**: Marketing / CS. **Portability**: data-gated.

---

### VM-36: Portal Traffic Decline Signal *(Churn Input → VM-29)*

**Audience**: Internal [I] — input signal feeding VM-29 · **Commerce Lens**: Non-commerce · **Internal Name**: portal_traffic_decline_signal · **Customer-Facing Name**: N/A — internal churn signal

**Client value**: Internal churn signal — the customer benefits via a proactive save before they disengage. · **SuperCat value**: Demand-side disengagement leads supply-side (logins/orders) by 30–60 days; an early churn input to VM-29.

**Decision**: *"2+ consecutive months of >15% portal-traffic decline = earliest demand-side churn flag — fires RM-level urgency into VM-29, 30–60 days before reps go quiet."*

**Gating**: `has_clicky=true`.

**Signal** (Q-CL-01 → Q-CI-08): MoM portal daily-visitor trend; ≥2 consecutive months >15% decline → fires into `at_risk_accounts`/VM-29. Demand-side disengagement leads supply-side by 30–60 days.

**Example** *(validated 2026-03-24)*: Sixtrees & Renwil CRITICAL (traffic crashed >30%, <5 visitors/day) → RM-level urgency in VM-29. Counter-example Gabby: Dec −19% then Jan +31% = seasonal, not churn.

**Complexity**: Simple · **Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics` → `at_risk_accounts` + VM-29 · **Data Readiness**: Live (gate `has_clicky`) · **Bundle**: eCat Online + Clicky · **Query IDs**: Q-CL-01, Q-CI-08

**Allowed Claims**: MoM portal-traffic trend as a churn input; CRITICAL/WARNING portal-health flags. **Forbidden Claims**: presenting as standalone churn prediction without the VM-29 composite · sharing decline signals with clients.

**Internal use**: churn early-warning (VM-29 synthesizes VM-06 + VM-36 + Health V2 RMs). **Portability**: data-gated to Clicky portals.

---

## Domain 9 — Commerce Economics (the "Money Map," Layer 1)

*The owner/CEO/CFO/PE-grade economics of how a client sells — revenue, realization, concentration, conversion, returns, quality, and (gated) margin. Built on invoiced `net_amount` truth and within-table arithmetic. Full design + rankings in [`insights_moneymap_SYNTHESIS.md`](insights_moneymap_SYNTHESIS.md); every figure obeys the through-line gate in the header. All example dollars are `[ILLUSTRATIVE]`.*

> **Note on inline `Rank N` tokens (Domains 9–13).** The `**Rank N**` markers in the VM bodies below are the **legacy money-map AGREE-3/3 scores**, retained as design provenance. They are **superseded by the single [Unified Stack Rank](#unified-stack-rank-v41)** (top of document), which is the authoritative cross-domain priority. Where a legacy `Rank N` and the Unified Stack Rank tier disagree, **the Unified Stack Rank wins** (e.g., VM-C1's legacy "Rank 1" and the unified Tier-S anchor agree; VM-CHAN-1's legacy "Rank 9" maps to unified Tier B).

**Domain-wide gating (inherited by every VM below):** run `Q-ECON-00`/`Q-PROV-00` first → read `TOTAL_BUSINESS_SOURCE`, `COMMERCE_CONFIDENCE`, `report_through_date`, `FEED_COMPLETENESS`. A money number is shown **at its lowest input's confidence or not at all**; `NONE`/`PROVABLY-INCOMPLETE`/`DEAD` → suppress; `PARTIAL` → labeled floor; never print `$0`/stale totals; always say **invoiced**, never **collected**. The eCat-SALE filter (Spine §6.5) excludes quotes/holds/wishlists from every sales numerator (the FAL trap: $37.9M → $0.98M).

> ### Query-ID Reconciliation (catalog ↔ `query_library_v2.md`) — authoritative
> The C-series numbering follows the **Money Map synthesis design** ([`insights_moneymap_SYNTHESIS.md`](insights_moneymap_SYNTHESIS.md)). The **audited SQL library is a deliberately smaller hardened set** (only pilot "GO" candidates shipped). This table is the source of truth for what is **live in the library** vs **designed/pending**; inline `**Query IDs**` tokens on each VM are indicative and defer to this table.
>
> | VM | Live query in `query_library_v2.md` | Status |
> |---|---|---|
> | VM-C1 | `Q-ECON-00`, `Q-PROV-00`, `Q-16` | ✅ live |
> | VM-C2 / C12 | `Q-ECON-LEAK` (tier-aware dispersion; **naive "% off list" was KILLED in hardening** — list semantics vary MSRP vs wholesale) | ✅ live |
> | VM-C4 | `Q-59` (Fill Rate & Backorder Revenue Impact) | ✅ live |
> | VM-C5 | `Q-ECON-RETURNS` | ✅ live |
> | VM-C13 | `Q-60` (Price Erosion / Trade-Down) | ✅ live |
> | VM-C14 | `Q-45`, `Q-CHAN-05` | ✅ live |
> | VM-C15 | `Q-ECON-LEADTIME`, `Q-ECON-TERMS` (narrow) | ✅ live (partial) |
> | VM-C16 | `Q-ECON-NETREV` (net-of-freight, **not** margin) | ✅ live |
> | VM-C18 | `Q-ECON-CARRIER`, `Q-ECON-NETREV` | ⚠️ conditional |
> | VM-C22 | `Q-54` (Geographic eCat Penetration), `Q-67` (Geographic Revenue Displacement) | ✅ live |
> | VM-C23 | `Q-42` (New Item Performance), `Q-61` (New Introduction Adoption Gap) | ✅ live |
> | VM-C24 | `Q-SELL-QC` (quote→purchase), `Q-21` (order type) | ✅ live |
> | VM-C3 | `Q-ECON-CONC` (top-N share + HHI) | ✅ live (validated 2026-06-30, cci) |
> | VM-C7 | `Q-ECON-QUALITY` (recurring vs one-time) | ✅ live (validated 2026-06-30, cci) |
> | VM-C8 | `Q-ECON-SEASON` (multi-year month-share) | ✅ live (validated 2026-06-30, cci) |
> | VM-C9 | `Q-ECON-PACE` (pacing-band inputs) | ✅ live (validated 2026-06-30, cci) |
> | VM-C10 | `Q-ECON-MOMENTUM` (comparable-window YoY) | ✅ live (validated 2026-06-30, cci) |
> | VM-C11 | `Q-ECON-LUMP` (invoice-size dist + Gini) | ✅ live (validated 2026-06-30, cci) |
> | VM-C17 | `Q-ECON-NRR` (dollar NRR + expansion/contraction) | ✅ live (validated 2026-06-30, cci) |
> | VM-C20 | `Q-ECON-CONTRIB` (contribution proxy, **not** margin) | ✅ live (validated 2026-06-30, cci) |
> | VM-48 | `Q-48` (HubSpot expansion signals — **internal only**, BigQuery) | ✅ live (validated 2026-06-30) |
> | VM-C19, C21, C25 | — | ⏳ **cost-gated / client-input** (`unit_cost` / show cost) |
>
> Related Domain-9 enrichment queries also in the library: `Q-55` (category competitive displacement → Exception S2), `Q-68` (spending contraction → C17/K3), `Q-51`–`Q-70` (rep/customer enrichment). **Customer K-series** maps to the CI authority `customer_query_library.md` (`G-00` + `CQ-01..CQ-26`), not this library.

---

### VM-C1: True Topline

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: true_topline · **Customer-Facing Name**: Total Business Overview *(supersedes VM-16)*

**Client value**: The honest total-business number (invoiced net) with a completeness label — the anchor every other figure ties back to. · **SuperCat value**: The trust anchor of the whole report; getting the total right is what earns the right to say anything else.

**Decision & Dollar**: *"The revenue number in your board deck can be off by up to 9×. Here is the one figure that reconciles to your own Sales Portal to the dollar — `$XXM` invoiced — and the monthly shape behind it."* The denominator that makes every other money VM honest.

**Gating**: `Q-PROV-00` source = INVOICES (preferred) → `SUM(portal_invoices.net_amount)`; `portal_orders` is the labeled booked fallback only. Carries the `FEED_COMPLETENESS` verdict: **CORROBORATED** (booked≈invoiced, 0.90–1.30) → present as complete-**STRONG** (Option A: corroboration is internal, so STRONG not FULL); **UNVERIFIED–SINGLE-FEED** → "single-source; channel completeness unverified," **cap STRONG** (Spine §6.3 — single-feed UNVERIFIED caps at STRONG, never PARTIAL on consistency grounds); **PROVABLY-INCOMPLETE** (eCat > invoiced, e.g. `sc`) → **PARTIAL** + never "complete"; **DEAD** (`heb`) → **suppress**; **STALE** (>45d, e.g. `mhc`, live 190d) → PARTIAL, cap window at `report_through_date`, **and** carry any `DOESNT_CORRELATE` reconciliation caveat (mhc is *both* stale and non-OVERLAPS — the window-clamp must not mask the reconciliation flag).

**Signal**: `SUM(COALESCE(net_amount, Σ line discount-adjusted amount))` over `portal_invoices` by month/quarter/LTM, credit memos included as negatives, date-clamped `2010-01-01 .. CURRENT_DATE+90d`. ~14 of 21 cohort orgs are completeness-CORROBORATED; ~1 in 3 are not (live re-check 2026-06-30: 4/6 probe orgs in band — `vm_org_coverage_matrix_2026-06-30.md`). **Coverage guard:** CORROBORATED also requires the booked feed *materially present* — `bcf`'s `portal_orders` covers only ~11% of invoiced, so despite a clean topline it is UNVERIFIED-SINGLE-FEED, not CORROBORATED. The 0.90–1.30 band is a *consistency* check, not proof of an independent feed (`cci` books 1.26× invoiced and still counts) — which is precisely why economics caps at STRONG (Option A).

**Example**: *"Your total invoiced business is `$XXM` (LTM); `FEED_COMPLETENESS`: STRONG, single-feed. Monthly shape attached. This is invoiced, not collected — we have no AR feed."*

**Complexity**: Simple · **Data Dependency**: MCP `portal_invoices` (→ `portal_orders` fallback) · **Data Readiness**: Live (suppress on PROVABLY-INCOMPLETE/DEAD) · **Query IDs**: Q-ECON-00, Q-PROV-00, Q-16

**Allowed Claims**: Invoiced total business with its `FEED_COMPLETENESS` label; monthly/quarterly shape clamped to `report_through_date`. **Forbidden Claims**: `SUM(portal_orders.total_amount)` as total business · "complete business" without CORROBORATED · any implication of cash collected · a `$0`/years-stale total.

**Who pays**: CEO / CFO. **Rank 1** (AGREE 3/3 — the spine).

---

### VM-C2: Net Realization & Discount Leakage

**Audience**: Dual [D] (internal-lead) · **Commerce Lens**: ERP total-business · **Internal Name**: net_realization_leakage · **Customer-Facing Name**: Price Realization & Discount Review

**Client value**: The gap between list and what you actually collected — discount leakage in real dollars. · **SuperCat value**: A direct recoverable-margin conversation and the realization input that feeds pacing and momentum.

**Decision & Dollar**: *"You think you sell at list — you don't. You gave away `$X` in discounts/credits last 12 months, and 40% went to accounts that didn't grow in return. A 2-point realization gain on a `$40M` book is `$800K` of pure margin with zero extra units."*

**Gating**: Discount columns populated (detect via fill-rate — an org that bakes discount into `unit_price` reads false-0 → **suppress the leakage claim**). Net-of-returns half requires `RETURNS_IN_FEED=true` (gross-only orgs → show discount, suppress net). Capped at `COMMERCE_CONFIDENCE`. **Tier-aware dispersion** (true median + tier guard + volume guard + house auto-exclude) — never "% off list." Mandatory human gut-check before client delivery.

**Signal** (`Q-ECON-LEAK`): per line gross = `qty × unit_price`; net = `qty × (unit_price − unit_price_discount) − extended_price_discount`; leakage = gross − net; list→net waterfall rolled by `customer_bill_to_number` / `rep_number` / `category_code`; cross-plot discount% vs account YoY growth (the high-discount/no-growth quadrant = recoverable pool).

**Example**: *"Discretionary spread concentrates in 3 reps; the widest is ~$163K / 5.9% of book vs ~2% peers — a discount-discipline conversation."* *(The naive build mis-flagged a volume-pricing rep as a "$1.35M / 42% rogue" — the guards exist to prevent exactly that.)*

**Complexity**: Complex · **Data Dependency**: `portal_invoice_items` (+ `quantity_returned`) · **Data Readiness**: Live (suppress where discount cols unpopulated) · **Query IDs**: Q-ECON-LEAK

**Allowed Claims**: Realized-vs-reference spread in $ and %, by account/rep/category, after the guards. **Forbidden Claims**: "% off list" / "overcharging" / "unauthorized" · leakage on zeroed-discount feeds · net-of-returns on gross-only feeds.

**Who pays**: CFO / VP Sales. **Rank 2** (AGREE 3/3). *(Pushed as Exception [VM-C2-rep](#vm-c2-rep-leakage-by-rep-the-rogue-discounting-alarm).)*

---

### VM-C3: Revenue Concentration & Single-Account Risk (HHI)

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: revenue_concentration_hhi · **Customer-Facing Name**: Revenue Concentration & Account-Risk Analysis

**Client value**: How exposed you are if a single top account walks — concentration risk most clients never quantify. · **SuperCat value**: A board-level risk metric (HHI) that reframes a "great year" against its fragility — a retention narrative.

**Decision & Dollar**: *"62% of your invoiced revenue rides on 9 accounts; your largest is `Y%` of the company and its spend quietly fell 18% — a `$4.1M` hole forming in plain sight."* The number that sets enterprise value, covenants, insurance, and the M&A story.

**Gating**: Invoiced source; **billing-entity grain** (no native parent key — `mapped_code` ~0%; parent roll-up is derived/gated, labeled "estimated family," see [VM-K6](#vm-k6-parent--corporate-family-roll-up)). Multiple bill-to codes for one parent **understate** concentration (real risk is worse, never overstated). `ORDERS`/`SALES_DATA` source → cap PARTIAL/LIMITED.

**Signal**: `SUM(net_amount)` by `customer_bill_to_number` LTM; top-1/5/10 share, **Herfindahl (HHI)**, Pareto curve, walk-away sensitivity (revenue if account N reverts to trailing run-rate or zero); repeat by `rep_number` (key-person risk) and category; geography from `customer_bill_to_state`. Decline signal = two equal comparable windows ending at `report_through_date`.

**Complexity**: Moderate · **Data Dependency**: `portal_invoices` · **Data Readiness**: Live · **Query IDs**: Q-ECON-CONC

**Allowed Claims**: Top-N share, HHI, walk-away $ at billing-entity grain. **Forbidden Claims**: parent/family concentration without the derived+gated label · concentration on a non-invoiced source framed as total-business.

**Who pays**: Owner / CFO / board / lenders / acquirers. **Rank 3** (AGREE 3/3). *(Customer-grain twin: [VM-K2](#vm-k2-concentration--single-account-risk-customer-grain); eCat cousin: VM-13.)*

---

### VM-C4: Booked→Invoiced Conversion & Fill Leakage

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: fill_leakage · **Customer-Facing Name**: Order Fill & Conversion Analysis

**Client value**: How much booked business never converts to invoiced — fill leakage you can act on. · **SuperCat value**: Connects bookings to cash; a fulfillment-not-billing story that also underpins pacing accuracy.

**Decision & Dollar**: *"You earned `$Y` in orders and shipped `$Z`. The N% you dropped is mostly fixable fulfillment — in-stock, reorderable demand — not lost customers."* Turns a fuzzy "we have stockouts" into a sized buy-inventory decision.

**Gating**: Computed **within one line** (`quantity_ordered` vs `quantity_invoiced` on the same `portal_invoice_items`/`portal_order_items` row) — sidesteps the ≈0% order→invoice header join. Non-OVERLAPS orgs → **never sum order+invoice tables** (double-count). Stale feed → clamp to fully-aged cohorts at `report_through_date`. STRONG.

**Signal**: fill rate = `Σ qty_invoiced / Σ qty_ordered`; leaked $ = (ordered − invoiced) × `unit_price`; segment by `item_number` (join `inventories` to split stockout vs cancel) and category; add post-ship layer from `quantity_returned`; open backlog = (ordered − invoiced + backordered) × price. Split structural (discontinued) vs addressable (reorderable).

**Complexity**: Moderate · **Data Dependency**: `portal_order_items`, `portal_invoice_items`, `inventories` · **Data Readiness**: Live · **Query IDs**: Q-ECON-FILL

**Allowed Claims**: Within-line fill rate, leaked addressable $, backlog. **Forbidden Claims**: summing order+invoice tables on non-OVERLAPS orgs · treating stale not-yet-shipped lines as leaked.

**Who pays**: CFO / COO / demand planning. **Rank 6** (AGREE 3/3).

---

### VM-C5: Returns & Credit-Memo Drag

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: returns_drag · **Customer-Facing Name**: Returns & Credit Analysis

**Client value**: How much credits and returns quietly drag down realized revenue, and which accounts/items drive it. · **SuperCat value**: A clean returns lens that sharpens contribution and realization — a recoverable-margin input.

**Decision & Dollar**: *"Gross sales say `$A`; after returns and credits you kept `$B`. The N-point drag is concentrated in M items and K accounts — and it's a product-quality early-warning."* Measured by **dollars, not count** (35% by count can be 8% by $).

**Gating**: `RETURNS_IN_FEED=true` — gross-only orgs (`ufi`, `pf`, `jyc`, `bcf`, + `kll`/`clm`/`lpf`/`wwjc`/`sarreid`) read a silent 0% → **suppress/relabel "returns not represented in your feed," never "$0 returns."**

**Signal**: return rate $ = `SUM(net_amount<0)` / gross positive, plus line `SUM(quantity_returned × unit_price)`; rank by `item_number`/`category_code`/`customer_bill_to_number`; trend monthly to catch a worsening defect/fit problem.

**Complexity**: Simple · **Data Dependency**: `portal_invoices` (credit memos), `portal_invoice_items.quantity_returned` · **Data Readiness**: Live (per-org gated) · **Query IDs**: Q-ECON-RETURNS

**Allowed Claims**: $-based return rate and concentration where returns are fed. **Forbidden Claims**: implying 0% returns on a gross-only feed.

**Who pays**: CFO / Ops / Quality. **Rank 7** (AGREE 3/3). *(Feeds the composite and roadmap exception C3.)*

---

### VM-C-POOL: Recoverable Margin Pool *(the literal "Money Map" — composite)*

**Audience**: Internal [I] → Dual when components trusted · **Commerce Lens**: ERP total-business · **Internal Name**: recoverable_margin_pool · **Customer-Facing Name**: Recoverable Margin Worklist

**Client value**: One worklist of the recoverable dollars across discount, returns, and freight — the literal "money map." · **SuperCat value**: The flagship composite — turns the economics domain into a prioritized action list and the strongest ROI artifact in the report.

**Decision & Dollar**: *"`$R` of margin is sitting in your own transaction data — here is the ranked, owner-assigned worklist to go get it: renegotiate these discounts, restock these lines, fix these returns, re-price this freight."* Each dollar traced to a line, a customer/rep, and an action.

**Gating**: Fusion of **C2 (off-policy discount) + C4 (dropped fillable demand) + C5 (returns drag) + C18 (under-recovered freight)** — built **only after each component is trusted in production**; shown at the **lowest confidence of its inputs**. **Net carefully** to avoid double-counting (a discounted line that also returns is one event, not two).

**Signal**: the four levers, netted and ranked by recoverable $, each with an action owner (VP Sales/pricing, demand planning/Ops, Quality/Ops, Finance/Ops).

**Complexity**: Complex (composite) · **Data Dependency**: C2+C4+C5+C18 outputs · **Data Readiness**: Deferred until components trusted · **Query IDs**: composite of Q-ECON-LEAK / -FILL / -RETURNS / -FREIGHT

**Allowed Claims**: a netted, owner-assigned recoverable-margin worklist at the lowest input confidence. **Forbidden Claims**: double-counting a discount-and-return as two recoveries · a predictive/optimization framing (the cut ML "early-warning"/"optimal-discount" bets).

**Who pays**: CFO + owner. **Rank 80 (fusion)** — the artifact the title promises.

---

### VM-C7: Revenue Quality — Recurring vs One-Time

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: revenue_quality_recurring · **Customer-Facing**: Revenue Durability Analysis. **Client value**: Know how much revenue is durable reorder business vs one-and-done you must re-win each year — the difference between real growth and churn-and-replace. · **SuperCat value**: Durable-revenue share is the number boards multiply; framing it makes SuperCat the system of record for revenue quality. **Decision & Dollar**: *"Only 58% of revenue is durable reorder business; the rest is one-and-done you re-win every year — your 'growth' is lumpier than it looks."* **Gating**: ≥2 full comparable windows ending at `report_through_date`; <2 or LIMITED source → suppress; classify seasonal buyers on multi-year cadence (pair with C11). **Signal**: per-account recurring (invoiced both windows / ≥2 periods) vs one-off $ split + reorder-interval stability grade. **Readiness**: Live · **Query IDs**: Q-ECON-QUALITY. **Allowed**: durable-revenue share/trend. **Forbidden**: durability on <2 windows. **Who pays**: CFO / board (drives the multiple). **Rank 8** (AGREE 3/3).

---

### VM-C8: Seasonality & Market-Month Calendar

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: seasonality_calendar · **Customer-Facing**: Seasonality & Cash Calendar. **Client value**: Shape cash, inventory, and staffing around the real demand curve instead of reacting month to month. · **SuperCat value**: Turns transaction history into an operating calendar — a recurring planning touchpoint that deepens reliance. **Decision & Dollar**: *"Two market months drive a third of your year — shape cash, inventory, and staffing around that curve."* **Gating**: ≥2–3 years, date-clamped; <2 yrs → suppress; one-off big order → use median-of-years per month. **Signal**: multi-year monthly `net_amount` → month-share curve; recurring market/showroom spikes (cross-ref `order_origin` market codes where present); peak-to-trough cash swing. **Readiness**: Live · **Query IDs**: Q-ECON-SEASON. **Allowed**: month-share curve, cash peaks/troughs. **Forbidden**: a single year's month as "the pattern." **Who pays**: CFO / Ops. **Rank 10**.

---

### VM-C9: Run-Rate Pacing (a range, never a forecast)

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: run_rate_pacing · **Customer-Facing**: Year-End Pacing Range. **Client value**: See where the year lands now (as a band), not in December — time to act while it still matters. · **SuperCat value**: A defensible pacing range (never a forecast) that makes the report a standing CFO / FP&A tool without overclaiming. **Decision & Dollar**: *"At today's pace plus your open book, you land the year at `$W ± band` — X% off last year, visible now, not in December. A pacing line, not a crystal ball."* **Gating**: ≥24 months, FULL/STRONG; **always a band, never a point**; date-clamp far-future corruptions. **Signal**: seasonally-adjusted trailing run-rate + open backlog (C4, discounted by historical fill) + recurring floor (C7); band widened by lumpiness (C11). **Readiness**: Live · **Query IDs**: Q-ECON-PACE. **Allowed**: a caveated pacing band. **Forbidden**: a point estimate · "forecast"/"prediction" (the cut "Quarter-End Oracle" nowcast). **Who pays**: CEO / CFO / FP&A. **Rank 9**.

---

### VM-C10: Comparable-Window Momentum (staleness-proof YoY)

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: comparable_window_momentum · **Customer-Facing**: True YoY Momentum. **Client value**: A true year-over-year number a lagging feed can't fake into a false crash. · **SuperCat value**: Staleness-proof momentum protects credibility — the trust foundation the whole economics domain rests on. **Decision & Dollar**: *"Your real YoY growth is N% — measured on equal, fully-billed windows so a lagging feed can't fake a crash."* **Gating**: both windows fully billed, equal length, **both ending at `report_through_date`** (the `mhc` fake-collapse fix); suppress trend on LIMITED/`SALES_DATA` (no dates). **Signal**: trailing-12mo vs prior-12mo invoiced; decompose into volume vs price/realization (via C2). **Readiness**: Live · **Query IDs**: Q-ECON-MOMENTUM. **Allowed**: equal-window YoY/QoQ. **Forbidden**: a trailing window running into empty post-feed months. **Who pays**: CEO / board. **Rank 5**.

---

### VM-C11: Revenue Lumpiness / Big-Deal Dependence *(the honesty metric)*

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: revenue_lumpiness · **Customer-Facing**: Big-Deal Dependence. **Client value**: Honest answer to "was that growth broad-based or three big deals?" before you bet on it. · **SuperCat value**: The integrity check that keeps every other economics claim honest — the moat is the discipline, not just the data. **Decision & Dollar**: *"That record quarter was three invoices — strip them out and you were flat. Here's how much of your 'growth' is broad-based vs a few big deals."* **Gating**: invoice grain; separate credit memos from the size distribution; annotate (don't auto-discount) legitimate large contract orders. **Signal**: distribution of invoiced $ by invoice size; top-1%/5% share; ex-top-N vs headline growth; Gini on invoice size. **Readiness**: Live · **Query IDs**: Q-ECON-LUMP. **Allowed**: ex-top-N growth, concentration of growth. **Forbidden**: presenting a lumpy headline as broad-based. **Who pays**: CFO / FP&A. **Rank 4** — *this is the suppression check that keeps the rest of the domain honest; rarely suppressed itself.*

---

### VM-C12: Price Realization by Account & Off-List Adherence

**Audience**: Dual [D] (internal-lead) · **Lens**: ERP total-business · **Internal Name**: price_realization_offlist · **Customer-Facing**: Off-List / Price-Discipline Review. **Client value**: See the dollars — and the reps — where you're billing below your own reference price. · **SuperCat value**: A recoverable-margin conversation framed safely as "below reference," not accusation — high value, low risk. **Decision & Dollar**: *"Your deepest-discounted accounts aren't your biggest, and on N% of lines you billed below your own published/entitled price — here's the $ and the reps doing it most."* **Gating**: `products.net_price` must be a meaningful reference (blank/0 → suppress off-list claim); net out known price-levels first → present **"below reference," not "unauthorized"**; suppress the recoverable-$ where tiers unknown (show spread descriptively). **Signal**: realized vs catalog `net_price` per item; realized vs price implied by `DefaultPriceCode`; gap $ by rep/customer/category. **Readiness**: Conditional (needs list/price-level context) · **Query IDs**: Q-ECON-OFFLIST. **Allowed**: below-reference spread $ where a clean reference exists. **Forbidden**: "unauthorized" framing · off-list on blank-`net_price` orgs. **Who pays**: VP Sales / CFO. **Rank 12** (AGREE 3/3).

---

### VM-C13: Price-Increase Pass-Through

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: price_passthrough · **Customer-Facing**: Price-Increase Pass-Through. **Client value**: How much of an announced increase you actually realized, and where the rest leaked back as discount. · **SuperCat value**: Connects pricing actions to realized dollars — a CFO / VP-Sales conversation few systems can support. **Decision & Dollar**: *"You announced a 6% list increase; you realized 3.8% — here's where the other 2.2 points leaked back as discount, and whether volume even moved."* **Gating**: needs a known increase date + stable item identity; no `net_price` history → use realized-price step-change as a labeled proxy; control for category/item mix; elasticity is correlational — hedge, never causal. **Signal**: realized price (`unit_price − unit_price_discount`) before/after net of mix; pass-through % = realized Δ ÷ list Δ; pair with volume change. **Readiness**: Conditional (soon) · **Query IDs**: Q-ECON-PASSTHRU. **Allowed**: pass-through % with mix controls. **Forbidden**: causal elasticity claims. **Who pays**: CFO / VP Sales. **Rank 16**.

---

### VM-C14: eCat Capture / Platform Footprint

*Capture, not attribution.*

**Audience**: Dual [D] — Conditional [C] · **Lens**: Comparative capture · **Internal Name**: ecat_capture_footprint · **Customer-Facing**: eCat Platform Penetration *(supersedes VM-45; channel headline is [VM-CHAN-1](#vm-chan-1-ecat-vs-non-ecat-split-the-headline))*. **Client value**: How much of total invoiced business eCat carries, and whether that share is climbing. · **SuperCat value**: The platform-value headline — proves eCat's footprint and the runway to grow it (the expansion narrative). **Decision & Dollar**: *"eCat carries X% of your total invoiced sales — and that share is climbing N points a year. The rest flows through every other channel."* **Gating** *(rate only when ALL hold)*: `TOTAL_BUSINESS_SOURCE=INVOICES`, `COMMERCE_CONFIDENCE ≥ STRONG`, **`FEED_COMPLETENESS=CORROBORATED`**, eCat-SALE GMV ≤ invoiced, share ≥ 5%. Else **absolute captured dollars only**. `sc` (eCat > invoiced, >100%) → suppress and report the completeness gap. **Signal**: eCat-SALE `orders` GMV ÷ invoiced total (`Q-PROV-00`); posture band (>50% primary / 25–50% dual / 10–25% growing / <10% enablement-heavy). **Readiness**: Conditional (rate); absolute capture broad · **Query IDs**: Q-45 (invoiced denominator + completeness gate). **Allowed**: capture share *when gated in*; absolute captured GMV *always*. **Forbidden**: `portal_orders` denominator · a rate when the gate fails · attribution ("eCat drove X%") · low capture = failure. **Who pays**: SuperCat + CEO. **Rank 9** — *capture is a fact; attribution is a suppressed estimate (Spine §4).*

---

### VM-C15: Working Capital — Backlog Aging & Booking-to-Cash Lag

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: working_capital_backlog · **Customer-Facing**: Backlog & Cash-Conversion Analysis. **Client value**: How much cash is tied up in aged backlog and order-to-cash lag — every extra day has a dollar cost. · **SuperCat value**: A treasury-grade working-capital lens from data you already hold; elevates the report to the CFO's desk. **Decision & Dollar**: *"`$4.7M` of booked orders are >90 days unshipped, and you wait N days from order to cash — every extra day is `$D` of working capital tied up."* **Gating**: **cohort/distributional lag only** (no 1:1 join); pair with C4 so backorders read as fulfillment not billing dysfunction; cap at `report_through_date`; age out dead never-to-ship orders. **Signal**: open booked $ aged by `order_date`; expected ship via `inventories.next_scheduled_receipt_date`; order-month→invoice-month cohort lag × daily revenue. **Readiness**: Conditional (PARTIAL) · **Query IDs**: Q-ECON-WCAP. **Allowed**: distributional lag, aged backlog. **Forbidden**: per-order order→invoice trace. **Who pays**: CFO / Treasury. **Rank 20**.

---

### VM-C16: Revenue Composition Strip-Out (freight / tax / discount)

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: composition_stripout · **Customer-Facing**: Product-Revenue Strip-Out. **Client value**: Your real product revenue (and true margin %) once freight and tax pass-through are stripped out. · **SuperCat value**: Foundational plumbing for C2/C19/C20 — owning the clean revenue denominator makes the rest defensible. **Decision & Dollar**: *"6% of your 'revenue' is freight and tax pass-through — your real product sales are smaller (and your margin % higher) than you think."* **Gating**: header component cols populated and meaningful; orgs that fold freight into line price → **suppress strip-out, report topline as-is**; don't double-subtract a discount already netted into `net_amount`. **Signal**: decompose `portal_invoices` `net_amount` vs `freight_amount`/`tax_amount`/`discount_amount` → product-only revenue + clean margin denominator. **Readiness**: Live (where itemized) · **Query IDs**: Q-ECON-COMPOSITION. **Allowed**: product-only revenue where components are itemized. **Forbidden**: strip-out on bundled-freight orgs. **Who pays**: CFO (foundational plumbing for C2/C19/C20). **Rank 13**.

---

### VM-C17: Net Revenue Retention ($-based, all-channel)

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: nrr_dollar · **Customer-Facing**: Net Revenue Retention. **Client value**: What your existing book is worth year-over-year before a single new logo — the leaky-bucket number. · **SuperCat value**: NRR$ is the retention metric investors price; surfacing it positions SuperCat at the board level. **Decision & Dollar**: *"Your existing accounts are worth 96 cents on the dollar year-over-year — you're refilling a leaky bucket before counting a single new logo."* **Gating**: ≥2 yrs contiguous, stable keys; customer-number changes / bill-to splits → reconcile keys, present a band; gross-of-returns slightly inflates. **Signal**: cohort by first-invoice period; this-year ÷ last-year `net_amount` = NRR$; decompose expansion vs contraction. *(Money-framed; the who's-churning version is [VM-K3](#vm-k3-account-decline--churn-risk).)* **Readiness**: Conditional (≥2 yrs) · **Query IDs**: Q-ECON-NRR. **Allowed**: NRR$ band, expansion/contraction split. **Forbidden**: NRR on unstable keys without a band. **Who pays**: CEO / CFO / investors. **Rank 13**.

---

### VM-C18: Freight & Small-Order Recovery

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: freight_recovery · **Customer-Facing**: Freight & Small-Order Economics. **Client value**: Freight you under-recover and the small orders that lose money once freight is netted — six figures in aggregate. · **SuperCat value**: A concrete margin-recovery action (minimum-order / freight policy) with a dollar figure attached. **Decision & Dollar**: *"You under-recovered `$C` in freight last year — six figures in aggregate — and orders under `$500` lose money once you net freight. You ship 9,000 of them a year."* **Gating**: org must **itemize** `freight_amount` (bundled → reads $0 → "itemized freight only"); without a carrier cost feed, report **charged** freight trends, not recovery %; exclude free-freight promos/prepaid. **Signal**: `SUM(freight_amount)` charged vs modeled cost by order size/region/channel; break-even order value + loss tail; minimum-order/freight-policy threshold with $ impact. **Readiness**: Live (charged); recovery % cost-gated · **Query IDs**: Q-ECON-FREIGHT. **Allowed**: charged-freight trend, break-even size. **Forbidden**: recovery % without a cost side. **Who pays**: CFO / Ops. **Rank 16**.

---

### VM-C20: Customer Contribution & Account Margin Tiering

**Audience**: Dual [D] (internal-lead) · **Lens**: ERP total-business · **Internal Name**: customer_contribution · **Customer-Facing**: Account Contribution Tiering. **Client value**: Which "top" accounts you actually keep money on once discounts, returns, and freight are netted. · **SuperCat value**: Reframes account value from revenue to contribution — drives renegotiation and the landed-cost upsell to true margin. **Decision & Dollar**: *"Your #3 account by revenue is your #11 by what you actually keep — and your #5 by sales is your #2 by margin loss. Discounts, returns, and freight eat the difference."* **Gating**: inherits every C2/C5/C18 gate; **without cost it is a contribution proxy, not gross profit — label precisely**; freight allocation is assumption-heavy. **Signal**: per account `net_amount` − discount (C2) − returns (C5) − under-recovered freight (C18) = contribution proxy; sales-vs-margin quadrant; surface biggest rank-drops for renegotiation. **Readiness**: Live (contribution proxy). Landed cost unlocks **true margin** (→ VM-C19/C21), but the single-feed presentation ceiling stays **STRONG**, not FULL (Option A). · **Query IDs**: Q-ECON-CONTRIB. **Allowed**: contribution proxy ranking, labeled. **Forbidden**: calling it gross profit without verified cost. **Who pays**: CFO / VP Sales. **Rank 15**.

---

### VM-C22: Geographic Profit Map

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: geographic_profit_map · **Customer-Facing**: Regional Economics Map. **Client value**: Which regions look strong on sales but thin on what you keep, and why (freight / discount). · **SuperCat value**: A derivative cut that extends the economics story into territory and ops decisions. **Decision & Dollar**: *"The Northeast is your #1 region by sales and #4 by margin — freight and discounts eat the difference."* **Gating**: prefer **ship-to** geo (bill-to ≠ ship-to misplaces freight); without cost → a **contribution** map, labeled (not profit); needs a clean state field. **Signal**: price/freight/(cost) bridge rolled to `customer_bill_to_state`/region; margin per $ and per shipment; overlay rep/territory. **Readiness**: Conditional (contribution now; profit cost-gated) · **Query IDs**: Q-ECON-GEO. **Allowed**: regional contribution map. **Forbidden**: "profit" map without cost. **Who pays**: CRO / Ops. **Rank 20** — *a derivative cut of C18/C19/C20.*

---

### VM-C23: New-Introduction Revenue Vitality

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: new_intro_vitality · **Customer-Facing**: New-Product Revenue Vitality. **Client value**: How much revenue your last 12 months of launches actually produce — your innovation engine, compounding or stalling. · **SuperCat value**: A CEO-level vitality metric from a derived first-sale date — elevates the buyer persona. **Decision & Dollar**: *"Items launched in the last 12 months are 9% of revenue — your innovation engine is either compounding or stalling, and now you can see which."* **Gating**: **prefer a derived first-sale date** over the `products.new_item` flag (flags go stale, never cleared → overstate vitality). **Signal**: `SUM(net_amount line)` for items with first-sale < 12mo ÷ total invoiced; trend the vitality %. **Readiness**: Live · **Query IDs**: Q-ECON-VITALITY. **Allowed**: vitality % on a derived first-sale date. **Forbidden**: vitality off a stale `new_item` flag. **Who pays**: CEO / CFO. **Rank 13** — *money-framed only; assortment curation is out of Layer 1.*

---

### VM-C24: Quote-to-Cash Pipeline Value (eCat) *(pipeline, never sales)*

**Audience**: Dual [D] · **Lens**: eCat transaction · **Internal Name**: quote_to_cash_pipeline · **Customer-Facing**: eCat Pipeline Value. **Client value**: Forecastable eCat pipeline (labeled pipeline, never sales) that nobody is currently tracking. · **SuperCat value**: Monetizes the quote data eCat already captures — pipeline value that strengthens the sales-process story. **Decision & Dollar**: *"Your reps wrote `$Q` in eCat quotes; historically ~22% convert and bill within 60 days — `$700K` of forecastable pipeline nobody's tracking. This is pipeline, not revenue."* **Gating**: **never sum quote $ into sales (the FAL trap — $37.9M → $0.98M, 97% quotes)**; conversion is cohort % only (≈0% 1:1 join + re-keying); `order_type` vocabulary is per-org. **Signal**: `order_type` states (Quote/Estimate/Hold/WishList vs Confirmed) as a funnel — the rows eCat-SALE excludes — cohort quote→confirmed→invoiced conversion + timing; value the live pipeline. **Readiness**: Conditional (PARTIAL; per-org state map) · **Query IDs**: Q-ECON-PIPELINE / Q-SELL-QC. **Allowed**: pipeline $ + cohort conversion, labeled "pipeline." **Forbidden**: any quote figure called "sales." **Who pays**: VP Sales / CFO. **Rank 18**.

---

### VM-C19 / VM-C21 / VM-C25 — ⏳ COST-GATED ("the one ask": a landed `unit_cost` column)

> These are the highest-*value* economics insights but are **`pending_engineering` / Deferred** until a verified landed `unit_cost` per item-period lands on the invoice line. **Never impute cost; if cost coverage < 90% of invoiced $, show revenue mix only and flag "margin pending cost feed."** The *trend/mix* decomposition can survive imperfect cost; the *level* cannot — label separately.

- **VM-C19 Margin Pool & Mix (PVM bridge)** — *"Revenue is flat but gross margin slid 2.3 points — same dollars of cheaper-margin mix; your biggest revenue line isn't your biggest profit line."* Price/volume/mix bridge on invoice lines. **Rank 22** — the lobbying target; one column unlocks C19/C21 + the true-margin half of C20/C22.
- **VM-C21 Margin-Weighted Concentration** — *"Your revenue looks diversified; your profit depends on three accounts."* C3 re-run on margin. **Suppress whenever C19 is suppressed.** **Rank 23**.
- **VM-C25 Market & Trade-Show $ ROI** — *"High Point booked `$2.1M`; only `$1.3M` invoiced and 18% reordered — show ROI is half the booking number."* Needs market-coded `order_origin` (gated by `Q-CHAN-00`) **and** client-supplied show cost. **Suppress without both.** **Rank 24**.

---

## Domain 10 — Channel / "Where You Sell"

*Answers "where you sell" at two levels, gated on the one column that carries channel — `portal_orders.order_origin`. Full evidence in [`commerce_where_you_sell.md`](../_archive/commerce_layer1_build/commerce_where_you_sell.md). The structural fact: `portal_invoices` (the sales truth) has **no** channel field, so channel **mix** comes from `order_origin` (booked grain) applied as a lens over the invoiced magnitude — and `order_origin` is bespoke/sparse (~8 of 41 orgs usable; only `cci` tags eCat reliably). The confidence tier is the honesty mechanism.*

---

### VM-CHAN-1: eCat vs non-eCat Split (the Headline)

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: Comparative capture · **Internal Name**: channel_ecat_vs_noncat · **Customer-Facing Name**: Where Your Business Flows

**Client value**: The honest share of your business that actually flows through eCat vs everything else — in dollars, not vibes. · **SuperCat value**: The platform-ROI headline; proves where SuperCat already carries the business and the runway to grow that share.

**Decision & Dollar**: *"Here's the share of your business that actually flows through eCat (our truth) vs everything else — in dollars, not vibes."* Available for ~10–11 of 15 pilot clients; the rest are suppressed by the gate.

**Gating** (`Q-CHAN-05`): eCat % = confirmed eCat-SALE GMV (our `orders`) ÷ invoiced total (`Q-PROV-00`). **CORROBORATED → state the split, presented at STRONG** (Option A — never FULL; one-line caveat for gross-of-returns); PARTIAL (stale, e.g. `mhc`/`bmc`) → state but cap window + flag staleness; **SUPPRESS** when no real invoiced total (`uhc`/`da`/`fal`) or eCat > invoiced (`sc`, partial feed); LIMITED (`wag`, no comparable period) → single total "as provided," no %. Basis caveat: numerator is **ordered** value, denominator **invoiced** (0% join), so the % is an approximation the confidence tier carries.

**Example**: *"~85.6% of `sccon`'s invoiced business flows through eCat (STRONG, CORROBORATED); for `cci`, 11.4% (STRONG, CORROBORATED) — the rest reaches the ERP via channels we don't directly see."* *(`sc`: eCat ordered > invoiced → SUPPRESS, report the completeness gap — the FAL discipline.)*

**Complexity**: Moderate · **Data Dependency**: MCP `orders` (eCat-SALE) + `portal_invoices` · **Data Readiness**: Conditional (live for ~10–11/15) · **Query IDs**: Q-CHAN-00 (gate), Q-CHAN-05

**Allowed Claims**: eCat vs non-eCat share where the gate passes; absolute eCat dollars always. **Forbidden Claims**: a split on a suppressed/partial-feed org · >100% capture · attributing non-eCat to eCat. **Who pays**: CEO / CRO + SuperCat (the honest ROI story). *(Capture-dollar twin: [VM-C14](#vm-c14-ecat-capture--platform-footprint); supersedes VM-45.)*

---

### VM-CHAN-2: Non-eCat Sub-Channel Decomposition

**Audience**: Dual [D] — Conditional [C] · **Commerce Lens**: ERP total-business · **Internal Name**: channel_subchannel_decomp · **Customer-Facing Name**: Channel Mix Detail

**Client value**: Of the non-eCat dollars, where they actually go — online / EDI / rep / customer-direct / market. · **SuperCat value**: A fuller channel picture that frames eCat against its alternatives and the room to convert.

**Decision & Dollar**: *"Of the non-eCat dollars, here's the split — online / EDI / rep / customer-direct / market / returns."* Only ~3 of 15 clients can do this; `cci` is the model case where eCat reconciles to the `ECAT` origin tag.

**Gating** (`Q-CHAN-00` → `Q-CHAN-10`): `CHANNEL_CONFIDENCE ≠ NONE` (≥60% booked $ attributed, ≥2 origins, ≥25 rows) + a **maintained per-org `order_origin → channel` map**. NONE-tier (~30 orgs blank) → **suppress the sub-channel pie; present "eCat vs all other" (CHAN-1) only**. Over/under-tagged eCat (`ril` ~12×, `wwjc` ~0.25×) → **overlay eCat from `orders` truth, never read it from origin**. Magnitudes are booked → caption "channel mix from booked orders, applied to the invoiced total."

**Complexity**: Complex · **Data Dependency**: `portal_orders.order_origin` + per-org map + `orders` overlay · **Data Readiness**: Conditional (~3–4/15) · **Query IDs**: Q-CHAN-00, Q-CHAN-10

**Allowed Claims**: sub-channel mix % applied to the invoiced total, captioned as booked-grain, where the map is maintained. **Forbidden Claims**: a sub-channel pie for NONE-tier orgs · eCat magnitude read from `order_origin`. **Who pays**: CEO / CRO. *(This is C6 "Channel Economics" Level 2.)*

---

### VM-CHAN-3: Channel Cannibalization / Conflict

**Audience**: Internal [I] → Conditional [C] · **Commerce Lens**: Comparative capture · **Internal Name**: channel_cannibalization · **Customer-Facing Name**: Channel Conflict Analysis

**Client value**: When you turned on ecommerce, did you grow — or just move dealer orders to a cheaper-to-serve channel? · **SuperCat value**: A correlational channel-conflict read that supports the "grow, don't cannibalize" expansion story.

**Decision & Dollar**: *"When you turned on ecommerce, did you grow — or just move dealer orders to a cheaper-to-serve channel?"* The buyer-wishlist question (see [`commerce_buyer_wishlist.md`](../_archive/commerce_layer1_build/commerce_buyer_wishlist.md)).

**Gating**: requires CHAN-2-grade origin reliability **and** ≥2 comparable windows spanning the channel-launch date; otherwise suppress (most orgs). Correlational, never causal — a shift in channel mix is not proof of cannibalization.

**Complexity**: Complex · **Data Dependency**: `order_origin` time series + `orders` + invoiced trend · **Data Readiness**: Conditional (gated, few orgs) · **Query IDs**: Q-CHAN-20 (proposed)

**Allowed Claims**: pre/post channel-mix shift, labeled correlational. **Forbidden Claims**: a causal "ecommerce cannibalized dealers" verdict. **Who pays**: CEO / CRO.

---

## Domain 11 — Customer Economics (Layer 3, the K-series)

*The invoiced-truth customer layer, expressed as the per-customer pre-visit brief. Full map in [`provenance_map_customer.md`](provenance_map_customer.md). All customer grain is **billing-entity** (Spine §7.2 — no native parent key; `mapped_code` ~0%). The headline is the §15 Revenue-at-Risk / §16 competitive-loss banner. Segmentation (K5) is 🧊 **FROZEN** (Spine §8, owner directive 2026-06-29).*

> **Query-ID note:** the K-series is implemented in the **CI authority** `Customer Intelligence/authority/customer_query_library.md` (`G-00` gate + `CQ-01..CQ-26`), **not** `query_library_v2.md`. Inline `CQ-*` tokens below are indicative — confirmed live: `CQ-01` (account snapshot/value, invoiced-net re-anchored), `CQ-02` (category), `CQ-07/08` (frequency/seasonality, invoiced re-anchored), `CQ-09` (per-SKU reorder decay). **K2 (concentration), K4 (tenure), K6 (parent roll-up)** are composed/derived over `CQ-01`-grade invoiced data and are **pending a dedicated CQ** — reconcile exact IDs against the CI library before client use. K7/K8 are the customer-grain forms of `Q-ECON-LEAK` / Exception `S1`.

---

### VM-K-HEADLINE: Revenue-at-Risk / Competitive-Loss Banner (§15/§16)

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: revenue_at_risk_banner · **Customer-Facing Name**: Revenue-at-Risk Headline

**Client value**: One risk number, one provenance, at the top of the brief — what's at stake before the visit. · **SuperCat value**: The pre-visit hook that makes the brief indispensable to reps and CS; the report's lead.

**Decision & Dollar**: **one** risk number, **one** provenance, at the top of the brief — fed by exception **S1** (account-health $-at-risk) and **K7** (price-realization leakage, directional). The §16 competitive-loss banner fires when eCat is down while total business is up (S2).

**Gating**: consumes the Layer-1-gated `Q-ECON-*` outputs. **Suppressed entirely when the topline is PROVABLY-INCOMPLETE** — the operator caught `sc/1213728`'s booked **+58.8% "growth" = −52.4% invoiced decline** and suppressed the §15 headline. Confidence inherits **LEAST(input ceilings, `COMMERCE_CONFIDENCE`)**; S1 dollars dedupe against dormancy; K7 stays **directional** (human gut-check). Banner correctly **off** on a declining account (validated cci/CLIVE D).

**Signal**: §15 = S1 $-at-risk (counted once) + K7 leakage (directional); §16 = S2 competitive-displacement trigger. **Readiness**: Live (operator v5.1) · **Query IDs**: S1, Q-ECON-LEAK (K7), Q-CHAN-05 (S2). **Allowed**: a single suppressible risk number with its provenance. **Forbidden**: a §15 headline on a suppressed/incomplete topline · a hard $ on a directional (K7) figure. **Who pays**: rep / sales manager / CS (pre-visit).

---

### VM-K1: Customer Value Ranking

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: customer_value_ranking · **Customer-Facing**: Who Drives Your Revenue. **Client value**: Who actually drives your invoiced revenue, ranked at billing-entity grain. · **SuperCat value**: The foundational account view every customer conversation starts from. **Decision & Dollar**: *"Here's who actually drives your invoiced revenue — ranked, at billing-entity grain."* **Gating**: invoice feed; **STRONG** (FULL needs CORROBORATED); no feed → suppress $ ranking, offer order-activity ranking (intent, labeled). **Signal**: `SUM(net_amount)` by customer identity, LTM. **Readiness**: Live · **Query IDs**: CQ-01. **Allowed**: invoiced value ranking, billing-entity grain. **Forbidden**: a $ ranking on an order-only/intent feed framed as invoiced.

---

### VM-K2: Concentration & Single-Account Risk (customer grain)

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: customer_concentration · **Customer-Facing**: Account Concentration. **Client value**: How much of your book rides on the top-N accounts — and which one is quietly shrinking. · **SuperCat value**: A customer-grain risk metric that reframes a strong book against its fragility (retention narrative). **Decision & Dollar**: *"% of your book on the top-N accounts — and which top account is quietly shrinking."* **Gating**: billing-entity grain unless a parent roll-up is derived+gated (K6); STRONG. **Signal**: top-N share + HHI by customer identity (the customer-grain twin of [VM-C3](#vm-c3-revenue-concentration--single-account-risk-hhi)). **Readiness**: Live · **Query IDs**: CQ-02. **Allowed**: top-N share/HHI at billing-entity grain. **Forbidden**: family concentration without the "estimated family" label. *(eCat cousin: VM-13.)*

---

### VM-K3: Account Decline / Churn-Risk

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: account_decline · **Customer-Facing**: Quietly-Shrinking Accounts. **Client value**: Accounts quietly shrinking before they ever show up as churned. · **SuperCat value**: A relationship-level early warning that feeds the at-risk alarm — proactive-save value. **Decision & Dollar**: *"These accounts are quietly shrinking — before they show up as churned."* **Gating**: ≥2 periods of history; <2 → suppress trend, show current period only. **Signal**: equal-window invoiced decay by customer (the relationship view of [VM-C17 NRR$](#vm-c17-net-revenue-retention--based-all-channel)); the dollar-and-who-to-call alarm is [Exception S1 / VM-K8](#vm-s1-account-health--at-risk-the-quietly-dying-alarm). **Readiness**: Live · **Query IDs**: CQ-07/08. **Allowed**: account-level decline on ≥2 periods. **Forbidden**: a trend on <2 periods. *(eCat cousin: VM-17.)*

---

### VM-K4: New vs Reactivated vs Lapsed

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: book_composition_tenure · **Customer-Facing**: Book Composition by Tenure. **Client value**: How much of your book is new, reactivated, or lapsing — the composition behind the topline. · **SuperCat value**: Explains growth quality; a recurring conversation about where the book is heading. **Decision & Dollar**: *"How much of your book is new, reactivated, or lapsing — the composition behind the topline."* **Gating**: dated invoice feed; `sales_data`-only (no dates) → cannot compute tenure → suppress. **Signal**: classify each account by first/last invoice into new / reactivated / lapsed; $ + count by class. **Readiness**: Live (dated feed) · **Query IDs**: CQ-09. **Allowed**: tenure composition on a dated feed. **Forbidden**: tenure on a dateless source.

---

### VM-K5: Segment Composition of the Book — 🧊 FROZEN

**Audience**: Internal [I] · **Lens**: ERP total-business · **Internal Name**: segment_composition · **Customer-Facing**: N/A. **Status**: 🧊 **FROZEN** (Spine §8; owner directive 2026-06-29) — the final rung, deferred. Method preserved in [`segmentation_derivation.md`](segmentation_derivation.md) (first-party, emergent: product type × realized price point × behavioral customer type; no imposed labels; TAM `FIT_*`/`Segment_Opus_*` excluded as input, validation-only). **Do not advance, cluster, or ship segmentation until the owner unfreezes it.** `Q-SEG-DERIVE` is frozen in the library.

---

### VM-K6: Parent / Corporate-Family Roll-Up

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: parent_family_rollup · **Customer-Facing**: Estimated Family Exposure. **Client value**: Your true enterprise exposure once bill-to codes roll up to the corporate family. · **SuperCat value**: Surfaces hidden concentration and whitespace at the family level — a strategic-account lens. **Decision & Dollar**: *"Your true enterprise exposure once you roll bill-to codes up to the corporate family."* **Gating**: **PARTIAL (derived identity)** — no native parent key; always labeled **"estimated family"**; suppress where the name field is degenerate. **Signal**: derived parent map + `portal_invoices`. **Readiness**: Conditional (derived/gated) · **Query IDs**: CQ-parent. **Allowed**: an "estimated family" roll-up, labeled. **Forbidden**: presenting a derived family as a native/confirmed hierarchy.

---

### VM-K7: Price-Realization Leakage (customer grain)

**Audience**: Dual [D] (directional) · **Lens**: ERP total-business · **Internal Name**: customer_leakage · **Customer-Facing**: Same-Product Price Dispersion. **Client value**: Where the same product is sold cheaper to some accounts than others — the dispersion, in dollars. · **SuperCat value**: A directional discount-discipline conversation framed safely (dispersion, never "% off list"). **Decision & Dollar**: *"The same product is sold cheaper to some accounts than others — here's the dispersion, in dollars."* **Gating**: `leakage_dispersion_ok` (priced lines ≥60%, Spine §6.8); **dispersion, never "% off list"** (Spine §6.10); **stays directional** in client-facing surfaces with a mandatory human gut-check; suppress where the join < 60%. **Signal**: tier-aware `Q-ECON-LEAK` at customer grain (the customer-side of [VM-C2](#vm-c2-net-realization--discount-leakage)). **Readiness**: Live (directional) · **Query IDs**: Q-ECON-LEAK. **Allowed**: same-product dispersion $, directional. **Forbidden**: "% off list" · a hard recoverable-$ client claim without gut-check.

---

### VM-K8: Account-Health $-at-Risk

**Audience**: Dual [D] · **Lens**: ERP total-business · **Internal Name**: account_health_at_risk · **Customer-Facing**: At-Risk Accounts. **Client value**: Accounts quietly dying, flagged 90 days early, with the dollars at risk and who to call. · **SuperCat value**: The flagship pre-visit save — turns retention into a pushed, dollar-stamped action. **Decision & Dollar**: *"These accounts are quietly dying — flagged 90 days early, with the $ at risk and who to call."* **Gating**: **equal-length decay windows** (last 6mo vs prior 6mo) — unequal windows false-flagged WAYFAIR ($7.9M) as at-risk while it was *accelerating*; $ at risk = LTM revenue; suppressed at `COMMERCE_CONFIDENCE=NONE`, floored/labeled at PARTIAL. **Signal**: per-account equal-window decay anchored on `report_through_date`; pushed via the exception layer. **Readiness**: Live · **Query IDs**: S1. **Allowed**: $-at-risk + who-to-call on equal windows. **Forbidden**: unequal-window decay (false positives) · a hard CRITICAL on a PARTIAL feed. *(This is the live form of [Exception S1](#vm-s1-account-health--at-risk-the-quietly-dying-alarm).)*

---

### VM-K-HEALTH: Composite Account Health Score (confidence-capped)

**Audience**: Internal [I] · **Lens**: composite · **Internal Name**: customer_health_capped · **Customer-Facing**: N/A. **Note**: the v4 health score is **re-disciplined to inherit the lowest input's confidence** (cap or decompose) — it never surfaces externally (Forbidden Claims Register), and on a suppressed topline the economics inputs drop out rather than silently inflating the score. *(Org-level account health remains VM-27 / Health V2; this is the customer-grain cap rule.)*

---

## Domain 12 — Rep Outcome & Copilot (Layer 2, the R-series)

*The rep layer built on the Sales Rep Copilot, re-anchored on invoiced truth. Full design in [`rep_intelligence_layer2_build.md`](../build_notes/rep_intelligence_layer2_build.md); map in [`provenance_map_rep.md`](provenance_map_rep.md). **Governing principle: the rep layer is ERP-optional** — it always ships behavior (R1–R4); the ERP only decides whether outcomes (R5/R6) attach. The existing behavioral VMs (VM-01–06, VM-22, VM-43, VM-46) are the **behavior floor**; this domain adds the outcome ceiling, the identity gate, and the packaged copilot prompts.*

**Rep-identity tier gate (Spine §7.1; date-aligned recount 2026-06-29 — supersedes the census "~11" and the map §3.1 7-org table):** run first; it sets whether reps are named.

| Tier | Orgs (date-aligned bridge) | Rep reporting mode |
|---|---|---|
| **2 — named** (bridge ≥80%, **8**) | sarreid (100%), clc (100%), **mhc (100%, ⚠ DORMANT)**, cci (100%), wwjc (98.8%), pf (89.7%), ril (87.7%), **bcf (81.8%)** | Named rep→revenue allowed, capped by `COMMERCE_CONFIDENCE` |
| **1 — `rep_number`-only** (**9**) | gh (39%), scw (36%), sc (3.2%), clm, clli, bri, vic, shl, jyc | `rep_number` grain, **no names**; never invent a name from eCat authorship |
| **0 — no rep key** (**4**) | ufi, heb, kll, lpf | **Suppress rep→revenue**; behavior-only is the default design, not a degraded one |

> **Never** rank reps by revenue while silently dropping unmapped `rep_number`s — that fabricates a leaderboard (Spine §7.1). Suppress or label. **House accounts auto-flag + excluded** from the rep headline (on `cci` the raw #1 "rep" is `HOUSE ACCOUNT` $10.1M).

---

### VM-R1–R4: The Behavior Floor (always-on, ERP-optional)

**Audience**: Dual [D] · **Commerce Lens**: Non-commerce / eCat transaction · **Data Readiness**: Live (never dark). These four ship regardless of ERP; only the outcome enrichment is gated. Mixpanel-dependent VMs degrade to login/order effort under the **Mixpanel-coverage gate** (CORROBORATED 20/21 cohort orgs; only `mhc` is LOGINS-ONLY).

**Client value**: An always-on view of rep activity, coverage, asset engagement, and quote discipline — even when there's no ERP feed. · **SuperCat value**: The ERP-optional floor that lets the rep layer ship for every org; behavior is the durable base under the outcome ceiling.

- **VM-R1 Rep activity & cadence** — who's logging in, writing orders, going quiet (`login_events`, `orders`). **FULL** (owned). *(≈ VM-06 engagement trajectory.)*
- **VM-R2 Coverage / territory penetration** — how much of the assigned book each rep touches (`orders`, `org_users.territory_codes`/`customers`). Territory-format preflight; blank → touched-accounts only. *(≈ VM-43.)*
- **VM-R3 Catalog/asset engagement** — what reps present & share, feature depth (Mixpanel, `shared_resources`, `smart_stacks`). Mixpanel-gated. *(≈ VM-22 / VM-47 / VM-50.)*
- **VM-R4 Quote→submit discipline** — drafts that never become orders (`orders.order_type`/`is_submitted`; eCat-SALE filter separates quotes from sales). *(≈ VM-03 funnel gap.)*

> **Active-rep roster (Spine §7.3 / map §3.3):** reps = iPad-active seats (`org_users.last_ipad_login_at IS NOT NULL`) ∪ order authors — **not** raw `org_users` (which conflates B2B buyers, e.g. wwjc 20,740). **The standalone Mixpanel rep-engagement score stays demoted as vanity until fused to a dollar** — that fusion is Rung 4 ([VM-R-FUSION](#vm-r-fusion-coached-dollar-internal-only-tier-2)).

---

### VM-R5: Rep → Revenue Outcome

**Audience**: Dual [D] (identity-gated) · **Lens**: ERP total-business · **Internal Name**: rep_revenue_outcome · **Customer-Facing**: Rep Performance (Invoiced). **Client value**: Whose customers actually invoiced — and the realized price each rep is getting. · **SuperCat value**: Ties coaching to dollars, gated to protect against fabricated leaderboards (the credible rep outcome). **Decision & Dollar**: *"Whose customers actually invoiced — and the realized price each rep is getting."* **Gating**: invoiced re-anchor (swap booked `portal_orders.total_amount` → invoiced `net_amount`, the rep-side D1 fix); **3-tier identity gate** (Tier 2 → names; Tier 1 → `rep_number`; Tier 0 → behavior-only); house-account flag; capped at `COMMERCE_CONFIDENCE`; cohort grain only (re-keying). **Signal**: invoiced rep leaderboard (`Q-51`), name-bridged via `portal_orders.rep_name`, house-excluded. **Readiness**: Live (Tier-2 validated on cci) · **Query IDs**: Q-51, Q-16, Q-45. **Allowed**: invoiced per-rep $ at the tier-appropriate grain. **Forbidden**: a named leaderboard below Tier 2 · dropping unmapped reps · booked framed as invoiced · rep-revenue on Tier 0. **Owner gate**: client-facing rep naming signed off (Tier 2 only; **mhc held — dormant**).

---

### VM-R6: Book-of-Business Health by Rep

**Audience**: Dual [D] (identity-gated) · **Lens**: ERP total-business · **Internal Name**: rep_book_health · **Customer-Facing**: Rep Book Health. **Client value**: Concentration and decline inside each rep's own accounts — whose book is fragile. · **SuperCat value**: A management lens that routes risk to the right owner and deepens the rep layer. **Decision & Dollar**: *"Concentration and decline inside each rep's own accounts — whose book is fragile."* **Gating**: inherits R5's identity + completeness gates; customer grain = billing entity. **Signal**: per-rep concentration (HHI) + equal-window decline across the rep's covered accounts; rep-attributed revenue-at-risk = S1 rolled to the account's owning `rep_number` (Tier-0 → routes to sales management, no named owner). **Readiness**: Live · **Query IDs**: Q-51 + S1. **Allowed**: per-rep book concentration/decline at the tier grain. **Forbidden**: naming a rep below Tier 2 · attributing risk to a fabricated rep mapping.

---

### VM-R-PROMPTS: The Six Packaged Copilot Prompts

*The rep-facing copilot delivery shell (kept, not rewritten), each prompt now consuming the re-anchored data:*

| Prompt | Consumes |
|---|---|
| **"Prep me for [Customer]"** | invoiced trend + reorder cadence (header confidence label) |
| **"Who needs attention?"** | **rep-attributed revenue-at-risk (S1)** with $ + who-to-call, capped at `COMMERCE_CONFIDENCE` |
| **"What should I show?"** | inventory × sales (VM-37; catalog/inventory, unchanged) |
| **"Customers like X buying?"** | peer-category compare on invoiced value where the feed permits |
| **"Best new-account opps?"** | opportunity sizing by invoiced GMV |
| **"Who else nearby?"** | proximity prospecting; nearby account value → invoiced (booked labeled where invoices absent) |

**Readiness**: Live (Rung-3 applied; copilot surface retrofit + owner sign-off per `rep_intelligence_label_signoff.md`). **One-org-only signals stay out of cohort VMs** (map §3.4): `sales_quotas` (sarreid), `commitment_reports` (ufi), `placement_reports` (ufi/cci/clm) — org-scoped conditionals only.

---

### VM-R-FUSION: Coached-Dollar (internal-only, Tier-2)

**Audience**: Internal [I] · **Lens**: composite · **Internal Name**: rep_coached_dollar · **Customer-Facing**: N/A. **Status**: Rung 4 — **Option A ✅ APPROVED** (owner 2026-06-29), **⬜ NOT BUILT**, queued. **Internal-only, Tier-2-only (8 orgs), coaching-grade.** Juxtapose existing **C2 leakage-$ + S1 $-at-risk** with Mixpanel feature-depth/cadence **beside** them — **NO fused single number** — capped at `COMMERCE_CONFIDENCE`, framed "coaching hypothesis, not attribution," **never** "this rep cost you $X." See [`rung4_fusion_decision_brief.md`](../handoffs/rung4_fusion_decision_brief.md). **Forbidden**: a client-facing fusion · a fused per-rep dollar (Option B, deferred) · naming/fusing below Tier 2.

---

## Domain 13 — Exception Push ("answers, not dashboards")

*The delivery model that turns the economics/customer/rep VMs into **pushed, ranked, dollar-stamped alerts** — arguably the purest VMs. Full spec in [`selling_customer_exception_layer.md`](selling_customer_exception_layer.md). The buyer's ask: "Tell me 'these 12 accounts are at risk, worth $1.4M, here's who to call' and 'you leaked $340K in these three reps.' Push me the exceptions and the dollar impact. Don't make me go fishing."*

**The exception object** — every push is one row, never a chart:

| field | meaning |
|---|---|
| `type` | exception family (S1 account-health, C2 leakage-by-rep, …) |
| `severity` | CRITICAL / WARNING / INFO |
| `dollar_impact` | the single number that earns attention ($ at risk or $ leaked) |
| `subject` | the account/rep (name-resolved per identity gate) |
| `who_to_call` | the rep/owner to act |
| `one_line` | the pushed sentence |
| `evidence` | the 2–3 backing numbers |
| `confidence` | `LEAST(own ceiling, COMMERCE_CONFIDENCE)`: **NONE → suppress**, **PARTIAL → labeled floor (never a hard CRITICAL)**, STRONG → push. `FULL` unreachable for economics. |

**Ranking rule**: sort the daily push by `dollar_impact × severity_weight`, **cap ~12 items** (beyond that it reads as "everything is on fire"). Everything else stays queryable but unpushed.

---

### VM-S1: Account-Health $-at-Risk (the "Quietly-Dying" Alarm)

**Audience**: Dual [D] · **Commerce Lens**: ERP total-business · **Internal Name**: exc_account_health_at_risk · **Customer-Facing Name**: At-Risk Accounts Alert

**Client value**: The pushed alarm — "this $70K account is down 79%, call rep MKJ" — 90 days before a hard dormancy flag. · **SuperCat value**: The purest VM — an answer, not a dashboard; the retention engine that earns daily attention.

**Decision & Dollar**: *"HATCH P is down 79% over the last 6 months ($58K → $12K), $70K LTM at risk — call rep MKJ."* · *"JGASTON has gone 82 days silent, $69K LTM at risk — call rep ROBB."* Catches decline **90 days before** a hard dormancy flag because it watches the slope.

**Gating**: **equal-length windows** (last 6mo vs prior 6mo) — the unequal-window build false-flagged **WAYFAIR ($7.9M) as at-risk while it was accelerating**; precondition runs `Q-ECON-00` first → **NONE → suppress entirely**, **PARTIAL → $ is a labeled floor** ("at-risk ≥ $X (partial feed)"), never a hard CRITICAL; windows anchored on `report_through_date` so a stale feed measures decay against its own last real invoice. Name-resolve `subject` via `customers` (Tier-2 bridge for rep naming).

**Signal**: per-account equal-window decay OR silence past 2× normal order gap; `dollar_impact` = LTM revenue. **Readiness**: Live (validated cci) · **Query IDs**: S1. **Allowed**: $-at-risk + who-to-call on equal windows, confidence-stamped. **Forbidden**: unequal-window decay · a hard CRITICAL on PARTIAL · firing at NONE. **Who pays**: rep / sales manager / CS. *(Live form: [VM-K8](#vm-k8-account-health--at-risk); §15 headline input.)*

---

### VM-C2-rep: Leakage-by-Rep (the "Rogue Discounting" Alarm)

**Audience**: Internal [I] → Dual (signed off) · **Commerce Lens**: ERP total-business · **Internal Name**: exc_leakage_by_rep · **Customer-Facing Name**: Discount-Discipline Alert

**Client value**: The pushed alarm on the rep carrying the widest discretionary discount spread — worth a discipline conversation. · **SuperCat value**: Recoverable margin surfaced safely after guards + gut-check; a high-value internal-to-dual exception.

**Decision & Dollar**: *"Rep 12 carries the widest discretionary spread — ~$163K, 5.9% of their book, vs ~2% peers. Worth a discount-discipline conversation."*

**Gating**: tier-aware `Q-ECON-LEAK` (true median + tier guard + volume guard + `house_suspect` auto-exclude) — the naive build mis-flagged **rep 69 as a "$1.35M / 42% rogue"** (it was volume pricing; corrected to a normal 2.1%). Requires `leakage_dispersion_ok` (priced lines ≥60%); caps at `COMMERCE_CONFIDENCE` (suppress on PARTIAL/stale); rep naming requires **Tier 2** (else `rep_number`); **mandatory human gut-check before client delivery**; never "% off list." **Client-facing label APPROVED 2026-06-29** (`selling_customer_label_signoff.md`).

**Signal**: tier-aware dispersion rolled to `rep_number`; severity keys on leak-rate (leaked ÷ rep revenue). **Readiness**: Live (validated asi) · **Query IDs**: Q-ECON-LEAK. **Allowed**: leaked $ + leak-rate after the guards, tier-appropriate naming. **Forbidden**: "% off list" · a named rep below Tier 2 · skipping the gut-check. **Who pays**: VP Sales / CFO. *(Customer-grain form: [VM-K7](#vm-k7-price-realization-leakage-customer-grain); the leakage VM is [VM-C2](#vm-c2-net-realization--discount-leakage).)*

---

### VM-S/C-ROADMAP: Next Exception Types (designed / candidate)

| id | exception | source | status |
|---|---|---|---|
| **S2** | Competitive displacement (eCat down while total business up) | CI v4 §16 banner + Q-CHAN-05 | designed (CI-side §16) |
| **S3** | Stock-out on a top-15 item with live demand | VM-37 / Q-37 | designed |
| **C3** | Returns spike by SKU (dollar-based) | VM-C5 / Q-ECON-RETURNS | candidate |
| **C4** | Vanity-quoting org (quote→purchase < ~15%) | VM-C24 / Q-SELL-QC | candidate (org-level) |

> **Hard gaps that will NOT generate exceptions** (no data — do not fabricate): margin-at-risk, AR/credit-risk, damage-by-carrier, quoted-lead-time miss, market/showroom ROI. See [Register C — Hard-gap roadmap](#register-c--hard-gap-roadmap--never-viable-until-a-feed-lands).

---

## Prioritization Matrix — ⛔ SUPERSEDED → [Unified Stack Rank](#unified-stack-rank-v41)

> **Removed in v4.1.** The old Tier-1/2/2.5/Conditional/Deferred matrix that lived here was the stale half of the catalog: it ranked the **superseded VM-16 and VM-45 as "Tier 1 — Implement Now"** (VM-45 was even labeled "most important new commerce VM") and ran a numbering system that never reconciled with the money-map's `Rank N`. It is replaced wholesale by the single **[Unified Stack Rank](#unified-stack-rank-v41)** near the top of this document, which carries every VM's tier, Confidence Ceiling, and binding Gate on one scale, anchored on [VM-C1](#vm-c1-true-topline).
>
> The legacy "Why now / Data Source" notes that had value are preserved in the v4.0 snapshot ([`_archive/value_moment_catalog_v4.0_2026-06-29.md`](../_archive/value_moment_catalog_v4.0_2026-06-29.md)).

---

## Summary Statistics

> **v4.1 framing.** The catalog is now counted by its **[Unified Stack Rank](#unified-stack-rank-v41)** tier (one scale across all 13 domains), not the old "49 original + 9–13 families" split. Redirect stubs (VM-16, VM-45) and the three non-ranked registers (Cousins / Frozen / Hard-gap) are **not** counted as active ranked VMs. Every economics/rep/customer VM is governed by the `COMMERCE_CONFIDENCE` + `FEED_COMPLETENESS` through-line; `FULL` is unreachable for economics (STRONG ceiling).

**Ranked VMs by tier (the priority spine):**

| Tier | Count | Members |
|---|---|---|
| **S** (spine) | 2 | VM-C1, VM-C11 |
| **A** (headline) | 6 | VM-01, VM-03, VM-K8/S1, VM-C3, VM-C2, VM-C10 |
| **B** (strong) | 13 | VM-C7, VM-K-HEADLINE, VM-C4, VM-C5, VM-C9, VM-C2-rep, VM-CHAN-1/C14, VM-K1, VM-K3, VM-37, VM-C17, VM-C20, VM-R1–R4 |
| **C** (conditional/derivative) | ~34 | Domains 1/3/5/6/9/10/11/12 conditionals (see table) |
| **D** (internal/ops) | ~21 | Domains 2/7/8 + internal composites |

**Non-ranked registers (governance, not priority):**

| Register | Count | Members |
|---|---|---|
| **Demoted eCat-intent cousins** | 7 | VM-13, VM-14, VM-17, VM-18, VM-19, VM-20, VM-21 |
| **Redirect stubs** (not VMs) | 2 | VM-16 → VM-C1; VM-45 → VM-C14/VM-CHAN-1 |
| **🧊 Frozen** | 1 + class | VM-K5 + any imposed customer-type label |
| **⏳ Hard-gap** (feed-blocked) | 3 VMs + 5 feed gaps | VM-C19/C21/C25 + margin / AR-DSO / claims / lead-time / market-ROI |

**Structure & sourcing:**

| Metric | Count |
|--------|-------|
| Domains | **13** (8 original behavioral/eCat + 5 Intelligence-Stack: Commerce Econ, Channel, Customer Econ, Rep Outcome, Exception-Push) |
| Menu anchor | **VM-C1 True Topline** (the invoiced-net denominator) |
| Confidence ceiling — economics VMs | **STRONG** (FULL unreachable on a single invoice feed, Spine §6.8) |
| SuperCat-internal only | VM-27, VM-28, VM-29, VM-36, VM-48 + economics internal-leads (VM-C-POOL, VM-R-FUSION, VM-K-HEALTH) |
| Pending Engineering / cost-gated | VM-38b (`invoice_date` on `sales_data`) + VM-C19/C21/C25 (the landed `unit_cost` "one ask") |
| Data sources: MCP Postgres (owned) | behavior floor + eCat + invoiced economics |
| Data sources: BigQuery Mixpanel | CORROBORATED 20/21 cohort orgs (only `mhc` logins-only) |
| Data sources: BigQuery (HelpScout / Clicky / insightful_product / HubSpot) | internal + portal/demand |
| Data sources: Health V2 operator | VM-27, VM-29 |

---

## Appendix: Forbidden Claims Register

| Forbidden Claim | Why | Allowed Alternative |
|-----------------|-----|---------------------|
| "net-new customers" | Cannot confirm ERP lifecycle | "first-time eCat orderers" |
| "`portal_orders`" as buyer self-service | `portal_orders` = ERP-synced data, not buyer activity | "orders synced from your ERP" / "total business" |
| "buyer self-service" for anything other than B2B Cart | Sales Portal is internal BI | Only for `order_source = 'server'` with `has_cart = true` confirmed |
| "self-service portal" for Sales Portal | Sales Portal = internal BI | "Sales Intelligence Dashboard" / "Sales Portal" |
| "revenue at risk" for OOS items without caveating | Inventory is point-in-time | "historically high-volume items currently showing zero availability" |
| "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" in client-facing text | Internal segment labels | Use bundle names or describe what the client has |
| "full-stack deployment" | Invented label | Describe actual products ("eCat iPad, Online Ordering, and Sales Intelligence Dashboard") |
| eOL orders / channel mix for iPad-only clients | No eCat Online ordering channel exists | No eOL column; no channel mix section |
| CPQ/Kit Builder as "adoption gap" when client doesn't have the product | That's an "expansion opportunity" | "Enabling [Product Name] would allow..." |
| Health score from any formula other than Health V2 in VM-27 | Legacy formula conflicts with Health V2 | Health V2 outputs only |
| "Low eCat submit volume = low platform value" | Ignores enablement-without-submit-through pattern | Frame via VM-46 workflow maturity lens |
| Clicky Analytics mention when `has_clicky = false` | Clicky setup is a SuperCat-side action for these clients | Omit from client-facing report entirely |
| Total business = `SUM(portal_orders.total_amount)` (booked) | Booked ≠ shipped/billed; off 4×–9× (`bcf` 8.9× under, `cci` 25% over, `rw` $0) | Invoiced net via `Q-PROV-00`; booked only as labeled fallback (VM-C1) |
| "complete / total business" without `FEED_COMPLETENESS=CORROBORATED` | Circular validation — the Sales Portal reads the same feed; a partial export matches a partial dashboard | Attach "single-source; channel completeness unverified," present at **STRONG** (single-feed UNVERIFIED caps STRONG, not PARTIAL — Spine §6.3); **PARTIAL** only for PROVABLY-INCOMPLETE/STALE; suppress on PROVABLY-INCOMPLETE-as-DEAD/DEAD (D6) |
| "collected" / "revenue you've banked" | No AR/cash-receipt feed exists in schema | Always say "invoiced" |
| eCat capture as a **rate** when the gate fails | Partial feed → >100% (`sc` 126.9%); attribution dressed as capture | Absolute captured dollars only (VM-C14) |
| "% off list" / "unauthorized" for leakage | It's tier-aware dispersion, not authorized-price deviation; negotiated tiers ≠ leakage | "realized vs reference spread," directional, after the guards (VM-C2/K7) |
| Margin / net numbers without verified cost or returns | Missing/zero/stale cost turns margin into revenue; gross-only orgs fake 0% returns | Exclude items without landed cost (≥90% coverage); net-of-returns only when `RETURNS_IN_FEED=true` (VM-C19/C5) |
| Naming a rep below the Tier-2 identity bridge (≥80%) | Loose name guess mis-maps; silently dropping unmapped reps fabricates a leaderboard | `rep_number` grain (Tier 1) or behavior-only (Tier 0); never drop unmapped reps (VM-R5) |
| A fused per-rep "coached-dollar" or "this rep cost you $X" | Re-weaponizes a defused metric; internal-only, juxtapose-not-fuse (Option A) | "coaching hypothesis, not attribution," internal, Tier-2 (VM-R-FUSION) |
| Any segment label / fit score, externally | Segmentation is 🧊 FROZEN (Spine §8) | Omit; derived behavioral framing only when unfrozen (VM-K5) |
| Quote $ summed into sales | eCat carries Quote/Hold/WishList states (FAL $37.9M → $0.98M) | eCat-SALE filter on every numerator; label pipeline "pipeline," never "sales" (VM-C24) |

---

## Appendix: Demand-Side Honest-Gaps Roadmap → consolidated into [Register C](#register-c--hard-gap-roadmap--never-viable-until-a-feed-lands)

> **Consolidated in v4.1.** The feed-blocked CEO/CFO wishlist that used to live here (true net margin, AR/DSO, claims/damage-by-carrier, inventory/lead-time risk, market ROI) now lives in exactly one place — **[Register C — Hard-gap roadmap](#register-c--hard-gap-roadmap--never-viable-until-a-feed-lands)** — so hard gaps aren't catalogued twice. They remain **never-shippable VMs until the feed lands; do not fabricate them.**

**The meta-want the buyer would pay most for:** *a single reconciled source of truth across all selling channels* — which is exactly the commerce-bones mandate (Domain 9). The provenance discipline (`COMMERCE_CONFIDENCE` + `FEED_COMPLETENESS`) is how we deliver that honestly: a number ships with a confidence/provenance stamp or is suppressed.
