#!/usr/bin/env python3
"""Import-order manifest, and the option_groups re-send that everyone forgets.

Canonical order:

    options.csv -> option_groups.csv -> products.csv -> stories.csv ->
    inventory.csv -> customers.csv -> matrix_options.csv

Importing `options.csv` **hard-deletes all options and nulls every option-group
membership**, so `option_groups.csv` must be sent again afterwards. Getting this backwards
nulled group membership at both tcs and pebl. The order is documented in three separate
places and was still gotten wrong, which is the argument for a manifest rather than
another paragraph.

Given a set of files this emits the correct sequence, with the second `option_groups.csv`
pass already appended. Given an explicit sequence (`--order`), it verifies it.
"""
from ..core import fail, warn
from ..files import classify, order_position

CHECK = "order"
SUBSYSTEM = "core"


def manifest(names):
    """Canonical upload sequence for a set of files, with the groups re-send."""
    known = [n for n in names if order_position(n) is not None]
    ordered = sorted(set(known), key=order_position)
    if "options.csv" in ordered and "option_groups.csv" in ordered:
        ordered.append("option_groups.csv")  # second pass restores membership
    return ordered


def run(paths, declared_order=None):
    """Check the planned upload set (and optionally its declared sequence)."""
    findings = []
    names, unknown = [], []
    for path in paths:
        name = classify(path)
        (names.append(name) if name else unknown.append(path))

    for path in unknown:
        findings.append(warn(
            CHECK,
            f"{path} is not a recognized eCat import file — it has no known delete "
            f"semantics or order position. Confirm what it is before uploading",
        ))

    unique = set(names)

    if "options.csv" in unique and "option_groups.csv" not in unique:
        findings.append(fail(
            CHECK,
            "options.csv is being sent WITHOUT option_groups.csv. Importing options "
            "nulls every group's membership, and nothing else restores it — every group "
            "will end up empty. Send option_groups.csv immediately after",
        ))

    if "option_groups.csv" in unique and "options.csv" not in unique:
        findings.append(warn(
            CHECK,
            "option_groups.csv without options.csv: this hard-deletes all groups and "
            "reloads from the file. Fine if the options themselves are unchanged",
        ))

    if declared_order:
        declared = [classify(p) or p for p in declared_order]
        # Only a file's FIRST appearance carries ordering information. A repeat is a
        # deliberate re-send — the mandatory second option_groups.csv pass lands after
        # products.csv by design, and reading that as "out of sequence" would make the
        # one correct sequence the only one this check rejects.
        ranked, seen = [], set()
        for i, name in enumerate(declared):
            position = order_position(name)
            if position is None or name in seen:
                continue
            seen.add(name)
            ranked.append((i, name, position))
        for (i1, n1, p1), (i2, n2, p2) in zip(ranked, ranked[1:]):
            if p2 < p1:
                findings.append(fail(
                    CHECK,
                    f"declared order puts {n2} (position {p2}) after {n1} (position "
                    f"{p1}). Correct sequence: {' -> '.join(manifest(declared))}",
                ))
        first_groups = next((i for i, n, _ in ranked if n == "option_groups.csv"), None)
        first_options = next((i for i, n, _ in ranked if n == "options.csv"), None)
        if first_groups is not None and first_options is not None and first_groups < first_options:
            findings.append(fail(
                CHECK,
                "option_groups.csv is scheduled BEFORE options.csv. The options import "
                "will null the membership you just loaded",
            ))
        if (first_options is not None
                and declared.count("option_groups.csv") < 2
                and "option_groups.csv" in declared):
            findings.append(fail(
                CHECK,
                "option_groups.csv appears once alongside options.csv. It needs TWO "
                "passes — once in sequence and once after options.csv, which nulls "
                "membership on import",
            ))

    if unique:
        findings.append(warn(
            CHECK,
            "upload in this order: " + " -> ".join(manifest(names)),
        ))
    return findings
