# Customer Intelligence Brief — Example (Illustrative)

> **Status**: Mock example using real data model, illustrative numbers
> **Date**: 2026-06-15
> **Purpose**: Show what the full-data version looks like for a single customer

---

# Customer Intelligence Brief

**Prepared for:** Sarah Mitchell (Southeast Territory Rep)
**Account:** Magnolia Design Group
**Code:** MDG-4421 | Charlotte, NC
**Brief Date:** June 15, 2026 | **Data through:** June 14, 2026

---

## Account at a Glance

| | Trailing 12 Months | Prior 12 Months | Change |
|---|---:|---:|---:|
| **Total Business (all channels)** | $284,620 | $241,890 | +17.7% |
| **eCat Orders** | $73,410 (42 orders) | $51,220 (29 orders) | +43.3% |
| **eCat Penetration** | 25.8% | 21.2% | +4.6 pts |
| **Avg Order Value** | $1,748 | $1,766 | -1.0% |
| **Days Since Last Order** | 11 | — | On cadence |

**Price Level:** Designer (DES) | **Terms:** Net 30 | **Territory:** C-14 Southeast
**Ship-to Locations:** 3 — Charlotte NC, Asheville NC, Greenville SC

---

## Purchase DNA

### Top Categories (trailing 12 months, all channels)

| Category | Revenue | % of Spend | Units | Trend vs. Prior Year |
|---|---:|---:|---:|---|
| Upholstery | $118,440 | 41.6% | 86 | +22% |
| Case Goods | $67,190 | 23.6% | 41 | +8% |
| Lighting | $42,380 | 14.9% | 127 | +31% |
| Accent Tables | $31,240 | 11.0% | 64 | -4% |
| Outdoor | $14,870 | 5.2% | 19 | **NEW** |
| Rugs & Textiles | $10,500 | 3.7% | 38 | -12% |

### Top 10 SKUs by Revenue

| # | Item | Description | Units | Revenue | In Stock? |
|---|---|---|---:|---:|---|
| 1 | 0848-026 | Meridian Sectional | 6 | $28,440 | 3 avail |
| 2 | 1205-011 | Harlow Sofa | 8 | $19,200 | **0 — backordered, due 7/12** |
| 3 | 0635-008 | Langley Dining Table | 4 | $14,800 | 7 avail |
| 4 | 3340-019 | Coastal Pendant (set/3) | 22 | $11,880 | 41 avail |
| 5 | 0728-004 | Monroe Chair | 12 | $10,680 | 2 avail |
| 6 | 1822-003 | Willow Accent Table | 14 | $8,960 | 15 avail |
| 7 | 0510-001 | Bedford Nightstand (pair) | 8 | $7,840 | **0 — backordered, due 8/03** |
| 8 | 4100-012 | Savannah Outdoor Lounge | 4 | $7,200 | 12 avail |
| 9 | 3340-044 | Harper Sconce | 18 | $5,940 | 28 avail |
| 10 | 2200-006 | Indigo Rug 8x10 | 6 | $5,400 | 4 avail |

**Inventory alert:** 2 of their top 10 items are currently out of stock. The Harlow Sofa (#2, $19.2K) is backordered with a July 12 receipt. Flag alternative: SKU 1205-018 (Harlow Loveseat, same collection, 9 in stock).

### Collections They Buy
Coastal (34%), Madison (22%), Heritage (18%), Studio (14%), Other (12%)

### New Introductions Adoption
Of 230 new-intro SKUs, Magnolia has purchased 14 (6.1%). Similar-profile customers average 22 new-intro SKUs. Gap = 8 SKUs they haven't tried.

Top new intros bought by similar customers that Magnolia hasn't ordered:

| Item | Description | Collection | Avg Units (Similar Customers) |
|---|---|---|---:|
| 4100-028 | Riviera Outdoor Dining | Coastal | 3.2 |
| 0848-041 | Meridian Ottoman | Coastal | 2.8 |
| 1822-017 | Geometric Accent Table | Studio | 2.1 |

### Next Best Product (purchase sequence prediction)

| Prediction | Basis | Confidence |
|---|---|---|
| Meridian Ottoman (0848-041) | 82% of Meridian Sectional buyers also buy within 60d | High |
| Coastal Pendant Large (3340-022) | 71% of Coastal Pendant (set/3) buyers upgrade | Medium |
| Harlow Loveseat (1205-018) | Top alternative when Harlow Sofa is backordered | Contextual |

---

## Buying Rhythm

### Order Frequency

| Metric | This Customer | Org Median | Percentile |
|---|---:|---:|---|
| Orders per month | 3.5 | 1.8 | **Top 15%** |
| Avg days between orders | 8.6 | 16.4 | **Top 20%** |
| Active months (of last 12) | 11 | 7 | **Top 10%** |

### Seasonality Pattern

```
Jan ████████░░░░░░░░  $18K
Feb ██████░░░░░░░░░░  $14K
Mar ████████████░░░░  $28K  ← Pre-Spring Market
Apr ██████████████░░  $32K  ← Post-Market orders
May ████████░░░░░░░░  $19K
Jun ██████████░░░░░░  $22K
Jul ████████░░░░░░░░  $17K
Aug ██████░░░░░░░░░░  $13K  ← Summer dip
Sep ████████████░░░░  $26K  ← Pre-Fall Market
Oct ██████████████░░  $31K  ← Post-Market orders
Nov ████████░░░░░░░░  $19K
Dec ████░░░░░░░░░░░░  $11K  ← Holiday slowdown
```

**Insight:** Buying peaks in April and October — market-aligned. Next peak window opens in ~3.5 months (September/October). Pre-market outreach in August would be optimal timing.

### Recency & Velocity

- Last order: **June 4, 2026** (11 days ago) — on cadence
- Order velocity trend (last 3 quarters): **accelerating** (+14% Q/Q)
- Predicted next order window: **June 18–22** (based on 8.6-day avg interval)
- Risk level: **Low** — consistent ordering pattern, no decay signal

### Reorder Decay Alerts

| Item | Historical Interval | Recent Intervals | Status |
|---|---:|---|---|
| 0728-004 (Monroe Chair) | 28 days | 32, 41, 58 days | **DECAY DETECTED** |
| All other top items | — | — | On pace |

---

## Money Profile

### Spend Trajectory (quarterly)

```
Q3 2025  ████████████░░  $62K
Q4 2025  ██████████████  $71K   +15%
Q1 2026  ██████████████  $74K   +4%
Q2 2026  ████████████░░  $78K*  +5% (projected)
```

### Price & Discount Behavior

| Metric | This Customer | Org Avg |
|---|---:|---:|
| Avg unit price | $1,284 | $890 |
| Price level | Designer (DES) | — |
| Avg discount applied | 2.1% | 4.8% |
| Promo price usage | 8% of line items | 15% |
| Freight-to-revenue ratio | 3.4% | 5.1% |

**Insight:** Premium buyer. Pays near-list, rarely uses promos, low discount sensitivity. Do NOT lead with price on new intros — lead with product.

### Price Trajectory

Avg unit price declining 4.2% per quarter ($1,340 → $1,284). Monitor — could indicate a shift toward lower-price-point items or increasing promo usage.

---

## Channel Mix

| Channel | Orders | Revenue | % of Total |
|---|---:|---:|---:|
| iPad (rep-submitted) | 38 | $68,210 | 24.0% |
| eCat Online (self-serve) | 4 | $5,200 | 1.8% |
| Phone/Fax (from ERP) | 89 | $142,400 | 50.0% |
| Market/Showroom | 12 | $48,810 | 17.2% |
| EDI | 6 | $20,000 | 7.0% |

**Insight:** 50% of business still placed by phone. eCat is growing (+43% YoY) but 89 phone orders = 89 opportunities to demonstrate self-service.

---

## Rep Engagement Profile (Mixpanel, trailing 6 months)

| Activity | Count |
|---|---:|
| Customer selections | 67 |
| Product searches while in account | 142 |
| Configured items built | 18 |
| PDF catalogs generated | 6 |
| Documents viewed | 23 |
| Orders submitted | 21 |
| Order history reviewed | 14 |
| Previous orders copied | 4 |
| SmartPicks viewed | 3 |

**Engagement score: 8.4/10** — One of your most-engaged accounts. 31% session-to-order rate (vs. avg 12%).

---

## Buyer Intelligence

| Buyer | % of Volume | Categories | First Order | Status |
|---|---:|---|---|---|
| Jennifer Walsh | 68% | All categories | Mar 2024 | Primary relationship |
| David Chen | 24% | Lighting only | Feb 2026 | **NEW BUYER** |
| Magnolia Admin | 8% | Reorders only | Jun 2024 | Likely automated |

**Alert:** David Chen is a new decision-maker (started 4 months ago). Build this relationship.

---

## Fulfillment & Returns

### Fill Rate (trailing 12 months)

| Metric | Value | Org Avg |
|---|---:|---:|
| Fill rate | 88.1% | 91.4% |
| Avg backorder days | 22 | 18 |
| Items currently on backorder | 3 | — |

### Return History

| Period | Returns | Return $ | Return Rate |
|---|---:|---:|---:|
| Trailing 12 months | 4 | $3,840 | 1.3% |
| Prior 12 months | 2 | $1,200 | 0.5% |

**Backorder impact:** When backordered, this customer's reorder interval for that SKU increases 2.3x. Projected impact from current backorders: -$14K annualized.

---

## Market Commitments vs. Actuals

| Market | Committed | Ordered | Conversion |
|---|---:|---:|---:|
| High Point Oct 2025 | $48,000 | $41,200 | 86% |
| High Point Apr 2026 | $52,000 | $31,400 | **60%** |

**Uncommitted items (April):**

| Item | Description | Committed Qty | In Stock? |
|---|---|---:|---|
| 4100-028 | Riviera Outdoor Dining | 2 | Yes (12 avail) |
| 0848-041 | Meridian Ottoman | 3 | Yes (8 avail) |
| 1822-017 | Geometric Accent Table | 2 | Yes (15 avail) |

**Category conversion:** Upholstery 91%, Lighting 95%, Outdoor 0%, Bedroom 0%.

---

## Cross-Sell Opportunity

vs. 23 similar customers (Southeast, $200K–$400K spend tier):

| Category | Similar Avg | Magnolia | Gap |
|---|---:|---:|---:|
| **Bedroom** | $28,400 | $7,840 | **-$20,560** |
| **Outdoor** | $31,200 | $14,870 | **-$16,330** |
| **Dining** | $22,100 | $14,800 | **-$7,300** |

**Total whitespace: $44,190**

---

## Category Share Evolution

| Category | Prior Year % | Current % | Change | $ Impact |
|---|---:|---:|---|---:|
| Upholstery | 48% | 42% | -6 pts | -$8.2K |
| Lighting | 11% | 15% | +4 pts | +$9.4K |
| Outdoor | 0% | 5% | +5 pts | +$14.9K (new) |
| **Bedroom** | **12%** | **3%** | **-9 pts** | **-$21.8K** |

**Competitive loss signal:** Bedroom dropped $21.8K while total business grew. These dollars went somewhere else.

---

## Showroom Placements

| Location | Items Placed | Last Updated |
|---|---:|---|
| Charlotte Showroom | 34 | May 2026 |
| Asheville Showroom | 18 | Mar 2026 |
| Greenville Showroom | 12 | **Jan 2026 — STALE** |

Greenville: 4 placed items now discontinued. Suggest refresh.

---

## Same-Store Performance

| Location | Revenue LTM | vs. Prior Year |
|---|---:|---:|
| Charlotte, NC | $168,400 | +24% |
| Asheville, NC | $78,200 | +11% |
| Greenville, SC | $38,020 | **-18%** |

Greenville had 4 top-item stockouts in Q1. Decline may be supply-driven.

---

## Account Health Signal

```
 GROWING ████████████████████░░░░  Score: 82/100
```

| Signal | Status |
|---|---|
| Spend trajectory | **Accelerating** (+17.7% YoY) |
| Order frequency | **Stable** (3.5/month) |
| eCat adoption | **Growing** (21% → 26%) |
| Product breadth | **Expanding** (added Outdoor) |
| Fill rate | **Watch** (88.1% vs. 91.4%) |
| Market conversion | **Watch** (60% in April) |
| Bedroom category | **Alert** (competitive loss signal) |

---

## Pre-Meeting Priorities for Sarah

1. **Close the 3 uncommitted market items** — all in stock, buyer already committed at market
2. **Flag Harlow Sofa backorder** (their #2 item, $19.2K) — present Harlow Loveseat alternative
3. **Explore Bedroom category** — $21.8K competitive loss signal, $20.5K whitespace vs. similar accounts
4. **Build relationship with David Chen** — new buyer, 4 months in, currently Lighting only
5. **Ask about Greenville showroom** — placements 5 months stale, 4 discontinued items, revenue -18%
6. **Monroe Chair reorder decay** — their reorder interval is stretching, check floor performance

---

## Account Lifecycle Position

Month 26 of relationship. Tracking 18% above cohort curve. Projected peak: ~$400K (Year 3). $116K addressable growth if trajectory holds.
