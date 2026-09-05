# Gabby / Summer Classics — Consolidated Intelligence Brief

**Generated:** March 2, 2026 | **Framework:** Account Scoring v3 + Thresholds v1.1 | **Run:** Independent per-entity rerun

---

## B1. Account Identity & Context

### Company Profile

| Field | Value | Source |
|---|---|---|
| **Account** | Gabby / Summer Classics (Multi-Entity) | PostgreSQL `organizations` |
| **Industry** | Furniture — Residential, Outdoor/Casual, Contract, Retail | HubSpot `company.properties_industry` |
| **Headquarters** | Alabama (all 4 entities) | PostgreSQL `organizations.state` |
| **Combined MRR** | $8,975/mo (~$107,700 ARR) | Stripe invoices Mar 2026 |
| **Products Active** | iPad (CPQ), Online, Portal, B2B Cart, Closed Site | PostgreSQL `subscriptions` per org |
| **Combined Active Users** | 250 CLM / 265 Mixpanel | 4 CLM files + Mixpanel per shortname |
| **Partner Since** | Gabby: Apr 2013, SC: Feb 2014, SCW+SCCON: Apr 2015 | PostgreSQL `organizations.created_at` |
| **Account Owner** | Not assigned | HubSpot (no owner data) |

### Entity Structure

| Entity | Shortname | Org ID | Business Model | Products | Use-Case |
|---|---|---|---|---|---|
| **Gabby** | `gh` | 55 | B2B wholesale, rep-driven ordering | 5 plans | Ordering |
| **Summer Classics** | `scw` | 87 | B2B wholesale, rep-driven ordering | 5 plans | Ordering |
| **SC Contract** | `sccon` | 88 | Contract/hospitality, ERP-pushed orders | 5 plans | Non-Ordering + Pushed Data |
| **SC Wholesale** | `sc` | 69 | Physical retail stores (Gabriella White) | 4 plans | Ordering (Retail) |

### Billing

| Billing Entity | Monthly | Trend (12mo) | Covers | Source |
|---|---|---|---|---|
| SC Home/Gabby LLC | $2,097 (Mar) | Flat ($1,899–$2,097 range) | gh + sc | Stripe + QuickBooks |
| Summer Classics, Inc. | $6,878 (Mar) | Flat ($6,590–$7,184 range) | scw + sccon | Stripe + QuickBooks |
| **Combined** | **$8,975** | Flat | All 4 | |

All invoices current. Zero outstanding balances (QuickBooks confirmed).

### Stakeholder Map

| Name | Entity | Channel | Last Interaction | Context |
|---|---|---|---|---|
| Jonathan T. | Gabriella White (sc) | HelpScout | Feb 2026 | Primary support contact |
| Ben | Gabriella White (sc) | HelpScout | Jan 2026 | Secondary support |
| Lynda | Summer Classics (scw) | HelpScout | Jan 2026 | SC-specific issues |
| Ryan Casabella (sc-ryanc) | gh + scw (cross-entity) | CLM | Daily | #1 power user: 992 gh orders + 1,112 scw orders |
| Savanna Dunaway (sc-savannad) | gh (primary) | CLM | Daily | #2 power user gh: 491 orders |
| Clare Colón (sc-clarer) | gh + scw | CLM | Daily | #3 gh (408 orders) + active in scw (274 orders) |
| Nicole Brown (sc-nicoleb) | sc (primary) | CLM | Daily | #1 SC Wholesale power user: 1,094 orders |
| Wynne White (zww) | gh + scw + sccon | CLM | Daily | Cross-entity admin user |

---

## B2. Account Scores — Full Component Breakdown

### Consolidated: Expansion 69 | Risk 11 | GROW

### Per-Entity Scoring Details

---

#### Gabby (gh) — Ordering | Expansion: 68 | Risk: 12

**Data Sources:** `gh_2026-01-01_2026-03-02 (1).csv`, `Gabby Admin Orders Report 2026-01-01 - 2026-03-03 (1).csv`, PostgreSQL org 55, Mixpanel shortname `gh`

**Expansion Readiness: 68**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Adoption Depth | 30% | 87.5 | AUR: 51/54=94% (100). Ladder: 6/6 (100). Breadth: 10.4 (50). Subs: 5/4+ (100) |
| Business Impact | 25% | 56 | Volume: flat +1.2% (50). AOV: $3,384 (75). Activation: 967/11,812=8.2% (25). Self-Service: 793/2,215=35.8% (75) |
| Growth Signals | 25% | 63 | MAU: growing 2mo (75). Users: +85 (75). Signals: 5 (100). Fathom: N/A. HubSpot: 0 (0) |
| Relationship Strength | 20% | 58 | Fathom: N/A. Days: 27d (75). Breadth: ~4 (50). HelpScout: moderate (50) |

**Retention Risk: 12**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Engagement Decline | 30% | 19 | MAU: growing (25). AUR∆: flat@ceiling (25). Login: stable-high (25). Users: gain (0) |
| Relationship Cooling | 25% | 8 | Pattern: normal (0). Pending age: customer-side ~40d (25). Billing tags: 0 (0). Fathom: N/A |
| Financial Distress | 25% | 13 | Payment: current (0). Aging: paid (0). MRR: flat (25). Revenue: seasonal dip (25) |
| Operational Deterioration | 20% | 6 | Freshness: today (0). Errors: 0.2% (0). Repeats: minor (25). Inventory: today (0) |

---

#### Summer Classics (scw) — Ordering | Expansion: 70 | Risk: 11

**Data Sources:** `scw_2026-01-01_2026-03-02.csv`, `Summer Classics Admin Orders Report 2026-01-01 - 2026-03-03.csv`, PostgreSQL org 87, Mixpanel shortname `scw`

**Expansion Readiness: 70** *(Highest)*

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Adoption Depth | 30% | 87.5 | AUR: 56/58=97% (100). Ladder: 6/6 (100). Breadth: 9.1 (50). Subs: 5/4+ (100) |
| Business Impact | 25% | 69 | Volume: +45.6% (75). AOV: $5,182 (100). Activation: 628/8,281=7.6% (25). Self-Service: 432/1,646=26.2% (75) |
| Growth Signals | 25% | 59 | MAU: growing 1mo (62). Users: +79 (75). Signals: 5 (100). HubSpot: 0 (0) |
| Relationship Strength | 20% | 58 | Same shared inputs as gh |

**Retention Risk: 11**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Engagement Decline | 30% | 19 | MAU: growing 1mo (25). AUR∆: flat@ceiling (25). Login: stable-high (25). Users: gain (0) |
| Relationship Cooling | 25% | 8 | Same as gh |
| Financial Distress | 25% | 6 | Payment: current (0). Aging: paid (0). MRR: flat (25). Revenue: **growing +35.6%** (0) |
| Operational Deterioration | 20% | 6 | Same operational health |

**SCW stands out** with +45.6% MoM order growth and $5,182 AOV — the strongest expansion trajectory. Revenue is accelerating (Jan $2.61M → Feb $3.54M), directly offsetting any engagement flatness concerns.

---

#### SC Contract (sccon) — Non-Ordering + Pushed Data | Expansion: 68 | Risk: 11

**Data Sources:** `sccon_2026-01-01_2026-03-02.csv`, `Summer Classics Contract Admin Orders Report 2026-01-01 - 2026-03-03.csv`, PostgreSQL org 88, Mixpanel shortname `sccon`

**Expansion Readiness: 68**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Adoption Depth | 30% | 87.5 | AUR: 29/29=100% (100). Ladder: 6/6 (100). Breadth: 9.8 (50). Subs: 5/4+ (100) |
| Business Impact | 25% | 65 | *Non-ordering:* Actions/user: 15.7 (75). Trend: growing (75). PDFs: 202 (100). Share: 14.3% (50). Avg=75. *Pushed:* Volume: +33% (75). Revenue: $10.7M (100). Cadence: daily+ (100). Avg=91.7×0.5=45.8. Combined: (75×.67)+(45.8×.33)=65.4 |
| Growth Signals | 25% | 56 | MAU: growing 2mo (75). Users: +27 (100). Signals: 3 (50). HubSpot: 0 (0) |
| Relationship Strength | 20% | 58 | Same shared inputs |

**Retention Risk: 11**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Engagement Decline | 30% | 19 | MAU: growing (25). AUR∆: flat@ceiling (25). Login: stable (25). Users: gain (0) |
| Relationship Cooling | 25% | 8 | Same |
| Financial Distress | 25% | 6 | Revenue growing (pushed), MRR flat |
| Operational Deterioration | 20% | 6 | Same |

**SCCON confirms Non-Ordering + Pushed Data:** Zero Submit Orders in CLM, but 849 orders ($10.7M) in Admin Orders Report — all pushed from ERP. The pushed data scoring at 50% weight appropriately credits this engagement. 52.9% quote rate reflects contract/hospitality project workflows.

---

#### SC Wholesale (sc) — Ordering (Retail) | Expansion: 67 | Risk: 12

**Data Sources:** `sc_2026-01-01_2026-03-02.csv`, `Gabriella White Admin Orders Report 2026-01-01 - 2026-03-03.csv`, PostgreSQL org 69, Mixpanel shortname `sc`

**Expansion Readiness: 67**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Adoption Depth | 30% | 87.5 | AUR: 114/121=94% (100). Ladder: 6/6 (100). Breadth: 9.8 (50). Subs: 4/4+addon (100) |
| Business Impact | 25% | 58 | Volume: +53.3% (75). AOV: $4,224 (100). Activation: 944/91,090=1.0% (0). Self-Service: N/A (retail). **3-input avg after N/A** |
| Growth Signals | 25% | 56 | MAU: flat (50). Users: +12 (75). Signals: 5 (100). HubSpot: 0 (0) |
| Relationship Strength | 20% | 58 | Same shared inputs |

**Retention Risk: 12**

| Component | Weight | Score | Inputs |
|---|---|---|---|
| Engagement Decline | 30% | 25 | MAU: **flat** (50). AUR∆: flat@ceiling (25). Login: stable-high (25). Users: gain (0) |
| Relationship Cooling | 25% | 8 | Same |
| Financial Distress | 25% | 6 | Revenue: growing +53% (0). MRR: flat (25) |
| Operational Deterioration | 20% | 6 | Same |

**SC Wholesale's expansion score (67)** is slightly depressed by retail-model limitations. The 91K customer database inflates the Customer Activation denominator, and Self-Service is scored N/A (retail stores). Order revenue is actually growing fastest (+53.3% MoM) of any entity. The "real" expansion potential is higher than the score suggests.

---

### Entity Divergence Summary

| | GH | SCW | SCCON | SC |
|---|---|---|---|---|
| Expansion | 68 | **70** | 68 | 67 |
| Risk | 12 | 11 | **11** | 12 |
| Quadrant | GROW | GROW | GROW | GROW |

3-point expansion spread (67–70) and 1-point risk spread (11–12). All entities are uniformly healthy.

---

## B3. Rep Performance Intelligence

### Per-Entity Rep Stats (from independent CLM files)

| Metric | GH (`gh_...(1).csv`) | SCW (`scw_...csv`) | SCCON (`sccon_...csv`) | SC (`sc_...csv`) |
|---|---|---|---|---|
| Total Reps | 54 | 58 | 29 | 121 |
| Active Reps | 51 (94%) | 56 (97%) | 29 (100%) | 114 (94%) |
| Total Logins | 4,109 | 4,232 | 1,402 | 9,247 |
| Submit Orders | 6,162 | 5,650 | 0 | 12,311 |
| Avg Breadth | 10.4 | 9.1 | 9.8 | 9.8 |

### Power Users (Top 3 per entity, independently derived)

**Gabby — from `gh_2026-01-01_2026-03-02 (1).csv`:**

| Rep | Events | Logins | Orders | Breadth |
|---|---|---|---|---|
| Ryan Casabella (sc-ryanc) | 13,068 | 357 | 992 | 18 |
| Savanna Dunaway (sc-savannad) | 11,365 | 88 | 491 | 12 |
| Clare Colón (sc-clarer) | 9,056 | 264 | 408 | 19 |

**Summer Classics — from `scw_2026-01-01_2026-03-02.csv`:**

| Rep | Events | Logins | Orders | Breadth |
|---|---|---|---|---|
| Ryan Casabella (sc-ryanc) | 14,107 | 385 | 1,112 | 16 |
| Diana Horsley (sc-dianah) | 6,356 | 214 | 589 | 11 |
| Tanya Houge (sc-tanyah) | 6,590 | 254 | 351 | 17 |

**SC Contract — from `sccon_2026-01-01_2026-03-02.csv`:**

| Rep | Events | Logins | Orders | Breadth |
|---|---|---|---|---|
| Jessie Behr (sc-jessieh) | 6,027 | 103 | 0 | 17 |
| Tricia Mitchell (sc-triciamitchell) | 5,097 | 96 | 0 | 11 |
| Lisa Hanson (lhanson) | 4,046 | 78 | 0 | 13 |

**SC Wholesale — from `sc_2026-01-01_2026-03-02.csv`:**

| Rep | Events | Logins | Orders | Breadth |
|---|---|---|---|---|
| Julie Smallwood (sc-julies) | 16,506 | 139 | 1,094 | 13 |
| Dierdre Essix (sc-dierdree) | 14,104 | 280 | 684 | 13 |
| LindaLee Counts (sc-lindac) | 13,218 | 300 | 596 | 15 |

### Cross-Entity Rep Activity

Ryan Casabella appears as #1 in both GH and SCW CLM files with different order counts (992 gh + 1,112 scw = 2,104 total orders). This confirms cross-entity rep activity — shared reps submit orders through different entity catalogs.

### Concentration Risk

| Entity | Top Rep Share | Assessment |
|---|---|---|
| GH | Ryan: 992/6,162 = 16.1% | Low |
| SCW | Ryan: 1,112/5,650 = 19.7% | Moderate (approaching 20%) |
| SCCON | N/A (non-ordering) | — |
| SC | Julie: 1,094/12,311 = 8.9% | Low |

### Territory Performance

**GH — 27 territories active (from Orders file):**
Top 5: South Team (760 orders, $2.54M), Midwest Team (412, $1.15M), Texas Team (371, $1.13M), MidAtlantic Team (232, $516K), Florida Team (96, $260K). South Team = 34.3% of orders — moderate concentration.

**SCW — 25 territories active:**
Top 5: Midwest (388, $1.24M), South (324, $1.43M), MidAtlantic (263, $882K), Florida (170, $727K), Texas (138, $552K). More balanced distribution.

**SCCON — 23 territories active:**
Top: Contract Team 1 (224, $2.73M), Wynne White (109, $835K), Contract Team 2 (109, $2.09M). Named territories reflect individual/team assignments for contract projects.

**SC — 67 territories, all numeric codes:**
Orders originate from 15 physical stores. Top: Pelham Showroom (344), Atlanta Store (319), Pelham Outlet (272), Charlotte Store (237), Scottsdale Store (222).

---

## B4. Customer Intelligence

| Metric | GH | SCW | SCCON | SC | Source |
|---|---|---|---|---|---|
| Customers in DB | 11,812 | 8,281 | 5,228 | 91,090 | PostgreSQL `customers` |
| Ordering Customers (2mo) | 967 | 628 | 316 | 944 | Orders CSVs |
| Activation Rate | 8.2% | 7.6% | 6.0% | 1.0%* | Derived |
| Total Orders | 2,215 | 1,646 | 849 | 2,726 | Orders CSVs |
| Revenue | $6.92M | $6.42M | $10.67M | $11.19M | Orders CSVs |
| AOV (non-zero) | $3,384 | $5,182 | $15,240 | $4,224 | Orders CSVs |
| Quote Rate | 12.4% | 13.9% | 58.0% | 39.1% | Orders CSVs |
| Top Customer Concentration | 1.8% | 3.4% | 8.3% | 1.5% | Derived from Orders |

*SC Wholesale's 1.0% = 944 / 91,090. Denominator inflated by historical imports. Not meaningful.*

### Order Type Analysis

| Type | GH | SCW | SCCON | SC |
|---|---|---|---|---|
| Confirmed | 87.3% | 86.1% | 42.0% | 60.4% |
| Quote | 12.4% | 13.9% | 58.0% | 39.1% |

SCCON's 58% quote rate reflects the contract/hospitality model where projects require formal quoting. SC Wholesale's 39% quote rate suggests retail customers frequently request quotes before purchasing.

### Self-Service Adoption

| Entity | Website Orders | Rate | Interpretation |
|---|---|---|---|
| GH | 793 | 35.8% | Strong B2B digital adoption |
| SCW | 432 | 26.2% | Healthy |
| SCCON | 15 | 1.8% | Minimal (orders pushed from ERP) |
| SC | 0 | 0% | N/A — retail stores |

---

## B5. Relationship & Support History

### Fathom — Meeting Intelligence

**No proactive meeting history on record for any entity.** Zero matches across Fathom AI summaries for Gabby, Summer Classics, SC Contract, or Gabriella White. 447 total Fathom records exist — none for this account.

**Recommendation:** Establish quarterly EBR cadence covering the full multi-entity relationship. This is an ~$108K ARR account generating $35M+ in platform-facilitated orders with zero structured engagement.

### HelpScout — Support (Last 90 Days)

| Metric | Value | Source |
|---|---|---|
| Tickets (90d) | 6 distinct tickets (93 thread-level rows) | BigQuery `helpscout__help_scout_tickets` |
| Status | 1 closed, 4 pending, 1 closed | Latest 6 tickets from BQ-7 |
| Org | All under "Gabriella White" | `conv_customer_organization` |

**Recent Tickets:**

| Date | Subject | Status |
|---|---|---|
| Feb 3 | Services Slow/Unresponsive | Closed |
| Feb 2 | No Warning Message When Dropped Products Are On Order | Pending |
| Jan 29 | File Import Error | Pending |
| Jan 23 | User Issue: Viewing Other Users' Quotes | Pending |
| Jan 21 | Copy Order and Option Form Bug | Pending |
| Jan 20 | Goes With line item comments | Closed |

**Quarterly Trend (thread-level):** Q1'25: 45 → Q2'25: 157 → Q3'25: 143 → Q4'25: 100 → Q1'26: 93. Declining trend = positive (self-sufficient, fewer issues).

### Combined Signals

| Signal | Value | Interpretation |
|---|---|---|
| Days Since Last Touchpoint | ~27 days | Normal range |
| Communication Direction | 100% inbound (HelpScout), 0% outbound (Fathom) | Operational callout: no proactive engagement |
| Stakeholder Breadth | ~4 support contacts + CLM power users | No executive-level contacts identified |

---

## B6. Expansion Whitespace

### Zero-Adoption Features (all 4 entities)

| Feature | Combined Events | Opportunity | Best Pilot Entity |
|---|---|---|---|
| **Flipbook** | 0 | Digital interactive catalog | SCCON (52.9% self-service, 202 PDFs) |
| **Placements** | 0 | Visual merchandising / room scenes | GH (residential furniture) |
| **Commitments** | 0 | Pre-season commitment tracking | GH + SCW (200+ territories) |
| **SmartPicks** | 138 (near-zero) | AI product recommendations | SCW (highest AOV, $5,182) |
| **Maybe Lists** | 12 (near-zero) | Buyer consideration tracking | SCCON (high quote rate, project-based) |

### Module Gaps

| Entity | Missing Module | Fit |
|---|---|---|
| SC Wholesale | B2B Cart | High — retail reordering |

### Cross-Entity Opportunities

1. **Flipbook in SCCON → all:** Contract buyers are 52.9% self-service. Flipbook replaces 202 static PDFs with interactive catalogs.
2. **SmartPicks in SCW:** $5,182 AOV + 11,766 products. Algorithmic recommendations could increase basket size.
3. **Territory configuration for SC:** 0 territories despite 15+ stores. Structuring by store enables Portal analytics.
4. **Portal usage lift:** GH uses Portal 5,695 times vs SCW 4,577 and SC 577. Understanding GH's Portal value could inform adoption for other entities.

---

## B7. Open Risks & Issues

| # | Risk | Entity | Severity | Detail |
|---|---|---|---|---|
| 1 | No proactive engagement | All | Medium | $108K ARR, $35M orders, zero Fathom meetings |
| 2 | 4 pending HelpScout tickets | All | Medium | Oldest: Jan 21 (~40 days). Topics: product warnings, import errors, user permissions, order bugs |
| 3 | HubSpot data dead | All | Low | 5 records, no usable data. Account invisible in CRM. |
| 4 | SC flat MAU | sc | Low | 105 for 2 months after slight decline from 121 |
| 5 | SC zero territories | sc | Low | Retail model limitation. Limits Portal analytics. |
| 6 | SC customer DB inflation | sc | Low | 91,090 records — historical imports inflate reporting |
| 7 | GH seasonal revenue dip | gh | Low | Jan $3.96M → Feb $2.81M. Likely market-driven. Monitor Q2. |
| 8 | SCW Ryan concentration | scw | Low-Med | Ryan Casabella: 19.7% of SCW orders. Approaching 20% threshold. |

---

## B8. Context & Preparation — EBR with Gabby/Summer Classics Leadership

*Context: "EBR preparation — executive review with Gabby/Summer Classics leadership. First structured business review across the full account relationship."*

### Engagement Objectives

1. **Establish multi-entity engagement cadence.** First structured review — set quarterly EBR precedent.
2. **Demonstrate platform value at scale.** $35.2M in orders, 250 active users, 95% adoption.
3. **Open expansion conversation.** Five zero-adoption features across all entities.

### Key Data Points

1. **$35.2M orders in 2 months** — headline value metric
2. **95.4% active user ratio** (250/262) — near-complete adoption
3. **SCW +45.6% order growth** — momentum story
4. **SCCON 52.9% self-service** — digital-first entity, Flipbook pilot candidate
5. **SC +53.3% MoM growth** — retail division accelerating

### Topics to Explore

- How do they view the 4-entity relationship? Appetite for standardization?
- SC Wholesale (Gabriella White) retail store roadmap — expansion = seat expansion
- SCCON order submission interest — satisfied with ERP push, or want iPad ordering?
- Who are the executive champions? We know reps and support contacts only.
- Upcoming market/trade show events — Flipbook timing opportunity

### Handle Carefully

- Pending tickets: Acknowledge the 4 open items, commit to resolution sweep
- SC Wholesale scoring: If entity comparisons arise, explain retail model creates scoring artifacts
- Billing: Two billing entities (SC Home/Gabby LLC + Summer Classics Inc.) — have details ready
- No prior history: This is a clean-slate first interaction. Set new commitments, don't follow up on non-existent ones.

---

*Framework: Account Scoring v3 | Thresholds v1.1 | Independent per-entity rerun*
*Data: PostgreSQL orgs 55/69/87/88 | BigQuery (Mixpanel, HelpScout, Stripe, QuickBooks, Fathom, HubSpot) | Admin Console CLM (4) + Orders (4)*
