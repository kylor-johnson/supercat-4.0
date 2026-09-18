"""Characterization — §2-§11 + Gate-STOP rendering in `report_render/sections.py`.

W2 / Phase 3. Covers collapse-section wrapping, the table/cell cleanup path,
the call-list and team row tints, play cards, coaching cards, nested details,
callouts, the subsection walkers (H3 and bold-colon soft boundaries), the
methodology pair and the Mode-2 Gate-STOP assembly.

§1 has its own file, `test_sections_summary.py`.

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every behavior below is the one we want.
"""
from __future__ import annotations

import pytest

from report_render.md_parse import Chunk, ParsedReport, parse_md
from report_render.sections import (
    _build_callout,
    _build_nested_details,
    _build_play_card,
    _call_list_row_class,
    _clean_cell,
    _collect_h3_titles,
    _default_sub_blurb,
    _enrich_title,
    _generic_row_class,
    _parse_md_table,
    _pick_card_badge_class,
    _pick_card_tone,
    _render_freeform_blocks,
    _render_table_with_classes,
    _smart_titlecase,
    _split_card_stats_and_body,
    _split_heading_prefix,
    _split_quotes_vs_prose,
    _strip_em_wrappers,
    _strip_md_inline,
    _team_row_class,
    _truncate_clean,
    _try_render_coaching_card,
    _wrap_collapse_section,
    _wrap_open_section,
    _wrap_prose,
    render_base,
    render_channels,
    render_gatestop,
    render_growth,
    render_methodology,
    render_products,
    render_risk,
    render_team,
    render_thismonth,
    render_thisweek,
)


def _chunk(section_id: str, heading: str, body: str) -> Chunk:
    return Chunk(section_id=section_id, heading=heading, body_md=body)


# ─── Inline-text helpers ───────────────────────────────────────────────────

@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Text *(ESTIMATED)*", "Text"),
        ("Text  *(a note)*  ", "Text"),
        ("Text (not italic)", "Text (not italic)"),
    ],
)
def test_strip_em_wrappers(raw, expected):
    assert _strip_em_wrappers(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("**bold**", "bold"),
        ("*em*", "em"),
        ("`code`", "code"),
        ("**a** and *b* and `c`", "a and b and c"),
    ],
)
def test_strip_md_inline(raw, expected):
    assert _strip_md_inline(raw) == expected


@pytest.mark.parametrize(
    "heading,expected",
    [
        ("What this report can't see — and what to add next", "What this report can't see"),
        ("Title – suffix", "Title"),
        ("No separator here", "No separator here"),
    ],
)
def test_split_heading_prefix(heading, expected):
    assert _split_heading_prefix(heading) == expected


def test_truncate_clean_breaks_on_a_word_boundary():
    assert _truncate_clean("short", 40) == "short"
    out = _truncate_clean("one two three four five six seven", 20)
    assert out.endswith("…") and " …" not in out and len(out) <= 21


# ─── Cell cleanup (P0-5 render-time normalization) ─────────────────────────

@pytest.mark.parametrize(
    "raw,expected",
    [
        ("FRANCE AND SONS", "France and Sons"),
        ("OP JENKINS FURNITURE & DESIGN", "OP Jenkins Furniture & Design"),
        ("ENGLISH GEORGIAN AMERICA LLC", "English Georgian America LLC"),
        # "THE" at position 0 hits the short-all-caps initialism branch, so it
        # stays shouted — see test_the_render_time_titlecaser_diverges_from_gather.
        ("THE SWAN'S NEST INC", "THE Swan's Nest Inc"),
        ("ACME LTDA", "Acme Ltda"),
        ("A COMPANY", "A Company"),
    ],
)
def test_smart_titlecase(raw, expected):
    assert _smart_titlecase(raw) == expected


def test_the_render_time_titlecaser_matches_the_data_layer_on_most_names():
    from pipeline.gather import normalize_account_name
    for raw in ("FRANCE AND SONS", "ENGLISH GEORGIAN AMERICA LLC"):
        assert _smart_titlecase(raw) == normalize_account_name(raw)


@pytest.mark.xfail(
    reason="W2 finding F-6: `_smart_titlecase` keeps a leading 3-letter ALL-CAPS "
           "word (THE / AND) shouted, where `gather.normalize_account_name` "
           "title-cases it — two casers, two answers (Phase 6)",
    strict=True,
)
def test_the_render_time_titlecaser_diverges_from_gather():
    from pipeline.gather import normalize_account_name
    raw = "THE SWAN'S NEST INC"
    assert _smart_titlecase(raw) == normalize_account_name(raw)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("FRANCE  AND   SONS", "France and Sons"),   # whitespace runs collapse
        ("Mixed Case Co", "Mixed Case Co"),          # mixed case untouched
        ("1489", "1489"),                            # a code, not a name
        ("$1.45M", "$1.45M"),                        # formatted values untouched
        ("", ""),
        ("AB", "AB"),                                # < 3 letters: left alone
    ],
)
def test_clean_cell(raw, expected):
    assert _clean_cell(raw) == expected


# ─── Table rendering ───────────────────────────────────────────────────────

def test_render_table_emits_a_wrapped_table_with_a_thead():
    html = _render_table_with_classes([["Account", "Value"], ["FRANCE AND SONS", "$402K"]])
    assert html.startswith('<div class="table-wrap"><table>')
    assert "<thead><tr><th>Account</th><th>Value</th></tr></thead>" in html
    assert "<td>France and Sons</td>" in html   # body cells are cleaned
    assert html.endswith("</tbody></table></div>")


def test_header_cells_are_not_re_cased():
    html = _render_table_with_classes([["ACCOUNT NAME", "VALUE"], ["a", "b"]])
    assert "<th>ACCOUNT NAME</th>" in html


def test_render_table_of_nothing_is_empty():
    assert _render_table_with_classes([]) == ""


def test_row_class_fn_tints_rows():
    html = _render_table_with_classes(
        [["a", "b"], ["x", "y"]], row_class_fn=lambda cells, idx: "row-danger"
    )
    assert '<tr class="row-danger">' in html


@pytest.mark.parametrize(
    "cells,expected",
    [
        (["France and Sons", "-57%"], "row-danger"),
        (["OP Jenkins", "-22%"], "row-warn"),
        (["Quiet Co", "-8%"], None),
        (["Grower Inc", "beat-skip"], "row-highlight"),
        (["Grower Inc", "growing"], "row-highlight"),
        (["Grower Inc", "+45"], "row-highlight"),
        (["Cluster", "-57% pattern"], "row-warn"),
        (["Flat Co", "no signal"], None),
    ],
)
def test_call_list_row_class(cells, expected):
    assert _call_list_row_class(cells, 0) == expected


@pytest.mark.parametrize(
    "cells,expected",
    [(["Rep", "-22%"], "row-warn"), (["Rep", "-8%"], None), (["Rep", "+12%"], None)],
)
def test_team_row_class(cells, expected):
    assert _team_row_class(cells, 0) == expected


@pytest.mark.parametrize(
    "cells,idx,expected",
    [
        (["**Total**", "$1.45M"], 0, "row-highlight"),
        (["**Total**", "$1.45M"], 1, None),
        (["Plain", "$1.45M"], 0, None),
        (["**Total**", "no money"], 0, None),
    ],
)
def test_generic_row_class(cells, idx, expected):
    assert _generic_row_class(cells, idx) == expected


# ─── Section wrappers ──────────────────────────────────────────────────────

def test_wrap_open_section_escapes_its_title():
    html = _wrap_open_section("summary", "A & B", "<p>body</p>")
    assert 'id="summary"' in html
    assert "A &amp; B" in html


def test_wrap_collapse_section_defaults_to_closed_with_an_expand_hint():
    html = _wrap_collapse_section("risk", "Risk", "<p>b</p>")
    assert '<details class="section-collapse" id="risk">' in html
    assert " open" not in html.split("\n")[1]
    assert "expand-hint" in html


def test_an_open_collapse_section_drops_the_expand_hint():
    html = _wrap_collapse_section("thisweek", "Do this week", "<p>b</p>", is_open=True)
    assert 'id="thisweek" open>' in html
    assert "expand-hint" not in html


@pytest.mark.parametrize("variant", ["urgent", "month", "quarter"])
def test_collapse_variants_land_in_the_class_list(variant):
    html = _wrap_collapse_section("x", "T", "b", variant=variant)
    assert f'class="section-collapse {variant}"' in html


def test_collapse_blurbs_are_optional_and_html_safe():
    bare = _wrap_collapse_section("x", "T", "b")
    assert "section-sub" not in bare and "section-contents" not in bare
    rich = _wrap_collapse_section("x", "T", "b", contents_blurb="A &middot; B", sub_blurb="Sub")
    assert '<div class="section-contents">A &middot; B</div>' in rich
    assert '<div class="section-sub">Sub</div>' in rich


def test_wrap_prose_tags_every_paragraph():
    assert _wrap_prose("<p>a</p><p>b</p>") == '<p class="prose">a</p><p class="prose">b</p>'
    assert _wrap_prose("") == ""
    assert _wrap_prose("<table></table>") == "<table></table>"


@pytest.mark.parametrize(
    "heading,expected",
    [
        ("Do this week — 7 calls", "Do this week &middot; 7 calls"),
        ("Do this week · 7 calls", "Do this week &middot; 7 calls"),
        ("Do this week - 7 calls", "Do this week &middot; 7 calls"),
        ("No separator", "No separator"),
    ],
)
def test_enrich_title(heading, expected):
    assert _enrich_title(heading) == expected


def test_enrich_title_colors_the_suffix_when_an_accent_is_given():
    out = _enrich_title("Do this week — 7 calls", accent_class="var(--danger)")
    assert '<span style="color: var(--danger);">7 calls</span>' in out


# ─── _default_sub_blurb ────────────────────────────────────────────────────

def test_sub_blurb_takes_the_first_real_sentence():
    md = "| a | b |\n| --- | --- |\n\n### A heading\n\n**A lead-in:**\n\n> A quote\n\nThe real sentence. And more."
    assert _default_sub_blurb(md) == "The real sentence."


def test_sub_blurb_is_empty_when_there_is_no_prose():
    assert _default_sub_blurb("| a | b |\n| --- | --- |") == ""
    assert _default_sub_blurb("") == ""


# ─── §2 Do this week ───────────────────────────────────────────────────────

_THISWEEK = """Seven calls worth making. Each one is a named account.

| Account | Stakes |
| --- | --- |
| FRANCE AND SONS | -57% · $402K |
| GROWER INC | beat-skip |

**Don't conflate** the declines with the beat-skips — they are two different conversations.

*How these were chosen*

Ranked by actionability: dollars in play, slope, and days since last order.
"""


def test_thisweek_renders_an_open_urgent_collapsible():
    html = render_thisweek(_chunk("thisweek", "Do this week — 7 calls", _THISWEEK))
    assert '<details class="section-collapse urgent" id="thisweek" open>' in html
    assert "Click to expand the call list" not in html   # open sections hide the hint


def test_thisweek_tints_the_call_list_rows():
    html = render_thisweek(_chunk("thisweek", "Do this week", _THISWEEK))
    assert '<tr class="row-danger">' in html
    assert '<tr class="row-highlight">' in html
    assert "<td>France and Sons</td>" in html


def test_thisweek_lifts_the_first_sentence_into_the_section_sub():
    html = render_thisweek(_chunk("thisweek", "Do this week", _THISWEEK))
    assert '<div class="section-sub">Seven calls worth making.</div>' in html
    assert "Each one is a named account." in html


def test_thisweek_builds_the_alert_callout_and_the_nested_details():
    html = render_thisweek(_chunk("thisweek", "Do this week", _THISWEEK))
    assert '<div class="callout alert">' in html
    assert '<details class="nested">' in html
    assert "How these were chosen &middot; selection logic" in html
    assert "Ranked by actionability" in html


def test_a_blockquote_becomes_an_insight_callout():
    html = render_thisweek(_chunk("thisweek", "Do this week", "Lead.\n\n> A standing insight."))
    assert '<div class="callout insight">' in html


def test_thisweek_falls_back_to_a_default_contents_blurb():
    html = render_thisweek(_chunk("thisweek", "Do this week", "Lead sentence."))
    assert "Call list · talking points" in html


# ─── _build_callout ────────────────────────────────────────────────────────

def test_a_callout_lifts_a_bold_lead_as_its_title():
    html = _build_callout("**Don't conflate.** Two different conversations.", "alert")
    assert '<div class="callout alert">' in html
    assert '<div class="callout-title">Don\'t conflate</div>' in html
    assert "Two different conversations." in html


def test_a_callout_without_a_bold_lead_has_no_title():
    html = _build_callout("Just body prose.", "insight")
    assert "callout-title" not in html


def test_a_blockquote_callout_strips_its_markers():
    html = _build_callout("> Line one\n> Line two", "insight")
    assert "&gt;" not in html and "Line one" in html


def test_nested_details_with_an_empty_body():
    html = _build_nested_details("How these were chosen", "")
    assert '<details class="nested">' in html
    assert '<div class="nested-body"></div>' in html


# ─── §3 Do this month (play cards) ─────────────────────────────────────────

_THISMONTH = """Three plays, ranked by dollars.

### 1. Depth in the Lilac book

Every Lilac dealer already buys Jupe, so the gap is depth, not breadth.

| | |
| --- | --- |
| Target dealers | **24** |

> Worth noting: the cross-sell gap is zero.

**$90K – $160K product upside · ESTIMATED**

### 2. The second-order push

212 first-time dealers never placed a second order.

| Dealer | Value |
| --- | --- |
| ACME LIGHTING | $12K |
"""


def test_thismonth_builds_one_play_card_per_h3():
    html = render_thismonth(_chunk("thismonth", "Do this month — 3 plays", _THISMONTH))
    assert html.count('class="play-card"') == 2
    assert '<span class="play-card-num">Play 01</span>' in html
    assert '<span class="play-card-num">Play 02</span>' in html
    assert "<h4>Depth in the Lilac book</h4>" in html


def test_a_play_card_renders_metrics_tables_callouts_and_the_upside_chip():
    html = render_thismonth(_chunk("thismonth", "Do this month", _THISMONTH))
    assert '<div class="metrics">' in html           # the 2-col unlabeled table
    assert '<div class="table-wrap">' in html        # the labelled one
    assert '<div class="callout insight">' in html
    assert '<div class="play-upside">$90K – $160K product upside · ESTIMATED</div>' in html
    assert '<p class="play-sub">' in html


def test_thismonth_blurb_and_contents_come_from_the_intro_and_the_h3s():
    html = render_thismonth(_chunk("thismonth", "Do this month", _THISMONTH))
    assert '<div class="section-sub">Three plays, ranked by dollars.</div>' in html
    assert "Depth in the Lilac book · The second-order push" in html
    assert "Click to expand the 2 plays" in html


def test_thismonth_without_h3s_renders_flat_prose():
    html = render_thismonth(_chunk("thismonth", "Do this month", "No plays qualified this month."))
    assert "play-card" not in html
    assert '<p class="prose">No plays qualified this month.</p>' in html
    assert "Click to expand<" in html


@pytest.mark.parametrize(
    "line",
    [
        "**$90K product upside**",
        "**A directional estimate**",
        "**+$45K**",
        "**Real upside worth chasing**",
    ],
)
def test_upside_chip_shapes(line):
    html = _build_play_card(1, "1. Title", f"Body prose.\n\n{line}")
    assert "play-upside" in html


def test_a_bold_line_that_is_not_an_upside_stays_prose():
    html = _build_play_card(1, "1. Title", "Body.\n\n**A bolded sentence with no money.**")
    assert "play-upside" not in html


def test_collect_h3_titles_truncates_and_caps_at_four():
    text = "\n".join(f"### {i}. Title number {i}" for i in range(1, 7))
    out = _collect_h3_titles(text)
    assert out.count("·") == 3


# ─── §5 / §8 / §10 — subsection walkers ────────────────────────────────────

_GROWTH_H3 = """The engine has three layers.

### Layer 1 — same-dealer spend

| | |
| --- | --- |
| Same-dealer lift | **+29%** |

### Layer 2 — new dealers

| Dealer | Value |
| --- | --- |
| ACME LIGHTING | $12K |

> An opportunity worth naming.
"""


def test_growth_walks_h3_subsections():
    html = render_growth(_chunk("growth", "The growth engine — three layers", _GROWTH_H3))
    assert html.count('class="subsection"') == 2
    assert '<h3 class="subsection-title">Layer 1 &middot; same-dealer spend</h3>' in html
    assert '<div class="metrics">' in html
    assert '<div class="callout opportunity">' in html
    assert 'style="margin-top: 0;"' in html   # the first subsection only
    assert "same-dealer spend · new dealers" in html


def test_growth_renders_the_intro_before_the_first_h3():
    html = render_growth(_chunk("growth", "The growth engine", _GROWTH_H3))
    # Phase 4 render fix: the intro shows ONCE, in the collapsed-section
    # teaser. It used to print in the teaser AND again as the body's first
    # paragraph, so every section opened by repeating its own header.
    assert '<div class="section-sub">The engine has three layers.</div>' in html
    assert html.count("The engine has three layers.") == 1


_CHANNELS_SOFT = """Channel mix, in one view.

| Channel | Share |
| --- | --- |
| Platform | 41% |

**eCat as a channel:**

The platform carries 41% of confirmed orders.

**Phone and email:**

The rest still arrives the old way.
"""


def test_channels_splits_on_bold_colon_soft_boundaries_when_there_are_no_h3s():
    html = render_channels(_chunk("channels", "Channels", _CHANNELS_SOFT))
    assert html.count('class="subsection"') == 2
    assert '<h3 class="subsection-title">eCat as a channel</h3>' in html
    assert '<h3 class="subsection-title">Phone and email</h3>' in html
    assert "eCat as a channel · Phone and email" in html
    # the blocks before the first boundary stay flat
    assert '<p class="prose">Channel mix, in one view.</p>' in html


def test_channels_with_neither_h3s_nor_soft_boundaries_renders_flat():
    html = render_channels(_chunk("channels", "Channels", "One flat paragraph."))
    assert "subsection" not in html
    assert "Channel mix · eCat as a channel" in html   # the fallback blurb


def test_products_falls_back_to_a_default_contents_blurb():
    html = render_products(_chunk("products", "What's selling", "Flat prose."))
    assert "Top items · the cross-sell" in html


def test_base_renders_freeform_blocks():
    html = render_base(_chunk("base", "The dealer base", _GROWTH_H3))
    assert 'id="base"' in html
    assert "In · out · returning" in html


def test_render_freeform_blocks_falls_back_when_a_table_will_not_parse():
    out = _render_freeform_blocks("| A | B |\n| --- | --- |\nnot a row")
    assert 'class="prose"' in out or "<table>" in out


# ─── §7 Risk ───────────────────────────────────────────────────────────────

def test_risk_renders_one_tinted_table():
    md = "The tail of the watchlist.\n\n| Account | Slope |\n| --- | --- |\n| FADING CO | -61% |\n\n> A closing note."
    html = render_risk(_chunk("risk", "Full risk watchlist — 30 dealers", md))
    assert 'id="risk"' in html
    assert '<tr class="row-danger">' in html
    assert '<div class="callout insight">' in html
    assert "tail of the watchlist" in html
    assert "Positions 6 – 25" not in html  # was hardcoded, contradicted the rows


# ─── §6 Team ───────────────────────────────────────────────────────────────

_TEAM = """### Leaderboard

| Rep | LTM | Change |
| --- | --- | --- |
| Clyde Barnard | $1.2M | -22% |
| Ann Reyes | $900K | +4% |

### Coaching cards

> **Card 1 — Clyde Barnard · 3 at-risk accounts**
> **$402K at risk** · 3 accounts. Book a territory review this week.

> **Card 2 — Ann Reyes · both accounts growing**
> Her book is growing on two accounts. Keep the cadence.

**A note on discount discipline.** Nothing here is out of band.
"""


def test_team_renders_the_leaderboard_and_the_coaching_cards():
    html = render_team(_chunk("team", "The team", _TEAM))
    assert html.count('class="coaching-card') == 2
    assert '<div class="coaching-name">Card 1 &middot; Clyde Barnard</div>' in html
    assert '<span class="badge info">3 at-risk accounts</span>' in html
    assert '<span class="badge ok">both accounts growing</span>' in html
    assert '<tr class="row-warn">' in html          # the -22% leaderboard row
    assert '<div class="callout insight">' in html  # the discount-discipline note


def test_team_without_h3s_still_renders_its_subsection_body():
    body = _TEAM.split("### Coaching cards", 1)[1]
    html = render_team(_chunk("team", "The team", body))
    assert "subsection" not in html
    assert html.count('class="coaching-card') == 2


def test_a_coaching_card_carries_its_stats_line():
    html = _try_render_coaching_card(
        "> **Card 1 — Clyde Barnard · 3 at-risk accounts**\n"
        "> **$402K at risk** · 3 accounts. Book a territory review."
    )
    assert '<div class="coaching-stats">' in html
    assert "Book a territory review." in html


def test_a_blockquote_that_is_not_a_card_returns_none():
    assert _try_render_coaching_card("> Just a quote, no card header.") is None


def test_a_card_without_a_badge_renders_no_badge_span():
    html = _try_render_coaching_card("> **Card 3 — Sam Ortiz**\n> Plain body prose.")
    assert "badge" not in html
    assert "coaching-stats" not in html


@pytest.mark.parametrize(
    "text,expected",
    [
        ("all the dollars sit on 1 account", "alarm"),
        ("the book is growing", "growing"),
        ("a 7-account pattern", "pattern"),
        ("nothing tonal", ""),
    ],
)
def test_pick_card_tone(text, expected):
    assert _pick_card_tone(text) == expected


@pytest.mark.parametrize(
    "badge,expected",
    [
        ("all the dollars on 1 account", "danger"),
        ("only top-10 book shrank", "danger"),
        ("both accounts growing", "ok"),
        ("3 at-risk accounts", "info"),
        ("steady", "muted"),
    ],
)
def test_pick_card_badge_class(badge, expected):
    assert _pick_card_badge_class(badge) == expected


def test_a_short_first_clause_is_not_lifted_as_stats():
    stats, body = _split_card_stats_and_body("Her book is growing. Keep the cadence.")
    assert stats == ""
    assert body.startswith("Her book is growing.")


def test_split_quotes_vs_prose_separates_the_runs():
    segs = _split_quotes_vs_prose("prose one\n\n> quote a\n\n> quote b\n\nprose two")
    kinds = [k for k, _ in segs]
    assert kinds.count("quote") == 2
    assert kinds.count("prose") == 2


# ─── §11 Methodology ───────────────────────────────────────────────────────

_GAPS = """This report reads one feed.

- No cost data
- No returns
- No competitor view

**Two specific upgrades worth queuing:**

**A cost feed (any channel).** Margin would replace revenue as the lens.

| Gap | Impact |
| --- | --- |
| Cost | High |

> A closing note on scope.
"""


def test_methodology_combines_both_chunks_into_one_collapsible():
    html = render_methodology(
        _chunk("methodology_gaps", "What this report can't see — and what to add next", _GAPS),
        _chunk("methodology_trust", "How to trust these numbers", "Every figure traces to one query."),
    )
    assert html.count('id="methodology"') == 1
    assert html.count('class="subsection"') == 2
    assert '<h3 class="subsection-title">What this report can\'t see</h3>' in html
    assert "Data gaps · upgrades to queue · Methodology" in html
    # The entity used to leak into the NAV line specifically; it is still
    # correct inside the section <h2> title, so scope the assertion.
    import re as _re
    nav = _re.search(r'section-contents">([^<]*)', html)
    assert nav and "&middot;" not in nav.group(1)


def test_methodology_renders_with_only_one_chunk():
    html = render_methodology(None, _chunk("methodology_trust", "How to trust these numbers", "Prose."))
    assert html.count('class="subsection"') == 1
    assert "Methodology" in html


def test_methodology_with_neither_chunk_renders_nothing():
    assert render_methodology(None, None) == ""


def test_methodology_body_promotes_a_bold_colon_lead_to_an_h3():
    html = render_methodology(_chunk("methodology_gaps", "What this report can't see", _GAPS), None)
    assert '<h3 class="subsection-title">Two specific upgrades worth queuing</h3>' in html


def test_methodology_body_renders_upgrades_quotes_and_tables_as_notes():
    html = render_methodology(_chunk("methodology_gaps", "What this report can't see", _GAPS), None)
    assert html.count('<div class="callout note">') == 2   # the upgrade para + the blockquote
    assert "<table>" in html
    assert "<li>No cost data</li>" in html


# ─── Mode-2 Gate-STOP ──────────────────────────────────────────────────────

_GATESTOP_MD = """# Shadow Catchers — VALIDATION ARTIFACT, GATE-FAILED

> Profile state: no ratified profile.

## Bottom line

| Gate | State |
| --- | --- |
| Q-ECON-00 | FAIL |

## What the preflights returned

The economics preflight returned zero invoiced dollars.

## User-grain concentration finding

One user carries 94% of LTM capture.

## Patch-validation observations

PASS1 to PASS3 register is closed.

## Recommended next action

Wire an invoice feed, then re-run.

## Appendix

Identity and live query trace.

## Something unclassified

Catch-all body.
"""


def test_gatestop_splits_into_a_summary_block_and_a_body():
    report = parse_md(_GATESTOP_MD)
    assert report.mode == "gatestop"
    summary_html, body_html = render_gatestop(report)
    assert "Profile state" in summary_html
    assert '<h3 class="subsection-title">Bottom line</h3>' in summary_html
    assert "<table>" in summary_html


@pytest.mark.parametrize(
    "section_id",
    ["preflights", "concentration", "patchnotes", "nextaction", "appendix"],
)
def test_each_gatestop_section_becomes_its_own_collapsible(section_id):
    _, body_html = render_gatestop(parse_md(_GATESTOP_MD))
    assert f'id="{section_id}"' in body_html


def test_the_three_open_gatestop_sections():
    _, body_html = render_gatestop(parse_md(_GATESTOP_MD))
    for sid in ("preflights", "concentration", "nextaction"):
        assert f'id="{sid}" open>' in body_html
    for sid in ("patchnotes", "appendix"):
        assert f'id="{sid}" open>' not in body_html


def test_an_unclassified_gatestop_chunk_still_renders():
    _, body_html = render_gatestop(parse_md(_GATESTOP_MD))
    assert "Catch-all body." in body_html


def test_gatestop_with_no_preamble():
    report = ParsedReport(
        mode="gatestop", org_display_name="X", org_h1_full="X", org_subtitle="",
        preamble_md="", chunks=[_chunk("summary", "Bottom line", "Body.")],
    )
    summary_html, body_html = render_gatestop(report)
    assert summary_html.startswith("\n    <div class=\"subsection\"")
    assert body_html == ""
