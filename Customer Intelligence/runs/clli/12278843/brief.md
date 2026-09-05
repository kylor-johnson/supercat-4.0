# Customer Intelligence Brief

> **Generated**: 2026-06-15 | **Org**: Craftmade (clli, 149) | **Customer**: 12278843
> **Data Richness**: 5/9 (Standard) | **Mode**: Full (minimal data)

---

## §1 — Header

| Field | Value |
|-------|-------|
| **Customer** | WOODARD HOSPITALITY SHOWROOM |
| **Code** | 12278843 |
| **Location** | GRAND PRAIRIE, TX |
| **Price Level** | 0 |
| **Territory** | 9150 |
| **Terms** | Net 30 |
| **Ship-To Locations** | 1 |
| **Lifecycle Stage** | **Growing** ⚠ |
| **Last Order** | 2026-04-01 |
| **Days Since Last Order** | 76 🟡 |

*Note: "Growing" lifecycle label is misleading — this is a $0→$15 transition, not genuine growth. Prior-year revenue was $0.00, making YoY calculation undefined.*

---

## §2 — Account at a Glance

| Metric | LTM | Prior Year | YoY |
|--------|-----|------------|-----|
| **Total Orders** | 2 | 7 | — |
| **Total GMV** | $14.54 | $0.00 | N/A |
| **Last Order** | 2026-04-01 | — | — |

*Account does not use eCat iPad — orders via unspecified channel.*

This is a **showroom/samples account**. 7 prior-year orders totaled $0.00 (catalog and swatch shipments at no charge). The $14.54 LTM revenue is from a single non-zero invoice.

---

## §3 — Purchase DNA: Categories

Not rendered — all invoiced items are catalog/binder/swatch material codes (99-CATALOG-*, 99-BINDER-*, etc.) with $0.00 unit prices. No product-category purchasing activity.

---

## §4 — Purchase DNA: Top Items

| Item | Description | Units | Revenue |
|------|-------------|-------|---------|
| 99-CATALOG-WH | (catalog) | 174 | $0.00 |
| 99-PRICESHEET-WH | (price sheet) | 17 | $0.00 |
| 99-CATALOG-W | (catalog) | 14 | $0.00 |
| 99-COLORCHIPS-W1 | (color chips) | 14 | $0.00 |
| 99-WEAVE-SET | (weave sample set) | 9 | $0.00 |
| 99-CATALOG-M | (catalog) | 7 | $0.00 |
| 99-NEXTEAK-SET | (teak sample set) | 6 | $0.00 |
| 99-PRICESHEET-W | (price sheet) | 4 | $0.00 |
| 99-BINDER-W | (binder) | 3 | $0.00 |
| 99-PRICESHEET-M | (price sheet) | 3 | $0.00 |

All items are showroom collateral — catalogs (174 units), price sheets, color chips, material samples. No product purchases. This account exists to supply a Woodard Hospitality showroom in Grand Prairie, TX.

---

## §6 — Spend Trajectory

| Quarter | Orders | Revenue | AOV |
|---------|--------|---------|-----|
| Q3 2024 | 1 | $0.00 | $0.00 |
| Q4 2024 | 4 | $0.00 | $0.00 |
| Q1 2025 | 2 | $0.00 | $0.00 |
| Q4 2025 | 1 | $0.00 | $0.00 |
| Q2 2026 | 1 | $14.54 | $14.54 |

6-month gap between Q1 2025 and Q4 2025. Single $14.54 order in Q2 2026 breaks what was otherwise a purely zero-revenue account.

---

## §7 — Buying Rhythm

| Metric | Value |
|--------|-------|
| Total orders (LTM) | 2 |
| Orders/month | 0.2 |
| Active months | 2/12 |
| Avg days between orders | 177.0 |

Near-dormant cadence — two orders in 12 months, 177 days apart. This is not a commercial buyer; it's a showroom restocking account.

---

## §8 — Channel Mix

| Channel | Orders | Revenue | % |
|---------|--------|---------|---|
| (unspecified) | 2 | $14.54 | 100% |

---

## §9 — Wallet Share

| Metric | Value |
|--------|-------|
| Customer LTM revenue | $14.54 |
| TX cohort average | $80,161 |
| TX cohort max | $919,758 |
| TX cohort size | 100 |

**Below cohort — at 0.02% of the TX average.** This is not a wallet-share opportunity — it's a non-commercial showroom account. Comparing against the TX cohort is not meaningful.

---

## §12 — Rep Engagement

No Mixpanel events found for customer 12278843 in the last 180 days.

---

## §20 — Strategic Summary

**Classification**: This is a **showroom/samples-only account**, not a commercial buyer. All activity consists of catalog and material sample shipments at $0 revenue. The single $14.54 invoice appears to be an anomalous charge on what is otherwise a cost-center account.

**Findings:**
- 174 catalogs shipped over the relationship lifetime — Woodard Hospitality likely distributes Craftmade collateral through their Grand Prairie showroom.
- No product purchases, no eCat activity, no rep engagement, no buyer intelligence.
- The "Growing" lifecycle label is a false positive — the algorithm sees $0 → $15 as growth, but this is noise on a non-commercial account.

**Recommendation**: This account type should be flagged in the brief generator. Accounts where 100% of invoiced items are collateral codes (99-*) and total LTM revenue < $100 should render a "Showroom/Collateral Account" badge instead of the standard brief, with a note: *"This account receives promotional materials only. No product-level analysis is applicable."*

---

## Performance Notes

| Query | Status | Notes |
|-------|--------|-------|
| CQ-01 | ✅ OK | Fast |
| CQ-02 | ⏭ Skipped | All items are $0 collateral — no category analysis meaningful |
| CQ-03 | ✅ OK | Fast — all $0 items |
| CQ-04 | ⏭ Skipped | No meaningful collection data |
| CQ-05 | ⏭ Skipped | No product purchases to measure adoption |
| CQ-06 | ⏭ Skipped | No purchase history for sequence analysis |
| CQ-07 | ✅ OK | Fast |
| CQ-08 | ⏭ Skipped | Insufficient data |
| CQ-09 | ⏭ Skipped | No reorder cycles |
| CQ-10 | ✅ OK | Fast |
| CQ-11 | ⏭ Skipped | $0 unit prices make pricing analysis meaningless |
| CQ-12 | ✅ OK | Fast |
| CQ-13 | ✅ OK | BigQuery — no events |
| CQ-14 | ⏭ Skipped | Gate: HAS_BUYER_NAMES = false |
| CQ-15 | ⏭ Skipped | Not meaningful for collateral orders |
| CQ-16 | ⏭ Skipped | Gate: HAS_RMA = false |
| CQ-17 | ⏭ Skipped | Gate: HAS_COMMITMENT_REPORTS = false |
| CQ-18 | ⏭ Skipped | Gate: HAS_PLACEMENT_REPORTS = false |
| CQ-19 | ⏭ Skipped | No category spend to compare |
| CQ-20 | ⏭ Skipped | No meaningful category evolution |
| CQ-21 | ⏭ Skipped | Only 1 ship-to |
| CQ-22 | ✅ OK | Fast — but comparison is not meaningful |
| CQ-23 | ✅ OK | Fast |

### Edge Case Findings

This customer validates an important edge case: **the brief generator needs a collateral-account detector.** When:
- 100% of items match a `99-*` pattern (or similar collateral prefix)
- Total LTM revenue < $100
- All unit prices = $0

...the brief should short-circuit to a "Showroom/Collateral Account" template instead of running the full query suite. The current lifecycle classifier marks this as "Growing" (technically correct: $0 → $15), which is misleading.
