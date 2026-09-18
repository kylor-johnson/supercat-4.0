"""Characterization — `report_render/md_parse.py` + the MD→HTML seam (W2 / Phase 3).

P0-3 lived here: a Jinja whitespace chomp glued a paragraph onto the row above
it, markdown treated the paragraph as a lazy continuation of the table, and the
parser kept consuming — absorbing the NEXT table including its `|---|---|`
separator, which reached the client as a literal `---` cell.

The Phase-1 fix was upstream, in `section_06_team.md.j2` (keep the blank line).
The renderer itself has no defense, so the lazy-continuation tests below pin
both halves: the shape that is safe today, and the shape that still leaks
(marked xfail).

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every behavior below is the one we want.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from report_render.md_parse import (
    CANONICAL_TOC,
    GATESTOP_TOC,
    Chunk,
    ParsedReport,
    _classify_h2,
    _detect_mode,
    _extract_footer_lines,
    merge_methodology,
    parse_md,
)
from report_render.md_render import md_to_html, md_inline_to_html
from report_render.sections import _parse_md_table, _split_paragraphs

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"


# ─── P0-3: lazy continuation ────────────────────────────────────────────────

_SAFE = """| Metric | Value |
| --- | --- |
| Reps who placed an order | **7** |

**3 of 12 seats are quiet or dark** (2 quiet, 1 dark).

| Coverage | Value |
| --- | --- |
| Platform coverage rate | **41.0%** |"""

# The exact P0-3 shape: `{%-` ate the blank lines, so the paragraph and the
# table after it are one continuous run.
_CHOMPED = """| Metric | Value |
| --- | --- |
| Reps who placed an order | **7** |
**3 of 12 seats are quiet or dark** (2 quiet, 1 dark).
| Coverage | Value |
| --- | --- |
| Platform coverage rate | **41.0%** |"""


def test_blank_lines_keep_the_two_tables_and_the_paragraph_apart():
    """The shape the Phase-1 template fix produces: three blocks, two tables."""
    blocks = _split_paragraphs(_SAFE)
    assert len(blocks) == 3
    assert _parse_md_table(blocks[0]) == [
        ["Metric", "Value"],
        ["Reps who placed an order", "**7**"],
    ]
    assert not blocks[1].startswith("|")
    assert _parse_md_table(blocks[2]) == [
        ["Coverage", "Value"],
        ["Platform coverage rate", "**41.0%**"],
    ]
    assert "<td>---</td>" not in md_to_html(_SAFE)


def test_a_paragraph_abutting_a_table_row_is_swallowed_as_a_row():
    """One blank line lost → the paragraph becomes a table cell (not prose)."""
    lazy = _SAFE.replace("| **7** |\n\n**3 of 12", "| **7** |\n**3 of 12")
    html = md_to_html(lazy)
    assert "<td><strong>3 of 12 seats are quiet or dark</strong> (2 quiet, 1 dark).</td>" in html
    # It is still only the paragraph that is absorbed; the second table survives
    # because its own blank line is intact.
    assert html.count("<table>") == 2
    assert "<td>---</td>" not in html


def test_chomped_shape_splits_into_one_block_that_parse_md_table_rejects():
    """`_split_paragraphs` sees one block; `_parse_md_table` returns None
    because not every line starts with `|`, so the caller falls back to the raw
    markdown-it render — which is where the `---` reaches the client."""
    blocks = _split_paragraphs(_CHOMPED)
    assert len(blocks) == 1
    assert _parse_md_table(blocks[0]) is None


def test_chomped_shape_collapses_both_tables_into_one():
    """Pinned P0-3 damage: two tables render as one, 5 body rows."""
    html = md_to_html(_CHOMPED)
    assert html.count("<table>") == 1
    assert html.count("<tr>") == 6  # 1 header + 5 body


@pytest.mark.xfail(
    reason="P0-3 is fixed only in the Jinja templates; the renderer still emits "
           "a literal `---` cell when a table is lazily continued (Phase 4+)",
    strict=True,
)
def test_renderer_should_not_leak_a_separator_row_as_a_cell():
    assert "<td>---</td>" not in md_to_html(_CHOMPED)


# ─── `_split_paragraphs` — the table re-join repair ─────────────────────────

def test_a_stray_blank_line_inside_one_table_is_rejoined():
    """A Jinja whitespace artifact between header+separator and body would
    otherwise render an empty table plus a headerless one."""
    split_table = "| A | B |\n| --- | --- |\n\n| 1 | 2 |\n| 3 | 4 |"
    blocks = _split_paragraphs(split_table)
    assert len(blocks) == 1
    assert _parse_md_table(blocks[0]) == [["A", "B"], ["1", "2"], ["3", "4"]]


def test_two_tables_separated_by_prose_stay_two_blocks():
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n\nSome prose.\n\n| C | D |\n| --- | --- |\n| 3 | 4 |"
    assert len(_split_paragraphs(md)) == 3


def test_split_paragraphs_drops_empty_blocks_and_strips():
    assert _split_paragraphs("\n\n  a  \n\n\n   \n\nb\n\n") == ["a", "b"]


def test_split_paragraphs_on_empty_input():
    assert _split_paragraphs("") == []
    assert _split_paragraphs("   \n  \n") == []


# ─── `_parse_md_table` ──────────────────────────────────────────────────────

def test_parse_md_table_discards_the_alignment_row():
    rows = _parse_md_table("| A | B |\n|:---|---:|\n| 1 | 2 |")
    assert rows == [["A", "B"], ["1", "2"]]


def test_parse_md_table_keeps_an_unlabeled_header():
    rows = _parse_md_table("| | |\n| --- | --- |\n| Same dealers | **+29%** |")
    assert rows == [["", ""], ["Same dealers", "**+29%**"]]


@pytest.mark.parametrize(
    "block",
    [
        "",                                  # empty
        "just prose",                        # no pipes
        "| A | B |",                         # single line — needs 2+
        "| A | B |\n| --- | --- |\nnot a row",  # a non-pipe line anywhere
    ],
)
def test_parse_md_table_returns_none_for_non_tables(block):
    assert _parse_md_table(block) is None


def test_parse_md_table_tolerates_a_header_only_table():
    """Header + separator with no body rows still parses (to just the header)."""
    assert _parse_md_table("| A | B |\n| --- | --- |") == [["A", "B"]]


# ─── Footer-code-line extraction ────────────────────────────────────────────

def test_extracts_stacked_footer_lines_in_order():
    md = "body text\n\n`[STEP-0 OVERRIDE · x]`\n`[STEP-10 LEDGER · org · 1:pass]`\n"
    body, footers = _extract_footer_lines(md)
    assert footers == ["[STEP-0 OVERRIDE · x]", "[STEP-10 LEDGER · org · 1:pass]"]
    assert body.strip() == "body text"


def test_stops_at_the_first_non_footer_line():
    md = "`[STEP-10 LEDGER · a]`\nreal prose\n`[STEP-10 LEDGER · b]`\n"
    body, footers = _extract_footer_lines(md)
    assert footers == ["[STEP-10 LEDGER · b]"]
    assert "[STEP-10 LEDGER · a]" in body


def test_no_footers_returns_the_body_unchanged():
    body, footers = _extract_footer_lines("# Title\n\nbody\n")
    assert footers == []
    assert body == "# Title\n\nbody"


# ─── Mode detection ─────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "text,expected",
    [
        ("# Org — VALIDATION ARTIFACT, GATE-FAILED", "gatestop"),
        ("# Org — VALIDATION ARTIFACT GATE FAILED", "gatestop"),
        ("# Shadow Catchers — GATE-FAILED", "gatestop"),
        ("# Sarreid, Ltd. — CEO Intelligence Brief", "mode1"),
        # the marker must be in an H1, not buried mid-prose
        ("# Sarreid\n\nprose about a gate-failed run", "mode1"),
        ("", "mode1"),
    ],
)
def test_detect_mode(text, expected):
    assert _detect_mode(text) == expected


# ─── H2 → section_id classification ─────────────────────────────────────────

@pytest.mark.parametrize(
    "heading,expected",
    [
        ("The 60-second read", "summary"),
        ("The 60 second read", "summary"),
        ("Do this week — 7 calls, $1.45M+ in play", "thisweek"),
        ("Do this month", "thismonth"),
        ("The growth engine — three layers, all real", "growth"),
        ("What's driving the +5.95% — three layers", "growth"),
        ("The team", "team"),
        ("The full risk picture — 30 dealers", "risk"),
        ("The full at-risk picture — positions 6–25", "risk"),
        ("Full risk watchlist", "risk"),
        ("What's selling", "products"),
        ("Product intelligence", "products"),
        ("The dealer base", "base"),
        ("Channels", "channels"),
        ("What an invoiced ERP feed would unlock", "unlock"),
        ("What this report can't see — and what to add next", "methodology_gaps"),
        ("How to trust these numbers", "methodology_trust"),
        ("Appendix — traceability", "appendix"),
    ],
)
def test_classify_mode1_headings(heading, expected):
    assert _classify_h2(heading, "mode1") == expected


@pytest.mark.parametrize(
    "heading,expected",
    [
        ("Bottom line — gate state", "summary"),
        ("What the preflights returned", "preflights"),
        ("User-grain concentration finding", "concentration"),
        ("Patch-validation observations", "patchnotes"),
        ("Recommended next action", "nextaction"),
        ("Appendix", "appendix"),
    ],
)
def test_classify_gatestop_headings(heading, expected):
    assert _classify_h2(heading, "gatestop") == expected


def test_classify_falls_back_to_a_misc_slug():
    assert _classify_h2("Dealer coverage & platform activity", "mode1") == (
        "misc-dealer-coverage-platform-activity"
    )
    assert _classify_h2("###", "mode1") == "misc-section"


def test_channels_pattern_is_anchored():
    """`^channels` — a heading that merely mentions channels is not §10."""
    assert _classify_h2("Channels", "mode1") == "channels"
    assert _classify_h2("Your channels at a glance", "mode1").startswith("misc-")


def test_the_two_toc_tables_carry_the_ids_the_renderer_emits():
    assert [sid for sid, _ in CANONICAL_TOC] == [
        "summary", "thisweek", "thismonth", "growth", "team",
        "risk", "products", "base", "channels", "methodology",
    ]
    assert [sid for sid, _ in GATESTOP_TOC] == [
        "summary", "preflights", "concentration", "nextaction", "appendix",
    ]


# ─── parse_md end to end ────────────────────────────────────────────────────

_MINIMAL = """# Sarreid, Ltd. — CEO Intelligence Brief

### Trailing 12 months through Jun 30, 2026 · vs the prior matching 12 months

Some preamble prose.

## The 60-second read

---
Hero paragraph.
---

## Do this week — 7 calls

<!--slot:B-->
Call list prose.

`[STEP-10 LEDGER · sarreid · 1:pass]`
"""


def test_parse_md_pulls_h1_h3_preamble_and_chunks():
    r = parse_md(_MINIMAL)
    assert r.mode == "mode1"
    assert r.org_h1_full == "Sarreid, Ltd. — CEO Intelligence Brief"
    assert r.org_display_name == "Sarreid, Ltd."
    assert r.org_subtitle == "Trailing 12 months through Jun 30, 2026 · vs the prior matching 12 months"
    assert r.preamble_md == "Some preamble prose."
    assert [c.section_id for c in r.chunks] == ["summary", "thisweek"]
    assert r.footer_code_lines == ["[STEP-10 LEDGER · sarreid · 1:pass]"]


def test_leading_and_trailing_rules_are_stripped_from_a_chunk_body():
    r = parse_md(_MINIMAL)
    assert r.chunk_by_id("summary").body_md == "Hero paragraph."


def test_standalone_slot_marker_lines_are_dropped():
    """A bare `<!--slot:C-->` line shatters the structure it wraps, so the
    whole line goes; inline markers inside a content line are preserved."""
    r = parse_md(_MINIMAL)
    assert "<!--slot:B-->" not in r.chunk_by_id("thisweek").body_md
    inline = parse_md("# T\n\n## Do this week\n\n| a <!--slot:B-->x<!--/slot:B--> | b |\n")
    assert "<!--slot:B-->" in inline.chunk_by_id("thisweek").body_md


def test_chunk_by_id_returns_none_for_a_missing_section():
    assert parse_md(_MINIMAL).chunk_by_id("channels") is None


def test_a_document_with_no_h2_becomes_all_preamble():
    r = parse_md("# Org\n\nJust prose, no sections.")
    assert r.chunks == []
    assert r.preamble_md == "Just prose, no sections."


def test_a_document_with_no_h1():
    r = parse_md("## The 60-second read\n\nbody")
    assert r.org_h1_full == "Untitled"
    assert r.org_display_name == "Untitled"
    assert [c.section_id for c in r.chunks] == ["summary"]


def test_raw_heading_line_round_trips():
    """`_H2` is `$`-anchored under re.M, so the captured line keeps its
    trailing newline."""
    r = parse_md(_MINIMAL)
    assert r.chunk_by_id("thisweek").raw_heading_line == "## Do this week — 7 calls\n"


def test_merge_methodology_is_a_documented_no_op():
    r = parse_md(_MINIMAL)
    assert merge_methodology(r) is r


# ─── Real cohort MDs (skip when the gitignored outputs are absent) ──────────

COHORT_MD = {
    "sarreid": ("sarreid_DRAFT_2026-07-02.md", "mode1", "Sarreid, Ltd."),
    "da": ("da_DRAFT_2026-07-09.md", "mode1", "Dainolite Ltd."),
    "bsc": ("bsc_GATESTOP_2026-07-14.md", "mode1", "Butler Specialty Company"),
}


@pytest.mark.parametrize("org", sorted(COHORT_MD), ids=sorted(COHORT_MD))
def test_real_cohort_md_parses_to_the_expected_shape(org):
    name, mode, display = COHORT_MD[org]
    path = OUTPUTS / name
    if not path.exists():
        pytest.skip(f"no tracked output for {org} (outputs/ is gitignored)")
    r = parse_md(path.read_text(encoding="utf-8"))
    assert r.mode == mode
    assert r.org_display_name == display
    assert r.chunks
    assert r.chunks[0].section_id == "summary"


def test_the_invoiced_and_behavior_only_layouts_differ():
    sarreid = OUTPUTS / "sarreid_DRAFT_2026-07-02.md"
    da = OUTPUTS / "da_DRAFT_2026-07-09.md"
    if not (sarreid.exists() and da.exists()):
        pytest.skip("no tracked outputs (outputs/ is gitignored)")
    inv = [c.section_id for c in parse_md(sarreid.read_text(encoding="utf-8")).chunks]
    beh = [c.section_id for c in parse_md(da.read_text(encoding="utf-8")).chunks]
    assert "thisweek" in inv and "thisweek" not in beh
    assert "unlock" in beh and "unlock" not in inv


# ─── md_render helpers ──────────────────────────────────────────────────────

def test_html_comments_are_stripped_before_render():
    assert md_to_html("a <!-- hidden --> b").strip() == "<p>a  b</p>"
    assert md_inline_to_html("a <!--\nmulti\nline\n--> b") == "a  b"


def test_md_to_html_returns_empty_string_for_blank_input():
    assert md_to_html("") == ""
    assert md_to_html("   \n ") == ""
    assert md_inline_to_html("") == ""


def test_soft_breaks_do_not_become_br():
    assert "<br" not in md_to_html("line one\nline two")


def test_raw_html_in_the_md_is_escaped_not_passed_through():
    assert "&lt;script&gt;" in md_to_html("<script>alert(1)</script>")
