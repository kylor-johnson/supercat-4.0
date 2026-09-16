# Health V3.0 — Forensic Spot-Check, 10 Clients

**Run:** 2026-05-11
**Source CSV:** `Health V3/runs/2026-05-11/client_health_scores_2026-05-11.csv`
**Cache used:** `Health V3/cache/2026-05-11/` (the exact Postgres + BigQuery extracts the operator scored against)
**Operator under review:** `Health V3/health_operator_v3.py`
**Purpose:** Walk every score back to its raw inputs, interpret the *why*, and surface calibration questions for CEO review.

> All 10 requested orgs were present in the CSV — no substitutions required.

---

## sc — Gabriella White

- Bundle: iPad+Catalog+Portal
- Cohort year: 2013
- ARR: $24,936.00
- **Composite: 90.9 (Thriving)**
- Kylor's blind classification: Green AND non-ghost-active (dual-purposed in the spread)
- Match? **Yes.** Top-quartile engagement (15.7K logins, 86% active ratio), every applicable surface lit up, contract-pricing carveout firing cleanly. Catalog drag on ops is real but cosmetic.

### Engagement: 94.0

| Raw input | Value |
|---|---|
| logins_90d | 15,719 |
| active_users_90d | 124 |
| enabled_users (internal-domain-filtered) | 144 |
| last_login_at | 2026-05-11 23:01:11 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.861 |
| capped ratio | 0.861 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 15,719 → ≥ 3,000 band → **100**
- Active user ratio: 86.1% → 0.75 ≤ x < 0.90 band → **82**
- Recency: 0 days → ≤ 7 band → **100**
- Average: (100 + 82 + 100) / 3 = **94.0** ✓

**Interpretive narrative — the WHY:** Engagement is at the structural ceiling — 15,719 logins from 124 of 144 internal users in 90 days is the kind of "everyone, every day" pattern that the LOGIN_BANDS top tier was designed to recognize, and the 86% active-user ratio rules out the "one power user inflating the count" failure mode. The single point of give in the dimension is the 82 ratio sub-score: at 86% they sit *just* below the 90% ceiling, which is the right calibration outcome — a 14-point gap on user breadth is signal, not noise, and the math correctly leaves room to reward an org that hits true universal coverage.

### Adoption: 100.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 15,719 logins_90d |
| Smart Stacks | Yes | Yes | 4 smart_stacks rows |
| Sharing / quoting | Yes | Yes | 402 mp_sharing_events_90d (40 item + 362 doc) |
| eCat Online Catalog | Yes (`enable_online_catalog=true`) | Yes | flag-only gate |
| Online Ordering | No (`enable_online_ordering=false`) | — | not applicable |
| Sales Portal | Yes (`enable_sales_portal=true`) | Yes | 3,940 portal_orders_90d |
| Inventory Management | Yes (Inventory imports active 180d) | Yes | 179 Inventory runs in 90d |
| Sales Data | Yes (`enable_sales_data=true`) | Yes | 160 Sales Data runs in 90d |

**Interpretive narrative — the WHY:** sc is a configuration-saturated, usage-saturated account: every one of the 7 applicable features fired the binary "used in 90d" gate, including the two that should be hardest to fake (Sharing at 402 Mixpanel events and Sales Portal at 3,940 portal orders). The 7-not-8 denominator is the iPad+Catalog+Portal bundle correctly *not* counting Online Ordering — they don't have B2B Cart, so absence is honest. Adoption can't tell you anything more useful for this org than "yes, they use what they bought."

### Value Delivery: 100.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 8,092 | Yes |
| Sharing activity | Yes | ≥ 3 | 402 | Yes |
| Online catalog active | Yes | portal > 0 | 3,940 | Yes |
| Portal ordering | No (eoo=false) | — | — | n/a |
| Sales Portal engagement | Yes | portal > 0 | 3,940 | Yes |
| Inventory data flowing | Yes | inv runs_90d > 0 | 179 | Yes |

**Interpretive narrative — the WHY:** Value delivery is saturated at 100 — and the *actuals* under the saturation are what justify it: 8,092 iPad-submitted orders against a ≥10 threshold (the README itself calls these "intentionally low for V1") and 402 sharing events against a ≥3 threshold. Even if the calibration tightened by an order of magnitude in V3.1 (≥100 iPad orders, ≥30 sharing events), sc would still hit 100. There is no question this org is converting product touch into business outcome.

### Operational Health: 69.7

**Sub-signal detail:**

- **Catalog:** 11,617 of 18,852 active products complete = 62%. Step ladder: 0.50 ≤ pct < 0.70 → **40**. Forensic breakdown via Postgres: 0 missing description, 0 failing price (`contract_pricing_enabled=true` satisfies the price clause for all 18,852 products), 7,235 (38%) missing image. The contract-pricing carveout is functioning correctly — the catalog gap is entirely `image_exists=false` on roughly 4 in 10 products.
- **Import Health:** 13 active import types in trailing 180d, all 13 with no error on most recent run → **100**.
- **Data Freshness:** 12 measurable feed types (Products has only 1 run in 180d, below the 3-run minimum, omitted). Mean staleness scores across types: Customers/Inventory/Sales Data/Taxonomies/Portal Invoices/Options/Territories/Images all daily-cadence and current → 100; Kit Items slightly behind cadence (16.9d gap, 22d since last) → 80; Matrix Options stale (34d gap, 76d since last) → 50; Option Images, Portal Orders, Product Stories all > 4× their cadence → 0. Average: **69.2**.
- Composite: (40 + 100 + 69.2) / 3 = **69.7** ✓

**Interpretive narrative — the WHY:** Operational health lands at 69.7 because the catalog sub-signal is dragging — 38% of active products have `image_exists=false`, a real content-coverage issue (not a carveout bug; contract pricing is satisfying the price clause for every product, and every product has a long_description). That sole 40 on catalog pulls a 100-rated import stack and a 69 freshness average down by roughly 30 points. Freshness itself is a tale of two cadences — eight production feeds run daily-or-faster and score 100, while three side feeds (Option Images, Portal Orders, Product Stories) have gone quiet for months and the algorithm penalizes them against their own historical cadence, exactly as designed.

### Composite analysis

**The story in one paragraph:** sc is a textbook Thriving — Engagement, Adoption, and Value Delivery are all at or near saturation, and the only headwind is a catalog with ~7,200 imageless products. The composite (90.9) is being pulled down ~6 points by the operational dimension, but even that is "polish opportunity," not "risk." The biggest opportunity is reaching back into the catalog to drive image coverage, which would lift ops from 69.7 to ~89 and push the composite into the mid-90s — a CSM motion, not a save motion.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: **true** — 2 open conversations tagged `l3 - engineering intervention` (gabriellawhite.com)
- ghost_account: false

> The support fire is meaningful: a $24.9K-ARR account in Thriving with two open L3 escalations is the support-modifier doing its job — calling out that the *experience* is shaky even when the *usage* looks great.

---

## ufi — Universal Furniture

- Bundle: iPad+Catalog+Portal
- Cohort year: 2011
- ARR: $25,475.04
- **Composite: 97.8 (Thriving)**
- Kylor's blind classification: Green AND price-level pricing carveout candidate
- Match? **Yes.** Highest composite in the spot-check set. Both carveout checks (price-level not contract — see below) verified.

### Engagement: 94.0

| Raw input | Value |
|---|---|
| logins_90d | 6,957 |
| active_users_90d | 76 |
| enabled_users | 95 |
| last_login_at | 2026-05-11 23:03:08 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.800 |
| capped ratio | 0.800 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 6,957 → ≥ 3,000 → **100**
- Active user ratio: 80% → 0.75 ≤ x < 0.90 → **82**
- Recency: 0 days → **100**
- Average: (100 + 82 + 100) / 3 = **94.0** ✓

**Interpretive narrative — the WHY:** Engagement is structurally identical to sc — top-tier logins and recency, with the only point of give being the 80% active-user ratio (76 of 95 internal users) putting them in the 82-point band rather than the 100-point ≥ 90% band. For a 15-year-old account with 95 enabled internal users, 80% active is healthy daily-driver behavior — the dimension is correctly pricing in a small breadth gap that a 100/100 would mask.

### Adoption: 100.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 6,957 logins_90d |
| Smart Stacks | Yes | Yes | 45 smart_stacks rows (most in spot-check set) |
| Sharing / quoting | Yes | Yes | 591 mp_sharing_events_90d (477 item + 114 doc) |
| eCat Online Catalog | Yes (eoc=true) | Yes | flag-only gate |
| Online Ordering | No (eoo=false) | — | not applicable |
| Sales Portal | Yes (esp=true) | Yes | 15,311 portal_orders_90d |
| Inventory Management | **No** (no Inventory import type in 180d history) | — | not applicable |
| Sales Data | Yes (esd=true) | Yes | 96 Sales Data runs in 90d |

**Interpretive narrative — the WHY:** All 6 applicable features are in active use, and the 6-feature denominator is the important narrative point: the Inventory feature is correctly *not* counted as applicable because ufi has zero Inventory import history in the trailing 180d. That's exactly the spec's design — don't penalize an org for not using a feature they've never had set up — but it also means a 100 here is over 6 surfaces, not 8. Smart Stacks at 45 entries is the highest count in the spot-check, suggesting ufi has invested in catalog organization beyond what most accounts do.

### Value Delivery: 100.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 610 | Yes |
| Sharing activity | Yes | ≥ 3 | 591 | Yes |
| Online catalog active | Yes | portal > 0 | 15,311 | Yes |
| Portal ordering | No (eoo=false) | — | — | n/a |
| Sales Portal engagement | Yes | portal > 0 | 15,311 | Yes |
| Inventory data flowing | No (Inventory not active) | — | — | n/a |

**Interpretive narrative — the WHY:** 4 of 4 applicable channels achieved. Underneath the saturation: 610 iPad orders (60× the threshold), 591 sharing events (197× the threshold), and 15,311 portal orders (the second-highest in the spot-check, behind only kll). The narrower 4-channel denominator vs. sc/gh's 5–6 reflects the same bundle and config reality — ufi runs a Catalog + Sales Portal model, no B2B Cart, no inventory pipeline.

### Operational Health: 97.2

**Sub-signal detail:**

- **Catalog:** 2,201 of 2,201 active products complete = 100%. Step ladder → **100**. Forensic breakdown: 0 missing description, 0 missing image, 0 failing price. ufi is **not** a contract-pricing org (`contract_pricing_enabled=false`); the price-level carveout (`prices_json` populated for all 2,201 products) is what satisfies the price clause. This is the cleanest catalog in the spot-check set and *the* exemplar of the price-level carveout working.
- **Import Health:** 7 active import types, 0 errors → **100**.
- **Data Freshness:** 6 measurable feed types (Territories has 1 run, below the 3-run minimum). Customers, Portal Invoices, Portal Orders, Products, Sales Data all current against their own cadence → 100; Images slightly behind (1.7d gap, 3d since last → ratio 1.75 → 50). Average: **91.7**.
- Composite: (100 + 100 + 91.7) / 3 = **97.2** ✓

**Interpretive narrative — the WHY:** Operational health is the highest in the spot-check at 97.2, and the structure is the inverse of sc's: catalog is perfect (100% — every priced product has `prices_json` populated under the price-level carveout, every product has `image_exists=true`, every product has a description), imports are perfect, and freshness is held back only by the Images feed running on a ~1.7-day cadence with its most recent run 3 days ago. This is the operationally tightest account in the spot-check — and validates that the price-level pricing clause in `load_pg_catalog` is fully operational for a non-contract org.

### Composite analysis

**The story in one paragraph:** ufi is the highest-scoring account in the spot-check and the cleanest validation of the price-level pricing carveout — a non-contract, non-$0-net_price org that ships 100% catalog completeness because `prices_json` is populated. The composite (97.8) is the average of two 94s (engagement) and two near-100s (adoption + value + ops), and there is no actionable risk in the data. The single open L3 support escalation is the only friction visible — and even that is exactly the case the support modifier exists to surface.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: **true** — 1 open `l3 - engineering intervention` (universalfurniture.com)
- ghost_account: false

---

## gh — Gabby

- Bundle: Full (Cart+Portal)
- Cohort year: 2013
- ARR: $24,336.00
- **Composite: 85.8 (Thriving)**
- Kylor's blind classification: Green
- Match? **Yes**, but with the same denominator-quality wrinkle as the readiness review's `denominator_quality=stale` candidates — gh's enabled_users count is implausibly large.

### Engagement: 66.7

| Raw input | Value |
|---|---|
| logins_90d | 6,246 |
| active_users_90d | 56 |
| enabled_users | **7,911** |
| last_login_at | 2026-05-11 23:12:02 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.00708 |
| capped ratio | 0.00708 |
| denominator_quality | null *(but should arguably fire)* |

**Sub-signal scoring:**
- Login count: 6,246 → ≥ 3,000 → **100**
- Active user ratio: 0.71% → **below the 0.01 threshold** → **0**
- Recency: 0 days → **100**
- Average: (100 + 0 + 100) / 3 = **66.7** ✓

**Interpretive narrative — the WHY:** Engagement is the only dimension drag for gh, and it is being driven entirely by a denominator problem the spec doesn't currently catch. The enabled_users count is 7,911 — far larger than gh's actual rep base — which forces the ratio sub-score off a cliff: 0.71% falls *just below* the 1% threshold for the 20-point band and lands at 0. The `denominator_quality=stale` flag is designed for the inverse case (raw ratio > 100% means denominator is too small), not this case (raw ratio is implausibly small because denominator includes customer-portal accounts). The 6,246 logins and same-day recency strongly suggest the org is engaged — the score is artificially low and the model isn't surfacing why.

### Adoption: 100.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 6,246 logins |
| Smart Stacks | Yes | Yes | 2 smart_stacks |
| Sharing / quoting | Yes | Yes | 814 mp_sharing_events_90d (34 + 780) |
| eCat Online Catalog | Yes (eoc=true) | Yes | flag-only |
| Online Ordering | Yes (eoo=true) | Yes | 6,812 portal_orders_90d |
| Sales Portal | Yes (esp=true) | Yes | 6,812 portal_orders_90d |
| Inventory Management | Yes (Inventory active) | Yes | 179 runs in 90d |
| Sales Data | Yes (esd=true) | Yes | 160 runs in 90d |

**Interpretive narrative — the WHY:** Full bundle, full saturation — every one of the 8 applicable features fires its binary gate. Sharing is unusually strong at 814 events (780 of them document-email-drafted, which is the quoting flow), so gh is using the platform for value-bearing communications, not just browsing. The 8-feature denominator is the largest in the spot-check, which is also the structural reason gh's Adoption can't be anything other than 100 if every gate fires — Full-bundle orgs are *built* to top out here.

### Value Delivery: 100.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 2,550 | Yes |
| Sharing activity | Yes | ≥ 3 | 814 | Yes |
| Online catalog active | Yes | portal > 0 | 6,812 | Yes |
| Portal ordering | Yes | portal > 0 | 6,812 | Yes |
| Sales Portal engagement | Yes | portal > 0 | 6,812 | Yes |
| Inventory data flowing | Yes | inv > 0 | 179 | Yes |

**Interpretive narrative — the WHY:** 6 of 6, and the actuals are emphatic — 2,550 iPad orders (255× the threshold), 6,812 portal orders, 780 document drafts. gh is one of the highest-output accounts in the portfolio by raw activity. The three portal-fed channels (online catalog, portal ordering, sales portal) all derive from the same `portal_orders_90d > 0` observation, which is intentional per the spec — they're three different config gates, all satisfied, so all three score.

### Operational Health: 76.7

**Sub-signal detail:**

- **Catalog:** 4,412 of 7,397 active = 60%. Step ladder → **40** (0.50 ≤ x < 0.70). Forensic breakdown: 0 missing description, 0 failing price (contract pricing satisfies the price clause), 2,985 (40.4%) missing image. Same shape as sc: a catalog with full text and pricing coverage but ~40% image gaps.
- **Import Health:** 14 active import types, 0 errors → **100**.
- **Data Freshness:** 12 measurable feed types. Customers, Images, Inventory, Kit Items, Options, Portal Invoices, Portal Orders, Sales Data, Taxonomies, Territories all current → 100; Product Stories slightly behind cadence (12d gap, 14d since last → ratio 1.17 → 80); Option Images stale (4.1d gap, 18d since last → ratio 4.39 → 0). Average: **90.0**.
- Composite: (40 + 100 + 90) / 3 = **76.7** ✓

**Interpretive narrative — the WHY:** Same shape as sc — a 40 on catalog (image-coverage drag, not carveout failure) sitting next to a 100 on imports and a 90 on freshness. Contract pricing is satisfying the price check on all 7,397 products; the catalog sub-score is being held at 40 because 2,985 products lack `image_exists=true`. Freshness is held back almost entirely by the Option Images feed having gone quiet for 18 days against a 4-day cadence, plus a slight Product Stories drift — both side-pipelines, neither operationally critical.

### Composite analysis

**The story in one paragraph:** gh would be a 90-something Thriving like sc and ufi if not for the inflated `enabled_users` denominator dragging engagement to 67. The model is being technically correct (the math is exactly as spec'd) but interpretively wrong: a 6,246-login, 814-sharing-event, 2,550-iPad-order account is not engagement-impaired. The biggest opportunity here is a denominator audit — pruning customer-portal accounts from the `org_users` count — which would likely move ratio sub-score from 0 to the 45–65 range and lift the composite into the low 90s. Secondary opportunity is the same image-coverage gap as sc.

**Flags worth surfacing:**
- denominator_quality: null *(model didn't fire — the existing logic only catches > 100%, not implausibly-low cases)*
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false

---

## kll — Kuzco Lighting Inc.

- Bundle: Full (Cart+Portal)
- Cohort year: 2022
- ARR: $26,780.04
- **Composite: 80.2 (Thriving)**
- Kylor's blind classification: Non-ghost active AND price-level pricing carveout candidate
- Match? **Yes.** Healthy across all four dimensions, with the price-level carveout doing exactly what it's supposed to.

### Engagement: 69.3

| Raw input | Value |
|---|---|
| logins_90d | 1,761 |
| active_users_90d | 60 |
| enabled_users | 933 |
| last_login_at | 2026-05-11 22:32:47 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.0643 |
| capped ratio | 0.0643 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 1,761 → ≥ 1,000 → **88**
- Active user ratio: 6.43% → 0.01 ≤ x < 0.25 → **20**
- Recency: 0 days → **100**
- Average: (88 + 20 + 100) / 3 = **69.3** ✓

**Interpretive narrative — the WHY:** Engagement is at the lower end of "healthy" because the model is seeing the same pattern it does at gh and fsf — a strong login count (1,761, well into the 88-point band) and same-day recency, but a low active-user ratio (60 of 933 = 6%). The 933-enabled-users figure for a lighting wholesaler is plausible (Kuzco runs a large dealer network), so the ratio cliff at 1% may genuinely reflect that only a fraction of provisioned reps are daily-active — but the cliff itself is steep: at 6% ratio they hit the 20-point band, which would also be the score at 1.1% or 24%. The dimension is correctly flagging "deep but not broad," and the broad-base question is the right one for Kuzco to answer in V3.1 calibration.

### Adoption: 87.5

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 1,761 logins |
| Smart Stacks | Yes | Yes | 20 smart_stacks |
| Sharing / quoting | Yes | Yes | 44 mp_sharing_events_90d (18 + 26) |
| eCat Online Catalog | Yes | Yes | flag-only |
| Online Ordering | Yes | Yes | 31,794 portal_orders_90d |
| Sales Portal | Yes | Yes | 31,794 portal_orders_90d |
| Inventory Management | Yes | Yes | 75 runs in 90d |
| Sales Data | **Yes** (esd=true) | **No** | no Sales Data import type in 180d history |

**Interpretive narrative — the WHY:** 7 of 8 applicable features — and the one gap is exactly what the narrative says: Sales Data is enabled on the org but has never run. With 31,794 portal orders, 75 inventory runs, and active iPad/Smart Stacks/sharing, kll is using every commerce-facing surface; the gap is purely the reporting feed. Worth surfacing to CSM as "is Sales Data actually wanted, or should it be disabled in the org config?" — that's a 1-point swing on adoption and clarifies the bundle posture.

### Value Delivery: 83.3

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | **9** | **No** |
| Sharing activity | Yes | ≥ 3 | 44 | Yes |
| Online catalog active | Yes | portal > 0 | 31,794 | Yes |
| Portal ordering | Yes | portal > 0 | 31,794 | Yes |
| Sales Portal engagement | Yes | portal > 0 | 31,794 | Yes |
| Inventory data flowing | Yes | inv > 0 | 75 | Yes |

**Interpretive narrative — the WHY:** This is the most calibration-sensitive cell in the entire spot-check: kll has **9** iPad-submitted orders in 90 days, exactly one below the ≥10 threshold. They lose a point on iPad order volume and the score drops from 100 to 83.3. But the same org submitted 31,794 portal orders in the same window — the iPad-channel question for kll is real (their reps aren't using the iPad app to *submit*, they're using the portal), but the dimension score doesn't communicate the asymmetry. The 5 of 6 narrative reads like an account with mild gaps; the underlying reality is "iPad-as-order-entry is essentially zero, everything goes through the portal."

### Operational Health: 80.9

**Sub-signal detail:**

- **Catalog:** 6,084 of 6,268 active = 97%. Step ladder → **100** (≥ 95%). Forensic breakdown: 7 missing description, 184 missing image (3%), 0 failing price. kll is **not** contract-pricing (`contract_pricing_enabled=false`); the 0 failing-price count is the price-level carveout (`prices_json` populated) doing its job. Exemplar of the carveout working for a price-level org.
- **Import Health:** 7 active import types. Most recent run for Customers had an error → 6 of 7 healthy → **85.7**.
- **Data Freshness:** 7 measurable feed types (no skips — all 7 have ≥ 3 runs). Customers, Inventory, Portal Invoices, Portal Orders all current → 100; Images stale (1.0d gap floored, 122d since last — likely an "initial-load then abandoned" pattern that the spec's carveout *should* have caught but didn't, see Calibration §) → 0; Product Stories ratio 122 → 0; Products ratio 63 → 0. Average: **57.1**.
- Composite: (100 + 85.7 + 57.1) / 3 = **80.9** ✓

**Interpretive narrative — the WHY:** kll's ops score is the most internally heterogeneous in the spot-check: a 100 on catalog (the price-level carveout doing exactly what it should), a 85.7 on imports (one failed Customers run), and a 57.1 on freshness (three of seven feed types either stale or initial-load-only). The price-level carveout is the headline finding — a non-contract org with `prices_json` populated cleared the price check on 6,084 of 6,084 priced products. The freshness drag is mostly side-pipelines that initial-loaded in January and went quiet, which is a content/setup question (does Kuzco want Images and Product Stories to keep running?) rather than an operational health crisis.

### Composite analysis

**The story in one paragraph:** kll is a "healthy at the bottom of Thriving" — composite 80.2 sits exactly 0.2 over the band line. Every dimension is in the 69–88 range; nothing is broken and nothing is at the ceiling. The biggest single calibration question this account raises is the iPad-order threshold: kll runs commerce through the portal (31,794 orders) but the iPad-orders metric is sub-threshold at 9 by a single order — if the threshold were ≥ 5, they'd be at 100/100 on value delivery; if it were ≥ 50, the structural pattern would still read the same. There is also a denominator-breadth question similar to gh, though less extreme.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false

---

## fsf — Four Seasons Furniture

- Bundle: Full (Cart+Portal)
- Cohort year: 2023
- ARR: $22,560.00
- **Composite: 88.2 (Thriving)**
- Kylor's blind classification: Non-ghost active, Full bundle (Cart+Portal carveout check)
- Match? **Yes.** Full-bundle, every gate firing, no internal anomalies.

### Engagement: 69.3

| Raw input | Value |
|---|---|
| logins_90d | 1,501 |
| active_users_90d | 25 |
| enabled_users | 718 |
| last_login_at | 2026-05-11 22:42:20 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.0348 |
| capped ratio | 0.0348 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 1,501 → ≥ 1,000 → **88**
- Active user ratio: 3.48% → 0.01 ≤ x < 0.25 → **20**
- Recency: 0 days → **100**
- Average: (88 + 20 + 100) / 3 = **69.3** ✓

**Interpretive narrative — the WHY:** Engagement reads identically to kll (88 / 20 / 100 → 69.3), and for the same reason: a strong login count from a small share of a large enabled-users denominator. fsf shows 25 active users out of 718 enabled (3.5%); the 718 figure may include customer-portal accounts the same way gh's 7,911 does — fsf is a Full-bundle furniture wholesaler, so customer logins inflate the denominator. The 1,501 logins and 0-days recency say the core sales team is active; the ratio sub-score is signaling a breadth question that may be a data-hygiene issue (denominator), not a usage gap.

### Adoption: 100.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 1,501 logins |
| Smart Stacks | Yes | Yes | 5 smart_stacks |
| Sharing / quoting | Yes | Yes | 103 mp_sharing_events_90d (22 + 81) |
| eCat Online Catalog | Yes | Yes | flag-only |
| Online Ordering | Yes | Yes | 1,656 portal_orders_90d |
| Sales Portal | Yes | Yes | 1,656 portal_orders_90d |
| Inventory Management | Yes | Yes | 128 runs in 90d |
| Sales Data | Yes | Yes | 132 runs in 90d |

**Interpretive narrative — the WHY:** 8 of 8 — Full bundle saturated. The 103 sharing events skew toward document-email-drafted (81 of 103), suggesting fsf reps are quoting through the platform rather than just sharing items. The Inventory and Sales Data feeds both running 128–132 times in 90 days (roughly daily) means the operational pipelines are healthy enough to fire the binary gates with room to spare.

### Value Delivery: 100.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 255 | Yes |
| Sharing activity | Yes | ≥ 3 | 103 | Yes |
| Online catalog active | Yes | portal > 0 | 1,656 | Yes |
| Portal ordering | Yes | portal > 0 | 1,656 | Yes |
| Sales Portal engagement | Yes | portal > 0 | 1,656 | Yes |
| Inventory data flowing | Yes | inv > 0 | 128 | Yes |

**Interpretive narrative — the WHY:** 6 of 6 applicable channels achieved. The 255 iPad orders is the smallest among the Full-bundle Thrivings in this spot-check (vs. gh's 2,550 and sc's 8,092) but still 25× the threshold — fsf's iPad-channel volume is real, just not headline-grabbing.

### Operational Health: 83.3

**Sub-signal detail:**

- **Catalog:** 4,470 of 4,835 active = 92%. Step ladder → **85** (0.85 ≤ x < 0.95). Forensic breakdown: 1 missing description, 335 missing image (6.9%), 0 failing price. fsf is non-contract; the price-level carveout (`prices_json`) clears the price check for every priced product. Catalog is operationally tight.
- **Import Health:** 9 active import types, 0 errors → **100**.
- **Data Freshness:** 8 measurable feed types (Products has 1 run, omitted). Customers, Inventory, Portal Invoices, Sales Data current → 100; Portal Orders slightly behind (2.95d gap, 5d since last → ratio 1.69 → 50); Options slightly behind (2.55d gap, 4d since last → ratio 1.57 → 50); Images notably behind (6.0d gap, 19d since last → ratio 3.17 → 20); Option Images very behind (1.0d gap floored, 24d since last → ratio 24 → 0). Average: **65.0**.
- Composite: (85 + 100 + 65) / 3 = **83.3** ✓

**Interpretive narrative — the WHY:** Operational health is solidly above the Thriving floor, with catalog at 85 (one missing description and ~7% image gap) and imports at 100. Freshness is the dimension's softest spot at 65 — Images is 19 days late against a 6-day cadence (real catalog-content lag) and Option Images is 24 days late against a daily cadence (likely abandoned). Neither is operationally critical, but Images going stale on a Full-bundle furniture wholesaler with active commerce is worth surfacing.

### Composite analysis

**The story in one paragraph:** fsf is a clean Thriving at 88.2 — every dimension is healthy, with engagement held back only by the same large-denominator pattern visible at gh and kll. The biggest single calibration question this org raises is the same as kll's: 88.2 sits well above the Thriving cutoff, but the underlying numbers (3.5% active ratio, 9 of 8 imports clean, 65 freshness) read like a "competent and current" rather than "exemplary" account. If the V3.1 calibration tightens Adoption/Value Delivery thresholds, fsf would likely drop into Healthy, which would be a more honest portrayal of the gap between it and sc/ufi.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false *(the readiness review identified an operator string-match bug that **fails to flag** Full-bundle orgs whose MAL bundle is "Full (Cart+Portal)" — fsf is one of the affected orgs, but in fsf's case there is no actual underlying mismatch to surface, only the bug's silence)*
- support_fire: false
- ghost_account: false

---

## mfc — Morgan Fabrics Corporation

- Bundle: iPad+Catalog
- Cohort year: 2012
- ARR: $13,440.00
- **Composite: 53.3 (Watch)**
- Kylor's blind classification: Red, price-level pricing, 29% catalog (data-hygiene anomaly)
- Match? **No** — Kylor placed in At Risk/Critical, model produced Watch. Drift is consistent with the readiness review's "Reds drift one band high" finding.

### Engagement: 53.3

| Raw input | Value |
|---|---|
| logins_90d | 116 |
| active_users_90d | 10 |
| enabled_users | 561 |
| last_login_at | 2026-05-08 16:54:01 UTC |
| days_since_last_login | 3 |
| raw active_user_ratio | 0.0178 |
| capped ratio | 0.0178 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 116 → 50 ≤ x < 200 → **40**
- Active user ratio: 1.78% → 0.01 ≤ x < 0.25 → **20**
- Recency: 3 days → **100**
- Average: (40 + 20 + 100) / 3 = **53.3** ✓

**Interpretive narrative — the WHY:** Engagement sits at 53.3, and the recency sub-signal at 100 is the entire reason it isn't lower — somebody at mfc logged in 3 days ago, which masks how thin the rest of the activity is. 116 logins from 10 of 561 enabled users in 90 days is *barely* daily activity by a handful of reps, and the 1.78% active ratio is the kind of breadth that would benefit from a denominator check (the 561 figure for a fabric wholesaler likely includes customer-portal accounts, similar to gh/fsf). Engagement is correctly flagging "thin and shrinking" — the 53.3 reads more like a Watch-level concern than the dimension's 40-point boundary, which is itself an argument that the recency-sub-signal weight is generous.

### Adoption: 80.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 116 logins |
| Smart Stacks | Yes | Yes | 46 smart_stacks |
| Sharing / quoting | Yes | Yes | 25 mp_sharing_events_90d (25 + 0) |
| eCat Online Catalog | Yes (eoc=true) | Yes | flag-only |
| Online Ordering | No (eoo=false) | — | not applicable |
| Sales Portal | No (esp=false) | — | not applicable |
| Inventory Management | No (no Inventory imports in 180d) | — | not applicable |
| Sales Data | **Yes** (esd=true) | **No** | no Sales Data import in 180d |

**Interpretive narrative — the WHY:** This is the dimension where the "Reds drift high" pattern is most visible: 80/100 on adoption for an account with 116 logins and a 29% catalog. The math is correct — they fire iPad, Smart Stacks, Sharing, and eCat (the flag-only gate) and miss Sales Data — but the picture it paints is "competent breadth use," which mismatches what the underlying activity actually says. The flag-only eCat gate is the most generous of the eight feature checks: `enable_online_catalog=true` scores a point even if no one ever browsed the catalog. Removing that surface-only score would drop mfc to 3 of 4 (= 75) or, with a stricter usage gate, to 3 of 5 (= 60), both of which would read more like the Red Kylor had in mind.

### Value Delivery: 33.3

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | **0** | No |
| Sharing activity | Yes | ≥ 3 | 25 | Yes |
| Online catalog active | Yes | portal > 0 | 0 | No |
| Portal ordering | No (eoo=false) | — | — | n/a |
| Sales Portal engagement | No (esp=false) | — | — | n/a |
| Inventory data flowing | No | — | — | n/a |

**Interpretive narrative — the WHY:** Value delivery at 33.3 is the dimension that most cleanly tells the truth about mfc — they have zero iPad orders submitted in 90 days, zero portal traffic, and a single channel (Sharing) firing at 25 events. The model is correctly saying "one of three applicable channels is producing output, and it's the lowest-leverage one." If the spot-check found anything that argued for Watch over At Risk, it isn't here.

### Operational Health: 46.7

**Sub-signal detail:**

- **Catalog:** 1,507 of 5,257 active = 29%. Step ladder → **20** (0.25 ≤ x < 0.50). Forensic breakdown via Postgres: **3,749 missing description (71%)**, 148 missing image (3%), 0 failing price. mfc is a price-level pricing org (`contract_pricing_enabled=false`, no `prices_json` carveout failure on any product). The catalog gap is overwhelmingly description-driven, not a carveout bug — confirms the readiness review's hypothesis with direct evidence.
- **Import Health:** 2 active import types (Images, Products), both no error → **100**.
- **Data Freshness:** 2 measurable feed types. Images stale (14.4d gap, 55d since last → ratio 3.82 → 20); Products stale (9.5d gap, 32d since last → ratio 3.35 → 20). Average: **20**.
- Composite: (20 + 100 + 20) / 3 = **46.7** ✓

**Interpretive narrative — the WHY:** Operational health is the dimension that gives the most actionable read on mfc: a 29% catalog (entirely driven by 3,749 of 5,257 products lacking a `long_description`), a 100 on imports (the two pipelines they have are firing without errors), and a 20 on freshness (both of those pipelines have gone stale — last Images run 55 days ago, last Products run 32 days ago). The imports = 100 is technically correct but misleading — "100% of pipelines that ran most-recently ran without errors" isn't the same as "the data infrastructure is healthy." The ops dimension's three-way average masks that the pipelines stopped running, because the *runs that did happen* didn't error.

### Composite analysis

**The story in one paragraph:** mfc is the cleanest example in the spot-check of the readiness review's two main calibration findings working in tandem: (1) catalog completeness is real (29% complete, 71% missing description — not a carveout bug; price-level pricing is functioning), and (2) the breadth-of-features point system in Adoption gives partial credit for configured-but-unused surfaces, so an account with 0 iPad orders and 0 portal traffic still scores 80 on Adoption. The composite (53.3) lands in Watch, which is one band high of Kylor's read; the dimension breakdown shows exactly why — Engagement (53) and Value Delivery (33) are properly cold, but Adoption (80) and Ops (47) are warmer than the underlying activity merits, mostly because of the eCat flag-only gate and a 100 on imports for an organization that imports infrequently.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false

---

## st — Sixtrees Limited

- Bundle: iPad+Catalog
- Cohort year: 2015
- ARR: $6,960.00
- **Composite: 49.6 (Watch)**
- Kylor's blind classification: Red, ghost-candidate
- Match? **No** — Kylor placed in At Risk/Critical (and as a ghost-account candidate). Model produced Watch; ghost override correctly *did not* fire (logins_90d = 7, not 0) but ARR $6,960 ≥ the $5,000 floor, so a single calibration change would shift the override scope to catch this org.

### Engagement: 46.7

| Raw input | Value |
|---|---|
| logins_90d | 7 |
| active_users_90d | 1 |
| enabled_users | 22 |
| last_login_at | 2026-05-07 21:07:26 UTC |
| days_since_last_login | 4 |
| raw active_user_ratio | 0.0455 |
| capped ratio | 0.0455 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 7 → 1 ≤ x < 50 → **20**
- Active user ratio: 4.55% → 0.01 ≤ x < 0.25 → **20**
- Recency: 4 days → **100**
- Average: (20 + 20 + 100) / 3 = **46.7** ✓

**Interpretive narrative — the WHY:** Engagement is the textbook case of the recency sub-signal *artificially* propping up a dimension. Seven logins from one user in 90 days is, in any reasonable read, a near-ghost; the model gives it 46.7 because that one user logged in 4 days ago and the recency band rewards "logged in within a week" with 100 regardless of how thin the rest of the picture is. The login count (7) and breadth (1 of 22 users) both score 20 (the lowest non-zero band), which is the model correctly recognizing minimal activity — but the average dilutes those signals 2:1 with a recency score that says nothing about whether the account is actually being *used*.

### Adoption: 60.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 7 logins (above zero) |
| Smart Stacks | Yes | Yes | 2 smart_stacks |
| Sharing / quoting | Yes | **No** | 0 mp_sharing_events_90d |
| eCat Online Catalog | Yes (eoc=true) | Yes | flag-only |
| Online Ordering | No (eoo=false) | — | not applicable |
| Sales Portal | No (esp=false) | — | not applicable |
| Inventory Management | No (no Inventory imports) | — | not applicable |
| Sales Data | Yes (esd=true) | **No** | no Sales Data imports in 180d |

**Interpretive narrative — the WHY:** Adoption at 60 is the same "configured-equals-credit" pattern as mfc, only thinner. The 3-of-5 ratio gives full points for iPad ("any login in 90d" — passed with 7), Smart Stacks (2 configured), and eCat (flag-only). Removing the flag-only eCat gate would make this 2 of 5 (40), which fits better with the underlying observation that one user is doing seven logins.

### Value Delivery: 0.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 0 | No |
| Sharing activity | Yes | ≥ 3 | 0 | No |
| Online catalog active | Yes | portal > 0 | 0 | No |
| Portal ordering | No (eoo=false) | — | — | n/a |
| Sales Portal engagement | No (esp=false) | — | — | n/a |
| Inventory data flowing | No | — | — | n/a |

**Interpretive narrative — the WHY:** Value delivery is the only dimension in the spot-check at a flat 0.0 — and it is the dimension that most loudly says "this account is dormant." Zero iPad orders, zero sharing events, zero portal traffic across all three applicable channels. The 0 here is not a calibration artifact — it is the model accurately reporting that nothing of business value is happening on this account.

### Operational Health: 91.7

**Sub-signal detail:**

- **Catalog:** 18,484 of 18,819 active = 98%. Step ladder → **100** (≥ 95%). Forensic breakdown: 8 missing description, 335 missing image (1.8%), 0 failing price. st is non-contract; price-level pricing covers the price check.
- **Import Health:** 2 active import types (Images, Products), 0 errors → **100**.
- **Data Freshness:** 2 measurable feed types. Images slightly behind (1.6d gap, 3d since last → ratio 1.84 → 50); Products current (1.0d gap floored, 0d since last → ratio 0 → 100). Average: **75**.
- Composite: (100 + 100 + 75) / 3 = **91.7** ✓

**Interpretive narrative — the WHY:** This is the most consequential dimension in the spot-check for the Red-drift question: st has a 91.7 on operational health — driven by a 98% complete catalog and two healthy pipelines — *while* having 7 logins, 0 orders, and 0 sharing. The data infrastructure is being maintained beautifully for an account that nobody is using. The model is doing the right math (the infrastructure *is* healthy) but the composite averaging then weighs that 91.7 equally with the 0 on value delivery and the 46.7 on engagement, and the result is a Watch instead of an At Risk.

### Composite analysis

**The story in one paragraph:** st is the spot-check's clearest argument that the 25/25/25/25 unweighted composite is generous to abandoned accounts with healthy data feeds — Engagement 46.7, Adoption 60 (largely flag-only credit), Value Delivery 0, Operational Health 91.7. A weighted scheme where Engagement and Value Delivery had a larger combined share (say 60% to 40%) would put st in At Risk, which matches Kylor's read. The composite is also flirting with the ghost-account override scope: ARR $6,960 (above the $5,000 floor) and logins_90d = 7 — a single change to the ghost-trigger (logins_90d ≤ 10, or even ≤ 5) would catch this exact case.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: **false (but logically should be — 7 logins from 1 user is functionally a ghost)**

---

## hmjc — Hancock & Moore / Jessica Charles

- Bundle: iPad-only
- Cohort year: 2018
- ARR: $7,908.84
- **Composite: 50.4 (Watch)**
- Kylor's blind classification: Red, ghost-candidate
- Match? **No** — Kylor placed in At Risk/Critical (and as a ghost-account candidate). Same drift pattern as st.

### Engagement: 46.7

| Raw input | Value |
|---|---|
| logins_90d | 10 |
| active_users_90d | 3 |
| enabled_users | 118 |
| last_login_at | 2026-05-04 20:17:53 UTC |
| days_since_last_login | 7 |
| raw active_user_ratio | 0.0254 |
| capped ratio | 0.0254 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 10 → 1 ≤ x < 50 → **20**
- Active user ratio: 2.54% → 0.01 ≤ x < 0.25 → **20**
- Recency: 7 days → exactly at the ≤ 7 boundary → **100**
- Average: (20 + 20 + 100) / 3 = **46.7** ✓

**Interpretive narrative — the WHY:** Same dynamics as st — engagement is held aloft by a recency score of 100 that only fires because someone logged in 7 days ago (exactly on the boundary; one more day and it drops to 70 and engagement drops to 36.7, into At Risk territory). The actual usage signal is 10 logins from 3 of 118 users (3% active ratio), which by any reasonable read is functionally dormant. Worth noting that the recency boundary at exactly 7 days is the kind of fragile signal that can flip a band on a single user happening to log in at the right moment.

### Adoption: 60.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 10 logins |
| Smart Stacks | Yes | Yes | 2 smart_stacks |
| Sharing / quoting | Yes | **No** | 0 mp_sharing_events_90d |
| eCat Online Catalog | No (eoc=false) | — | not applicable |
| Online Ordering | No | — | not applicable |
| Sales Portal | No | — | not applicable |
| Inventory Management | Yes (Inventory active 180d) | Yes | 3 runs in 90d |
| Sales Data | Yes (esd=true) | **No** | 0 Sales Data runs |

**Interpretive narrative — the WHY:** 3 of 5 applicable features — iPad, Smart Stacks, and Inventory (note: 3 inventory runs in 90 days, just above the binary threshold). The gaps are Sharing (0 events) and Sales Data (0 runs). This is the cleanest case in the spot-check of the model rewarding minimal activity: 3 inventory runs over 90 days is once-a-month-ish, which fires the binary gate as readily as a daily feed. A graduated scoring (e.g., 0 / partial / full credit based on cadence) would more honestly reflect that hmjc's data pipelines are barely twitching.

### Value Delivery: 33.3

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 0 | No |
| Sharing activity | Yes | ≥ 3 | 0 | No |
| Online catalog active | No (eoc=false) | — | — | n/a |
| Portal ordering | No | — | — | n/a |
| Sales Portal engagement | No | — | — | n/a |
| Inventory data flowing | Yes | inv > 0 | 3 | Yes |

**Interpretive narrative — the WHY:** Value delivery at 33.3 is achieved by Inventory data flowing alone — 3 imports in 90 days is enough to fire the binary threshold. iPad orders is 0 and sharing is 0; the only "value-delivering" channel is a thinly-running data pipeline. The 33.3 here is more flattering than the underlying behavior warrants — a stricter "Inventory ≥ weekly" threshold would correctly take this to 0 of 3 (=0).

### Operational Health: 61.7

**Sub-signal detail:**

- **Catalog:** 2,748 of 3,152 active = 87%. Step ladder → **85** (0.85 ≤ x < 0.95). Forensic breakdown: 92 missing description (3%), 190 missing image (6%), 209 failing price (6.6%). hmjc is non-contract, non-price-level — they have ~6.6% of products with `net_price = 0` and no `prices_json`, which is the same "price-data gap" pattern we'll see at hh. Not a carveout bug; a real data-quality gap.
- **Import Health:** 4 active import types, 0 errors → **100**.
- **Data Freshness:** 4 measurable feed types. Customers (1d gap floored, 140d since last → ratio 140 → 0); Images (1.85d gap, 88d since last → ratio 47 → 0); Inventory (1.0d gap floored, 88d since last → ratio 88 → 0); Products (1.01d gap, 88d since last → ratio 87 → 0). Average: **0**.
- Composite: (85 + 100 + 0) / 3 = **61.7** ✓

**Interpretive narrative — the WHY:** Operational health at 61.7 is the spot-check's clearest case of the import-health vs. freshness split telling two different stories. Imports = 100 because the most recent run of each of the 4 active types had no errors. Freshness = 0 because every single feed went silent in mid-February and hasn't run since (Customers stopped 140 days ago, the others 88 days ago — all four likely lost their cron simultaneously). The catalog at 85 is the genuinely-healthy sub-signal of the three.

### Composite analysis

**The story in one paragraph:** hmjc is the second instance of the st pattern in the spot-check: minimal engagement (46.7) and value delivery (33.3) being averaged with adoption (60, mostly breadth-of-config credit) and ops (61.7, where the catalog and a deceptive imports = 100 mask the fact that the data pipelines went silent 3 months ago). The composite lands at 50.4, exactly inside Watch by 10 points. The single biggest structural argument for "this should be At Risk" is the imports = 100: if Import Health were re-defined as "most recent run within the org's cadence" instead of "most recent run had no errors," hmjc's imports would score 0, ops would drop to 28.3, and the composite would land at 42 (high Watch / barely-Watch). Recommend revisiting whether import-recency should fold into the Import Health sub-signal.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false *(narrowly missed: ARR $7,908 ≥ $5K floor and logins_90d = 10, just above the 0 threshold)*

---

## hh — Highland House

- Bundle: iPad-only
- Cohort year: 2013
- ARR: $7,830.00
- **Composite: 50.4 (Watch)**
- Kylor's blind classification: Red
- Match? **No** — Kylor placed in At Risk/Critical. Same drift as st and hmjc.

### Engagement: 46.7

| Raw input | Value |
|---|---|
| logins_90d | 17 |
| active_users_90d | 4 |
| enabled_users | 60 |
| last_login_at | 2026-05-08 17:09:09 UTC |
| days_since_last_login | 3 |
| raw active_user_ratio | 0.0667 |
| capped ratio | 0.0667 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 17 → 1 ≤ x < 50 → **20**
- Active user ratio: 6.67% → 0.01 ≤ x < 0.25 → **20**
- Recency: 3 days → **100**
- Average: (20 + 20 + 100) / 3 = **46.7** ✓

**Interpretive narrative — the WHY:** Same pattern as st and hmjc — 17 logins from 4 users out of 60 (7% active ratio) is functionally minimal usage, and the dimension only scrapes to 46.7 because the recency sub-signal at 100 is averaging up. The 60-enabled-users figure is the most plausible denominator in the Red set (smaller furniture wholesaler, not a customer-portal-inflation case), so the 4-of-60 ratio is more likely an accurate "4 reps are using it sporadically" signal than a denominator-quality issue.

### Adoption: 75.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 17 logins |
| Smart Stacks | Yes | Yes | 8 smart_stacks |
| Sharing / quoting | Yes | **No** | 0 mp_sharing_events_90d |
| eCat Online Catalog | No (eoc=false) | — | not applicable |
| Online Ordering | No | — | not applicable |
| Sales Portal | No | — | not applicable |
| Inventory Management | Yes (Inventory active) | Yes | 23 runs in 90d |
| Sales Data | No (esd=false) | — | not applicable |

**Interpretive narrative — the WHY:** Adoption at 75 (3 of 4) is the highest among the Reds — and the highest because hh has the *fewest* applicable features (4), so any single gap weighs more. iPad, Smart Stacks, and Inventory are firing; Sharing is the gap. Note that hh is the only Red in the spot-check that doesn't have the flag-only eCat surface to inflate Adoption, which is the reason 75 still reads as restrained relative to mfc's 80 and st/hmjc's 60.

### Value Delivery: 33.3

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 0 | No |
| Sharing activity | Yes | ≥ 3 | 0 | No |
| Online catalog active | No (eoc=false) | — | — | n/a |
| Portal ordering | No | — | — | n/a |
| Sales Portal engagement | No | — | — | n/a |
| Inventory data flowing | Yes | inv > 0 | 23 | Yes |

**Interpretive narrative — the WHY:** Same shape as hmjc — 1 of 3 applicable channels, driven entirely by Inventory data flowing. 23 inventory runs in 90 days is roughly weekly cadence; that fires the binary threshold cleanly but doesn't tell us anything about whether the data is going anywhere useful (0 iPad orders submitted from it, 0 sharing). This is the dimension that most cleanly reflects "data is moving but nothing is being done with it."

### Operational Health: 46.7

**Sub-signal detail:**

- **Catalog:** 1,232 of 1,564 active = 79%. Step ladder → **65** (0.70 ≤ x < 0.85). Forensic breakdown: 0 missing description, 4 missing image, **330 failing price (21%)**. hh is **not** contract-pricing and **not** using price-level pricing — they have $0 `net_price` and no `prices_json` on 330 of 1,564 products. This is a real catalog data-quality gap, the only org in the spot-check with a non-zero price-failure count of any size. The carveouts are NOT firing for hh (correctly — they qualify for neither), so the 21% gap reads as a "pricing data isn't populated" coaching opportunity.
- **Import Health:** 4 active import types. Products had an error on its most recent run → 3 of 4 healthy → **75**.
- **Data Freshness:** 4 measurable feed types. Customers (140d since last → ratio 140 → 0); Images (6.2d gap, 79d since last → ratio 12.8 → 0); Inventory (1.0d floored, 77d since last → ratio 77 → 0); Products (1.0d gap, 77d since last → ratio 75 → 0). Average: **0**.
- Composite: (65 + 75 + 0) / 3 = **46.7** ✓

**Interpretive narrative — the WHY:** Operational health is the lowest among the Reds at 46.7 and it gets there honestly — catalog is at 65 (real data-quality gap from 330 priceless products), imports is at 75 (one of four pipelines threw an error on its last run), and freshness is at 0 (every feed went silent ~77–140 days ago, same Feb-stopped pattern as hmjc). This is the cleanest "Operational Health is also failing" reading in the Red set — and even with that, the composite still rounds up into Watch because the unweighted average masks the breadth of the failure.

### Composite analysis

**The story in one paragraph:** hh is the Red with the cleanest "everything is failing" pattern — engagement at 46.7 (thin), value delivery at 33.3 (Inventory only), and ops at 46.7 (catalog drag + import error + total freshness collapse). The composite lands at 50.4 only because Adoption (75) is doing the heavy lifting — and that 75 is largely "they have 3 applicable features and they're configured." With Adoption excluded, the average of the other three would be 42, which is exactly the kind of high-Watch / borderline-At-Risk read that matches Kylor's intuition. The pattern across the four Reds (mfc 53.3, st 49.6, hmjc 50.4, hh 50.4) is striking — they cluster within a 4-point range *just* above the Watch line, despite very different underlying activity profiles.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false

---

## wac — WAC/Modern Forms Lighting

- Bundle: iPad-only
- Cohort year: 2023
- ARR: $22,104.00
- **Composite: 90.7 (Thriving)**
- Kylor's blind classification: contract-pricing carveout verification (no Green/Red — included to verify carveout)
- Match? **N/A** — included to verify the contract-pricing carveout, which fires correctly: catalog 100% with the `contract pricing — price check skipped` note in the narrative.

### Engagement: 88.3

| Raw input | Value |
|---|---|
| logins_90d | 3,127 |
| active_users_90d | 94 |
| enabled_users | 160 |
| last_login_at | 2026-05-11 22:51:47 UTC |
| days_since_last_login | 0 |
| raw active_user_ratio | 0.5875 |
| capped ratio | 0.5875 |
| denominator_quality | null |

**Sub-signal scoring:**
- Login count: 3,127 → ≥ 3,000 → **100**
- Active user ratio: 58.75% → 0.50 ≤ x < 0.75 → **65**
- Recency: 0 days → **100**
- Average: (100 + 65 + 100) / 3 = **88.3** ✓

**Interpretive narrative — the WHY:** Strong engagement across all three sub-signals — 3,127 logins just clears the top login band (≥ 3,000), 94 of 160 users active represents the most plausible "true active ratio" in the spot-check (medium-sized lighting rep network, no obvious denominator inflation), and a 0-day recency. The 65 on ratio is the dimension's only headroom — at 59% they're a Goldilocks "more than half but not yet broadly universal," which the bands appropriately price as healthy-not-saturated.

### Adoption: 100.0

| Feature | Applicable? | Used? | Source evidence |
|---|---|---|---|
| iPad App | Yes | Yes | 3,127 logins |
| Smart Stacks | Yes | Yes | 11 smart_stacks |
| Sharing / quoting | Yes | Yes | 83 mp_sharing_events_90d (11 + 72) |
| eCat Online Catalog | No (eoc=false) | — | not applicable |
| Online Ordering | No (eoo=false) | — | not applicable |
| Sales Portal | No (esp=false) | — | not applicable |
| Inventory Management | Yes (Inventory active) | Yes | 86 runs in 90d |
| Sales Data | Yes (esd=true) | Yes | 40 runs in 90d |

**Interpretive narrative — the WHY:** 5 of 5 applicable — iPad-only bundle with sales-data and inventory pipelines, all firing. 5-feature denominator is the smallest among the Thriving accounts in the spot-check, reflecting the iPad-only bundle (no eCat / portal / cart surfaces). 86 inventory runs and 40 sales-data runs in 90d are both well-paced daily/weekly cadences.

### Value Delivery: 100.0

| Channel | Applicable? | Threshold | Actual | Achieved? |
|---|---|---|---|---|
| Order volume (iPad) | Yes | ≥ 10 | 857 | Yes |
| Sharing activity | Yes | ≥ 3 | 83 | Yes |
| Online catalog active | No (eoc=false) | — | — | n/a |
| Portal ordering | No | — | — | n/a |
| Sales Portal engagement | No | — | — | n/a |
| Inventory data flowing | Yes | inv > 0 | 86 | Yes |

**Interpretive narrative — the WHY:** 3 of 3 applicable channels achieved — 857 iPad orders (85× the threshold), 83 sharing events (28×), and 86 inventory runs. The 3-channel denominator reflects the iPad-only bundle correctly excluding the three portal-fed channels; this is the carveout's structural counterpart on Value Delivery side.

### Operational Health: 74.4

**Sub-signal detail:**

- **Catalog:** 28,821 of 28,833 active = 99.96% → ~100%. Step ladder → **100**. Forensic breakdown: 0 missing description, 12 missing image, 0 failing price. wac is contract-pricing (`contract_pricing_enabled=true`); the contract-pricing carveout is satisfying the price clause for every product, exactly as designed. Narrative correctly emits `(contract pricing — price check skipped)`.
- **Import Health:** 6 active import types. Products had an error on its most recent run → 5 of 6 healthy → **83.3**.
- **Data Freshness:** 6 measurable feed types. Customers (4.1d gap, 43d since last → ratio 10.5 → 0); Images (4.15d gap, 14d since last → ratio 3.37 → 20); Inventory current → 100; Product Stories (1.0d floored, 124d since last → ratio 124 → 0 — but should have been excluded under the initial-load carveout, see Calibration §); Products (5.13d gap, 13d since last → ratio 2.53 → 20); Sales Data current → 100. Average: **40**.
- Composite: (100 + 83.3 + 40) / 3 = **74.4** ✓

**Interpretive narrative — the WHY:** Operational health at 74.4 is the highest among the iPad-only accounts in the spot-check and the carveout works cleanly: 28,833 active products and 28,821 complete because `contract_pricing_enabled=true` clears the price check for all of them. The drag is freshness at 40 — Customers stopped firing 43 days ago, Product Stories was initial-loaded in January and never ran again, and Images/Products are running on a sub-cadence basis. Imports = 83.3 (the Products error pulls it down) is doing useful work that didn't need to happen — wac is the only org in the spot-check where the import-health sub-signal actively flagged a real failure (the Products feed's most recent run errored).

### Composite analysis

**The story in one paragraph:** wac is the spot-check's clean confirmation that the contract-pricing carveout (the WAC/FAL-style case) is firing as designed — `contract_pricing_enabled=true` produces a catalog score of 100 on 28,833 products without forcing the operator to walk every `net_price` row. The composite (90.7) reads correctly as a Thriving account with above-band engagement, full adoption/value-delivery saturation, and a freshness drag from side pipelines that have gone quiet. No risk surfaced anywhere; the carveout verification is a clean Pass.

**Flags worth surfacing:**
- denominator_quality: null
- bundle_config_mismatch: false
- support_fire: false
- ghost_account: false

---

# Calibration observations

1. **The recency sub-signal averages up Engagement disproportionately for thin accounts.** In all four Reds (mfc, st, hmjc, hh), Engagement is held aloft by a recency score of 100 that fires because *one user* logged in within the last 7 days — and recency is one of three sub-signals averaged equally, so a single login can be worth ~33 engagement points. st (1 user / 7 logins / last login 4 days ago) → 46.7. hmjc (7 days, on the boundary) → 46.7. **Classification:** Calibration.

2. **The flag-only `eCat Online Catalog` gate in Adoption gives a free point to any org with `enable_online_catalog=true`, regardless of usage.** This is most visible at mfc (Adoption 80 with 0 portal traffic), st (Adoption 60 with 0 sharing and 0 orders), and hmjc (Adoption 60 with 0 sharing and 0 iPad orders). **Classification:** Calibration — README §2 lists the gate as `mobile_site EXISTS with enable_online_catalog = true`, which is a config check, not an engagement check. Consider gating eCat usage on `portal_orders_90d > 0` (like Online Ordering and Sales Portal already do) to make the dimension internally consistent.

3. **Reds cluster within a 4-point band just above the Watch line (49.6–53.3), and the 25/25/25/25 average is the structural reason why.** Their Engagement and Value Delivery are correctly cold (often 0–47), but Adoption (60–80, breadth-of-config credit) and Operational Health (47–92, data infrastructure being maintained for accounts no one is using) keep the average above 40. This matches the readiness review's "Reds drift one band high" finding and is what the §9 stratified validation plan is designed to test. **Classification:** Calibration — fixable with weighting once correlation data exists; structural under V3.0 spec.

4. **The Import Health sub-signal counts "most recent run had no errors" as healthy even when the most recent run was months ago.** hmjc and hh both score 100/100 on Import Health while every active feed went silent in mid-February. The catalog can be complete and the most recent run can be error-free, and the dimension reports green — while in reality the pipelines have stopped. **Classification:** Calibration / Known V3.1 gap — README §4 defines an "active import type" as having run in trailing 180d, which means a once-3-months-ago run still counts as active. Consider tightening Import Health to "ran successfully within X× cadence" (folding part of the Freshness signal into Import Health).

5. **The initial-load carveout in the Freshness sub-signal does not fire in practice.** Visible at kll (Product Stories: 3 runs in 2 days, last run 122 days ago — the carveout should exclude it; instead it scores 0 and drags the freshness average from 66.7 to 57.1) and at wac (same pattern on Product Stories). The carveout's check `days_since_last == days_since_first - days_span` is a floating-point identity that almost never returns True due to ULP differences in how the three values are computed. **Classification:** Bug (in operator implementation, not spec) — but contained: when the carveout fires-spuriously-fails-to-fire, the affected import type scores 0 and dilutes the freshness sub-signal, which has at most a 4–8 point impact on operational health. Worth a future fix; doesn't invalidate V3.0 output for this run.

6. **mfc's 29% catalog completeness is description-driven, not a carveout bug — confirmed directly via Postgres.** 3,749 of 5,257 active products (71%) have no `long_description`; 0 fail the price check (price-level pricing is functioning correctly). This is real data hygiene — coaching opportunity for the CSM, not a fix for the operator. **Classification:** Portfolio truth.

7. **Catalog completeness drag at sc (62%) and gh (60%) is entirely image-driven (38–40% of products lacking `image_exists=true`).** Description is 100% covered on both; contract pricing satisfies the price check on every product. Two of the strongest accounts in the portfolio have substantial image-coverage gaps — that's a content/CSM motion, not an infrastructure problem. **Classification:** Portfolio truth.

8. **The denominator-quality flag only catches inflated ratios (> 100% raw), not deflated ones from customer-portal accounts inflating the enabled_users count.** Visible at gh (7,911 enabled users, ratio 0.71% → 0 sub-score) and likely at fsf (718 enabled). Both orgs are stronger than their Engagement score reads, and the model has no flag to surface why. **Classification:** Calibration / Known V3.1 gap.

---

# Recommended edits

This section follows the user's constraint of *surgical threshold/band changes only* — no architectural changes, no operator rewrites, no scoring-logic edits. The list below is intentionally short; most of the calibration observations above are V3.1 design questions that warrant CEO + Kylor discussion rather than pre-rerun edits.

I have **two** specific surgical proposals to surface. Both are calibration adjustments inside the existing band tables; both can be implemented as single-line changes to `LOGIN_BANDS` / `RECENCY_BANDS` / threshold constants without restructuring the operator.

### 1. Tighten the Engagement recency band to soften the "one login = 100" cliff

- **WHAT:** Change `RECENCY_BANDS` from `[(7, 100), (30, 70), (90, 40)]` to `[(7, 90), (30, 60), (90, 30)]` (or equivalent — drop each tier by 10–15 points).
- **WHY:** Calibration observation #1 — in all four Reds, the recency-100 score is averaging up engagement by ~17 points and obscuring the 7/10/17-login reality underneath. A 90 instead of 100 still rewards same-week recency without letting it single-handedly carry the dimension.
- **IMPACT:** Of the 10 spot-checked orgs, the four Reds (mfc, st, hmjc, hh) and likely a portion of the wider Watch tier would drop ~3 points on Engagement and ~0.8 points on the composite. mfc 53.3 → ~52.5 (still Watch); st 49.6 → ~48.8 (still Watch, closer to At Risk); hmjc 50.4 → ~49.6 (Watch → Watch boundary); hh 50.4 → ~49.6 (same). None shift bands, but the gap to the At Risk boundary narrows from ~10 points to ~9, and the dimension becomes more honest. Greens are unaffected (their recency scores already round to 100 on same-day logins).

### 2. Raise the iPad Order Volume threshold from ≥ 10 to ≥ 50

- **WHAT:** In `score_value_delivery`, change `activities.append(("Order volume (iPad)", True, ipad_orders_90d >= 10))` to `... >= 50`.
- **WHY:** The README itself flags this in §3: "Thresholds are intentionally low for V1. Calibrate upward in V3.1 after spot-checking." In the spot-check, this threshold matters precisely once: at kll, where 9 iPad orders sits 1 below the current threshold (Value Delivery 83.3) and the actual usage pattern is "all 31,794 orders are going through the portal, iPad isn't used as an order channel." Raising the threshold to ≥ 50 catches more of those "portal-only" orgs in the wider portfolio.
- **IMPACT:** Of the 10 spot-checked orgs, kll already has Value Delivery 83.3 (1 channel short of saturation) — raising the threshold doesn't change kll. Of the remaining 9, the iPad order counts are: sc 8,092, ufi 610, gh 2,550, fsf 255, wac 857 (all well above ≥ 50, no change); mfc 0, st 0, hmjc 0, hh 0 (all already failing the ≥ 10, will continue to fail ≥ 50, no change). So **within this spot-check, the threshold change has zero band-shift impact** — but in the wider portfolio (per readiness review §4: 53% Thriving, 17 of 20 Full-bundle in Thriving), it would catch portal-only Full-bundle accounts whose iPad order count is 10–49 and bring some of them down from 100 Value Delivery to 83.3.

### Edits explicitly NOT recommended

- **Flag-only eCat Online Catalog gate change (Calibration observation #2):** This is a spec-level change (config-gate vs. usage-gate) and per the user's constraint should not be edited unilaterally. Surface to Kylor for V3.1 discussion.
- **Ghost-account threshold change (st, hmjc):** Both narrowly miss the override (st: logins_90d=7, ARR $6,960; hmjc: logins_90d=10, ARR $7,909). Changing the trigger from `= 0` to `≤ 10` would catch both, but the override is intentionally surgical per §5.1 ("zero login events ... the highest-leverage save target") and broadening it changes the override's character. Surface as a discussion point, not an edit.
- **Initial-load carveout bug fix (Calibration observation #5):** This is a code-level bug fix in `score_operational_health`, not a threshold/band edit. Surface for a separate fix pass; impact on the run is small (4–8 ops points on a handful of orgs).
- **Bundle/config mismatch over-flagging bug (readiness review):** Same — code fix, not a threshold edit. The readiness review already proposes the one-line fix; for the spot-check, none of our 10 orgs have a real mismatch and only fsf is among the 20 false positives, so the bug does not materially affect this report.

---

*Report end. Composite math, sub-signal math, and band assignments were verified against the operator and the cache for all 10 orgs; every score in the CSV reconciles to the inputs documented in this report within ≤ 0.1 (banker's-rounding tolerance per the readiness review).*
