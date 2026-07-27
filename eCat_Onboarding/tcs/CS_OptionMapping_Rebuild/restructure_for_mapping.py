#!/usr/bin/env python3
"""
CopperSmith eCat — Option Mapping Restructure

Transforms the existing 8-OptionSet architecture into a 7-set layout that
supports eCat Option Mapping with a Mount Type selector cascading to
mount hardware and wall accessories.

Old layout:
  OS1=Finish | OS2=Wall Mount | OS3=Wall Accessories | OS4=Ceiling Mount
  OS5=Post & Pier | OS6=Decorative | OS7=Electric | OS8=Gas

New layout:
  OS1=Finish | OS2=Mount Type (NEW) | OS3=Mount Hardware (merged OS2+OS4+OS5)
  OS4=Wall Accessories (old OS3) | OS5=Decorative (old OS6)
  OS6=Electric (old OS7) | OS7=Gas (old OS8) | OS8=(empty)
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent

OPTIONS_FILE = BASE / "options.csv"
GROUPS_FILE = BASE / "option_groups.csv"
PRODUCTS_FILE = BASE / "products.csv"
MAPPING_FILE = BASE / "option_mapping.json"
REPORT_FILE = BASE / "RESTRUCTURE_REPORT.md"

# Mount type option codes and group codes
MT_OPTIONS = [
    {"Code": "WALL", "Name": "Wall Mount", "SortValue": "01", "Description": "Mount Type", "ImageName": "wall-mount.jpg", "PriceAddend": "", "PriceFactor": ""},
    {"Code": "CEIL", "Name": "Ceiling Mount", "SortValue": "02", "Description": "Mount Type", "ImageName": "ceiling-mount.jpg", "PriceAddend": "", "PriceFactor": ""},
    {"Code": "POST", "Name": "Post & Pier Mount", "SortValue": "03", "Description": "Mount Type", "ImageName": "post-mount.jpg", "PriceAddend": "", "PriceFactor": ""},
]

MT_GROUPS = [
    {"Code": "MT_WALL", "Name": "Wall Mount", "Options": "WALL", "PriceAddend": "", "PriceFactor": ""},
    {"Code": "MT_CEIL", "Name": "Ceiling Mount", "Options": "CEIL", "PriceAddend": "", "PriceFactor": ""},
    {"Code": "MT_POST", "Name": "Post & Pier Mount", "Options": "POST", "PriceAddend": "", "PriceFactor": ""},
]

# Prefixes that identify which mount family an option group belongs to
WALL_MOUNT_PREFIXES = ("WM",)
CEILING_MOUNT_PREFIXES = ("CM",)
POST_PIER_PREFIXES = ("PP",)
WALL_ACCESSORY_PREFIXES = ("W", "WA")
DECORATIVE_PREFIXES = ("D", "DEC")
ELECTRIC_PREFIXES = ("ELE", "GE")
GAS_PREFIXES = ("GAS",)


def classify_group(code: str) -> str:
    """Classify an option group code by its mount/accessory family."""
    if code.startswith("WM"):
        return "wall_mount"
    if code.startswith("CM"):
        return "ceiling_mount"
    if code.startswith("PP"):
        return "post_pier"
    if code.startswith("WA"):
        return "wall_accessory"
    if code.startswith("W") and code[1:2].isdigit():
        return "wall_accessory"
    if code.startswith("DEC"):
        return "decorative"
    if code.startswith("D") and code[1:2].isdigit():
        return "decorative"
    if code.startswith("ELE"):
        return "electric"
    if code.startswith("GAS"):
        return "gas"
    if code.startswith("GE"):
        return "gas_electric_old"
    if code.startswith("FIN"):
        return "finish"
    if code.startswith("MT_"):
        return "mount_type"
    return "unknown"


def step1_update_options():
    """Append mount type options to options.csv."""
    existing_codes = set()
    with open(OPTIONS_FILE) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_codes.add(row["Code"])

    added = []
    with open(OPTIONS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for opt in MT_OPTIONS:
            if opt["Code"] not in existing_codes:
                writer.writerow(opt)
                added.append(opt["Code"])

    return added


def step2_update_groups():
    """Append mount type groups to option_groups.csv."""
    existing_codes = set()
    with open(GROUPS_FILE) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_codes.add(row["Code"])

    added = []
    with open(GROUPS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for grp in MT_GROUPS:
            if grp["Code"] not in existing_codes:
                writer.writerow(grp)
                added.append(grp["Code"])

    return added


def step3_restructure_products():
    """
    Remap OptionSet columns in products.csv.

    Old: OS1=Finish, OS2=WallMount, OS3=WallAcc, OS4=Ceiling, OS5=Post, OS6=Deco, OS7=Elec, OS8=Gas
    New: OS1=Finish, OS2=MountType, OS3=MountHardware, OS4=WallAcc, OS5=Deco, OS6=Elec, OS7=Gas, OS8=empty
    """
    rows = []
    with open(PRODUCTS_FILE) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(dict(row))

    stats = {
        "total": len(rows),
        "with_mounts": 0,
        "without_mounts": 0,
        "mount_combos": defaultdict(int),
        "edge_cases": [],
    }

    transformed = []
    for row in rows:
        old_os1 = row.get("OptionSet1", "").strip()
        old_os1r = row.get("OptionSet1Required", "").strip()
        old_os2 = row.get("OptionSet2", "").strip()  # Wall Mount
        old_os3 = row.get("OptionSet3", "").strip()  # Wall Accessories
        old_os4 = row.get("OptionSet4", "").strip()  # Ceiling Mount
        old_os5 = row.get("OptionSet5", "").strip()  # Post & Pier
        old_os6 = row.get("OptionSet6", "").strip()  # Decorative
        old_os7 = row.get("OptionSet7", "").strip()  # Electric
        old_os8 = row.get("OptionSet8", "").strip()  # Gas

        has_wall = bool(old_os2)
        has_ceiling = bool(old_os4)
        has_post = bool(old_os5)
        has_wall_acc = bool(old_os3)
        has_any_mount = has_wall or has_ceiling or has_post

        # Edge case: wall accessories without wall mount hardware
        # If product has wall accessories but no wall mount bracket, those accessories
        # are decorative (not mount-dependent). Move them to Decorative (OS5) so they
        # aren't hidden when the mapping filters OS4 by mount type.
        wall_acc_is_decorative = has_wall_acc and not has_wall
        if wall_acc_is_decorative:
            stats["edge_cases"].append(
                f"{row['BaseItemCode']}: WallAcc ({old_os3}) without wall mount → moved to Decorative (OS5)"
            )

        # Edge case: wall accessories without ANY mount at all implies wall context
        if has_wall_acc and not has_any_mount:
            has_wall = True
            stats["edge_cases"].append(f"{row['BaseItemCode']}: WallAcc without any mount → added MT_WALL")

        # Build new OS2 (Mount Type)
        mt_groups = []
        if has_wall:
            mt_groups.append("MT_WALL")
        if has_ceiling:
            mt_groups.append("MT_CEIL")
        if has_post:
            mt_groups.append("MT_POST")

        # Build new OS3 (Mount Hardware = merge old OS2 + OS4 + OS5)
        mount_hardware_parts = []
        if old_os2:
            mount_hardware_parts.append(old_os2)
        if old_os4:
            mount_hardware_parts.append(old_os4)
        if old_os5:
            mount_hardware_parts.append(old_os5)

        # Track stats
        combo = ("W" if has_wall else "-") + ("C" if has_ceiling else "-") + ("P" if has_post else "-")
        if has_any_mount or has_wall_acc:
            stats["with_mounts"] += 1
            stats["mount_combos"][combo] += 1
        else:
            stats["without_mounts"] += 1

        # Write new values
        new_os2 = ",".join(mt_groups) if mt_groups else ""
        new_os2r = "Y" if mt_groups else ""
        new_os3 = ",".join(mount_hardware_parts) if mount_hardware_parts else ""

        # Wall accessories: if the product has wall mount hardware, put in OS4 (filtered by mapping).
        # If it has wall accessories but NO wall mount hardware (decorative context only), merge into OS5.
        if wall_acc_is_decorative:
            new_os4 = ""
            # Merge wall acc into decorative: combine old_os3 with old_os6
            deco_parts = []
            if old_os3:
                deco_parts.append(old_os3)
            if old_os6:
                deco_parts.append(old_os6)
            new_os5 = ",".join(deco_parts) if deco_parts else ""
        else:
            new_os4 = old_os3  # Wall Accessories
            new_os5 = old_os6  # Decorative

        new_os6 = old_os7  # Electric
        new_os7 = old_os8  # Gas
        new_os8 = ""

        row["OptionSet1"] = old_os1
        row["OptionSet1Required"] = old_os1r
        row["OptionSet2"] = new_os2
        row["OptionSet3"] = new_os3
        row["OptionSet4"] = new_os4
        row["OptionSet5"] = new_os5
        row["OptionSet6"] = new_os6
        row["OptionSet7"] = new_os7
        row["OptionSet8"] = new_os8

        transformed.append(row)

    with open(PRODUCTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed)

    return stats


def step4_generate_mapping():
    """
    Generate option_mapping.json for Admin Console configuration.

    Structure: When an option from MT_WALL/MT_CEIL/MT_POST is selected in OS2,
    filter OS3 (Mount Hardware) and OS4 (Wall Accessories) accordingly.
    """
    # Read all group codes from option_groups.csv
    all_groups = {}
    with open(GROUPS_FILE) as f:
        for row in csv.DictReader(f):
            all_groups[row["Code"]] = classify_group(row["Code"])

    wall_mount_groups = sorted(c for c, t in all_groups.items() if t == "wall_mount")
    ceiling_mount_groups = sorted(c for c, t in all_groups.items() if t == "ceiling_mount")
    post_pier_groups = sorted(c for c, t in all_groups.items() if t == "post_pier")
    wall_acc_groups = sorted(c for c, t in all_groups.items() if t == "wall_accessory")

    mapping = {
        "option_type_code": "OptionSet2",
        "mapping": {
            "MT_WALL": {
                "OptionSet3": wall_mount_groups,
                "OptionSet4": wall_acc_groups,
            },
            "MT_CEIL": {
                "OptionSet3": ceiling_mount_groups,
                "OptionSet4": [],
            },
            "MT_POST": {
                "OptionSet3": post_pier_groups,
                "OptionSet4": [],
            },
        },
    }

    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

    return {
        "wall_mount_groups": len(wall_mount_groups),
        "ceiling_mount_groups": len(ceiling_mount_groups),
        "post_pier_groups": len(post_pier_groups),
        "wall_acc_groups": len(wall_acc_groups),
    }


def step5_validate():
    """Cross-check all group references in products against option_groups."""
    # Load all valid group codes
    valid_groups = set()
    with open(GROUPS_FILE) as f:
        for row in csv.DictReader(f):
            valid_groups.add(row["Code"])

    # Load all valid option codes
    valid_options = set()
    with open(OPTIONS_FILE) as f:
        for row in csv.DictReader(f):
            valid_options.add(row["Code"])

    # Check option codes in groups
    group_option_errors = []
    with open(GROUPS_FILE) as f:
        for row in csv.DictReader(f):
            opts = [o.strip() for o in row["Options"].split(",") if o.strip()]
            for o in opts:
                if o not in valid_options:
                    group_option_errors.append(f"Group {row['Code']}: option '{o}' not found")

    # Check group codes in products
    product_group_errors = []
    product_count = 0
    with open(PRODUCTS_FILE) as f:
        for row in csv.DictReader(f):
            product_count += 1
            for i in range(1, 9):
                val = row.get(f"OptionSet{i}", "").strip()
                if val:
                    codes = [c.strip() for c in val.split(",")]
                    for c in codes:
                        if c not in valid_groups:
                            product_group_errors.append(
                                f"Product {row['BaseItemCode']} OS{i}: group '{c}' not found"
                            )

    return {
        "product_count": product_count,
        "valid_groups_count": len(valid_groups),
        "valid_options_count": len(valid_options),
        "group_option_errors": group_option_errors,
        "product_group_errors": product_group_errors,
    }


def write_report(options_added, groups_added, product_stats, mapping_stats, validation):
    """Write the restructure report."""
    lines = [
        "# CopperSmith Option Mapping Restructure — Report",
        "",
        "## Summary",
        "",
        f"- Options added: {options_added}",
        f"- Groups added: {groups_added}",
        f"- Products transformed: {product_stats['total']}",
        f"  - With mounts: {product_stats['with_mounts']}",
        f"  - Without mounts (no change to mount logic): {product_stats['without_mounts']}",
        "",
        "## Mount Type Combinations",
        "",
        "| Combo | Count |",
        "|-------|-------|",
    ]
    for combo, count in sorted(product_stats["mount_combos"].items(), key=lambda x: -x[1]):
        labels = []
        if combo[0] == "W":
            labels.append("Wall")
        if combo[1] == "C":
            labels.append("Ceiling")
        if combo[2] == "P":
            labels.append("Post")
        lines.append(f"| {combo} ({' + '.join(labels)}) | {count} |")
    lines.append("")

    if product_stats["edge_cases"]:
        lines.append("## Edge Cases")
        lines.append("")
        for ec in product_stats["edge_cases"]:
            lines.append(f"- {ec}")
        lines.append("")

    lines.extend([
        "## Option Mapping Stats",
        "",
        f"- Wall Mount groups in mapping: {mapping_stats['wall_mount_groups']}",
        f"- Ceiling Mount groups in mapping: {mapping_stats['ceiling_mount_groups']}",
        f"- Post & Pier groups in mapping: {mapping_stats['post_pier_groups']}",
        f"- Wall Accessory groups in mapping: {mapping_stats['wall_acc_groups']}",
        "",
        "## Validation",
        "",
        f"- Total products: {validation['product_count']}",
        f"- Total valid groups: {validation['valid_groups_count']}",
        f"- Total valid options: {validation['valid_options_count']}",
        "",
    ])

    if validation["group_option_errors"]:
        lines.append(f"### Option Code Errors in Groups ({len(validation['group_option_errors'])})")
        lines.append("")
        for err in validation["group_option_errors"][:20]:
            lines.append(f"- {err}")
        if len(validation["group_option_errors"]) > 20:
            lines.append(f"- ... and {len(validation['group_option_errors']) - 20} more")
        lines.append("")
    else:
        lines.append("- All option codes in groups are valid")
        lines.append("")

    if validation["product_group_errors"]:
        lines.append(f"### Group Code Errors in Products ({len(validation['product_group_errors'])})")
        lines.append("")
        for err in validation["product_group_errors"][:20]:
            lines.append(f"- {err}")
        if len(validation["product_group_errors"]) > 20:
            lines.append(f"- ... and {len(validation['product_group_errors']) - 20} more")
        lines.append("")
    else:
        lines.append("- All group codes in products are valid")
        lines.append("")

    lines.extend([
        "## New OptionSet Layout",
        "",
        "| OptionSet | Label | Content |",
        "|-----------|-------|---------|",
        "| OS1 | Finish | FIN001 or FIN002 (Required) |",
        "| OS2 | Mount Type | MT_WALL, MT_CEIL, MT_POST (Required for mount products) |",
        "| OS3 | Mount Hardware | Merged WM###, CM###, PP### groups |",
        "| OS4 | Wall Accessories | W### / WA### groups (filtered by OS2 mapping) |",
        "| OS5 | Decorative | D### / DEC### groups |",
        "| OS6 | Electric | ELE### / GE### groups |",
        "| OS7 | Gas | GAS### / GE### groups |",
        "| OS8 | (empty) | — |",
        "",
        "## Option Mapping (Admin Console)",
        "",
        "One mapping record on OptionSet2:",
        "",
        "- **MT_WALL** → OS3: wall mount groups | OS4: wall accessory groups",
        "- **MT_CEIL** → OS3: ceiling mount groups | OS4: [] (hidden)",
        "- **MT_POST** → OS3: post/pier groups | OS4: [] (hidden)",
        "",
        "See `option_mapping.json` for the full mapping payload.",
    ])

    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    print("=" * 60)
    print("CopperSmith Option Mapping Restructure")
    print("=" * 60)
    print()

    print("[1/5] Adding mount type options...")
    options_added = step1_update_options()
    print(f"      Added: {options_added}")

    print("[2/5] Adding mount type groups...")
    groups_added = step2_update_groups()
    print(f"      Added: {groups_added}")

    print("[3/5] Restructuring products.csv OptionSet columns...")
    product_stats = step3_restructure_products()
    print(f"      {product_stats['total']} products transformed")
    print(f"      {product_stats['with_mounts']} with mounts, {product_stats['without_mounts']} without")

    print("[4/5] Generating option_mapping.json...")
    mapping_stats = step4_generate_mapping()
    print(f"      Wall Mount groups: {mapping_stats['wall_mount_groups']}")
    print(f"      Ceiling Mount groups: {mapping_stats['ceiling_mount_groups']}")
    print(f"      Post & Pier groups: {mapping_stats['post_pier_groups']}")
    print(f"      Wall Accessory groups: {mapping_stats['wall_acc_groups']}")

    print("[5/5] Validating...")
    validation = step5_validate()
    errors = len(validation["group_option_errors"]) + len(validation["product_group_errors"])
    if errors:
        print(f"      WARNING: {errors} validation errors found")
    else:
        print("      All references valid")

    print()
    print("Writing report...")
    write_report(options_added, groups_added, product_stats, mapping_stats, validation)
    print(f"      Report: {REPORT_FILE}")
    print(f"      Mapping: {MAPPING_FILE}")
    print()
    print("Done.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
