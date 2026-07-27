#!/usr/bin/env python3
"""Restore the separate mount sections in products.csv (undo the Mount Type overhaul).

Background
----------
A prior pass consolidated the three mount families into a two-step
"Mount Type -> Mount Hardware" cascade:

    OS1 Finish | OS2 Mount Type (MT_*) | OS3 Mount Hardware (WM+CM+PP mixed)
    OS4 Wall Accessories | OS5 Decorative | OS6 Electric | OS7 Gas

Jordan/Eric approved the *separate-section* layout instead. This script rewrites
each product's OptionSet columns back to standalone mount sections and drops the
Mount Type selector:

    OS1 Finish | OS2 Wall Mount (WM) | OS3 Ceiling Mount (CM) | OS4 Post & Pier (PP)
    OS5 Wall Accessories | OS6 Decorative | OS7 Electric | OS8 Gas

products.csv is rewritten; the now-dead Mount Type artifacts are also removed so the
catalog is fully clean (no orphans):
  - options.csv      -> drops the WALL / CEIL / POST selector options
  - option_groups.csv-> drops the MT_WALL / MT_CEIL / MT_POST groups

The SKU builder needs no change: each product still has exactly one mount family, and
the relative suffix order (Finish -> Mount -> Wall Acc -> Decorative -> Electric/Gas)
is preserved, so configured item numbers are identical.

Because options.csv and option_groups.csv change, the re-import must run the full
mandatory order: options.csv -> option_groups.csv -> products.csv (importing options
nulls group membership, so option_groups must follow).

Platform-side changes (Admin Console, done separately):
  1. Option-type labels -> Finish / Wall Mount / Ceiling Mount / Post & Pier Mount /
     Wall Accessories / Decorative Accessories / Electric Options / Gas Options
  2. Remove the OptionSet2 (Mount Type) Option Mapping cascade.

Idempotent: if no MT_* codes remain in OptionSet2, it reports "already restored".
"""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

BASE = Path(__file__).parent
PRODUCTS = BASE / "products.csv"
OPTIONS = BASE / "options.csv"
OPTION_GROUPS = BASE / "option_groups.csv"
BACKUP = PRODUCTS.with_suffix(".csv.pre_mount_restore_bak")

OLD_OPTIONSET_COLS = [f"OptionSet{i}" for i in range(1, 8)]
NEW_OPTIONSET_COLS = [f"OptionSet{i}" for i in range(1, 9)]

# Dead Mount Type artifacts to remove once products no longer reference them.
MT_OPTION_CODES = {"WALL", "CEIL", "POST"}
MT_GROUP_CODES = {"MT_WALL", "MT_CEIL", "MT_POST"}


def split_codes(value: str) -> list[str]:
    return [c.strip() for c in (value or "").split(",") if c.strip()]


def restructure_products() -> bool:
    with PRODUCTS.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    # Idempotency guard: Mount Type set is the source layout marker.
    has_mt = any(
        code.startswith("MT") for r in rows for code in split_codes(r.get("OptionSet2"))
    )
    if not has_mt:
        print("products.csv: no MT_* in OptionSet2 — already restored, skipped.")
        return False

    shutil.copy(PRODUCTS, BACKUP)

    # Build new header: insert OptionSet8 right after OptionSet7.
    new_fields: list[str] = []
    for col in fields:
        new_fields.append(col)
        if col == "OptionSet7":
            new_fields.append("OptionSet8")

    n_changed = 0
    leftovers: list[tuple[str, str]] = []
    for r in rows:
        finish = r.get("OptionSet1", "")
        mount_hw = split_codes(r.get("OptionSet3"))
        wall_acc = r.get("OptionSet4", "")
        decorative = r.get("OptionSet5", "")
        electric = r.get("OptionSet6", "")
        gas = r.get("OptionSet7", "")

        wm = [c for c in mount_hw if c.startswith("WM")]
        cm = [c for c in mount_hw if c.startswith("CM")]
        pp = [c for c in mount_hw if c.startswith("PP")]
        other = [c for c in mount_hw if not c.startswith(("WM", "CM", "PP"))]
        for c in other:
            leftovers.append((r.get("BaseItemCode", "?"), c))

        had_content = any(
            split_codes(r.get(c)) for c in OLD_OPTIONSET_COLS
        )

        r["OptionSet1"] = finish
        r["OptionSet2"] = ",".join(wm)
        r["OptionSet3"] = ",".join(cm)
        r["OptionSet4"] = ",".join(pp)
        r["OptionSet5"] = wall_acc
        r["OptionSet6"] = decorative
        r["OptionSet7"] = electric
        r["OptionSet8"] = gas

        if had_content:
            n_changed += 1

    with PRODUCTS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=new_fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r.setdefault("OptionSet8", "")
            w.writerow(r)

    print(f"products.csv: restored separate mount sections on {n_changed} products "
          f"(backup {BACKUP.name}).")
    print("  Layout: OS1 Finish | OS2 Wall Mount | OS3 Ceiling Mount | OS4 Post & Pier "
          "| OS5 Wall Acc | OS6 Decorative | OS7 Electric | OS8 Gas")
    if leftovers:
        print(f"  WARNING: {len(leftovers)} mount-hardware code(s) not WM/CM/PP "
              f"(left out of mount sections):")
        for sku, code in leftovers[:20]:
            print(f"    {sku}: {code}")
    return True


def strip_rows(path: Path, key_col: str, drop_codes: set[str], label: str) -> bool:
    """Remove rows whose key_col value is in drop_codes. Idempotent."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    keep = [r for r in rows if (r.get(key_col) or "").strip() not in drop_codes]
    removed = len(rows) - len(keep)
    if removed == 0:
        print(f"{path.name}: no {label} rows present — already clean, skipped.")
        return False

    shutil.copy(path, path.with_suffix(path.suffix + ".pre_mount_restore_bak"))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(keep)
    print(f"{path.name}: removed {removed} {label} row(s); {len(keep)} remain.")
    return True


def main() -> int:
    changed = restructure_products()
    changed |= strip_rows(OPTIONS, "Code", MT_OPTION_CODES, "Mount Type option (WALL/CEIL/POST)")
    changed |= strip_rows(OPTION_GROUPS, "Code", MT_GROUP_CODES, "Mount Type group (MT_*)")
    if not changed:
        print("\nNothing to do — full revert already applied.")
    else:
        print("\nDone. Re-import in mandatory order: options.csv -> option_groups.csv -> products.csv")
        print("Also (Admin Console): set OptionSet1-8 labels + remove the OptionSet2 Mount Type mapping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
