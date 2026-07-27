#!/usr/bin/env python3
"""Org fingerprint — does this file actually belong to this org?

The load-bearing incident (Appendix B): Legrand's 1,194-row inventory file was imported
into Magic Lite. Inventory hard-deletes then reloads, so mali's real inventory was
replaced with 1,194 rows matching zero mali products. The orphan counts corroborate it
exactly — leg's own inventory is 1,194 rows, precisely the foreign row count.

Nothing about that file was malformed. It was valid, just for a different tenant, which
is why no data-quality check could have caught it and why this one exists.

Three independent signals, all cheap:

1. **Key overlap.** Sample the file's keys against the org's live keys and require
   >= 95% membership. A foreign file scores near zero.
2. **Row count tolerance.** A file 10x or 0.1x the live count is either a different
   tenant or an accidental partial export.
3. **Path containment.** The file must live under this client's own build folder. The
   mali/leg swap was a path mistake before it was a data mistake.

Signals 1 and 2 need live state passed in; the path check works offline. For hard-delete
files a failed fingerprint is a hard block — there is nothing to undo afterwards.
"""
import os

from ..core import fail, get, warn
from ..files import HARD_DELETE_FILES, describe_delete

CHECK = "fingerprint"
SUBSYSTEM = "core"

MIN_OVERLAP = 0.95
COUNT_TOLERANCE = 0.5  # live count may differ by +/-50% before it warns


def run(csv_file, rows, lookup, key_field, live_keys=None, live_count=None,
        path=None, client_dir=None, shortname=None):
    findings = []
    hard = csv_file in HARD_DELETE_FILES
    tier = fail if hard else warn
    stakes = (
        f" This file {describe_delete(csv_file)}, so a wrong-org import is not "
        f"recoverable." if hard else ""
    )

    file_keys = {get(r, lookup, key_field) for r in rows if get(r, lookup, key_field)}

    if live_keys is None:
        findings.append(warn(
            CHECK,
            f"no live key list supplied: could not confirm this file belongs to "
            f"{shortname or 'this org'}. Supply the org's {key_field} values "
            f"(--live-state for the gate) before uploading"
            + (" — this file hard-deletes, so a wrong-org import cannot be undone"
               if hard else ""),
        ))
    elif not live_keys:
        findings.append(warn(
            CHECK,
            f"the org has zero existing {key_field} values, so key overlap proves "
            f"nothing. Treat this as a first import and verify the org by hand",
        ))
    elif file_keys:
        live = {str(k).strip() for k in live_keys if str(k).strip()}
        matched = len(file_keys & live)
        overlap = matched / len(file_keys)
        if overlap < MIN_OVERLAP:
            findings.append(tier(
                CHECK,
                f"only {matched}/{len(file_keys)} ({overlap:.0%}) of this file's "
                f"{key_field} values exist in org {shortname or '?'} — below the "
                f"{MIN_OVERLAP:.0%} threshold. This file may belong to a different "
                f"org.{stakes}",
            ))
        else:
            findings.append(warn(
                CHECK,
                f"key overlap {overlap:.0%} ({matched}/{len(file_keys)}) — passes the "
                f"{MIN_OVERLAP:.0%} threshold",
            ) if overlap < 1.0 else None)

    if live_count is not None and live_count > 0 and rows:
        ratio = len(rows) / live_count
        if not (1 - COUNT_TOLERANCE) <= ratio <= (1 + COUNT_TOLERANCE):
            findings.append(warn(
                CHECK,
                f"{len(rows)} rows vs {live_count} live ({ratio:.2f}x) — outside the "
                f"+/-{COUNT_TOLERANCE:.0%} tolerance. Confirm this is a full file and "
                f"not a partial export or another org's data",
            ))

    if path and client_dir:
        resolved = os.path.realpath(path)
        base = os.path.realpath(client_dir)
        if not (resolved == base or resolved.startswith(base + os.sep)):
            findings.append(fail(
                CHECK,
                f"file lives outside the client's build folder.\n"
                f"      file:   {resolved}\n"
                f"      client: {base}\n"
                f"    This is the exact shape of the mali/leg inventory wipe — a valid "
                f"file from the wrong tenant.{stakes}",
            ))

    return [f for f in findings if f is not None]
