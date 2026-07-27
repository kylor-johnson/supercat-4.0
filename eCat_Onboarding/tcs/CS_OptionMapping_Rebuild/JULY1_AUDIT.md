# CopperSmith (tcs) — July 1 Catalog Audit

Generated after Eric's FTP push (~3:00 PM MDT). Live DB is source of truth for what's on iPad.

## Executive summary

| Issue | Scope | Severity |
|-------|-------|----------|
| GT36W still on generic mount codes (WY, CML, QCM, PF36) | 1 product | **Critical** — up to $380/order revenue leak |
| Option display names don't match Accessory Index | GT36 size-specific codes + others | **High** — rep confusion, wrong labels on orders |
| Story text bullets run together (no line breaks) | **379 of 396** products | **High** — all collections look broken |
| Eric's July 1 files not in Kylor's local rebuild folder | options/groups | Process gap — local CSVs are stale |

## GT36 family — live vs expected

| Product | Wall (OS2) | Ceiling (OS3) | Post/Pier (OS4) | Decorative (OS6) | Status |
|---------|------------|-----------------|-----------------|------------------|--------|
| GT36E | WM059 (WY36) | CM166 (QCM36, CM36, HSCM) | PP048 (PFP36, PFA36, PM36) | DEC051 (TS36, TSW36, BS36, BSW36, SP36) | Fixed by Eric |
| GT36G | WM059 | CM087 (gas ceiling) | PP048 | DEC051 | Fixed by Eric |
| GT36W | **WM049 (WY $292)** | **CM142 (QCM $98, CML $150)** | **PP027 (PF36 null, PFPA $85)** | DEC007 (no SP36) | **NOT UPDATED** |

## Option name mismatches (live vs Accessory Index)

| Code | Live name | Accessory Index name | Price OK? |
|------|-----------|---------------------|-----------|
| WY36 | Wall Yoke | Wall Yoke for GT36 | Yes |
| QCM36 | Quartet Chain Mount | Quartet Chain Mount for GT35 & AM35 | Yes |
| PFP36 | Post Fitter | Post Fitter for GT36 | Yes |
| PFA36 | Post Fitter Adapter | Post Fitter Adaptor for GT36 | Yes |
| PM36 | Pier Mount | Pier Mount w/ Post Fitter for GT36 | Yes |
| TS36 | Top Scroll | Top Scroll for GT36 | Yes |
| TSW36 | Top Scroll Wide | Top Scroll Wide for GT36 | Yes |
| HSCM | Heavy Slope Ceiling Mt | Heavy Slope Ceiling Mount | Yes |
| BS36 | GT36 Bottom Scroll | Bottom Scroll for GT36 | Yes |
| BSW36 | GT36 Bottom Scroll Wide | Bottom Scroll Wide for GT36 | Yes |

## Stories (catalog-wide)

- **Local** `stories.csv` GT36E: clean 2-paragraph text, no bullets.
- **Live** GT36E: Eric's July 1 push replaced it with 6 inline bullet points — one wall of text on iPad.
- **379 of 396** live products have `•` bullets without `<br>` line breaks (Arcadia, Biltmore, Turtle Friendly, all collections).
- **Fix in `stories.csv.july1_fix`:** Georgetown GT36E/G/W restored to local clean text; remaining 376 stories get `<br><br>` + `<br>•` HTML formatting.

## Option names (catalog-wide)

Live DB has **368 options**. Cross-check against Accessory Index (419 SKUs) found **44 name mismatches** in the fix file, including:

- All GT36 size-specific codes (WY36, QCM36, PFP36, PFA36, PM36, TS36, TSW36, BS36, BSW36, HSCM)
- Biltmore pier mount abbreviations (BMCPM1–18: "Biltmore Copper Pier Mt" → full name)
- Grand Harbor combo labels (GH1-PF, etc.)
- DBPA abbreviation

Prices on GT36 codes are **correct** on live — only display names are wrong.

## Import events (July 1)

| Time (UTC) | File | Result |
|------------|------|--------|
| 20:56 | options.csv | Clean |
| 21:02 | option_groups.csv | Clean |
| 21:07 | products.csv | Warnings only (Feature1-6, ProductTags, missing UPCs) |
| 21:16 | stories.csv | Clean (orphan warnings gone) |

## Recommended fix order

1. **options.csv** — full file; align all Accessory Index names (especially GT36 codes)
2. **option_groups.csv** — full file; no structural change needed except verify WM059 groups
3. **products.csv** — update GT36W OptionSet2/3/4/6 to WM059/CM166/PP048/DEC051
4. **stories.csv** — restore pre-Eric formatting OR add HTML breaks
5. Import order: options → option_groups → products → stories
6. Re-import option_groups after options (options import nulls group membership)

## Open question for Jordan

QCM36 is labeled "Quartet Chain Mount for GT35 & AM35" in the Accessory Index but assigned to GT36E ceiling mount. No GT35 product exists. Confirm label or assignment.
