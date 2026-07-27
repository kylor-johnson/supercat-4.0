# CopperSmith — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `tcs` (Postgres org id 291)
- **Vertical:** configurable lighting (copper lanterns, gas/electric)
- **Status / stage:** fully suspended (churned; retained for options/mapping learnings)

## Archetype & applicability
- **Archetype:** snowflake
- **Product line:** ecat-ipad
- **Flags:** `churned`, `manual-review`
- **File owner mode:** csv
- **Image mode:** cdn-url
- **Source cutover date:** 2026-04-21
- **Sub-brands:** none

- **Snowflake annotates; it never blocks.** The unusual parts are real — buildable SKUs,
  nested options, a PIM (Catsy) upstream, and a live builder script in org properties — but
  the failures here were **ordinary bugs in an unusual costume**: invented field limits,
  wrong import order, and PNG URLs. Nothing about this client is un-automatable.
- **`image_mode: url` is the reason the URL census exists.** PNG assets and a JPEG-only
  requirement were **both raised at the 2026-04-21 kickoff** and never checked against each
  other: 23 PNG URLs across 54 rows cost eight weeks. HEAD every URL for `200` +
  `image/jpeg`; reject `.png`, dead links, and Drive/Dropbox share links.
- **`file_owner: csv` was decided the hard way.** A generator that owned `products.csv`
  destroyed weeks of work on this org and was formally retired. One owner per artifact.
- **Option groups were imported before options here**, nulling membership — the order check
  refuses that sequence.
- **Cutover date = the Catsy migration.** The prior Google Drive data was explicitly
  demo-only, so no pre-kickoff row count means anything for this org.
- **Churned means excluded from go-live metrics, not deleted.** The 364 options / 343 groups
  and the `configured_item_number_builder` config are the reference implementation to reuse.
- **Systems:** PIM = Catsy; inventory = Odoo; goal = API integration (avoid dual maintenance)

## Contacts
- **Client:** Jordan Anna (data/PIM), Brent (technical)
- **SuperCat:** Kylor Johnson; Jon (integration tiers)

## Source of truth
- **Master Excel workbook** (`CS_Master_Product_List_*`): Master Sheet, Accessories,
  Image Family Links. The SKU Builder (copper-sku.pages.dev) is **logic reference only**,
  not a structural source. Accessories tab = canonical finish dictionary.

## Options model
- **OptionSet1 = Finish, 2 = Mount, 3 = Decorative, 4 = Gas/Electric.**
- Option/group codes ≤15 chars; group code naming `FIN_STD`, `MNT_<sku>`.
- **Group addend blank** (not `0` — `0` zeroes option prices); per-option `PriceAddend`.
- Parent accessory codes (`FH`, `BS`, …) are non-orderable groupings — use the
  **`Accessory Parent SKU`** column to filter to orderable variants (`FH1`–`FH11`).
- AOB families = bare brass + Clear Coat only (`brassOnly`), not the full 5-finish set.

## Smart SKU Builder (NOT set by import)
- Org property `configured_item_number_builder` (JSONB) — set by **superadmin** via
  Rails console / Admin "Order Item Number Construction". Verified SKUs e.g.
  `CO18G-BLK-DSMS-ASV`, `AOB28E-CLEAR-COY10`.

## Pricing
- **MAP = Dealer Net × 2.0** (arithmetic). **MSRP = round(MAP × 1.1)**. Finish upcharge
  BLK/GRAY/BRZ/CLEAR = $136 Dealer Net; COPPER = $0 default.

## Fidelity gaps (defer to API phase)
- No native cross-set conditional logic (companions, gas/Wind-Guard exclusions,
  top+bottom additive). Model Mount as one combined OptionSet for the demo.

## Open items
- [ ] Confirm load order options → option_groups → products, then set builder JS
- [ ] 20 product-tab codes with no Accessories row (exclude + flag, don't guess)
- [ ] Integration tier decision (Brent/Jon)
