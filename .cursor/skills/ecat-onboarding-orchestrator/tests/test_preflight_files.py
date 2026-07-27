"""Tests for preflight/files.py — the file family, delete semantics, and order.

Delete semantics are the highest-stakes facts in the whole gate: `customers.csv` and
`inventory.csv` hard-delete everything and reload, `products.csv` soft-deletes, and
`stories.csv` only nulls a column. Getting one of these wrong in a *description* is how
an operator gets talked into an unrecoverable upload, so the wording is pinned too.
"""
import pytest

from preflight.files import (FAMILY, HARD_DELETE_FILES, IMPORT_ORDER, classify,
                             describe_delete, key_column, meta, order_position)


@pytest.mark.parametrize("filename,expected", [
    ("products.csv", "products.csv"),
    ("PRODUCTS.CSV", "products.csv"),
    ("/abs/path/customers.csv", "customers.csv"),
    # Working files rarely carry the canonical name exactly.
    ("products_2026-07-27.csv", "products.csv"),
    ("customers_final.csv", "customers.csv"),
    ("inventory-updated.csv", "inventory.csv"),
    # The supplement pattern is a genuinely different file, checked first.
    ("products_1.csv", "products_N.csv"),
    ("products_12.csv", "products_N.csv"),
    ("nonsense.csv", None),
    ("readme.txt", None),
])
def test_classify(filename, expected):
    assert classify(filename) == expected


def test_longest_stem_wins_so_groups_never_resolve_to_options():
    """`options` is a prefix of nothing, but `option_groups_x` must not become options.csv.

    Getting this backwards would silently apply the wrong delete semantics to the one
    pair of files whose ordering already causes the most damage.
    """
    assert classify("option_groups_final.csv") == "option_groups.csv"
    assert classify("options_final.csv") == "options.csv"


def test_hard_delete_set_is_exactly_the_unrecoverable_files():
    assert HARD_DELETE_FILES == {
        "options.csv", "option_groups.csv", "inventory.csv", "customers.csv",
        "matrix_options.csv", "contract_prices.csv", "riser_prices.csv",
    }


def test_products_soft_deletes_and_stories_only_nulls():
    """These two are the ones people conflate, and the difference is recoverability."""
    assert meta("products.csv")["delete"] == "soft"
    assert meta("stories.csv")["delete"] == "null"
    assert "soft-deletes" in describe_delete("products.csv")
    assert "products survive" in describe_delete("stories.csv")


def test_customers_description_says_ship_tos_go_too():
    text = describe_delete("customers.csv")
    assert "HARD-DELETES" in text
    assert "ship-tos" in text


def test_options_description_warns_about_nulled_group_membership():
    """The reason option_groups.csv needs a second pass has to appear here."""
    assert "NULLS every option-group membership" in describe_delete("options.csv")


def test_supplement_files_never_delete():
    assert meta("products_N.csv")["delete"] == "none"
    assert "deletes nothing" in describe_delete("products_N.csv")


def test_unknown_file_is_described_as_unverified_rather_than_safe():
    assert "unverified" in describe_delete("mystery.csv")


def test_canonical_import_order():
    core = [n for n in IMPORT_ORDER if n in (
        "options.csv", "option_groups.csv", "products.csv", "stories.csv",
        "inventory.csv", "customers.csv", "matrix_options.csv")]
    assert core == ["options.csv", "option_groups.csv", "products.csv", "stories.csv",
                    "inventory.csv", "customers.csv", "matrix_options.csv"]


def test_portal_files_are_a_separate_family():
    """order_data / invoice_data go through a different tool and must not be sequenced in."""
    assert "order_data.csv" not in IMPORT_ORDER
    assert "invoice_data.csv" not in IMPORT_ORDER
    assert FAMILY["order_data.csv"]["subsystem"] == "portal"


def test_options_sort_before_products():
    assert order_position("options.csv") < order_position("products.csv")
    assert order_position("options.csv") < order_position("option_groups.csv")


@pytest.mark.parametrize("name,column", [
    ("products.csv", "BaseItemCode"),
    ("inventory.csv", "BaseItemCode"),
    ("stories.csv", "BaseItemCode"),
    ("customers.csv", "BillToCode"),
    ("options.csv", "Code"),
    ("option_groups.csv", "Code"),
])
def test_key_column(name, column):
    assert key_column(name) == column


def test_every_family_entry_is_complete():
    for name, info in FAMILY.items():
        assert info["delete"] in ("hard", "soft", "null", "none"), name
        assert info["subsystem"], name
        assert info["scope"], name
        assert describe_delete(name)
