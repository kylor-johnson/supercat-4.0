# Legrand eCat Taxonomy — build worksheet

Live org `leg` (id 273) import method = **FurnishWeb / Auto-Create**. On the product import, **TradeName, Collections, and Categories auto-create** from the name strings in `products.csv`; empty leftover taxonomy from the sales POC is auto-pruned once no product references it. **Groups do NOT come from the product file** — every auto-created category lands under a single *Default Group*, so the Group -> Category assignment below must be done in Admin (see two options at the bottom).

## Brand axis — Trade Names (adorne / radiant)

| Trade Name | CollectionCodes (mirrors TN) | Products |
|---|---|---|
| adorne | adorne | 455 |
| radiant | radiant | 565 |

> **2026-07-24:** Trade Names are **adorne** and **radiant** (not a parent "Legrand" TN). Matches client ask: pick brand before category. `CollectionCodes` mirrors the trade name (required field). Old Legrand / COL1 / COL2 rows prune on a clean import once unused.

## Functional axis — Group -> Category

Categories mapped to the client's **5 existing Admin groups** (`Switches & Outlets`, `Dimmers`, `Sensors & Timers`, `Plates, Boxes & Blanks`, `Smart Technology`). Rows marked **CONFIRM** are best-guess placements for the meeting.

### Switches & Outlets  (457 products, 14 categories)

| Category | Products | Collection(s) | Confirm? |
|---|---|---|---|
| USB Outlet | 109 | adorne,radiant |  |
| GFCI | 62 | adorne,radiant |  |
| Outlets | 54 | adorne,radiant |  |
| GFCI/USB | 52 | radiant |  |
| Switches | 42 | radiant |  |
| Light Switch | 41 | adorne,radiant |  |
| Combination Devices | 29 | radiant |  |
| Connectivity | 23 | adorne | **CONFIRM** |
| Night Lights | 11 | adorne,radiant | **CONFIRM** |
| AFCI Devices | 10 | radiant |  |
| Antimicrobial Devices | 8 | radiant | **CONFIRM** |
| Countertop Outlet | 8 | radiant |  |
| EV Charging | 6 | radiant | **CONFIRM** |
| Locator Light | 2 | adorne | **CONFIRM** |

### Dimmers  (87 products, 3 categories)

| Category | Products | Collection(s) | Confirm? |
|---|---|---|---|
| Dimmer | 44 | adorne,radiant |  |
| Dimmer Kit | 36 | radiant |  |
| Fan Control | 7 | adorne,radiant | **CONFIRM** |

### Sensors & Timers  (19 products, 3 categories)

| Category | Products | Collection(s) | Confirm? |
|---|---|---|---|
| Timer Switch | 9 | adorne,radiant |  |
| Occupancy Sensor | 6 | adorne,radiant |  |
| Vacancy Sensor | 4 | adorne,radiant |  |

### Plates, Boxes & Blanks  (292 products, 7 categories)

| Category | Products | Collection(s) | Confirm? |
|---|---|---|---|
| Plastics Wall Plate | 105 | adorne |  |
| Cast Metal Wall Plate | 60 | adorne |  |
| Real Materials Wall Plate | 55 | adorne |  |
| Screwless Wall Plates | 54 | radiant |  |
| Inserts | 9 | radiant |  |
| Sub Frame | 6 | adorne |  |
| Device Blank | 3 | adorne |  |

### Smart Technology  (165 products, 9 categories)

| Category | Products | Collection(s) | Confirm? |
|---|---|---|---|
| Smart Color Change Kit | 69 | adorne,radiant |  |
| Smart Scene Controller | 43 | adorne,radiant |  |
| Smart Switch | 14 | adorne,radiant |  |
| Smart Gateway | 12 | adorne,radiant |  |
| Smart Outlet | 12 | adorne,radiant |  |
| Smart Dimmer | 9 | adorne,radiant | **CONFIRM** |
| Smart Home (Netatmo) | 2 | radiant |  |
| Smart Lamp Module | 2 | radiant |  |
| Smart Outlet Kit | 2 | radiant |  |

## Confirm with the client

- **~7 best-guess placements** (marked CONFIRM above): `Antimicrobial Devices`, `Connectivity`, `EV Charging`, `Fan Control`, `Locator Light`, `Night Lights`, `Smart Dimmer`. Decide the right group, or add a 6th **Accessories** group for the odd ones (Connectivity, Night Lights, Locator Light, Antimicrobial).
- **`Light Switch` vs `Switches`** — kept separate; confirm whether to merge (adorne says 'Light Switch', radiant says 'Switches').
- Auto-applied singular/plural merges: `Outlet` -> `Outlets`, `Night Light` -> `Night Lights`.

## How to make the groups stick (pick one)

1. **Pre-create (clean):** in `Products > Groups & Categories`, create each category above under its group *before* importing products. The importer matches categories by name (`find_or_create_category`), so it reuses them and they keep their group — nothing lands in Default Group.
2. **Import then reassign:** import first (all categories land in *Default Group*), then drag/reassign each to its group in Admin. Group reassignment does not require re-importing products.

`group-category-map.csv` is the machine-readable version of this sheet.
