#!/usr/bin/env python3
"""The eCat import file family: canonical names, delete semantics, and order.

Two facts drive every omission and ordering check:

1. **What happens to a record you leave out differs per file.** `products.csv`
   soft-deletes; `customers.csv`, `inventory.csv`, `options.csv` and the pricing files
   HARD-delete everything and reload; `stories.csv` nulls the story without touching
   the product. Importing another org's inventory file is how Magic Lite's inventory
   was replaced with 1,194 rows matching zero of its products.

2. **Deletes only run on a clean import.** An `Error`-tier row makes the importer skip
   every delete of an omitted record. So "the deletes didn't happen" is a symptom of an
   error row, not of a missing file — and a catalog full of PNG URLs (which log at
   `:error`) probably also silently failed to soft-delete discontinued products.

`option_groups.csv` must be re-sent after `options.csv` because importing options nulls
group membership. That is a sequence requirement, not a preference.
"""
import os
import re

# delete: what happens to a record present in the DB but absent from the file
#   hard    every existing record is deleted and the file reloaded
#   soft    omitted records are flagged deleted=true (recoverable)
#   null    a column is cleared; the parent record survives
#   none    upsert only; omission does nothing
FAMILY = {
    "options.csv": {
        "order": 1, "delete": "hard", "subsystem": "options",
        "scope": "ALL options for the org, and it NULLS every option-group membership",
    },
    "option_groups.csv": {
        "order": 2, "delete": "hard", "subsystem": "options",
        "scope": "ALL option groups for the org",
    },
    "products.csv": {
        "order": 3, "delete": "soft", "subsystem": "core",
        "scope": "products absent from the file (deleted=true), on a clean import only",
    },
    "stories.csv": {
        "order": 4, "delete": "null", "subsystem": "stories",
        "scope": "story=null for products absent from the file; products survive",
    },
    "inventory.csv": {
        "order": 5, "delete": "hard", "subsystem": "inventory",
        "scope": "ALL inventory rows for the org",
    },
    "customers.csv": {
        "order": 6, "delete": "hard", "subsystem": "customers",
        "scope": "ALL customers AND all ship-tos for the org",
    },
    "matrix_options.csv": {
        "order": 7, "delete": "hard", "subsystem": "options",
        "scope": "ALL matrix option pricing for the org",
    },
    "contract_prices.csv": {
        "order": 8, "delete": "hard", "subsystem": "pricing",
        "scope": "ALL contract prices for the org",
    },
    "riser_prices.csv": {
        "order": 9, "delete": "hard", "subsystem": "pricing",
        "scope": "ALL riser prices for the org",
    },
    "sentinel.csv": {
        "order": 10, "delete": "none", "subsystem": "core",
        "scope": "nothing — it triggers the multi-file product merge",
    },
    "order_data.csv": {
        "order": 20, "delete": "none", "subsystem": "portal",
        "scope": "Sales Portal order history (separate file family)",
    },
    "invoice_data.csv": {
        "order": 21, "delete": "none", "subsystem": "portal",
        "scope": "Sales Portal invoice history (separate file family)",
    },
}

IMPORT_ORDER = [
    name for name, meta in sorted(FAMILY.items(), key=lambda kv: kv[1]["order"])
    if meta["subsystem"] != "portal"
]

HARD_DELETE_FILES = {n for n, m in FAMILY.items() if m["delete"] == "hard"}

# products_1.csv, products_2.csv ... update by BaseItemCode and never delete.
SUPPLEMENT_RE = re.compile(r"^products_(\d+)\.csv$", re.I)

# Exact filenames the Sales Portal importer requires; a TBL_ prefix fails the file.
PORTAL_EXACT_NAMES = {"order_data.csv": "Order_Data.csv",
                      "invoice_data.csv": "Invoice_Data.csv"}


# Longest stem first, so `option_groups_final.csv` never resolves to `options.csv`.
_STEMS = sorted(
    ((name[: -len(".csv")], name) for name in FAMILY),
    key=lambda pair: len(pair[0]), reverse=True,
)


def classify(path):
    """Canonical family name for a path, or None if it isn't a known eCat file.

    Working files rarely carry the canonical name exactly — `products_2026-07-27.csv`
    and `customers_final.csv` are both normal — so a stem prefix resolves to its family.
    The `products_N.csv` supplement pattern is checked first because it is a genuinely
    different file with different delete semantics.
    """
    name = os.path.basename(path).lower()
    if name in FAMILY:
        return name
    if SUPPLEMENT_RE.match(name):
        return "products_N.csv"
    stem = name[: -len(".csv")] if name.endswith(".csv") else name
    for prefix, canonical in _STEMS:
        if stem == prefix or stem.startswith(prefix + "_") or stem.startswith(prefix + "-"):
            return canonical
    return None


def meta(name):
    if name == "products_N.csv":
        return {
            "order": 3, "delete": "none", "subsystem": "core",
            "scope": "nothing — supplements update existing products by BaseItemCode",
        }
    return FAMILY.get(name)


def key_column(name):
    """The column that identifies a record in this file."""
    return {
        "products.csv": "BaseItemCode",
        "products_N.csv": "BaseItemCode",
        "stories.csv": "BaseItemCode",
        "inventory.csv": "BaseItemCode",
        "customers.csv": "BillToCode",
        "options.csv": "Code",
        "option_groups.csv": "Code",
    }.get(name)


def order_position(name):
    m = meta(name)
    return m["order"] if m else None


def describe_delete(name):
    m = meta(name)
    if not m:
        return "unknown file — delete semantics unverified"
    return {
        "hard": f"HARD-DELETES {m['scope']}, then reloads from this file",
        "soft": f"soft-deletes {m['scope']}",
        "null": f"clears {m['scope']}",
        "none": f"deletes nothing ({m['scope']})",
    }[m["delete"]]
