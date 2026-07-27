#!/usr/bin/env python3
"""Two-tier field-length checking against code-derived limits.

The numbers come from `limits_generated.py`, which is produced by
`tools/gen_limits.py` out of supercat_server. Nothing here may hard-code a limit —
IMPLEMENTATION_PLAN.md 4.1 is the story of what happens when a validator asserts
against the transform's own rules instead of an external authority.

Two tiers, because the importer has two:

* `Product::ATTRS_TO_TRUNCATE` — six fields warn and silently truncate. A 300-char
  `LongDesc` is survivable, so overflow here is a WARNING.
* everything else — a validation error rejects the row. A 16-char option code is not
  survivable, which is why 16 of Pebl's 24 option groups died in one import.

Plus an advisory tier for thresholds that live in importer logic rather than in
`ATTR_LENGTHS` (`BillToCode` warns above 15 while the model errors above 20).
"""
import re

from . import limits_generated as gen
from .core import fail, get, warn

LIMITS = gen.LIMITS
ADVISORY_LIMITS = gen.ADVISORY_LIMITS
REQUIRED_HEADERS = gen.REQUIRED_HEADERS
IMAGE_RULES = gen.IMAGE_RULES
BOM_FATAL_MESSAGE = gen.BOM_FATAL_MESSAGE
PROVENANCE = f"supercat_server @ {gen.SOURCE_GIT_SHA[:8]}"

# eCat convention: a "-" in a ship-to cell means "same as bill-to", not a value.
PLACEHOLDER = "-"

# Limits asserted in the canonical docs that could NOT be traced to code or to the
# database, and are therefore NOT enforced. Kept here rather than deleted so the next
# agent finds the evidence instead of re-adding the rule.
#
# Verified 2026-07-27 against supercat_server and the live DB.
RETIRED_CLAIMS = {
    "ProductStory <= 500": (
        "PHASE_GATES.md G3. `products.story` is an unbounded `text` column and the "
        "importer sets it verbatim — no 500-char limit exists at any layer. "
        "Legrand's 442 over-500 rows are fine."
    ),
    "RelatedItems <= 255": (
        "IMPLEMENTATION_PLAN.md 4.1/9. `products.related_items` is an unbounded `text` "
        "column and `related_items` is absent from Product::ATTR_LENGTHS. The "
        "'a 207-SKU collection needs ~2,690 chars so related-by-collection is "
        "impossible' argument rests on a limit that does not exist. RelatedItems is "
        "still checked referentially — the importer warns \"Related item: 'X' not "
        "found\" — just not for length."
    ),
    "LongDesc 50 / ShortDesc 15 / MediumDesc 25": (
        "ecat-core-files. All three are 255 and warn-and-truncate, per "
        "Product::ATTR_LENGTHS. Transcribing 15 and 50 into a sync script is what "
        "mangled 355 product names at one client."
    ),
    "BaseItemCode 20 (advisory)": (
        "ecat-ground-truth. The real limit is 40 and it IS enforced as a validation "
        "error. mali's 21-char codes pass because 21 < 40, not because the limit is "
        "advisory. Keep codes short for image filenames, but that is a preference."
    ),
}


def limit_for(csv_file, header):
    """Code-derived limit metadata for a header, or None if the field is unbounded."""
    return LIMITS.get(csv_file, {}).get(header.lower())


def advisory_for(csv_file, header):
    return ADVISORY_LIMITS.get(csv_file, {}).get(header.lower())


def required_headers(csv_file):
    return REQUIRED_HEADERS.get(csv_file, [])


def check_row_lengths(csv_file, row, lookup, row_no, label="", check="lengths"):
    """Two-tier length findings for one row.

    Returns [] when nothing overflows. Blank cells and the "-" ship-to placeholder
    are skipped — "-" means "same as bill-to", not a one-character value.
    """
    findings = []
    where = f"row {row_no}" + (f" ({label})" if label else "")

    for header, meta in LIMITS.get(csv_file, {}).items():
        value = get(row, lookup, header)
        if not value or value == PLACEHOLDER or len(value) <= meta["limit"]:
            continue
        detail = (
            f"{lookup.get(header, header)} {len(value)}>{meta['limit']} chars "
            f"({meta['model']}::ATTR_LENGTHS[:{meta['attr']}], {PROVENANCE})"
        )
        if meta["tier"] == "truncate":
            findings.append(warn(
                check,
                f"{detail} — importer WARNS and TRUNCATES to {meta['limit']}; the row "
                f"imports with the value cut mid-word",
                where,
            ))
        else:
            findings.append(fail(
                check,
                f"{detail} — importer REJECTS the row",
                where,
            ))

    for header, meta in ADVISORY_LIMITS.get(csv_file, {}).items():
        value = get(row, lookup, header)
        if not value or value == PLACEHOLDER or len(value) <= meta["limit"]:
            continue
        hard = limit_for(csv_file, header)
        if hard and len(value) > hard["limit"]:
            continue  # already reported at the blocking tier; don't double-count
        findings.append(warn(
            check,
            f"{lookup.get(header, header)} {len(value)}>{meta['limit']} chars — "
            f"{meta['note']} ({meta['source']})",
            where,
        ))

    return findings


def check_lengths(csv_file, rows, lookup, label_field=None, check="lengths"):
    """Two-tier length findings across every row of a file."""
    findings = []
    for i, row in enumerate(rows, start=2):  # row 1 is the header
        label = get(row, lookup, label_field) if label_field else ""
        findings.extend(check_row_lengths(csv_file, row, lookup, i, label, check))
    return findings


def image_filename_is_valid(name):
    """Mirror Product::VALID_IMAGE_REGEX plus CdnImageSync's extension gate."""
    if not re.match(IMAGE_RULES["filename_regex"], name):
        return False, "contains a forbidden character (/ or parentheses)"
    lowered = name.lower()
    if not any(lowered.endswith(ext) for ext in IMAGE_RULES["extensions"]):
        return False, (
            f"extension not in {IMAGE_RULES['extensions']} — CdnImageSync skips it"
        )
    return True, ""
