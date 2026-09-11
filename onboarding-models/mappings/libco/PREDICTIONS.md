# libco — what I decided, blind, and what I could not decide

Written BEFORE opening `rebuild_lib_co_files.py`, the built `products.csv`, or
the live org. This is the scoring sheet: without it, "I got that right" after
unblinding is unfalsifiable.

## Decisions I made from the source

| # | decision | evidence I had |
|---|---|---|
| D1 | **`LIB_Co_Upload_Fixed_Prices.xlsx` is the primary**, not the spec master | fixed prices names its columns (`Subcategory`, `Dimmable`, `Price_cad`) where the spec master uses `Custom1`–`Custom39` and one header literally `?????`; it also adds RelatedItems, IntroDate, NewItem |
| D2 | Spec master is a **superset by key**: 897 of 897 fx keys are in it, 9 sm keys are not in fx | containment, both directions |
| D3 | **Ship 897 rows**, flag the 9 | can't tell from source whether the 9 were discontinued or dropped by accident |
| D4 | **Backfill `LongDesc` from the spec master** | LongDesc 0/897 in fx, 906/906 in sm, max len 82 |
| D5 | **Money = 2dp** (`legrand` dialect) | fx stores bare floats; the only format statement in any client file is the spec master's `$1,025.00`, 906/906 |
| D6 | **Pass Yes/No booleans through unchanged**, report them | class-2 rule is validate-don't-transform |
| D7 | **Header `netprice` → `NetPrice`** | header case; an unrecognised column is a fatal import error |
| D8 | **Drop `ShipLBS`** | duplicate of ShipWeight carrying a unit string |
| D9 | **Drop `Video`** | 9% Google Drive URLs; not a products.csv field |
| D10 | **Keep `CollectionCodes` UPPERCASE**, report it | recasing a label is a client decision |
| D11 | **Ship `Subcategory` as a custom field** | 4 values from CategoryCodes' vocabulary but a different distribution — a real second level, but eCat's home for it is a client question |
| D12 | **strip float tails** on UPCValue and 8 numeric columns | openpyxl returns floats; UPCValue is a TEXT field so `.0` ships verbatim |
| D13 | **`IntroDate` datetime → date** | `2023-01-01 00:00:00`; eCat wants YYYY-MM-DD |
| D14 | **CRLF line terminator** | pure guess — nothing in the source says |
| D15 | **42 columns need Admin registration** before import | not built-in eCat fields; unregistered = silently dropped |

## What I flagged as UNKNOWABLE from the source

These are the deliverable. Each is a question only a human can close.

| # | question | why the source cannot answer it |
|---|---|---|
| U1 | Should whole-dollar prices keep `.00`? | the source stores floats; the client's own presentation is 2dp, but the eCat output format is a separate choice nobody wrote down |
| U2 | Are the 9 spec-master-only SKUs discontinued, or missing? | both files are internally consistent; nothing marks them. **products.csv soft-deletes omitted rows**, so guessing wrong removes 9 live products |
| U3 | Which eCat price level is which? `netprice`, `Price_cad`, `Price_imapcad`, `Price_imapusd` are 4 genuinely distinct levels (0 rows identical between any pair) | the codes must exist in Admin first; the source names them but does not say what a rep should see, or which is the default |
| U4 | Is `Subcategory` a second category level, a filter, or a tag? | it reuses CategoryCodes' four words with a different distribution |
| U5 | Are `Dimmable` / `SlopeCeilingCompatible` / `MotionSensor` / `BulbIncluded` / `ADA` registered as iPad **filters**? | the consequence of Yes/No depends entirely on this, and it lives in Admin, not in the file |
| U6 | Should `Aged Brass` and `Aged brass` be merged? (15 such pairs in FinishCode) | genuinely-distinct finishes exist in this catalogue; only the client knows |
| U7 | 191 of 1,812 referenced images are absent from both image folders | cannot tell "not yet uploaded" from "wrong filename" without the FTP listing |
| U8 | Should `CollectionCodes` ship as `ADELFIA` or `Adelfia`? | Auto-Create makes it the iPad label; both spellings appear across the client's own files |
| U9 | What are the Admin labels for the 42 custom fields? | the spec master's second header row has human labels (`2a - Product spec - Bulb Type`); whether those are the labels to register is a client call |

## Predicted score

I expect to be wrong about U1 (the money format) and about D3/U2 (the row
count), because both are decisions rather than derivations. I expect D1, D4,
D12 and D13 to be right, because the data forced them.
