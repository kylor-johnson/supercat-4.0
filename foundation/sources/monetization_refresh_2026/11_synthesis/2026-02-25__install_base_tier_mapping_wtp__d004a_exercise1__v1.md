# Install-Base Tier Mapping & Revealed WTP Analysis

> **Purpose**: Map every active account to its natural tier under the new Good/Better/Best architecture based on current module stack, then analyze current pricing by tier-equivalent to establish a data-driven WTP floor and ceiling for each tier. First exercise for D-004a (Set price points for each tier).
>
> **Phase**: 2, Workstream B (Price Point Modeling)
>
> **Data sources**: Master account table v3 (104 accounts, Angie-audited), `build_account_master_v3.py` book rate definitions
>
> **Date**: February 25, 2026

---

## Tier Assignment Methodology

Each account is assigned to its **natural tier** based on the highest-tier module it currently pays for:

| Natural Tier | Module Signal | Current Stacks |
|---|---|---|
| **T1: Catalog Essentials** | No Cart, No Portal. iPad-only or iPad+Catalog. | `iPad-only`, `iPad+Catalog` |
| **T2: Commerce Professional** | Has Cart but NOT Portal. Commerce capabilities without analytics/self-serve portal. | `iPad+Catalog+Cart` |
| **T3: Commerce Enterprise** | Has Portal (regardless of Cart). Portal currently bundles analytics + buyer self-serve — both map to T3 as the tier where Sales Intelligence (analytics) is gated. | `iPad+Catalog+Portal`, `Full (Cart+Portal)` |

**Add-ons** (CPQ, PCI, Image Upgrade, Closed Site) are orthogonal to tier assignment — tracked separately.

**What "platform-only MRR" means**: Each account's MRR decomposes into three components: (1) platform/module fees, (2) additional user charges, and (3) add-on charges (CPQ, PCI). The **platform-only MRR** strips out users and add-ons to isolate what they pay for the *capability bundle* — this is the price that a new tier fee replaces.

---

## Step 1: Tier Assignment Summary

| | **T1: Catalog Essentials** | **T2: Commerce Professional** | **T3: Commerce Enterprise** |
|---|:---:|:---:|:---:|
| **Accounts** | **61** (59%) | **9** (9%) | **34** (33%) |
| **Total MRR** | $59,132/mo (40%) | $13,735/mo (9%) | $75,731/mo (51%) |
| **Total ARR** | $709,586 | $164,822 | $908,774 |
| **Stack breakdown** | 56 iPad-only, 5 iPad+Catalog | 9 iPad+Catalog+Cart | 20 Full Stack, 14 Catalog+Portal |

### Critical observation: T2 is tiny

Only **9 accounts** (9%) map to T2 by module stack. This means the overwhelming majority of accounts either haven't adopted any commerce modules (T1) or went directly to the full stack including Portal (T3). Very few stopped at Cart-only.

**Implications for pricing**:
- T2 is the **hero tier for growth**, not the hero tier by install base. Almost the entire T2 opportunity is in *new customers* and *T1 upgrades*, not in migrating existing accounts.
- The T2 price point needs to be attractive enough to pull T1 accounts upward — it's an aspirational landing zone, not a correction exercise.
- T3's dominance (51% of MRR from 33% of accounts) means T3 pricing is the most consequential for install-base revenue.

### Crosswalk to M1 Segments

The M1 behavioral segments and the module-based tier mapping don't perfectly overlap:

| | M1 Segment | Natural Tier |
|---|:---:|:---:|
| Catalog-Focused | 56 | — |
| Commerce-Active | 28 | — |
| Platform-Embedded | 20 | — |
| T1 (by module) | — | 61 |
| T2 (by module) | — | 9 |
| T3 (by module) | — | 34 |

The delta: M1 classified 28 accounts as "Commerce-Active" (T2 behavioral), but only 9 have the T2 module stack. This means ~19 accounts that M1 considers Commerce-Active are either:
- **iPad-only/Catalog accounts with high order volume** (behaviorally active but modularly T1) — these are the prime T1→T2 upgrade candidates
- **Portal-having accounts** that M1 classified as Commerce-Active rather than Platform-Embedded — these are modularly T3 but behaviorally mid-stage

This gap is actually good news for the pricing model: it means there's significant **natural upgrade pull** from T1 to T2 — accounts that are *behaviorally* ready for commerce but haven't yet paid for the modules.

---

## Step 2: MRR Decomposition by Tier-Equivalent Group

### 2a: Total MRR Structure

| Component | T1 | T2 | T3 | Total |
|---|---:|---:|---:|---:|
| **Platform fees** | $44,288 (75%) | $12,422 (90%) | $57,236 (76%) | $113,946 (77%) |
| **User charges** | $14,844 (25%) | $1,314 (10%) | $18,496 (24%) | $34,653 (23%) |
| **Add-on charges** | $1,170 (2%) | $0 (0%) | $975 (1%) | $2,145 (1%) |
| **Total MRR** | **$59,132** | **$13,735** | **$75,731** | **$148,598** |

User revenue ($34,653/mo, $416K/yr) is 23% of total MRR. This revenue stream must be preserved and ideally grown under the new model — it's not replaced by tier pricing.

### 2b: Platform-Only MRR Distribution (the tier-price proxy)

This is the core WTP signal — what accounts currently pay for capabilities alone, excluding users and add-ons:

| Statistic | T1 | T2 | T3 |
|---|---:|---:|---:|
| **Mean** | $707 | $1,380 | $1,655 |
| **Median** | $725 | $1,414 | $1,670 |
| **P25** | $652 | $1,387 | $1,515 |
| **P75** | $725 | $1,427 | $1,810 |
| **Min** | $306 | $920 | $732 |
| **Max** | $1,291 | $1,684 | $2,862 |

**Key observations**:
- **T1 clusters tightly at $725**: The median and P75 are both $725 (current iPad book rate). The distribution has a long left tail (deeply discounted legacy accounts) and a right tail of accounts paying above book (iPad+Catalog or above-book platform fees).
- **T2 clusters tightly at $1,387–$1,427**: Very narrow IQR. The median ($1,414) is just above the current iPad+Catalog+Cart book rate ($1,315). T2 accounts generally pay at or above book.
- **T3 has meaningful spread**: P25–P75 is $1,515–$1,810, reflecting the mix of Catalog+Portal ($1,415 book) and Full Stack ($1,710 book). The median ($1,670) falls between these two book rates.

### 2c: Tier Price Ratios

| Ratio | Value | Implication |
|---|:---:|---|
| **T2 / T1** | **2.0x** | The step from catalog to commerce is a doubling — consistent with the value jump (adding ordering + buyer self-serve) |
| **T3 / T1** | **2.3x** | T3 is ~2.3x T1 — a clear premium but not extreme |
| **T3 / T2** | **1.2x** | The step from T2 to T3 is only ~20% — this is tight and may need to be wider to justify the T3 premium |

The 1.2x T3/T2 ratio is a pricing concern. In typical Good/Better/Best models, each tier step is 1.5–2.5x. A 1.2x gap means T3 barely differentiates from T2 on price, which:
- Reduces the perceived "upgrade" value
- Makes T3 feel like "T2 with a small surcharge for analytics" rather than a distinct tier
- Could be addressed by *either* raising T3 *or* lowering T2 relative to current pricing

### 2d: User Economics by Tier

| | T1 | T2 | T3 |
|---|:---:|:---:|:---:|
| **Accounts with addl users** | 26/61 (43%) | 3/9 (33%) | 31/34 (91%) |
| **Mean addl users** | 26 | 17 | 30 |
| **Median addl users** | 23 | 6 | 25 |
| **Mean effective rate** | $21/user | $19/user | $19/user |
| **Median effective rate** | $20/user | $20/user | $20/user |

The effective user rate is remarkably consistent across tiers: ~$20/user vs. the $25 book rate. This is driven by the pervasive $20/user discount (the most common negotiated rate). The user discount curve design (D-004b) should account for this revealed rate as a de facto market price.

---

## Step 3: Tier Value Gap Analysis

### What accounts GAIN in the new tier (capabilities they don't have today)

| Tier | Avg new capabilities gained | Key value-adds |
|---|:---:|---|
| **T1** | 0.9 | Online Product Catalog (for the 56 iPad-only accounts that don't have it) |
| **T2** | 6.0 | Closed Site, Buyer Registration, Customer-Specific Pricing, Quick-Order Grid, Address Validation, Order & Invoice Tracking |
| **T3** | 8.2 | Sales Intelligence Dashboard, Territory Views, Reports, Data Export, Priority Support, Dedicated CSM, Executive Business Reviews, Image upgrade (12 images) |

**The value-add story is strongest for T2 and T3**. These accounts gain significant new capabilities bundled into their tier that they'd previously have to purchase separately (or don't have at all). This creates a compelling migration narrative: "For the same or slightly higher price, you now get [6-8 additional capabilities]."

### T3 sub-population: Catalog+Portal (no Cart)

14 of 34 T3 accounts have Portal but NOT Cart. Under the new architecture, Cart is a T2 feature — these accounts would be landing in T3 and **gaining B2B Cart as an included capability** they don't have today. This is a meaningful value add that strengthens the migration argument for this sub-group.

### Accounts with features "above" their tier

- 1 T1 account (Visual Comfort Signature) has Closed Site — a T2 feature
- 1 T1 account (Hooker Furnishings) has Image Upgrade — a T3 feature
- Both are edge cases, not structural issues

---

## Step 4: Revealed WTP Summary

### Per-Tier WTP Ranges (platform-only MRR)

| | **Price Floor (P25)** | **Revealed Median** | **Price Ceiling (P75)** | **Current Book** |
|---|---:|---:|---:|---:|
| **T1** | $652/mo | **$725/mo** | $725/mo | $725 (iPad-only) |
| **T2** | $1,387/mo | **$1,414/mo** | $1,427/mo | $1,315 (iPad+Cart) |
| **T3** | $1,515/mo | **$1,670/mo** | $1,810/mo | $1,710 (Full Stack) |

### Migration Risk at Candidate Price Points

The tables below show how many accounts fall below each candidate price point on platform-only MRR, and the total monthly revenue gap (what those below-point accounts would need to absorb).

#### T1: Catalog Essentials

| Candidate Price | Accounts Below | Accounts At/Above | % Below | Revenue Gap |
|---:|:---:|:---:|:---:|---:|
| $500 | 8 | 53 | 13% | $912/mo |
| $600 | 11 | 50 | 18% | $1,772/mo |
| **$700** | **26** | **35** | **43%** | **$3,575/mo** |
| **$725** | **30** | **31** | **49%** | **$4,274/mo** |
| $800 | 53 | 8 | 87% | $8,038/mo |
| $900 | 54 | 7 | 89% | $13,418/mo |

**T1 guidance**: $725 is the natural anchor (current book rate, revealed median). Pricing below $725 would be a de facto price cut for the majority. Pricing above $725 would require a strong value narrative (Online Catalog now included). 43% of accounts are below $700 — largely legacy/multi-org discounts that need migration treatment regardless.

#### T2: Commerce Professional

| Candidate Price | Accounts Below | Accounts At/Above | % Below | Revenue Gap |
|---:|:---:|:---:|:---:|---:|
| $900 | 0 | 9 | 0% | $0/mo |
| $1,000 | 1 | 8 | 11% | $80/mo |
| $1,100 | 1 | 8 | 11% | $180/mo |
| $1,200 | 1 | 8 | 11% | $280/mo |
| **$1,315** | **2** | **7** | **22%** | **$436/mo** |
| **$1,400** | **4** | **5** | **44%** | **$633/mo** |
| $1,500 | 7 | 2 | 78% | $1,277/mo |

**T2 guidance**: The revealed WTP clusters tightly around $1,387–$1,427. The current book rate ($1,315 for iPad+Cart) is below the revealed median — accounts are already paying more. Pricing T2 at $1,300–$1,400 would fit within the revealed range. Only 1 account (Alden Home, deeply discounted at $920) is a significant outlier.

#### T3: Commerce Enterprise

| Candidate Price | Accounts Below | Accounts At/Above | % Below | Revenue Gap |
|---:|:---:|:---:|:---:|---:|
| $1,200 | 3 | 31 | 9% | $874/mo |
| $1,400 | 3 | 31 | 9% | $1,474/mo |
| **$1,500** | **5** | **29** | **15%** | **$1,929/mo** |
| **$1,600** | **16** | **18** | **47%** | **$3,153/mo** |
| **$1,710** | **18** | **16** | **53%** | **$4,992/mo** |
| $1,800 | 22 | 12 | 65% | $6,758/mo |
| $2,000 | 32 | 2 | 94% | $12,611/mo |

**T3 guidance**: The distribution is wide (P25–P75: $1,515–$1,810). The median ($1,670) falls below the current Full Stack book rate ($1,710). At $1,710, 53% of T3 accounts are below — meaning the majority would need migration accommodation. At $1,500, only 15% are below — but this would represent a significant price cut from current book.

---

## Key Findings for D-004a

### Finding 1: The install base reveals three distinct price bands

The revealed WTP data confirms that three tiers are the right structure — the price bands are clearly separated:
- **T1 band**: $650–$725/mo (tightly clustered around current iPad book rate)
- **T2 band**: $1,300–$1,430/mo (slightly above current iPad+Cart book rate)
- **T3 band**: $1,500–$1,810/mo (spanning from Catalog+Portal to Full Stack book rates)

### Finding 2: T2 is the growth tier, not the install-base tier

Only 9 accounts (9%) currently map to T2. This tier's price point should be set to **attract T1 upgrades and new customers**, not to optimize existing-customer revenue. The T2 price is primarily a *sales* tool, not a *migration* tool.

### Finding 3: The T3/T2 ratio needs widening

At revealed pricing, the T3/T2 ratio is only 1.2x — too tight for meaningful differentiation. Options:
1. **Raise T3** to create a clear premium (e.g., $1,800–$2,000 with the value narrative of Sales Intelligence + premium support + expanded capacity)
2. **Lower T2** to widen the gap (e.g., $1,200–$1,300, making it more accessible)
3. **Both** — which would create a wider "aspirational gap" for upgrades

### Finding 4: User revenue is significant and tier-independent

User charges ($34,653/mo, 23% of total) must be preserved. The effective market rate is ~$20/user across all tiers, well below the $25 book rate. The user discount curve (D-004b) should use $20/user as the realistic baseline, not $25.

### Finding 5: T3 accounts missing Cart = strongest value-add migration story

14 T3 accounts have Portal but NOT Cart. They gain B2B Cart (online ordering) bundled into T3 — a tangible new capability that didn't exist in their old deal. This is the easiest migration conversation: "You get the same portal you have today, plus online ordering and [5 other new capabilities], at a comparable price."

### Finding 6: T1 has a bimodal distribution

T1 platform-only MRR splits into two clusters:
- **At-book cluster** (~31 accounts at $700–$725): Standard or near-standard pricing
- **Below-book cluster** (~30 accounts at $306–$680): Legacy discounts, multi-org programs, rollup children

Any T1 price point at or near $725 will be revenue-neutral for the at-book cluster but require migration treatment for the below-book cluster. This is not a pricing problem — it's a migration sequencing problem (Phase 2, Workstream D).

### Finding 7: New tier prices can include MORE value at comparable cost

| Tier | Revealed Median | Avg Capabilities Gained | Migration Narrative |
|---|---:|:---:|---|
| T1 | $725/mo | 0.9 | "Same price, plus Online Product Catalog included" |
| T2 | $1,414/mo | 6.0 | "For what you pay now, you get 6 more capabilities" |
| T3 | $1,670/mo | 8.2 | "For what you pay now, you get 8+ more capabilities including analytics and premium support" |

This "more value at comparable cost" framing is the strongest migration argument. Tier prices near the revealed medians would be approximately revenue-neutral for existing accounts while significantly increasing the perceived value.

---

## Preliminary Price Point Ranges for D-004a Discussion

Based on this exercise, the following ranges are data-informed anchors (not final recommendations — competitive benchmarking and concept testing will pressure-test):

| Tier | Revealed Anchor | Suggested Range | Rationale |
|---|---:|---:|---|
| **T1** | $725 | **$695–$795** | At or near current book. Online Catalog inclusion justifies modest uplift. Below $700 would be a price cut. |
| **T2** | $1,414 | **$1,195–$1,395** | Below the revealed median to maximize T1→T2 upgrade pull. The hero tier should be priced for adoption, not extraction. |
| **T3** | $1,670 | **$1,795–$2,195** | Above the revealed median to create clear T2→T3 premium. The value narrative (Sales Intelligence, priority support, CSM, 50 users) justifies uplift beyond what current module bundling commands. |

These ranges would produce tier ratios of approximately:
- T2/T1: 1.5–2.0x (vs. 2.0x revealed)
- T3/T2: 1.3–1.8x (vs. 1.2x revealed — widened)
- T3/T1: 2.3–3.2x (vs. 2.3x revealed)

---

## Open Concerns

### Concern 1: Barbell Distribution vs. Expected Bell Curve

Classic G/B/B models target a bell curve (e.g., 20/60/20) with the hero tier capturing the majority. This exercise produced a barbell: 59% T1, 9% T2, 33% T3.

**Assessment**: The barbell describes the current state under the old a-la-carte model — it is the symptom of Problem 2 ("per-module pricing does not support natural expansion or tier logic"). Under the old model, there was no structural middle to land in. The new T2 is designed to create the bell curve landing zone. Three sources should populate it over time:

1. **T1 upgrades**: ~19 behaviorally-Commerce-Active T1 accounts are the immediate pipeline
2. **New customers**: Prospects with existing B2B sites or trade logins see a coherent middle option for the first time
3. **T3 right-sizing**: Some current T3 accounts (the 14 with Portal but no Cart) may be better served at T2 if their Portal use is primarily buyer self-serve rather than analytics

**Monitoring**: If T2 remains at <15% of accounts after 12 months of new-customer acquisition, the tier fence or pricing needs revisiting.

### Concern 2: T3 Support Capacity

T3 promises priority support SLA, dedicated CSM, and executive business reviews. At 34 accounts, this may exceed current support capacity.

**Mitigating factors**:
- T3 population may shrink to 20–25 if some Portal-but-no-Cart accounts resolve to T2 after the Sales Portal decomposition decision
- "Dedicated CSM" at 10–15 account book size is standard; 20–25 T3 accounts = 2 CSMs, 34 = 3
- Support tiers within T3 can be graduated (quarterly vs. semi-annual business reviews)

**Resolution path**: Workstream C (Operational Readiness) must answer "can we deliver T3-level support to N accounts?" before T3 pricing is finalized.

**Dependency resolved (2026-02-25)**: Sales Portal decomposition stamped as D-003e — Option A (Buyer Self-Serve in T2, Sales Intelligence in T3), confirmed by Sales + CTO. Portal-but-no-Cart accounts primarily using buyer self-serve rather than analytics are now T2 candidates, potentially reducing T3 from 34 to 20–25.

---

## Exercise 2: Competitive Price Benchmarking — COMPLETE

See `11_synthesis/2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md`.

Exercise 2 validated T1 and T2 ranges unchanged. T3 shifted upward from $1,795–$2,195 to **$1,995–$2,495** based on competitive headroom (AmpTab Pro at $3,000, Pepperi Ultimate at $6,400+). Combined ranges and tier ratios documented in the Pricing Constitution.

---

## Appendix: Analysis Script

Analysis generated by `03_data/tier_mapping_wtp_analysis.py` against `03_data/extracts/2026-02-28__master_account_table__v3.csv`. Full account-level data available in script output.
