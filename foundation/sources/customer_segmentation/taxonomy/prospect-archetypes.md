---
id: TAX-B
title: Layer B — Prospect Archetypes
version: 0.1
status: hardened
date: 2026-08-25
hardened: 2026-08-26
owner: Kylor Johnson
layer: B
availability: pre-sale
source_lineage:
  - Public company websites, manually reproducible observation (fetched 2026-08-25)
  - Postgres (read-only): organizations.company_website  # domain resolution only
  - foundation/07_how_we_establish_truth.md              # principle 7 — enrichment validated against, never seeded from
depends_on: []
consumed_by: [TAX-MAP]
---

# Layer B — Prospect Archetypes

**What this layer is.** Classification built **only** from features observable before a company is
a SuperCat customer. Every feature here is verifiable by a person with a browser.

**The naming rule, and its authority.** No archetype may carry an Account Segment's name, and no
Layer B output may be presented as a Layer A value. This is not a style preference — it is
`foundation/07_how_we_establish_truth.md` **principle 7**: *"Segments, types, and scores are derived
from what customers actually do, never imposed from an external label or an LLM-enrichment guess.
Enrichment is validated against, never seeded from."* Layer B **is** enrichment. Naming an
archetype "Luxury Specification" would seed a first-party segment from an external observation,
which principle 7 forbids.

Consequently every archetype below is named for **what was observed**, never for the motion it is
suspected to imply.

---

## 1. Collection reality — what can actually be gathered

`[MEASURED]` 2026-08-25, roster n=109:

| State | n | Orgs |
|---|---:|---|
| Automated observation succeeded | **87** | the back-test set |
| Site live but bot-blocked or JS-only shell → **manual-only** | 7 | `afx`, `ol`, `shl` (Cloudflare challenge), `eglo`, `eglo_can` (503), `mlc`, `sarreid` (empty shell) |
| Domain dead (DNS fail / 404) | 6 | `arl`, `cl`, `pw`, `soi`, `tl`, `uhc` |
| No domain recorded in Postgres | 9 | `all`, `dals`, `hf`, `hvl`, `ilc`, `mlg`, `ssi`, `ufi`, `yw` |

**80% of the roster is automatable; a human with a browser reaches 86%.** The 7 manual-only orgs
include `shl` (Savoy House) — the Phase 4 lane-3 lookalike — which is why lane 3's criteria must be
manually derivable.

Method: homepage fetch with a browser user-agent, plus up to 5 internal pages whose URL or anchor
text matched trade / dealer / rep / contract / where-to-buy / login / catalog keywords. 275 subpages
fetched. No marketplace or dealer-locator API was touched.

---

## 2. Feature register

Every candidate feature from the brief, with what happened when I tried to collect it.

### 2.1 KEPT — collectible and automatable

| Feature | What it is | Where observable | Collection | Hit rate (n=87) |
|---|---|---|---|---:|
| `TRADE_GATE` | Site gates access behind trade/designer credentials | Nav, account pages, "to the trade" copy | Auto | 28 (32%) |
| `DEALER_PORTAL` | Named dealer/retailer/wholesale login or resource area | Nav, footer, login pages | Auto | 21 (24%) |
| `RETAIL_ECOM` | Consumer cart mechanics present | "add to cart"/"checkout" strings | Auto | 25 (29%) |
| `PRICE_VISIBLE` | Prices publicly listed | `$nn.nn` pattern on public pages | Auto | 14 (16%) |
| `WHERE_TO_BUY` | Dealer/store/showroom locator offered | Nav, footer | Auto | 41 (47%) |
| `REP_NETWORK` | Published rep or territory structure | Rep locator, territory pages, "sales representative" | Auto | 22 (25%) |
| `CONTRACT_SPEC` | Hospitality / contract / A&D / spec-sheet language | Body copy, dedicated contract pages | Auto | 49 (56%) |
| `COM_PROGRAM` | Customer's Own Material programme | Product/ordering copy | Auto | 18 (21%) |
| `CATALOG_DL` | Downloadable catalog / price list / tearsheets | Nav, resource pages | Auto | 23 (26%) |

### 2.2 KEPT BUT LOW-VALUE — collectible, poor discrimination

| Feature | Hit rate | Why kept |
|---|---:|---|
| `COLLECTIONS_NAV` | 76 (87%) | Near-universal in this industry; useful only as a category sanity check |
| `LOGIN_ANY` | 76 (87%) | Near-universal; superseded by `TRADE_GATE` / `DEALER_PORTAL` |
| `FOUNDED` | 24 (28%) | Tenure proxy; no observed segment separation |
| `MARKETPLACE` | 11 (13%) | Self-declared marketplace presence only; no separation observed |

### 2.3 PRUNED — could not be collected

| Candidate feature (from the brief) | Verdict | Evidence |
|---|---|---|
| **Rep recruiting pages** | **Prune** | `[MEASURED]` **0 hits across all 87 sites.** "Become a rep", "rep opportunities", "seeking representation" appear nowhere. The feature does not exist in observable form |
| **MAP policy** | **Prune** | `[MEASURED]` **1 hit across 87 sites.** Publicly posted MAP policy is essentially absent in this industry |
| **SKU depth / catalog size** | **Prune** | Not publicly countable. This is `product_count` — a Layer A field. Keeping it would be a Layer A field wearing a Layer B label |
| **Collection vs program organisation** | **Prune as a cut** | `COLLECTIONS_NAV` fires on 87% of sites; "program" organisation is not distinguishable from public nav |
| **Price positioning from listed prices** | **Downgrade to conditional** | Only 16% of sites list any price. Available only when `PRICE_VISIBLE`=1, so it cannot be a primary feature |
| **HPMKT footprint** (showroom vs temporary, building, sq ft, tenure) | **Keep, MANUAL ONLY — not collected** | Not present on company websites. Requires the HPMKT exhibitor directory. **No values gathered; this feature is unpopulated and contributes nothing to the back-test below** |
| **LinkedIn headcount** | **Keep, MANUAL ONLY — not collected** | LinkedIn blocks automated access. Unpopulated |
| **Facility count** | **Prune** | Not reliably stated publicly |
| **Agency listings** | **Prune** | Rep agency rosters are not published by manufacturers; the reverse direction (agency sites listing lines) is a different data source, not a feature of the prospect |

**Three of the brief's named candidate features do not survive contact with the data**
(`rep recruiting`, `MAP policy`, `SKU depth`), and two more are real but were not collected
(`HPMKT footprint`, `LinkedIn headcount`). The archetypes below therefore rest on **web channel
signals only** — that is a material limit on this layer and is carried into the back-test.

---

## 3. The archetypes

Defined as boolean rules over §2.1 features. First match wins. No scoring, no weights.

| ID | Name | Definition | n (of 87) |
|---|---|---|---:|
| ARCH-01 | **Trade-Gated Access** | `TRADE_GATE` AND NOT `RETAIL_ECOM` | 20 |
| ARCH-03 | **Open-Price Retail Presence** | `RETAIL_ECOM` OR `PRICE_VISIBLE` | 26 |
| ARCH-02 | **Dealer-Locator Network** | `WHERE_TO_BUY` OR `REP_NETWORK` OR `DEALER_PORTAL` | 25 |
| ARCH-04 | **No Public Channel Signal** | none of the above fire | 16 |

Evaluation order is ARCH-01 → ARCH-03 → ARCH-02 → ARCH-04. ARCH-03 precedes ARCH-02 because a
consumer cart is a stronger and less ambiguous observation than a dealer locator, which many
brands publish regardless of motion.

**Names describe the observation, not the inferred motion.** "Trade-Gated Access" says the site
gates access; it does not claim the company sells by specification. That claim is a Layer A
question and belongs to the mapping document, where it is measured rather than assumed.

---

## 4. Known limits of this layer

1. **Web presence is a proxy for web strategy, not for selling motion.** A company can run a
   dealer network and publish nothing about it.
2. **A brand family shares a site.** `visualcomfort.com` serves four separate roster orgs; each
   inherits identical Layer B features while carrying its own Layer A label. Layer B cannot
   distinguish sibling brands `[MEASURED]`.
3. **Sites change.** Every observation is stamped 2026-08-25 and needs re-observation before reuse.
4. **The absence of a marker is weak evidence.** Not finding "to the trade" means the crawler did
   not find it, not that the company sells openly — especially for the 7 manual-only orgs.

---

## 5. The method gap — what this layer's failure does and does not prove

This layer scores **33.3%** against a **34.5% majority-class baseline (n=87)**. The established
prior run scored **53%** against a **30% baseline**. Those two numbers are not in conflict, and the
difference is **method, not data**:

| | This layer | The prior 53% run |
|---|---|---|
| Method | Binary feature extraction — regex over fetched pages, boolean markers, rule over markers | An LLM reading whole sites and inferring holistically |
| What it can see | Presence/absence of specific vocabulary | Tone, assortment, price positioning, who the copy is written for |
| Fails when | The company uses different words for the same thing | — |

**A worked example of the failure mode, from the lane-1 exemplar.** Interlude Home is SEG-01 and is
plainly trade-oriented, but scores `TRADE_GATE = 0`. Its site gates by **"DESIGNER RESOURCES"** and
**"CREATE AN ACCOUNT"**, with no public prices `[OBSERVED: interludehome.com nav, 2026-08-25]` —
real gating in vocabulary my markers did not match. A person reading that homepage identifies the
gating in seconds. A regex for "to the trade" does not.

So the correct claim is narrow:

> **Binary public feature extraction cannot predict a v4.0 segment. Holistic reading gets to
> roughly 53%. Neither is good enough to put a v4.0 segment label on a prospect.**

It is **not** "public data cannot predict segment." That overstates the finding, and it would be
the wrong lesson to carry into the field kit — **because the field kit is the holistic method**: a
person with a browser forming a judgment, not a checklist. The gap is not closed here by design;
Phase 4 tests it for free, since the field kit runs the holistic method on fresh companies.

---

Per-archetype accuracy against the answer key is in
[`segment-archetype-mapping.md`](segment-archetype-mapping.md). Read it before using any archetype
for a decision — **three of the four fail to beat baseline.**
