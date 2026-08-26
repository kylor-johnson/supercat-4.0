---
id: PROS-CRIT
title: HPMKT lane criteria — screen definitions, pre-sourcing
version: 0.1
status: draft-for-review
date: 2026-08-25
owner: Kylor Johnson
purpose: Define the observable screen for three HPMKT prospect lanes. No companies sourced yet.
source_lineage:
  - taxonomy/prospect-archetypes.md      # observable feature register
  - taxonomy/segment-archetype-mapping.md # ARCH-01 exclusion power
  - Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv  # exemplar stamped labels
  - Direct observation of exemplar sites, 2026-08-25
depends_on: [TAX-A, TAX-B, TAX-MAP]
---

# HPMKT lane criteria

**Status: criteria only. No candidate has been sourced.** Review gate before any company research.

---

## 1. The screen is not a classifier

Phase 4 does not route through archetype → segment prediction, and never needed to. That path
predicts at 33.3% against a 34.5% majority baseline (n=87) and would poison the candidate list.

The screen has three components, applied in this order:

| Order | Component | What it does | Strength |
|---|---|---|---|
| **a** | **Category filter** — furniture / lighting / décor | Does most of the work. Publicly observable at near-100% | Strong, cheap |
| **b** | **Lookalike match** — resemblance to the lane's named exemplar | Characterises the anchor on the open web; does not ask "which segment is this?" | Moderate, manual |
| **c** | **ARCH-01 exclusion** — trade-gated access | Disqualifies only. **Never assigns** | Strong as a negative: 0 of 20 trade-gated roster orgs are SEG-03, 1 of 20 SEG-04 `[MEASURED]` |

Category is the load-bearing component because it is the one thing the public web reports
reliably. Everything after it narrows a category list; nothing after it is trusted to label.

---

## 2. Exemplar reference vectors

The three anchors, as they actually appear — stamped label plus observed features. This is the
reference to match against, not a segment definition.

| | **Interlude Home** (`ih`) | **Braxton Culler** (`bcf`) | **Savoy House** (`shl`) |
|---|---|---|---|
| Stamped segment `[MEASURED]` | SEG-01 Luxury Specification | SEG-02 Premium Trade Brand | SEG-03 Mid-Market Multi-Channel |
| Roster `what_they_sell` | Furniture | Furniture | Lighting |
| Roster `who_they_sell_to` | Trade (Designers/Architects) | Wholesale (Dealers) | Wholesale (Dealers/Retailers) |
| Observed nav `[OBSERVED 2026-08-25]` | DESIGNER RESOURCES · CREATE AN ACCOUNT · SHOWROOMS · CONTRACT · FIND A REP · IH Collections · Custom Upholstery · Quick Ship | Find A Store · **Dealer Portal** · **Apply to Become a Dealer** · **Dealer Locator** · Showroom Information · Room Planner · Warranty | **UNKNOWN — Cloudflare-blocked to both `curl` and automated fetch** |
| Assortment shape | Bedroom / Dining / Living / Office / **Décor** | **Seating-dominant**: chairs, sofas, sectionals, sleepers, swivel, recliners, loveseats, chaises, slipcovered | UNKNOWN |
| Public prices / cart | No / No | No / No | UNKNOWN |
| Rep network published | **Yes** ("FIND A REP") | No | UNKNOWN |
| Dealer locator | No | **Yes** | UNKNOWN |
| Contract language | **Yes** | No | UNKNOWN |

**Two findings from this table drive the criteria below.**

**(i) The lane-1 and lane-2 anchors separate on vocabulary, not on structure.** Both are furniture,
both hide prices, both have no consumer cart. The cut is **designer-facing vs dealer-facing
language**: Interlude says *designer, showroom, contract, find a rep*; Braxton Culler says *dealer,
apply to become a dealer, find a store*. That is a manual read, and it is exactly what a person
does in ten seconds on a homepage.

**(ii) Interlude Home scores `TRADE_GATE = 0`.** The lane-1 anchor does not fire the lane-1-adjacent
marker, because it gates via "DESIGNER RESOURCES" + "CREATE AN ACCOUNT" rather than "to the trade."
**Criteria are therefore written as observations a person makes, not as strings a crawler matches.**
Where a criterion is marked automatable, that is a convenience for building the longlist — the
judgment is always the human one.

**Savoy House cannot be observed automatically.** Lane 3's criteria are written so every one of them
is manually verifiable, and the anchor itself needs a manual pass before the field kit runs.

---

## 3. Cohort evidence behind the criteria

Marker rates within each lane's roster cohort `[MEASURED 2026-08-25]`, automated observation only:

| Marker | Lane 1 cohort — SEG-01 × Furniture (n=17) | Lane 2 cohort — SEG-02 × Furniture (n=6) | Lane 3 cohort — SEG-03 × Lighting (n=11) |
|---|---:|---:|---:|
| Visible consumer prices | **0/17** | **0/6** | 1/11 |
| Consumer cart | 1/17 | 1/6 | 2/11 |
| Dealer/store locator | 5/17 | 4/6 | **9/11** |
| Trade/designer gating | 6/17 | 2/6 | **1/11** |
| COM programme | 5/17 | 1/6 | **0/11** |
| Contract / hospitality language | **10/17** | 2/6 | 6/11 |
| Published rep network | 4/17 | 1/6 | 5/11 |
| Downloadable catalog / price list | 6/17 | 2/6 | 5/11 |

Lane 2's cohort is n=6. **Every lane-2 rate below is low-confidence** and is used for exclusion
only, never inclusion.

---

## 4. Lane 1 — Luxury Spec × Furniture (anchor: Interlude Home)

Specify-into-a-project, High Point-native.

| # | Criterion | What it is | Where observable | Collection | Use |
|---|---|---|---|---|---|
| 1.1 | **Furniture is the primary category** | Case goods, upholstery, occasional — furniture leads the nav, not accessories or lighting | Homepage nav / category structure | **Auto** | **INCLUDE** |
| 1.2 | **Designer-facing account gate** | Account required to see pricing or order; the audience named is designer / trade / to-the-trade. Vocabulary varies — "Designer Resources", "Trade Program", "Create an Account" all count | Homepage nav, account/registration page | **Manual** (auto assists) | **INCLUDE** |
| 1.3 | **No consumer prices and no consumer cart** | A retail shopper cannot see a price or buy | Any product page | **Auto** | **EXCLUDE if present** — 0/17 of the lane-1 cohort show prices |
| 1.4 | **Project/contract vocabulary** | Hospitality, contract, A&D, specification, COM, tearsheets, custom upholstery | Nav, dedicated contract page, product copy | **Auto** | **INCLUDE** (supporting — 10/17 cohort) |
| 1.5 | **HPMKT permanent showroom** | Named building + space, not a temporary or shared booth; multi-market tenure | HPMKT exhibitor directory; company "Showrooms" page | **MANUAL** | **INCLUDE** (supporting) |
| 1.6 | **No consumer-facing store locator** | Absence of "find a store near you" aimed at end consumers | Homepage nav / footer | **Auto** | **EXCLUDE if present** (weak — 5/17 cohort do have one) |

**Disqualifiers:** visible consumer pricing (1.3). Dealer-application vocabulary dominant over
designer vocabulary → this is lane 2, not lane 1.

---

## 5. Lane 2 — Premium Trade × Furniture (anchor: Braxton Culler)

Dealer seating and casual. **Explicitly not décor accessories.**

| # | Criterion | What it is | Where observable | Collection | Use |
|---|---|---|---|---|---|
| 2.1 | **Seating or casual furniture is the assortment core** | Chairs, sofas, sectionals, recliners, slipcovered, outdoor/casual — not accessories, art, mirrors, or tabletop | Category nav depth | **Auto** | **INCLUDE** |
| 2.2 | **Décor-accessory house** | Assortment led by mirrors, art, tabletop, giftware, textiles | Category nav | **Auto** | **EXCLUDE — hard.** This is the lane's stated boundary |
| 2.3 | **Dealer-facing recruitment and access** | "Become a dealer" / "Apply to become a dealer" / dealer portal / dealer login. The company is openly recruiting stockists | Homepage nav, footer, dealer page | **Auto** | **INCLUDE** |
| 2.4 | **Consumer-facing dealer locator** | "Find a store" / "Where to buy" aimed at end consumers | Homepage nav | **Auto** | **INCLUDE** (supporting — 4/6 cohort, low confidence) |
| 2.5 | **Named collection/program structure** | Assortment organised into named collections carried as a line (e.g. Bedford, Bridgeport, Gramercy Park), not one-off SKUs | Collections nav | **Auto** | **INCLUDE** (supporting) |
| 2.6 | **HPMKT presence** | Showroom or established temporary space | HPMKT exhibitor directory | **MANUAL** | **INCLUDE** (supporting) |

**Disqualifiers:** décor-accessory assortment (2.2, hard). Designer-gated with no dealer
recruitment → lane 1. Visible consumer pricing with full DTC checkout → neither lane.

---

## 6. Lane 3 — Mid-Market × Lighting (anchor: Savoy House)

Programs, price codes, trade + retail + online. **Anchor is manually verifiable only.**

| # | Criterion | What it is | Where observable | Collection | Use |
|---|---|---|---|---|---|
| 3.1 | **Lighting is the primary category** | Decorative lighting — chandeliers, pendants, sconces, flush/semi-flush, fans | Homepage nav | **Auto** | **INCLUDE** |
| 3.2 | **Consumer-facing "where to buy"** | Store/dealer/retailer locator aimed at end consumers | Homepage nav / footer | **Auto** | **INCLUDE** — strongest positive: 9/11 cohort |
| 3.3 | **No trade/designer access gate** | Catalog is browsable without trade credentials | Homepage, product pages | **Manual** (auto assists) | **EXCLUDE if gated** — only 1/11 cohort is gated, and 0/20 trade-gated roster orgs are SEG-03 `[MEASURED]`. This is the ARCH-01 exclusion filter |
| 3.4 | **No COM programme** | No customer's-own-material offering | Product / ordering copy | **Auto** | **EXCLUDE if present** — 0/11 cohort. A COM programme indicates lane 1 |
| 3.5 | **Multi-channel evidence** | Product findable through more than one route — own site plus authorised online retailers, showrooms, or a retail-facing brand presence. Do **not** query marketplaces; observe what the company itself states | Company site; "where to buy" listings | **MANUAL** | **INCLUDE** |
| 3.6 | **Breadth over depth in assortment** | Wide catalog organised by fixture type and finish/program rather than a small curated aesthetic line | Category nav | **Manual** | **INCLUDE** (supporting) |

**Disqualifiers:** trade gating (3.3). COM programme (3.4). Pure commodity/utility lighting with
flat single-tier pricing → Volume Distribution territory, which is not a lane here.

---

## 7. Recording contract for every candidate

Binding when sourcing starts.

Each candidate row carries: name · domain · HPMKT presence (building/showroom if findable) ·
each lane criterion marked **met / not met / UNKNOWN** with a source URL and what was observed ·
lane-match confidence HIGH / MEDIUM / LOW · the single strongest disqualifying risk ·
mapped ARCH-id.

**Predicted segment — labelling is mandatory.** Every predicted Account Segment is written as:

> `PREDICTED SEG-0n — prediction only, not an assigned segment.`
> Pre-sale prediction accuracy: binary feature extraction 33.3% vs a 34.5% majority baseline
> (n=87); holistic reading ~53% vs a 30% baseline. The stamped Layer A rule itself reproduces only
> 38.5% vs a 34.9% majority baseline (n=109). **No prospect carries a bare segment label.**

**UNKNOWN is a valid and preferred answer.** Never invent a company detail. Do not scrape Wayfair,
1stDibs, or dealer-locator APIs — manual observation of a website is fine and expected.

---

## 8. What this screen is expected to get wrong

Stated in advance so Phase 5 can falsify it rather than rationalise it:

1. **Lane 1 vs lane 2 will be the error-prone boundary.** Both are furniture with hidden prices; the
   separator is vocabulary, and vocabulary is inconsistent across companies (finding (ii) above).
2. **Lane 2's evidence base is n=6.** Its inclusion criteria are the weakest in this document.
3. **Category may over-select.** Being a furniture company is necessary, not sufficient — most
   HPMKT exhibitors clear 1.1 or 2.1.
4. **Manual criteria (1.5, 2.6, 3.5) are unvalidated.** HPMKT footprint has never been collected
   for any roster org, so its discriminating power is genuinely unknown, not merely uncertain.
