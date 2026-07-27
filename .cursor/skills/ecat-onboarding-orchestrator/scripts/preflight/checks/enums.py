#!/usr/bin/env python3
"""Enum and required-field checks, shared by the gate and validate_customers.py.

The headline case is Terracotta: `DefaultPriceCode = 0` — an ERP placeholder, not a price
level — rejected every row of the customer file, which is why the docs still said "0
customers" long after it was fixed. The model validation is explicit:

    unless PriceLevel.code_exists?(customer.default_price_code, customer.organization_id)
      customer.errors.add(:default_price_code, 'must be a valid price level code')

So membership in the org's real price levels is the only thing that settles it. The
placeholder blacklist below catches the common shapes offline; `--price-levels` is what
actually proves it, and its absence is reported rather than assumed away.

Living here rather than inside `validate_customers.py` means the gate and the standalone
validator cannot drift apart on the one check that matters most.
"""
from ..core import fail, get

CHECK = "enums"
SUBSYSTEM = "core"

# DefaultPriceCode values that are never real price levels: ERP placeholders and status
# strings that arrive in the price-code column because the export had nowhere else to put
# them.
BAD_PRICE_CODES = {"", "0", "pending", "closed", "inactive", "hold", "n/a", "na", "none"}

HIDEABLE_VALUES = ("Y", "N")


def where(row_no, label):
    return f"row {row_no} ({label or '?'})"


def check_required(row_no, label, row, lookup, fields, present_only=False):
    """Blank-but-present required fields. present_only skips absent columns."""
    findings = []
    for field in fields:
        if present_only and field.lower() not in lookup:
            continue
        if not get(row, lookup, field):
            prefix = "blank required " if not present_only else "blank "
            findings.append(fail(CHECK, f"{prefix}{field}", where(row_no, label)))
    return findings


def check_price_code(row_no, label, code, valid_levels=None):
    """The tcd blocker, plus membership when the org's real levels are supplied."""
    if not code:
        return []
    if code.lower() in BAD_PRICE_CODES:
        return [fail(
            CHECK,
            f"DefaultPriceCode '{code}' is a placeholder/status, not a price level -> "
            f"import will reject the row",
            where(row_no, label),
        )]
    if valid_levels and code.lower() not in valid_levels:
        return [fail(
            CHECK,
            f"DefaultPriceCode '{code}' not in price levels {sorted(valid_levels)}",
            where(row_no, label),
        )]
    return []


def check_enum(row_no, label, field, value, allowed):
    if value and value not in allowed:
        return [fail(
            CHECK,
            f"invalid {field} '{value}' (want {'/'.join(allowed)})",
            where(row_no, label),
        )]
    return []


def check_hideable(row_no, label, value):
    return check_enum(row_no, label, "Hideable", value, HIDEABLE_VALUES)
