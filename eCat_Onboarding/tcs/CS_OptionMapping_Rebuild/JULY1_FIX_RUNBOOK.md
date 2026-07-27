# CopperSmith July 1 Fix Runbook

**Org:** `tcs` (org_id=291)  
**Situation:** Eric's FTP push (~July 1 3PM MDT) fixed GT36E/G option codes but left GT36W on generic codes, used wrong option display names, and replaced stories with unformatted bullet walls.

## Fix files (ready to upload)

| File | Source | What changed |
|------|--------|--------------|
| `options.csv.july1_fix` | Exported from **live DB** + Accessory Index names | 44 name corrections (WY36, QCM36, PFP36, etc.) |
| `option_groups.csv.july1_fix` | Exported from **live DB** | No structural changes — preserves Eric's WM059/CM166/PP048/DEC051 groups |
| `products.csv.july1_fix` | **Draft only** — see products caution below | GT36E/G/W OptionSet patches |
| `stories.csv.july1_fix` | Live stories + HTML bullet fixes | Georgetown (GT36E/G/W) restored to clean local text; 376 others get `<br>` before bullets |

## Upload order (mandatory)

```
1. options.csv
2. option_groups.csv   ← MUST re-run after options (options import nulls group membership)
3. products.csv
4. stories.csv
```

Rename `.july1_fix` files to standard names before FTP upload to `/data`, or upload via Admin Console in the order above.

### Products.csv caution

Eric's July 1 `products.csv` is on the server now; Kylor's local `products.csv` is **stale** (June 30). Do **not** upload `products.csv.july1_fix` wholesale — it could revert Eric's other product changes.

**Safe approach:** Download current `/data/products.csv` from FTP, then change **only GT36W**:

| Column | Change to |
|--------|-----------|
| OptionSet2 | `WM059` |
| OptionSet3 | `CM166` |
| OptionSet4 | `PP048` |
| OptionSet6 | `DEC051` |

GT36E and GT36G already have these groups on the live server. Only GT36W was missed.

## Verify after import

1. Admin → File Import Status — each file should show clean (no blue error links)
2. On iPad (sync on Wi-Fi):
   - **GT36W** → Wall mount shows **WY36** ($467), not WY ($292)
   - **GT36W** → Ceiling shows **QCM36** ($204), not QCM ($98)
   - **GT36E** → Option labels match Accessory Index ("Wall Yoke for GT36", etc.)
   - **GT36E** → Story text has readable paragraphs (not bullet wall)
   - Spot-check Arcadia, Biltmore, Turtle Friendly — bullets should line-break

## Do NOT upload Kylor's stale local `options.csv` / `option_groups.csv`

Those files predate Eric's July 1 push and are missing WM059, CM166, WY36, etc.

## Open question for Jordan

QCM36 label in Accessory Index says "for GT35 & AM35" but it's on GT36E ceiling mount. Confirm whether label or assignment should change.
