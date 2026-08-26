---
id: PROS-DQ
title: Disqualified and flagged — the triage list
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
depends_on: [PROS-CRIT, PROS-L1, PROS-L2, PROS-L3]
---

# Disqualified and flagged

Near-misses are the point. This list is longer than the qualified lists combined — 21 qualified
across three lanes, **60+ disqualified or flagged here** — which is the intended ratio, because this
is what the field kit has to triage on a market floor.

Three reasons, kept distinct: **failed Gate 0** · **wrong lane** · **already a customer / open opp**.

---

## 1. Already a customer — excluded at source

**51 HPMKT exhibitors matched an existing SuperCat org by exact normalized name** `[MEASURED]`,
plus **21 more confirmed by hand as brand-family matches**. Excluded before any lane logic ran.

Exact matches include: Alden Home, Baker | McGuire, Bassett Mirror, Bethel International, Braxton
Culler, Buster + Punch, Butler Specialty, Century Furniture, Charleston Forge, Corbett, Crystorama,
Currey & Company, Decca/Bolier, DellaRobbia, Elegant Lighting, Elements International, El Ran,
Fairfield Chair, Fine Art Handcrafted Lighting, Four Seasons Furniture, Gabby, Geo Contemporary,
Highland House, Hooker Furnishings, Hubbardton Forge, Hudson Valley Lighting Group, Interlude Home,
Jamie Young, Jonathan Charles, Karat Home, Lucas + McKearn, Made Goods, Maxim Lighting, Moe's Home
Collection, Palecek, RENWIL, Rowe Furniture, Sarreid, Schonbek, Southern Furniture, Summer Classics,
The M|T Company, Theodore Alexander, Troy Lighting, Universal Furniture, Verellen, Wendover Art,
Wesley Allen.

Brand-family matches caught by hand after automated matching missed them:

| Exhibitor | Existing org | Why automation missed it |
|---|---|---|
| Chelsea House, Wildwood | `wwjc` Wildwood/Chelsea House | Compound org name |
| Hancock & Moore, Jessica Charles | `hmjc` | Compound org name |
| Kindel, Karges, Councill | `kkc` Kindel Karges | Extra brand in exhibitor name |
| Modern Forms | `wac` WAC/Modern Forms | Compound org name |
| Modern History Inc. | `sbmh` Somerset Bay and Modern History | Compound org name |
| Visual Comfort & Co. | `fms`/`vcg`/`tla`/`vce` | Four sibling orgs on one domain |
| Allegri Crystal by Kalco | `kal` Kalco/Allegri | Token order reversed |
| Tomlinson/Directional | `tel` Tomlinson Companies | Suffix differs |
| Oly | `ol` Oly Studio | Key too short for the length threshold |
| Mitzi | `hvl` Hudson Valley Lighting Group | Sub-brand, no separate org row |
| **Sauder** | `swc` Sauder Woodworking | 6-char key, below the ≥7 fuzzy threshold |
| Interlude Home Custom Upholstery | `ih` | Sub-brand |
| Coaster Fine Furniture, Homelegance, Intercon, Magnussen by Banner House, Pulaski by Banner House, McGuire, Palliser, Simply Amish, Style Line by Elements, Furniture Classics Ltd | various | Suffix/parent variants |

**Sauder reached a lane-2 ranking before being caught by hand.** Recorded as a live defect in the
dedupe method, not a near-miss: automated name matching under-catches at 6 characters and cannot see
brand families at all. **Any future sourcing pass must run the hand-adjudication step.**

### False positives — restored to the candidate pool

Automated fuzzy matching wrongly flagged these as existing customers. Verified distinct, kept:
American Woodcrafters, Atelier Home, **Bassett Furniture** (≠ Bassett Mirror), Brentwood Classics,
Classic Home, Elegant Earth, Parker Southern, Royal Classics, Southern Motion, Southern Roots by
Craftmaster.

---

## 2. Already in HubSpot — flagged, not dropped

**26 of 30 checked candidates already exist in HubSpot** `[MEASURED 2026-08-25]`. Useful intel for
the market kit; **must not be presented as fresh prospects.**

**Open deals — do not approach as new:**

| Company | Domain | Deals | Lane |
|---|---|---:|---|
| Jensen Outdoor | jensenoutdoor.com | **2** | L1 |
| Lexington Home Brands | lexington.com | **1** | L1 |
| JDouglas | jdouglas.com | **1** | L1 |

**Sales-qualified leads:** Steve Silver Company, England Furniture.
**Marketing-qualified leads:** Accent Decor, Albany Industries, Fireside Lodge, MINIFORMS.
**Leads:** Bellona USA, Coast Lamp Mfg, Continental Home, Delta Furniture Mfg, Fourteenth Colony
Lighting, Global Views, Green Gables, IMG Comfort, Jackson Catnapper, Kalalou, Lancer Furniture,
La Vida Abode, Najarian, Phillips Scott, Sligh, Sofamaster, St. James Lighting.

**Genuinely fresh (not in HubSpot, of those checked):** Mr. Brown London, Designmaster Furniture,
Home Trends and Design, Parker House Furniture, Sagebrook Home.

**Yield finding:** of 30 checked, **5 fresh = ~17%.** The HPMKT exhibitor frame is already largely
worked. That is a real constraint on the field kit's purpose and should shape what market week is
*for* — displacement and re-engagement conversations, not net-new discovery.

---

## 3. Failed Gate 0

| Company | Frame category | Gate-0 failure |
|---|---|---|
| Crypton, Inc. | Upholstered Furniture | G0.1 — **fabric mill**, supplies material, not a furniture brand |
| InsideOut Performance Fabrics | Upholstered Furniture | G0.1 — performance fabric supplier |
| RM COCO + Kasmir Fabrics | Upholstered Furniture | G0.1 — fabric |
| Big House Fabrics | Upholstered Furniture | G0.1 — fabric (runs WizCommerce) |
| Fabricut, Thibaut, Kravet family | Upholstered Furniture | G0.1 — fabric/wallcovering |
| **Furniture First** | Upholstered Furniture | G0.1 — **buying group / member co-op**, not a manufacturer. Nav: "Learn About Membership", "Current Member Login" |
| Clubcu / COHAB.space | Upholstered Furniture | G0.1 — marketplace / shared retail space |
| 313.Space, 220 Elm, 200 Steele, 518 North, Atrium on Main, Centers of High Point, InterHall, Antique and Design Center | both | G0.1 — **buildings, not companies**. 5 auto-detected, more caught by name |
| Asia Minor Carpets, Jaipur Living, Surya, V Rugs & Home, Safavieh, SAMS International | both | Category — rugs, not furniture or lighting |
| B Kelley Antiques, Boxwood Antique Market, Continental Antiques, DelRay & Associates, Half Acre Antiques, Maria's Antiques, Peridot Antiques, Sandy Luther Antiques, Sherwood Antiques, Whitehall Antiques, Golden Oldies | both | G0.1 — antiques/consignment dealers |
| Sadice Marketing Services, Imagine Home Digital, CODARUS | both | G0.1 — services / rep agency |
| Sleepwell/Silentnight, Sealy, Serta, DeRucci, Saatva | Upholstered Furniture | Category — mattresses |
| Ashley Furniture Industries | Lamp & Lighting | G0.4 — far above the size band |
| Williams-Sonoma B2B | Upholstered Furniture | G0.1/G0.4 — retailer, and far above band |
| Stressless (Ekornes) | Upholstered Furniture | G0.4 — global; decision offshore |
| Elizabeth Gray, HKFA, Flocke Lighting, Finesse Decor, International Shades | Lamp & Lighting | **Domain unresolved** — guessed domain returned an unrelated site (an author's blog, a Hong Kong football body, a bare Shopify login). Marked **UNKNOWN**, not disqualified on merit |

---

## 4. Wrong lane — the most useful bucket

These pass Gate 0 and are real prospects, but the lane they surfaced in is wrong. **These are the
field kit's actual triage problem.**

| Company | Surfaced in | Belongs in | Why |
|---|---|---|---|
| Fourteenth Colony Lighting | L3 | L1-shaped | Handcrafted gas/copper lanterns — specification profile, not mid-market |
| St. James Lighting | L3 | L1-shaped | Custom lanterns, sizing guides, made-to-order |
| Continental Home | L3 | neither | Décor-accessory importer that happens to sell lamps |
| Accent Decor, Kalalou, Sagebrook Home, Napa Home & Garden, Emissary, Art Floral Trading | L3 | décor/gift | Accessory houses inside the Lamp & Lighting category |
| Jensen Outdoor | L1 | L2-shaped | Outdoor/teak. On the roster, outdoor is **SEG-02 only** (n=7) `[MEASURED: stamped v4.0 §2.3]` |
| Najarian Furniture | L2 | uncertain | Bedroom/casegoods-led with a visible consumer cart |
| Global Views / Surya | L1 | uncertain | Accessories-led; two brands on one masthead — buying entity unclear |
| **Designmaster Furniture** | L1 | **L1 ∩ L2** | Has *both* "Designer Resources" and a "Dealer Portal" |
| **Home Trends and Design** | L1 | **L1 ∩ L2** | Designer gate *and* "Find A Rep" *and* a store locator |

The last two are the **live test of the lane-1/lane-2 boundary** — the boundary this pass
pre-registered as its most likely failure. Walk them in both lanes.

---

## 5. Competitor platforms detected — qualification signal, not disqualification

Scanning candidate page source for competitor B2B platform signatures `[OBSERVED 2026-08-25]`:

| Platform | Count | Companies |
|---|---:|---|
| **AmpTab** (named direct competitor) | **7** | Steve Silver, Parker House, Delta Furniture Mfg, Albany Industries, La Vida Abode, Bellona USA, **Coast Lamp Mfg** |
| **WizCommerce** (named direct competitor) | 3 | Sagebrook Home, Fireside Lodge, Big House Fabrics |
| NuOrder | 5 | Handy Living, Apricot Sofa, Chesterfield Leather, St. James Lighting, Centers of High Point |
| Shopify (consumer/DTC) | 55 | — weak signal, not carried |
| RepZio · Pepperi · MarketTime · Brandwise · JOOR | **0** | none detected |

**This is the strongest qualification signal produced by the whole pass.** A company running AmpTab
or WizCommerce has already demonstrated all four Gate-0 conditions and a proven willingness to pay
for this exact category. It converts the conversation from greenfield to displacement.

Not a Phase 4 deliverable and not asked for — recorded because it fell out of the observation and
would be wasteful to discard. Worth its own pass.
