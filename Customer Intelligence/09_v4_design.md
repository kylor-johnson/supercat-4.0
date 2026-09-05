# Customer Intelligence — v4+ Strategic Design Notes

> **Status**: §13–§14 design-only; **§15–§16 re-anchored to the provenance spine (v5, 2026-06-29)** — they now
> consume the Layer-1 gated `Q-ECON-*` + exception **S1** outputs and the G-00 invoiced Total, rather than
> re-deriving from booked orders.
> **Date**: 2026-06-16 (v4 design) · 2026-06-29 (v5 provenance wiring)
> **Source**: Pilot audit recommendations §13–§16; provenance re-anchor per
> `Insightful Product 4.0/intelligence_stack_roadmap.md` (Layer 3) and
> `selling_customer_NORTHSTAR_MVP_reconciliation_handoff.md` §5 item 8.

These capabilities emerged from the v3 40-brief pilot audit as the next frontier. Each addresses a pattern observed across multiple briefs that the current architecture cannot handle. They are documented here for future implementation planning.

> **Provenance binding (v5).** §15 and §16 emit dollar claims, so they obey the Provenance Anchor
> (`authority/customer_query_library.md`) and G-00 (`authority/customer_gate_rules.md`): **one revenue-at-risk
> number, one provenance.** Risk/opportunity dollars are computed on the **invoiced** Total and are
> **suppressed when the Total is suppressed** (`FEED_COMPLETENESS ∈ {PROVABLY INCOMPLETE, DEAD}`) or shown as
> directional ranges on `PARTIAL`/`STALE`. The composite risk number inherits the **lowest** `COMMERCE_CONFIDENCE`
> of its inputs (Spine §5.3). Layer 1 (`Q-ECON-*`, S1/C2) is locked/read-only — §15/§16 *consume* it.

---

## 13. Multi-Account Customer Grouping

### Problem

Major buyers often have multiple bill-to codes — either across orgs within SuperCat (e.g., a retailer buying from two different manufacturers) or within a single org (e.g., Wayfair with CUS003640 + CUS010704 at MHC, or Sunstar Properties at scw/1103467 + gh/1103467).

The v3 pilot produced two separate briefs for MHC's Wayfair accounts. The companion brief (CUS010704) correctly cross-referenced CUS003640, but only because the brief generator noticed the timing correlation manually. A $6.99M combined relationship was fragmented into two separate intelligence views.

### Design Direction

**Customer Group entity**: A lightweight grouping that links related bill-to codes under a single "vendor relationship" umbrella.

**Data model options**:
- **Option A — Admin-defined groups**: A new `customer_groups` table where the client admin manually links related codes. Pros: precise, client-controlled. Cons: requires Admin Console UI work, adoption friction.
- **Option B — Heuristic auto-grouping**: Match on `customer_name` fuzzy similarity + same billing address. Pros: zero setup. Cons: false positives (chains with different buyers at each location aren't really "one relationship").
- **Option C — Hybrid**: Auto-detect candidates, present for admin confirmation. Best of both worlds but most complex.

**Brief impact**: When a customer belongs to a group, the brief header shows: *"Part of [Group Name] — [N] accounts, $[combined] combined LTM"*. Key metrics (total GMV, wallet share, health score) would have both individual and group-level views. The Strategic Summary would reference the group context when making recommendations.

**Prerequisite**: Customer matching logic. The v3 audit showed MHC's two Wayfair accounts were identifiable by name + timing correlation, but there's no general-purpose matching today.

**Estimated complexity**: Medium-High. Requires either new DB schema or a matching heuristic, plus changes to the brief rendering pipeline to aggregate across codes.

---

## 14. Anomaly-First Brief Reordering

### Problem

The current brief follows a fixed section order (§1 Header → §2 Snapshot → §3 Categories → ... → §23 Summary). This works well for comprehensive review, but the best briefs in the v3 pilot all had one section that was dramatically more important than the rest:

- mhc/CUS003640: The 176-day silence on a $4.68M account is THE story — it belongs at the top, not buried in the rhythm section.
- sc/1213728: Three rep handoffs in 6 months is the defining fact about this account.
- ufi/2747: 55.2% fill rate (31 pts below org) explains everything else in the brief.

A rep scanning a 200-line brief may not reach the critical finding if it's in §16 or §20.

### Design Direction

**Surprise score per section**: After computing all sections, assign each a "surprise score" based on how far its key metric deviates from expected/normal:

| Signal | Surprise Computation |
|--------|---------------------|
| Days since last order | `days_since / avg_days_between` — high ratio = surprising silence |
| Fill rate | `ABS(customer_fill_rate - org_fill_rate)` — large gap = surprising |
| YoY revenue change | `ABS(yoy_pct)` — large swing in either direction |
| Reorder decay | `MAX(latest_interval / avg_interval)` across items |
| Rep handoff | Count of distinct reps in 6 months > 1 |
| Category collapse | Any category with YoY < -50% |
| Competitive loss | eCat declining while total business grows |

**Reorder trigger**: If any section's surprise score exceeds a threshold (e.g., 2 standard deviations from the org norm), promote that section to render immediately after §2 (Account at a Glance), with a banner: *"⚠ ALERT: [one-line summary of the anomaly]"*

**Constraints**:
- Maximum 2 promoted sections (beyond that, the brief is just "everything is on fire").
- §1 Header and §23 Summary always stay in their positions.
- Promoted sections still appear in their canonical position as well (with a back-reference: *"See alert above"*) — this preserves the comprehensive review flow for readers who want it.

**Estimated complexity**: Medium. Requires a post-processing step after all sections are computed. No new queries — just a scoring/reordering pass on existing output.

---

## 15. Revenue at Risk / Opportunity Quantification

### Problem

The Magnolia example quantifies opportunity: *"$116K addressable growth."* The v3 pilot occasionally does this (ufi/2747: *"$1.7M in additional invoiced revenue from existing demand"*) but it's ad hoc, not systematic.

A rep needs two numbers going into every meeting: "How much am I at risk of losing?" and "How much could I gain?"

### Design Direction

**Revenue at Risk** (computed from rendered sections — all dollars on the **invoiced** spine):

| Risk Source | Computation | Briefs Where It Appeared |
|-------------|-------------|--------------------------|
| Reorder decay | Sum of LTM **invoiced** revenue for items with DECAY_DETECTED status | clm/463, ufi/8682, sc/1213728 |
| Stock-out on top items | Sum of LTM **invoiced** revenue for top-15 items with qty_available=0 | All 20 briefs |
| Competitive loss signal | `ecat_gmv_prior × (total_business_yoy_pct - ecat_yoy_pct) / 100` — YoY on **invoiced** Total (CQ-01 canonical) | sc/1213728, mhc/CUS003640 |
| Fulfillment impact | Sum of `item_ltm_revenue × (1 - 1/slowdown_multiplier)` for backordered items | ufi/2747 |
| Dormancy risk | **Invoiced** LTM revenue if days_since_last_order > 2× avg_days_between (recency vs `report_through_date`) | mhc/CUS003640 |
| **Account-health $-at-risk (S1)** | Consume the Layer-1 exception **S1** object directly (Spine-gated, provenance-capped) — do not re-derive | (new) |
| **Price leakage (K7 / Q-ECON-LEAK)** | Consume the Layer-1 tier-aware dispersion leakage at customer grain (capped, house-account-excluded) — **directional until owner sign-off** | (new) |

Formula: `revenue_at_risk = SUM(all applicable risk sources)` — deduplicate items that appear in multiple risk
categories. **Provenance:** the headline number inherits the **lowest** `COMMERCE_CONFIDENCE` among contributing
sources and is **suppressed** when the Total is suppressed (G-00 `PROVABLY INCOMPLETE`/`DEAD`); on `PARTIAL`/`STALE`
present a range labeled "floor." S1 and leakage arrive **already gated** from Layer 1 — pass their confidence
through, never upgrade it.

**Revenue Opportunity** (computed from rendered sections):

| Opportunity Source | Computation |
|--------------------|-------------|
| Cross-sell gaps | Sum of category gaps from §18 |
| Wallet share whitespace | `cohort_avg - customer_revenue` if customer < cohort_avg |
| Uncommitted market items | Sum of committed-but-not-ordered item values from §10 |
| Lifecycle growth curve | `addressable_growth` from CQ-23 |

Formula: `revenue_opportunity = MAX(cross_sell_gap, wallet_share_gap)` — take the larger of the two (they overlap conceptually). Add uncommitted market items separately.

**Rendering**: Two headline stats at the top of §23 Strategic Summary, each carrying one provenance label:
```
Revenue at Risk: $47K  |  Revenue Opportunity: $116K
(invoiced through 2026-05-31 · UNVERIFIED — SINGLE FEED · STRONG)
```
On a suppressed Total: `Revenue at Risk: suppressed — invoice feed provably incomplete (eCat capture 126% of invoiced).`

**Estimated complexity**: Low-Medium. All inputs already exist in rendered sections (now on the invoiced spine)
plus the Layer-1 S1 / Q-ECON-LEAK objects. This is a **gated synthesis** computation, not new data — its only
new dependency is reading the already-capped Layer-1 outputs and inheriting their confidence.

---

## 16. Competitive Loss Signal as Primary Alert Banner

### Problem

When eCat orders decline while total business grows, it means the customer is shifting spend to a competitor (or alternative channel). This is the single most important signal in the entire Customer Intelligence system — it's the "your customer is leaving you" alarm.

Currently, this signal appears as:
1. A callout in §2 (Account at a Glance)
2. A -5 point health score penalty in §22
3. A mention in §23 (Strategic Summary)

This is too subtle. In the v3 pilot, sc/1213728 had this signal, and it was the most important finding in the entire brief — but you had to read through 6 sections before encountering it.

### Design Direction

**Top-of-brief banner**: When the competitive loss signal fires (`ecat_yoy_pct < 0` AND `total_business_yoy_pct > 0`, both on the **invoiced** canonical Total from CQ-01), insert a full-width banner immediately after §1 Header, before any other content:

```
┌─────────────────────────────────────────────────────────┐
│  ⚠ COMPETITIVE DISPLACEMENT DETECTED                    │
│                                                         │
│  eCat capture: -15.2% ($72K → $61K)                     │
│  Total business (invoiced): +8.3% ($442K → $479K)       │
│  Revenue shifting away: ~$29K                           │
│  Provenance: invoiced through 2026-05-31 · STRONG       │
│                                                         │
│  This customer is buying MORE overall but LESS from     │
│  your eCat channel. The gap is going elsewhere.         │
└─────────────────────────────────────────────────────────┘
```

**Provenance gate (v5)**: This banner makes a "total business grew" claim, so it **only fires when the invoiced
Total is reportable** — `TOTAL_BUSINESS_SOURCE = INVOICES` AND `FEED_COMPLETENESS ∉ {PROVABLY INCOMPLETE, DEAD}`.
On a provably-incomplete/dead feed the "total business +Y%" claim is unprovable (the gap may simply be the
unfed channels), so **suppress the banner** and fall back to the §2 capture-only note. On `PARTIAL`/`STALE`,
fire the banner with directional language ("invoiced total appears to be growing") and the completeness caveat.
On `ORDERS` (booked, no invoices), label both legs "booked" and downgrade to the §16 *Info* tier (it is a
booked-vs-eCat divergence, not a confirmed invoiced one).

**Severity tiers**:

| Tier | Condition | Banner Color/Treatment |
|------|-----------|----------------------|
| Critical | eCat YoY < -25% AND total business YoY > +10% | Red banner, "URGENT" prefix |
| Warning | eCat YoY < 0% AND total business YoY > 0% | Amber banner, "WATCH" prefix |
| Info | eCat flat AND total business growing >15% | Gray note, "MONITOR" prefix |

**Interaction with other signals**: The competitive loss banner should cross-reference:
- Channel mix (§8): Is the revenue shifting to a specific channel?
- Category evolution (§21): Which categories are declining in eCat but growing in total?
- Rep engagement (§12): Has rep engagement declined simultaneously?

**Estimated complexity**: Low. All data is already in CQ-01. This is a rendering/layout change with a conditional banner template.

---

*Design notes created 2026-06-16 | Source: Customer Intelligence v3 Pilot Audit §13–§16*
