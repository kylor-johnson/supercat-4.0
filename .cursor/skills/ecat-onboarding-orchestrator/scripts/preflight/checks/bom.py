#!/usr/bin/env python3
"""BOM check — the cheapest gate in the plan (IMPLEMENTATION_PLAN.md 4.8).

Three leading bytes (`EF BB BF`) attach to the first header name, so `BaseItemCode`
becomes `\\ufeffBaseItemCode` and the importer rejects the whole file with a fatal
naming the one column that is plainly present.

Verified mechanism, and it is worth knowing *why* it looks absurd — two code paths
disagree about the BOM:

* `Importer::LineDataValidator#validate_header` reads the header with
  `CSV.open(path, 'r', &:first)` — no `bom|` prefix, so the BOM survives into the
  header name and `missing_columns` reports it as absent, at `:fatal`.
* `FileReader.each_line` opens with `encoding: 'bom|utf-8'`, which *does* strip it.

So row parsing would have tolerated the file; header validation kills it first. Excel
for Windows emits a BOM by default via Save As -> CSV UTF-8, so this recurs every time
a client hand-edits a deliverable. It cost a full round trip on Lib & Co's stories.csv.
"""
import os

from ..core import fail, first_header_name, has_bom
from ..limits import BOM_FATAL_MESSAGE

CHECK = "bom"
SUBSYSTEM = "core"


def run(paths):
    findings = []
    for path in paths:
        name = os.path.basename(path)
        try:
            if not has_bom(path):
                continue
            header = first_header_name(path).strip().lstrip("\ufeff").lower()
        except OSError as exc:
            findings.append(fail(CHECK, f"could not read: {exc}", name))
            continue
        expected = (BOM_FATAL_MESSAGE or "Column {column} is missing").format(
            column=header or "<first column>")
        findings.append(fail(
            CHECK,
            f"starts with a UTF-8 BOM (EF BB BF). The importer will reject the whole "
            f'file with "{expected}" — a column that IS present. Re-save as plain '
            f"UTF-8 (Excel: Save As -> CSV, not 'CSV UTF-8')",
            name,
        ))
    return findings
