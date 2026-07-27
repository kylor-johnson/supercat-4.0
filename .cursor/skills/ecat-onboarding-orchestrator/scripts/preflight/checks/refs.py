#!/usr/bin/env python3
"""Cross-file referential integrity (IMPLEMENTATION_PLAN.md 4.2).

Live orphan inventory rows at the time of writing: leg 247, libco 83, tcd 30, mali 11.
Legrand's 2026-07-14 inventory import produced 24 KB of `Product not found, record
ignored` warnings — the rows silently did not import, so the file claimed to set stock
levels it never set.

Tiering follows what the importer actually does with each dangling reference:

| reference | importer behavior | tier |
|---|---|---|
| `inventory.BaseItemCode` not a product | row ignored entirely | FAIL |
| `stories.BaseItemCode` not a product | story silently lost | FAIL |
| `RelatedItems` target missing | warns, drops just that link | WARNING |
| `OptionSet*` group missing | product references a nonexistent group | FAIL |
| group member not in `options.csv` | OptionGroup validation error | FAIL |

`RelatedItems` is a WARNING because `transform_related_items` partitions the list and
emits `add_error(:warning, "Related item: 'X' not found")`, keeping the product.
"""
from ..core import fail, get, split_codes, warn

CHECK = "refs"
SUBSYSTEM = "core"

MAX_LISTED = 10
OPTION_SET_FIELDS = [f"OptionSet{i}" for i in range(1, 6)]


def _summarize(findings_ctor, check, label, offenders, total_rows, detail):
    """One finding per offender up to MAX_LISTED, then a single roll-up line."""
    out = []
    listed = offenders[:MAX_LISTED]
    for where, value in listed:
        out.append(findings_ctor(check, f"{label} '{value}' {detail}", where))
    if len(offenders) > MAX_LISTED:
        out.append(findings_ctor(
            check,
            f"...and {len(offenders) - MAX_LISTED} more ({len(offenders)} of "
            f"{total_rows} rows total). Full list suppressed — fix the join, not the "
            f"individual rows",
        ))
    return out


def product_codes(rows, lookup):
    return {get(r, lookup, "BaseItemCode") for r in rows if get(r, lookup, "BaseItemCode")}


def check_child_file(csv_file, rows, lookup, products, field="BaseItemCode"):
    """inventory.csv / stories.csv keys must exist in products.csv."""
    if not products:
        return []
    offenders = []
    for i, row in enumerate(rows, start=2):
        value = get(row, lookup, field)
        if value and value not in products:
            offenders.append((f"row {i}", value))
    if not offenders:
        return []
    detail = (
        "is not in products.csv — the importer logs 'Product not found, record "
        "ignored' and the row does NOT import"
    )
    return _summarize(fail, CHECK, field, offenders, len(rows), detail)


def check_related_items(rows, lookup, products):
    """RelatedItems targets should resolve; the importer warns and drops the link."""
    if "relateditems" not in lookup or not products:
        return []
    offenders = []
    for i, row in enumerate(rows, start=2):
        bic = get(row, lookup, "BaseItemCode")
        for target in split_codes(get(row, lookup, "RelatedItems")):
            if target not in products:
                offenders.append((f"row {i} ({bic})", target))
    if not offenders:
        return []
    detail = (
        "is not an item in this file — importer warns \"Related item: not found\" and "
        "drops the link (the product still imports)"
    )
    return _summarize(warn, CHECK, "RelatedItems target", offenders, len(rows), detail)


def check_option_sets(rows, lookup, group_codes):
    """Every OptionSet* value must name a group defined in option_groups.csv."""
    if group_codes is None:
        return []
    offenders = []
    for i, row in enumerate(rows, start=2):
        bic = get(row, lookup, "BaseItemCode")
        for field in OPTION_SET_FIELDS:
            if field.lower() not in lookup:
                continue
            value = get(row, lookup, field)
            if value and value.lower() not in group_codes:
                offenders.append((f"row {i} ({bic}) {field}", value))
    if not offenders:
        return []
    return _summarize(
        fail, CHECK, "OptionSet group", offenders, len(rows),
        "is not defined in option_groups.csv",
    )


def check_group_membership(rows, lookup, option_codes):
    """option_groups.csv members must exist in options.csv.

    Group membership is newline-separated in the Options column, NOT comma-separated —
    commas produce one giant invalid option code.
    """
    if option_codes is None:
        return []
    offenders = []
    for i, row in enumerate(rows, start=2):
        code = get(row, lookup, "Code")
        raw = get(row, lookup, "Options")
        members = [m.strip() for m in raw.replace("\r", "\n").split("\n") if m.strip()]
        if len(members) == 1 and "," in members[0]:
            offenders.append((f"row {i} ({code})", members[0][:40] + "..."))
            continue
        for member in members:
            if member.lower() not in option_codes:
                offenders.append((f"row {i} ({code})", member))
    if not offenders:
        return []
    return _summarize(
        fail, CHECK, "option group member", offenders, len(rows),
        "is not in options.csv (membership is NEWLINE-separated, not comma-separated)",
    )
