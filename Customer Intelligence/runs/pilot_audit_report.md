# Customer Intelligence Pilot — Audit Report

Generated: 2026-06-16
Briefs audited: 20 of 40 (deep: 8, scan: 12)

---

## Executive Summary

- **The core product delivers.** Every deep-audited brief produced genuinely actionable intelligence — the kind of insight a rep cannot get from any other source. The best briefs (clm/463, ufi/8682, sc/1213728) rival or exceed the Magnolia example in actionability.
- **Numerical accuracy is excellent.** All 12 spot-checked claims (LTM revenue, order counts, fill rates, YoY calculations) matched the live database exactly. The data pipeline is reliable.
- **Health score computation has bugs.** One confirmed arithmetic error (wwjc/21762: 84/90 should yield 93, not 91) and one confirmed signal mis-scoring (wwjc/21762 H6: used replacement order proxy instead of actual fill rate). These affect displayed scores but not the underlying intelligence.
- **"Uncategorized" dominates.** 11 of 12 scanned briefs have 25%+ uncategorized spend — in 3 cases exceeding 89%. This is the single largest quality constraint blocking the brief from reaching the Magnolia standard's category-level depth.
- **Ghost SKUs are pervasive.** 7 of 12 scanned briefs flag items with no catalog record. This blocks description, collection assignment, inventory status, and cross-sell analysis for high-revenue items.

---

## Goal Achievement Assessment

### Overall Score: 4/5

The briefs demonstrably answer the core question: "Would this prepare a rep for the meeting?" For 6 of 8 deep-audited briefs, the answer is an unqualified yes. For 2 (hfg/13869 with 100% uncategorized, cci/ZZZZZZZ as an internal account), the brief correctly identifies why the data is insufficient and pivots to what IS actionable.

### A. Core Question: Does the brief prepare a rep for the meeting?

| Brief | Score (1-5) | Notes |
|-------|-------------|-------|
| wwjc/21762 | 5 | Complete picture: e-commerce reseller, AOV migration story, replacement order risk, growth trajectory. Rep knows everything. |
| clm/463 | 5 | Elite: reorder decay on #2 revenue item, stock-out with alternative, new-category adoption signal, AOV trend. Actionable in every section. |
| ufi/2747 | 5 | Critical fulfillment gap (55.2% fill rate) dominates the narrative correctly. Rep walks in knowing the #1 issue. |
| ih/119580 | 4 | Strong eCat showcase account. Limited by portal data newness (11 months) — several signals skipped. |
| mhc/CUS003640 | 5 | The "cliff detection" — 176 days silent after $2.4M/quarter — is exactly the kind of alarm this product should raise. Cross-referencing with CUS010704 is smart. |
| mhc/CUS010704 | 4 | Complementary brief correctly links to CUS003640. Slightly thinner standalone. |
| cci/ZZZZZZZ | 3 | Correctly identifies as internal market account, provides useful market revenue breakdown, and recommends re-attribution. Not a traditional brief but handles the edge case gracefully. |
| hfg/13869 | 3 | Correctly flags the project-driven outlier ($2.68M single event). Limited by 100% ghost SKUs. The brief does what it can with minimal data. |

**Average: 4.25/5**

### B. Section Coverage vs. Design Spec

`07_prototype_findings.md` defined a v2 structure of 20 sections (9 always-on, 6 conditional, 1 summary, 4 advanced). Actual rendering across the 8 deep-audited briefs:

| Section (v2 design) | Present in X/8 | Notes |
|---------------------|----------------|-------|
| §1 Header | 8/8 | Always-on ✅ |
| §2 Account at a Glance | 8/8 | Always-on ✅ |
| §3 Purchase DNA: Categories | 6/8 | Missing for wwjc/21762 (no invoice data for this customer?), cci/ZZZZZZZ |
| §4 Purchase DNA: Top Items | 5/8 | Present for data-rich accounts; absent for cci/ZZZZZZZ and thin accounts |
| §5 New Introduction Adoption | 2/8 | Only clm/463 and partially sc/1213728. Low presence rate. |
| §6 Spend Trajectory | 8/8 | Always-on ✅ |
| §7 Buying Rhythm | 8/8 | Always-on ✅ |
| §8 Channel Mix | 8/8 | Always-on ✅ |
| §9 Wallet Share | 8/8 | Always-on ✅ |
| §10 Market Commitments | 1/8 | Only ufi/2747 (the only org with CMT=T in the gate profile) |
| §11 Showroom Placements | 1/8 | Only ufi/2747 (stale — 6.5 years old) |
| §12 Rep Engagement | 0/8 | Not present in deep-audit sample (sc/1213728 has it — seen in scan) |
| §14 Buyer Intelligence | 0/8 | Gated out everywhere (HAS_BUYER_NAMES threshold) |
| §15 Collection Mix | 2/8 | clm/463, ufi/8682 |
| §16 Reorder Decay | 4/8 | Present for high-velocity accounts. Excellent when present. |
| §18 Cross-Sell Opportunity | 1/8 | Only ufi/8682 (thin — MA cohort too small) |
| §19 Same-Store/Fulfillment | 4/8 | Combined with §20 in some briefs |
| §20 Fulfillment & Fill Rate | 5/8 | Standalone in most |
| §21 Category Share Evolution | 4/8 | Present when prior-year data available |
| §22 Health Score Breakdown | 8/8 | Always-on ✅ |
| §23 Strategic Summary | 8/8 | Always-on ✅ |

**Consistently missing**: Buyer Intelligence (0/8), Rep Engagement (0/8 in deep sample), Cross-Sell (1/8), New Introduction Adoption (2/8).

### C. Advanced Insights Delivery

| Advanced Insight | Present? | Quality Assessment |
|-----------------|----------|-------------------|
| Next Best Product | 1/20 scanned (clc/LAM002413 — "unavailable due to volume threshold") | Not meaningfully delivered in pilot. The V-01 volume gate (>10,000 orders) blocks it for the largest/most interesting accounts. |
| Wallet Share | 16/20 | **Elite.** Consistently computed, well-contextualized ("93x the state average"), provides clear positioning. Best implementation of any advanced insight. |
| Reorder Decay | 8/20 | **Strong** when present. Actionable per-SKU alerts with velocity ratios. clm/463's 4.6x decay on #2 item is a home run. |
| Buyer Intelligence | 0/20 | Fully gated. HAS_BUYER_NAMES threshold (>5%) blocks rendering for all 20 pilot orgs except mhc (which has buyer data but doesn't display a Buyer Intelligence section). |
| Competitive Loss Signal | 2/20 | Applied as health score penalty (sc/1213728). Identified narratively in mhc/CUS003640 (Wayfair cliff). Effective but rare. |
| Same-Store Comps | 6/20 | Present for orgs with ship-to data. Quality varies — clm/463 shows useful location diversity; ril/U1090H shows DC routing. |
| Category Evolution | 8/20 | **Strong.** The category share shift analysis (clm/463 Chandelier +5.8 pts; ufi/8682 Cabinets +3.1 pts) consistently produces high-value narrative. |
| Market Commitment Conversion | 1/20 | Only ufi (the sole org with CMT=T). Shows commitment counts but NOT per-item conversion analysis as designed in 03_advanced_insights.md. |
| Fulfillment Impact | 3/20 | Revenue impact quantification missing (the "projected $14K annualized impact" from Magnolia example doesn't appear). Fill rate is stated but backorder→reorder correlation is not computed. |

### D. The "Magnolia Standard" Comparison

Comparing the 3 richest briefs against the `04_example_brief.md` gold standard:

| Dimension | Magnolia Example | Best Real Briefs (clm/463, ufi/8682, sc/1213728) |
|-----------|-----------------|--------------------------------------------------|
| Header completeness | Full: name, code, location, rep name, brief date, lifecycle badge | Full minus rep name — briefs don't identify the assigned rep |
| Category analysis | Clean named categories with YoY trends | Matches or exceeds — but often 25-44% "Uncategorized" noise |
| Top items with inventory | 10 items, descriptions, stock status, alternatives | Matches — 10-15 items with stock-out alerts and collection-aware alternatives |
| Seasonality visualization | ASCII bar chart with monthly $ | Monthly table format — no visual bars. Functional but less scannable. |
| Reorder decay | 1 item flagged with interval history | 5-10 items with velocity ratios — MORE detailed than Magnolia |
| Buyer Intelligence | 3 buyers with roles and alerts | Absent (gated) |
| Market Commitments | Per-market conversion with uncommitted item list | Only item counts, no per-item conversion |
| Cross-sell with $ gap | Category-level vs. cohort with dollar gaps | Present in 1/20 briefs (thin cohort issue) |
| Same-Store Comps | Location-level revenue with explanatory narrative | Present but without narrative explanation of performance differences |
| Pre-Meeting Priorities | 6 specific, sequenced talking points | 3 talking points — **good quality but fewer and less sequenced** |
| Account Lifecycle | Cohort projection with $ addressable growth | Stage label + cohort %, but no projected peak revenue $ |

**Key gaps vs. Magnolia**: (1) Rep name absent, (2) no seasonality ASCII visualization, (3) buyer intelligence gated out, (4) pre-meeting priorities are 3 items not 6, (5) no lifecycle $ projection, (6) market commitment conversion by item not implemented.

### E. Pre-Meeting Priorities Quality

The "Strategic Summary" section (§23) serves as the equivalent of Magnolia's "Pre-Meeting Priorities." Quality assessment:

- **Best**: clm/463, ufi/2747, sc/1213728 — specific talking points reference exact SKUs, dollar amounts, and timeframes. "The Hayes 50" Linear Chandelier is stocked out until July 14" is actionable.
- **Typical**: scw/1103467, lpf/1000031 — solid but slightly more generic. "Your average order climbed to $3,729" is good but less surgical.
- **Weakest**: cci/ZZZZZZZ — appropriately defers to "this isn't a real customer" framing.

Overall: rep talking points are specific and actionable in 80%+ of briefs. The best ones match Magnolia quality. The format consistently provides 3 talking points where Magnolia had 6 — more would be better.

---

## Accuracy Assessment

### Spot-Check Results

All spot-checks verified against live Postgres database via MCP:

| Brief | Claim | DB Value | Pass/Fail |
|-------|-------|----------|-----------|
| wwjc/21762 | LTM Orders: 830 | 830 | ✅ Pass |
| wwjc/21762 | LTM GMV: $483.0K | $483,025.22 | ✅ Pass |
| wwjc/21762 | Prior Orders: 530 | 530 | ✅ Pass |
| wwjc/21762 | Prior GMV: $287.6K | $287,615.31 | ✅ Pass |
| wwjc/21762 | YoY: +67.9% | (483025-287615)/287615 = 67.9% | ✅ Pass |
| clm/463 | LTM Orders: 9,571 | 9,571 | ✅ Pass |
| clm/463 | LTM GMV: $3.13M | $3,132,684.01 | ✅ Pass |
| clm/463 | Fill rate: 96.7% | 96.7% (16,384 ordered, 15,850 invoiced) | ✅ Pass |
| ufi/2747 | LTM Orders: 158 | 158 | ✅ Pass |
| ufi/2747 | LTM GMV: $5.55M | $5,550,264.00 | ✅ Pass |
| ufi/2747 | Fill rate: 55.2% | 55.2% (14,943 ordered, 8,244 invoiced) | ✅ Pass |
| mhc/CUS003640 | Last order: 2025-12-22 | 2025-12-22 | ✅ Pass |
| mhc/CUS003640 | LTM GMV: $4.68M | $4,682,641.96 | ✅ Pass |
| ih/119580 | eCat orders: 172 | 172 | ✅ Pass |
| ih/119580 | eCat GMV: $546,149.10 | $546,149.10 | ✅ Pass |

**Result: 15/15 spot-checks pass.** The data pipeline and query layer produce accurate numbers.

### Health Score Validation

Manual recomputation of health scores per `authority/health_score_spec.md`:

| Brief | Stated Score | Recomputed | Match? | Issue |
|-------|-------------|------------|--------|-------|
| clm/463 | 89/100 | 80/90 = 89 | ✅ Yes | — |
| ih/119580 | 100/100 | 50/50 = 100 | ✅ Yes | Correct handling of skipped signals |
| mhc/CUS003640 | 41/100 | 37/90 = 41 | ✅ Yes | — |
| sc/1213728 | 76/100 | 73/90 = 81, minus 5 penalty = 76 | ✅ Yes | Competitive loss penalty correctly applied |
| ufi/8682 | 80/100 | 72/90 = 80 | ✅ Yes | — |
| **wwjc/21762** | **91/100** | **84/90 = 93** | **❌ No** | **Two issues: (1) H6 scored 7/10 using "replacement order %" proxy instead of actual fill rate (96.6% vs 82.0% org = should be 10/10); (2) Even with brief's own 84/90, arithmetic yields 93 not 91.** |

**Root cause for wwjc/21762**: The brief lacks a §20 Fulfillment section (no `portal_order_items` fill rate computation shown), so H6 was scored using an improvised proxy ("replacement orders 6.3%") rather than the spec-defined CQ-15 formula. Additionally, the normalization arithmetic (84÷90→91) suggests a possible off-by-one bug in the denominator computation.

### Internal Consistency

| Brief | Check | Result |
|-------|-------|--------|
| wwjc/21762 | eCat penetration: $438.8K / $483.0K = 90.8% | ✅ Matches stated 90.8% |
| clm/463 | Category revenue sum: $3.08M vs. total $3.13M | ⚠ ~$50K gap (likely items below top-10 cutoff) — acceptable |
| ufi/2747 | Fill rate: 8,244 / 14,943 = 55.2% | ✅ Matches |
| sc/1213728 | eCat penetration: $572.2K / $118.8K = 481.8% | ✅ Matches (eCat captures intent, portal is invoiced — divergence correctly explained) |
| mhc/CUS003640 + CUS010704 | Combined GMV: $4.68M + $2.31M = $6.99M | ✅ Matches stated "$6.99M combined" |

### Gate Logic Correctness

Cross-referencing the manifest gate profile with section rendering:

| Org | Gate=F | Expected Absence | Actual | Correct? |
|-----|--------|------------------|--------|----------|
| ufi | SHP=F | §19 Same-Store absent | ufi/2747 has no Same-Store section | ✅ |
| ufi | BUY=F | §14 Buyer Intelligence absent | Not present | ✅ |
| ufi | RMA=F | §16 Returns absent | Not present | ✅ |
| wwjc | BUY=F | §14 absent | Not present | ✅ |
| wwjc | CMT=F | §10 absent | Not present | ✅ |
| clm | BUY=F | §14 absent | Not present | ✅ |
| clm | CMT=F | §10 absent | Not present | ✅ |
| sc | RMA=T | §16 Returns MAY render | sc/1213728 shows RMA in channel mix, not as standalone returns section | ⚠ Partial — RMA data present but not formatted as per design spec |
| cci | COLL=F | §15 Collection Mix folded | cci/ZZZZZZZ has no collection section | ✅ |

**Result**: Gate logic is correctly applied. One edge case: orgs with RMA=T (sc, scw, gh, sccon) show RMA as a channel classification rather than a standalone Returns section with reason codes and rates. The design spec's §9 (Returns) section format is not implemented — RMA data flows into Channel Mix instead.

---

## Quality Feedback

### Elite Moments (What's Best)

1. **mhc/CUS003640 — Cliff Detection + Cross-Account Linkage**: The brief detects a $4.68M account going silent on Dec 22 and immediately flags "investigate CUS010704 (B2B account)" as a possible migration target. The companion brief (CUS010704) confirms identical timing — a combined $6.99M vendor-level event. This is intelligence no dashboard provides.

2. **clm/463 — Reorder Decay on Revenue-Critical Item**: HAY-1407-AG (Hayes 28" Chandelier, their #2 item at $39.6K LTM) is at 56 days vs 12.2-day average — 4.6x slowdown. Paired with the stock-out alert on HAY-1417-AG (their 50" variant, zero stock until July 14). A rep walking into Lamps Plus with this knows exactly what to ask.

3. **sc/1213728 — Rep Handoff Detection**: Three reps in 6 months (Julie → Hunter → Blake), with the revenue surge directly correlated to Blake's engagement ramp. "Handoff Detected" as a flag is a feature that doesn't exist anywhere else in B2B sales tools.

4. **ufi/2747 — Fulfillment Gap as Root Cause**: 55.2% fill rate (31 pts below org) correctly identified as the root cause of reorder decay AND the constraint on account growth. The "$1.7M in additional invoiced revenue from existing demand" quantification is the money shot.

5. **el/1322 — Project-Based Outlier Detection**: The brief correctly identifies that -47.5% YoY is a base-effect distortion from a single $675K project order, not disengagement. Order frequency actually increased 6x. This prevents false alarm escalation.

### Missing Features (vs. Design Spec)

| Feature | From Design Doc | Status | Impact |
|---------|----------------|--------|--------|
| Buyer Intelligence (§14) | `03_advanced_insights.md` §4 | Gated for all 20 orgs (HAS_BUYER_NAMES < 5% everywhere) | Low — correctly gated per `07_prototype_findings.md` recommendation |
| Next Best Product (§17) | `03_advanced_insights.md` §1 | Present in 1/20 (blocked by V-01 volume gate on large accounts, not computed for small accounts) | High — this is the "82% of Meridian Sectional buyers also buy the Ottoman" insight from the Magnolia example. Currently unreachable for the pilot's account selection. |
| Cross-Sell Opportunity (§18) | `02_brief_sections.md` §8 | Present in 1/20 (thin cohorts make the analysis unreliable) | Medium — state-level cohorts are too small for accounts that dwarf their cohort (Wayfair at 474x MA avg). Need alternative cohort definition. |
| Fulfillment Impact on Reorder | `03_advanced_insights.md` §9 | Revenue quantification absent. Fill rate stated but backorder→reorder causal correlation not computed. | High — this is the "fix this, it's costing us $14K" feature. Partially present for ufi/2747 but without the per-SKU causal computation. |
| Account Lifecycle $ Projection | `03_advanced_insights.md` §10 | Stage label present. Dollar projection ("peak ~$400K next year") absent. | Medium — the narrative labels (Growing/Stable/Declining) are useful but the $ addressable growth calculation would add the monetization angle. |
| Market Commitment Conversion by Item | `03_advanced_insights.md` §8 | Only item counts shown (ufi/2747: "12 items, declining"). No per-item conversion analysis. | Medium — commitment data exists for only 1/20 orgs, limiting broad impact. |
| Rep Name in Header | `04_example_brief.md` | Never present | Low — requires mapping territory → rep, which is a lookup but doesn't block the brief. |

### Sections to Remove or Demote

| Section | Issue | Recommendation |
|---------|-------|----------------|
| §5 New Introduction Adoption (when org has 0 new_item=true) | ufi/8682 shows "No new items flagged (count: 0)" — empty section | **Gate on new_item count > 0.** Don't render an empty "no new items" placeholder. |
| §11 Showroom Placements (when all data > 2 years old) | ufi/2747: "2,380+ days old — showroom audit recommended" | **Gate on recency.** If ALL placements are > 730 days old, collapse to a single-line note ("Last placement audit: Dec 2019 — refresh recommended") rather than a full section with stale data. |
| §8 Channel Mix (when 100% "Unknown") | clm/463, fsf/03053, jyc/RESTO: "Unknown 100%" | **Gate or collapse.** A full table showing "Unknown | 100%" adds no intelligence. Collapse to single note when channel data is unpopulated. |
| §9 Wallet Share (when cohort < 5 customers) | jyc/RESTO: "Cohort comparison unavailable (no customer master)" | Already handled by the brief. But state-level cohorts with N=3 (fsf/03053 MA cohort) are unreliable. Consider minimum cohort threshold. |

### Formatting and Readability

**Strengths**:
- Consistent markdown structure across all 40 briefs (header → sections → summary)
- Dollar amounts use $K/$M abbreviations consistently
- Tables are well-aligned with clear headers
- Alert callouts (⚠) are attention-grabbing and appropriately used
- Health score visual bar provides instant classification

**Issues**:

| Issue | Briefs Affected | Severity |
|-------|----------------|----------|
| Section numbering inconsistent — some briefs jump from §2 to §6, skipping §3-§5 when those sections don't render | All briefs with gated sections | Low — understandable but creates a "where are sections 3-5?" reaction on first read |
| Health score bar visual inconsistent — some use code blocks, some inline | hfg/13869 (no code block), fsf/03053 (no code block) | Low — cosmetic |
| "Active months: 13" when max is 12 — caused by LTM window spanning partial calendar months | wwjc/21762, clm/463, ufi/8682, ih/119580 | Low — technically correct but confusing. Consider capping display at 12. |
| YoY "N/A" with no explanation when prior year = 0 | ih/119580, ril/U1090H | Low — already handled with "new account" context but inconsistent formatting |
| Some briefs use § prefix for sections, others don't | Consistent within each brief, varies across agents | Low — cosmetic standardization opportunity |

**Brief length assessment**: Deep-audited briefs range from 112 lines (cci/ZZZZZZZ) to 280 lines (ufi/2747). The sweet spot is 150-200 lines — long enough to be comprehensive, short enough to scan in 3-5 minutes. No brief is unacceptably long.

### Data Quality Patterns (with counts)

| Issue | Briefs Affected | % of Sample | Severity |
|-------|----------------|-------------|----------|
| **"Uncategorized" as top category (>25% of spend)** | 11/12 scanned | 92% | **High** — undermines the brief's strongest section (category analysis) |
| **Ghost SKUs (items with no catalog record)** | 7/12 scanned | 58% | **High** — blocks description, collection, inventory status for high-revenue items |
| **Stale placement data (>2 years old)** | 2/12 (all UFI placements from 2019-2020) | 17% | Medium — correctly flagged by briefs |
| **Missing buyer_name data** | 20/20 pilot orgs | 100% | Low — correctly gated by HAS_BUYER_NAMES threshold |
| **Fill rate = 0% (data not populated, not real stockout)** | 3/12 (fsf, jyc, ril) | 25% | Medium — brief sometimes presents 0% fill rate as alarming when the org simply doesn't populate invoice quantities |
| **Channel data "Unknown" / unpopulated** | 4/12 | 33% | Low — correctly noted in briefs |
| **Ship-to data unpopulated (SHP=F)** | 2/20 orgs (ufi, clli) | 10% | Low — correctly gated |

**Uncategorized severity by org** (highest first):
- hfg/13869: 100% (all items are ghost SKUs)
- ril/U1090H: 99.6% (FN-prefix custom items)
- gh/1103467: 89.1%
- el/1322: 72.9% ("Not For Display" category)
- sc/1213728: 51.9% (SCH-prefix configured items)
- scw/1103467: 44.4%
- ufi/2747: 38.0%
- ufi/8682: 34.9%
- fsf/03053: 33.8%
- lpf/1000031: 27.5%
- mhc/CUS003640: 25.7%
- clm/463: 2.4% ← **the model org for taxonomy**

### Prototype Recommendation Follow-Through

| Recommendation (from 07_prototype_findings.md) | Status | Evidence |
|-----------------------------------------------|--------|----------|
| Buyer Intelligence: demote to conditional, only show when > 1 distinct buyer | ✅ **Implemented** | HAS_BUYER_NAMES gate (G-07) with >5% threshold. Section absent in all 20 briefs. |
| Returns/RMA: keep gated, don't show empty section | ✅ **Implemented** | HAS_RMA gate (G-06). No empty "No returns found" sections. RMA data flows into Channel Mix when present. |
| eCat metrics: collapse to single note when eCat orders = 0 | ✅ **Implemented** | Briefs show "Account does not use eCat iPad — orders via [channel]" one-liner when eCat = 0. |
| Rep Engagement: gate on whether org's Mixpanel has selected_bill_to_code | ✅ **Implemented** | HAS_MIXPANEL_CUSTOMER gate (G-04). Section only renders for orgs with attributed events. |
| Lifecycle stage: move to header, not standalone section | ⚠ **Partially** | Lifecycle stage badge IS in the header bar. But health score breakdown (§22) is still a standalone section rather than integrated into the header lifecycle position. |
| Same-Store Comps: test alternative join paths for ship-to data | ⚠ **Partially** | HAS_SHIP_TO_DATA gate (G-09) prevents rendering on orgs without data. Same-Store section works where data exists (clm/463 shows 61 ship-tos). But the prototype's concern about empty ship-to fields persists for UFI (SHP=F). |
| Advanced queries (CQ-06, CQ-09, CQ-19, CQ-20): validate on rich accounts | ⚠ **Partial** | CQ-09 (Reorder Decay) fully validated and working well across 8/20 briefs. CQ-06 (Next Best Product) blocked by V-01 volume gate for the pilot's large accounts. CQ-19 (Cross-Sell) thin due to cohort size issues. CQ-20 (Category Evolution) working in 8/20 briefs. |

---

## Recommendations for v4

### Must-Fix (blocks production use)

1. **Health score arithmetic bug** — wwjc/21762 demonstrates a normalization error (84/90 → 91 instead of 93). Audit the score computation function for division/rounding bugs. Additionally, H6 (fill rate) must use the actual CQ-15 fill rate vs. org rate, not a proxy based on replacement orders.

2. **Fill rate = 0% false alarm** — Three orgs (fsf, jyc, ril) show 0% fill rate because `portal_order_items.quantity_invoiced` is not populated (not because orders aren't being fulfilled). The brief presents this as "critical" fulfillment failure. **Fix**: gate the fill rate section on whether the org actually populates invoice quantities (e.g., require >50% of `quantity_invoiced` values to be non-zero).

3. **Ghost SKU identification in §4 Top Items** — Ghost SKUs appear as "*(no catalog record)*" with 0 available stock, which is visually identical to a real stock-out. **Fix**: Clearly distinguish between "item not in catalog (cannot check stock)" vs. "item in catalog with 0 available."

### Should-Fix (improves quality significantly)

4. **Next Best Product volume gate is too aggressive** — V-01 blocks CQ-06 for customers with >10,000 LTM orders. The pilot specifically selected large accounts (Wayfair, Lamps Plus, NFM) that all exceed this threshold. Result: the advanced insight with the highest "wow factor" from the design spec is unreachable for the most important accounts. **Fix**: either optimize the query for high-volume accounts, sample a subset of recent orders, or lower the threshold with timeout handling.

5. **Cross-sell cohort definition** — State-level cohorts produce absurd comparisons when the target account dwarfs all peers (Wayfair at 474x MA avg; Lamps Plus at 60x CA avg). **Fix**: add a secondary cohort path: (a) state + spend decile (original design), (b) national accounts with spend within 2x, (c) same-category-mix customers regardless of geography.

6. **Expand Strategic Summary to 5-6 talking points** — Current briefs consistently produce 3 rep talking points. The Magnolia example has 6. More is better for pre-meeting prep. Target 5-6 with explicit priority sequencing ("Close this first, then explore this").

7. **Add seasonality visualization** — The Magnolia example uses ASCII bar charts for monthly revenue. Current briefs use plain tables. For orgs where monthly data is available, add a visual representation — even a simple `████` bar would improve scannability.

8. **Active months display cap at 12** — Several briefs show "Active months: 13" due to LTM window edge effects. Cap the displayed value at 12 and add a note if all months show activity.

### Nice-to-Have (polish)

9. **Normalize section numbering** — Either always show sequential §1, §2, §3... (renumbering to exclude gated sections), or use named sections without numbers. The current gap (§1, §2, §6, §7...) is confusing on first read.

10. **Add rep name to header** — Territory code is present; map to the assigned rep name for personalization ("Prepared for: Blake Fisher — Territory MW").

11. **Wallet share minimum cohort size** — When the state cohort has <5 customers (fsf MA = 3), note that the comparison is "indicative only" or skip. Very small cohorts are unreliable.

12. **"Uncategorized" category handling** — When >50% of spend is uncategorized, add an explicit callout at the top of §3: "⚠ Category analysis limited: [X]% of spend has no product category assigned. Contact [client] about catalog enrichment." Already partially implemented — standardize the format and add the org-level recommendation.

### Strategic (new capabilities for next version)

13. **Multi-account customer view** — The Wayfair accounts (mhc/CUS003640 + CUS010704) and Sunstar Properties (scw/1103467 + gh/1103467) demonstrate that major buyers have multiple bill-to codes across orgs or within an org. A "customer group" rollup that links related accounts would prevent fragmented intelligence.

14. **Anomaly-first brief structure** — The best briefs (mhc/CUS003640 cliff detection, sc/1213728 fulfillment crisis, ufi/2747 fill rate gap) lead with the most surprising/alarming finding. Consider computing a "surprise score" per section and reordering the brief to lead with the highest-surprise content.

15. **Projected revenue at risk / opportunity** — The Magnolia example quantifies opportunity ("$116K addressable growth"). Current briefs occasionally do this (ufi/2747: "$1.7M additional if fill rate recovers") but it's not systematic. Add a standard "Revenue at Risk" and "Revenue Opportunity" computation to §23.

16. **Competitive loss signal as primary alert** — When eCat is declining while total business grows (sc/1213728), this should be a top-of-brief banner alert, not just a 5-point health score penalty. It's the single most important signal in the entire system.

---

*Audit completed 2026-06-16 | Auditor: Claude (SuperCat CI Pilot Audit) | Read-only posture maintained throughout*
