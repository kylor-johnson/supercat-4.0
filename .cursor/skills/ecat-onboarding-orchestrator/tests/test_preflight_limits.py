"""Tests for preflight/limits.py — the two-tier length check.

The tier split is not cosmetic. `ATTRS_TO_TRUNCATE` fields warn and silently truncate,
so a long LongDesc imports mangled; everything else rejects the row outright. Reporting
a truncation as a blocker would train an operator to ignore the gate, and reporting a
rejection as advisory is how 16 of Pebl's 24 option groups died in one import.

These tests assert the *tier and the provenance*, never a specific number — the numbers
come from tools/gen_limits.py, and hard-coding one here would recreate the transcription
bug the generator exists to prevent.
"""
from preflight.core import FAIL, WARNING
from preflight.limits import (ADVISORY_LIMITS, LIMITS, PROVENANCE, RETIRED_CLAIMS,
                              advisory_for, check_lengths, check_row_lengths,
                              image_filename_is_valid, limit_for, required_headers)


def _overflow(csv_file, header, over=1):
    meta = limit_for(csv_file, header)
    return "x" * (meta["limit"] + over), meta


def test_truncating_field_warns_rather_than_blocks(rows_from, severities):
    """LongDesc is in ATTRS_TO_TRUNCATE: the row imports, cut mid-word."""
    value, meta = _overflow("products.csv", "longdesc")
    assert meta["tier"] == "truncate"
    rows, lookup = rows_from(f"BaseItemCode,LongDesc\nA-1,{value}\n")
    by = severities(check_row_lengths("products.csv", rows[0], lookup, 2, "A-1"))
    assert FAIL not in by
    assert "TRUNCATES" in by[WARNING][0]
    assert "row 2 (A-1)" in by[WARNING][0]


def test_erroring_field_blocks(rows_from, severities):
    """Option Code is a plain validation: over the limit, the row is rejected."""
    value, meta = _overflow("options.csv", "code")
    assert meta["tier"] == "error"
    rows, lookup = rows_from(f"Code,Name\n{value},Black\n")
    by = severities(check_row_lengths("options.csv", rows[0], lookup, 2))
    assert "REJECTS the row" in by[FAIL][0]


def test_finding_cites_the_ruby_attribute_and_the_commit(rows_from):
    """A limit without provenance is a transcribed constant wearing a disguise."""
    value, meta = _overflow("options.csv", "code")
    rows, lookup = rows_from(f"Code,Name\n{value},Black\n")
    message = check_row_lengths("options.csv", rows[0], lookup, 2)[0].render()
    assert f"{meta['model']}::ATTR_LENGTHS[:{meta['attr']}]" in message
    assert PROVENANCE in message


def test_value_exactly_at_the_limit_passes(rows_from):
    meta = limit_for("options.csv", "code")
    rows, lookup = rows_from(f"Code,Name\n{'x' * meta['limit']},Black\n")
    assert check_row_lengths("options.csv", rows[0], lookup, 2) == []


def test_reports_the_original_header_casing(rows_from):
    """Findings quote the operator's own column name, not the downcased lookup key."""
    value, _ = _overflow("customers.csv", "billtocode", over=10)
    rows, lookup = rows_from(f"BillToCode\n{value}\n")
    message = check_row_lengths("customers.csv", rows[0], lookup, 2)[0].render()
    assert "BillToCode" in message
    assert "billtocode" not in message


def test_blank_and_dash_placeholder_are_not_lengths(rows_from):
    """"-" in a ship-to cell means "same as bill-to", not a one-character value."""
    rows, lookup = rows_from("BillToCode,ShipToCity\n,-\n")
    assert check_row_lengths("customers.csv", rows[0], lookup, 2) == []


def test_advisory_tier_warns_between_the_two_thresholds(rows_from, severities):
    """BillToCode warns above 15 in the importer but only errors above 20 in the model."""
    soft = advisory_for("customers.csv", "billtocode")
    hard = limit_for("customers.csv", "billtocode")
    assert soft["limit"] < hard["limit"]
    value = "x" * (soft["limit"] + 1)
    rows, lookup = rows_from(f"BillToCode\n{value}\n")
    by = severities(check_row_lengths("customers.csv", rows[0], lookup, 2))
    assert FAIL not in by
    assert f">{soft['limit']}" in by[WARNING][0]
    assert soft["source"] in by[WARNING][0]


def test_advisory_does_not_double_report_a_blocking_overflow(rows_from, severities):
    """Past the hard limit it is one FAIL, not a FAIL plus a redundant warning."""
    hard = limit_for("customers.csv", "billtocode")
    rows, lookup = rows_from(f"BillToCode\n{'x' * (hard['limit'] + 5)}\n")
    by = severities(check_row_lengths("customers.csv", rows[0], lookup, 2))
    assert len(by[FAIL]) == 1
    assert WARNING not in by


def test_check_lengths_numbers_rows_from_two(rows_from):
    """Row 1 is the header, so the first data row is row 2 — matching the import log."""
    value, _ = _overflow("options.csv", "code")
    rows, lookup = rows_from(f"Code,Name\nok,Fine\n{value},Bad\n")
    findings = check_lengths("options.csv", rows, lookup, label_field="Code")
    assert len(findings) == 1
    assert "row 3" in findings[0].render()


def test_unknown_file_has_no_limits_and_does_not_crash(rows_from):
    rows, lookup = rows_from("Whatever\nx\n")
    assert check_lengths("not_an_ecat_file.csv", rows, lookup) == []


def test_terms_is_covered_now(rows_from, severities):
    """Pebl's customer file was rejected on Terms, which the old MAX_LEN table omitted.

    Their real payment terms are 55 characters against a 30-char field, so this is a
    structural mismatch needing a client decision — not something to silently truncate.
    (It was eventually shortened by hand to "30% TT Adv, Bal on B/L".) The comma inside
    the value is why it is quoted here: unquoted, it splits into two columns and the
    overflow disappears, which is its own class of source-file bug.
    """
    assert limit_for("customers.csv", "terms") is not None
    terms = "30% T/T Advance, Balance Against Copy of Bill of Lading"
    assert len(terms) == 55
    rows, lookup = rows_from(f'BillToCode,Terms\nC-1,"{terms}"\n')
    by = severities(check_row_lengths("customers.csv", rows[0], lookup, 2, "C-1"))
    assert FAIL in by and "Terms" in by[FAIL][0]
    assert "55>30" in by[FAIL][0]


def test_every_limit_carries_its_source():
    for csv_file, headers in LIMITS.items():
        for header, meta in headers.items():
            assert meta["tier"] in ("truncate", "error"), (csv_file, header)
            assert meta["model"] and meta["attr"], (csv_file, header)
    for csv_file, headers in ADVISORY_LIMITS.items():
        for header, meta in headers.items():
            assert meta["note"] and meta["source"], (csv_file, header)


def test_required_headers_are_known_for_the_core_files():
    for name in ("products.csv", "customers.csv", "options.csv", "option_groups.csv"):
        assert required_headers(name)


def test_image_filename_rules():
    assert image_filename_is_valid("ML-001.jpg")[0] is True
    assert image_filename_is_valid("ML-001.JPG")[0] is True
    assert image_filename_is_valid("ML-001.jpeg")[0] is True
    ok, why = image_filename_is_valid("ML-001.png")
    assert ok is False and "CdnImageSync" in why
    ok, why = image_filename_is_valid("chair (2).jpg")
    assert ok is False and "forbidden character" in why


def test_retired_claims_are_documented_not_deleted():
    """A limit we removed must leave its evidence, or the next agent re-adds it."""
    assert RETIRED_CLAIMS
    for claim, why in RETIRED_CLAIMS.items():
        assert len(why) > 40, claim
    # The two that would otherwise get re-derived from the docs.
    assert any("story" in k.lower() for k in RETIRED_CLAIMS)
    assert any("relateditems" in k.lower() for k in RETIRED_CLAIMS)


def test_long_desc_is_not_the_transcribed_50():
    """ecat-core-files says 50. It is 255 and it truncates. That doc is wrong."""
    meta = limit_for("products.csv", "longdesc")
    assert meta["limit"] == 255
    assert meta["tier"] == "truncate"
