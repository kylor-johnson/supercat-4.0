#!/usr/bin/env python3
"""Blank-stays-blank — a blank source image cell is a decision, not a defect.

The standing client rule, verbatim: *"If an image isn't linked for that specific SKU,
please don't make assumptions that a similar SKU image link will suffice... Just leave it
blank."*

Inheriting a sibling's image violates it, and it is mechanically checkable in two
directions:

1. A SKU blank at source must be blank in the output.
2. No two SKUs may share an image filename unless the **source** shares it.

Both need the source file to judge, which is the point — this is the one image check that
asserts against an external authority rather than against the transform's own rules. That
distinction is exactly what a validator at one client got wrong when it asserted
`ShortDesc == source[:15]` and certified its own bug as passing.

Without a source file the shared-filename scan still runs, but it can only warn: a
genuinely shared hero is legitimate when the source shares it.
"""
from ..core import fail, get, load_rows, split_codes, warn

CHECK = "blank-stays-blank"
SUBSYSTEM = "images"

MAX_LISTED = 15


def _image_map(rows, lookup, key_field, image_field):
    out = {}
    for row in rows:
        key = get(row, lookup, key_field)
        if key:
            out[key] = split_codes(get(row, lookup, image_field))
    return out


def run(rows, lookup, source_path=None, key_field="BaseItemCode",
        image_field="ImageFileName", source_key_field=None, source_image_field=None):
    if image_field.lower() not in lookup:
        return [warn(CHECK, f"no {image_field} column — nothing to compare")]

    output = _image_map(rows, lookup, key_field, image_field)
    findings = []

    shared = {}
    for key, names in output.items():
        for name in names:
            shared.setdefault(name, []).append(key)
    shared = {n: sorted(k) for n, k in shared.items() if len(k) > 1}

    if source_path is None:
        findings.append(warn(
            CHECK,
            "no --source supplied: could not verify that SKUs blank at source stayed "
            "blank. This is the only check that compares the output against the client's "
            "own file rather than against our own transform",
        ))
        for name, keys in sorted(shared.items())[:MAX_LISTED]:
            findings.append(warn(
                CHECK,
                f"image '{name}' is shared by {len(keys)} SKUs ({', '.join(keys[:5])}"
                f"{'...' if len(keys) > 5 else ''}) — legitimate only if the source "
                f"shares it too; pass --source to decide",
            ))
        return findings

    src_rows, src_lookup = load_rows(source_path)
    src_key = source_key_field or key_field
    src_image = source_image_field or image_field
    if src_key.lower() not in src_lookup:
        return [warn(
            CHECK,
            f"source {source_path} has no '{src_key}' column — cannot align rows. Pass "
            f"--source-key to name the source's SKU column",
        )]
    if src_image.lower() not in src_lookup:
        return [warn(
            CHECK,
            f"source {source_path} has no '{src_image}' column — cannot compare image "
            f"cells. Pass --source-image-field to name it",
        )]

    source = _image_map(src_rows, src_lookup, src_key, src_image)

    invented = [
        (key, names) for key, names in sorted(output.items())
        if key in source and not source[key] and names
    ]
    for key, names in invented[:MAX_LISTED]:
        findings.append(fail(
            CHECK,
            f"blank at source but '{', '.join(names)}' in the output — the client's "
            f"standing rule is to leave it blank rather than borrow a similar SKU's image",
            key,
        ))
    if len(invented) > MAX_LISTED:
        findings.append(fail(
            CHECK, f"...and {len(invented) - MAX_LISTED} more SKU(s) given an image they "
                   f"do not have at source"))

    src_shared = {}
    for key, names in source.items():
        for name in names:
            src_shared.setdefault(name, []).append(key)

    for name, keys in sorted(shared.items()):
        src_keys = set(src_shared.get(name, []))
        if not src_keys >= set(keys):
            findings.append(fail(
                CHECK,
                f"image '{name}' is shared by {len(keys)} SKUs in the output "
                f"({', '.join(keys[:5])}{'...' if len(keys) > 5 else ''}) but the source "
                f"assigns it to {sorted(src_keys) or 'none of them'} — sibling-image "
                f"inheritance",
            ))

    dropped = [
        key for key, names in sorted(source.items())
        if names and key in output and not output[key]
    ]
    if dropped:
        findings.append(warn(
            CHECK,
            f"{len(dropped)} SKU(s) have an image at source but none in the output: "
            f"{', '.join(dropped[:5])}{'...' if len(dropped) > 5 else ''}",
        ))

    if not findings:
        findings.append(warn(
            CHECK,
            f"all {len(output)} SKU(s) match the source's blank/non-blank pattern and no "
            f"image is shared beyond what the source shares",
        ))
    return findings
