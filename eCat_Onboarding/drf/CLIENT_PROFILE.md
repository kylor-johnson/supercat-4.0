# Dorell — eCat Client Profile

> Reconciled against live Postgres (`drf` / org_id 290) + Help Scout on 2026-07-21.
> Prefer live DB + `import_events` over this file if they diverge.

## Identity
- **Org shortname:** `drf`
- **Admin Console:** supercatsolutions.com/DRF
- **TradeNameCode:** `DOR` (single tradename)
- **Vertical:** fabric / textiles (showroom, market / Showtime)
- **Status / stage:** **go-live / training** — catalog complete; Support (Kyla) owns Admin + rep training. Org flag still `onboarding`.

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** `inventory: n/a`, `options: none`, `sample-catalog`
- **File owner mode:** mixed
- **Image mode:** ftp
- **Source cutover date:** unknown
- **Sub-brands:** none

- **`inventory: n/a` and `options: none` are confirmed both ways:** the 2026-04-29 call
  (*"The app will not include pricing or inventory data"*) and live state — 0 inventory
  rows, 0 options, 0 option groups.
- **`pricing: n/a` is deliberately NOT set**, though `IMPLEMENTATION_PLAN.md` 2.4 lists it
  for this client. The April call is superseded: the org has **11 live price levels**, and
  this profile (reconciled 2026-07-21) documents 10 imported levels plus `net` and
  `Price_<Code>` columns in the products file. Skipping the pricing gates here would hide
  real defects. Flag the plan, not the client.
- **File owner is mixed by deliverable, never by file:** `stories.csv` is generator-owned
  (`build_stories_with_pricing.py`); `products.csv` is CSV-owned. Neither has two owners.
- **Cutover date is open** (Open Decision 4) — until it is set, treat any pre-2026 row
  count as possibly containing POC residue.

## Contacts
- **Client:** Suzanne Fukunaga (PM), Christine Soh (Ops/IT — Admin lead), Brian Frankel (TX / loomcraft), Gina / Heather / Kate (iPad users)
- **SuperCat:** Kyla Bosch (Support primary), Jon Vanderberg (rep training), Kylor Johnson (onboarding — handed off)

## Taxonomy decisions
- **Method:** Standard with **readable labels** (never ship `COL#`/`TN1` codes)
- **Collections →** fabric Family (e.g. `Adelina-UV`, `Anaya-UV`)
- **Categories →** product sub-class (`Chenille`, `Texture`, `Waterfall`, `Sample 18 X 54`, …)
- **Group:** single `Fabric` group (created manually — groups don't auto-create)
- **Custom fields:** Origin, Content, Cleaning, Direction, Abrasion, Backing, Finishing, ColorFamily, Class, SubClass, ProductOrderCode, ProductOrderColorCode, …

## Pricing / inventory
- **10 ad-hoc imported levels** (+ `net`): List, MFR, WHS, FOBList, FOBLow, C2CList/C2CLow (CNY), CAList/CALow (CAD), Retail
- Columns in products file: `Price_<Code>` (e.g. `Price_List`)
- **NetPrice = $1 placeholder** on all SKUs; all customers `DefaultPriceCode = net`
- **Multi-price on detail page** = Product Story text (not native multi-level UI) — regenerate via `build_stories_with_pricing.py`
- **No inventory** (by design — sample / show selling)

## Images
- FTP `/images` **flat root only**
- Live coverage ~**1,564 / 1,627**; **63** still without images (mostly WF/SB assorted + some colorways)
- Case-sensitive exact match to `ImageFileName`

## Snowflake quirks
- Row types: base color, Waterfall (`WF-ASSORTED` / sometimes `WF-ASST`), Sample Book (`SB-ASSORTED`), 18×54 sample
- `-A-` segment = product variant/grade (NOT a color)
- `-C0-` = separate catalog SKU (coating), not an option
- BaseItemCode from `ProductOrderCode-ProductOrderColorCode`; 20-char limit advisory only
- RelatedItems by family; WF/18×54 link to base colors
- SmartLists: **Spring 2026 Rotation**, **Dorell Studio**

## Files & paths
- **Working folder:** `SuperCat_Simple_Final/02_Implementation/Dorell/`
- **Handoff:** `HANDOFF.md` (onboarding → go-live)
- A **new source file the client sends is the source of truth**; prior files are reference
- Stories rebuild: `build_stories_with_pricing.py` + base `stories.csv.20260703-0215.csv`

## Scale (live 2026-07-21)
- **1,627** active products; **~115** collections; **1,564** with images; **389** customers; **0** inventory

## Open items
- [ ] Confirm order / company email (Suzanne currently temporary)
- [ ] Admin training (Kyla) + rep training (Jon)
- [ ] Field-rep invites with territory-scoped codes (if/when)
- [ ] Image long-tail (63)
- [ ] Re-run stories script when newly costed items get prices
- [ ] Flip org status from `onboarding` when Support signs off
