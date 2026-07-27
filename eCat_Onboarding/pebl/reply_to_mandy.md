**Subject:** Re: Option mapping files — updates applied

Hi Mandy,

Thank you for sending the files and the mapping spreadsheet — that was exactly what we needed.

We’ve reviewed everything and prepared corrected import files. **Please upload these to FileZilla `/data`** (replacing the current files), then import in this order:

1. **`options.csv`**
2. **`option_groups.csv`**
3. **`products.csv`**

Leave the app/import running on each step until it completes, then sync the iPad on Wi‑Fi.

---

### What we fixed

**Options import (was failing)**  
Three ceramic option codes were over the 15-character system limit. We shortened them:

- `DGREEN_GLAZED_CER` → `DGREEN_GLAZ_CER`
- `WBROWN_GLAZED_CER` → `WBROWN_GLAZ_CER`
- `OCHRE_GLAZED_CER` → `OCHRE_GLAZ_CER`

**Option groups (expanded from your mapping sheet)**  
We kept your existing Haven/Wave groups and added new groups for the new collections (frame colors, ceramics, cushions). Ceramic/cushion **price differences** from your spreadsheet are applied via **option group price addends** (not matrix pricing), for example:

- Wave ceramic coffee table 150×85: **-$70**
- Wave ceramic coffee table 100×85: **-$16**
- Albatros extension table: **-$32**
- Newport sofa cushion UV931609: **-$50**
- Haven Alu. sunlounger Jalousie 160: **+$10**

**Products file**  
We replaced the placeholder group names (`FRAMECOLOR`, `MATCOLOR`, `CUSHFABRIC`) with real option group codes and filled in missing material/cushion groups for Hilo, Bistro, Tube, Albatros, Orbit, Horizon, Newport, Levl, Bold, and Haven Alu. neo — based on your **ecat-options mapping** workbook.

**Option Mapping (Admin Console)**  
We prepared the extended Frame Color → Material/Cushion mapping for the new collections (same approach as Haven/Wave). We will apply this in Admin Console after your imports complete.

---

### Assumptions we made (please confirm)

1. **Tube ceramic table:** Dark Brown frame → Offwhite ceramic top.
2. **Newport 3-seater:** Teak frame with cushion choices UV931609 (-$50) and Lajolla 185.
3. **Orbit sofas:** Mocha frame + cushion 1763 only (no separate material option).
4. **Orbit coffee tables:** Teak frame + Travertine top only.
5. **Bold coffee tables:** Frame color only (7 colors from your sheet) — no material/cushion options.
6. **Price deltas** are applied against each product’s base net price when that option group is selected.

If any of these don’t match your intent, let us know and we can adjust quickly.

---

After importing, please test a few items on the iPad (e.g. Wave ceramic coffee table 150×85, Newport 3-seater, Orbit 1-seater) and send screenshots if anything looks off.

Thanks,  
Kylor
