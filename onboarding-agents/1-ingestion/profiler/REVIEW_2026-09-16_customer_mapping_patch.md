# Review packet — 2026-09-16 customer-mapping patch

> **2026-09-25.** Rescued from the dead `onboarding-models/` path. The source edits this
> packet describes (`norm_token`, `field_owner`, `field_in_target` in `ecat_vocab.py`,
> `propose(raw, target=)` in `ecat_aliases.py`, the `folder_mode.py` and `file_mode.py`
> changes) are **not in this tree** and are on no branch. `test_customer_mapping.py` fails
> on import until they are recovered from the machine that made them.

Profiler repairs only. No commit. No `customers.csv`. No edits to
`runner/clients.toml`, `mappings/**`, or `02_Implementation/`.

Interpreter: `/opt/homebrew/bin/python3`. Unit tests:
`onboarding-agents/1-ingestion/profiler/test_customer_mapping.py` (16 tests, all OK).

---

## What changed, file by file

**`ecat_vocab.py`**
- Added `norm_token()`: lowercase, keep alphanumerics **and underscores**.
- `PATTERNED` for Price_<code> is now `^price_[a-z0-9]+$` on that form.
  `Price_trade` → `price_trade` matches; `Price Level` → `pricelevel` does not.
- `patterned_match` / `is_ecat_header` take the raw header so the underscore is
  still visible. Passing already-stripped `pricetrade` does not match — that is
  the point.
- Per-division qty regex allows an optional underscore (`NSL_QtyOnHand`).
- Added `field_owner` / `field_in_target` so a proposal can be rejected when it
  belongs to a different eCat file.

**`folder_mode.py`**
- `find_header_row`, `score_target`, `classify_input`, and the transposed-options
  detector now pass raw headers into `is_ecat_header` / `patterned_match`.

**`ecat_aliases.py`**
- `propose(raw, target=)` accepts a proposal only if the field belongs to that
  target. An alias that matches a **foreign** field returns None and does **not**
  fall through to token hints (that is the anti-overfit latch).
- Aliases added, all ordinary ERP English: `company name` → BillToName [high];
  `phone number` (Phone / Phone 1 still work) → BuyerPhone [high]; `net terms` →
  Terms; `first & last name` → BuyerFirstName / BuyerLastName [moderate];
  `zip code` → BillToPostCode; `street 2` → BillToAddress2.
- `company` is **not** a PREFIX.

**`file_mode.py`**
- Mapping loop: this-target exact/patterned → `propose(target=)` → foreign-eCat
  note only if propose returned nothing → unmapped.
- Section 6 (generic): email-shaped column whose values have no `@`; trailing
  rows whose only content is whitespace/NBSP; unique customer ids **and** no
  address/ship-to **headers**; BillToName over the importer limit from
  `limits_generated.py` (60, tier error).

**`test_customer_mapping.py`** (new, no iCloud)
- Price Level vs Price_trade; propose() with `target=customers` vs `products`
  for Name / Company Name / Price Level / Phone Number / Phone 1 / Zip Code /
  Street 2.

**`SKILL.md`** — one sentence on the underscore form and the target latch.
**`REVIEW_LOG.md`** — 2026-09-16 section.
**`KICKOFF_ingestion.md`** — fifth shape: the Mercer customer xlsx (bare list,
no addresses, not buildable). Nothing else in that file rewritten.

---

## BEFORE vs AFTER mapping tables

### A1 — Magic Lite raw (lock)

Both files **unchanged**. Missing required: `defaultpricecode` only.

**ML CUSTOMER LIST.xlsx** (raw; customers.csv, low-inference)

| source | field | conf |
|---|---|---|
| Customer Number | BillToCode | high |
| Customer Name | BillToName | high |
| Address 1 | BillToAddress1 | high |
| Address 2 | BillToAddress2 | high |
| City | BillToCity | high |
| Province | BillToState | high |
| Postal | BillToPostCode | high |
| Phone 1 | BuyerPhone | high |
| Salesperson ID | TerritoryCodes | high |

**NSL CUSTOMER LIST.xlsx** — same table except State / Zip in place of
Province / Postal. Unchanged.

Section 6 unique-ids + no-address-headers did **not** fire (address headers
are present).

### A2 — Magic Lite Combined 2.0 (lock)

**Unchanged.** Class 2 pre-mapped, 16 of 16 eCat headers, VALIDATE do not
re-map. Every required field present. Headers remain BillTo* / ShipTo* /
DefaultPriceCode at [certain]. Unique-ids + no-address-headers did **not**
fire (those columns exist; BillToCode also repeats by design).

### A3 — CopperSmith Dealers_eCat-Table 1.csv

Addresses present: unique-ids + no-address-headers did **not** fire.
Pricelist was **not** marked DefaultPriceCode [certain] (values are discount
prose). `Type=Vendor` left alone.

| source | BEFORE | AFTER |
|---|---|---|
| Name | Name [moderate] (foreign options field; propose skipped) | **BillToName [high]** |
| Street | BillToAddress1 [high] | same |
| Street 2 | *unmapped* | **BillToAddress2 [high]** |
| City | BillToCity [high] | same |
| State | BillToState [high] | same |
| Zip Code | *unmapped* (`^zip$` missed it) | **BillToPostCode [high]** |
| Phone | BuyerPhone [high] | same |
| Email | BuyerEmail [high] | same |
| Customer Payment Terms | Terms [moderate] | same |
| Pricelist | Pricelist [moderate] (false Price_<code> from stripped `pricelist`) | **unmapped** |
| Territory # / Territory (full) | TerritoryCodes [low] | same |

Missing required: BEFORE `billtocode, billtoname, billtopostcode, defaultpricecode`
→ AFTER `billtocode, defaultpricecode` only (Name and Zip Code filled the other
two). Incidental eCat headers 2 → 1 (`Name` is still a real options field name;
`Pricelist` no longer matches Price_<code>).

Street 2 / Zip Code were genuinely unmapped before — that is the alias fix.
Name → BillToName and Pricelist dropping off Price_<code> are the two general
bugs, not CopperSmith special cases.

### B — Mercer customer xlsx (change allowed)

Input class: BEFORE `raw (with incidental eCat-shaped names)`, 1 of 9 recognised
(`Price Level` as Price_<code>) → AFTER **`raw`**, 0 incidental eCat headers.

| source | BEFORE | AFTER |
|---|---|---|
| Customer ID | BillToCode [high] | BillToCode [high] |
| Company Name | LongDesc [low] (token `name`) | **BillToName [high]** |
| First & Last Name | LongDesc [low] | **BuyerFirstName / BuyerLastName [moderate]** |
| Email Address | BuyerEmail [high] | BuyerEmail [high] |
| Phone Number | *unmapped* | **BuyerPhone [high]** |
| Price Level | Price Level [moderate] (false Price_<code>) | **DefaultPriceCode [high]** |
| Net Terms | NetPrice or Price_<code> [low] (token `net`) | **Terms [high]** |

Missing required: BEFORE billtoaddress1, billtocity, **billtoname**,
billtopostcode, billtostate, **defaultpricecode** → AFTER
**billtoaddress1, billtocity, billtopostcode, billtostate only**.

Still no `customers.csv`. Still MAP, BUT NOT YET / refuse to build — the
missing list is the four address fields, which are absent as columns.

Section 6 (generic; 39 is a count, not a special case):
- 17 trailing rows whose only content is whitespace/NBSP
- email-shaped column, 1 of 39 values has no `@` (specimen happens to be
  `Need to get from Jen` — that string is not in the code)
- unique customer ids and no address/ship-to headers
- 1 BillToName value over the importer 60-char limit (specimen happens to end
  ` - 111 Mercer` — that suffix is not in the code)

### C — Mercer ItemExport (anti-overfit)

Header `Name` is the SKU. **Still Name [moderate] (foreign options field), not
BillToName.** Numbered / Base / Purchase price columns still map as
`NetPrice or Price_<code>`, not DefaultPriceCode.

Phase 0 extra: inventory qty aliases are now rejected on a products target
(in-target latch):

| source | BEFORE | AFTER |
|---|---|---|
| On Hand | QtyOnHand [high] | *unmapped* |
| Available | QtyAvailable [high] | *unmapped* |
| On Order | QtyOnPOrder [high] | *unmapped* |
| Back Ordered | QtyOnBackorder [high] | *unmapped* |

Those four now sit in UNMAPPED SOURCE COLUMNS. Name and price mappings
otherwise match the golden file.

---

## products_template.csv Price_* still recognised

**Yes.** Still pre-mapped, 21 of 24 eCat headers (88%), all five
`Price_tempaper` / `Price_dropship` / `Price_wholesale` / `Price_allpro` /
`Price_distributor` → themselves [certain] as Price_<code>. Mapping table
unchanged. This was checked immediately after the regex change, before any
other work.

---

## Phase 0 four-file mapping-line diffs

Golden file `RUN_2026-09-04_file_mode_four_tests.txt` was **not** rewritten.

| file | mapping-line diffs |
|---|---|
| Legrand adorne CA csv-that-is-xlsx | **none**. (The 5+ decimal specimen *string* in section 6 shuffled because values are a set; counts 143 / 59 are the same.) |
| Mercer ItemExport | four qty lines, listed under C above |
| CopperSmith Master | `Marketing Copy` → ProductStory [high] **dropped** (ProductStory is a stories.csv field; in-target latch) |
| CopperSmith Parts | **none** |

---

## Special-cases tempted and not done

- Did not teach the profiler Mercer-shaped files.
- Did not treat a missing-address file as buildable, or emit customers.csv.
- Did not special-case `Need to get from Jen`, ` - 111 Mercer`, 39 rows, Jen,
  or “if no addresses still emit a file.”
- Did not add `company` to PREFIXES.
- Did not require a digit in Price_<code> (that would drop `Price_trade`).
- Did not parse `.numbers`.
- Did not “fix” CopperSmith Pricelist into an Admin price-level code.
- Did not map `external_id` → BillToCode (not in the alias list).

---

## git diff stat (not committed)

```
 onboarding-agents/1-ingestion/ground-truth/KICKOFF_ingestion.md              |   1 +
 onboarding-agents/1-ingestion/profiler/REVIEW_LOG.md                         |  17 +++
 onboarding-agents/1-ingestion/profiler/SKILL.md                              |   2 +-
 onboarding-agents/1-ingestion/profiler/ecat_aliases.py                       |  33 ++++--
 onboarding-agents/1-ingestion/profiler/ecat_vocab.py                         |  88 ++++++++++++++--
 onboarding-agents/1-ingestion/profiler/file_mode.py                          | 117 +++++++++++++++++++--
 onboarding-agents/1-ingestion/profiler/folder_mode.py                        |  45 +++++---
 7 files changed, 266 insertions(+), 37 deletions(-)
```

Untracked (this session):
- `onboarding-agents/1-ingestion/profiler/test_customer_mapping.py` (106 lines)
- `onboarding-agents/1-ingestion/profiler/REVIEW_2026-09-16_customer_mapping_patch.md` (this file)

Stop here. Human review before any commit.
