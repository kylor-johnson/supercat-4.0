# Pebl customers.csv — fixes applied 2026-06-30

Source: client `customers (4).csv` (171 rows)

## Import-ready file

`Ready_For_Import/customers.csv`

## Fixes applied

### Placeholder addresses (15 accounts — no address in ERP export)

These rows would have **failed import** without ship-to/bill-to address. We used company name + `City pending` / `NA` / `00000` so the batch can load. **Client should send real addresses when available.**

CCS, PURE INTERIOR P, KRE, OG, HAS, DGA, HH, OKL, TBK, RAL, YAYA, DION, FNV, FL, Jtrade

### Country code corrections

| BillToCode | Was | Now |
|---|---|---|
| PSM | ES | HK |
| ALT | IN | CN |
| ABY | SA | KW |
| Al Jadwal | US | JO |
| KPBR | US | TH |
| LFT | US | NZ |
| TZT | US | NZ |
| FL | US | MT |
| AF | BE | HK |

### City / postcode corrections

- **BP** — city set to Moscow, postcode 119618
- **NAN** — city Honolulu, postcode 96819, country US

### Other cleanup

- Flattened embedded newlines in address fields to single lines (23 rows)
- **BuyerEmail** — first address only where multiple (`;` or `/`); malformed emails cleaned (BP, KFR, CMA, BTM, MOB, etc.)
- Encoding cleanup where detectable (accents, mojibake)
- Sorted by `BillToCode`

## Not changed (client may refine later)

- `DefaultPriceCode` = `fob` on all rows (USD)
- `BillToCode` values with spaces (`Al Jadwal`, `PEBL USA-WL`) — valid, left as-is
- Some city/postcode fields still approximate — non-US addresses, no validation enforced
