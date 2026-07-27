# CopperSmith — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `tcs` (Postgres org id 291)
- **Vertical:** configurable lighting (copper lanterns, gas/electric)
- **Status / stage:** onboarding — demo build
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
