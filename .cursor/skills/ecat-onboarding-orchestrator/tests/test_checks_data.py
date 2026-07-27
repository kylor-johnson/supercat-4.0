"""Tests for the data-shape checks: bom, dupes, refs, custom_fields, taxonomy, enums.

Each check is tiered by what the importer actually does with the offending row, and the
tier is the assertion that matters. A dangling `RelatedItems` link warns because the
importer keeps the product; a dangling `inventory.BaseItemCode` fails because the row is
discarded outright and the file silently claims to have set stock it never set.
"""
import pytest

from preflight.checks import bom, custom_fields, dupes, enums, refs, taxonomy
from preflight.core import BOM_BYTES, FAIL, WARNING


# --- BOM ------------------------------------------------------------------------


def test_bom_is_reported_with_the_fatal_it_will_produce(tmp_path):
    """The value of this check is explaining an error message that looks absurd."""
    path = tmp_path / "stories.csv"
    path.write_bytes(BOM_BYTES + b"BaseItemCode,ProductStory\nA-1,A chair\n")
    findings = bom.run([str(path)])
    assert len(findings) == 1
    message = findings[0].render()
    assert findings[0].severity == FAIL
    assert "UTF-8 BOM" in message
    # The point: it names the column the importer will claim is missing.
    assert "baseitemcode is missing" in message.lower()
    assert "a column that IS present" in message
    assert "CSV UTF-8" in message  # the Excel setting that causes it


def test_no_bom_is_silent(tmp_path):
    path = tmp_path / "products.csv"
    path.write_text("BaseItemCode\nA-1\n", encoding="utf-8")
    assert bom.run([str(path)]) == []


def test_bom_check_reports_an_unreadable_file_rather_than_skipping_it(tmp_path):
    findings = bom.run([str(tmp_path / "does_not_exist.csv")])
    assert findings and findings[0].severity == FAIL
    assert "could not read" in findings[0].render()


def test_bom_scans_every_file_in_the_set(tmp_path):
    clean = tmp_path / "products.csv"
    clean.write_text("BaseItemCode\nA-1\n", encoding="utf-8")
    dirty = tmp_path / "customers.csv"
    dirty.write_bytes(BOM_BYTES + b"BillToCode\nC-1\n")
    findings = bom.run([str(clean), str(dirty)])
    assert len(findings) == 1
    assert findings[0].where == "customers.csv"


# --- duplicates -----------------------------------------------------------------


def test_duplicate_key_blocks_and_names_both_rows(rows_from, severities):
    rows, lookup = rows_from("Code,Name\nMT_FAROEXT_GR,A\nMT_FAROEXT_GR,B\n")
    by = severities(dupes.run("option_groups.csv", rows, lookup, key_field="Code"))
    assert len(by[FAIL]) == 1
    assert "MT_FAROEXT_GR" in by[FAIL][0]
    assert "[2, 3]" in by[FAIL][0]
    assert "later row(s) are rejected" in by[FAIL][0]


def test_duplicate_upc_only_warns(rows_from, severities):
    """upc_value has no uniqueness constraint, so it imports — but it is usually a typo."""
    rows, lookup = rows_from(
        "BaseItemCode,UPCValue\nA-1,0001\nA-2,0001\n")
    by = severities(dupes.run("products.csv", rows, lookup, key_field="BaseItemCode",
                              warn_fields=("UPCValue",)))
    assert FAIL not in by
    assert "UPCValue '0001'" in by[WARNING][0]


def test_unique_file_is_clean(rows_from):
    rows, lookup = rows_from("BaseItemCode\nA-1\nA-2\n")
    assert dupes.run("products.csv", rows, lookup, key_field="BaseItemCode") == []


def test_blank_keys_are_not_duplicates_of_each_other(rows_from):
    """Two blank cells are a required-field problem, not a duplicate-key problem."""
    rows, lookup = rows_from("BaseItemCode,LongDesc\n,A\n,B\n")
    assert dupes.run("products.csv", rows, lookup, key_field="BaseItemCode") == []


def test_absent_key_column_is_not_an_error(rows_from):
    rows, lookup = rows_from("LongDesc\nChair\n")
    assert dupes.run("products.csv", rows, lookup, key_field="BaseItemCode") == []


# --- cross-file refs ------------------------------------------------------------


def test_orphan_inventory_row_blocks(rows_from, severities):
    """Legrand's inventory import logged 24 KB of these; the rows silently did not load."""
    rows, lookup = rows_from("BaseItemCode,QtyAvailable\nA-1,5\nGHOST,9\n")
    by = severities(refs.check_child_file(
        "inventory.csv", rows, lookup, products={"A-1"}))
    assert len(by[FAIL]) == 1
    assert "GHOST" in by[FAIL][0]
    assert "Product not found, record ignored" in by[FAIL][0]
    assert "does NOT import" in by[FAIL][0]


def test_orphan_check_is_skipped_when_products_are_unknown(rows_from):
    """Without products.csv there is nothing to join against — don't invent failures."""
    rows, lookup = rows_from("BaseItemCode\nGHOST\n")
    assert refs.check_child_file("inventory.csv", rows, lookup, products=set()) == []


def test_orphan_list_rolls_up_past_the_display_limit(rows_from, severities):
    body = "".join(f"GHOST-{i},1\n" for i in range(refs.MAX_LISTED + 5))
    rows, lookup = rows_from(f"BaseItemCode,QtyAvailable\n{body}")
    by = severities(refs.check_child_file(
        "inventory.csv", rows, lookup, products={"A-1"}))
    assert len(by[FAIL]) == refs.MAX_LISTED + 1
    assert "and 5 more" in by[FAIL][-1]
    assert "fix the join, not the individual rows" in by[FAIL][-1]


def test_dangling_related_item_only_warns(rows_from, severities):
    """transform_related_items drops just the link and keeps the product."""
    rows, lookup = rows_from("BaseItemCode,RelatedItems\nA-1,\"A-2,GHOST\"\nA-2,\n")
    by = severities(refs.check_related_items(
        rows, lookup, products={"A-1", "A-2"}))
    assert FAIL not in by
    assert "GHOST" in by[WARNING][0]
    assert "the product still imports" in by[WARNING][0]


def test_related_items_length_is_not_checked():
    """A 2,690-char RelatedItems cell is fine: related_items is an unbounded text column.

    The plan argued related-by-collection was impossible against a 255-char limit that
    does not exist at any layer.
    """
    from preflight.limits import limit_for
    assert limit_for("products.csv", "relateditems") is None


def test_missing_optionset_group_blocks(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,OptionSet1,OptionSet2\nA-1,FIN_STD,GHOST\n")
    by = severities(refs.check_option_sets(rows, lookup, group_codes={"fin_std"}))
    assert len(by[FAIL]) == 1
    assert "GHOST" in by[FAIL][0]
    assert "OptionSet2" in by[FAIL][0]


def test_optionset_check_is_case_insensitive(rows_from):
    rows, lookup = rows_from("BaseItemCode,OptionSet1\nA-1,FIN_STD\n")
    assert refs.check_option_sets(rows, lookup, group_codes={"fin_std"}) == []


def test_optionset_check_skipped_when_groups_file_absent(rows_from):
    rows, lookup = rows_from("BaseItemCode,OptionSet1\nA-1,ANYTHING\n")
    assert refs.check_option_sets(rows, lookup, group_codes=None) == []


def test_group_membership_is_newline_separated(rows_from):
    """The KB says comma-separated. The importer wants newlines."""
    rows, lookup = rows_from('Code,Name,Options\nFIN,Finishes,"100\n101"\n')
    assert refs.check_group_membership(
        rows, lookup, option_codes={"100", "101"}) == []


def test_comma_separated_membership_is_caught_as_one_giant_code(rows_from, severities):
    rows, lookup = rows_from('Code,Name,Options\nFIN,Finishes,"100,101,102"\n')
    by = severities(refs.check_group_membership(
        rows, lookup, option_codes={"100", "101", "102"}))
    assert FAIL in by
    assert "NEWLINE-separated" in by[FAIL][0]


def test_group_member_not_in_options_blocks(rows_from, severities):
    rows, lookup = rows_from('Code,Name,Options\nFIN,Finishes,"100\nGHOST"\n')
    by = severities(refs.check_group_membership(rows, lookup, option_codes={"100"}))
    assert "GHOST" in by[FAIL][0]


# --- custom fields --------------------------------------------------------------


def test_unknown_column_blocks_and_says_the_data_is_dropped(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,carton1_h\nA-1,10\n")
    by = severities(custom_fields.run("products.csv", lookup, registered=["Color"]))
    assert FAIL in by
    assert "carton1_h is unknown" in by[FAIL][0]
    assert "DROP the data" in by[FAIL][0]


def test_case_drift_is_named_rather_than_reported_as_two_problems(rows_from, severities):
    """ML_qtybackordered vs ML_QtyOnBackorder is one mistake, not an unknown plus a gap."""
    rows, lookup = rows_from("BaseItemCode,ML_QtyBackOrdered\nA-1,1\n")
    by = severities(custom_fields.run(
        "products.csv", lookup, registered=["ML_QtyOnBackorder"]))
    assert any("did you mean the registered field 'ML_QtyOnBackorder'" in m
               for m in by[FAIL])


def test_registered_field_absent_from_the_file_warns(rows_from, severities):
    """Legrand's live warning set: rohscompliant, Color, voltage."""
    rows, lookup = rows_from("BaseItemCode\nA-1\n")
    by = severities(custom_fields.run(
        "products.csv", lookup, registered=["rohscompliant", "Color", "voltage"]))
    assert FAIL not in by
    assert len(by[WARNING]) == 3
    assert any("omitting it does NOT clear it" in m for m in by[WARNING])


def test_registered_field_matches_case_insensitively(rows_from):
    rows, lookup = rows_from("BaseItemCode,COLOR\nA-1,Red\n")
    assert custom_fields.run("products.csv", lookup, registered=["Color"]) == []


def test_price_and_qty_prefixed_columns_are_accepted(rows_from):
    rows, lookup = rows_from(
        "BaseItemCode,Price_dn,Price_imap,Qty_Warehouse,OptionSet1\nA-1,1,2,3,FIN\n")
    assert custom_fields.run("products.csv", lookup, registered=[]) == []


def test_missing_custom_field_list_warns_instead_of_passing(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,whatever\nA-1,x\n")
    by = severities(custom_fields.run("products.csv", lookup, registered=None))
    assert FAIL not in by
    assert "no --custom-fields list supplied" in by[WARNING][0]


# --- taxonomy -------------------------------------------------------------------


def test_a_space_in_a_code_signals_auto_create(rows_from):
    """Length is not the signal: mali ships ACCESSORIES as one token and is Standard."""
    rows, lookup = rows_from(
        "BaseItemCode,TradeNameCode,CollectionCodes,CategoryCodes\n"
        "A-1,ML,ACCESSORIES,STRING\n")
    assert taxonomy.infer_method(taxonomy.extract(rows, lookup)) == "standard"

    rows, lookup = rows_from(
        "BaseItemCode,TradeNameCode,CollectionCodes,CategoryCodes\n"
        "A-1,ML,Outdoor Living,Dining Chairs\n")
    assert taxonomy.infer_method(taxonomy.extract(rows, lookup)) == "auto-create"


def test_standard_method_blocks_an_unregistered_code(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,TradeNameCode,CollectionCodes\nA-1,ML,GHOSTCOL\n")
    by = severities(taxonomy.run(rows, lookup, admin_codes=["ML"], groups=["MAIN"]))
    assert FAIL in by
    assert "GHOSTCOL" in by[FAIL][0]
    assert "pre-create it" in by[FAIL][0]


def test_auto_create_warns_that_the_string_becomes_the_ipad_label(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,CollectionCodes\nA-1,Outdoor Living\n")
    by = severities(taxonomy.run(rows, lookup, admin_codes=[], groups=["MAIN"]))
    assert FAIL not in by
    assert "becomes the iPad label" in by[WARNING][0]


def test_cryptic_code_under_auto_create_is_flagged(rows_from, severities):
    """COL126 auto-creates as the literal label a rep reads on the iPad."""
    rows, lookup = rows_from(
        "BaseItemCode,CollectionCodes,CategoryCodes\nA-1,COL126,Dining Chairs\n")
    by = severities(taxonomy.run(rows, lookup, admin_codes=[], groups=["MAIN"]))
    assert any("looks like an internal code" in m for m in by[WARNING])


def test_zero_admin_groups_blocks_because_groups_never_auto_create(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,CategoryCodes\nA-1,CHAIRS\n")
    by = severities(taxonomy.run(rows, lookup, admin_codes=["CHAIRS"], groups=[]))
    assert FAIL in by
    assert "never auto-create" in by[FAIL][0]


def test_unsupplied_group_list_warns_about_the_fatal_it_cannot_rule_out(rows_from,
                                                                       severities):
    rows, lookup = rows_from("BaseItemCode,CategoryCodes\nA-1,CHAIRS\n")
    by = severities(taxonomy.run(rows, lookup, admin_codes=["CHAIRS"], groups=None))
    assert FAIL not in by
    assert any("Groups NEVER auto-create" in m for m in by[WARNING])


# --- enums and required fields --------------------------------------------------


@pytest.mark.parametrize("code", ["0", "PENDING", "pending", "n/a", "CLOSED", "inactive"])
def test_placeholder_price_codes_are_caught_offline(code):
    """The tcd blocker: an ERP placeholder in the price-code column rejected 100% of rows."""
    findings = enums.check_price_code(2, "C-1", code)
    assert findings and findings[0].severity == FAIL
    assert "placeholder/status" in findings[0].render()


def test_valid_looking_code_passes_without_a_price_level_list():
    assert enums.check_price_code(2, "C-1", "dn") == []


def test_membership_is_what_actually_settles_it():
    """Only the org's real price_levels prove a code exists."""
    assert enums.check_price_code(2, "C-1", "dn", {"dn", "imap"}) == []
    findings = enums.check_price_code(2, "C-1", "ns", {"dn", "imap"})
    assert findings and "not in price levels" in findings[0].render()


def test_blank_price_code_is_left_to_the_required_field_check():
    assert enums.check_price_code(2, "C-1", "") == []


def test_required_field_findings_name_the_row_and_the_customer(rows_from):
    rows, lookup = rows_from("BillToCode,BillToName,BillToCity\nC-1,Acme,\n")
    findings = enums.check_required(
        2, "C-1", rows[0], lookup, ["BillToName", "BillToCity"])
    assert len(findings) == 1
    assert findings[0].render() == "row 2 (C-1): blank required BillToCity"


def test_present_only_mode_ignores_absent_columns(rows_from):
    rows, lookup = rows_from("BillToCode\nC-1\n")
    assert enums.check_required(
        2, "C-1", rows[0], lookup, ["ShipToCity"], present_only=True) == []
    assert enums.check_required(2, "C-1", rows[0], lookup, ["ShipToCity"])


def test_hideable_enum():
    assert enums.check_hideable(2, "A-1", "Y") == []
    assert enums.check_hideable(2, "A-1", "") == []
    findings = enums.check_hideable(2, "A-1", "TRUE")
    assert findings and "want Y/N" in findings[0].render()
