# The CopperSmith (tcs) — Handoff Prompt (July 1 Crisis)

See also: `CS_OptionMapping_Rebuild/JULY1_AUDIT.md`, `JULY1_FIX_RUNBOOK.md`, `JORDAN_EMAIL_JULY1.md`

## Context

CopperSmith is a luxury copper lantern manufacturer. eCat org `tcs` (org_id=291), live on iPad with SmartStringBuilder JS (order SKUs = base item + selected option codes joined with hyphens).

**Crisis:** Jordan frustrated. Eric pushed corrected files via FTP July 1 (~3PM MDT) changing option codes/groups. Partially correct (GT36E/G use WY36, CM36, etc.) but broadly broken — wrong option display names, GT36W missed, story formatting degraded, possible issues across ALL collections.

## Chain of custody

| When | What |
|------|------|
| June 30 | Kylor imported Eric's "corrected catalog files" (generic codes WY, CML, QCHM). Stray-comma fix on 6 bulb rows. Eric said keep existing stories.csv. |
| June 30 | Jordan angry — WY36 must never simplify to WY. These are configurator options with exact accessory SKUs on orders. |
| July 1 ~3PM MDT | Eric FTP push: size-specific codes (WY36, CM36, QCM36, PFP36, PFA36, PM36, SP36), new groups (WM059, CM166, PP048, DEC051), story orphan cleanup. |
| July 1 ~4:20 PM MDT | Kylor synced iPad — multiple problems found. |

**Kylor's local files do NOT contain Eric's July 1 changes.** Live iPad state = Eric's FTP push.

## Source of truth

| Asset | Path |
|-------|------|
| Accessory Index | `Source Data/Accessories-Table 1.csv` |
| Master Sheet | `Source Data/Master Sheet E+G-Table 1.csv` |
| Kylor last-imported (STALE) | `CS_OptionMapping_Rebuild/*.csv` |
| Eric original (June 30) | `~/Downloads/correctedecatfiles/` |
| Email thread | `~/Downloads/cursor_onboarding_email_review.md` |

## SmartStringBuilder

Joins `[baseItemNumber, ...selectedOptionCodes].join("-")`, skips COPPER, WALL, CEIL, POST. Selected option **code** appears on the order — why Jordan insists on exact Accessory Index codes.

## Known problems (verified July 1 ~5PM MDT)

1. **Option display names** — Eric's size-specific codes have wrong labels vs Accessory Index (WY36 shows "Wall Yoke" not "Wall Yoke for GT36", etc.)
2. **GT36W not updated** — still WM049/CM142/PP027/DEC007 with generic WY ($292), CML ($150), QCM ($98). Revenue leak up to $380+/order.
3. **Story formatting** — 379/396 products: bullet characters inline, no line breaks. GT36E live story is wall of text; local stories.csv was clean.
4. **Broader audit needed** — all stories, all option names, collection assignments (agent completed initial audit — see JULY1_AUDIT.md)
5. **Products import warnings** — Feature1-6, ProductTags unrecognized; missing UPCs on LL-TUBE6A, LL-TUBE8A, FB12V, FBBM1, GTTL, CHSI, GLC

## Confirmed working (GT36E/G)

- Option codes correct (WY36, CM36, QCM36, PFP36, PFA36, PM36, SP36) with correct prices
- Gas/electric separation correct
- Grand Harbor combos on CS43G
- Austin PFPAU/PMAU, Aurora PMAO
- Story orphan warnings gone

## Fix files ready

| File | Status |
|------|--------|
| `options.csv.july1_fix` | Ready — exported from live DB + 44 Accessory Index name fixes |
| `option_groups.csv.july1_fix` | Ready — exported from live DB (343 groups) |
| `stories.csv.july1_fix` | Ready — 376 bullet HTML fixes + GT36 clean restore |
| `products.csv.july1_fix` | **Do not upload wholesale** — patch GT36W only on FTP products.csv |

## Open items

- [ ] Upload fix files (options → option_groups → products GT36W patch → stories)
- [ ] Jordan confirm QCM36 label ("GT35 & AM35" vs on GT36E)
- [ ] Draft/send email (`JORDAN_EMAIL_JULY1.md`)
- [ ] iPad verify GT36E/G/W after import

## Email tone

Plain English for Jordan. No importer/option_groups/PriceAddend jargon. No blame. Numbered points. Kylor owns mistakes briefly. Sign off: Best, Kylor.
