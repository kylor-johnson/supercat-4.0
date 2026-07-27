# Mount Sections — Revert Writeup (for Eric)

**Goal:** restore the approved layout where **Wall Mount, Ceiling Mount, and Post & Pier
Mount each show as their own grouped section** alongside Wall Accessories, Decorative
Accessories, Electric Options, and Gas Options — and remove the "Mount Type" picker that
last week's update introduced.

## What changed last week (the "overhaul")

The mount families had been consolidated into a two-step cascade:

```
OS1 Finish | OS2 Mount Type (MT_*) | OS3 Mount Hardware (WM+CM+PP mixed)
OS4 Wall Acc | OS5 Decorative | OS6 Electric | OS7 Gas
```

So instead of three standalone mount sections, the rep first picked a **Mount Type**
(Wall/Ceiling/Post) and then the hardware list was filtered by an Option Mapping cascade.
That's what made the structure hard to follow.

## What it is now (reverted)

```
OS1 Finish | OS2 Wall Mount | OS3 Ceiling Mount | OS4 Post & Pier Mount
OS5 Wall Accessories | OS6 Decorative Accessories | OS7 Electric Options | OS8 Gas Options
```

Each populated OptionSet renders as its own section on the iPad configure screen.

## Eric's two questions, answered

1. **If we remove the Mount Type option set from the import, does eCat show Wall Mount /
   Wall Accessories / Ceiling Mount / Post & Pier as their own sections again?**
   Yes — sections are driven purely by which `OptionSetN` columns a product fills plus the
   Admin Option Type labels. Splitting the hardware back into separate OptionSet columns
   restores the separate sections.

2. **Is an eCat-side config change also needed?**
   Yes, two small Admin steps (below). The CSVs alone restore the data; Admin sets the
   section headings and removes the now-dead cascade.

## File changes (already applied in this folder)

- `products.csv` — mount hardware split back into separate columns:
  `OS2 Wall Mount (WM*) | OS3 Ceiling Mount (CM*) | OS4 Post & Pier (PP*)`, with Wall Acc /
  Decorative / Electric / Gas shifted to OS5–OS8. `OptionSet8` added to the header.
- `options.csv` — removed the `WALL`, `CEIL`, `POST` Mount Type selector options.
- `option_groups.csv` — removed the `MT_WALL`, `MT_CEIL`, `MT_POST` groups.

Reproducible/idempotent via `restore_mount_sections.py` (backs up each file first).
Referential integrity verified: every group a product references exists, and every option a
group references exists (0 dangling refs).

## SKU builder — no change needed (verified)

The live SKU script (org `tcs`, id 291) builds the configured item number as
`itemNumber` + each **selected option code**, sorted by the number in `optionTypeCode`
(OptionSet1→8), skipping the default finish code `COPPER` and the legacy `WALL/CEIL/POST`
routing codes:

```js
function main(orderItem) {
  var DEFAULT_FINISH = "COPPER";
  var SKIP_CODES = {"WALL": true, "CEIL": true, "POST": true};
  function setIndex(o){ var m=/(\d+)$/.exec(o.optionTypeCode||""); return m?parseInt(m[1],10):999; }
  var opts = (orderItem.options||[]).slice().sort(function(a,b){return setIndex(a)-setIndex(b);});
  var suffixes = [];
  for (var i=0;i<opts.length;i++){ var code=opts[i].code;
    if(!code) continue; if(code===DEFAULT_FINISH) continue; if(SKIP_CODES[code]) continue;
    suffixes.push(code); }
  return [orderItem.itemNumber].concat(suffixes).join("-");
}
```

Because the script keys off the OptionSet **order** and the selected option **codes** — not
on a "Mount Type" selection — the revert needs no script edit. For any single valid
selection the new separate-section layout produces a **byte-identical** SKU to the old
cascade layout. Verified with a faithful port over the live script: **1222/1222 cases pass**,
including **790/790 old-vs-new single-mount equivalence** checks and a 425-product walk with
zero null/empty/duplicate SKUs. The `SKIP_CODES` for `WALL/CEIL/POST` are now dead but
harmless (those codes were removed). The live SKU Builder can be locked as planned.

## Mount selection behavior — matches the source

The June **Master Sheet E+G** structures mounts as **separate sections** — its own column
groups are `WALL MOUNT`, `CEILING MOUNT`, `POST & PIER MOUNT`, and `WALL ACCESSORIES (only
available on standard wall mount)`. The restored layout matches that one-to-one. Each product
is populated with the mount families it actually offers, e.g.:

- `AS41G` — 9 wall + 7 wall-acc + 3 ceiling + 10 post (all sections)
- `AOB28E` — 0 wall + 1 ceiling + 7 post (no wall section)
- `16WST` — finish only (no mount sections)

So a lantern that can be mounted three ways legitimately shows three mount sections; the rep
picks the one the customer wants. The source does **not** define a hard "exactly one mount"
rule, and the SKU script correctly appends whatever is selected. (If a rep selected hardware
in two sections the script would emit both, e.g. `AS41G-WY-CY05` — a rep mis-click, not a data
or script defect. Optional belt-and-suspenders: make OS2/OS3/OS4 mutually exclusive via Admin
Option Mapping. Not required by the source.)

### The real dependency to rebuild: Wall Accessories → Wall Mount
The source explicitly notes **Wall Accessories are only available on standard wall mount**.
That is a genuine dependent-option relationship: the OS5 (Wall Accessories) section should be
gated on a (standard) Wall Mount selection in OS2. This is the kind of dependency to rebuild
in Admin Option Mapping (parent OS2 → child OS5), per the client's SKU Builder + Rules sheet.

### Pre-existing finish note (not caused by the revert)
The script omits a finish from the SKU **only** when its code is exactly `COPPER`. Products
whose default finish is a different code (e.g. Antique Brass `BRASS` in `FIN002`, used by the
`AOB*` family) will include that finish code in the SKU (`AOB28E-BRASS-...`). If the rule
should be "omit each product's default finish," that's a separate decision about the locked
script — flag it with Jordan; it predates this revert.

## Admin Console steps (do BEFORE re-import)

1. **Option Types → labels:**
   `1 Finish · 2 Wall Mount · 3 Ceiling Mount · 4 Post & Pier Mount · 5 Wall Accessories ·
   6 Decorative Accessories · 7 Electric Options · 8 Gas Options`
2. **Option Mapping → delete the OptionSet2 (Mount Type) cascade** (it now points at the
   deleted `MT_*` groups).

## Re-import order (all three files changed)

Importing `options.csv` hard-deletes options and **nulls group membership**, so
`option_groups.csv` must follow it:

```
options.csv → option_groups.csv → products.csv
```

(`upload_image_fixes.sh data` already enforces this order.)
