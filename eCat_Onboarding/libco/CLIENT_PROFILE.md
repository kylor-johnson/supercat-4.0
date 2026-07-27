# Lib & Co — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **TradeNameCode:** `LC` (Lib & Co / Liberty)
- **Vertical:** lighting
- **ERP:** Microsoft Business Central
- **Status / stage:** build → import → go-live
- **Events:** Lightovation (June 23); rep training June 16, 3:30 PM ET

## Contacts
- **Client:** Silvio (non-technical — keep emails jargon-free)
- **SuperCat:** Kylor Johnson; AE Jon Vanderberg (POC work); CTO Brent (BC integration)

## Pricing — 4 levels, dual currency
- US WSP = `NetPrice`; US IMAP = `Price_imapusd`; CA WSP = `Price_cad`; CA IMAP = `Price_imapcad`.
- WSP→IMAP ≈ 2.5×. Strip `$`/commas. Always backfill `NetPrice`.
- Discontinued promo: 25% off across all 4 columns (69 in-stock SKUs).

## Catalog
- **42 custom product fields** (lighting specs: Feature1–5, BulbType, IPRating, …) —
  pre-register in Admin, "Send to iPad".
- 9 parts SKUs (Bellissima tubes + Alcamo rods) as `Accessory` category + RelatedItems.
- LongDesc 50-char limit — 587 source rows over; truncation is a Warning.
- Stories: `ProductStory` from features; also used to backfill LongDesc.

## Files
- Spec master: `Lib_Co_Spec_Master_eCat_Mapped`; build via `rebuild_lib_co_files.py`.
- Customers: 318 showroom accounts (`Lib Showroom Customers`), BC export lacks address
  columns — needs enrichment; sort by BillToCode; DefaultPriceCode must map to a level.

## Quirks
- Orphan SKU `10193-02` (111 qty, missing from spec master — cloned from `10193-030`).
- Inventory `NextReceiptDate` had prose ("Discontinued once sold-out") → must be date/blank.
- Smart list "Discontinued — 25% Off".
- Reps assigned by customer (TerritoryCodes), not by state/zip.

## Open items
- [ ] Address-enriched customer export + hierarchy decision (318 bill-tos vs ship-tos)
- [ ] FTP/CDN image delivery
- [ ] Smart list visibility on iPad (user-group + sync)
