---
name: ecat-customers-build
description: Build and troubleshoot the eCat iPad customers.csv — required bill-to/ship-to fields, sort order, DefaultPriceCode, TerritoryCodes, and ERP-export mapping. Use when building a customer file, mapping a Business Central/ERP export, or diagnosing a failed customer import.
---

# eCat customers.csv (iPad)

Reminder (see `ecat-ground-truth`): a partial customers.csv **HARD-deletes ALL
customers + ship-tos** then reloads. Always send the full file.

## Required fields (importer-fatal)

`BillToCode`(15), `BillToName`(60), `BillToAddress1`(60), `BillToCity`(60),
`BillToState`(60), `BillToPostCode`(20), `DefaultPriceCode`(30).
Ship-to rows additionally require `ShipToAddress1`, `ShipToCity`.

- **`DefaultPriceCode` must exactly match an Admin price level Code** (Products →
  Price Levels). This is the #1 failure: ERP placeholder `0` or status text like
  `PENDING`/`CLOSED` is not a valid code → every row rejected → 0 customers.
- **`TerritoryCodes`**: KB-required but NOT importer-fatal. Needed so reps in a
  "show only associated customers" group see the account. Comma-separated, no spaces.

## File structure

- **Sort by `BillToCode`.** Multiple ship-tos = additional rows immediately under
  the same `BillToCode` (bill-to fields optional on continuation rows).
- A customer with zero ship-to rows is destroyed with an error — every customer
  needs at least its own address as the first ship-to.
- `ShipToTerritoryCodes` controls which ship-tos a rep sees; if blank, `TerritoryCodes`
  governs the whole account + all ship-tos.

## Mapping an ERP / Business Central export

1. Detect the real file type (exports are often `.xlsx` renamed `.csv`).
2. Required-field gap check — BC exports usually **lack address columns**; request
   an address-enriched export before anything else.
3. Map: `No.`→`BillToCode`, `Name`→`BillToName`, `Salesperson Code`→`TerritoryCodes`,
   `Phone No.`→`BuyerPhone`, `Country/Region Code`→`BillToCountry`/`ShipToCountry`.
4. `DefaultPriceCode`: when two ERP columns could be the price (e.g. disc group vs
   export code), produce a conflict report and ask the client which wins.
5. Filter out `CLOSED`/`PENDING` accounts unless the client confirms inclusion.
6. Decide hierarchy: 318 separate bill-tos vs parent + ship-to rows.

## Other useful fields

`BillToShortname`, `BuyerEmail/FirstName/LastName/Fax`, `Terms`, `Carrier`,
`TradenameCodes` (purchasable tradenames), `ShowroomLocationCode` (enables
placements/showroom audits), `BillTo_<custom>` columns (pre-register in Admin),
`CreditCardAuth` (`required`/`allowed`/`disallowed`).
Country validation: if "Enable country validation?" is on, `BillToCountry`/
`ShipToCountry` must be ISO-3166 2-char codes; only US validates state/postal.

## Import + verify

Tools → Upload Data → Customers (or FTP `/data`). Check File Import Status; a blue
timestamp link lists line-level problems. Errors leave old records in place.

## Missing customer vs import Error (do not fuse)

A ticket that names customer A and pastes an Error on line N is **two lookups**,
not one story.

- Line numbers are physical lines in **that morning's** `customers.csv`. They move
  as rows above shift. A regenerated file's row N is a different customer.
- Older events sometimes include `Customer # = 0021270`. That number is the failing
  row **that day**, not whoever the client is asking about today.
- An `Error` skips that row. Other rows still import. If A is missing, look A up
  by code **and** name. If neighbors on either side of the code exist in Postgres
  and A does not, A was omitted from the imported file or failed on **its** row —
  not blocked by a different row's `DefaultPriceCode`.
- Excel filters on `DefaultPriceCode` showing only `0`–`5` do not disprove a letter
  in the file that actually imported (quoting / column shift / a different export).
