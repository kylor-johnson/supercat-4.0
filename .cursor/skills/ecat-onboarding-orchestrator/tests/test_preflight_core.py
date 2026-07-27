"""Tests for preflight/core.py — severity tiers, exit codes, and CSV primitives.

The tier semantics are the whole contract a phase gate branches on, so they are pinned
here rather than inferred from any one check's behavior.
"""
import pytest

from preflight.core import (BOM_BYTES, EXIT_ERROR, EXIT_FAIL, EXIT_OK, ERROR, FAIL,
                            SKIP, WARNING, Report, error, fail, first_header_name, get,
                            has_bom, is_url, load_rows, skip, split_codes, warn)


def test_warnings_and_skips_do_not_block():
    report = Report()
    report.add(warn("c", "advisory")).add(skip("c", "(flag: options none)"))
    assert report.exit_code == EXIT_OK
    assert "PASS" in report.render()


def test_fail_blocks_and_error_outranks_it():
    report = Report()
    report.add(fail("c", "blocking"))
    assert report.exit_code == EXIT_FAIL
    report.add(error("c", "could not run"))
    assert report.exit_code == EXIT_ERROR


def test_skip_renders_its_reason():
    """A skipped check must say why. A silent pass is the failure mode being prevented."""
    report = Report()
    report.record("options.csv/lengths")
    report.add(skip("options.csv/lengths", "(flag: options none)"))
    out = report.render()
    assert "SKIPPED (1)" in out
    assert "flag: options none" in out


def test_render_separates_the_tiers():
    report = Report()
    report.add([fail("a", "bad"), warn("b", "meh"), skip("c", "(flag: x)")])
    out = report.render()
    assert "these block the import" in out
    assert "advisory, do not block import" in out
    # FAILURES render last so the blocking items are what's left on screen.
    assert out.index("WARNINGS") < out.index("FAILURES")


def test_report_counts_checks_not_findings():
    report = Report()
    report.record("one").record("one").record("two")
    report.add([warn("one", "a"), warn("one", "b")])
    assert "across 2 check(s)" in report.render()


def test_header_lookup_is_case_insensitive(rows_from):
    """The importer downcases every header, so every lookup here must too."""
    rows, lookup = rows_from("BaseItemCode,LONGDESC\nA-1,Chair\n")
    assert get(rows[0], lookup, "baseitemcode") == "A-1"
    assert get(rows[0], lookup, "LongDesc") == "Chair"
    assert lookup["longdesc"] == "LONGDESC"


def test_get_returns_empty_for_absent_column(rows_from):
    rows, lookup = rows_from("BaseItemCode\nA-1\n")
    assert get(rows[0], lookup, "Nope") == ""


def test_get_strips_whitespace(rows_from):
    rows, lookup = rows_from("BaseItemCode,LongDesc\n  A-1  ,  Chair \n")
    assert get(rows[0], lookup, "BaseItemCode") == "A-1"


def test_load_rows_tolerates_an_empty_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    assert load_rows(path) == ([], {})


def test_load_rows_strips_the_bom_but_has_bom_still_sees_it(tmp_path):
    """Our parse must not break on a BOM, but the check must still be able to find it.

    These are deliberately two code paths, mirroring the importer: FileReader strips the
    BOM while the header validator does not, which is why the file fails at all.
    """
    path = tmp_path / "bom.csv"
    path.write_bytes(BOM_BYTES + b"BaseItemCode,LongDesc\nA-1,Chair\n")
    rows, lookup = load_rows(path)
    assert "baseitemcode" in lookup
    assert get(rows[0], lookup, "BaseItemCode") == "A-1"
    assert has_bom(path) is True
    assert first_header_name(path).startswith("\ufeff")


def test_has_bom_false_for_plain_utf8(tmp_path):
    path = tmp_path / "plain.csv"
    path.write_text("BaseItemCode\nA-1\n", encoding="utf-8")
    assert has_bom(path) is False


def test_split_codes_drops_blanks():
    assert split_codes("A, B ,, C ") == ["A", "B", "C"]
    assert split_codes("") == []


@pytest.mark.parametrize("value,expected", [
    ("https://cdn.example.com/a.jpg", True),
    ("http://example.com/a.jpg", True),
    ("ftp://host/a.jpg", True),
    ("  https://example.com/a.jpg  ", True),
    ("A-1.jpg", False),
    ("C:\\images\\a.jpg", False),
    ("", False),
])
def test_is_url(value, expected):
    assert is_url(value) is expected


def test_severity_constants_are_distinct():
    assert len({FAIL, WARNING, SKIP, ERROR}) == 4
