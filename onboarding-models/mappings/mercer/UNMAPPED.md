# 111 Mercer — what is NOT mapped, and why

Generated from `Source Data/111Mercer-ItemExport .csv` (102 rows, 56 columns)

## Importer-required fields

`products.csv` has exactly **one** importer-required header: `BaseItemCode`.
It is mapped, from the source `Name` column.

So the strict answer to "every unmapped required field" is: **none**. The
useful answer is below — the source columns carrying data that no eCat field
receives. Each is a decision for the client, not a default.

## Source columns not mapped

| source column | fill | why not mapped |
|---|---|---|
| `Internal ID` | 100.0% | NetSuite surrogate id. `Name` is the code reps search by (102/102 join to the live build). |
| `Display Name` | 0.0% | 0% populated — a header, not a field. |
| `(blank header)` | 100.0% | **Blank header.** An unrecognised column is a FATAL import error; it is not carried into the output. |
| `Purchase Description` | 0.0% | 0% populated — a header, not a field. |
| `Vendor Name` | 0.0% | 0% populated — a header, not a field. |
| `Primary Units Type` | 0.0% | 0% populated — a header, not a field. |
| `Primary Stock Unit` | 0.0% | 0% populated — a header, not a field. |
| `Primary Purchase Unit` | 0.0% | 0% populated — a header, not a field. |
| `Primary Sale Unit` | 0.0% | 0% populated — a header, not a field. |
| `Display in Web Site` | 100.0% | Single constant (No). Also identical to `Drop Ship Item` and `Special Order Item` — three names, one value. |
| `Purchase Price` | 0.0% | 0% populated — a header, not a field. |
| `Preferred Vendor` | 0.0% | 0% populated — a header, not a field. |
| `1. Tempaper.com Price` | 90.2% | Price tier the client confirmed does not apply to this brand/division. |
| `5. All Pro Stock` | 83.3% | Price tier the client confirmed does not apply to this brand/division. |
| `7. Distributor` | 93.1% | Price tier the client confirmed does not apply to this brand/division. |
| `Amazon` | 6.9% | 7% populated. Channel price, not a catalogue price level. |
| `Complimentary Customer` | 100.0% | Single constant (0) across all 102 rows — no information. |
| `Decorator's Best` | 46.1% | 46% populated. Channel price, not a catalogue price level. |
| `Kohl's DVS` | 0.0% | 0% populated — a header, not a field. |
| `Ontario Wallcovering` | 32.4% | 32% populated. Channel price, not a catalogue price level. |
| `WALLPAPER BOOK - DROPSHIP` | 62.7% | Sample-book pricing, a separate product line. 63% populated; needs a client decision. |
| `WALLPAPER BOOK - TRADE` | 62.7% | Sample-book pricing, a separate product line. 63% populated; needs a client decision. |
| `WALLPAPER BOOK - WHOLESALE/CASEPACK` | 61.8% | Sample-book pricing, a separate product line. 62% populated; needs a client decision. |
| `Income Account` | 100.0% | Accounting, not catalogue. Single constant (Sales). |
| `Asset Account` | 100.0% | Accounting, not catalogue. Single constant. |
| `Expense/COGS Account` | 100.0% | Accounting, not catalogue. Single constant. |
| `Costing Method` | 100.0% | Accounting, not catalogue. Single constant (Average). |
| `On Special` | 0.0% | 0% populated — a header, not a field. |
| `Tax Schedule` | 100.0% | Accounting, not catalogue. Single constant (Taxable). |
| `On Hand` | 55.9% | Inventory, not products. Belongs in `inventory.csv`, which is not built here. |
| `Available` | 55.9% | Inventory, not products. Also holds values IDENTICAL to `On Hand` on all 57 populated rows — one field under two names. |
| `On Order` | 0.0% | 0% populated — a header, not a field. |
| `Committed` | 0.0% | 0% populated — a header, not a field. |
| `Back Ordered` | 1.0% | 1% populated (1 of 102) — too sparse to be a field. |
| `Reorder Point` | 80.4% | Replenishment planning, not catalogue. |
| `Preferred Stock Level` | 70.6% | Replenishment planning, not catalogue. |
| `Reorder Multiple` | 0.0% | 0% populated — a header, not a field. |
| `Drop Ship Item` | 100.0% | Single constant (No), identical to `Display in Web Site`. |
| `Special Order Item` | 100.0% | Single constant (No), identical to `Display in Web Site`. |
| `Copy SO Descr.` | 0.0% | 0% populated — a header, not a field. |
| `Weight Units` | 100.0% | Single constant (lb). `ShipWeight` is already in pounds. |
| `Class` | 100.0% | NetSuite class hierarchy. Taxonomy comes from `Collection`, already mapped. |
| `Department` | 0.0% | 0% populated — a header, not a field. |
| `Date Created` | 100.0% | ERP metadata, no eCat field. |
| `Last Modified` | 100.0% | ERP metadata, no eCat field. |
| `Planner` | 69.6% | Single constant (a staff name). Internal, not rep-facing. |
| `SPS Item Synch` | 0.0% | 0% populated — a header, not a field. |
| `Active on Tempaper.com` | 100.0% | Channel visibility flag. Not asked for; would need a client decision before becoming `Hideable`. |

## Open questions for the client — flagged, not guessed

These come from the existing build notes and are unchanged by this mapping:

1. **`Price_trade` is `0` on all 45 sample SKUs.** Base is 6.95 and the other
   tiers are 6. If samples are free to trade accounts this imports fine and reps
   see $0.00. If it means "not priced yet", a $0 price on the iPad is
   indistinguishable from a free sample.
2. **Trade is $2 above base on 6 SKUs** — `PR5141`–`PR5144`, `CF5134`, `CF5135`.
   Base $160, Trade $162. Every other SKU has Trade below Base. Pricing floor or
   a NetSuite typo — the client's call, unchanged here.
3. **Image filenames are a convention we chose**, not names the client supplied
   (`GL9190-S` → `gl9190-s.jpg`). If his files are named anything else all 102
   values are wrong, and a clean import will not catch it.
