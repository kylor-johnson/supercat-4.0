# Legrand — Pricing Review

Auto-generated QA pass on the 6 price columns (`NetPrice`, `Price_retail`, `Price_imap`,
`Price_canet`, `Price_caimap`, `Price_camsrp`) in `products.csv`, cross-checked against
every sheet of all 4 source price workbooks (US Radiant, US adorne, CA Radiant, CA adorne).

**Bottom line: no script bug found.** Every gap below is traced to a specific row (or
absence of a row) in Legrand's own price files. The build script already does the safe
thing — it never invents a price; a gap in the source stays a gap in the output. What
needs a decision is what the **catalog** should do with these SKUs, not the pricing
logic itself.

## 0. File-format note (resolved, no action needed)

The "CSV" price lists in `Source Data/US Price Lists/` and `Canadian Price Lists/` are
actually XLSX files saved with a `.csv` extension (openpyxl confirmed this — they open
fine as XLSX, fail as CSV). The `Source Data/_converted/` folder already has them
correctly renamed to `.xlsx` and byte-identical to the originals. The build script's
loaders (`load_us_radiant_prices`, `load_us_adorne_prices`, `load_ca_radiant_prices`,
`load_ca_adorne_prices`) already read from `_converted/`. Nothing to fix.

## 1. Coverage summary (current build, 1,020 products)

| Column | Populated | Notes |
|---|---|---|
| `NetPrice` (US) | 1,014 / 1,020 | 6 gaps, see §2 |
| `Price_retail` (US MSRP) | — | tracks NetPrice source rows |
| `Price_imap` (US) | 592 / 1,020 | many SKUs legitimately have no US iMAP row |
| `Price_canet` (CA) | 994 / 1,020 | 26 gaps, see §3 |
| `Price_caimap` (CA) | 455 / 1,020 | **0 / 565 on radiant** — entire CA radiant sheet uses literal `"N/A"` in the iMAP column for every row, confirmed by direct inspection. adorne CA iMAP is 455/455 (full coverage). This is a genuine "Legrand doesn't publish CA iMAP for radiant" situation, not a parsing miss. |
| `Price_camsrp` (CA) | 994 / 1,020 | mirrors `Price_canet` gaps |
| `PromotionPrice` | 0 / 1,020 | no promo price list provided |

## 2. The 6 SKUs with no US `NetPrice` (import as `0.00`)

Per `ecat-pricing-levels`: blank and `"0.00"` render identically on the iPad in Net Price
display mode (both show **$0**), so this isn't a display bug — but a real SKU showing
**$0.00** in the US catalog is a live risk (looks free, or lets a rep submit a $0 line).

Checked every sheet of every price workbook (main sheet, Discontinued, MATRIX, Deco
Combo, LSR — everywhere) for all 6 codes:

| Code | Product | Found where | Read |
|---|---|---|---|
| `1597TRUSBAA` | Self-Test GFCI Recep TR 15A USB A/A, Brown | **CA Radiant → Discontinued sheet only** — nowhere in any US sheet | Discontinued in Canada; absent from every US price sheet too. Likely fully EOL — the 1,020-row product file just wasn't pruned to match. |
| `1597TRUSBCCI` | same family, USB C/C, Ivory | CA Radiant → Discontinued only | same as above |
| `1597TRUSBCCLA` | same family, USB C/C, Light Almond | CA Radiant → Discontinued only | same as above |
| `1597TRWRUSBCCW` | same family, WR USB C/C, White | CA Radiant → Discontinued only | same as above |
| `AWP6GBL1` | adorne Pale Blue 6-Gang Wall Plate | **CA adorne → LSR sheet**, real CAD pricing (Net 75.68) | Real, active, priced product — just a Canada-only color. Not a data error; a market-availability question. |
| `R26USBPD65WCC6` | radiant 65W USB PD Outlet, White | **CA Radiant → active/main sheet**, flagged `"NEW"`, real CAD pricing (Net 94.51) | Brand-new SKU. Legrand added Canadian pricing first; US price list hasn't caught up yet. Timing gap on Legrand's side. |

Note: a 5th CA-Discontinued sibling, `1597TRWRUSBCCBK` (WR USB C/C, Black), **does** have
a real US price (`$48.19` net, found in US Radiant) — it's discontinued in Canada only,
still active in the US. Listed in §3, not here.

**Ask Legrand:** (a) confirm the 4 `1597TR...` GFCI/USB variants are fully discontinued
and should be dropped from the product file entirely (rather than shipped at $0); (b) for
`AWP6GBL1`, confirm Pale Blue is Canada-only and not meant to be orderable by US reps —
if so this SKU may need to be excluded from the US-visible catalog or price level, not
just left at $0; (c) request the updated US radiant price list once `R26USBPD65WCC6` is
added.

## 3. The 26 SKUs with no CA `Price_canet` / `Price_camsrp`

Same method — checked every sheet of both CA workbooks. All 26 fall cleanly into three
explained buckets:

**A. Explicitly on Legrand's CA "Discontinued" sheet (6 SKUs)** — real rows exist, just
flagged discontinued-in-Canada:

`1597TRUSBAA`, `1597TRUSBCCI`, `1597TRUSBCCLA`, `1597TRWRUSBCCBK`, `1597TRWRUSBCCW`,
`R26USBCCNICCV4`

**B. AFCI/GFCI combo devices — never appear in any CA sheet at all (10 SKUs)** — active
US products (full pricing in US Radiant), but genuinely absent from the Canadian
Radiant workbook (not even on the Discontinued sheet — just never listed):

`AFGF152TR`, `AFGF152TRBK`, `AFGF152TRI`, `AFGF152TRLA`, `AFGF152TRW`, `AFGF202TR`,
`AFGF202TRBK`, `AFGF202TRGRY`, `AFGF202TRI`, `AFGF202TRLA`

Likely explanation: AFCI/GFCI self-test combo devices may be a US-only regulatory/code
product (Canadian electrical code often specifies different combo-device requirements).
**Needs a direct question to Legrand** — not something inferable from the files.

**C. "with Microban®" (WAM) / screwless-plate (CC6) SKUs — never appear in any CA sheet
(10 SKUs)** — same pattern as bucket B, active in the US only:

`TM873WAMCC4`, `TM870WAMCC4`, `RWP264WAMCC6`, `RWP263WAMCC6`, `RWP262WAMCC6`,
`RWP26WAMCC6`, `RH703PTUWAMCC4`, `RHCL453PWAMCC4`, `R26USBPDCC6`, `R26USBPDWCC6`

Likely explanation: the Microban antimicrobial treatment line may not be sold/certified
in Canada. Same ask as bucket B.

**Ask Legrand:** confirm buckets B and C are intentionally US-only product lines (not
sold in Canada) — if so, no fix needed, this is expected and can be noted in the client
checklist as "by design." If Canadian pricing should exist and is simply missing from
the file we were given, request the corrected CA price list.

## 4. What the build already does right (no change made)

- `Price_canet`/`Price_caimap`/`Price_camsrp` are left **blank** when no source price
  exists — never fabricated, never defaulted to a fake number.
- `NetPrice` (US) is the one column that falls back to `"0.00"` rather than blank. Per
  `ecat-pricing-levels`, blank reads as $0 anyway in Net display mode, so this is
  cosmetically identical — flagged here only because the underlying data gap deserves a
  business decision (§2), not because the fallback itself is wrong.
- Pricing always prefers the dedicated price-list workbook over the main product file's
  embedded price columns (`Dist NET 1`, `Canadian NET`, etc.) and only falls back to the
  main file when the price-list workbook has no row for that SKU — so no double-sourcing
  or silent overwrite risk.

## 5. Questions for the client meeting (roll into checklist §B)

1. Drop the 4 fully-EOL `1597TR...` GFCI/USB codes from the product file, or keep them
   at $0 net intentionally?
2. Is `AWP6GBL1` (Pale Blue wall plate) Canada-only? If so, restrict it from the
   US-visible catalog/price level rather than shipping at $0 US net.
3. Request updated US radiant pricing that includes `R26USBPD65WCC6` (new SKU, CA-only
   so far).
4. Confirm AFCI/GFCI combo devices (10 SKUs) and Microban/screwless-plate SKUs (10 SKUs)
   are intentionally US-only lines not sold in Canada.
5. Confirm CA radiant iMAP is genuinely not published (every radiant row in the CA file
   uses `"N/A"` for iMAP) — if so, hide the iMAP price level for Canadian radiant reps
   rather than showing a $0/blank field.
