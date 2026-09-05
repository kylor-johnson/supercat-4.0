# Customer Intelligence — Changelog

## v5 — 2026-06-29 — Layer-3 re-anchor on the invoiced provenance spine

Source: `Insightful Product 4.0/intelligence_stack_roadmap.md` (Rung 2 — Layer 3) +
`selling_customer_NORTHSTAR_MVP_reconciliation_handoff.md` §5 (items 3, 4, 5, 6, 8). This is the
**"foundation, not rewrite"** move: the v4 brief shape/sections/prompts are unchanged; only the **numbers
underneath the Totals** moved from booked orders onto the invoiced spine, and each Total now carries a
provenance label inherited from Layer 1 (`provenance_spine.md`, **locked/read-only**).

### 1. Total business re-anchored on invoiced `net_amount` (D1 fix / reconciliation W1)
**Files**: `authority/customer_query_library.md`
- New **Provenance Anchor** section: canonical total = `SUM(portal_invoices.net_amount)` clamped to
  `report_through_date`; booked `portal_orders` demoted to a labeled fallback; per-query re-anchor table.
- **CQ-01** rewritten: invoiced net + booked fallback + window clamp + eCat-SALE filter; emits
  `total_business_source`, `total_business_ltm/prior`, `total_business_yoy_pct` (invoiced), `ecat_capture_pct_display`
  (capped ≤100%) + `ecat_capture_pct_raw` and `booked_over_invoiced` as completeness diagnostics. Legacy
  `total_gmv_*` (booked) names retired.
- **CQ-10** (trajectory) and **CQ-22** (wallet share, customer + cohort) rewritten to invoiced net; booked
  fallbacks retained and labeled.
- **CQ-07/CQ-08/CQ-23** re-anchor notes: cadence/tenure stay on booked orders; their dollar columns move to
  invoiced net (or are labeled "booked"). **CQ-12/CQ-14/CQ-21** stay on `portal_orders` for grain reasons
  (channel/buyer/ship-to) but their dollars are labeled "booked," never total business.

### 2. New provenance preflight gate G-00 + completeness labels (W2, W5)
**Files**: `authority/customer_gate_rules.md`, `authority/customer_brief_sections.md`
- **G-00 `TOTAL_BUSINESS_PROVENANCE`** (runs first): resolves `TOTAL_BUSINESS_SOURCE`, `COMMERCE_CONFIDENCE`,
  `FEED_COMPLETENESS`, `report_through_date` and the eCat-capture / booked-vs-invoiced triangulation — mirroring
  the Layer-1 `Q-PROV-00`/`Q-ECON-00` contract.
- Every Total prints source/confidence/completeness; **suppressed on `PROVABLY INCOMPLETE`/`DEAD`**; directional
  on `PARTIAL`/`STALE`; eCat capture **never headlined > 100%**. New third rendering mode: **Behavior-Only**.

### 3. Health Score re-disciplined to inherit lowest-input confidence (W3)
**Files**: `authority/health_score_spec.md`
- Composite capped at G-00 `COMMERCE_CONFIDENCE` (band form on PARTIAL; no numeric score on suppressed feeds);
  signals decomposed into invoiced-truth core / cadence / soft (eCat-only H4 no longer silently inflates the
  headline tier). H1 reads invoiced YoY; H4 reads capped eCat capture.
- **Rep Engagement Score** demoted out of the lead and never blended into health (W4); its dollar fusion is
  owner-gated (roadmap Rung 4) and explicitly not built here.

### 4. v4 §15/§16 wired to the gated Layer-1 outputs (FIX item 8)
**Files**: `09_v4_design.md`
- §15 Revenue-at-Risk/Opportunity consumes Spine-gated **S1** (account-health $-at-risk) and **Q-ECON-LEAK** (K7)
  directly, on invoiced revenue; one risk number, one provenance; inherits lowest confidence; suppressed when the
  Total is suppressed.
- §16 competitive-loss banner fires only on a reportable invoiced Total (both legs on invoiced YoY), with
  PARTIAL/STALE/ORDERS downgrades.

### Scope guard
Layers 1 and 2 (provenance spine, Domain-10 economics, exception layer, rep copilot) were treated as a
**locked, read-only foundation** — consumed, not modified. Owner-gated client-facing label flips
(`selling_customer_label_signoff.md`) and segmentation (🧊 frozen) were **not** touched. Per the roadmap, work
**stopped at Rung 2**.

---

## v4 — 2026-06-16

Source: [v3 Pilot Audit Report](runs/pilot_audit_report.md) (40 briefs, 20 audited)

### Phase 1 — Must-Fix (blocks production)

#### 1. Health Score Arithmetic Bug — FIXED
**Files**: `authority/health_score_spec.md`
**Audit finding**: wwjc/21762 scored 84/90 raw points but displayed 91 instead of the correct 93. Root cause: (a) possible off-by-one in denominator computation, (b) H6 signal used a "replacement order %" proxy instead of CQ-15 fill rate.

**Changes**:
- Added explicit worked example to normalization formula: `ROUND(100 × 84 / 90)` = 93, not 91
- Clarified that the denominator must be the sum of Max Points for *scored signals only* — skipped signals excluded from both numerator and denominator
- Specified that the competitive loss penalty applies AFTER normalization, not before
- Added H6 fallback rules: when CQ-15 cannot compute fill rate (or `FILL_RATE_POPULATION` gate fails), SKIP H6 entirely — no proxy metrics allowed

#### 2. Fill Rate 0% False Alarm — FIXED
**Files**: `authority/customer_gate_rules.md`, `authority/customer_brief_sections.md`
**Audit finding**: Three orgs (fsf, jyc, ril) showed 0% fill rate because `portal_order_items.quantity_invoiced` is never populated, not because fulfillment is failing.

**Changes**:
- Added new gate **G-10: `FILL_RATE_POPULATION`** — checks whether ≥50% of `portal_order_items` have non-zero `quantity_invoiced`
- When G-10 fails: §20 Fulfillment section is suppressed, health score signal H6 is skipped
- Added **G-11: `HAS_NEW_ITEMS`** (bonus fix) — suppresses §5 New Introduction Adoption when org has zero `new_item=true` products, preventing empty placeholder sections

#### 3. Ghost SKU vs. Stock-Out Disambiguation — FIXED
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: 7/12 scanned briefs had ghost SKUs (items with no catalog record) that appeared identically to real stock-outs — both showed `qty_available = 0` with no distinction.

**Changes**:
- §4 Top Items now requires two distinct alert types:
  - **STOCK OUT**: Item exists in catalog, qty_available = 0 → shows inventory details, receipt date, alternative SKUs
  - **GHOST SKU**: Item has no product record → explicitly states "no catalog record, cannot verify stock status"
- Detection rule: `p.long_description IS NULL` in CQ-03 LEFT JOIN indicates ghost SKU
- Ghost SKUs are grouped separately (after stock-outs) and do not show alternatives

---

### Phase 2 — Should-Fix (significant quality improvement)

#### 4. Next Best Product Volume Gate — RELAXED
**Files**: `authority/customer_gate_rules.md`, `authority/customer_brief_sections.md`, `authority/customer_query_library.md`
**Audit finding**: V-01 blocked CQ-06 at >10,000 LTM orders, making the highest-impact advanced insight unreachable for the pilot's most important accounts (Wayfair, Lamps Plus, NFM).

**Changes**:
- V-01 now uses a tiered approach:
  - ≤5,000 orders: full CQ-06 query
  - 5,001–50,000: CQ-06R recent-window variant (6-month invoice window)
  - >50,000: skip (ultra-high-volume warehouse accounts)
- Added CQ-06R variant to query library

#### 5. Cross-Sell Cohort Definition — IMPROVED
**Files**: `authority/customer_brief_sections.md`, `authority/customer_query_library.md`
**Audit finding**: State-level cohorts produced absurd comparisons when the target account dwarfs all peers (Wayfair at 474x MA average).

**Changes**:
- §18 now uses tiered cohort fallback: (1) same state + within 2x revenue, (2) same state any revenue, (3) org-wide within 2x revenue
- Added dominance guard: >10x cohort average triggers a disclaimer
- Query library CQ-19 updated with tier selection instructions and revenue filter variant

#### 6. Strategic Summary Expanded — 5-6 Talking Points
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: Briefs consistently produced 3 talking points where the Magnolia example had 6.

**Changes**:
- §23 split into Part A (Situation Assessment, 2-3 bullets) and Part B (Pre-Meeting Priorities, 5-6 numbered items)
- Priority sequencing defined: revenue-at-risk first, growth opportunities second, relationship items third
- Each item must reference a specific data point (SKU, dollar amount, date, %)

#### 7. Seasonality ASCII Bar Chart
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: Magnolia example uses ASCII bar charts for monthly revenue; v3 briefs used plain tables — less scannable.

**Changes**:
- §7 Buying Rhythm now specifies ASCII bar chart format for monthly seasonality
- Bar width proportional to revenue (max = 16 `█` chars)
- Peak months annotated, gap months flagged vs. prior year
- Fallback to plain table if <6 months of history

#### 8. Active Months Cap at 12
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: Several briefs showed "Active months: 13" due to LTM window spanning partial calendar months.

**Changes**:
- §7 frequency metrics: `active_months` display capped at 12
- When raw value exceeds 12, display "12" with note "All months active"

---

### Phase 3 — Nice-to-Have (polish)

#### 9. Sequential Section Numbering
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: Briefs jumped from §2 to §6 when §3-§5 were gated out, creating a "where are sections 3-5?" reaction.

**Changes**:
- Added rendering rule: sections are renumbered sequentially in the output (§1, §2, §3...) based on which sections actually render
- Spec file §-numbers remain as canonical IDs for internal reference

#### 10. Rep Name in Header
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: Briefs never included the assigned rep name, unlike the Magnolia example ("Prepared for: Sarah Mitchell").

**Changes**:
- §1 Header now includes territory → rep name lookup
- Rendered as: "Prepared for: [Rep Name] — Territory [code]"
- Graceful fallback if no rep found for territory

#### 11. Wallet Share Minimum Cohort Size
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: State cohorts with <5 customers (fsf MA = 3) are unreliable for comparison.

**Changes**:
- §9 Wallet Share: cohort_size < 5 triggers "indicative only" disclaimer
- cohort_size < 3 skips comparison entirely, shows customer revenue only

#### 12. Standardized "Uncategorized" Callout
**Files**: `authority/customer_brief_sections.md`
**Audit finding**: 11/12 scanned briefs had >25% uncategorized spend; format was inconsistent.

**Changes**:
- §3 Categories now uses tiered callout:
  - ≤15%: no callout
  - 16-50%: inline note about catalog enrichment
  - >50%: prominent top-of-section callout with specific recommendation
- >50% callout renders before the table, not after

---

### Phase 4 — Strategic (design only)

Design notes for future capabilities documented in `09_v4_design.md`:

- **§13 Multi-Account Customer Grouping**: Link related bill-to codes under a single vendor relationship (e.g., Wayfair CUS003640 + CUS010704)
- **§14 Anomaly-First Brief Reordering**: Compute surprise scores per section, promote highest-anomaly sections to top of brief
- **§15 Revenue at Risk / Opportunity Quantification**: Systematic computation of `revenue_at_risk` and `revenue_opportunity` headline stats
- **§16 Competitive Loss Signal as Primary Alert Banner**: Full-width banner when eCat declining while total business grows

---

*Changelog created 2026-06-16 | All changes traced to pilot audit findings*
