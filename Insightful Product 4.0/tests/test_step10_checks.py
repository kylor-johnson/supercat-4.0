"""Characterization — Step-10 checks [8] [9] [11] [12] + the CLI (W2 / Phase 3).

Check [4] (the §P sweep) has its own file, `test_step10_forbidden_vocab.py`.

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every behavior below is the one we want.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from report_render.step10_check import (
    _HEADER_SELECTORS,
    _check_anchors,
    _check_number_reconciliation,
    _check_phrase_echo,
    _check_structure,
    _extract_numbers,
    _normalize,
    main,
    run_checks,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


# ─── [11] structure pairing ────────────────────────────────────────────────

def test_structure_passes_on_a_well_formed_document():
    html = '<html><body><details id="a"><section><table></table></section></details></body></html>'
    assert _check_structure(Path("x.html"), html, _soup(html)) == []


def test_duplicate_ids_are_reported():
    html = '<div id="summary"></div><div id="summary"></div>'
    out = _check_structure(Path("x.html"), html, _soup(html))
    assert len(out) == 1
    assert "duplicate id(s)" in out[0] and "summary" in out[0]


@pytest.mark.parametrize("tag", ["details", "section", "table"])
def test_unclosed_tags_are_reported_per_tag(tag):
    """The pairing check counts raw markup, not the parsed tree, so a missing
    close tag is caught even though lxml would silently repair it."""
    html = f"<{tag}><{tag}></{tag}>"
    out = _check_structure(Path("x.html"), html, _soup(html))
    assert len(out) == 1
    assert f"{tag} open/close mismatch" in out[0]
    assert "2 open vs 1 close" in out[0]


def test_the_check_names_the_file():
    html = '<div id="a"></div><div id="a"></div>'
    assert "report.html" in _check_structure(Path("out/report.html"), html, _soup(html))[0]


# ─── [12] anchor resolution ────────────────────────────────────────────────

def test_resolved_in_document_anchors_pass():
    html = '<a href="#risk">go</a><section id="risk"></section>'
    assert _check_anchors(Path("x.html"), _soup(html)) == []


def test_a_broken_in_document_anchor_is_reported_with_its_label():
    html = '<a href="#nowhere">See the exposure</a><section id="risk"></section>'
    out = _check_anchors(Path("x.html"), _soup(html))
    assert len(out) == 1
    assert "#nowhere" in out[0]
    assert "'See the exposure'" in out[0]


@pytest.mark.parametrize("href", ["#", "https://example.com", "mailto:a@b.co", "report.pdf"])
def test_external_and_empty_hrefs_are_ignored(href):
    html = f'<a href="{href}">x</a>'
    assert _check_anchors(Path("x.html"), _soup(html)) == []


# ─── [9] verbatim 12-word phrase echo ──────────────────────────────────────

_PHRASE = "the swan s nest is down fifty six percent in six months"  # 12 words


def _two_site_doc(phrase_a: str, phrase_b: str) -> str:
    return (
        f'<section id="summary"><div class="hero-sub">{phrase_a}</div></section>'
        f'<section id="thisweek"><div class="section-sub">{phrase_b}</div></section>'
    )


def test_a_twelve_word_phrase_shared_by_two_fragments_is_reported():
    """The two fragments must differ somewhere — see
    `test_an_exact_duplicate_fragment_is_invisible_to_check_9`."""
    out = _check_phrase_echo(_soup(_two_site_doc(f"{_PHRASE} one", f"{_PHRASE} two")))
    assert len(out) == 1
    assert _PHRASE in out[0]


def test_an_exact_duplicate_fragment_is_invisible_to_check_9():
    """`_check_phrase_echo` requires >= 2 DISTINCT fragment texts, so the most
    obvious echo — the identical string in two places — reports nothing.
    Pinned, not endorsed (W2 finding F-3)."""
    assert _check_phrase_echo(_soup(_two_site_doc(_PHRASE, _PHRASE))) == []


@pytest.mark.xfail(
    reason="W2 finding F-3: check [9] de-dupes on fragment text, so a verbatim "
           "duplicate header in two sections is never reported (Phase 8)",
    strict=True,
)
def test_check_9_should_catch_a_verbatim_duplicate():
    assert _check_phrase_echo(_soup(_two_site_doc(_PHRASE, _PHRASE))) != []


def test_eleven_words_is_below_the_window():
    eleven = " ".join(_PHRASE.split()[:11])
    assert _check_phrase_echo(_soup(_two_site_doc(eleven, eleven))) == []


def test_the_same_fragment_appearing_once_is_not_an_echo():
    html = f'<section id="summary"><div class="hero-sub">{_PHRASE}</div></section>'
    assert _check_phrase_echo(_soup(html)) == []


def test_two_sites_with_identical_text_in_the_same_section_still_count():
    html = (
        f'<section id="summary"><div class="hero-sub">{_PHRASE} one</div>'
        f'<div class="ceo-title">{_PHRASE} two</div></section>'
    )
    assert len(_check_phrase_echo(html and _soup(html))) >= 1


def test_body_prose_is_out_of_scope_for_the_echo_check():
    """Step 10 [9] targets headers/subs/callouts — `.prose`, `.ceo-body`,
    `.play-sub` and `.coaching-body` legitimately repeat the summary teaser."""
    html = (
        f'<section id="summary"><div class="hero-sub">{_PHRASE}</div>'
        f'<p class="prose">{_PHRASE}</p></section>'
    )
    assert _check_phrase_echo(_soup(html)) == []


def test_sections_outside_the_first_four_are_out_of_scope():
    html = (
        f'<section id="team"><div class="section-sub">{_PHRASE}</div></section>'
        f'<section id="risk"><div class="section-sub">{_PHRASE}</div></section>'
    )
    assert _check_phrase_echo(_soup(html)) == []


def test_smart_quotes_are_normalized_before_comparison():
    curly = "the swan’s nest is down fifty six percent in six months and counting"
    straight = curly.replace("’", "'")
    assert _check_phrase_echo(_soup(_two_site_doc(curly + " one", straight + " two"))) != []


def test_min_words_is_tunable():
    six = " ".join(_PHRASE.split()[:6])
    doc = _soup(_two_site_doc(f"{six} one", f"{six} two"))
    assert _check_phrase_echo(doc) == []
    assert _check_phrase_echo(doc, min_words=6) != []


def test_header_selector_list_shape():
    """The selector list is the [9] scope contract; Phase 8 must not shrink it
    silently."""
    assert "h2" in _HEADER_SELECTORS
    assert ".hero-sub" in _HEADER_SELECTORS
    assert ".ceo-title" in _HEADER_SELECTORS
    for excluded in (".prose", ".ceo-body", ".play-sub", ".coaching-body"):
        assert excluded not in _HEADER_SELECTORS


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("a’b", "a'b"),
        ("a“b”", 'a"b"'),
        ("a   b\n c", "a b c"),
        ("  padded  ", "padded"),
    ],
)
def test_normalize(raw, expected):
    assert _normalize(raw) == expected


# ─── [8] number reconciliation ─────────────────────────────────────────────

@pytest.mark.parametrize(
    "text,expected",
    [
        ("$1.45M in play", {"$1.45M": 1}),
        ("$12,345 invoiced", {"$12,345": 1}),
        ("down -56%", {"-56%": 1}),
        ("up +29 %", {"+29 %": 1}),
        # the count pattern needs a 2-5 digit number AND a unit noun
        ("655 dealers and 25 reps", {"655 dealers": 1, "25 reps": 1}),
        ("7 calls this week", {}),   # 1 digit — below the floor
    ],
)
def test_extract_numbers_token_shapes(text, expected):
    counts = _extract_numbers(text)
    for tok, n in expected.items():
        assert counts[tok] == n


def test_counts_repeat_tokens():
    assert _extract_numbers("$1.45M and $1.45M")["$1.45M"] == 2


def test_minus_glyph_variants_canonicalize_to_a_hyphen():
    counts = _extract_numbers("−56% and –56% and -56%")
    assert counts["-56%"] == 3


def test_a_repeated_html_number_absent_from_the_md_is_reported():
    out = _check_number_reconciliation("$9.9M here and $9.9M there", "no numbers")
    assert len(out) == 1
    assert "$9.9M" in out[0] and "appears 2×" in out[0]


def test_a_repeated_md_number_that_never_reached_the_html_is_reported():
    out = _check_number_reconciliation("nothing", "$9.9M here and $9.9M there")
    assert len(out) == 1
    assert "never reached the HTML" in out[0]


def test_a_number_appearing_once_is_not_reconciled():
    assert _check_number_reconciliation("$9.9M once", "no numbers") == []


def test_matching_numbers_pass():
    assert _check_number_reconciliation("$9.9M and $9.9M", "$9.9M") == []


# ─── run_checks + CLI ──────────────────────────────────────────────────────

_CLEAN_DOC = """<html><body><div class="page">
<section id="summary"><div class="hero-sub">Invoiced $15.64M this year</div></section>
<section id="thisweek"><a href="#risk">See the exposure</a></section>
<section id="risk"><p class="prose">The tail of the watchlist.</p></section>
</div></body></html>"""


def test_run_checks_passes_a_clean_document(tmp_path):
    html = tmp_path / "clean.html"
    html.write_text(_CLEAN_DOC, encoding="utf-8")
    passing, results = run_checks(html)
    assert passing is True
    assert set(results) == {"4", "8", "9", "11", "12"}
    assert all(v == [] for v in results.values())


def test_check_8_is_skipped_without_an_md(tmp_path):
    html = tmp_path / "clean.html"
    html.write_text(_CLEAN_DOC.replace("$15.64M this year", "$9.9M and $9.9M"), encoding="utf-8")
    passing, results = run_checks(html)
    assert results["8"] == []
    assert passing is True


def test_check_8_runs_when_an_md_is_given(tmp_path):
    html = tmp_path / "x.html"
    html.write_text(_CLEAN_DOC.replace("$15.64M this year", "$9.9M and $9.9M"), encoding="utf-8")
    md = tmp_path / "x.md"
    md.write_text("no numbers here", encoding="utf-8")
    passing, results = run_checks(html, md)
    assert passing is False
    assert results["8"] and "$9.9M" in results["8"][0]


def test_a_missing_md_path_is_treated_as_no_md(tmp_path):
    html = tmp_path / "x.html"
    html.write_text(_CLEAN_DOC, encoding="utf-8")
    passing, results = run_checks(html, tmp_path / "absent.md")
    assert passing is True


def test_cli_returns_zero_on_a_clean_document(tmp_path, capsys):
    html = tmp_path / "clean.html"
    html.write_text(_CLEAN_DOC, encoding="utf-8")
    assert main(["--html", str(html)]) == 0
    assert "PASS" in capsys.readouterr().out


def test_cli_returns_one_and_prints_detail_on_failure(tmp_path, capsys):
    html = tmp_path / "bad.html"
    html.write_text('<div class="page"><section id="x"><p>Run the playbook.</p></section></div>',
                    encoding="utf-8")
    assert main(["--html", str(html)]) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out and "playbook" in out


def test_cli_quiet_suppresses_the_detail(tmp_path, capsys):
    html = tmp_path / "bad.html"
    html.write_text('<div class="page"><section id="x"><p>Run the playbook.</p></section></div>',
                    encoding="utf-8")
    assert main(["--html", str(html), "--quiet"]) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out and "playbook" not in out


def test_cli_returns_two_when_the_html_is_missing(tmp_path, capsys):
    assert main(["--html", str(tmp_path / "nope.html")]) == 2
    assert "ERROR" in capsys.readouterr().err


# ─── The real cohort (skip when the gitignored outputs are absent) ──────────

SHIP_HTML = [
    "Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html",
    "Hubbardton_Forge_CEO_intelligence_report_2026-07-02.html",
    "Dainolite_Ltd._CEO_intelligence_report_2026-07-09.html",
    "Currey_and_Company_CEO_intelligence_report_2026-07-02.html",
]


@pytest.mark.parametrize("name", SHIP_HTML, ids=[n.split("_CEO")[0] for n in SHIP_HTML])
def test_shipped_reports_pass_every_step10_html_check(name):
    path = OUTPUTS / name
    if not path.exists():
        pytest.skip("no tracked output (outputs/ is gitignored)")
    passing, results = run_checks(path)
    assert passing, {k: v for k, v in results.items() if v}
