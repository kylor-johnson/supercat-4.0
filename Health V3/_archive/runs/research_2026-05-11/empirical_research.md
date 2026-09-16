# Empirical Research — SuperCat Client Portfolio (2026-05-11)

**Purpose:** Surface real-data patterns from the 104-org paying portfolio to inform calibration of Health V3 scoring bands. **Findings only — not a model.**

**Data sources used:**
- MAL: `Health V2/inputs/master_account_list_2026-04-14_canonical.csv` (104 orgs)
- Postgres `login_events`, `org_users`, `users`, `organizations`, `mobile_sites`, `smart_stacks`, `orders`, `portal_orders`, `products`, `subscriptions`, `import_events` (live MCP `user-supercat-postgres-vpn`)
- BigQuery `mixpanel.events` (`item_email_drafted`, `document_email_drafted`, trailing 90d + 30d) (live MCP `user-bigquery-vpn`)

**Critical baseline caveat that constrains every section below:** `login_events.MIN(created_at) = 2024-11-12`. The earliest login event in the warehouse is ~6 months ago. Year-over-year seasonality cannot be observed; the trailing-12-month series only spans April 2025 → April 2026. Multi-year cohort behavior cannot be inferred from this table.

A second caveat: `subscriptions.start_date` for 272 of 279 rows falls between 2025-08-25 and 2025-08-29 — a backfill date. `end_date` is null on every single row. The table is effectively useless as a churn-history source for any cohort earlier than mid-2025.

---

## Section 1: Engagement Signal Distributions

### 1a. Login count distribution (trailing 90d)

**Pooled (all 104 orgs):**

| Quantile | logins_90d |
|---|---|
| min | 7 |
| p10 | 97 |
| p25 | 314 |
| p50 (median) | 927 |
| p75 | 2,100 |
| p90 | 3,623 |
| max | 15,720 |

**Band breakdown (against current V3 bands):**

| Band | n | % of portfolio | Current V3 score |
|---|---|---|---|
| 0 logins | **0** | 0.0% | 0 |
| 1–9 | 2 | 1.9% | 20 |
| 10–49 | 5 | 4.8% | 20 |
| 50–199 | 8 | 7.7% | 40 |
| 200–499 | 23 | 22.1% | 60 |
| 500–999 | 16 | 15.4% | 75 |
| 1,000–2,999 | 34 | 32.7% | 88 |
| 3,000+ | 16 | 15.4% | 100 |

**By tier:**

| Tier | n | median | p25 | p75 | min | max |
|---|---|---|---|---|---|---|
| iPad-only | 56 | 473 | 225 | 1,114 | 9 | 4,499 |
| iPad+Catalog | 5 | 116 | 12 | 1,626 | 7 | 6,250 |
| iPad+Catalog+Cart | 9 | 1,062 | 551 | 1,352 | 228 | 2,040 |
| iPad+Catalog+Portal | 14 | 2,521 | 2,030 | 3,995 | 299 | 15,720 |
| Full | 20 | 2,000 | 1,433 | 2,929 | 333 | 7,450 |

**Observations:**
1. **Zero orgs have zero logins.** The current `0 → 0 pts` band is empty in V3.0 — no paying org in the portfolio is a true ghost on logins alone. The §5.1 Ghost Account override (`arr ≥ 5000 AND logins_90d = 0`) cannot fire on this snapshot.
2. **The bottom of the distribution is iPad-only and iPad+Catalog.** The 9 orgs in the bottom decile (`logins_90d < 100`) are all iPad-only or iPad+Catalog. Three iPad+Catalog orgs (`tel`=12, `st`=7, `mfc`=116) and four iPad-only orgs (`hh`=17, `krb`=9, `ol`=40, `cf`=44) account for the entire low-engagement tail.
3. **The portfolio is heavily right-shifted.** Median is 927 logins/90d ≈ 10/day. The current V3 ladder gives a median org a score of 75 (the `500-999` band), which means half the portfolio sits in just two bands (75 and 88).

**Implications for calibration:**
- The `1–49` band (20 pts) catches only 7 orgs (6.7%). Combining `1–9` and `10–49` into a single `1-49 → 20 pts` band, as the V3 spec already does, is fine — but the `0 → 0` band may not need to exist as a separate scoring slot since no paying org reaches it.
- A natural break in the pooled data is at ~100 logins (tail vs. middle) and at ~500 logins (middle vs. heavy-user). The current break at 200 (the 60-pt threshold) sits between two adjacent percentiles (p25=314) — it's well-placed.
- **The iPad+Catalog tier (n=5) has so much within-tier variance (min=7, max=6,250) that any tier-stratified analysis using this group is statistically meaningless.** Pre-register that the iPad+Catalog tier is not big enough to produce reliable per-tier band thresholds.

---

### 1b. Active user ratio distribution

**Pooled (raw uncapped ratio = active_users_90d / enabled_users):**

| Quantile | ratio |
|---|---|
| min | 0.00 |
| p10 | 0.00 |
| p25 | 0.10 |
| p50 (median) | 0.40 |
| p75 | 0.60 |
| p90 | 0.90 |
| max | **1.50** |

Orgs with raw ratio > 100% (denominator inflated): **2 of 104 = 1.9%** (`mlc`=108%, `soi`=150% — both small iPad-only orgs where stale `org_users` rows are likely the explanation).

**By tier — and the B2B-customer-account inflation problem:**

| Tier | n | median ratio | p90 | inflated >1.0 | **median enabled_users** |
|---|---|---|---|---|---|
| iPad-only | 56 | 0.57 | 0.88 | 2 | **48** |
| iPad+Catalog | 5 | 0.10 | 0.58 | 0 | **133** |
| iPad+Catalog+Cart | 9 | 0.04 | 0.11 | 0 | **361** |
| iPad+Catalog+Portal | 14 | 0.57 | 0.86 | 0 | **100** |
| Full | 20 | **0.03** | 0.09 | 0 | **1,366** |

**Full-tier `enabled_users` distribution (the headline finding):**

| n | min | p25 | median | p75 | max |
|---|---|---|---|---|---|
| 20 | 266 | 678 | **1,366** | 3,666 | **20,422** |

**13 of 20 Full-tier orgs have `enabled_users > 1000`.** Specific outliers:

| Org | enabled_users | active_users_90d | "ratio" |
|---|---|---|---|
| wwjc | 20,422 | 50 | 0.2% |
| jyc | 15,961 | 69 | 0.4% |
| fc | 9,229 | 35 | 0.4% |
| gh | 7,911 | 56 | 0.7% |
| scw | 4,484 | 60 | 1.3% |
| sbmh | 3,393 | 31 | 0.9% |
| lpf | 2,341 | 49 | 2.1% |
| shl | 2,104 | 50 | 2.4% |
| kal | 1,662 | 53 | 3.2% |
| bcf | 1,423 | 56 | 3.9% |
| bri | 1,308 | 61 | 4.7% |
| sccon | 1,170 | 35 | 3.0% |
| clc | 1,046 | 59 | 5.6% |

**Observations:**
1. **Inflated denominator is a tier-correlated structural issue, not a few stale-flag bugs.** `org_users` for Full-tier orgs is dominated by B2B customer-portal accounts. The §1 spec note about `denominator_quality = stale` only triggers when raw ratio > 100% — that catches 2 orgs. The real problem is the 13 Full-tier orgs whose ratio is *plausibly* inflated to look like 1–6% but where the "true" rep-only ratio is closer to 50–80%. The current ratio score gives most of these orgs a `20` (the `1–24%` band) when their internal-user activity is probably normal.
2. **iPad+Catalog+Portal tier looks healthy on ratio (median 0.57)** because its `enabled_users` median is 100 — it doesn't have the B2B portal customer contamination that Full does. So the `enabled_users` issue isn't about portal in general; it's about Full bundles where the *cart* + portal customer accounts pile into `org_users`.
3. **iPad+Catalog+Cart (n=9) shows the same problem** with median enabled_users=361 — Cart-tier orgs have customer accounts even without Sales Portal.

**Implications for calibration:**
- The `denominator_quality = stale` flag, as currently specified (`raw ratio > 100%`), only catches 2 of the 13 Full-tier orgs whose denominator is structurally inflated. **Recommend: trigger the stale flag whenever `enabled_users > 500 AND tier IN ('Full', 'iPad+Catalog+Cart')`**, not based on the raw ratio. Or — better — **count enabled internal users from `login_events` (distinct user_id in 365d) when enabled_users > 500**, which is already specified as the fallback but is currently only a manual spec note, not an automatic switch.
- 16 of 56 iPad-only orgs have active_user_ratio ≥ 0.90 → score 100. The ratio scoring is doing useful work in iPad-only but is essentially a no-op (everyone scores 20) for Full-bundle orgs.

---

### 1c. Recency

**Days-since-last-login bucketing:**

| Bucket | n | % |
|---|---|---|
| ≤ 7 days | 103 | 99.0% |
| 8–30 days | 0 | 0.0% |
| 31–90 days | 1 | 1.0% |
| > 90 days | 0 | 0.0% |
| Never | 0 | 0.0% |

**The recency dimension does almost no work in V3.0.** 99% of paying orgs logged in within the past 7 days → recency score = 100 for nearly everyone. The only org outside that window is `tel` (67 days since last login).

**"Cooling off" detection — orgs with high logins_180d but low logins_30d (< 10% of 180d total):**

| Org | tier | logins_180d | logins_30d | days since last |
|---|---|---|---|---|
| kl | iPad-only | 1,218 | 114 | 0 |
| prog | iPad-only | 804 | 80 | 0 |
| afx | iPad-only | 688 | 65 | 0 |

These orgs *are* still active in the last 7 days, just slower than they used to be. The current recency band can't see this — it only thresholds on the most recent login date.

**Implications for calibration:**
- **The "Last Login Recency" sub-signal in §1 carries effectively zero discriminating power on this portfolio.** It is contributing 100 to ~99% of orgs and is dragging the engagement composite up.
- Consider replacing the recency sub-signal with a **trend / "activity decay" signal** like `logins_30d / logins_180d × 6`. Values much below 1.0 indicate a cooling-off pattern that the current scoring misses entirely. (Three orgs above qualify as plausible decay candidates.)
- Or remove the recency sub-signal entirely and average the remaining two — it is essentially a no-op.

---

### 1d. Seasonality

**Coverage warning:** `login_events` only goes back to 2024-11-12. We can compare April 2025 to April 2026 for orgs that existed both years, but we cannot see HPMKT 2024 (April–May) or any pre-2024-11 baseline.

**Aggregate monthly logins, sum across 30 sampled orgs:**

| Month | logins | YoY available? |
|---|---|---|
| 2025-04 | 60,479 | (baseline) |
| 2025-05 | 52,064 | (baseline) |
| 2025-06 | 53,551 | |
| 2025-07 | 52,693 | |
| 2025-08 | 48,566 | |
| 2025-09 | 50,595 | |
| 2025-10 | 57,559 | |
| 2025-11 | 44,819 | |
| 2025-12 | 40,229 | |
| 2026-01 | **65,611** | |
| 2026-02 | 54,387 | |
| 2026-03 | 57,700 | |
| 2026-04 | 59,512 | -1.6% YoY |
| 2026-05 (partial) | 17,864 | (in-progress) |

**Observations:**
1. **There is no clear April HPMKT spike at the portfolio level.** April 2025 = 60.5k, April 2026 = 59.5k — both higher than the surrounding months but only ~7-12% above the trough months (Aug 2025 = 48.6k, Dec 2025 = 40.2k). The April peak is much smaller than expected for a "market-driven" business.
2. **There is a sharp January spike: 2026-01 = 65,611 (highest month observed).** Several orgs show this clearly: `clm` jumps from 512 → 1,318; `wac` from 437 → 1,438; `vcg` from 870 → 2,073; `sbl` from 224 → 723. This is consistent with the major lighting/furniture markets in January (Las Vegas / Dallas / Atlanta winter shows).
3. **Per-org seasonality is highly variable.** `mh` (lighting) has spikes in 2025-04 (1,839) AND 2025-10 (1,747) AND 2026-04 (2,158) — a clear bi-annual pattern. `pf` (furniture) has its peak in 2026-04 (2,411) and 2025-10 (2,159). `wwjc` (lighting) is remarkably flat (range 700–1,200/month). `sc` (Summer Classics — outdoor) is also flat (3,400–5,700) across all months.
4. **Several orgs show declining trends that look like they should be flagged as at-risk:** `jc` 2025-10=178 → 2026-02=42 → 2026-04=171 (volatile but no clean "decline"). `hmjc` 2025-10=57 → 2026-02=7 → 2026-05=1 (clear cliff-fall, possibly churned — see §5.c subscriptions data: hmjc's only sub rows are `canceled`).

**Implications for calibration:**
- The spec correctly defers seasonality to V3.1 because there isn't enough history. With only 18 months of data, **any seasonality model based on this table will be confounded with portfolio growth**.
- However, the V3.1 trigger logic ("dimension drop ≥ 20 points MoM") will misfire for HPMKT-driven orgs: April spikes followed by May drops would otherwise look like collapse. Document a winter/spring peak whitelist (lighting orgs spike Jan and Oct; furniture orgs spike Apr and Oct) before V3.1 ships.
- The January 2026 spike is so large at the portfolio level (65k vs Dec 40k = +63%) that **a 90-day window ending in late January will systematically over-credit engagement vs a 90-day window ending in early November**. The score will look ~15-20% better in February–April than in November–December at the same true activity level. CSMs should be warned of this artifact during the November–December monthly run cycles.

---

## Section 2: Adoption Signal Distributions

### 2a + 2b. Per-feature applicability and usage

| Feature | % orgs applicable | % of applicable that USE it |
|---|---|---|
| iPad App | 100% (104/104) | 100% |
| Smart Stacks | 100% (104/104) | 100% (every org has ≥1 stack) |
| Sharing/quoting (≥3 events) | 100% (104/104) | 85.6% (89/104) |
| Online Catalog | 49.0% (51/104) | 68.6% (35/51) |
| Online Ordering | 29.8% (31/104) | gated by portal_orders > 0 |
| Sales Portal | 33.7% (35/104) | gated by portal_orders > 0 |
| Inventory Management | 74.0% (77/104) | 93.5% (72/77) |
| Sales Data | 82.7% (86/104) | 50.0% (43/86) |

**Observations:**
1. **iPad and Smart Stacks pass at 100%.** No org has zero logins and no org has zero smart stacks. These two sub-signals don't contribute *any* discriminating power across the portfolio. The current Adoption score formula (`features_used / features_applicable × 100`) gives every org 2 free points.
2. **Sales Data has the worst adoption-of-applicable rate: 50%.** Of the 86 orgs that have it enabled, 43 have not had a Sales Data import in 90 days. This is by far the biggest gap in the adoption matrix.
3. **Inventory adoption is very high (93.5% of applicable orgs are using it).** Of 77 orgs with any inventory imports in 180d, 72 had at least one in 90d. The 5 with stale inventory are real signal.

### 2c. Adoption breadth distribution

| Quantile | adoption % |
|---|---|
| min | 40% |
| p10 | 50% |
| p25 | 60% |
| **p50** | **66.7%** |
| p75 | 80% |
| p90 | 100% |
| max | 100% |

**Histogram:**

| Band | n |
|---|---|
| 0–19% | 0 |
| 20–39% | 0 |
| 40–59% | 22 |
| 60–79% | 54 |
| 80–99% | 7 |
| 100% | 21 |

**Observations:**
1. **No org scores below 40% adoption.** The minimum possible is 40% because iPad + Smart Stacks always pass (2 of a base 5), and most orgs trip 1–2 more. The Adoption dimension's effective range is **40–100**, not 0–100. Any V3 spot-check that treats adoption=40 as "low" should remember that 40 is the floor.
2. **The dimension is bimodal-ish:** 21 orgs at 100% + 22 in the 40–59% band, with the bulk (54) in the middle 60–79% bucket. Orgs cluster around either "everything I have I use" or "I configured stuff and never turned it on."
3. **The 22 orgs at 40–59% are dominated by Sales Data and Sales Portal not being used.** This is the clearest signal of "configured but unused" infrastructure in the portfolio.

### 2d. Sharing/quoting distribution

**90d Mixpanel events (`item_email_drafted` + `document_email_drafted`):**

| Quantile | events | quantile (orgs with any) |
|---|---|---|
| min | 0 | 1 |
| p10 | 1 | 3 |
| p25 | 7 | 15 |
| p50 | 47 | 53 |
| p75 | 135 | 141 |
| p90 | 304 | 307 |
| max | 991 | 991 |

**Histogram bands around the V3 threshold of 3:**

| Band | n |
|---|---|
| 0 | 8 |
| 1–2 | 7 |
| 3–9 | 12 |
| 10–29 | 15 |
| 30–99 | 28 |
| 100–299 | 22 |
| 300–999 | 12 |

**Threshold sweep:**

| Threshold | Orgs passing | % portfolio |
|---|---|---|
| ≥ 1 | 96 | 92.3% |
| ≥ 2 | 93 | 89.4% |
| ≥ 3 | 89 | **85.6%** ← current |
| ≥ 5 | 83 | 79.8% |
| ≥ 10 | 77 | 74.0% |
| ≥ 20 | 70 | 67.3% |
| ≥ 50 | 50 | 48.1% |

**Observations:**
1. **There IS a small natural gap between "very low" (1–9 events) and "regular use" (30+).** The 1–9 band has 19 orgs, the 30+ band has 62 orgs, and the 10–29 buffer has 15 orgs. The current threshold of 3 puts a noisy boundary in the middle of the small-volume band — orgs at 3 (just barely passing) and at 5 (also passing) are functionally indistinguishable from orgs at 1 or 2.
2. **The "real activity" floor seems to be around 10 events / 90d.** That's roughly 1 share every 9 days — a natural cadence for a single rep working a single account. Below 10, the data looks noise-shaped (probably one rep tested it once).
3. **Median for orgs with any sharing is 53 events.** A more natural threshold would be ≥10 (catches 74% of portfolio, separates "this is part of their workflow" from "someone clicked it once").

**Implications for calibration:**
- Move the sharing threshold from `≥ 3` to `≥ 10`. Effect: 12 orgs that currently "pass" sharing would no longer pass, dropping their adoption score by ~13 percentage points. Spot-check whether those 12 are actually using sharing as a workflow.

### Smart-stack distribution

| Quantile | smart_stack_count |
|---|---|
| min | 1 |
| p10 | 1 |
| p25 | 4 |
| p50 | 10 |
| p75 | 19 |
| p90 | 40 |
| max | 255 |

**Observations:**
1. **Every org has ≥ 1 smart stack** (heb has 255 — likely a config artifact). Using `count > 0` as the "uses Smart Stacks" signal is meaningless — it's a 100% pass rate.
2. **The bottom decile is at 1 stack.** Orgs with exactly 1 stack are very different from orgs with 10–20 stacks (the median band). A default "all products" stack is likely seeded automatically.
3. **A meaningful threshold would be ≥ 5 stacks**, which corresponds to roughly the 25th–30th percentile and would catch ~25 orgs that have only token usage of the feature.

**Implications for calibration:**
- The current `smart_stack_count > 0` criterion is a no-op. **Recommend either: (a) raise the bar to `count ≥ 5` (real use), or (b) drop Smart Stacks as a scored adoption signal** because it can't distinguish anyone.

---

## Section 3: Value Delivery Signal Distributions

### 3a. iPad orders (trailing 90d)

**Distribution:**

| Quantile | all 104 | with any orders (n=81) |
|---|---|---|
| min | 0 | 1 |
| p10 | 0 | 5 |
| p25 | 3 | 18 |
| p50 | 38 | 87 |
| p75 | 263 | 484 |
| p90 | 881 | 1,082 |
| max | 8,091 | 8,091 |

**Histogram around the V3 threshold of 10 (and the legacy 50):**

| Band | n |
|---|---|
| 0 | 23 |
| 1–4 | 7 |
| 5–9 | 7 |
| 10–29 | 13 |
| 30–49 | 5 |
| 50–99 | 10 |
| 100–299 | 14 |
| 300–999 | 15 |
| 1,000+ | 10 |

| Threshold | % of orgs with any iPad orders that pass |
|---|---|
| ≥ 10 (V3 current) | 82.7% (67/81) |
| ≥ 30 | 66.7% (54/81) |
| ≥ 50 | 60.5% (49/81) |

**Observations:**
1. **The current V3 threshold of 10 iPad orders is well-placed.** It separates "1 rep tested it" (1–9 orders, 14 orgs) from "real ongoing usage" (10+, 67 orgs). The histogram shows a natural shoulder around 10–30.
2. **22% of the portfolio (23 orgs) have ZERO iPad orders in 90 days.** Among these:
   - Several have configured portal/cart and use that channel instead (e.g., `ali`=0 iPad / 7,077 portal; `hh`=0 iPad / 0 portal too).
   - Of the 23 zero-iPad-order orgs, **13 also have zero portal traffic — these are the genuine "platform configured but no orders flowing" cases.**
3. **The 50-threshold the user asked about does NOT appear to be a natural break in the data.** 49 orgs are at ≥50 vs 67 at ≥10 — the loss of 18 orgs going from 10 to 50 is mostly orgs that genuinely *do* have "real" order activity (e.g., `eli`=64, `eglo`=11). Raising the threshold from 10 to 50 would penalize legitimate-but-modest order volume.

**Implications for calibration:**
- Keep the current `≥ 10` threshold for iPad orders. The legacy 50 threshold (mentioned by the user) appears to be too aggressive — it would demote orgs with real but modest activity.
- The 13 orgs with zero iPad orders AND zero portal traffic are the real value-delivery problem cases worth flagging in narrative regardless of the score.

### 3b. Portal orders (trailing 90d)

**Distribution among configured orgs (n=51):**

| Band (portal_orders_90d) | n |
|---|---|
| 0 | 16 |
| 1–9 | 0 |
| 10–99 | 1 (jc=72) |
| 100–999 | 8 |
| 1,000–9,999 | 16 |
| 10,000+ | 10 |

**The portal IS effectively binary.** Of 51 configured orgs, 35 (68.6%) have any traffic and 34 of those 35 are in the 100+ band. There is a clean cliff: either an org has zero portal traffic, or it has hundreds-to-tens-of-thousands. The single org sitting in the "10–99" range (`jc`=72) is the only data point in the gap.

**Configured-but-unused channels (16 orgs):**

| Org | tier | ARR | Configured channels |
|---|---|---|---|
| dccl | iPad+Catalog+Cart | $22,038 | catalog, ordering |
| eli | iPad+Catalog+Cart | $26,570 | catalog, ordering |
| cfg | iPad+Catalog+Cart | $21,066 | catalog, ordering |
| ah | iPad+Catalog+Cart | $18,560 | catalog, ordering |
| ml | iPad+Catalog | $17,980 | catalog |
| kii | iPad+Catalog+Cart | $16,643 | catalog, ordering |
| mah | iPad+Catalog+Cart | $16,642 | catalog, ordering |
| gc | iPad+Catalog+Cart | $16,980 | catalog, ordering |
| bp | iPad-only | $15,280 | catalog, ordering |
| mpc | iPad+Catalog+Cart | $15,282 | catalog, ordering |
| mfc | iPad+Catalog | $13,440 | catalog |
| tel | iPad+Catalog | $13,440 | catalog |
| ap | iPad+Catalog+Cart | $11,040 | catalog, ordering |
| abol | iPad-only | $8,700 | catalog |
| st | iPad+Catalog | $6,960 | catalog |
| rw | iPad+Catalog+Portal | $25,374 | catalog, sales_portal |

**Observations:**
1. **Portal is functionally binary on this portfolio.** The current `portal_orders_90d > 0` threshold is correct — there is no "low usage" middle band where calibration matters.
2. **9 of 16 unused-portal orgs are iPad+Catalog+Cart.** The Cart bundle has a systematic problem: customers buy the bundle, get configured for Cart + Catalog, and then never enable Portal traffic. **All iPad+Catalog+Cart orgs except 0 (out of 9 in MAL) are in this list.** This bundle's portal-related applicability gates fire for *every* org in the tier.
3. **`rw` is unusual:** ARR $25,374, iPad+Catalog+Portal tier, configured for catalog + sales_portal — but zero portal traffic. Yet `rw` has 2,344 iPad orders/90d, indicating a heavy iPad-orders org that's not using the portal channel they're paying for. Flag for CS — they're either using portal differently (e.g., for browsing) or they're not aware they have it.

**Implications for calibration:**
- Keep portal threshold at `> 0`. Calibration risk is low.
- The "configured but unused" pattern is concentrated in iPad+Catalog+Cart and creates a systematic value-delivery score penalty for that whole tier. Recommend surfacing this as a tier-level CS observation rather than a per-org failure.

---

## Section 4: Operational Health Baselines

### 4a. Catalog completeness

**Distribution:**

| Quantile | completeness % |
|---|---|
| min | 0.0% |
| p10 | 60.5% |
| p25 | 81.1% |
| **p50** | **95.8%** |
| p75 | 99.3% |
| p90 | 100.0% |
| max | 100.0% |

**By V3 step-ladder bands:**

| Band | Score | n | % |
|---|---|---|---|
| 0–24% | 0 | 4 | 3.8% |
| 25–49% | 20 | 5 | 4.8% |
| 50–69% | 40 | 7 | 6.7% |
| 70–84% | 65 | 13 | 12.5% |
| 85–94% | 85 | 21 | 20.2% |
| 95–100% | 100 | **54** | **51.9%** |

**Decile histogram (sanity check for clusters):**

| Decile | n |
|---|---|
| 0–10% | 2 (`krb`=0, `all`=2.5) |
| 10–20% | 1 (`tel`=19.7) |
| 20–30% | 5 |
| 30–40% | 1 |
| 40–50% | 0 |
| 50–60% | 1 |
| 60–70% | 6 |
| 70–80% | 9 |
| 80–90% | 10 |
| 90–100% | 58 |
| 100% exactly | 11 |

**Observations:**
1. **The portfolio is heavily clustered at the top.** 54 of 104 orgs are in the top band (95-100%) and would all score 100. That's almost no discrimination above 85%.
2. **There is a clear bimodal pattern:** 11 orgs at exactly 100%, then a long left tail with very few orgs in the 30–60% range (only 1 each in 30–40 and 50–60). The portfolio is mostly "either complete or in trouble" — the middle bands of the step ladder (40, 65) catch only 20 orgs combined.
3. **The 4 orgs at <25% (score 0) are:**
   - `krb` (Kaleen Rugs): 0% — 1,493 active products with no descriptions/images/pricing. Brand new org (cohort 2024) — likely incomplete onboarding.
   - `all` (Accord Lighting): 2.5% — 686 active products. Accord is contract-pricing per `contract_pricing_enabled=true`, but the spec already accounts for that — so the missing piece is descriptions or images.
   - `tel` (Tomlinson): 19.7% — and this is the same org that has `logins_90d=12` and `days_since_last_login=67`. **Cross-cutting failure signal — likely already churned.**
   - `tl` (Troy Lighting): 22.4% — 5,325 active products, the catalog is largely missing.

**Implications for calibration:**
- **The current step ladder is over-complex for the actual distribution.** With 51.9% of orgs at 100 and the next 20.2% at 85, two-thirds of the portfolio is in the top two bands. The middle bands (40, 65) carry only 20 orgs combined.
- **A simpler 3-band ladder would be more honest:** `≥ 90% → 100`, `60–89% → 60`, `< 60% → 20`. This still preserves the meaningful split between "table-stakes complete" and "real coaching opportunity" without inventing distinctions in clusters that don't exist.
- The current ladder boundary at 95% is well-placed (51.9% pass). The boundary at 85% catches 21 orgs in the next band — also reasonable. But the boundaries at 70% (only 13 orgs), 50% (only 7 orgs), and 25% (only 5 orgs) are mostly empty bands.

### 4b. Import health

| Stat | Value |
|---|---|
| Orgs with at least one import in 180d | 102 of 104 |
| Orgs with at least one feed in error on its last run | **51 (50.0%)** |

**Per-import-type error rate (`last_run_had_error`):**

| Import type | Errored / total | Error rate |
|---|---|---|
| Multifile Import | 5/5 | **100%** |
| Import File Processing | 1/1 | 100% |
| Product Image Downloads | 4/4 | 100% |
| Kit Items | 4/11 | 36.4% |
| Sales Data | 16/45 | 35.6% |
| Customers | 22/79 | 27.8% |
| Products | 22/100 | 22.0% |
| Portal Invoice Tracking Data | 1/5 | 20.0% |
| Inventory | 11/77 | 14.3% |
| Taxonomies | 1/8 | 12.5% |
| Product Stories | 5/46 | 10.9% |
| Portal Invoices | 1/35 | 2.9% |
| Images | 0/97 | 0.0% |
| Portal Orders | 0/34 | 0.0% |
| (others — Options, Territories, Contract Prices, etc.) | 0/many | 0.0% |

**Observations:**
1. **The "Multifile Import," "Import File Processing," and "Product Image Downloads" types have 100% last-run error rates.** This is suspicious — either the YAML parser regex is misclassifying these, or these are background batch processes that are *expected* to surface warnings as errors. Either way, they will systematically penalize every org that has them, regardless of operational health. **Investigate and likely exclude from scoring.**
2. **50% of orgs have at least one feed in last-error state.** The current scoring (`successful types / active types`) will penalize half the portfolio for what appears to be partly normal operational noise.
3. **Customers (27.8%), Products (22%), Sales Data (35.6%), Inventory (14.3%) are the "real" feeds** — they are the most-run feeds and the error rates here reflect genuine operational quality. A focused score that uses just these 4 types would be much cleaner.

**Implications for calibration:**
- **Exclude `Multifile Import`, `Import File Processing`, and `Product Image Downloads` from the import-health score.** These have systematic 100% error rates that almost certainly reflect a parser/classification artifact rather than real failures.
- Consider weighting the import-health score by run frequency (see §4c below) so that a Customers feed with 100 runs and an error matters more than a Sales Quotas feed with 3 runs and no error.

### 4c. Data freshness — mean vs cadence

**Cadence by import type (median runs/180d for orgs that have it):**

| Import type | n_orgs | median runs/180d | p25 | p75 |
|---|---|---|---|---|
| Multifile Import | 5 | 5,253 | 920 | 6,325 |
| Inventory | 68 | 178 | 109 | 261 |
| Customer Payment Information | 1 | 157 | – | – |
| Territories | 6 | 156 | 50 | 295 |
| Portal Invoices | 30 | 82 | 10 | 144 |
| Sales Data | 44 | 80 | 25 | 180 |
| Options | 11 | 68 | 16 | 183 |
| Products | 94 | 65 | 21 | 179 |
| Images | 95 | 52 | 19 | 115 |
| Customers | 72 | 41 | 18 | 166 |
| Portal Orders | 31 | 38 | 9 | 174 |
| Riser Prices | 2 | 14 | 13 | 14 |
| Contract Prices | 9 | 13 | 10 | 17 |
| Kit Items | 8 | 12 | 8 | 23 |
| Option Images | 14 | 10 | 6 | 13 |
| Product Stories | 34 | 8 | 5 | 39 |
| Option Groups | 3 | 6 | 4 | 6 |
| Matrix Options | 10 | 5 | 3 | 12 |
| Sales Quotas | 1 | 3 | – | – |

**Key observation: `Inventory` runs ~178x in 180d (almost daily) while `Contract Prices` runs ~13x (every two weeks). These are not comparable on the same staleness ratio.**

**Equal-weighted vs frequency-weighted freshness — illustrative for 5 orgs:**

| Org | EQUAL-weighted freshness | FREQ-weighted (by runs_90d) | Difference |
|---|---|---|---|
| cci | 80.0 | 87.4 | +7.4 |
| sc | 69.2 | 98.3 | +29.1 |
| wwjc | 100.0 | 100.0 | 0 |
| clli | 78.6 | 98.6 | +20.0 |
| **clm** | **88.9** | **16.3** | **-72.6** |

**Observations:**
1. **The Equal-weighted vs Frequency-weighted scores can differ by tens of points in either direction.** For `clm` the EQUAL average is 88.9 (looks healthy) but the frequency-weighted average is 16.3 (looks broken) because `clm` has a `Multifile Import` feed with 5,253 runs that is 28 days stale — heavily weighted by runs_90d, this drags the score down. For `sc` and `clli`, the equal average is dragged DOWN by low-frequency feeds (Matrix Options, Option Images, Product Stories) that are stale on their 30-60-day cadence — but those feeds are barely run anyway, so penalizing the score equally with critical daily Inventory feeds overstates the operational issue.
2. **The "initial-load carve-out" rule (§4.3) likely won't catch the issue** because it only applies to feeds with <5 runs total. The bigger issue is *low-frequency* feeds (5–20 runs) that legitimately fire monthly or quarterly being scored on the same staleness scale as daily feeds.
3. **The 1-day-floor on the gap denominator hides the problem.** For Inventory at clli (4,203 runs / 180d = ~24x/day mean gap of 0.04 days), the floor pegs gap to 1.0d. So a 4-hour-late Inventory feed still scores 100 because gap is artificially raised to 1.0d. This is fine for that direction — but it means staleness ratios for very-frequent feeds are systematically favorable.

**Mean vs median gap discrepancy (cited in user's question):**

We confirmed the cached imports table only has `first_run_at` / `last_run_at` and run counts — not the actual gap distribution. From the per-feed data we can see that a feed with 1,075 Inventory runs in 180 days starting on 2025-11-13 has a *mean* gap of 0.17 days. If the actual cadence pattern is "20 imports in the first day during initial load, then daily runs after that," the mean would be biased downward by the burst — but with 1,075 runs the burst contribution is washed out. **For high-volume feeds, mean ≈ median.** The mean-vs-median gap problem only matters for low-volume feeds (5-20 runs in 180d) where a single front-loaded burst can pull the mean down by 50%+ — and those are exactly the feeds where you have the least information to begin with.

**Implications for calibration:**
- **Weight the freshness score by run frequency** (or at least by `log(run_count_90d)`). The current equal-average treats a once-quarterly Contract Prices feed and a daily Inventory feed as equally important — they are not. The `clm` org example above shows that an equal-weighted score can entirely miss a critical operational failure.
- Consider a **two-tier freshness check:** (a) "critical feeds" (Inventory, Products, Customers, Sales Data) scored individually with strict staleness; (b) "secondary feeds" (Contract Prices, Matrix Options, Option Images) scored more leniently or excluded.
- The 1-day gap floor is fine — it prevents bursty initial-load feeds from dominating. But document that high-frequency feeds will systematically score 100 unless they go entirely silent.

---

## Section 5: Retention/Outcome Signals

### 5a. Plausible churn — older cohorts with no logins

Strict criterion (`cohort_year ≤ 2024 AND logins_90d = 0`): **0 orgs.** Every paying MAL org logged in within the past 90 days.

Looser "cooling off" criterion (`logins_90d ≤ 50 AND days_since_last_login ≥ 14`): **1 org.**

| Org | tier | ARR | cohort | logins_90d | days since last |
|---|---|---|---|---|---|
| **tel** (Tomlinson Companies) | iPad+Catalog | $13,440 | 2015 | 12 | 67 |

`tel` is the only paying MAL org that exhibits a clear cooling-off pattern. It was last seen on 2026-03-06. It also has 19.7% catalog completeness (Section 4) — cross-cutting failure. Almost certainly already churned in fact if not yet in the system.

### 5b. High-ARR + low engagement

`ARR ≥ $10,000 AND logins_90d < 50`: **2 orgs.**

| Org | tier | ARR | logins_90d | days since last |
|---|---|---|---|---|
| tel | iPad+Catalog | $13,440 | 12 | 67 |
| ol | iPad-only | $13,380 | 40 | 0 |

`ol` (Oly Studio) is interesting — recent activity (last login today), modest 90d total. cohort_year=2025. This is a brand-new org that may still be in onboarding. The `skipped_new_orgs.csv` may already exclude it.

`ARR ≥ $20,000 AND logins_90d < 200`: **0 orgs.** Every $20k+ ARR account has substantial engagement. This is a positive signal: the high-ARR portfolio is not silently broken anywhere.

### 5c. Subscriptions table contents

| Stat | Value |
|---|---|
| Total subscription rows in MAL orgs | 279 |
| `start_date` range | 2025-05-01 → 2026-02-11 |
| Rows with `end_date` populated | **0** |
| Status: 'active' | 272 |
| Status: 'canceled' | 7 |
| Orgs with at least one 'canceled' row | 3 |

**Orgs with any 'canceled' subscription rows:**

| Org | non-canceled rows | tier | logins_90d |
|---|---|---|---|
| **abol** | 1 | iPad-only | 67 |
| **hmjc** | 0 | iPad-only | 10 |
| wwjc | 5 | Full | 2,907 |

**Observations:**
1. **The subscriptions table is essentially useless for retention/churn detection** as called out by the V3 spec. 272 of 279 rows have a backfilled start_date in late August 2025 and no end_date.
2. **`hmjc` has zero non-canceled subscription rows** — this is the closest thing to a churn signal in the database. `hmjc` also shows the engagement cliff in §1d (57 logins in Oct 2025 → 7 in Feb 2026 → 1 in May 2026). **`hmjc` is almost certainly an in-progress churn that is still in the MAL because the MAL hasn't been refreshed.**
3. `abol` (Americas Backyards) and `wwjc` (Wildwood/Chelsea House) both have mixed canceled+active rows. `wwjc` has 5 active subscription rows alongside the canceled ones — likely a multi-product subscription where one line was canceled, not a churned account (it has 2,907 logins/90d, which is healthy).

### 5d. Engagement by cohort year

| Cohort bucket | n | median logins_90d | p25 | p75 |
|---|---|---|---|---|
| pre-2020 | 55 | 1,317 | 338 | 2,351 |
| 2020–2022 | 14 | 1,665 | 540 | 2,371 |
| 2023–2024 | 27 | 598 | 267 | 968 |
| 2025 | 8 | 563 | 235 | 1,686 |

**Observations:**
1. **Older cohorts are MORE engaged on a per-org basis, not less.** Median logins for pre-2020 cohort = 1,317 vs 2023–2024 median = 598. This is the opposite of what you might expect if customers churned downward over time.
2. The most likely explanation: **survivorship bias.** Older cohorts are pre-filtered by churn — only the engaged old customers are still in the MAL. Newer cohorts include both committed users and accounts that haven't fully ramped yet.
3. **2014 is an outlier (n=4, median=4,291 logins)** because two of the four orgs are jyc and sccon, both Full-bundle high-volume accounts. Small-n cohorts are dominated by 1–2 outliers.

**Implications for calibration:**
- The "cohort_year" field in the MAL is not directly useful as a scoring input. It is, however, useful as a stratification variable: when validating the model in §9, we should check that newer cohorts (where the lower median is structurally lower) are not systematically scored as at-risk because of their cohort age.

---

## Section 6: Bundle-Stratified Analysis

### 6a. Median engagement score by tier (using current V3 formula)

| Tier | n | median engagement score | p25 | p75 |
|---|---|---|---|---|
| iPad-only | 56 | **75.0** | 68.3 | 84.3 |
| iPad+Catalog | 5 | 53.3 | 46.7 | 77.7 |
| iPad+Catalog+Cart | 9 | 69.3 | 65.0 | 69.3 |
| iPad+Catalog+Portal | 14 | **84.3** | 71.4 | 92.6 |
| Full | 20 | 69.3 | 62.7 | 69.3 |

**Observation:** Despite Full-tier orgs having the *highest* raw login counts (Section 1a: median 2,000), they score *lower* on the engagement composite (median 69.3) than the iPad+Catalog+Portal tier (median 84.3). The gap is driven entirely by the Active User Ratio sub-signal: Full-tier median ratio = 0.03 because of the inflated denominator (Section 1b).

### 6b. Value-delivery channel mechanics — product-mix artifact

| Tier | n | median # channels applicable | median # channels used | median %-used |
|---|---|---|---|---|
| iPad-only | 56 | 3 | 2 | 66.7% |
| iPad+Catalog | 5 | 3 | 1 | 33.3% |
| iPad+Catalog+Cart | 9 | 5 | 3 | 60.0% |
| iPad+Catalog+Portal | 14 | 5 | 5 | **100%** |
| Full | 20 | 6 | 6 | **100%** |

**Observations:**
1. **The §9 warning about pooled correlations is concretely visible here.** Full-tier orgs get 6 applicable value-delivery channels (vs 3 for iPad-only), and most of them are getting *all 6 credited*. Median value-delivery score for Full = 100, for iPad-only = 66.7. **This is a product-mix artifact, not a value-delivery quality difference.**
2. The portal channel fires 3 times for Full orgs (Online Catalog + Online Ordering + Sales Portal all use `portal_orders > 0` as the same usage signal) — so a Full-tier org with portal traffic gets 3 free channel-credits relative to an iPad-only org. This is by design in the spec, but it inflates the Full-tier value-delivery score in a way that pooled cross-bundle correlation can't see.

### 6c. logins_90d — pooled vs by-bundle

| Population | n | median | p25 | p75 |
|---|---|---|---|---|
| **POOLED** | 104 | 927 | 314 | 2,100 |
| iPad-only | 56 | 473 | 225 | 1,114 |
| iPad+Catalog | 5 | 116 | 12 | 1,626 |
| iPad+Catalog+Cart | 9 | 1,062 | 551 | 1,352 |
| iPad+Catalog+Portal | 14 | 2,521 | 2,030 | 3,995 |
| Full | 20 | 2,000 | 1,433 | 2,929 |

**Observation — concrete demonstration of the pooled-correlation problem:**

If we ran a naive correlation `logins_90d ~ ARR` across the pooled portfolio, we would find a strong positive relationship (Cart/Portal/Full bundles have BOTH higher ARR AND higher logins). But within iPad-only specifically (n=56, the largest tier), the same correlation would be much weaker — because the entire range from low-end ($4,392, `tl`) to high-end ($25,200, `prog`) is at similar median engagement (`tl`=219 logins, `prog`=291 logins, both modest).

**Median ARR by tier (for context):**

- iPad-only median ARR ~$9,000 (light) — median 473 logins
- iPad+Catalog+Portal median ARR ~$25,000 (heavy) — median 2,521 logins
- Full median ARR ~$26,000 (heaviest) — median 2,000 logins

The "ARR causes logins" story is mostly "Full-bundle orgs have more logins because they have more reps and more product mix, not because they pay more for the same activity." Any weighting scheme derived from pooled correlation will conflate these.

---

## Summary: 5 Things the Data Suggests We Should Change

Ordered by impact (highest first) and tied to specific empirical findings.

### 1. Replace the `enabled_users` denominator for Full and Cart bundles, OR change the staleness flag rule

**Finding:** 13 of 20 Full-tier orgs have `enabled_users > 1000`, with median 1,366 (max 20,422 for `wwjc`). The "stale" flag fires only when raw ratio > 100% — catching 2 orgs. The other 13 are silently scored as "1–24% active" (= 20 pts) when their internal-user activity is structurally normal. The current Engagement composite penalizes the entire Full tier by ~15-20 points for a `org_users` table-design issue.

**Concrete change:** When `enabled_users > 500` AND tier IN ('Full', 'iPad+Catalog+Cart'), automatically use the `active_users_365d` fallback (already specified as a manual fallback) for the denominator. Set `denominator_quality = stale` and explain in narrative.

### 2. Drop the "Last Login Recency" sub-signal or replace it with a 30d/180d ratio

**Finding:** 99% of orgs (103 of 104) had a login within the past 7 days → recency score = 100 for nearly everyone. The sub-signal contributes essentially zero discrimination. Meanwhile, 3 orgs (`kl`, `prog`, `afx`) show a clear cooling-off pattern (logins_30d < 10% of logins_180d) that the current recency check entirely misses.

**Concrete change:** Replace `Last Login Recency` with `Activity Decay Score = (logins_30d × 6) / max(logins_180d, 1)`, banded as: ratio ≥ 0.7 → 100, 0.4–0.7 → 60, 0.2–0.4 → 30, < 0.2 → 0. This catches the actually-cooling-off orgs that the current model can't see.

### 3. Move the Sharing/quoting threshold from ≥ 3 to ≥ 10 events

**Finding:** The 1–9 events band has 19 orgs and the 30+ events band has 62 orgs, with only 15 in the 10–29 buffer band. Current threshold of 3 sits in the noise band — orgs at exactly 3 events are functionally indistinguishable from orgs at 1. Median for orgs with any sharing is 53 events. A threshold at 10 catches 74% of the portfolio (vs 86% at 3) and represents a clean separation between "one-off test" and "regular workflow."

**Concrete change:** Update the sharing pass threshold in §3 (Value Delivery) and §2 (Adoption gating) from `mp_sharing_events_90d >= 3` to `>= 10`.

### 4. Frequency-weight the Data Freshness sub-signal, and exclude broken import types

**Finding:** Equal-weighted vs frequency-weighted freshness scores can differ by **±70 points** on individual orgs (`clm` shifts from 88.9 → 16.3; `sc` shifts from 69.2 → 98.3). The mismatch is severe enough that the current "average across all active types" formula is producing actively misleading scores in both directions. Separately, three import types have 100% last-run error rates across all orgs (`Multifile Import`, `Import File Processing`, `Product Image Downloads`) — strong evidence of a parser/classification bug. Including them inflates the import-health failure rate to 50% of the portfolio.

**Concrete change:** (a) Weight each import type's freshness contribution by `log(1 + run_count_90d)` so high-frequency feeds dominate. (b) Hard-exclude `Multifile Import`, `Import File Processing`, and `Product Image Downloads` from both freshness and import-health scoring pending investigation of why they always last-error.

### 5. Simplify the Catalog Completeness step ladder

**Finding:** 51.9% of the portfolio scores in the top band (95-100%) and 20.2% in the next band (85-94%). The middle bands of the current 6-tier ladder (40, 65) catch only 20 orgs combined. The bottom band (score 0) catches 4 orgs that are also dysfunctional on other dimensions. The ladder is too granular for the actual distribution.

**Concrete change:** Reduce to a 3-band ladder: `≥ 90% → 100`, `60–89% → 60`, `< 60% → 20`. This produces the same top-end / bottom-end splits the current ladder produces while removing pseudo-precision in the middle of an empty bucket.

---

## Honest "we cannot answer this from the data" notes

- **No 12-month seasonal baseline exists.** `login_events` only has 18 months of history. Any seasonality calibration requires waiting for V3 to accumulate its own monthly history (V3.1 trigger condition, per §10).
- **The subscriptions table cannot validate retention.** All `start_date` values are backfilled to mid-2025 and no `end_date` is populated. Validation per §9 cannot use this table; it must use either the MAL's monthly snapshots or a separate churn-event source.
- **iPad+Catalog tier (n=5) is too small for tier-stratified band calibration.** Any per-tier finding for this tier is one-org-changes-everything. Treat it as a special-case reporting tier and exclude it from per-tier band calibration.
- **The portal_orders count of 1 in the cached `pg_org_config.csv` data is an artifact of the COALESCE default in the original V3 query (`COUNT(*)` over a LEFT JOIN with no match returns 1 in some flavors).** The actual real-portal-traffic floor is 72 (single org `jc`). Any analysis built on the cached data needs to treat the portal_orders threshold as `> 1` rather than `> 0`. The live query confirms that 16 of 51 configured-portal orgs genuinely have zero traffic.
