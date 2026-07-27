#!/usr/bin/env python3
"""Duplicate scan — BaseItemCode, option/group Code, UPC.

Every one of these is a uniqueness validation in the model
(`validates_uniqueness_of :code, scope: :organization_id` on Option and OptionGroup;
one row per BaseItemCode for products), so a duplicate is a rejected row rather than a
merge. Pebl shipped `MT_FAROEXT_GR` twice; CopperSmith shipped duplicate items.

UPC is a softer case: `upc_value` carries no uniqueness constraint, so two SKUs sharing
a UPC imports fine but is almost always a copy-paste error in the source. It warns.
"""
from ..core import fail, get, warn

CHECK = "dupes"
SUBSYSTEM = "core"


def _collect(rows, lookup, field):
    seen = {}
    for i, row in enumerate(rows, start=2):
        value = get(row, lookup, field)
        if value:
            seen.setdefault(value, []).append(i)
    return {v: lines for v, lines in seen.items() if len(lines) > 1}


def run(csv_file, rows, lookup, key_field, extra_unique=(), warn_fields=()):
    """Findings for duplicate key values.

    key_field / extra_unique are model-unique -> FAIL. warn_fields are advisory.
    """
    findings = []

    for field in (key_field, *extra_unique):
        if not field or field.lower() not in lookup:
            continue
        for value, lines in sorted(_collect(rows, lookup, field).items()):
            findings.append(fail(
                CHECK,
                f"DUPLICATE {field} '{value}' on rows {lines} — the model enforces "
                f"uniqueness per org, so the later row(s) are rejected",
            ))

    for field in warn_fields:
        if field.lower() not in lookup:
            continue
        for value, lines in sorted(_collect(rows, lookup, field).items()):
            findings.append(warn(
                CHECK,
                f"{field} '{value}' repeats on rows {lines} — not enforced by the "
                f"importer, but a shared {field} is usually a source copy-paste error",
            ))

    return findings
