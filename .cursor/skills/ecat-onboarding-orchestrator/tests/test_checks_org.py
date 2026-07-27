"""Tests for the org-level checks: fingerprint, omission, order.

These three share a property that separates them from every other check: the file can be
perfectly well-formed and still be catastrophic. Legrand's inventory file was valid — it
just belonged to a different tenant, and importing it into Magic Lite replaced that org's
inventory with 1,194 rows matching zero of its products. No data-quality check could have
caught that, which is the entire argument for this group.
"""
from preflight.checks import fingerprint, omission, order
from preflight.core import FAIL, WARNING


# --- org fingerprint ------------------------------------------------------------


def test_foreign_file_blocks_on_a_hard_delete_file(rows_from, severities):
    """The mali/leg wipe, reproduced: valid rows, zero overlap with the target org."""
    rows, lookup = rows_from(
        "BaseItemCode,QtyAvailable\nLEG-1,5\nLEG-2,5\nLEG-3,5\n")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode",
        live_keys=["ML-1", "ML-2", "ML-3"], shortname="mali"))
    assert FAIL in by
    assert "0/3 (0%)" in by[FAIL][0]
    assert "may belong to a different org" in by[FAIL][0]
    # It must state the stakes, because there is nothing to undo afterwards.
    assert "HARD-DELETES" in by[FAIL][0]
    assert "not recoverable" in by[FAIL][0]


def test_same_mismatch_only_warns_on_a_soft_delete_file(rows_from, severities):
    """products.csv soft-deletes, so a wrong-org import is recoverable — warn, don't block."""
    rows, lookup = rows_from("BaseItemCode\nLEG-1\nLEG-2\nLEG-3\n")
    by = severities(fingerprint.run(
        "products.csv", rows, lookup, "BaseItemCode",
        live_keys=["ML-1", "ML-2", "ML-3"], shortname="mali"))
    assert FAIL not in by
    assert "0/3" in by[WARNING][0]


def test_matching_file_passes_the_threshold(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,QtyAvailable\nML-1,5\nML-2,5\nML-3,5\n")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode",
        live_keys=["ML-1", "ML-2", "ML-3", "ML-4"], shortname="mali"))
    assert FAIL not in by
    assert by.get(WARNING, []) == []  # a perfect match says nothing at all


def test_partial_overlap_above_the_threshold_is_reported_but_not_blocked(rows_from,
                                                                        severities):
    live = [f"ML-{i}" for i in range(100)]
    body = "".join(f"ML-{i},5\n" for i in range(99)) + "NEW-1,5\n"
    rows, lookup = rows_from(f"BaseItemCode,QtyAvailable\n{body}")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode", live_keys=live, shortname="mali"))
    assert FAIL not in by
    assert "passes the 95% threshold" in by[WARNING][0]


def test_absent_live_keys_warn_and_name_the_stakes(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nML-1,5\n")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode", live_keys=None, shortname="mali"))
    assert FAIL not in by
    assert "could not confirm this file belongs to mali" in by[WARNING][0]
    assert "cannot be undone" in by[WARNING][0]


def test_empty_org_is_treated_as_a_first_import(rows_from, severities):
    """Zero live keys means overlap proves nothing — say so rather than scoring 0%."""
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nML-1,5\n")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode", live_keys=[], shortname="mali"))
    assert FAIL not in by
    assert "first import" in by[WARNING][0]


def test_row_count_far_from_live_warns(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nML-1,5\n")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode",
        live_keys=["ML-1"], live_count=700, shortname="mali"))
    assert any("1 rows vs 700 live" in m for m in by[WARNING])
    assert any("partial export" in m for m in by[WARNING])


def test_file_outside_the_client_folder_blocks(rows_from, severities, tmp_path):
    """The wipe was a path mistake before it was a data mistake."""
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nML-1,5\n",
                             name="inventory.csv")
    other = tmp_path / "leg"
    other.mkdir()
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode",
        path=str(tmp_path / "inventory.csv"), client_dir=str(other), shortname="mali"))
    assert FAIL in by
    assert "outside the client's build folder" in by[FAIL][0]


def test_file_inside_the_client_folder_is_fine(rows_from, severities, tmp_path):
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nML-1,5\n",
                             name="inventory.csv")
    by = severities(fingerprint.run(
        "inventory.csv", rows, lookup, "BaseItemCode",
        path=str(tmp_path / "inventory.csv"), client_dir=str(tmp_path),
        shortname="mali"))
    assert FAIL not in by


# --- omission preview -----------------------------------------------------------


def test_hard_delete_file_blocks_until_acknowledged(rows_from, severities):
    rows, lookup = rows_from("BillToCode,BillToName\nC-1,Acme\n")
    by = severities(omission.run(
        "customers.csv", rows, lookup, "BillToCode", live_count=346))
    assert FAIL in by
    assert "replaces 346 existing record(s) with the 1 row(s)" in by[FAIL][0]
    assert "GONE, not hidden" in by[FAIL][0]
    assert "--ack-deletes" in by[FAIL][0]


def test_acknowledgement_downgrades_it_but_keeps_it_visible(rows_from, severities):
    rows, lookup = rows_from("BillToCode,BillToName\nC-1,Acme\n")
    by = severities(omission.run(
        "customers.csv", rows, lookup, "BillToCode", live_count=346,
        acknowledged=True))
    assert FAIL not in by
    assert any("[acknowledged]" in m for m in by[WARNING])


def test_soft_delete_lists_exactly_what_disappears(rows_from, severities):
    """Kylor's own invariant — always include ALL products — with nothing enforcing it."""
    rows, lookup = rows_from("BaseItemCode\nA-1\n")
    by = severities(omission.run(
        "products.csv", rows, lookup, "BaseItemCode", live_keys=["A-1", "A-2", "A-3"]))
    assert FAIL in by
    assert "2 of 3 live record(s) are absent" in by[FAIL][0]
    assert "A-2, A-3" in by[FAIL][0]
    assert "soft-deletes" in by[FAIL][0]


def test_complete_file_deletes_nothing_and_says_so(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode\nA-1\nA-2\n")
    by = severities(omission.run(
        "products.csv", rows, lookup, "BaseItemCode", live_keys=["A-1", "A-2"]))
    assert FAIL not in by
    assert any("nothing will be deleted" in m for m in by[WARNING])


def test_omitted_list_is_truncated(rows_from, severities):
    live = [f"A-{i}" for i in range(omission.MAX_LISTED + 6)]
    rows, lookup = rows_from("BaseItemCode\nA-0\n")
    by = severities(omission.run(
        "products.csv", rows, lookup, "BaseItemCode", live_keys=live))
    assert "and 5 more" in by[FAIL][0]


def test_supplement_file_omission_is_safe(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,Features\nA-1,Oak\n")
    by = severities(omission.run("products_N.csv", rows, lookup, "BaseItemCode"))
    assert FAIL not in by
    assert "omission is safe" in by[WARNING][0]


def test_unknown_file_refuses_to_guess(rows_from, severities):
    rows, lookup = rows_from("Whatever\nx\n")
    by = severities(omission.run("mystery.csv", rows, lookup, "Whatever"))
    assert "do not upload it blind" in by[WARNING][0]


def test_every_omission_report_carries_the_error_tier_reminder(rows_from, severities):
    """Deletes run only on a clean import — the fact that inverts the usual reasoning."""
    rows, lookup = rows_from("BaseItemCode\nA-1\n")
    by = severities(omission.run(
        "products.csv", rows, lookup, "BaseItemCode", live_keys=["A-1"]))
    assert any("ONLY on an error-free import" in m for m in by[WARNING])


# --- import order ---------------------------------------------------------------


def test_options_without_groups_blocks(severities):
    """Importing options nulls every group's membership and nothing else restores it."""
    by = severities(order.run(["options.csv", "products.csv"]))
    assert FAIL in by
    assert "WITHOUT option_groups.csv" in by[FAIL][0]
    assert "every group will end up empty" in by[FAIL][0]


def test_groups_without_options_only_warns(severities):
    by = severities(order.run(["option_groups.csv", "products.csv"]))
    assert FAIL not in by
    assert any("Fine if the options themselves are unchanged" in m for m in by[WARNING])


def test_manifest_appends_the_second_groups_pass():
    """The re-send everyone forgets, and the reason tcs and pebl both lost membership."""
    manifest = order.manifest(["products.csv", "option_groups.csv", "options.csv"])
    assert manifest == ["options.csv", "option_groups.csv", "products.csv",
                        "option_groups.csv"]


def test_manifest_is_emitted_for_the_upload_set(severities):
    by = severities(order.run(["customers.csv", "products.csv"]))
    assert any("upload in this order: products.csv -> customers.csv" in m
               for m in by[WARNING])


def test_declared_order_out_of_sequence_blocks(severities):
    by = severities(order.run(
        ["products.csv", "inventory.csv"],
        declared_order=["inventory.csv", "products.csv"]))
    assert FAIL in by
    assert "declared order puts products.csv" in by[FAIL][0]


def test_groups_scheduled_before_options_blocks(severities):
    by = severities(order.run(
        ["options.csv", "option_groups.csv"],
        declared_order=["option_groups.csv", "options.csv", "option_groups.csv"]))
    assert any("scheduled BEFORE options.csv" in m for m in by[FAIL])


def test_single_groups_pass_alongside_options_blocks(severities):
    by = severities(order.run(
        ["options.csv", "option_groups.csv"],
        declared_order=["options.csv", "option_groups.csv"]))
    assert any("It needs TWO passes" in m for m in by[FAIL])


def test_correct_two_pass_sequence_is_accepted(severities):
    by = severities(order.run(
        ["options.csv", "option_groups.csv", "products.csv"],
        declared_order=["options.csv", "option_groups.csv", "products.csv",
                        "option_groups.csv"]))
    assert FAIL not in by


def test_unrecognized_file_is_flagged_as_unknown_semantics(severities):
    by = severities(order.run(["mystery_data.csv"]))
    assert any("not a recognized eCat import file" in m for m in by[WARNING])
    assert any("no known delete semantics" in m for m in by[WARNING])
