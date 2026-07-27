#!/usr/bin/env python3
"""Omission preview — what disappears because it isn't in this file.

Kylor's own invariant, from a handoff: *"Always include ALL products in products.csv on
upload — missing products get deleted."* Nothing enforced it.

What omission costs differs per file, and the difference is the whole point:

* `customers.csv` / `inventory.csv` / `options.csv` and the pricing files HARD-delete
  every existing record and reload. Omission is total loss.
* `products.csv` soft-deletes omitted rows — recoverable, but they vanish from the iPad.
* `stories.csv` nulls the story and leaves the product alone.

One more trap worth stating plainly, because it inverts the usual reasoning: **deletes
only run on a clean import.** Any `Error`-tier row makes the importer skip every delete.
So if expected deletes didn't happen, look for an error row — and a catalog with PNG
image URLs (which log at `:error`) is probably also failing to soft-delete its
discontinued products, silently.

This check previews the blast and requires explicit acknowledgement. It never writes.
"""
from ..core import fail, get, warn
from ..files import HARD_DELETE_FILES, describe_delete, meta

CHECK = "omission"
SUBSYSTEM = "core"

MAX_LISTED = 15


def run(csv_file, rows, lookup, key_field, live_keys=None, live_count=None,
        acknowledged=False):
    findings = []
    info = meta(csv_file)
    if not info:
        return [warn(CHECK, f"{csv_file} is not a known eCat file; delete semantics "
                            f"unverified — do not upload it blind")]

    if info["delete"] == "none":
        findings.append(warn(
            CHECK,
            f"{csv_file} {describe_delete(csv_file)} — omission is safe for this file",
        ))
        return findings

    hard = csv_file in HARD_DELETE_FILES
    file_keys = {get(r, lookup, key_field) for r in rows if get(r, lookup, key_field)}

    if hard:
        target = live_count if live_count is not None else "an unknown number of"
        message = (
            f"{csv_file} {describe_delete(csv_file)}. Uploading this replaces {target} "
            f"existing record(s) with the {len(rows)} row(s) in this file. Anything not "
            f"in this file is GONE, not hidden"
        )
        findings.append(fail(CHECK, message + " — re-run with --ack-deletes to confirm")
                        if not acknowledged else warn(CHECK, message + " [acknowledged]"))
    elif live_keys is None:
        findings.append(warn(
            CHECK,
            f"no live key list supplied: could not compute which records this file "
            f"omits. {csv_file} {describe_delete(csv_file)} — supply the org's current "
            f"keys (--live-state for the gate) to see the blast radius before uploading",
        ))
    else:
        live = {str(k).strip() for k in live_keys if str(k).strip()}
        omitted = sorted(live - file_keys)
        if not omitted:
            findings.append(warn(
                CHECK,
                f"this file includes all {len(live)} live record(s); nothing will be "
                f"deleted",
            ))
        else:
            listed = ", ".join(omitted[:MAX_LISTED])
            tail = f" ...and {len(omitted) - MAX_LISTED} more" if len(omitted) > MAX_LISTED else ""
            message = (
                f"{len(omitted)} of {len(live)} live record(s) are absent from this file "
                f"and the import {describe_delete(csv_file)}: {listed}{tail}"
            )
            findings.append(
                fail(CHECK, message + " — re-run with --ack-deletes to confirm this is "
                                      "intentional")
                if not acknowledged else warn(CHECK, message + " [acknowledged]")
            )

    findings.append(warn(
        CHECK,
        "reminder: deletes run ONLY on an error-free import. If expected deletions do "
        "not happen, look for an Error-tier row rather than re-sending the file",
    ))
    return findings
