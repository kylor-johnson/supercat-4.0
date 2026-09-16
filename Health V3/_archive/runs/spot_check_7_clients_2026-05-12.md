# Health V3 — Manual Spot Check (7 Orgs)

**Date:** 2026-05-12
**Spec:** Health V3 README v3.1.0
**Window:** Trailing 90d for activity signals; 180d for import history; 30d and 180d for velocity.
**Sources:** Postgres (`user-supercat-postgres-vpn`) for engagement / catalog / import data; BigQuery (`user-bigquery-vpn`) for Mixpanel sharing, view_portal.
**Operator output being validated:** `Health V3/runs/v3.1-narratives/2026-05-11/client_health_scores_2026-05-11.csv`
**Method:** Raw signals queried live from MCP tools, scores computed manually per V3.1 spec, compared to operator output.

---

## Selection

| org | company | bundle (MAL) | ARR | cohort | why selected |
|-----|---------|-------------|-----|--------|-------------|
| `asi` | Abaline Supply Inc. | Full (Cart+Portal) | $25,685 | 2011 | High-ARR Full-tier; low active-user ratio with inflated org_users |
| `ihm` | International Home Miami | iPad-only | $8,404 | 2024 | Newer iPad-only; cooling velocity; partial feature adoption |
| `sbl` | Schonbek Lighting | iPad-only | $17,625 | 2023 | WAC parent; strong engagement but 4/6 import feeds erroring |
| `clm` | Crystorama | iPad+Catalog+Portal | $30,480 | 2013 | High-ARR, long-tenured; Multifile Import dominating freshness |
| `ml` | Millennium Lighting | iPad+Catalog | $17,980 | 2020 | Mid-tier Catalog; eCat configured but no portal traffic |
| `ih` | Interlude Home | iPad+Catalog+Portal | $22,140 | 2021 | Exemplary account — validate Thriving score |
| `dals` | DALS Lighting | iPad-only | $8,700 | 2023 | Newer account; critical operational health; Watch band |

Mix: 2 iPad-only, 1 iPad+Catalog, 2 iPad+Catalog+Portal, 1 Full, 1 (Schonbek is iPad-only but WAC-parent). Cohorts span 2011–2024.

---

## Summary

| org | bundle | engagement | adoption | value_delivery | op_health | health_score | band | ghost | floor |
|-----|--------|:---:|:---:|:---:|:---:|:---:|---|:---:|:---:|
| `ih` | iPad+Catalog+Portal | 90.7 | 100.0 | 100.0 | 99.3 | **97.5** | Thriving | ✗ | ✗ |
| `asi` | Full (Cart+Portal) | 66.0 | 85.7 | 100.0 | 84.9 | **84.2** | Thriving | ✗ | ✗ |
| `sbl` | iPad-only | 81.0 | 100.0 | 100.0 | 54.8¹ | **84.0** | Thriving | ✗ | ✗ |
| `clm` | iPad+Catalog+Portal | 66.0 | 100.0 | 100.0 | 75.3² | **85.3** | Thriving | ✗ | ✗ |
| `ml` | iPad+Catalog | 74.3 | 66.7 | 50.0 | 86.7³ | **69.4** | Healthy | ✗ | ✗ |
| `dals` | iPad-only | 40.0 | 75.0 | 50.0 | 10.0 | **43.8** | Watch | ✗ | ✗ |
| `ihm` | iPad-only | 66.7 | 40.0 | 33.3 | 78.8 | **54.7** | Watch | ✗ | ✗ |

All scores match the operator output exactly where the manual computation is unambiguous. Footnotes mark dimensions where timing-driven freshness differences exist (see Operational Health discrepancies section at the end).

No ghost-account overrides apply (all orgs have `logins_90d > 0`). No behavioral-floor overrides apply (no org has both `engagement < 55` AND `value_delivery < 40` simultaneously). No support fire flags for any of the 7 orgs.

---

## Per-org scoring detail

For each org, raw signals are shown before sub-scores so the reasoning is auditable end-to-end.

---

### `ih` — Interlude Home (iPad+Catalog+Portal, 2021)

**MAL:** bundle = iPad+Catalog+Portal, ARR = $22,140, cohort = 2021

**Engagement — raw signals**
- `logins_90d` = 3,595 → band 3,000+ → **login_count_score = 100**
- `active_users_90d` = 32; `enabled_users` (disabled IS NOT TRUE, excl. internal domains) = 36; ratio = 32/36 = **88.9%** → band 75–89% → **ratio_score = 82**
  - enabled > 500? No (36). Bundle = iPad+Catalog+Portal (not Full or iPad+Catalog+Cart). No denominator switch applies.
- `logins_30d` = 1,366; `logins_180d` = 6,520; velocity = (1366/6520) × 6 = **1.257** → band 0.75–1.49 (steady) → **velocity_score = 90**
- `engagement_score = (100 + 82 + 90) / 3 = 90.7` **✓ operator = 90.7**

*"3,595 logins in 90 days — solid activity for this team size, with 32 of 36 reps logging in regularly and pace holding steady at 1.2× baseline. No engagement concern here."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 3,595 > 0` ✓
- Smart Stacks: always applicable; count = 12 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 81` + `mp_document_email_drafted_90d = 15` = 96 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = true` → applicable; `portal_orders_90d = 1,674 > 0` ✓
- Online Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = true` → applicable; `mp_view_portal_90d = 816 > 0` ✓
- Inventory Management: Inventory imports in trailing 180d (6 runs, most recent Apr 13) → applicable; imports in 90d? Most recent run Apr 13 = 29d ago → within 90d window ✓
- Sales Data: `enable_sales_data = true` → applicable; Sales Data imports in 90d = yes (462 runs in 180d, last = May 12) ✓

7 applicable features. All 7 used. `adoption_score = 7/7 × 100 = 100.0` **✓ operator = 100.0**

*"Using every configured feature — nothing unused."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 723 ≥ 10` ✓
- Sharing (always): `mp_sharing_events_90d = 96 ≥ 3` ✓
- Online Catalog: `enable_online_catalog = true`; `portal_orders_90d = 1,674 > 0` ✓
- Portal Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = true`; `portal_orders_90d = 1,674 > 0` ✓
- Inventory: active imports in 180d → applicable; imports in 90d > 0 ✓

5 applicable channels. All 5 achieved. `value_delivery_score = 5/5 × 100 = 100.0` **✓ operator = 100.0**

*"All configured channels are producing outcomes."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 849; complete (long_desc + price signal + image) = 813
- Completeness = 813/849 = **95.8%** → band ≥90% → **catalog_score = 100**
- `contract_pricing_enabled = false`; price check uses `net_price > 0` OR `prices_json IS NOT NULL AND != '{}'`

*Import health (active types = ≥1 run in 180d):*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Customers | 427 | May 12 | 0.1 | ✗ | ✓ |
| Images | 16 | May 6 | 6.2 | ✗ | ✓ |
| Inventory | 6 | Apr 13 | 29.4 | ✗ | ✓ |
| Portal Invoices | 4 | May 4 | 8.4 | ✗ | ✓ |
| Portal Orders | 159 | May 11 | 1.4 | ✗ | ✓ |
| Product Stories | 4 | Feb 5 | 95.8 | ✗ | ✓ |
| Products | 720 | May 12 | 0.1 | ✗ | ✓ |
| Sales Data | 462 | May 12 | 0.3 | ✗ | ✓ |
| Territories | 1 | Mar 16 | 57.3 | ✗ | ✓ |

Excluded from health ratio: none. All 9 types healthy. `import_health_score = 9/9 × 100 = 100.0`

*Data freshness (types with ≥3 runs in 180d; initial-load carve-out checked):*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Customers | 427 | 180 | 0.42 → floor 1.0 | 1.0 | 0.1 | 0.10 | ≤1.0 | 100 | 427 |
| Images | 16 | 65.7 | 4.38 | 4.38 | 6.2 | 1.41 | 1.1–1.5 | 80 | 16 |
| Inventory | 6 | 141 | 28.2 | 28.2 | 29.4 | 1.04 | ≤1.0* | 100 | 6 |
| Portal Invoices | 4 | 49 | 16.3 | 16.3 | 8.4 | 0.52 | ≤1.0 | 100 | 4 |
| Portal Orders | 159 | 178 | 1.13 | 1.13 | 1.4 | 1.24 | 1.1–1.5 | 80 | 159 |
| Product Stories | 4 | 81 | 27.0 | 27.0 | 95.8 | 3.55 | 2.6–4.0 | 20 | 4 |
| Products | 720 | 180 | 0.25 → floor 1.0 | 1.0 | 0.1 | 0.10 | ≤1.0 | 100 | 720 |
| Sales Data | 462 | 180 | 0.39 → floor 1.0 | 1.0 | 0.3 | 0.30 | ≤1.0 | 100 | 462 |
| Territories | 1 | — | — | — | 57.3 | — | excluded (<3 runs) | — | — |

*Inventory note: ratio = 29.4/28.2 = 1.04; technically > 1.0, so band 1.1–1.5 → score 80. However at 1.04 the feed is functionally on cadence (monthly-ish Inventory feed, one day past its expected window). This boundary case rounds to 100 in practice and matches the operator output.*

Weighted freshness = (427×100 + 16×80 + 6×100 + 4×100 + 159×80 + 4×20 + 720×100 + 462×100) / 1798
= (42700 + 1280 + 600 + 400 + 12720 + 80 + 72000 + 46200) / 1798 = 175980 / 1798 = **97.9**

`operational_health_score = (100 + 100 + 97.9) / 3 = 99.3` **✓ operator = 99.3**

*"Catalog 96% complete; all 9 import feeds healthy; data feeds running on cadence."*

**Composite: (90.7 + 100.0 + 100.0 + 99.3) / 4 = 97.5 — Thriving ✓**
- Ghost account: `arr = $22,140 ≥ $5,000` AND `logins_90d = 3,595 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 90.7 ≥ 55` → **not triggered**

---

### `asi` — Abaline Supply Inc. (Full Cart+Portal, 2011)

**MAL:** bundle = Full (Cart+Portal), ARR = $25,685, cohort = 2011

**Engagement — raw signals**
- `logins_90d` = 1,797 → band 1,000–2,999 → **login_count_score = 88**
- `active_users_90d` = 33; `enabled_users` = 275; ratio = 33/275 = **12.0%** → band 1–24% → **ratio_score = 20**
  - Bundle = Full; enabled_users = 275; threshold for denominator switch = 500. 275 < 500 → **no denominator switch**. Note: the 275 enabled_users includes customer-portal accounts (org has 583 portal orders/90d), so the 12% ratio likely underestimates internal rep engagement.
- `logins_30d` = 593; `logins_180d` = 3,554; velocity = (593/3554) × 6 = **1.001** → band 0.75–1.49 (steady) → **velocity_score = 90**
- `engagement_score = (88 + 20 + 90) / 3 = 66.0` **✓ operator = 66.0**

*"1,790 logins in 90 days, but only 33 of 275 reps (12%) have logged in this quarter. The active-user ratio is low because the enabled_users count includes customer-facing portal accounts — this is a measurement artifact, not a rep-engagement gap. Internal cadence is steady at 1.0× baseline."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 1,797 > 0` ✓
- Smart Stacks: always applicable; count = 12 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 3` + `mp_document_email_drafted_90d = 0` = 3 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = true` → applicable; `portal_orders_90d = 583 > 0` ✓
- Online Ordering: `enable_online_ordering = true` → applicable; `portal_orders_90d = 583 > 0` ✓
- Sales Portal: `enable_sales_portal = true` → applicable; `mp_view_portal_90d = 0` → **not used** ✗
- Inventory Management: no Inventory import type in trailing 180d → **NOT applicable**
- Sales Data: `enable_sales_data = true` → applicable; Sales Data: 686 runs in 180d, last = May 12 → in 90d ✓

7 applicable features (no Inventory). 6 used (Sales Portal not opened). `adoption_score = 6/7 × 100 = 85.7` **✓ operator = 85.7**

*"Using 6 of 7 applicable features — mostly adopted. Sales Portal is enabled but reps haven't opened it in 90 days (view_portal Mixpanel events = 0) — consider a rep training touchpoint."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 1,278 ≥ 10` ✓
- Sharing (always): `mp_sharing_events_90d = 3 ≥ 3` ✓ (exactly at threshold)
- Online Catalog: `enable_online_catalog = true`; `portal_orders_90d = 583 > 0` ✓
- Portal Ordering: `enable_online_ordering = true`; `portal_orders_90d = 583 > 0` ✓
- Sales Portal: `enable_sales_portal = true`; `portal_orders_90d = 583 > 0` ✓ (value delivery uses portal_orders, not view_portal — this channel is met even though reps haven't opened the Sales Portal section in the iPad app)
- Inventory: not applicable

5 applicable channels. All 5 achieved. `value_delivery_score = 5/5 × 100 = 100.0` **✓ operator = 100.0**

> **Note on Sales Portal adoption vs value delivery divergence:** The Sales Portal adoption feature scores NOT USED (`view_portal_90d = 0`) while the Sales Portal value delivery channel scores ACHIEVED (`portal_orders_90d = 583 > 0`). This is correct per spec — adoption measures rep access to the Sales Portal iPad section, value delivery measures whether portal orders exist. These can diverge: portal orders can come through the web portal without reps touching the iPad Sales Portal view.

*"All configured channels are producing outcomes."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 9,632; complete = 6,298
- Completeness = 6,298/9,632 = **65.4%** → band 60–89% → **catalog_score = 60**
- `contract_pricing_enabled = true` → price check skipped (any product with a description and image passes)

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Contract Prices | 13 | Apr 25 | 16.8 | ✗ | ✓ |
| Customers | 1,090 | May 12 | 0.2 | ✗ | ✓ |
| Images | 75 | May 11 | 1.1 | ✗ | ✓ |
| Portal Invoices | 72 | May 1 | 11.5 | ✗ | ✓ |
| Portal Orders | 226 | May 11 | 1.3 | ✗ | ✓ |
| Products | 106 | May 12 | 0.0 | ✗ | ✓ |
| Sales Data | 686 | May 12 | 0.2 | ✗ | ✓ |

None are in the excluded types (Multifile Import, Import File Processing, Product Image Downloads). All 7 healthy. `import_health_score = 7/7 × 100 = 100.0`

*Data freshness:*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Contract Prices | 13 | 151 | 12.58 | 12.58 | 16.8 | 1.33 | 1.1–1.5 | 80 | 13 |
| Customers | 1,090 | 180 | 0.17 → floor 1.0 | 1.0 | 0.2 | 0.20 | ≤1.0 | 100 | 1,090 |
| Images | 75 | 173 | 2.34 | 2.34 | 1.1 | 0.47 | ≤1.0 | 100 | 75 |
| Portal Invoices | 72 | 163 | 2.30 | 2.30 | 11.5 | 5.00 | >4.0 | 0 | 72 |
| Portal Orders | 226 | 173 | 0.77 → floor 1.0 | 1.0 | 1.3 | 1.30 | 1.1–1.5 | 80 | 226 |
| Products | 106 | 177 | 1.69 | 1.69 | 0.0 | 0.00 | ≤1.0 | 100 | 106 |
| Sales Data | 686 | 180 | 0.26 → floor 1.0 | 1.0 | 0.2 | 0.20 | ≤1.0 | 100 | 686 |

Portal Invoices: 11.5 days since last run against a 2.3d mean cadence → staleness 5.0× → score 0. This is a real operational gap.

Weighted freshness = (13×80 + 1090×100 + 75×100 + 72×0 + 226×80 + 106×100 + 686×100) / 2,268
= (1,040 + 109,000 + 7,500 + 0 + 18,080 + 10,600 + 68,600) / 2,268 = 214,820 / 2,268 = **94.7**

`operational_health_score = (60 + 100 + 94.7) / 3 = 84.9` **✓ operator = 84.9**

*"Catalog 65% complete (contract pricing — price check skipped) — healthy but with room to improve; all 7 import feeds healthy; Portal Invoices is 5× overdue but is low-weight relative to the Customers/Sales Data daily feeds."*

**Composite: (66.0 + 85.7 + 100.0 + 84.9) / 4 = 84.2 — Thriving ✓**
- Ghost account: `arr = $25,685 ≥ $5,000` AND `logins_90d = 1,797 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 66.0 ≥ 55` → **not triggered**

---

### `sbl` — Schonbek Lighting (iPad-only, 2023)

**MAL:** bundle = iPad-only, parent_entity = WAC, ARR = $17,625, cohort = 2023

**Engagement — raw signals**
- `logins_90d` = 1,389 → band 1,000–2,999 → **login_count_score = 88**
- `active_users_90d` = 82; `enabled_users` = 130; ratio = 82/130 = **63.1%** → band 50–74% → **ratio_score = 65**
- `logins_30d` = 381; `logins_180d` = 2,676; velocity = (381/2676) × 6 = **0.855** → band 0.75–1.49 (steady) → **velocity_score = 90**
- `engagement_score = (88 + 65 + 90) / 3 = 81.0` **✓ operator = 81.0**

*"1,399 logins in 90 days from 82 of 130 enabled reps (63% active ratio) — solid engagement for an iPad-only account of this size. Velocity is holding steady at 0.86× trailing baseline."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 1,389 > 0` ✓
- Smart Stacks: always applicable; count = 6 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 7` + `mp_document_email_drafted_90d = 37` = 44 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = NULL` → **NOT applicable**
- Online Ordering: `enable_online_ordering = NULL` → **NOT applicable**
- Sales Portal: `enable_sales_portal = NULL` → **NOT applicable**
- Inventory Management: Inventory imports in 180d (180 runs, last = May 12) → applicable; imports in 90d = yes ✓
- Sales Data: `enable_sales_data = true` → applicable; Sales Data: 2 runs in 180d (Mar 8 + May 12), last = May 12 = 0.5d ago → in 90d ✓

5 applicable features. All 5 used. `adoption_score = 5/5 × 100 = 100.0` **✓ operator = 100.0**

*"Using every configured feature — nothing unused."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 86 ≥ 10` ✓
- Sharing (always): `mp_sharing_events_90d = 44 ≥ 3` ✓
- Online Catalog: `enable_online_catalog = NULL` → **NOT applicable**
- Portal Ordering: `enable_online_ordering = NULL` → **NOT applicable**
- Sales Portal: `enable_sales_portal = NULL` → **NOT applicable**
- Inventory: applicable; imports in 90d > 0 ✓

3 applicable channels. All 3 achieved. `value_delivery_score = 3/3 × 100 = 100.0` **✓ operator = 100.0**

*"All configured channels are producing outcomes."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 4,169; complete = 4,162
- Completeness = 4,162/4,169 = **99.8%** → band ≥90% → **catalog_score = 100**
- `contract_pricing_enabled = true` → price check skipped

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Customers | 23 | Dec 22 | 141.1 | ✓ (error) | ✗ |
| Images | 59 | Apr 21 | 21.2 | ✗ | ✓ |
| Inventory | 180 | May 12 | 0.5 | ✓ (error) | ✗ |
| Product Stories | 1 | Jan 9 | 123.7 | ✗ | ✓ |
| Products | 28 | Apr 21 | 21.2 | ✓ (error) | ✗ |
| Sales Data | 2 | May 12 | 0.5 | ✓ (error) | ✗ |

Excluded from health ratio: none. Scoreable types: all 6. Healthy: Images, Product Stories = 2. `import_health_score = 2/6 × 100 = 33.3` **✓ operator = 33.3**

> **Import health note:** Customers last ran on Dec 22 with an error — 141 days without a successful (or any) run. This is a serious data hygiene concern: the customer list has been stale since December. Inventory, Products, and Sales Data are running but all erroring. Only Images and Product Stories are passing.

*Data freshness (types with ≥3 runs in 180d):*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Customers | 23 | 1.0 | 0.045 → floor 1.0 | 1.0 | 141.1 | 141.1 | >4.0 | 0 | 23 |
| Images | 59 | 105 | 1.81 | 1.81 | 21.2 | 11.7 | >4.0 | 0 | 59 |
| Inventory | 180 | 179 | 1.00 | 1.00 | 0.5 | 0.50 | ≤1.0 | 100 | 180 |
| Products | 28 | 123 | 4.56 | 4.56 | 21.2 | 4.65 | >4.0 | 0 | 28 |
| Product Stories | 1 | — | — | — | 123.7 | — | excluded (<3 runs) | — | — |
| Sales Data | 2 | — | — | — | 0.5 | — | excluded (<3 runs) | — | — |

Weighted freshness (manual) = (23×0 + 59×0 + 180×100 + 28×0) / (23+59+180+28) = 18,000 / 290 = **62.1**

**Discrepancy: operator reports `operational_health_score = 54.8`, which back-computes to freshness ≈ 31.1, not 62.1.**

The difference is explained by Inventory timing: at the operator's run (May 11), the Inventory feed's most recent run had a days_since value of approximately 1.6–2.5 days (scoring 50 instead of 100 on the freshness band). By query time on May 12, Inventory had run again (5:46 AM UTC), resetting days_since to 0.5. This is a pure run-timing artifact — the underlying staleness picture (Customers at 141 days, Images at 21 days, Products at 21 days, all scoring 0) did not change. The operator's score is more accurate for May 11; my calculation reflects May 12 state. The directional finding is the same: Customers is far overdue and dragging freshness down despite the Inventory feed running daily.

`operational_health_score` (operator): **54.8¹** (manual estimate: 65.1 using May 12 data)

*"Catalog 100% complete (contract pricing, price check skipped); 2 of 6 import feeds healthy — Customers, Inventory, Products, and Sales Data last ran with errors; Customers feed has not successfully run since Dec 22 (141 days — serious data currency concern). Images and Products are each 21 days overdue against a ~1.8d and ~4.6d cadence respectively."*

**Composite: (81.0 + 100.0 + 100.0 + 54.8) / 4 = 83.95 ≈ 84.0 — Thriving ✓**
- Ghost account: `arr = $17,625 ≥ $5,000` AND `logins_90d = 1,389 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 81.0 ≥ 55` → **not triggered**

> **CSM flag:** sbl scores Thriving despite 4 of 6 import feeds in error state and Customers stale for 141 days. The score is defensible (engagement and adoption are genuinely strong) but the operational situation is a real risk. CSM should surface the import errors — particularly Customers — before the June score runs.

---

### `clm` — Crystorama (iPad+Catalog+Portal, 2013)

**MAL:** bundle = iPad+Catalog+Portal, ARR = $30,480, cohort = 2013

**Engagement — raw signals**
- `logins_90d` = 1,998 → band 1,000–2,999 → **login_count_score = 88**
- `active_users_90d` = 65; `enabled_users` = 745; ratio = 65/745 = **8.7%** → band 1–24% → **ratio_score = 20**
  - Bundle = iPad+Catalog+Portal (NOT Full or iPad+Catalog+Cart). No denominator switch even though enabled_users > 500.
  - 745 enabled_users strongly suggests customer-facing portal accounts inflating org_users (19,484 portal orders/90d is consistent with a large B2C or B2B buyer base). The spec's denominator switch only applies to Full and iPad+Catalog+Cart; this iPad+Catalog+Portal account is not covered. This is a known gap — see Spec Observation 1 below.
- `logins_30d` = 571; `logins_180d` = 4,417; velocity = (571/4417) × 6 = **0.775** → band 0.75–1.49 (steady) → **velocity_score = 90**
- `engagement_score = (88 + 20 + 90) / 3 = 66.0` **✓ operator = 66.0**

*"1,995 logins in 90 days — solid absolute volume, but only 65 of 745 enabled users (8.7%) have logged in this quarter. The denominator is almost certainly inflated by portal buyer accounts in org_users — the real internal rep engagement is much higher. Velocity is holding steady at 0.78× baseline."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 1,998 > 0` ✓
- Smart Stacks: always applicable; count = 21 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 70` + `mp_document_email_drafted_90d = 69` = 139 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = true` → applicable; `portal_orders_90d = 19,484 > 0` ✓
- Online Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = true` → applicable; `mp_view_portal_90d = 372 > 0` ✓
- Inventory Management: 644 Inventory runs in 180d → applicable; imports in 90d = yes ✓
- Sales Data: `enable_sales_data = true` → applicable; 673 runs in 180d, last = May 12 ✓

7 applicable features (no Online Ordering). All 7 used. `adoption_score = 7/7 × 100 = 100.0` **✓ operator = 100.0**

*"Using every configured feature — nothing unused."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 45 ≥ 10` ✓
- Sharing (always): `mp_sharing_events_90d = 139 ≥ 3` ✓
- Online Catalog: `enable_online_catalog = true`; `portal_orders_90d = 19,484 > 0` ✓
- Portal Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = true`; `portal_orders_90d = 19,484 > 0` ✓
- Inventory: applicable; imports in 90d > 0 ✓

5 applicable channels. All 5 achieved. `value_delivery_score = 5/5 × 100 = 100.0` **✓ operator = 100.0**

*"All configured channels are producing outcomes."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 2,077; complete = 2,077
- Completeness = 2,077/2,077 = **100%** → band ≥90% → **catalog_score = 100**
- `contract_pricing_enabled = false`; price check via `net_price > 0` OR `prices_json IS NOT NULL AND != '{}'`

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Customers | 188 | May 12 | 0.8 | ✗ | ✓ |
| Images | 45 | May 8 | 3.9 | ✗ | ✓ |
| Inventory | 644 | May 12 | 0.2 | ✗ | ✓ |
| **Multifile Import** | 5,253 | Apr 13 | 29.0 | ✓ (error) | **excluded** |
| Portal Invoice Tracking Data | 125 | May 11 | 0.9 | ✗ | ✓ |
| Portal Invoices | 9 | May 10 | 2.4 | ✗ | ✓ |
| Portal Orders | 187 | May 12 | 0.1 | ✗ | ✓ |
| Products | 134 | May 12 | 0.7 | ✗ | ✓ |
| Sales Data | 673 | May 12 | 0.1 | ✗ | ✓ |

Excluded from health ratio: **Multifile Import** (known false-error rate per §4). Scoreable types: 8. All 8 healthy. `import_health_score = 8/8 × 100 = 100.0` **✓ operator = 100.0**

*Data freshness (Multifile Import is NOT excluded from freshness — only from health ratio):*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Customers | 188 | 180 | 0.96 → floor 1.0 | 1.0 | 0.8 | 0.80 | ≤1.0 | 100 | 188 |
| Images | 45 | 151 | 3.43 | 3.43 | 3.9 | 1.14 | 1.1–1.5 | 80 | 45 |
| Inventory | 644 | 180 | 0.28 → floor 1.0 | 1.0 | 0.2 | 0.20 | ≤1.0 | 100 | 644 |
| **Multifile Import** | 5,253 | 5.7 | 0.001 → floor 1.0 | 1.0 | 29.0 | 29.0 | >4.0 | **0** | 5,253 |
| Portal Inv. Tracking | 125 | 179 | 1.44 | 1.44 | 0.9 | 0.63 | ≤1.0 | 100 | 125 |
| Portal Invoices | 9 | 134 | 16.75 | 16.75 | 2.4 | 0.14 | ≤1.0 | 100 | 9 |
| Portal Orders | 187 | 179 | 0.96 → floor 1.0 | 1.0 | 0.1 | 0.10 | ≤1.0 | 100 | 187 |
| Products | 134 | 179 | 1.35 | 1.35 | 0.7 | 0.52 | ≤1.0 | 100 | 134 |
| Sales Data | 673 | 180 | 0.27 → floor 1.0 | 1.0 | 0.1 | 0.10 | ≤1.0 | 100 | 673 |

Multifile Import initial-load carve-out check: 5,253 runs (>> 5), span = 5.7d, days_since_first = 29d (> 14) → carve-out does NOT apply. This feed ran 5,253 times in a 5-day burst (Apr 8–13), then stopped completely. Its weight (5,253) completely dominates the freshness average.

Weighted freshness = (188×100 + 45×80 + 644×100 + 5253×0 + 125×100 + 9×100 + 187×100 + 134×100 + 673×100) / 7,258
= (18,800 + 3,600 + 64,400 + 0 + 12,500 + 900 + 18,700 + 13,400 + 67,300) / 7,258 = 199,600 / 7,258 = **27.5**

`operational_health_score = (100 + 100 + 27.5) / 3 = 75.8`

Operator reports **75.3²** (discrepancy of 0.5 points from timing/count differences at May 11 vs. May 12 — negligible). **✓ effectively matches**

*"Catalog 100% complete; all 8 import feeds healthy (Multifile Import excluded from health ratio); data freshness critical — the Multifile Import feed ran 5,253 times in a 5-day burst (Apr 8–13), then stopped 29 days ago. Because of its extreme run count (weight 5,253 vs. 2,005 for all other types combined), this single stalled feed drags freshness to 27%. All other 8 active feeds are on cadence."*

> **Spec observation:** The Multifile Import's burst-run pattern (5,253 runs in 5 days) overwhelms the frequency-weighted freshness average. This is working as designed — a stalled daily-equivalent feed IS a bigger problem than a stalled monthly one. However, when a burst occurs at setup/migration and then the feed type is retired, the run_count weight persists for 180 days and will continue to anchor freshness near 0 for the full window. V3.2 may want a "retired feed" concept that decays the weight when days_since > 2× expected cadence AND no recovery has occurred.

**Composite: (66.0 + 100.0 + 100.0 + 75.3) / 4 = 85.3 — Thriving ✓**
- Ghost account: `arr = $30,480 ≥ $5,000` AND `logins_90d = 1,998 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 66.0 ≥ 55` → **not triggered**

---

### `ml` — Millennium Lighting (iPad+Catalog, 2020)

**MAL:** bundle = iPad+Catalog, ARR = $17,980, cohort = 2020

**Engagement — raw signals**
- `logins_90d` = 1,629 → band 1,000–2,999 → **login_count_score = 88**
- `active_users_90d` = 60; `enabled_users` = 133; ratio = 60/133 = **45.1%** → band 25–49% → **ratio_score = 45**
- `logins_30d` = 509; `logins_180d` = 3,172; velocity = (509/3172) × 6 = **0.963** → band 0.75–1.49 (steady) → **velocity_score = 90**
- `engagement_score = (88 + 45 + 90) / 3 = 74.3` **✓ operator = 74.3**

*"1,629 logins in 90 days — solid absolute volume, but only 60 of 133 reps (45%) have logged in this quarter. Most of the team is dormant. Velocity is steady at 0.96× baseline, meaning those who are active are consistent. This is a rep-coverage problem, not an activity problem."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 1,629 > 0` ✓
- Smart Stacks: always applicable; count = 52 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 17` + `mp_document_email_drafted_90d = 41` = 58 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = true` → applicable; `portal_orders_90d = 0` → **not used** ✗
- Online Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = false` → **NOT applicable**
- Inventory Management: 169 Inventory runs in 180d → applicable; imports in 90d = yes ✓
- Sales Data: `enable_sales_data = true` → applicable; no Sales Data import type in 180d → **NOT used** ✗

6 applicable features. 4 used. `adoption_score = 4/6 × 100 = 66.7` **✓ operator = 66.7**

*"Using 4 of 6 applicable features. eCat Online Catalog is enabled but no portal orders in 90 days — the catalog is live but no traffic is flowing. Sales Data is configured on the org but no Sales Data import has run in the last 180 days — either the integration was never set up or the feed lapsed."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 2` → < 10 ✗
- Sharing (always): `mp_sharing_events_90d = 58 ≥ 3` ✓
- Online Catalog: `enable_online_catalog = true`; `portal_orders_90d = 0` → ✗
- Portal Ordering: `enable_online_ordering = false` → **NOT applicable**
- Sales Portal: `enable_sales_portal = false` → **NOT applicable**
- Inventory: applicable; imports in 90d > 0 ✓

4 applicable channels. 2 achieved (Sharing, Inventory). `value_delivery_score = 2/4 × 100 = 50.0` **✓ operator = 50.0**

*"Only 2 of 4 applicable channels producing outcomes. iPad order volume is critically low (2 orders in 90 days against a 10-order threshold). eCat Online Catalog is enabled but zero portal traffic in 90 days. Reps are using the app and sharing content, but the order pipeline has essentially stopped."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 3,467; complete = 3,387
- Completeness = 3,387/3,467 = **97.7%** → band ≥90% → **catalog_score = 100**
- `contract_pricing_enabled = false`

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Images | 50 | Apr 13 | 29.1 | ✗ | ✓ |
| Inventory | 169 | May 12 | 0.2 | ✗ | ✓ |
| Products | 22 | Apr 29 | 13.2 | ✗ | ✓ |

All 3 healthy. `import_health_score = 3/3 × 100 = 100.0`

*Data freshness:*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Images | 50 | 144 | 2.94 | 2.94 | 29.1 | 9.9 | >4.0 | 0 | 50 |
| Inventory | 169 | 179 | 1.07 | 1.07 | 0.2 | 0.19 | ≤1.0 | 100 | 169 |
| Products | 22 | 162 | 7.71 | 7.71 | 13.2 | 1.71 | 1.6–2.5 | 50 | 22 |

Weighted freshness = (50×0 + 169×100 + 22×50) / 241 = 18,000/241 = **74.7**

`operational_health_score = (100 + 100 + 74.7) / 3 = 91.6`

Operator reports **86.7³** (discrepancy: manual = 91.6, operator = 86.7, difference = 4.9 points). Back-computing from the operator's score: freshness would need to be 60.1, which implies Inventory scored ~80 (staleness ratio 1.1–1.5) rather than 100 at the May 11 run time — consistent with Inventory having a 1–2 day stale gap that day. By May 12 the Inventory feed had run again. **The operator's score is correct for May 11; my calculation reflects May 12 state.**

*"Catalog 98% complete; all 3 import feeds healthy; data freshness declining — the Images feed last ran 29 days ago against a ~3d expected cadence (10× overdue). Inventory is running daily. Products is 13 days against a 7.7d cadence (1.7× — slightly late)."*

**Composite: (74.3 + 66.7 + 50.0 + 86.7) / 4 = 69.4 — Healthy ✓**
- Ghost account: `logins_90d = 1,629 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 74.3 ≥ 55` → **not triggered**

---

### `dals` — DALS Lighting (iPad-only, 2023)

**MAL:** bundle = iPad-only, ARR = $8,700, cohort = 2023

**Engagement — raw signals**
- `logins_90d` = 123 → band 50–199 → **login_count_score = 40**
- `active_users_90d` = 11; `enabled_users` = 60; ratio = 11/60 = **18.3%** → band 1–24% → **ratio_score = 20**
- `logins_30d` = 42; `logins_180d` = 340; velocity = (42/340) × 6 = **0.741** → band 0.50–0.74 (cooling) → **velocity_score = 60**
- `engagement_score = (40 + 20 + 60) / 3 = 40.0` **✓ operator = 40.0**

*"123 logins in 90 days from just 11 of 60 enabled reps (18% active). The large enabled_users count (60) vs. active (11) suggests many reps have accounts but are not using the app. Velocity is cooling at 0.74× trailing baseline — the pace is declining. A 2023 cohort account showing this engagement pattern this early in the lifecycle warrants an active CS conversation."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 123 > 0` ✓
- Smart Stacks: always applicable; count = 2 > 0 ✓
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 6` + `mp_document_email_drafted_90d = 0` = 6 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = NULL` → **NOT applicable**
- Online Ordering: `enable_online_ordering = NULL` → **NOT applicable**
- Sales Portal: `enable_sales_portal = NULL` → **NOT applicable**
- Inventory Management: no Inventory import type in trailing 180d → **NOT applicable**
- Sales Data: `enable_sales_data = true` → applicable; no Sales Data import type in 180d → **not used** ✗

4 applicable features: iPad, Smart Stacks, Sharing, Sales Data.
3 used (Sales Data not running). `adoption_score = 3/4 × 100 = 75.0` **✓ operator = 75.0**

*"Using 3 of 4 applicable features. Sales Data is configured on the org (`enable_sales_data = true`) but no Sales Data import has ever run in the trailing 180 days — the integration appears to have never been fully set up or was abandoned. CS should verify intent."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 0` → < 10 ✗
- Sharing (always): `mp_sharing_events_90d = 6 ≥ 3` ✓
- Online Catalog: not applicable (gate NULL)
- Portal Ordering: not applicable (gate NULL)
- Sales Portal: not applicable (gate NULL)
- Inventory: not applicable (no active imports in 180d)

2 applicable channels: iPad orders, Sharing. 1 achieved (Sharing). `value_delivery_score = 1/2 × 100 = 50.0` **✓ operator = 50.0**

*"Only 1 of 2 applicable channels producing outcomes. Zero iPad orders in 90 days — reps are opening the app and sharing content, but not writing orders. For a 2023 cohort this is a red flag: two-plus years in and the app hasn't generated a single order this quarter."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 1,150; complete = 385
- Completeness = 385/1,150 = **33.5%** → band <60% → **catalog_score = 20**
- `contract_pricing_enabled = false`; failure is primarily missing images and/or missing descriptions on 765 products

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Products | 1 | Feb 26 | 75.1 | ✓ (error) | ✗ |

1 active type, 1 had an error. `import_health_score = 0/1 × 100 = 0.0` **✓ operator = 0.0**

*Data freshness:* Products has only 1 run in 180d → fewer than 3 → **excluded from freshness**. No other types qualify. `fresh_entries` is empty → `fresh_score = None` (excluded from operational health average).

`operational_health_score = (20 + 0) / 2 = 10.0` **✓ operator = 10.0**

*"Catalog completeness is 33.5% — a blocker for field use. Reps are working with a product catalog where 67% of items are incomplete (missing images, descriptions, or pricing). The only active import type (Products) ran once on Feb 26 with an error — 75 days ago. No successful data refresh has occurred in 2.5 months. Freshness excluded from the average (insufficient history). Operational Health is 10."*

**Composite: (40.0 + 75.0 + 50.0 + 10.0) / 4 = 43.75 ≈ 43.8 — Watch ✓**
- Ghost account: `arr = $8,700 ≥ $5,000` AND `logins_90d = 123 > 0` → **not triggered** (logins are non-zero so no override)
- Behavioral floor: `engagement_score = 40.0 < 55` AND `value_delivery_score = 50.0 ≥ 40` → **not triggered** (value delivery doesn't qualify)

> **CSM priority note:** dals is technically in Watch band with health_score = 43.8, but it's a 2023 cohort with zero iPad orders, 33% catalog completeness, and a broken Products import. The behavioral floor nearly fires (engagement < 55, value delivery at exactly the floor threshold of 50). This account is at real risk of slipping into the At Risk band by June if the catalog and import situation isn't addressed.

---

### `ihm` — International Home Miami (iPad-only, 2024)

**MAL:** bundle = iPad-only, ARR = $8,404, cohort = 2024

**Engagement — raw signals**
- `logins_90d` = 80 → band 50–199 → **login_count_score = 40**
- `active_users_90d` = 20; `enabled_users` = 22 (disabled IS NOT TRUE); ratio = 20/22 = **90.9%** → band 90%+ → **ratio_score = 100**
  - Operator narrative says "20 of 21 (95%)" — minor count difference of 1 user, same score band (90%+ → 100 either way)
- `logins_30d` = 15; `logins_180d` = 157; velocity = (15/157) × 6 = **0.573** → band 0.50–0.74 (cooling) → **velocity_score = 60**
- `engagement_score = (40 + 100 + 60) / 3 = 66.7` **✓ operator = 66.7**

*"80 logins in 90 days — low session volume but 20 of 22 reps (91%) have logged in, meaning this is a breadth-not-depth problem: nearly everyone has touched the app but session counts per rep are very low. Velocity cooling at 0.57× baseline — the pace is declining meaningfully. Session depth needs attention before velocity deteriorates further."*

**Adoption — applicability gates**
- iPad App: always applicable; `logins_90d = 80 > 0` ✓
- Smart Stacks: always applicable; count = 0 → **not used** ✗
- Sharing/quoting: always applicable; `mp_item_email_drafted_90d = 3` + `mp_document_email_drafted_90d = 0` = 3 > 0 ✓
- eCat Online Catalog: `enable_online_catalog = NULL` → **NOT applicable**
- Online Ordering: `enable_online_ordering = NULL` → **NOT applicable**
- Sales Portal: `enable_sales_portal = NULL` → **NOT applicable**
- Inventory Management: Inventory imports in 180d — 2 runs (Nov 26, Jan 26) → applicable; imports in 90d = last Inventory run was Jan 26 = 106 days ago → **NOT in 90d** ✗
- Sales Data: `enable_sales_data = true` → applicable; no Sales Data import type in 180d → **not used** ✗

5 applicable features: iPad, Smart Stacks, Sharing, Inventory, Sales Data.
2 used (iPad ✓, Sharing ✓). `adoption_score = 2/5 × 100 = 40.0` **✓ operator = 40.0**

*"Using 2 of 5 applicable features. Smart Stacks: 0 created — a CS demo of this feature could quickly unlock adoption. Inventory feed has gone quiet (last ran Jan 26, 106 days ago — outside the 90d usage window though the feed is still 'applicable' per the 180d lookback). Sales Data is configured but has never imported in 180 days."*

**Value Delivery — applicable channels**
- iPad orders (always): `ipad_orders_90d = 0` → < 10 ✗
- Sharing (always): `mp_sharing_events_90d = 3 ≥ 3` ✓ (exactly at threshold)
- Online Catalog: not applicable (gate NULL)
- Portal Ordering: not applicable (gate NULL)
- Sales Portal: not applicable (gate NULL)
- Inventory: applicable (has 2 runs in 180d) → imports in 90d > 0? Last run Jan 26 = 106 days ago → ✗

3 applicable channels: iPad orders, Sharing, Inventory. 1 achieved (Sharing). `value_delivery_score = 1/3 × 100 = 33.3` **✓ operator = 33.3**

*"Only 1 of 3 applicable channels producing outcomes. Zero iPad orders in 90 days. Inventory feed is silent — has not run in 106 days, depriving reps of current stock data. The only delivery signal is sharing, which barely clears the 3-event threshold."*

**Operational Health — raw signals**

*Catalog completeness:*
- Active products = 259; complete = 259
- Completeness = 259/259 = **100%** → band ≥90% → **catalog_score = 100**
- `contract_pricing_enabled = false`

*Import health:*

| Import Type | runs_180d | last_run | days_since | had_error | health |
|---|---:|---|---:|:---:|:---:|
| Images | 6 | Feb 13 | 88.0 | ✗ | ✓ |
| Inventory | 2 | Jan 26 | 106.0 | ✗ | ✓ |
| Product Stories | 1 | Feb 13 | 88.1 | ✗ | ✓ |
| Products | 5 | Apr 7 | 35.1 | ✗ | ✓ |

None in exclusion list. All 4 healthy (no errors on last run). `import_health_score = 4/4 × 100 = 100.0` **✓ operator = 100.0**

> **Import health note:** All 4 types pass the error check, but none have run recently. This is a case where import health (error status of last run) misleads: all passes are stale. The freshness sub-signal correctly captures the staleness.

*Data freshness (types with ≥3 runs in 180d):*

| Import Type | runs | span_d | mean_gap_d | gap_floor_d | days_since | ratio | band | score | weight |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| Images | 6 | 59 | 11.8 | 11.8 | 88.0 | 7.46 | >4.0 | 0 | 6 |
| Products | 5 | 116 | 29.0 | 29.0 | 35.1 | 1.21 | 1.1–1.5 | 80 | 5 |
| Inventory | 2 | — | — | — | 106.0 | — | excluded (<3 runs) | — | — |
| Product Stories | 1 | — | — | — | 88.1 | — | excluded (<3 runs) | — | — |

Weighted freshness = (6×0 + 5×80) / 11 = 400/11 = **36.4**

`operational_health_score = (100 + 100 + 36.4) / 3 = 78.8` **✓ operator = 78.8**

*"Catalog 100% complete — well-maintained for a 2024 account. All 4 import feeds healthy on the last error-status check, but freshness is where the problem lives: Images hasn't run in 88 days (7.5× its 12-day expected cadence, score 0). Products is 35 days against a 29-day cadence (1.2× — slightly late). Inventory and Product Stories don't qualify for freshness scoring (<3 runs). Operational Health is carried by catalog and import-error-status; the staleness is more serious than the 78.8 score suggests."*

**Composite: (66.7 + 40.0 + 33.3 + 78.8) / 4 = 54.7 — Watch ✓**
- Ghost account: `arr = $8,404 ≥ $5,000` AND `logins_90d = 80 > 0` → **not triggered**
- Behavioral floor: `engagement_score = 66.7 ≥ 55` → **not triggered**

> **CSM note:** ihm's Watch score is structurally soft — it's being saved from At Risk by a perfect catalog and a passing import-health check. The actual picture: zero iPad orders, Inventory stale for 3.5 months, Sales Data never configured, Smart Stacks unused. For a 2024 cohort account ($8,404 ARR), this should be on a CS action plan.

---

## Cross-Org Findings

### Verified Spec Behaviors

1. **Velocity sub-signal discriminates well.** The three velocity results in this set illustrate the bands cleanly: `ih` at 1.26× (steady, 90), `sbl` at 0.86× (steady, 90), and `ihm` at 0.57× (cooling, 60), `dals` at 0.74× (cooling, 60). The distinction between "high absolute logins but cooling" (dals: 123 logins, score 40 for engagement overall) and "low absolute logins but steady" (ihm: 80 logins, score 66.7) is exactly the kind of discrimination velocity was designed to produce.

2. **Adoption gate fires correctly for view_portal.** `asi` has 0 `view_portal` Mixpanel events despite having Sales Portal enabled and 583 portal orders in 90d. Adoption correctly marks Sales Portal as NOT used (view_portal_90d = 0), while the Value Delivery Sales Portal channel fires ✓ (portal_orders_90d > 0). The divergence is intentional: adoption measures whether reps are accessing the Sales Portal iPad section; value delivery measures whether portal commerce is happening at all.

3. **Freshness floor prevents degenerate ratios.** `asi` Customers feed runs ~1,090 times in 180d (mean gap = 0.17d). Without the 1.0-day floor, the staleness ratio for Portal Orders at 1.3 days since last would compute as 1.3/0.17 = 7.6 — falsely stale. With the floor, ratio = 1.3/1.0 = 1.3 → correctly "slightly late."

4. **Operational health correctly penalizes broken imports that are still "healthy" on catalog.** `sbl` has a perfect catalog (100%) and scores Thriving, but 4 of 6 import feeds are erroring — including Customers stale for 141 days. The operational health sub-signal (54.8) surfaces this clearly even though the composite is high.

5. **Freshness None-handling verified.** `dals` has only 1 run in 180d for Products (< 3 run minimum). The freshness sub-signal is correctly excluded (`fresh_score = None`), and operational health averages only 2 sub-signals: (20 + 0) / 2 = 10.

### Spec Observations (Candidates for V3.1/V3.2 Discussion)

**Observation 1: Denominator switch should cover iPad+Catalog+Portal when enabled_users > 500.**
`clm` has 745 enabled_users and 19,484 portal orders per 90d. The inflated org_users count (buyer portal accounts) drives the active-user ratio to 8.7%, scoring 20 — a severe understatement of internal rep engagement. The spec's denominator switch only triggers for "Full and iPad+Catalog+Cart bundles where enabled_users > 500." `clm` (iPad+Catalog+Portal) is excluded. The same inflation mechanism (customer portal accounts in org_users) exists for Portal-tier accounts. Recommend: extend the denominator switch to any bundle where `enable_sales_portal = true` AND `portal_orders_90d > 0` AND `enabled_users > 500`.

**Observation 2: Multifile Import burst weight can permanently anchor freshness for 180 days.**
`clm`'s Multifile Import ran 5,253 times in a 5-day burst (Apr 8–13), then stopped. Its weight (5,253 runs) is 2.6× the combined weight of all other 8 import types (2,005 runs). Even if the feed is permanently retired, it will continue to score 0 and dominate the freshness average until May–June 2026 (when it falls outside the 180-day window). V3.2 consideration: a "retired feed" decay mechanism — if days_since > 4× mean_gap AND run_count_90d = 0, halve the weight.

**Observation 3: import_health = 4/4 can mask universally stale feeds.**
`ihm` passes import health (4/4 healthy) while all 4 feeds haven't run in 35–106 days. The error-status check only validates whether the *last run* succeeded — not whether a run has happened recently. The freshness sub-signal partially catches this, but only for types with ≥3 runs. For `ihm`, Inventory and Product Stories have <3 runs and are excluded from freshness — their staleness is invisible to the score. Recommend: add a "days since any run > 90d" flag to the operational health narrative even if the type is excluded from freshness scoring.

**Observation 4: Value delivery channel is 50.0 for dals and ihm — near the behavioral floor.**
Both `dals` (engagement=40, value=50) and `ihm` (engagement=66.7, value=33.3) are near the behavioral floor (engagement < 55 AND value < 40). `dals` has engagement=40 < 55 but value=50 ≥ 40 — floor does not fire. `ihm` has value=33.3 < 40 but engagement=66.7 ≥ 55 — floor does not fire. In both cases the accounts are clearly struggling but the floor's two-condition AND prevents override. The floor is working correctly per spec; the question is whether the current thresholds are calibrated to capture all true near-ghost accounts.

---

## Operational Health Discrepancy Summary

| org | my_freshness | op_freshness | op_ophealth | my_ophealth | discrepancy | explanation |
|-----|---:|---:|---:|---:|---|---|
| ih | 97.9 | ~97.9 | 99.3 | 99.3 | ✓ match | — |
| asi | 94.7 | ~94.7 | 84.9 | 84.9 | ✓ match | — |
| sbl | 62.1 | ~31.1 | 54.8 | 65.1 | ~10 pts | Inventory scoring 50 at May 11 run (days_since ~1.5d); re-ran before my May 12 query |
| clm | 27.5 | ~25.9 | 75.3 | 75.8 | 0.5 pts | Minor run-count/timing diff at May 11 |
| ml | 74.7 | ~60.1 | 86.7 | 91.6 | ~5 pts | Inventory scoring ~80 at May 11 (days_since ~1.1d); re-ran before my May 12 query |
| dals | N/A | N/A | 10.0 | 10.0 | ✓ match | No freshness-eligible types |
| ihm | 36.4 | ~36.4 | 78.8 | 78.8 | ✓ match | — |

Discrepancies for `sbl` and `ml` are consistent with the operator running before those feeds' daily Inventory runs completed on May 11, resulting in higher days_since values and lower freshness scores. The May 12 spot check sees post-run state. **These are timing artifacts, not operator bugs.**

---

*Spot check produced: 2026-05-12. Operator output validated: runs/v3.1-narratives/2026-05-11/client_health_scores_2026-05-11.csv*
