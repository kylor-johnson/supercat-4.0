"""Characterization — `pipeline/smoke_check.py` (W2 / Phase 3).

The §Q sensitivity-hedge gate is the load-bearing one: W1 made the
deterministic fallback depend on it at PARTIAL confidence (P0-10), and Phase 7
rewrites the materiality floors around it. `tests/test_deterministic_fallback.py`
exercises §Q across the real cohort; this file pins the gate's own mechanics —
the ±400-char window, the marker vocabulary, the STRONG short-circuit and the
three section headings it looks at.

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every behavior below is the one we want.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pipeline.smoke_check import (
    _BASE_QUALIFIER,
    _GATESTOP_REQUIRED_SECTIONS,
    _HEDGE_MARKERS,
    _NONE_REQUIRED_SECTIONS,
    _STANDARD_REQUIRED_SECTIONS,
    _check_addressable_base,
    _check_concentration_framing,
    _check_sensitivity_hedge,
    _check_topline_parity,
    _is_gatestop,
    main,
    smoke,
)


def _hedge(text: str, confidence: str | None = None) -> list[str]:
    issues: list[str] = []
    _check_sensitivity_hedge(text, issues, confidence)
    return issues


# ─── [5] §Q sensitivity hedge ──────────────────────────────────────────────

def test_an_unmarked_dollar_in_an_early_section_fails():
    out = _hedge("## The 60-second read\n\n$1.45M in play.\n", "PARTIAL")
    assert len(out) == 1
    assert "SENSITIVITY HEDGE: $1.45M" in out[0]
    assert "## The 60-second read" in out[0]
    assert "confidence=PARTIAL" in out[0]


@pytest.mark.parametrize(
    "marker",
    ["directional", "floor", "at least", "estimated", "approximate", "partial feed", "query result"],
)
def test_each_hedge_marker_clears_the_gate(marker):
    assert _hedge(f"## The 60-second read\n\n$1.45M in play ({marker}).\n", "PARTIAL") == []


def test_markers_are_case_insensitive():
    assert _hedge("## The 60-second read\n\n$1.45M — DIRECTIONAL.\n", "PARTIAL") == []


def test_strong_confidence_short_circuits_the_whole_check():
    assert _hedge("## The 60-second read\n\n$1.45M in play.\n", "STRONG") == []
    assert _hedge("## The 60-second read\n\n$1.45M in play.\n", "strong") == []


@pytest.mark.parametrize("confidence", ["PARTIAL", "LIMITED", "NONE", None])
def test_every_non_strong_level_is_gated(confidence):
    assert _hedge("## The 60-second read\n\n$1.45M in play.\n", confidence) != []


@pytest.mark.parametrize(
    "heading", ["## The 60-second read", "## Do this week", "## Do this month"]
)
def test_the_three_early_sections_are_in_scope(heading):
    assert _hedge(f"{heading}\n\n$1.45M in play.\n", "PARTIAL") != []


def test_later_sections_are_out_of_scope():
    md = "## The team\n\n$1.45M in play.\n\n## Channels\n\n$2.2M more.\n"
    assert _hedge(md, "PARTIAL") == []


def test_a_section_runs_to_the_next_h2():
    """A dollar under a later heading is not attributed to the early one."""
    md = "## The 60-second read\n\nNo dollars here.\n\n## The team\n\n$1.45M in play.\n"
    assert _hedge(md, "PARTIAL") == []


def test_the_last_early_section_is_capped_at_3000_chars():
    """With no following H2 the window is a fixed 3,000-char slice."""
    head = "## Do this month\n\n" + ("x " * 1600)
    assert _hedge(head + "\n$1.45M in play.\n", "PARTIAL") == []


def _filler(n: int) -> str:
    """`n` chars of word-separated junk — the markers are word-bounded, so a
    solid run of `x` would swallow the marker's closing boundary."""
    return ("x " * (n // 2 + 1))[:n]


def test_the_marker_window_is_four_hundred_chars_each_way():
    near = "## The 60-second read\n\ndirectional " + _filler(380) + "$1.45M\n"
    far = "## The 60-second read\n\ndirectional " + _filler(420) + "$1.45M\n"
    assert _hedge(near, "PARTIAL") == []
    assert _hedge(far, "PARTIAL") != []


def test_a_marker_after_the_dollar_also_counts():
    assert _hedge("## The 60-second read\n\n$1.45M in play — directional.\n", "PARTIAL") == []


def test_one_marker_covers_every_dollar_in_its_window():
    md = "## The 60-second read\n\nDirectional: $1.45M, $2.2M and $3.3M.\n"
    assert _hedge(md, "PARTIAL") == []


def test_each_unmarked_dollar_is_reported_separately():
    md = "## The 60-second read\n\n$1.45M, $2.2M and $3.3M.\n"
    assert len(_hedge(md, "PARTIAL")) == 3


@pytest.mark.parametrize("dollar", ["$1", "$1,450", "$1.45M", "$900K", "$2B"])
def test_dollar_shapes_the_gate_recognises(dollar):
    assert _hedge(f"## The 60-second read\n\n{dollar} in play.\n", "PARTIAL") != []


def test_a_percentage_is_not_a_dollar_claim():
    assert _hedge("## The 60-second read\n\nUp 29% this year.\n", "PARTIAL") == []


def test_hedge_marker_regex_is_word_bounded():
    assert _HEDGE_MARKERS.search("directionally") is None
    assert _HEDGE_MARKERS.search("this is directional") is not None


# ─── [6] §R concentration framing ──────────────────────────────────────────

def _conc(text: str) -> list[str]:
    issues: list[str] = []
    _check_concentration_framing(text, issues)
    return issues


@pytest.mark.parametrize(
    "phrase", ["broad-based", "broad based", "broadly spread", "diversified", "well-distributed"]
)
def test_broad_framing_over_a_concentrated_base_fails(phrase):
    text = f"Growth is {phrase}.\n\n| Top-1 share | 31.0 % |\n"
    out = _conc(text)
    assert len(out) == 1
    assert "CONCENTRATION FRAMING" in out[0]
    assert "top-1=31.0%" in out[0]


def test_broad_framing_over_a_spread_base_passes():
    assert _conc("Growth is broad-based.\n\n| Top-1 share | 9.0 % |\n") == []


def test_no_broad_framing_means_no_check():
    assert _conc("| Top-1 share | 90.0 % |\n") == []


@pytest.mark.parametrize("top1,fails", [(24.9, False), (25.0, True), (40.0, True)])
def test_the_top1_threshold_is_twenty_five_percent(top1, fails):
    out = _conc(f"Growth is diversified.\n\n| Top-1 share | {top1} % |\n")
    assert bool(out) is fails


@pytest.mark.parametrize("hhi,fails", [("1,499", False), ("1,500", True), ("2,400", True)])
def test_the_hhi_threshold_is_fifteen_hundred(hhi, fails):
    out = _conc(f"Growth is diversified.\n\n| HHI | {hhi} |\n")
    assert bool(out) is fails


def test_every_broad_phrase_occurrence_is_reported():
    text = "Broad-based growth. Diversified too.\n\n| Top-1 share | 40.0 % |\n"
    assert len(_conc(text)) == 2


def test_without_either_metric_the_framing_is_allowed():
    assert _conc("Growth is broad-based.") == []


# ─── [7] §S addressable base ───────────────────────────────────────────────

def _addr(text: str) -> list[str]:
    issues: list[str] = []
    _check_addressable_base(text, issues)
    return issues


@pytest.mark.parametrize("projection", ["+$90K", "+$1,200", "+$2.5M", "per 1-point", "per 5-point"])
def test_a_projection_without_a_base_qualifier_fails(projection):
    out = _addr(f"Upside of {projection} is available.")
    assert len(out) == 1
    assert "ADDRESSABLE BASE" in out[0]


@pytest.mark.parametrize("qualifier", ["addressable", "full base", "base of"])
def test_each_base_qualifier_clears_the_check(qualifier):
    assert _addr(f"Upside of +$90K across the {qualifier} 655 dealers.") == []


def test_the_qualifier_window_is_three_hundred_chars_each_way():
    assert _addr("addressable " + _filler(280) + "+$90K") == []
    assert _addr("addressable " + _filler(320) + "+$90K") != []


def test_a_plain_dollar_is_not_a_projection():
    assert _addr("Invoiced $15.64M this year.") == []


def test_base_qualifier_regex_is_word_bounded():
    assert _BASE_QUALIFIER.search("unaddressable") is None
    assert _BASE_QUALIFIER.search("the full base") is not None


# ─── Gate-STOP detection ───────────────────────────────────────────────────

def test_gatestop_detected_by_filename(tmp_path):
    assert _is_gatestop(tmp_path / "bsc_GATESTOP_2026-07-14.md", "no marker") is True


def test_gatestop_detected_by_header_marker(tmp_path):
    assert _is_gatestop(tmp_path / "x.md", "# Org — VALIDATION ARTIFACT, GATE-FAILED\n") is True


def test_the_marker_must_be_in_the_first_500_chars(tmp_path):
    late = ("x" * 600) + "VALIDATION ARTIFACT, GATE-FAILED"
    assert _is_gatestop(tmp_path / "x.md", late) is False


def test_a_standard_draft_is_not_a_gatestop(tmp_path):
    assert _is_gatestop(tmp_path / "sarreid_DRAFT_2026-07-02.md", "# Sarreid\n") is False


# ─── [13] topline parity ───────────────────────────────────────────────────

def _cache(tmp_path: Path, value: str) -> Path:
    d = tmp_path / "cache"
    d.mkdir(exist_ok=True)
    (d / "Q-ECON-00.csv").write_text(f"inv_ltm_net\n{value}\n", encoding="utf-8")
    return d


def test_matching_topline_passes(tmp_path):
    issues: list[str] = []
    md = "## Appendix\n\n| inv_ltm_net | $15,640,000 |\n"
    _check_topline_parity(md, issues, _cache(tmp_path, "15640000"))
    assert issues == []


def test_a_mismatched_topline_is_reported(tmp_path):
    issues: list[str] = []
    md = "## Appendix\n\n| inv_ltm_net | $15,000,000 |\n"
    _check_topline_parity(md, issues, _cache(tmp_path, "15640000"))
    assert len(issues) == 1
    assert "TOPLINE PARITY" in issues[0]


def test_a_sub_dollar_difference_is_tolerated(tmp_path):
    issues: list[str] = []
    md = "## Appendix\n\n| Invoiced LTM | $15,640,000.40 |\n"
    _check_topline_parity(md, issues, _cache(tmp_path, "15640000"))
    assert issues == []


@pytest.mark.parametrize(
    "md,cache_value",
    [
        ("no appendix at all", "15640000"),           # no ## Appendix
        ("## Appendix\n\nno numbers", "15640000"),    # no inv row
        ("## Appendix\n\n| inv_ltm_net | $1 |", ""),  # empty cache value
        ("## Appendix\n\n| inv_ltm_net | $1 |", "not-a-number"),
    ],
)
def test_parity_is_silent_when_either_side_is_unreadable(tmp_path, md, cache_value):
    issues: list[str] = []
    _check_topline_parity(md, issues, _cache(tmp_path, cache_value))
    assert issues == []


def test_parity_is_skipped_without_a_cache_dir():
    issues: list[str] = []
    _check_topline_parity("## Appendix\n\n| inv_ltm_net | $1 |", issues, None)
    assert issues == []


def test_parity_is_skipped_when_the_cache_csv_is_absent(tmp_path):
    issues: list[str] = []
    _check_topline_parity("## Appendix\n\n| inv_ltm_net | $1 |", issues, tmp_path)
    assert issues == []


# ─── smoke() end to end ────────────────────────────────────────────────────

def _draft(sections: list[str], filler_lines: int = 120) -> str:
    body = "\n\n".join(f"{h}\n\nDirectional detail for this section." for h in sections)
    return body + "\n" + ("\nfiller" * filler_lines) + "\n"


def test_a_missing_file_fails_immediately(tmp_path):
    ok, issues = smoke(tmp_path / "absent.md")
    assert ok is False
    assert issues == [f"MISSING: {tmp_path / 'absent.md'}"]


def test_a_complete_standard_draft_passes(tmp_path):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS), encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert (ok, issues) == (True, [])


def test_a_short_standard_draft_is_reported(tmp_path):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS, filler_lines=0), encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert ok is False
    assert any("TOO SHORT:" in i for i in issues)


def test_a_gatestop_artifact_has_a_20_line_floor(tmp_path):
    md = tmp_path / "org_GATESTOP_2026-07-14.md"
    md.write_text(_draft(_GATESTOP_REQUIRED_SECTIONS, filler_lines=25)
                  + "\n| Q-ECON-00 | n/a |\n", encoding="utf-8")
    ok, issues = smoke(md)
    assert (ok, issues) == (True, [])


def test_a_gatestop_artifact_under_twenty_lines_is_reported(tmp_path):
    md = tmp_path / "org_GATESTOP_2026-07-14.md"
    md.write_text(_draft(_GATESTOP_REQUIRED_SECTIONS, filler_lines=0)
                  + "\n| Q-ECON-00 | n/a |\n", encoding="utf-8")
    ok, issues = smoke(md)
    assert any("TOO SHORT (gatestop)" in i for i in issues)


def test_every_missing_section_is_named(tmp_path):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS[:-2]), encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert ok is False
    missing = [i for i in issues if i.startswith("MISSING SECTION")]
    assert len(missing) == 2
    assert "## How to trust these numbers" in missing[1]


def test_a_none_confidence_draft_uses_the_behaviour_only_section_list(tmp_path):
    md = tmp_path / "da_DRAFT_2026-07-09.md"
    md.write_text(_draft(_NONE_REQUIRED_SECTIONS), encoding="utf-8")
    ok, issues = smoke(md, confidence="NONE")
    assert (ok, issues) == (True, [])


def test_the_same_draft_fails_the_standard_list(tmp_path):
    md = tmp_path / "da_DRAFT_2026-07-09.md"
    md.write_text(_draft(_NONE_REQUIRED_SECTIONS), encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert ok is False
    assert any("## Do this week" in i for i in issues)


def test_a_none_gatestop_file_uses_the_behaviour_only_list_and_needs_no_appendix(tmp_path):
    md = tmp_path / "bsc_GATESTOP_2026-07-14.md"
    md.write_text(_draft(_NONE_REQUIRED_SECTIONS), encoding="utf-8")
    ok, issues = smoke(md, confidence="NONE")
    assert (ok, issues) == (True, [])


def test_a_legacy_gatestop_without_an_appendix_is_reported(tmp_path):
    md = tmp_path / "x_GATESTOP_2026-07-14.md"
    md.write_text(_draft(_GATESTOP_REQUIRED_SECTIONS[:2]), encoding="utf-8")
    ok, issues = smoke(md)
    assert "APPENDIX block missing entirely" in issues


def test_an_appendix_without_the_trace_reference_is_reported(tmp_path):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS + ["## Appendix"]), encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert "APPENDIX missing Q-ECON-00 trace reference" in issues


@pytest.mark.parametrize("leak", ["{{ ra.quiet_seats }}", "{% if x %}"])
def test_jinja_leakage_is_reported(tmp_path, leak):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS) + f"\n{leak}\n", encoding="utf-8")
    ok, issues = smoke(md, confidence="STRONG")
    assert ok is False
    assert any(i.startswith("JINJA LEAK: 1") for i in issues)


def test_smoke_runs_the_q_r_and_s_gates_together(tmp_path):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    body = _draft(_STANDARD_REQUIRED_SECTIONS).replace(
        "## The 60-second read\n\nDirectional detail for this section.",
        "## The 60-second read\n\n$1.45M in play. Growth is broad-based, with +$90K upside.\n\n"
        "| Top-1 share | 40.0 % |",
    )
    md.write_text(body, encoding="utf-8")
    ok, issues = smoke(md, confidence="PARTIAL")
    assert ok is False
    kinds = {i.split(":")[0] for i in issues}
    assert {"SENSITIVITY HEDGE", "CONCENTRATION FRAMING", "ADDRESSABLE BASE"} <= kinds


# ─── CLI ───────────────────────────────────────────────────────────────────

def test_cli_returns_zero_and_prints_pass(tmp_path, capsys, monkeypatch):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text(_draft(_STANDARD_REQUIRED_SECTIONS), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["smoke_check", str(md), "--confidence", "STRONG"])
    assert main() == 0
    assert capsys.readouterr().out.startswith("PASS:")


def test_cli_returns_one_and_lists_the_issues(tmp_path, capsys, monkeypatch):
    md = tmp_path / "org_DRAFT_2026-07-02.md"
    md.write_text("too short\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["smoke_check", str(md)])
    assert main() == 1
    out = capsys.readouterr().out
    assert out.startswith("FAIL:")
    assert "TOO SHORT" in out
