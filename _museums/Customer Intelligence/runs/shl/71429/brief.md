# Customer Intelligence Brief — Customer 71429

> **Generated**: 2026-06-15 | **Org**: Savoy House (shl, org 41)
> **Data Richness**: 5/9 (Standard) | **Rendering Mode**: Full (sparse)
> **Note**: No customer master record found in `customers` table — data sourced exclusively from `portal_orders` and `portal_invoice_items`.

---

## §1 — Header

| Field | Value |
|-------|-------|
| **Customer** | Unknown (no customer record) |
| **Code** | 71429 |
| **Location** | Unknown |
| **Price Level** | Unknown |
| **Territory** | Unknown |
| **Terms** | Unknown |
| **Ship-To Locations** | Unknown |
| **Lifecycle Stage** | 🔴 Declining |
| **Last Order** | ~2025-08 (last portal_orders activity) |
| **Days Since Last Order** | ~300+ |

---

## §2 — Account at a Glance

| Metric | LTM | Prior Year | YoY Change |
|--------|-----|------------|------------|
| **Orders** | 3 | 46 | -93.5% ↓ |
| **Revenue** | $110 | $28,211 | -99.6% ↓ |
| **AOV** | $36.60 | $613.28 | -94.0% ↓ |
| **Last Order** | ~2025-08 | — | — |

*Account does not use eCat iPad.*

> ⚠ **CRITICAL DECLINE**: Revenue collapsed from $28K to $110 (-99.6%). This customer has effectively gone dormant — the 3 remaining LTM orders are minimal/parts-only purchases.

---

## §3 — Purchase DNA: Categories

| Category | Revenue LTM | % of Spend | Units | YoY Change |
|----------|-------------|-----------|-------|------------|
| Bath | $110 | 83.9% | 2 | -98.6% ↓ |
| Uncategorized | $21 | 16.1% | 5 | -74.4% ↓ |

Only 2 product categories remain active, both collapsing. The "Uncategorized" $21 (5 units at $4.20/ea) is likely replacement parts (item 999-PARTS).

---

## §4 — Purchase DNA: Top Items

| Item | Description | Collection | Units | Revenue | Qty Avail |
|------|-------------|-----------|-------|---------|-----------|
| 8-1020-2-322 | Calhoun 2-Light Vanity Light in Warm Brass | Calhoun | 2 | $110 | 85 |
| 999-PARTS | (no description) | — | 5 | $21 | 0 |

Only 2 SKUs purchased in LTM. The Calhoun vanity light is the only real product; 999-PARTS is service/replacement parts.

---

## §5 — New Introduction Adoption

| Metric | Value |
|--------|-------|
| Org new items available | 827 |
| Customer purchased | 0 (0.0%) |
| Cohort average | 17.5 |

Zero new item adoption. Customer is not engaging with the current product line.

---

## §6 — Spend Trajectory

| Quarter | Orders | Revenue | AOV | QoQ Change |
|---------|--------|---------|-----|-----------|
| Q2 2024 | 1 | $89 | $89 | — |
| Q3 2024 | 7 | $2,488 | $355 | +2,696% ↑ |
| Q4 2024 | 7 | $8,327 | $1,190 | +235% ↑ |
| Q1 2025 | 18 | $11,447 | $636 | +37% ↑ |
| Q2 2025 | 12 | $5,969 | $497 | -48% ↓ |
| Q3 2025 | 1 | $0 | $0 | -100% ↓ |

**Inflection narrative**: Account ramped rapidly from Q2 2024 through Q1 2025 (peaking at $11.4K/quarter, 18 orders), then collapsed in Q2 2025 and went to zero revenue by Q3 2025. Classic account loss pattern — this customer has churned.

---

## §7 — Buying Rhythm

**Frequency Metrics (LTM):**
| Metric | Value |
|--------|-------|
| Total Orders LTM | 3 |
| Orders/Month | 0.3 |
| Active Months | 2 of 13 |
| Avg Days Between Orders | 36.0 |

**Monthly Activity (last 24 months):**

Active period was Jun 2024 – Jun 2025 (peaking Dec 2024 – Mar 2025). Zero activity since August 2025. The 3 LTM orders fall within the trailing window edge.

**Gap Detection**: ⚠ 10+ month gap since meaningful activity. Account is functionally dormant.

---

## §8 — Channel Mix

| Channel | Orders | Revenue | % |
|---------|--------|---------|---|
| Unattributed | 3 | $110 | 100% |

---

## §9 — Wallet Share

| Metric | Value |
|--------|-------|
| Customer LTM Revenue | $110 |
| State Cohort | Unknown (no billing_state on file) |

Wallet share cannot be computed — no customer master record exists to determine billing state.

---

## §12 — Rep Engagement

**No Mixpanel activity found** for this customer in the last 180 days.

---

## §20 — Strategic Summary

**Strengths:**
- None currently active. The prior-year relationship showed strong engagement (46 orders, $28K, broad category mix) — the customer was previously a solid mid-tier account.

**Risks:**
- **Account has effectively churned.** Revenue declined 99.6% YoY. Only 3 minimal orders ($110 total) remain in the LTM window, and those are likely service/parts from months ago.
- No customer master record — this account may have been removed from the customer file or consolidated under another bill-to code.
- Zero rep engagement in Mixpanel — no one is working this account.

**Opportunities:**
- **Win-back candidate**: Prior-year spending of $28K with 46 orders demonstrates this was once a viable account. If the churn cause is known (competitive loss, business closure, consolidation), a targeted outreach could recover revenue.
- If this is a consolidation (merged into another bill-to code), the brief is informational only — flag for data cleanup.

**Rep Talking Points:**
1. "What happened? This account went from $28K/year to essentially zero. Is there a competitive situation, or did they consolidate billing?"
2. "If they're still in business, they were buying chandeliers, sconces, and bath fixtures broadly — worth a reconnection call."
