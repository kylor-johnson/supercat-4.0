# Health V3 — Test Scoring Run (10 Orgs)

**Date:** 2026-05-11
**Spec:** Health V3 README v3.0.0
**Window:** Trailing 90 days for activity signals; 180 days for import history.
**Sources:** Postgres (`user-supercat-postgres-vpn`) for all behavioral / catalog / import data; BigQuery (`user-bigquery-vpn`) for HelpScout support fire check.
**Excluded:** `wwjc`, `pf`, `wac`, `rw`, `fal` (per instructions).

## Selection rationale

| Org | Bundle (MAL) | Cohort | Why it was picked |
|---|---|---|---|
| `tam` | iPad-only | 2016 | iPad-only #1 (mature, no eCat config flags) |
| `hf` | iPad-only | 2024 | iPad-only #2 (newer cohort, no eCat config flags) |
| `gsa` | iPad-only | 2011 | Long-tenured iPad-only with active sharing |
| `bp` | iPad-only | 2024 | iPad-only by MAL but `mobile_sites.enable_online_catalog=true` AND `enable_online_ordering=true` — anomaly worth checking (see Spec Flags) |
| `mfc` | iPad+Catalog | 2012 | eCat Online Catalog active #1 (mature, catalog-only) |
| `cci` | iPad+Catalog+Portal | 2021 | eCat Online Catalog active #2 + Sales Portal |
| `jc`  | iPad+Catalog+Portal | 2018 | eCat Online Catalog active #3 + Sales Portal |
| `dccl` | iPad+Catalog+Cart | 2024 | B2B Cart + `enable_online_ordering=true` (newer) |
| `fsf` | Full (Cart+Portal) | 2023 | B2B Cart + `enable_online_ordering=true` (full stack) |
| `kll` | Full (Cart+Portal) | 2022 | B2B Cart + `enable_online_ordering=true` (high-volume portal) |

Mix: 4 iPad-only, 1 iPad+Catalog, 2 iPad+Catalog+Portal, 1 iPad+Catalog+Cart, 2 Full. Cohorts span 2011→2024. Three orgs hit the B2B Cart + `enable_online_ordering=true` requirement (`dccl`, `fsf`, `kll`). Three hit the eCat Online Catalog active requirement (`mfc`, `cci`, `jc`).

---

## Summary

| org_shortname | bundle | engagement | adoption | value_delivery | operational_health | health_score | health_band | ghost_account |
|---|---|---:|---:|---:|---:|---:|---|:---:|
| `tam`  | iPad-only           | 76.5 | 60.0  | 100.0 | 99.9 | **84.1** | Thriving | false |
| `fsf`  | Full (Cart+Portal)  | 94.0 | 100.0 | 100.0 | 85.8 | **95.0** | Thriving | false |
| `jc`   | iPad+Catalog+Portal | 52.5 | 100.0 | 80.0  | 85.0 | **79.4** | Healthy  | false |
| `cci`  | iPad+Catalog+Portal | 76.5 | 100.0 | 60.0  | 79.2 | **78.9** | Healthy  | false |
| `gsa`  | iPad-only           | 62.5 | 100.0 | 33.3  | 86.1 | **70.5** | Healthy  | false |
| `hf`   | iPad-only           | 87.5 | 80.0  | 33.3  | 71.3 | **68.0** | Healthy  | false |
| `dccl` | iPad+Catalog+Cart   | 78.5 | 100.0 | 40.0  | 50.4 | **67.2** | Healthy  | false |
| `kll`  | Full (Cart+Portal)  | 54.0 | 87.5  | 83.3  | 43.8 | **67.2** | Healthy  | false |
| `bp`   | iPad-only (MAL)     | 70.0 | 71.4  | 20.0  | 79.7 | **60.3** | Healthy  | false |
| `mfc`  | iPad+Catalog        | 30.0 | 80.0  | 33.3  | 40.0 | **45.8** | Watch    | false |

> `ghost_account` is **not defined in the V3 README**. I used a transparent operational heuristic — `ghost_account = true` iff `engagement_score < 30` AND `active_user_ratio < 25%` AND `orders_90d < 10` AND `shared_resources_90d < 3`. No org in this set trips all four. `mfc` is the closest miss (`engagement_score = 30`, ratio 16%, `orders_90d = 0`, but `shared_resources_90d = 3`). Logged in Spec Flags.

Support fire (V3 §5 — L3/L4 escalation or S1/S2 severity, currently open in HelpScout): **none of the 10 orgs has a matching open conversation**. See Spec Flags re: HelpScout severity vocabulary.

---

## Per-org scoring detail

For each org, raw signals are shown before the sub-scores so the reasoning is auditable end-to-end.

---

### `tam` — Theodore Alexander Manhasset (iPad-only, 2016)

**Engagement**
- `logins_90d` = 1,021 (band 1,000–2,999 → 88)
- Active users 90d = 15; enabled users = 22; ratio = 68.2% (band 50–74% → 65)
- engagement_score = (88 + 65) / 2 = **76.5**

**Adoption (applicability gating)**
- iPad: applicable, logins > 0 ✓
- Smart Stacks: applicable, count = 0 ✗
- Shared Resources: applicable, total = 128 ✓
- eCat Online Catalog: `enable_online_catalog` is NULL → NOT applicable
- Online Ordering: NULL → NOT applicable
- Sales Portal: NULL → NOT applicable
- Inventory Management: 33 Inventory imports in 90d, history present → applicable + used ✓
- Sales Data: `enable_sales_data=true` → applicable; but **no `Sales Data` import type in trailing 180d** → not used ✗
- Used 3 of 5 applicable: **adoption_score = 60.0**

**Value Delivery**
- iPad orders: 103 in 90d (≥10) ✓
- Sharing: 19 shared resources in 90d (≥3) ✓
- Online Catalog browsing: not applicable (gate off)
- Portal/Sales Portal: not applicable (gates off)
- Inventory flowing: 33 imports in 90d ✓
- 3 of 3 applicable channels achieved: **value_delivery_score = 100.0**

**Operational Health**
- Catalog: 7,371 / 7,404 active products complete = **99.6%**
- Import Health: 6 of 6 active import types had last run with no `:error` / `:fatal` → **100%**
- Freshness: 6 active types with ≥3 runs; all `days_since_last / mean_gap ≤ 1.0` → **100%**
- operational_health_score = (99.6 + 100 + 100) / 3 = **99.9**

**Composite: 84.1 — Thriving**

- *"1,021 logins in 90 days from 15 of 22 enabled users (68% active ratio). Activity is steady — a top-quartile engagement profile for an iPad-only account this size."*
- *"Using 3 of 5 applicable features. Unused: Smart Stacks (0 created), Sales Data feed (configured but no imports in 180 days)."*
- *"Delivering value through 3 of 3 applicable channels. iPad order volume is active (103 orders in 90d), sharing activity is healthy (19 in 90d), and inventory is flowing daily."*
- *"Catalog 99.6% complete. Imports: 6 of 6 active feed types healthy. Freshness: every active feed is on or ahead of its observed cadence."*

---

### `fsf` — Four Seasons Furniture (Full Cart+Portal, 2023)

**Engagement**
- `logins_90d` = 1,503 (band 1,000–2,999 → 88)
- Active users 90d = 25; enabled users = 20; ratio = 125%, **capped at 100%** (band 90%+ → 100)
- engagement_score = (88 + 100) / 2 = **94.0**

> Ratio > 100% indicates iPad logins from `org_users` rows marked `disabled = true`. This is a real V3 spec ambiguity — see Spec Flags.

**Adoption**
- All 8 features applicable (iPad, SS, SR, Online Catalog, Online Ordering, Sales Portal, Inventory, Sales Data). All used: iPad(1,503), SS(5), SR(191), Online Catalog(enable=true), Online Ordering(portal_orders_90d=1,655), Sales Portal(portal_orders_90d=1,655), Inventory(128 imports/90d), Sales Data(133 imports/90d).
- **adoption_score = 100.0**

**Value Delivery**
- iPad orders: 255 in 90d ✓
- Sharing: 16 in 90d ✓
- Online Catalog browsing: gate on; `clicky_id=101476068` exists. Clicky data not directly queryable from this run — used heuristic ✓ (valid Clicky ID AND active portal traffic ≥ 1,655 orders in 90d are clear evidence of online engagement). Flagged.
- Portal Ordering: 1,655 portal_orders in 90d ✓
- Sales Portal: 1,655 portal_orders in 90d ✓
- Inventory flowing: 128 imports/90d ✓
- 6 of 6: **value_delivery_score = 100.0**

**Operational Health**
- Catalog: 4,470 / 4,835 = **92.5%**
- Import Health: 9 of 9 active types healthy → **100%**
- Freshness: 8 types qualify (≥3 runs); 4× 100, 2× 50 (Options 1.63, Portal Orders 1.69), 1× 20 (Images 3.18), 1× 0 (Option Images 242× — only 20 events all within 2 days, see Spec Flags) → avg **65**
- operational_health_score = (92.5 + 100 + 65) / 3 = **85.8**

**Composite: 95.0 — Thriving**

- *"1,503 logins in 90 days from 25 active iPad users against 20 enabled `org_users` rows — ratio capped at 100%. Activity is heavy and broad-based; the >100% raw ratio reflects active users whose `org_users.disabled` flag is true (data quality note, not a real engagement gap)."*
- *"Using 8 of 8 applicable features. Nothing unused."*
- *"Delivering value through 6 of 6 applicable channels. iPad orders (255), portal orders (1,655 in 90d), and daily inventory + sales-data imports are all active."*
- *"Catalog 92% complete. Imports: 9 of 9 active feed types healthy. Freshness: most feeds on cadence; Images is moderately stale (3.2× expected gap) and the short-lived Option Images feed (20 runs in 2 days) registers as extreme staleness because its measurement window is unrealistic — see Spec Flags."*

---

### `jc` — Jonathan Charles Fine Furniture (iPad+Catalog+Portal, 2018)

**Engagement**
- `logins_90d` = 299 (band 200–499 → 60)
- Active 11; enabled 29; ratio 37.9% (band 25–49% → 45)
- engagement_score = (60 + 45) / 2 = **52.5**

**Adoption**
- 7 applicable (no Online Ordering since gate is false). All 7 used: iPad ✓, SS(26) ✓, SR(354) ✓, Online Catalog ✓, Sales Portal(portal_orders_90d=72) ✓, Inventory(7) ✓, Sales Data(5) ✓.
- **adoption_score = 100.0**

**Value Delivery**
- iPad orders: 12 in 90d ✓
- Sharing: 10 in 90d ✓
- Online Catalog browsing: gate on, **no `clicky_id` set** — Clicky-based source unavailable for this org → not credited ✗
- Online Ordering: gate off → NOT applicable
- Sales Portal: portal_orders_90d=72 ✓
- Inventory: 7 imports/90d ✓
- 4 of 5: **value_delivery_score = 80.0**

**Operational Health**
- Catalog: 15,515 / 21,686 = **71.5%** (1,844 active products missing images; ~4,433 with `net_price=0`)
- Import Health: 12 of 12 active types healthy → **100%**
- Freshness: 11 qualifying types; 8× 100, 3× 80 (Products 1.17, Option Images 1.29, Portal Invoices 1.34, Options 1.24), 1× 0 (Matrix Options 156× — only 3 runs in 6 hours, see Spec Flags) → avg **83.6**
- operational_health_score = (71.5 + 100 + 83.6) / 3 = **85.0**

**Composite: 79.4 — Healthy**

- *"299 logins in 90 days from 11 of 29 enabled users (38% active ratio). Most of the team is not actively engaging — consider investigating whether reps are aware of recent catalog updates."*
- *"Using 7 of 7 applicable features. Nothing unused."*
- *"Delivering value through 4 of 5 applicable channels. Catalog browsing is enabled but no Clicky ID is configured on the mobile site — online catalog engagement can't be measured for this org (flag for ops)."*
- *"Catalog 71% complete — ~1,844 active products are missing images. Imports: 12 of 12 active feed types healthy. Freshness: most feeds on cadence; Matrix Options registers as stale due to a degenerate measurement window (3 runs in a 6-hour burst)."*

---

### `cci` — Currey & Company (iPad+Catalog+Portal, 2021)

**Engagement**
- `logins_90d` = 2,456 (band 1,000–2,999 → 88)
- Active 52; enabled 72; ratio 72.2% (band 50–74% → 65)
- engagement_score = **76.5**

**Adoption**
- 7 applicable (no Online Ordering — gate false). All used: iPad(2,456), SS(7), SR(104), Online Catalog ✓, Sales Portal(portal_orders_90d=14,980), Inventory(537), Sales Data(178).
- **adoption_score = 100.0**

**Value Delivery**
- iPad orders: 1,030 in 90d ✓
- Sharing: 0 in 90d ✗ (104 lifetime but none added/edited in the window)
- Online Catalog browsing: gate on, no `clicky_id` ✗
- Online Ordering: not applicable
- Sales Portal: portal_orders_90d=14,980 ✓
- Inventory: 537 imports/90d ✓
- 3 of 5: **value_delivery_score = 60.0**

**Operational Health**
- Catalog: 5,708 / 6,130 = **93.1%**
- Import Health: 6 of 9 healthy (Customers, Products, Sales Data each had `:error` on their most recent run) → **66.7%**
- Freshness: 9 types qualify; 7× 100, 2× 0 (Images 13.8×, Portal Orders 4.0×) → avg **77.8**
- operational_health_score = (93.1 + 66.7 + 77.8) / 3 = **79.2**

**Composite: 78.9 — Healthy**

- *"2,456 logins in 90 days from 52 of 72 enabled users (72% active ratio). Activity is steady — a healthy engagement profile across the rep base."*
- *"Using 7 of 7 applicable features. Nothing unused."*
- *"Delivering value through 3 of 5 applicable channels. Portal ordering is the workhorse (14,980 portal orders in 90d) and iPad order volume is healthy. Sharing has stalled — 0 new shared resources in 90d despite 104 lifetime, worth checking. Online catalog browsing can't be scored — no Clicky ID configured."*
- *"Catalog 93% complete. Imports: 6 of 9 active feed types healthy — Customers, Products, and Sales Data each error on the most recent run (price-level code validation, parse warnings). Freshness: most feeds on cadence; Images is ~14× overdue and Portal Orders is 4× overdue."*

---

### `gsa` — Godinger Silver Art (iPad-only, 2011)

**Engagement**
- `logins_90d` = 493 (band 200–499 → 60). Note: 493 is below the 500 cutoff for the next band.
- Active 19; enabled 31; ratio 61.3% (band 50–74% → 65)
- engagement_score = **62.5**

**Adoption**
- 4 applicable (iPad, SS, SR, Inventory). No mobile_sites flags. `enable_sales_data = false` so Sales Data not applicable.
- All 4 used: iPad(493), SS(19), SR(2), Inventory(75).
- **adoption_score = 100.0**

**Value Delivery**
- iPad orders: 5 in 90d ✗ (< 10)
- Sharing: 0 in 90d ✗
- Inventory flowing: 75 imports/90d ✓
- No conditional channels applicable
- 1 of 3: **value_delivery_score = 33.3**

**Operational Health**
- Catalog: 3,850 / 5,448 = **70.7%** (1,598 products missing images)
- Import Health: 5 of 5 active types healthy → **100%**
- Freshness: 4 qualifying types; 3× 100, 1× 50 (Customers 2.36×) → avg **87.5**
- operational_health_score = (70.7 + 100 + 87.5) / 3 = **86.1**

**Composite: 70.5 — Healthy**

- *"493 logins in 90 days from 19 of 31 enabled users (61% active ratio). Activity is steady but order throughput is light — only 5 iPad orders in 90 days for a 2011-cohort iPad-only account."*
- *"Using 4 of 4 applicable features. Nothing unused."*
- *"Delivering value through 1 of 3 applicable channels. iPad order volume (5 in 90d) is below the 10-order threshold and sharing is at zero — the iPad is being opened but not used to drive orders or share content. Worth a sales-coverage conversation."*
- *"Catalog 71% complete — ~1,598 active products are missing images. Imports: 5 of 5 active feed types healthy. Freshness: 3 of 4 measurable feeds on cadence; Customers feed is moderately late (2.4× the observed gap)."*

---

### `hf` — Hooker Furnishings (iPad-only, 2024)

**Engagement**
- `logins_90d` = 597 (band 500–999 → 75)
- Active 23; enabled **3**; raw ratio 767% → **capped at 100%** (band 90%+ → 100)
- engagement_score = (75 + 100) / 2 = **87.5**

> Real data anomaly — 23 distinct users logged in but only 3 `org_users` rows have `disabled=false`. The other 20 active users have `disabled=true`. The disabled flag is unreliable here. Flagged.

**Adoption**
- 5 applicable (iPad, SS, SR, Inventory, Sales Data — `enable_sales_data=true`).
- Used: iPad(597), SS(23), SR(4), Inventory(92). **Sales Data: no `Sales Data` import type in trailing 180d → not used ✗**.
- 4 of 5: **adoption_score = 80.0**

**Value Delivery**
- iPad orders: 1 in 90d ✗
- Sharing: 0 in 90d ✗
- Inventory flowing: 92 imports/90d ✓
- 1 of 3: **value_delivery_score = 33.3**

**Operational Health**
- Catalog: 2,958 / 3,328 = **88.9%**
- Import Health: 2 of 4 active types healthy (Customers and Products each errored on most recent run) → **50%**
- Freshness: 4 qualifying types; 3× 100, 1× 0 (Images 4.58×) → avg **75**
- operational_health_score = (88.9 + 50 + 75) / 3 = **71.3**

**Composite: 68.0 — Healthy**

- *"597 logins in 90 days from 23 active iPad users against just 3 enabled `org_users` rows. The 'enabled users' denominator is unreliable here — most active users have `disabled=true` on their org_users record. Effective engagement is high but the data needs cleanup before this score is trusted month over month."*
- *"Using 4 of 5 applicable features. Unused: Sales Data feed (configured on the org but no imports of that type in the last 180 days)."*
- *"Delivering value through 1 of 3 applicable channels. The iPad app is being opened (597 logins) but it is not producing orders (1 in 90 days) or sharing (0 in 90 days) — the team is logging in without converting that activity into output. Inventory data is flowing, so this is a usage problem, not a feed problem."*
- *"Catalog 89% complete. Imports: 2 of 4 active feed types healthy — Customers and Products each error on the most recent run. Freshness: 3 of 4 measurable feeds on cadence; Images feed is 4.6× overdue."*

---

### `dccl` — Donald Choi Canada (iPad+Catalog+Cart, 2024)

**Engagement**
- `logins_90d` = 551 (band 500–999 → 75)
- Active 9; enabled 11; ratio 81.8% (band 75–89% → 82)
- engagement_score = **78.5**

**Adoption**
- 7 applicable (iPad, SS, SR, Online Catalog, Online Ordering, Inventory, Sales Data).
- iPad(551) ✓, SS(12) ✓, SR(11) ✓, Online Catalog ✓, Online Ordering (orders_90d=77 incl. 4 non-iPad-source — adoption gate is "orders via portal origin OR portal_orders activity" — counts as ✓), Inventory(97) ✓, Sales Data(41) ✓.
- **adoption_score = 100.0**

**Value Delivery**
- iPad orders: 73 in 90d ✓
- Sharing: 1 in 90d ✗
- Online Catalog browsing: gate on, no `clicky_id` ✗
- Portal Ordering: `portal_orders` table count for dccl is **0 in 90d** (the 4 non-iPad orders show up in the `orders` table with `order_source != 'ipad'`, not in `portal_orders`). Per V3 §3 the source is `portal_orders`. ✗
- Sales Portal: not applicable
- Inventory: 97 imports/90d ✓
- 2 of 5: **value_delivery_score = 40.0**

**Operational Health**
- Catalog: 1,259 / 2,459 = **51.2%** (≈ 358 missing images plus ~1,165 with `net_price = 0`)
- Import Health: 4 of 7 active types healthy (Products, Product Stories, Sales Data errored on most recent run) → **57.1%**
- Freshness: 7 qualifying types; 3× 100, 4× 0 (Inventory 9.8×, Images 10.2×, Sales Data 8.9×, Taxonomies 36×) → avg **42.9**
- operational_health_score = (51.2 + 57.1 + 42.9) / 3 = **50.4**

**Composite: 67.2 — Healthy**

- *"551 logins in 90 days from 9 of 11 enabled users (82% active ratio). Activity is steady across a small but engaged rep base."*
- *"Using 7 of 7 applicable features. Nothing unused — the team is touching every product surface they're configured for."*
- *"Delivering value through 2 of 5 applicable channels. Portal ordering is enabled but the `portal_orders` table is empty for the org in 90 days — the 4 non-iPad orders in `orders` look like a different code path. Worth verifying whether the cart is fully live with customers. Online catalog browsing can't be scored — no Clicky ID configured."*
- *"Catalog 51% complete — ~358 products are missing images and ~1,165 have no `net_price` set (a Cart-bundle org shouldn't have that many priceless products). Imports: 4 of 7 active feed types healthy. Freshness: 4 active feeds are significantly overdue (Inventory 9.8×, Images 10.2×, Sales Data 8.9× their observed cadence). Operational Health is the primary drag — feeds are running on a tight cadence when they run but failing or stalling more than is acceptable for a Cart-tier account."*

---

### `kll` — Kuzco Lighting (Full Cart+Portal, 2022)

**Engagement**
- `logins_90d` = 1,759 (band 1,000–2,999 → 88)
- Active 60; enabled **795**; ratio 7.5% (band 1–24% → 20)
- engagement_score = **54.0**

> 795 enabled `org_users` is unusually high for a 60-active-user pattern — likely customer-facing portal users provisioned as `org_users` rather than internal reps. Worth a separate look at user-type segmentation in V3.1. Flagged.

**Adoption**
- 8 applicable (all features). Used: iPad(1,759), SS(20), SR(69), Online Catalog, Online Ordering(portal_orders_90d=10,564), Sales Portal(portal_orders_90d=10,564), Inventory(75). **Sales Data: no `Sales Data` import type in trailing 180d ✗.** `enable_sales_data=true` on the org but the feed isn't running.
- 7 of 8: **adoption_score = 87.5**

**Value Delivery**
- iPad orders: 9 in 90d ✗ (< 10 — under threshold by 1)
- Sharing: 12 in 90d ✓
- Online Catalog browsing: gate on, `clicky_id=101386790` set AND portal volume is huge → ✓ (heuristic)
- Portal Ordering: 10,564 portal_orders/90d ✓
- Sales Portal: 10,564 portal_orders/90d ✓
- Inventory: 75 imports/90d ✓
- 5 of 6: **value_delivery_score = 83.3**

**Operational Health**
- Catalog: **0 / 6,268 = 0%** under literal V3 logic — `contract_pricing_enabled=false`, every product's `net_price` is `NULL`. Pricing for kll lives in `prices_json` (price-level pricing), which V3 §4 does not consider. **This is the single biggest interpretation issue in this run.** Flagged.
- Import Health: 6 of 7 active types healthy (Customers errored on most recent run) → **85.7%**
- Freshness: 7 qualifying types; 4× 100, 1× 20 (Portal Orders 3.2×), 2× 0 (Products 63×, Images 1,106×, Product Stories 122×) → avg **45.7**

  Note: Images, Products, and Product Stories haven't run since January — they look "frozen". This may be intentional (image-fed externally) or a stalled feed.
- operational_health_score = (0 + 85.7 + 45.7) / 3 = **43.8**

**Composite: 67.2 — Healthy**

- *"1,759 logins in 90 days from 60 of 795 enabled users (7.5% active ratio). The denominator is suspicious — 795 enabled org_users is consistent with customer-side portal accounts being mixed into the `org_users` table. Real internal rep engagement is likely much higher than the 7.5% ratio suggests."*
- *"Using 7 of 8 applicable features. Unused: Sales Data feed (enabled on the org but no Sales Data imports in the last 180 days)."*
- *"Delivering value through 5 of 6 applicable channels. Portal is the engine (10,564 portal orders in 90d). iPad order volume sits at 9 in 90d — one shy of the 10-order threshold; this is a marginal miss, not a real gap."*
- *"Catalog 0% complete under the literal V3 check — but `net_price` is unused on this account; prices live in `prices_json` (price-level pricing). The literal score is misleading. Imports: 6 of 7 active feed types healthy. Freshness: Portal Orders, Inventory, Portal Invoices, and Customers are on cadence; Products / Images / Product Stories haven't run since January (look frozen). Operational Health is the primary drag, dominated by the spec-mismatch on price."*

---

### `bp` — Buster & Punch (iPad-only by MAL, 2024)

**Engagement**
- `logins_90d` = 684 (band 500–999 → 75)
- Active 41; enabled 81; ratio 50.6% (band 50–74% → 65)
- engagement_score = **70.0**

**Adoption**
- bp is iPad-only per the MAL but has `mobile_sites.enable_online_catalog=true` and `enable_online_ordering=true`. Per V3 §2, applicability is the `mobile_sites` flag, not the MAL bundle — so both features ARE applicable. Flagged.
- 7 applicable (iPad, SS, SR, Online Catalog, Online Ordering, Inventory, Sales Data). `enable_sales_portal=false` → Sales Portal not applicable.
- Used: iPad(684) ✓, SS(6) ✓, SR(17) ✓, Online Catalog ✓, Online Ordering (`portal_orders_90d=0` AND all 4 `orders_90d` rows have `order_source='ipad'` → ✗), Inventory(75) ✓, Sales Data (no Sales Data type in 180d → ✗).
- 5 of 7: **adoption_score = 71.4**

**Value Delivery**
- iPad orders: 4 in 90d ✗
- Sharing: 2 in 90d ✗
- Online Catalog browsing: gate on, no `clicky_id` ✗
- Portal Ordering: `portal_orders_90d=0` ✗
- Sales Portal: not applicable
- Inventory: 75 imports/90d ✓
- 1 of 5: **value_delivery_score = 20.0**

**Operational Health**
- Catalog: 1,870 / 2,360 = **79.2%** (`contract_pricing_enabled=true`, so price check skipped per spec — 490 products missing images)
- Import Health: 4 of 5 active types healthy (Customers errored on most recent run) → **80%**
- Freshness: 4 qualifying types; 3× 100, 1× 20 (Images 3.91×) → avg **80**
- operational_health_score = (79.2 + 80 + 80) / 3 = **79.7**

**Composite: 60.3 — Healthy**

- *"684 logins in 90 days from 41 of 81 enabled users (51% active ratio). Activity is steady but skewed — about half the seat base is dormant."*
- *"Using 5 of 7 applicable features. Unused: Online Ordering (the mobile site has `enable_online_ordering=true` but the `portal_orders` table is empty and no orders have `order_source != 'ipad'` in 90 days — flag for CS, this is a configured-but-not-live cart) and Sales Data feed (configured on the org but no imports in 180 days). Note: MAL has bp as iPad-only but the mobile_site is configured as if it were Cart+Catalog — see Spec Flags."*
- *"Delivering value through 1 of 5 applicable channels. The team is logging in but not producing observable output: 4 iPad orders in 90 days, 2 shared resources, no portal activity. Catalog completeness skipped the price check (contract pricing enabled), so the catalog look-and-feel is in better shape than the output suggests."*
- *"Catalog 79% complete (contract pricing in use — price check skipped). Imports: 4 of 5 active feed types healthy; Customers errored on most recent run. Freshness: Images is moderately late (3.9× expected gap); other 3 measurable feeds on cadence."*

---

### `mfc` — Morgan Fabrics (iPad+Catalog, 2012)

**Engagement**
- `logins_90d` = 116 (band 50–199 → 40)
- Active 10; enabled 63; ratio 15.9% (band 1–24% → 20)
- engagement_score = **30.0**

**Adoption**
- 5 applicable (iPad, SS, SR, Online Catalog, Sales Data). Inventory: no Inventory imports in the trailing 180 days and the last Inventory import overall was June 2024 — feed is dormant. Treated as NOT applicable (consistent with the Operational Health "active import type" definition, but the spec is technically silent on Inventory Management applicability for orgs whose feed lapsed years ago — flagged).
- Used: iPad(116), SS(46), SR(54), Online Catalog ✓. Sales Data: `enable_sales_data=true` but no Sales Data imports in 180d → ✗.
- 4 of 5: **adoption_score = 80.0**

**Value Delivery**
- iPad orders: 0 in 90d ✗
- Sharing: 3 in 90d ✓ (exactly at threshold)
- Online Catalog browsing: gate on, `clicky_id=101069835` set, but no portal activity and Clicky API not directly queryable here → treated as ✗ conservatively. Flagged.
- Inventory: not applicable
- 1 of 3: **value_delivery_score = 33.3**

**Operational Health**
- Catalog: **0 / 5,257 = 0%** under literal V3 — `contract_pricing_enabled=false`, every product has `net_price=NULL`, prices live in `prices_json` (same situation as `kll`). Also only 1,508 / 5,257 products have a long_description (29%) — so even if pricing were fixed, the description gap alone would hold this near 29%.
- Import Health: 2 of 2 active types healthy → **100%**
- Freshness: 2 qualifying types; both 20 (Products 3.35×, Images 3.88×) → avg **20**
- operational_health_score = (0 + 100 + 20) / 3 = **40.0**

**Composite: 45.8 — Watch**

- *"116 logins in 90 days from 10 of 63 enabled users (16% active ratio). Most of the seat base is silent — only ~1 user in 6 is actively logging in. Worth investigating whether reps are still working in the iPad app at all."*
- *"Using 4 of 5 applicable features. Unused: Sales Data feed (enabled on the org but no Sales Data imports in 180 days). Note: Inventory Management was excluded from applicability — last Inventory import was June 2024 — see Spec Flags re: how to treat long-dormant feeds."*
- *"Delivering value through 1 of 3 applicable channels. Zero iPad orders in 90 days for a 2012-cohort account — the most concerning signal in this report. Online catalog browsing has a Clicky ID set but no measurable evidence of engagement in this run."*
- *"Catalog 0% complete under the literal V3 check — pricing is price-level (in `prices_json`), not `net_price`, so the price check fires false. Even with that fixed, only 29% of products carry a `long_description`. Imports: 2 of 2 active feed types healthy, but Products and Images are each 3–4× overdue against their observed cadence. Operational Health is the primary drag, with description coverage and feed freshness both real and the price metric an artifact."*

---

## Spec Flags

The following issues either changed how I interpreted a rule, would have changed a score, or are situations the V3 README doesn't explicitly cover. Each is a candidate for V3.1 clarification.

1. **`net_price = 0` for orgs using price-level pricing (kll, mfc).** V3 §4 catalog completeness gives a pass on the price check only when `contract_pricing_enabled = true`. Both `kll` and `mfc` set `contract_pricing_enabled=false`, store pricing in `products.prices_json` (price-level pricing), and have `net_price IS NULL` on every active product. Under the literal V3 rule both score **0%** on Catalog Completeness — but neither is actually broken, they just use a third pricing model the spec doesn't mention. Recommendation: extend the V3 pass-rule to also accept `prices_json IS NOT NULL AND prices_json != '{}'` (or equivalent — e.g., a non-null `starts_at`) OR add a `pricing_model` flag on `organizations` and gate on it.

2. **`active_user_ratio > 100%` (fsf 125%, hf 767%).** The denominator (`org_users WHERE disabled=false`) can be smaller than the numerator (distinct `user_id` in `login_events` over 90d) when active users have their `disabled` flag set to `true`. V3 §1 doesn't define behavior > 100%. I capped at 100% for scoring. Recommendation: explicitly state the cap, and add a `denominator_quality` flag when ratio > 100% so CS knows the disabled flag for that org is stale.

3. **`bp` has iPad-only bundle in MAL but Cart-style `mobile_sites` config.** `enable_online_catalog=true` and `enable_online_ordering=true` on the mobile site, but the MAL `stack` is `iPad-only`. V3 §2 says applicability is driven by the `mobile_sites` flag, not the bundle — so I treated Online Catalog and Online Ordering as applicable. That is consistent with the literal spec, but it produces an adoption gap that the org may not actually owe (they haven't bought Cart). Recommendation: cross-check `subscriptions` against `mobile_sites` flags; flag mismatches as data hygiene rather than usage gaps.

4. **Ghost-account column not defined by V3.** The request asks for `ghost_account` in the output, but Health V3 README v3.0.0 does not define it. I used a transparent heuristic — `engagement_score < 30` AND `active_user_ratio < 25%` AND `orders_90d < 10` AND `shared_resources_90d < 3` — and none of the 10 orgs hit all four (mfc is closest, missing on sharing at exactly the 3-resource threshold). Recommendation: V3.1 should define this field or remove it from the output contract.

5. **Clicky page-view data is not directly queryable in this run.** V3 §3 Value Delivery's "Catalog browsing / online engagement" channel sources Clicky page views, but Clicky lives behind a per-org Clicky ID and is not in BigQuery or Postgres. For orgs with a populated `mobile_sites.clicky_id` AND strong portal activity (`fsf`, `kll`) I credited the channel by heuristic. For orgs whose gate is on but `clicky_id` is empty (`cci`, `jc`, `dccl`, `bp`) or `mobile_sites.clicky_id` is set but portal activity is zero (`mfc`), I marked the channel as not delivering. Recommendation: either land Clicky data into BigQuery for cohort-scale querying or replace the Clicky signal with a Postgres-derivable proxy (e.g., `portal_orders` table activity).

6. **HelpScout severity tag vocabulary doesn't include S1/S2 today.** V3 §5 lists "S1 or S2 severity" as a fire trigger. Querying the live `helpscout.conversations` tag corpus shows only `s3 - medium` and `s4 - low` in current use; L3/L4 escalation tags exist but no S1/S2. So the S1/S2 leg of the fire flag can never fire on present data. None of the 10 orgs have any open L3/L4 conversation either (the 11 open L3 conversations all map to `palecek.com`, `gabriellawhite.com`, `craftmade.com`, `charlestonforge.com`, `alfrescohome.com`, `visualcomfort.com`, `universalfurniture.com`, `wildwoodhome.com`, `savoyhouse.com`, and `samsonmktg.com`). Recommendation: confirm with Support whether S1/S2 are deprecated, drop them from the rule, or add the actual current severity vocabulary.

7. **"Inventory Management" applicability for orgs whose feed lapsed years ago (`mfc`).** V3 §2 defines applicability as "`import_events` history contains Inventory type" with no time bound. `mfc` has 4 Inventory imports — all in May–June 2024, almost two years ago. I treated this as NOT applicable (mirroring Operational Health's "active = run in trailing 180d" definition). Under a literal "history contains" read it would be applicable + unused, dropping the adoption score from 80 → 66.7. Recommendation: state the time bound in §2 explicitly.

8. **Online Ordering: V3 §2 vs §3 use different signals.** §2 Adoption gate is "`orders_90d > 0 via portal origin` OR `portal_orders activity`". §3 Value Delivery threshold is "portal orders activity in 90d > 0". For `dccl` this matters: 4 orders show up in `orders` with `order_source != 'ipad'` but `portal_orders` is empty — so the org counts as "adopted" but "not delivering value". The asymmetry is intentional per the literal spec but worth calling out — it makes the two scores diverge for the same underlying channel. Recommendation: confirm intent or unify on `portal_orders` only.

9. **"Order volume (iPad)" label vs. `orders_90d` field (V3 §3).** The Value Delivery matrix labels the row "Order volume (iPad)" but the threshold uses `orders_90d` without an `ipad_` prefix. I interpreted as iPad-source orders (consistent with the label) and used `LOWER(order_source) = 'ipad'`. This matters for `kll`: total `orders_90d` = 71 (above 10) but `ipad_orders_90d` = 9 (below 10). Under the label-first read this channel is unmet for `kll`; under the field-first read it is met. Recommendation: clarify which one the spec means.

10. **Mean gap used as freshness denominator instead of median (V3 §4 sub-signal 3).** V3 specifies median gap. The Postgres MCP rejected the `PERCENTILE_CONT() WITHIN GROUP (ORDER BY ...)` query (validator error, not a permissions problem), so I substituted mean gap = `(last_run - first_run) / (n - 1)`. For nearly-periodic feeds the two are identical to two decimal places; for bursty feeds (e.g., `fsf` Option Images had 20 runs in 2 days then nothing — mean gap ≈ 0.1 days, days_since_last ≈ 24 days → ratio 242×) the mean over-penalizes a feed that has clearly stopped. The score for those types lands at 0 either way (median would also be ~0.1 days), so the directional answer is unchanged, but the bursty case in §6 of the README would benefit from a minimum-gap floor (e.g., `max(median_gap, 1.0 day)`).

11. **Bursty-feed degenerate freshness (`jc` Matrix Options 3 runs in 6 hours, `fsf` Option Images 20 runs in 2 days).** Same root cause as #10 but worth a separate note: feeds that fire in a tight burst (initial load, then quiet) get a freshness ratio in the hundreds even when they're behaving exactly as expected. Recommendation: V3.1 should add a minimum median floor (1 day?) or an "initial-load" detection so initial-loaded feeds aren't unfairly stale-scored.

12. **`org_users` denominator inflated by customer-facing portal accounts (`kll` 795 enabled users; `fsf` 730 total).** Same family of issues as #2 but on the supply side. For Cart/Portal orgs the `org_users` table appears to include customer accounts provisioned for portal login, not just internal reps. This drags the ratio score (`kll` 7.5% → score 20). Recommendation: either filter `org_users` by `user_type` (e.g., exclude `customer` types) or use a rep-only count from a different surface. The V2 internal-domain exclusion list referenced in `Health V2/QUERIES.md` Q-PG-USERS is a related but distinct mechanism.

13. **No `subscriptions` data was used.** V3 §8 lists `subscriptions` + `subscription_plans` as the source for "bundle (derived from active subscriptions)", but I sourced `bundle` from the MAL CSV per Q-MAL convention. The MAL bundle and the subscriptions table can disagree (see #3 — bp). Recommendation: V3.1 should pick one authoritative source and call out the other as reference/diagnostic.

14. **HelpScout domain-to-org mapping not regenerated in this run.** Per V3 §5, the fire-flag check requires a domain map. I bypassed the map by checking that no domain in the open L3/L4 conversations matched any of the 10 orgs' user-email domains. For a full V3 run, the mapping should be regenerated and persisted (Q-PG-DOMAIN in `Health V2/QUERIES.md`). I recorded `support_data_available = true` for all 10 because the BigQuery query succeeded and no flag matched; a stricter read would require a confirmed domain entry for each org before claiming "available".

15. **`mp_item_email_drafted` / `mp_document_email_drafted` not used.** The instructions told me to confirm BigQuery table names and filters for these events. The V3 README (the sole authority for scoring) doesn't actually reference them — sharing in V3 is driven by Postgres `shared_resources`, not by Mixpanel email-draft events — so I confirmed the mapping (`mixpanel.events`, `event_name IN ('item_email_drafted', 'document_email_drafted')`, attribution via `current_organization_shortname` per Health V2 §2) but did not query them. Recommendation: if V3.1 wants to bring the Mixpanel sharing signal back into the model, wire `shared_resources_90d` + `mp_item_email_drafted_90d` + `mp_document_email_drafted_90d` into the same point.
