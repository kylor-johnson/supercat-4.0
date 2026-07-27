# CopperSmith (tcs, org 291) — Option Mapping Admin Setup

## Prerequisites

1. **Import order**: `options.csv` → `option_groups.csv` → `products.csv` (standard eCat order)
2. **Request SuperCat Support** enable the Option Mapping feature for org 291 (still beta-gated)
3. Upload 3 mount-type option images to FTP `/option_images/`: `wall-mount.jpg`, `ceiling-mount.jpg`, `post-mount.jpg` (300x300px, square, no white space)

## Step 1: Update Option Type Labels

**Admin Console → Tools → Company Settings → Option Types**

Change labels from current 8-type layout to new 7-type layout:

| # | Old Label | New Label |
|---|-----------|-----------|
| 1 | Finish | Finish |
| 2 | Wall Mount | **Mount Type** |
| 3 | Wall Mount Accessories | **Mount Hardware** |
| 4 | Ceiling Mount | **Wall Accessories** |
| 5 | Post & Pier Mount | **Decorative** |
| 6 | Decorative | **Electric** |
| 7 | Electric | **Gas** |
| 8 | Gas | *(blank or remove)* |

Save changes.

## Step 2: Import Files via FTP

Upload to FTP `/data/` in this exact order:

1. `options.csv` (adds WALL, CEIL, POST options)
2. `option_groups.csv` (adds MT_WALL, MT_CEIL, MT_POST groups)
3. `products.csv` (restructured OptionSet columns)

Wait for each to process (check Tools → Admin Reports → File Import Status). All should import cleanly with no errors.

## Step 3: Configure Option Mapping

**Admin Console → Products → Option Mappings → New Option Mapping**

### Create Mapping: OptionSet2 (Mount Type)

1. Select Option Type: **OptionSet2: Mount Type**
2. Add connections:

#### Connection 1: MT_WALL → OptionSet3

- Option Group: **MT_WALL** (Wall Mount)
- Option Type: **OptionSet3** (Mount Hardware)
- Option Groups to show: **All WM### groups** (WM001 through WM164 — 158 groups total)

#### Connection 2: MT_WALL → OptionSet4

- Option Group: **MT_WALL** (Wall Mount)
- Option Type: **OptionSet4** (Wall Accessories)
- Option Groups to show: **All W### and WA### groups** (W028-W156, WA001-WA062 — 164 groups total)

#### Connection 3: MT_CEIL → OptionSet3

- Option Group: **MT_CEIL** (Ceiling Mount)
- Option Type: **OptionSet3** (Mount Hardware)
- Option Groups to show: **All CM### groups** (CM001 through CM164 — 164 groups total)

#### Connection 4: MT_POST → OptionSet3

- Option Group: **MT_POST** (Post & Pier Mount)
- Option Type: **OptionSet3** (Mount Hardware)
- Option Groups to show: **All PP### groups** (PP001 through PP164 — 152 groups total)

3. Click **Update Mapping** to save.

### Alternative: API/DB Injection

If configuring 638 group references manually through the UI is impractical, the mapping can be applied via the SuperCat API:

```
POST /api/v1/option_mappings
Content-Type: application/json

{
  "option_mapping": {
    "option_type_code": "OptionSet2",
    "mapping": <contents of option_mapping.json>
  }
}
```

Or ask SuperCat Support to insert the `option_mapping.json` payload directly into the `option_mappings` table for organization_id 291.

## Step 4: Verify on iPad

After sync:

1. **Open a product with all 3 mount types** (e.g., AS41E — Adam Street 41 Electric)
   - OS1 (Finish): See COPPER, BLK, BRZ, GRAY, CLEAR
   - OS2 (Mount Type): See Wall Mount, Ceiling Mount, Post & Pier Mount
   - Select **Wall Mount** →
     - OS3 shows ONLY wall mount brackets (Gooseneck, Moustache, Grand Harbor, etc.)
     - OS4 shows wall accessories (scrolls, hooks)
   - Go back, select **Ceiling Mount** →
     - OS3 shows ONLY ceiling options (Yoke, Chain, Stem, Pendant)
     - OS4 should be EMPTY (no wall accessories for ceiling)
   - Go back, select **Post & Pier** →
     - OS3 shows ONLY post/pier options (Fitters, Pier Mounts, Lamp Posts)
     - OS4 should be EMPTY (no wall accessories for post)

2. **Open a no-mount product** (e.g., 16WST — Wildlife Friendly Sconce)
   - OS1 (Finish): See COPPER, BLK, BRZ, GRAY, CLEAR
   - No mount type, no mount hardware, no wall accessories visible

3. **Open a ceiling-only product with decorative scrolls** (e.g., EB27E)
   - OS2 (Mount Type): See only Ceiling Mount
   - OS3: See ceiling hardware (CM072)
   - OS4: Empty (no wall accessories for ceiling)
   - OS5 (Decorative): Shows W072 scrolls (moved here since they're decorative, not mount-dependent)

## Behavioral Note: Empty Array Mapping

The mapping uses empty arrays `[]` for MT_CEIL → OptionSet4 and MT_POST → OptionSet4. This instructs the iPad to show NO groups in OS4 when ceiling or post is selected.

**If this doesn't work as expected** (i.e., the iPad shows all OS4 groups instead of hiding them), the fallback is:
1. Create a dummy option group `NONE` with a single hidden option
2. Replace `[]` with `['NONE']` in the mapping
3. The rep would see an empty-looking option set

Contact SuperCat Support to confirm empty-array behavior before go-live.

## Rollback

If this restructure doesn't work well:
1. Re-upload the original files from `CS_eCat_Rebuild/` (products.csv, options.csv, option_groups.csv)
2. Revert Option Type labels to the original 8-type layout
3. Delete the Option Mapping record in Admin Console

The original files are fully preserved in `CS_eCat_Rebuild/` and were never modified.
