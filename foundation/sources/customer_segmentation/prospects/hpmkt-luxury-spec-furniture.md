---
id: PROS-L1
title: Lane 1 — Luxury Spec × Furniture — ranked candidates
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
lane: L1
anchor: Interlude Home (ih/ihw — existing customer, reference vector only, not a candidate)
frame: HPMKT Exhibitor Directory, Upholstered Furniture category, harvested 2026-08-25
depends_on: [PROS-CRIT, TAX-B]
---

# Lane 1 — Luxury Spec × Furniture

All observations `[OBSERVED]` 2026-08-25 from each company's own website plus the HPMKT exhibitor
directory. Building/space from `highpointmarket.org/ExhibitorDirectory`. Nothing invented; UNKNOWN
where not verified.

**Read the caveat before the predictions.** Every `PREDICTED SEG-0n` below is a prediction, not an
assigned segment. Pre-sale prediction accuracy: binary feature extraction **33.3% vs a 34.5%
majority baseline (n=87)**; holistic reading ~53% vs a 30% baseline. The Layer A rule itself
reproduces stamped labels only **38.5% vs a 34.9% majority baseline (n=109)**. **No prospect
carries a bare segment label.**

---

## Ranked candidates

Criteria: **1.1** furniture primary · **1.2** designer-facing account gate · **1.3** no consumer
price/cart · **1.4** project/contract vocabulary · **1.5** HPMKT permanent showroom.

| # | Company | Domain | HPMKT building / space | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 | Conf | ARCH | Predicted |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Mr. Brown London** | mrbrownlondon.com | 114–116 E. Martin Luther King Jr. Dr. (Hamilton Wrenn) | ✅ | ✅ | ✅ | ⬜ | ✅ | **HIGH** | ARCH-01 | PREDICTED SEG-01 |
| 2 | **Designmaster Furniture** | designmasterfurniture.com | 201 S. Main St. (Downtown Main) | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-01 | PREDICTED SEG-01 |
| 3 | **Phillips Scott** | phillipsscott.com | 200 Steele – 123, Floor 1 (Hamilton Wrenn) | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-01 | PREDICTED SEG-01 |
| 4 | **Home Trends and Design (HTD)** | hometrendsanddesign.com | 118 N. Wrenn St. (Commerce Concourse) | ✅ | ✅ | ✅ | ⬜ | ✅ | **HIGH** | ARCH-01 | PREDICTED SEG-01 |
| 5 | **JDouglas** | jdouglas.com | IHFC – IH408, Design Center, Floor 1 (InterHall) | ✅ | ✅ | ✅ | ⬜ | ✅ | MEDIUM | ARCH-01 | PREDICTED SEG-01 |
| 6 | **Global Views** | globalviews.com | IHFC – D213, D220, Design Center, Floor 2 | ⚠️ | ✅ | ✅ | ⬜ | ✅ | MEDIUM | ARCH-01 | PREDICTED SEG-01 |
| 7 | **Jensen Outdoor** | jensenoutdoor.com | IHFC – IH308, Commerce, Floor 1 (InterHall) | ⚠️ | ✅ | ✅ | ✅ | ✅ | MEDIUM | ARCH-01 | PREDICTED SEG-01 |
| 8 | **Surya** | surya.com | Showplace – 4100, Floor 4 | ⚠️ | ✅ | ✅ | ⬜ | ✅ | LOW | ARCH-01 | PREDICTED SEG-01 |

✅ met · ⬜ not met · ⚠️ partial/questionable · UNKNOWN where stated

### What was observed, per candidate

**1. Mr. Brown London** — `https://mrbrownlondon.com`
Nav reads `sign in | create trade account | Shop by Product | Furniture | Bar and Counter Stools |
Benches and Daybeds | Beds & Daybeds | Bookshelves | Cabinets | Chests & Bedsides | Desks | Dining
Chairs`. Explicit **"create trade account"** gate; no price or cart anywhere on public pages; COM
language present. Furniture-led assortment.
**Strongest disqualifying risk:** small/boutique — G0.4 size band unverified; may be below the band.
**HubSpot:** not found — genuinely fresh.

**2. Designmaster Furniture** — `https://designmasterfurniture.com`
Nav reads `Product | Residential | Hospitality | Quick Ship | Designer Resources | Coverings |
Finishes & Options | Construction & Care | Warranty | Dealer Portal | Log In`. Carries **both**
"Designer Resources" and a "Dealer Portal", plus an explicit **Hospitality** division — the clearest
lane-1 profile in the set. No public pricing.
**Strongest disqualifying risk:** the dealer portal suggests it may straddle lane 1 and lane 2.
**HubSpot:** not found — fresh.

**3. Phillips Scott** — `https://phillipsscott.com`
Nav: `Sign in | Living | Accent Chairs | Bars + Stools | Chests + Dressers | Cocktail Tables |
Consoles + Desks | Decor | Lighting | Mirrors | Occasional Tables | Ottomans + Benches | Tall
Cabinets | European Flooring | Dining`. Sign-in gated, no public prices, contract vocabulary present.
**Strongest disqualifying risk:** assortment includes décor/mirrors/lighting — may read as
accessories-led rather than furniture-led on the floor.
**HubSpot:** `lifecyclestage: lead` since 2025-09-24 — **already known, not a fresh prospect.**

**4. Home Trends and Design (HTD)** — `https://hometrendsanddesign.com`
Nav: `Dealer Login | Register | Store locator | Find A Rep | Product Catalog | About HTD | High
Point Showroom | Austin Showroom | LookBook`. **The only lane-1 candidate publishing a rep network**
("Find A Rep") alongside a dealer login and a store locator — a genuinely mixed channel profile.
**Strongest disqualifying risk:** the store locator + dealer login combination points at lane 2.
**HubSpot:** not found — fresh.

**5. JDouglas** — `https://jdouglas.com`
Nav: `FURNITURE | SEATING | LIGHTING | RUGS | BEDDING | BATH | ACCESSORIES | WALL DECOR`. Trade
gated, no public prices.
**Strongest disqualifying risk:** very broad assortment across eight categories — reads closer to a
multi-category décor house than a furniture specification brand.
**HubSpot:** **1 open deal**, lifecycle `1103273401`. **Existing opportunity — not a fresh prospect.**

**6. Global Views** — `https://globalviews.com`
Nav: `Surya | Global Views | Open a Trade Account | Sign In | New | Accessories | Furniture |
Lighting | Wall Decor | Textiles | Studio A Home | GV Design | Contract`. Explicit **"Open a Trade
Account"**, no public prices, a Contract line.
**Strongest disqualifying risk:** the nav shows **Surya and Global Views on one masthead** — likely
a parent/sibling brand family, so the buying entity may not be the exhibitor. Accessories-led.
**HubSpot:** `lead` since 2025-07-10 — already known.

**7. Jensen Outdoor** — `https://jensenoutdoor.com`
Nav: `Furniture | Our Story | How to Buy | Help Center | Find a Retailer | CARE PRODUCTS | View The
Catalog`. Trade gated, contract language, COM.
**Strongest disqualifying risk:** **outdoor/teak specialist** — on the roster, outdoor sits almost
entirely in SEG-02, not SEG-01 `[MEASURED: stamped v4.0 §2.3, outdoor n=7, "Brand-Building only"]`.
**HubSpot:** **2 open deals.** **Existing opportunity — not a fresh prospect.**

**8. Surya** — `https://surya.com`
Nav: `Open a Trade Account | Sign In | Rugs | Furniture | Lighting | Textiles | Wall Decor | Accents
| Outdoor`. Trade gated, no public prices.
**Strongest disqualifying risk:** **rugs-led, and large.** Rugs sit in SEG-04 on the roster (n=1,
Kaleen). Likely above the G0.4 size band. Shares a masthead with Global Views.
**HubSpot:** not checked in this pass — UNKNOWN.

---

## Honest read on this lane

**Only 3 of 8 are fresh prospects.** Phillips Scott, Global Views (leads), JDouglas and Jensen
Outdoor (open deals) are already in HubSpot. Mr. Brown London, Designmaster and HTD are the genuinely
new names, and Designmaster is the strongest match to the Interlude Home profile.

**Category over-selected exactly as predicted.** The Upholstered Furniture frame returned fabric
mills (Crypton, InsideOut Performance Fabrics), rug houses (Jaipur Living, Asia Minor, Surya) and a
co-working space (Clubcu / COHAB.space) at the top of the trade-gate ranking, because a trade gate is
common to all of them. Those are Gate-0 or category failures, listed in
[`disqualified.md`](disqualified.md). **Criteria were not tightened to fix this** — recorded for
Phase 5 to measure.

**NEEDS-FIELD-VERIFICATION for every row:** G0.4 size band, showroom tenure, and whether the
assortment reads furniture-led or accessories-led on the floor. Those are walk-list questions.
