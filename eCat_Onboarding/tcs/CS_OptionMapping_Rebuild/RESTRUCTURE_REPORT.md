# CopperSmith Option Mapping Restructure — Report

## Summary

- Options added: ['WALL', 'CEIL', 'POST']
- Groups added: ['MT_WALL', 'MT_CEIL', 'MT_POST']
- Products transformed: 425
  - With mounts: 272
  - Without mounts (no change to mount logic): 153

## Mount Type Combinations

| Combo | Count |
|-------|-------|
| WCP (Wall + Ceiling + Post) | 248 |
| -CP (Ceiling + Post) | 8 |
| -C- (Ceiling) | 6 |
| WC- (Wall + Ceiling) | 6 |
| W-P (Wall + Post) | 4 |

## Edge Cases

- EB20E: WallAcc (W070) without wall mount → moved to Decorative (OS5)
- EB27E: WallAcc (W072) without wall mount → moved to Decorative (OS5)
- EB27G: WallAcc (W073) without wall mount → moved to Decorative (OS5)
- EB33E: WallAcc (W074) without wall mount → moved to Decorative (OS5)
- EB33G: WallAcc (W075) without wall mount → moved to Decorative (OS5)

## Option Mapping Stats

- Wall Mount groups in mapping: 158
- Ceiling Mount groups in mapping: 164
- Post & Pier groups in mapping: 152
- Wall Accessory groups in mapping: 164

## Validation

- Total products: 425
- Total valid groups: 767
- Total valid options: 344

- All option codes in groups are valid

- All group codes in products are valid

## New OptionSet Layout

| OptionSet | Label | Content |
|-----------|-------|---------|
| OS1 | Finish | FIN001 or FIN002 (Required) |
| OS2 | Mount Type | MT_WALL, MT_CEIL, MT_POST (Required for mount products) |
| OS3 | Mount Hardware | Merged WM###, CM###, PP### groups |
| OS4 | Wall Accessories | W### / WA### groups (filtered by OS2 mapping) |
| OS5 | Decorative | D### / DEC### groups |
| OS6 | Electric | ELE### / GE### groups |
| OS7 | Gas | GAS### / GE### groups |
| OS8 | (empty) | — |

## Option Mapping (Admin Console)

One mapping record on OptionSet2:

- **MT_WALL** → OS3: wall mount groups | OS4: wall accessory groups
- **MT_CEIL** → OS3: ceiling mount groups | OS4: [] (hidden)
- **MT_POST** → OS3: post/pier groups | OS4: [] (hidden)

See `option_mapping.json` for the full mapping payload.
