# `customers.csv` — what we need before the next BC export

Hi Silvio — quick read-through of the customer file you sent. Most of the structure is there; we just need a few additional fields and one structural rule before we import it into eCat. Sharing here so you can update the export once and not have to bounce back to BC multiple times.

---

## What's missing in the current export

Per the eCat customer-file spec, these are **required** for every row and were not present in your last export:

| Field | Why we need it |
|---|---|
| `BillToState` | Required. iPad won't accept rows without a state/province on US/Canada bill-to addresses. |
| `BillToPostCode` | Required. |
| `ShipToState` | Required. If a customer has a single location, populate the same as bill-to. |
| `ShipToPostCode` | Required. |
| `BillToCountry` / `ShipToCountry` | Strongly recommended. If we turn on country validation (recommended for US + Canada mixed file), these must be **2-character ISO-3166 codes** — `US`, `CA`. Not `United States`, not `Canada`. |
| `DefaultPriceCode` | Required. Tells eCat which of the 4 price levels each customer should see. See "Pricing" section below. |
| `TerritoryCodes` | Required. This is your rep code per customer. Your current export already has a rep column — we just need it mapped to a short code we'll register in eCat for each rep. |

Also recommended (optional but high-value for the iPad UX):

| Field | Why |
|---|---|
| `BillToShortname` (≤25 chars) | Shown in compact customer pickers on the iPad. Falls back to `BillToName` if blank. |
| `BuyerEmail`, `BuyerFirstName`, `BuyerLastName`, `BuyerPhone` | Auto-fills the order form when reps select a customer. Saves typing at market. |
| `Terms` | Pre-fills payment terms on quotes/orders. |
| `ShipInstructions` | Pre-fills shipping notes per ship-to. Useful for "deliver to back door, ring bell" type guidance. |

---

## Pricing — `DefaultPriceCode` mapping

We're going to register 4 price levels in eCat that mirror your spec master:

| eCat price level code (proposed) | Spec master column | Audience |
|---|---|---|
| `us-wsp` (this is `NetPrice` in the product file) | `WSP-USD` | US customers see this as their net wholesale |
| `us-imap` | `IMAP-USD` | US — retail / MAP comparison shown next to wholesale |
| `cad-wsp` | `WSP-CAD` | Canadian customers see this as their net wholesale |
| `cad-imap` | `IMAP-CAD` | Canada — retail / MAP comparison |

For each customer, `DefaultPriceCode` should be one of `us-wsp` or `cad-wsp` based on the billing country. The IMAP price will display alongside on the iPad as a comparison — that part is configured in eCat, not in the customer file.

(Codes above are placeholders — happy to adjust on tomorrow's call if you prefer different short codes.)

---

## Multiple ship-tos

You mentioned customers with a single billing address but multiple physical locations (e.g., one PO box billing + 6 showroom/warehouse ship-tos). The file format supports this — here's the structure eCat expects:

```
BillToCode, BillToName, BillToAddress1, ..., ShipToCode, ShipToName, ShipToAddress1, ...
ACME001,    Acme Corp,  PO Box 123,     ..., DC-EAST,    Acme East, 100 Main St,     ...   <- row 1: full bill-to + first ship-to
,           ,           ,               ..., DC-WEST,    Acme West, 200 Oak Ave,     ...   <- row 2: bill-to fields BLANK, only ship-to
,           ,           ,               ..., SHOW-NYC,   Acme NYC,  300 5th Ave,     ...   <- row 3: bill-to fields BLANK, only ship-to
```

Rules:
- The file **must be sorted by `BillToCode`** so all rows for one customer are adjacent.
- The **first row per customer** has the full bill-to + first ship-to address.
- **Subsequent rows** for the same customer leave bill-to fields blank and only fill ship-to.

You don't need to repeat the customer's bill-to info on every line.

---

## Territory codes

In the export you sent, there's a column listing the rep's name next to each customer. eCat uses short rep codes (sometimes called "salesman numbers") instead of names. Two options:

1. **You give us a list of rep codes**: just a 2-column mapping like `Rep Name → Rep Code` (e.g., `Sarah Johnson → SJ`, `Mike Lin → ML`). We'll populate `TerritoryCodes` from that. You can use any short code — initials, ID number, whatever you use in BC.
2. **We pick the codes**: I can default to initials and you can override later. Slower if there are collisions (two reps with same initials).

Per your kickoff comments, reps are assigned to specific customers (not by zip/territory), so this is a 1:1 mapping per customer row. If a customer has multiple reps, comma-separate the codes (no spaces): `SJ,ML`.

For `ShipToTerritoryCodes` (per-ship-to rep override), only populate if a specific ship-to should be visible to a *different* rep than the bill-to rep. You don't have this case from what I saw, so leave empty.

---

## Customer scope (open question — your call)

In kickoff, Jon raised that we could load **all** customers and use eCat user groups to control visibility, vs. loading **showrooms only** as you've filtered. Tradeoff:

- **Showrooms only (current approach)**: cleaner, faster initial import, simpler mental model. But if reps ever pick up the iPad for non-showroom customers, those records won't be there.
- **Load everything + filter by group**: more setup work up front (define commercial vs. hospitality vs. showroom user groups), but reps can always find any customer.

For Lightovation specifically, showrooms-only is fine. We can expand scope after market without disrupting anything.

---

## Mapping & promotion (FYI, not blocking)

Two things to know about for after go-live:

- **`MappedBillToCode` / `MappedShipToCode`**: If a customer's BC ID ever changes (e.g., post-merger), the old ID goes in `MappedBillToCode` of the new row. eCat preserves the order history continuity. You won't need this for v1.
- **Local customer promotion**: Reps can create new customers on the iPad on the fly (e.g., walk-up showroom traffic). Those get a UUID. When you eventually add them to BC and re-export, the UUID goes in `MappedBillToCode` to stitch the order history back to the official record. This is automatic — just be aware it exists.

---

## What I need from you

When you do the next BC export, please include the additional fields above and:

1. Sort by `BillToCode`.
2. Country codes as `US` / `CA` (2-letter ISO).
3. Multi-ship-to customers split across rows with bill-to-blank for rows 2+.
4. Send the rep name → rep code mapping (separate file is fine — a 2-column CSV or just paste in an email).

Goal: get the next export back in front of me before our June 4 check-in so we can light up the iPad customer picker + price-level routing for the June 16 rep training.

Reach out anytime — happy to do a quick screenshare on BC's export side if it speeds this up.
