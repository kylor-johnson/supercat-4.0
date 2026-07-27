# Legrand — Custom Field & Related Items Setup

Custom fields must be pre-registered in **Admin > Products > Custom Fields** before import, with **Send to iPad** checked and a Label set. Any column in `products.csv` that is not registered is silently ignored on import (so shipping the columns now is harmless).

## Register these custom fields

| Field name (CSV header) | Label | Type | Send to iPad | Use as filter | Recommendation |
|---|---|---|---|---|---|
| `Finish` | Finish | String | Yes | **Multi-select** | Ship. 51 distinct values -> strong catalog filter |
| `CountryOfOrigin` | Country of Origin | String | Yes | No (detail only) | Ship. 7 values: China, France, India, Mexico, Taiwan, United States, Vietnam |
| `drop_ship` | Drop Ship | Boolean | Optional | Boolean (optional) | Constant (Y) — low value, OK to skip registering |
| `shipped_via` | Shipped Via | String | Optional | No | Constant (Fedex or Truck) — low value, OK to skip registering |
| `order_uom` | Order Unit | String | Optional | No | Low cardinality (MASTER, UNIT) — OK to skip registering |

### Distinct Finish values (for reference)

Bi-Color, Black, Black Ink, Black Nickel, Black Stainless, Bronze, Brown, Brushed Black Nickel, Brushed Satin Brass, Brushed Stainless, Brushed Stainless Steel, Champagne Bronze, Clear, Coffee, Copper, Dark Bronze, Evergreen, Gloss White, Gloss White on White, Graphite, Gray, Greige, Ivory, Light Almond, Macassar, Magnesium, Matte Antique Copper, Matte White, Mirror, Mirror Black, Mirror White, Mystic, Nickel, Oatmeal, Oil Rubbed Bronze, Pale Blue, Peachy, Powder White, Red, Rosa, Rustic Gray, Satin Black, Satin Nickel, Slate Linen, Spiraled Stainless, Stainless Steel, Titanium, Tri Color (WH, IV, LA), Tri-Color, True Linen, White

### Finish data quality — confirm with client

Applied unambiguous Finish spelling fixes automatically: `Grahite` -> `Graphite`, `Tri Color` -> `Tri-Color`, `Tri-color` -> `Tri-Color`.

Per-SKU Finish overrides (Name + SKU suffix were right; Finish column was wrong):

- `WNRL43CKITNI` -> `Nickel`
- `WNRL43CKITLA` -> `Light Almond`

The following look like possible duplicates but were **left as-is** because they may be genuinely distinct finishes. As a multi-select filter each becomes its own facet — confirm whether any should be merged:

- `Mirror` / `Mirror White` / `Mirror Black`
- `Gloss White` / `Gloss White on White` / `Powder White` / `Matte White`
- `Brushed Stainless` / `Brushed Stainless Steel` / `Stainless Steel` / `Spiraled Stainless`
- `Tri-Color` / `Tri Color (WH, IV, LA)`

## Freight / carton custom fields

Per the client rule that all non-blank source data must land, the source's carton/packaging columns are captured verbatim. **Recommend registering these as custom fields with 'Send to iPad' checked but 'Hide from details view' selected** — the data lands (and is usable in reports/SmartLists) without cluttering the rep-facing catalog. Confirm the display choice with the client.

| Field name (CSV header) | Label | Source column | Populated |
|---|---|---|---|
| `carton1_h` | Carton 1 Height | Carton Height | 0 |
| `carton1_l` | Carton 1 Length | Carton Length | 0 |
| `carton1_w` | Carton 1 Width | Carton Width | 0 |
| `carton1_wt` | Carton 1 Weight | Carton Weight | 0 |
| `carton2_h` | Carton 2 Height | Carton Height 2 | 0 |
| `carton2_l` | Carton 2 Length | Carton Length 2 | 0 |
| `carton2_w` | Carton 2 Width | Carton Width 2 | 0 |
| `carton3_h` | Carton 3 Height | Carton Height 3 | 0 |
| `carton3_l` | Carton 3 Length | Carton Length 3 | 0 |
| `carton3_w` | Carton 3 Width | Carton Width 3 | 0 |
| `carton3_wt` | Carton 3 Weight | Carton Weight 3 | 0 |
| `cartons_per_unit` | Cartons Per Unit | Cartons Per Unit | 0 |

**Notes:** `Carton Weight 2` was byte-identical to `Carton Weight` on every row, so it is captured once as `carton1_wt` (not duplicated). Carton tiers 1/2/3 are captured positionally; which physical package a tier represents varies row-to-row in the source, so treat them as raw freight data, not clean inner/master/pallet levels. `cartons_per_unit` is constant (`1`).

## Related Items (built-in — NO custom-field registration)

`RelatedItems` is a reserved product-file field. It is populated for **888 SKUs** across **178 finish families**, cross-linking each product to its other finish variants. Each product's list includes its own BaseItemCode (per eCat best practice) so reps can navigate in any direction. See `related-items-review.md` for the full grouping.

## Not applicable for this dataset

- **Product Options** — the source `Add Option 1..10` columns are 100% empty and each finish is its own orderable SKU, so the eCat Options feature is not used. Finish variants are modeled as Related Items.
- **Spec custom fields** (LED/fan/bulb specs, certifications, Materials, Special Feature, document URLs, etc.) — every one of these source columns is empty in this file, so there is nothing to publish.
- **Extra price levels** (`UMAP`, `Dist NET 2..10`, `Sales Price`) — all empty; only the mapped US/CA price levels carry data.
