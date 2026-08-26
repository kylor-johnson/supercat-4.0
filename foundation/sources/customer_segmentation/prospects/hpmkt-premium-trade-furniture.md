---
id: PROS-L2
title: Lane 2 — Premium Trade × Furniture — ranked candidates
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
lane: L2
anchor: Braxton Culler (bcf — existing customer, reference vector only, not a candidate)
frame: HPMKT Exhibitor Directory, Upholstered Furniture category, harvested 2026-08-25
depends_on: [PROS-CRIT, TAX-B]
---

# Lane 2 — Premium Trade × Furniture

Dealer seating and casual. **Not décor accessories.**

All observations `[OBSERVED]` 2026-08-25. Same prediction caveat as lane 1: every `PREDICTED SEG-0n`
is a prediction — binary extraction 33.3% vs a 34.5% majority baseline (n=87); Layer A's own rule
38.5% vs 34.9% (n=109). **No prospect carries a bare segment label.**

---

## Ranked candidates

Criteria: **2.1** seating/casual core · **2.2** not a décor-accessory house (hard exclude) ·
**2.3** dealer recruitment/access · **2.5** named collection structure · **2.6** HPMKT presence.
*(2.4 dealer locator is supporting evidence only — demoted, n=6 cohort.)*

| # | Company | Domain | HPMKT building / space | 2.1 | 2.2 | 2.3 | 2.5 | 2.6 | Conf | ARCH | Predicted |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Lancer Furniture** | lancerfurniture.com | 220 Elm – 218, Level 2 | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-02 | PREDICTED SEG-02 |
| 2 | **Parker House Furniture** | parkerhousefurniture.com | 309 S. Elm St. (Russell & Green) | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-02 | PREDICTED SEG-02 |
| 3 | **Steve Silver Company** | stevesilver.com | Plaza Suites – C-100, Club Level | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-02 | PREDICTED SEG-02 |
| 4 | **Green Gables Furniture** | greengablesfurniture.com | 310 N. Hamilton St. – S-307, Floor 3 | ✅ | ✅ | ✅ | ✅ | ✅ | **HIGH** | ARCH-02 | PREDICTED SEG-02 |
| 5 | **Sofamaster** | sofamaster.com | Centers of High Point: Centennial – 108, Floor 1 | ✅ | ✅ | ⚠️ | ⬜ | ✅ | MEDIUM | ARCH-02 | PREDICTED SEG-02 |
| 6 | **Jackson Furniture / Catnapper** | jacksonfurniture.com | Plaza Suites – 300, Floor 3 | ✅ | ✅ | ⬜ | ✅ | ✅ | MEDIUM | ARCH-02 | PREDICTED SEG-02 |
| 7 | **England Furniture** | englandfurniture.com | Plaza Suites – 100, Floor 1 | ✅ | ✅ | ⬜ | ✅ | ✅ | MEDIUM | ARCH-02 | PREDICTED SEG-02 |
| 8 | **Najarian Furniture** | najarianfurniture.com | 113 W. Green Dr. (Russell & Green) | ⚠️ | ✅ | ⬜ | ✅ | ✅ | LOW | ARCH-02 | PREDICTED SEG-02 |
| 9 | **IMG Comfort** | imgcomfort.com | 220 Elm – 206, Level 2 | ✅ | ✅ | ⬜ | ✅ | ✅ | LOW | ARCH-02 | PREDICTED SEG-02 |

### What was observed, per candidate

**1. Lancer Furniture** — `https://lancerfurniture.com` · **strongest match in the lane**
Nav: `Accent Chairs | Built for me | Fabrics | Homespun Collection | Leather | Ottomans | Recliners |
Sectionals | Suites | Find A Dealer | Dealer Login | Custom Options | Construction | Contract`.
**Both "Find A Dealer" and "Dealer Login"**, seating-dominant assortment, named collections
(Homespun), custom options. This is the closest structural analogue to Braxton Culler in the set.
**Risk:** possibly below the G0.4 size band. **HubSpot:** `lead` since 2025-11-18 — already known.

**2. Parker House Furniture** — `https://parkerhousefurniture.com`
Nav: `Living Room | Occasional Tables | Entertainment | TV Consoles | Entertainment Walls | Accents |
Upholstery | Stationary | Sofa Groups | Accent Chairs | Ottomans`. Dealer portal present, COM
language, no public prices, deep motion/upholstery line.
**Risk:** entertainment/TV console weighting reads more mass-market than premium trade.
**Runs AmpTab** `[OBSERVED: "amptab" in page source]`. **HubSpot:** not found — **fresh.**

**3. Steve Silver Company** — `https://stevesilver.com`
Nav: `CURRENT CATALOG | FLIP CATALOG | VIRTUAL SHOWROOM | DEALER LOGIN | DINING & KITCHEN | DINING
SETS | BAR & COUNTER STOOLS | MIX & MATCH SEATING`. Dealer login, downloadable/flip catalog, virtual
showroom, seating and dining core.
**Risk:** dining-led rather than upholstery-led; volume/promotional positioning possible.
**Runs AmpTab** `[OBSERVED]`. **HubSpot:** `salesqualifiedlead` — **already SQL, not fresh.**

**4. Green Gables Furniture** — `https://greengablesfurniture.com`
Nav: `Dealer Access | YELLOWSTONE COLLECTION | LIVING | DINING | BEDROOM | BATH | OFFICE |
ENTERTAINMENT | UPHOLSTERY | FABRICS LEATHERS HIDES | SILVERTON COLLECTION | STEELBOUND COLLECTION`.
Dealer-gated, strongly named-collection structured, rustic/lodge positioning.
**Risk:** licensed-collection model (Yellowstone) may mean a different commercial structure.
**HubSpot:** `lead` since 2025-09-04 — already known.

**5. Sofamaster** — `https://sofamaster.com`
Nav: `Products | Craftsmanship | Order Swatches | Find a Retailer | Become a Partner | See Full
Product Line`. "Become a Partner" is dealer recruitment in different words. US/MX phone numbers.
**Risk:** contract-manufacturer profile — may build for others rather than own a brand (G0.1).
**HubSpot:** `lead` — already known.

**6. Jackson Furniture / Catnapper** — `https://jacksonfurniture.com`
Nav: `Find A Retailer | Sofas | Reclining Sofas | Recliners | Sectionals | Lift Chairs | Sleepers |
Accent Chairs | Cocktail Ottomans | Catalog | Login`. Textbook dealer motion-furniture profile.
**Risk:** promotional motion furniture may sit closer to SEG-03/SEG-04 than premium trade.
**HubSpot:** `lead` — already known.

**7. England Furniture** — `https://englandfurniture.com`
Nav: `Sofas | Loveseats | Sectionals | Sleepers | Chairs | Ottomans | Del Mar | EZ Motion | Leather |
Simplicity | Find a Store`. Named programs (Del Mar, EZ Motion, Simplicity), consumer store locator.
**Risk:** **La-Z-Boy subsidiary** — likely a rollup child, so the buying decision may not sit here.
**HubSpot:** `salesqualifiedlead` — **already SQL, not fresh.**

**8. Najarian Furniture** — `https://najarianfurniture.com`
Nav: `View cart () | Login | All Bedroom | Dressers & Mirrors | Nightstands | Chests | Beds | All
Dining Room | All Occasional`. **A cart is present** — weakens the lane-2 read.
**Risk:** bedroom/casegoods-led, not seating; visible cart. **HubSpot:** `lead` — already known.

**9. IMG Comfort** — `https://imgcomfort.com`
Nav: `Collections | Relaxer | Luna Chair | Power Recliners | Reclining Sofas | Scandinavian
Recliners | Covers | Find a retailer`. Recliner specialist, collection-structured.
**Risk:** Norwegian parent (Ekornes family) — international, likely outside the G0.4 band and
decided offshore. **HubSpot:** `lead` — already known.

---

## Honest read on this lane

**Only 1 of 9 is a fresh prospect** — Parker House Furniture. Everything else is already in HubSpot
as a lead or SQL. This lane is the most heavily worked already.

**Three lane-2 candidates run AmpTab** — Steve Silver, Parker House, and (in the wider pool) Albany
Industries, Delta Furniture Mfg and La Vida Abode. AmpTab is a named direct competitor
`[OBSERVED: foundation/04_market_and_competitors.md]`. That is a *positive* qualification signal —
they have already bought this software category — and a competitive-displacement motion rather than
a greenfield one. See [`disqualified.md`](disqualified.md) §4 for the full competitor-platform list.

**Lane 2's criteria remain the weakest**, as pre-registered: the cohort behind them is n=6, criterion
2.4 was demoted to supporting evidence, and the lane-1/lane-2 boundary is separated only by
vocabulary (designer vs dealer). Designmaster Furniture appears in lane 1 but carries a Dealer
Portal; HTD appears in lane 1 but publishes a rep network and store locator. **Those two are the
live test of the boundary** and should be walked in both lanes at market.
