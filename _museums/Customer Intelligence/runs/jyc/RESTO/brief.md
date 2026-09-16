# Customer Intelligence Brief: RESTO (Restoration Hardware)

> **Client**: Jamie Young Company | **Org**: jyc (76)
> **Generated**: 2026-06-16 | **Period**: Last 12 months vs. prior 12 months
> **Data Richness**: 6/9 | **Lifecycle Stage**: New | **Health Score**: 74/100 (Healthy)

---

## §1 — Header

| Field | Value |
|-------|-------|
| Customer | RESTO |
| Billing City/State | *No customer master record* |
| Price Level | — |
| Terms | — |
| Territory | — |
| Ship-Tos | 6 (via order data) |
| Last Order | 2026-06-03 (13 days ago) |

NEW ████████████████████░░░░░░  Score: 74/100 (Healthy)

*Note: No customer master record exists for RESTO in the customers table. Account identified as Restoration Hardware based on ship-to locations (RH Patterson DC, RH Ohio DC, Gallery Retail locations).*

---

## §2 — Account at a Glance

| Metric | LTM | Prior Year | YoY |
|--------|-----|------------|-----|
| Total Orders | 16 | 0 | — (new) |
| Total GMV | $1.30M | $0 | — (new) |
| Last Order | 2026-06-03 | — | — |
| Days Since Last Order | 13 | — | — |

*Account does not use eCat iPad — orders via unknown channel (channel data not available for this client's order import).*

First order placed 2026-03-13 — account is 3 months old. $1.30M in initial volume places RESTO at +10,792.9% vs. the 0-year tenure cohort average ($11,955), making this account an immediate outlier among new customers.

---

## §5 — New Introduction Adoption

| Metric | Value |
|--------|-------|
| Org New Items | 149 |
| Customer Purchased | 0 |
| Cohort Avg | 2.3 |

RESTO has not purchased any of the 149 new introduction items. The cohort average is 2.3 new items. Given the account's scale ($1.30M LTM), this represents a meaningful adoption gap.

*Similar-customer recommendations unavailable (no customer master record — billing state unknown).*

---

## §6 — Spend Trajectory

| Quarter | Orders | Revenue | AOV | QoQ Change |
|---------|--------|---------|-----|------------|
| Q1 2026 | 1 | $9.12K | $9,124 | — |
| Q2 2026 | 15 | $1.29M | $86,211 | ↑ +14,078% |

Massive ramp in Q2 2026 — revenue inflected from a single $9.1K order in Q1 to $1.29M across 15 orders in Q2. This suggests Q1 was a trial/sample order and Q2 represents committed production purchasing.

---

## §7 — Buying Rhythm

| Metric | This Customer | Org Avg | Percentile |
|--------|--------------|---------|------------|
| Orders/Month | 1.3 | 0.2 | Top 2% |
| Avg Days Between | 5.5 | — | — |
| Active Months (of 12) | 3 | — | — |

**Predicted next order window**: 2026-06-07 to 2026-06-11 (based on 5.5-day avg interval) — *Predicted window was Jun 7–11 — 5 days overdue.*

### Monthly Seasonality (LTM)

| Month | Orders | Revenue |
|-------|--------|---------|
| Mar 2026 | 1 | $9.12K |
| Apr 2026 | 12 | $789.94K |
| Jun 2026 | 3 | $503.22K |

⚠ **Gap detected**: May 2026 shows zero orders despite active purchasing in April and June. Possible PO cycle gap or seasonal pause.

---

## §8 — Channel Mix

| Channel | Orders | Revenue | % of Orders |
|---------|--------|---------|-------------|
| Unknown | 16 | $1.30M | 100.0% |

*Channel data not available for this client's order import.*

---

## §9 — Wallet Share

| Metric | Value |
|--------|-------|
| Customer LTM Revenue | $1.30M |
| Cohort Comparison | Unavailable (no customer master record — billing state unknown) |

Customer revenue only — cohort comparison unavailable (no customer master record).

---

## §19 — Same-Store Performance

| Ship-To | Location | City, State | Orders | Revenue |
|---------|----------|-------------|--------|---------|
| SFDC | SFDC-Gallery Retail (0093) | Patterson, CA | 6 | $551.85K |
| LADC | LADC-Gallery Retail (0091) | Ontario, CA | 2 | $313.27K |
| RHPATT | RH Patterson Furn DC (0095) | Patterson, CA | 2 | $271.68K |
| RHOHIO | RH Ohio Dist. Ctr Dir (089D) | West Jefferson, OH | 3 | $140.83K |
| ODC | ODC-Gallery Retail (0088) | West Jefferson, OH | 2 | $15.52K |
| RH MDC | Restoration Hardware | North East, MD | 1 | $9.12K |

6 distribution/retail locations across 3 states. California operations (Patterson + Ontario) account for 87.2% of revenue ($1.14M). Ohio and Maryland are secondary.

---

## §22 — Account Health Score Breakdown

| Signal | Status | Points |
|--------|--------|--------|
| Spend trajectory | N/A (new account, no prior year) | — |
| Order recency | 13 days since last order | 15/15 |
| Order frequency | 1.3/month (Top 2%) | 15/15 |
| eCat adoption | 0% penetration | 0/10 |
| Product breadth | N/A (no invoice-level data) | — |
| Fill rate | 0.0% (vs 1.9% org) — within 5 pts | 7/10 |
| Market conversion | N/A (data unavailable) | — |
| Category stability | N/A (data unavailable) | — |
| **Total** | | **37/50 → 74/100 (Healthy)** |

### Lifecycle Position

| Metric | Value |
|--------|-------|
| Tenure | 3 months (New) |
| vs. Same-Tenure Cohort | +10,792.9% above |
| Cohort Size | 310 customers |
| Projected Peak | Tracking above cohort curve — no higher-tenure benchmark available |

---

## §23 — Strategic Summary

**Strengths:**
- Massive new account: $1.30M in first 3 months places RESTO in the top 2% of all jyc customers by order frequency and far above the 0-year tenure cohort avg ($11,955). This is Restoration Hardware operating through 6 distribution/retail locations.
- Strong recency: last order 13 days ago with a 5.5-day average order interval signals active purchasing.

**Risks:**
- No customer master record exists — RESTO is missing from the `customers` table, preventing wallet share analysis, cohort comparisons, and territory assignment. This is a data gap that should be resolved.
- Zero eCat iPad adoption — all 16 orders came through an unclassified channel. No digital catalog engagement.
- May 2026 gap: zero orders in May despite heavy April ($790K) and June ($503K) activity.
- No invoice-level data: portal_invoice_items is empty for this customer, blocking category, SKU, collection, reorder, and cross-sell analysis.

**Opportunities:**
- New introduction adoption: 0 of 149 new items purchased vs. cohort avg of 2.3. Given RESTO's volume, even modest adoption could drive incremental revenue.
- eCat onboarding: introducing the iPad catalog to RH buyers/merchandisers could improve order visibility and product discovery.
- Customer master setup: creating a proper customer record would unlock wallet share, cross-sell, and territory analytics.

**Rep Talking Points:**
1. "Your first 3 months have been exceptional — $1.3M across 6 locations. How do we set up for a strong H2 run?"
2. "We have 149 new introductions you haven't seen yet. Can we schedule a presentation for David Dimos and the merchandising team?"
3. "We'd like to get you set up on our digital catalog (eCat) — it would streamline ordering across your 6 locations."

---

*Generated by SuperCat Customer Intelligence • Data as of 2026-06-16 • Read-only — no data was modified*
