# Dorell Fabrics (`drf`) — Onboarding → Go-Live Handoff

**Date:** 2026-07-21  
**Audience:** Support / go-live (Kyla primary; Jon for rep training)  
**From:** Onboarding (Kylor)  
**Admin:** https://supercatsolutions.com/DRF  
**Working files:** `SuperCat_Simple_Final/02_Implementation/Dorell/`

---

## Context

Dorell is a fabric/textile manufacturer (showroom + market/Showtime). Catalog onboarding is **effectively complete**: ~1,627 active SKUs with images, 10 ad-hoc price levels loaded, multi-price reference via Product Stories, 389 customers with territories, user groups in place, and the team already placing sample iPad orders.

Kyla declared onboarding complete in Help Scout **#14799** (2026-07-20) and scheduled **Admin Training** with Christine (lead) / Suzanne (backup) for **2026-07-21 11:30–12:30 PST**. Remaining work is go-live hygiene: confirm email owners, run trainings, optionally invite field reps with territory-scoped access, and long-tail images/pricing maintenance.

Org `properties.status` is still **`onboarding`** — flip when Support is ready to call them live.

---

## Contacts

| Role | Person | Email |
|------|--------|-------|
| Ops / IT (Admin lead) | Christine Soh | christine.soh@dorellfabrics.com |
| Project Manager (backup) | Suzanne Fukunaga | Suzanne@dorellfabrics.com |
| TX / Brian | Brian Frankel | brian@loomcraft.com |
| Other iPad users | Gina Garza, Heather Steczko, Kate Gothreau | *@dorellfabrics.com |
| SuperCat Support | Kyla Bosch | kyla@supercatsolutions.com |
| SuperCat Rep training | Jon Vanderberg | jon@supercatsolutions.com |

Domain for Help Scout: `dorellfabrics.com`

---

## Live instance snapshot (Postgres `drf` / org_id **290**, audited 2026-07-21)

| Area | Live state |
|------|------------|
| Products | **1,627** active (39,402 deleted historical) |
| Images | **1,564** with images / **63** without |
| Stories | **1,512** non-null; **1,418** include embedded `List:` price text |
| Price levels | 11 ad-hoc: `list`, `mfr`, `whs`, `foblist`, `foblow`, `c2clist`/`c2clow` (CNY), `calist`/`calow` (CAD), `retail`, `net` |
| `prices_json` | Populated on all active products (sample ADELINA-UV-ASH has full 10-level JSON) |
| NetPrice | **$1.00 on every SKU** (placeholder — not real cost) |
| Customers | **389**, all `DefaultPriceCode = net` |
| Inventory | **0** (by design — sample/show use, not stock) |
| Options | **0** |
| Orders | **7** iPad orders (mostly $0 sample / Confirmed; latest 2026-07-14) |
| SmartLists | `Spring 2026 Rotation`, `Dorell Studio` (both published) |
| PDF formats | Org Tearsheet, 3×3, One Per Page (user groups auth = all) |
| Org emails | Order + company → **Suzanne@… (temporary)**; error notify → Christine + Suzanne |
| Org status flag | `onboarding` |

### User groups

| Group | Members (notable) | Customer sync | Price / PDF / SmartList auth |
|-------|-------------------|---------------|------------------------------|
| **Dorell Internal** | Christine, Suzanne, Gina, Heather, Kate, Brian | **Own / associated** (`o`) — territory-filtered | All (`a`) |
| **SuperCat Team** | Kyla, Jon, Kylor | **All** (`a`) | All (`a`) |

All current Dorell users carry territory codes: `2,7,40,53,62,65,98,103,500` (full book). Heather previously had none; that was fixed in the Jul 17 Admin pass.

### Recent clean imports

- Products: **2026-07-06** clean  
- Product Stories: **2026-07-08** (×3) clean  
- Images: ongoing through Jul 6 (incl. many `*-WF-Assorted.jpg`)

---

## Help Scout thread map (Suzanne + Christine)

| # | Subject | Status | What it closed / left open |
|---|---------|--------|----------------------------|
| **14401** | Initial Product & Customer Imports | closed | First 80-SKU subset + 389 customers; territory mapping explained (53 Chip, 62 Andy, 40 House, 65 Claudia, 2 Brian, 7 Danny, 98 Sample Yardage, 500 Retail, 103 Closeouts) |
| **14438** | Product File Progress | closed | Family/colorway model, waterfalls, RelatedItems, specs; inventory out of scope |
| **14638** / **14707** | Check-In & Next Steps / Pricing | closed | 10 price levels designed + loaded; multi-price on detail page via **stories workaround** (not native multi-level UI); `build_stories_with_pricing.py` handed to client |
| **14798** | Onboarding Check-In + Support Intro (Kylor) | pending | Admin cleanup + **email confirmation ask** (client never answered this part) |
| **14799** | Re: … Support Intro (Kyla) | **pending** | Kyla owns; Admin training booked Jul 21 11:30 PST; still need email confirmations + Jon rep training |

---

## How they use eCat (support must know)

1. **Primary use:** presentation / internal price reference at shows; sample orders free of charge.  
2. **Multi-price on detail page:** Product Story = marketing copy + static price lines (U+2028 line separators). Regenerated from `products.csv` via `build_stories_with_pricing.py`. **Not** live-linked to price levels — re-run script when prices change.  
3. **Customer selected → Net ($1):** every customer defaults to `net`. Browsing uploaded List/WHS/FOB/etc. requires Settings → Price Level, or no customer selected.  
4. **No inventory** — do not treat empty inventory as a defect.  
5. **Taxonomy:** TradeName `DOR`; Collections = fabric family; Categories = subclass (Chenille, Texture, Waterfall, Sample 18×54, etc.); Group `Fabric` created manually.  
6. **Row types:** base colorway, Waterfall (`WF-ASSORTED` / occasional `WF-ASST`), Sample Book (`SB-ASSORTED`), 18×54 samples. `-A-` in SKU is grade/variant, not color. `-C0-` is a separate coated SKU.

---

## Go-live checklist (what Support owns next)

```
[x] Catalog imported (products + stories + images majority)
[x] 10 price levels created + prices_json loaded
[x] Multi-price detail display (stories workaround)
[x] customers.csv live (389; DefaultPriceCode=net)
[x] User groups (not stuck in DefaultUserGroup)
[x] PDF formats (≥3) authorized (auth=all)
[x] SmartLists live + authorized (auth=all)
[x] Sample iPad orders already flowing
[ ] Confirm order email recipient (Suzanne is TEMP — ask shared inbox?)
[ ] Confirm company email / presentation email subject
[ ] Admin training (Kyla + Christine) — scheduled 2026-07-21 11:30 PST
[ ] Rep / iPad training (Jon)
[ ] Decide: invite field reps with single territory codes vs keep internal-only full-book users
[ ] Optional: map Net to a real transactional price (or leave $1 if samples stay $0)
[ ] Image long-tail (63 SKUs) — mostly WF/SB assorted + some colorways (Echelon, Hamlet, Mandara, Tempest, Veloura)
[ ] Flip org status off `onboarding` when Support signs off
```

---

## Open client confirmations (from #14798 / #14799 — still unanswered)

| Setting | Live now | Need from Christine/Suzanne |
|---------|----------|-----------------------------|
| Order email recipient | Suzanne@… (temp) | Real ops inbox or keep Suzanne |
| Backup order email | blank | Optional CC |
| Company email | Suzanne@… (temp) | Branding address on docs |
| Product / presentation email subject | blank | Suggested: `Product information from %repFirstName% %repLastName%` |
| Import error notify | Christine + Suzanne | Confirm OK |
| Enrollment notify | Suzanne + Christine | Confirm or clear |

---

## Source of truth & maintenance

| Artifact | Path / note |
|----------|-------------|
| Working folder | `SuperCat_Simple_Final/02_Implementation/Dorell/` |
| products.csv | Jul 8 local; **1,627** rows; Price_* columns present |
| stories.csv | Built by script; last live import Jul 8 |
| Base descriptions | `stories.csv.20260703-0215.csv` |
| Rebuild script | `build_stories_with_pricing.py` (uses U+2028 line separators — required) |
| customers.csv | Apr 27 vintage; **389** rows; `DefaultPriceCode=NET` — matches live |
| Live truth | Postgres + `import_events` — prefer over local CSVs if client re-imported |

**When prices change:** update `products.csv` → run script → re-import products **and** stories.

---

## Known gaps / gotchas (do not re-litigate unless asked)

1. **CLIENT_PROFILE.md was stale** (said “no pricing,” ~87 images, maintenance). Corrected alongside this handoff.  
2. **~63 missing images** — mix of intentional `-` ImageFileName (WF/SB) and real gaps (e.g. ECHELON-*, HAMLET-*, MANDARA-*, TEMPEST-*, VELOURA-CASHMERE). Some WF assets were imported as `*-WF-Assorted.jpg` while SKUs still show no image — filename/`ImageFileName` mismatch possible (`WF-ASST` vs `WF-ASSORTED`).  
3. **~209 products** still have $0 on main USD price columns in the local file (Christine: “not costed yet”); stories omit zero lines by design.  
4. **20 BaseItemCodes > 20 chars** — advisory only; importer accepts.  
5. **SmartList price selectivity** (Christine Jul 1): answered via per–user-group price-level auth. Today both groups authorize **all** levels — if they share SmartLists externally and want fewer prices visible, restrict `price_levels_auth` on a future “external/share” group.  
6. Early customer import (Apr 27) had `DefaultPriceCode=net` errors before `net` price level existed; later import succeeded — do not re-debug unless customers vanish.

---

## Suggested next actions (Support)

1. Run Admin training; capture email-owner answers in #14799.  
2. Update org order/company email from temp Suzanne if they name a shared inbox.  
3. Schedule Jon’s rep/iPad training.  
4. Ask whether field sales (Chip/Andy/etc.) need invites with **single** territory codes; current users are internal with full book.  
5. Leave inventory empty unless they reverse the sample-only decision.  
6. Image long-tail = maintenance, not a go-live blocker.

---

## Handoff prompt (paste into a new chat)

```
Resume Dorell Fabrics (drf, org_id 290). Onboarding → go-live handoff is in
SuperCat_Simple_Final/02_Implementation/Dorell/HANDOFF.md.

Catalog live: 1627 products, 1564 images, stories with embedded multi-price,
389 customers (DefaultPriceCode=net), NetPrice=$1 placeholder, no inventory.
User groups: Dorell Internal + SuperCat Team. Kyla owns Support; Admin training
was scheduled 2026-07-21 11:30 PST with Christine. Still need: confirm order/
company emails (Suzanne is temp), Jon rep training, optional field-rep invites.
Help Scout: #14799 (pending). Do not invent inventory. Prefer live DB over
stale CLIENT_PROFILE notes.
```
