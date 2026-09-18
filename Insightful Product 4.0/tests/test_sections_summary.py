"""Characterization — §1 assembly in `report_render/sections.py` (W2 / Phase 3).

P0-4 lived in `render_summary`'s hero-sub-paragraph branch: the block after the
hero was assumed to be narrative, so when the sanitizer collapsed the hero and
its numbered list into one block the STRUCTURAL lead-in
(`**Priority actions, by cadence:**`) was glued into the hero as prose while the
bullets below still emitted the real sub-label — 8 of 11 orgs shipped the
heading twice.

T1-3 (Phase 4) replaces the English-string hero-card trigger with structured
data, so every branch below is about to move. This file is the net under it.

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every behavior below is the one we want.
"""
from __future__ import annotations

import re

import pytest

from report_render.md_parse import Chunk
from report_render.sections import (
    _attach_hero_sub,
    _build_ceo_callouts,
    _build_hero,
    _build_metric_cards_from_table,
    _build_priorities,
    _callout_jump,
    _classify_delta,
    _delta_note_class,
    _extract_callout_num,
    _is_bullet_list,
    _is_numbered_list,
    _is_priorities_lead,
    _is_three_things_lead,
    _looks_like_ceo_callouts,
    _looks_like_metric_table,
    _looks_like_priorities,
    _pick_callout_tone,
    _shorten_callout_title,
    _split_priority_text,
    render_summary,
)

PERIOD = "LTM invoiced &middot; through Jun 29, 2026"


def _chunk(body: str, heading: str = "The 60-second read") -> Chunk:
    return Chunk(section_id="summary", heading=heading, body_md=body)


# ─── _build_hero ───────────────────────────────────────────────────────────

def test_hero_splits_the_lead_bold_into_number_delta_and_sub():
    html = _build_hero("**$15.64M invoiced, +5.95% YoY.** Same dealers, more spend.", PERIOD)
    assert f'<div class="hero-eyebrow">{PERIOD}</div>' in html
    assert '<div class="hero-num">$15.64M</div>' in html
    assert '<div class="hero-delta ok">+5.95% YoY</div>' in html
    assert '<div class="hero-sub">Same dealers, more spend.</div>' in html


def test_a_negative_delta_is_tinted_bad():
    html = _build_hero("**$9.9M invoiced, -12.4% YoY.** Contracting.", PERIOD)
    assert '<div class="hero-delta bad">-12.4% YoY</div>' in html


def test_a_hero_without_a_delta_omits_the_delta_div():
    html = _build_hero("**$9.9M invoiced.** Flat.", PERIOD)
    assert "hero-delta" not in html
    assert '<div class="hero-num">$9.9M</div>' in html


def test_a_hero_without_a_dollar_falls_back_to_the_prose_only_variant():
    """The behavior-only (COMMERCE_CONFIDENCE = NONE) shape."""
    html = _build_hero("There is no invoiced total in this window.", "")
    assert "hero-num" not in html
    assert '<div class="hero-eyebrow">LTM invoiced</div>' in html
    assert "There is no invoiced total in this window." in html


def test_an_empty_period_line_falls_back_to_the_default_eyebrow():
    assert '<div class="hero-eyebrow">LTM invoiced</div>' in _build_hero("**$1M.** x", "")


def test_the_period_line_is_treated_as_html_safe():
    html = _build_hero("**$1M.** x", "LTM invoiced &middot; through Jun 29")
    assert "&amp;middot;" not in html


def test_the_headline_dollar_is_escaped():
    html = _build_hero("**$1M <b>bold</b>.** x", PERIOD)
    assert "<b>bold</b>" not in html.split('hero-sub')[0]


def test_without_a_bold_lead_the_headline_is_split_on_the_first_period():
    """`first_para.split(".")[0]` cuts inside `$9.9M`, so the hero number
    renders as `$9`. Pinned, not endorsed (W2 finding F-4)."""
    html = _build_hero("$9.9M invoiced this year. And more prose.", PERIOD)
    assert '<div class="hero-num">$9</div>' in html
    assert "$9.9M invoiced this year. And more prose." in html


@pytest.mark.xfail(
    reason="W2 finding F-4: a hero paragraph with no bold lead splits the headline "
           "on the first `.`, truncating `$9.9M` to `$9` (Phase 4, T1-3)",
    strict=True,
)
def test_an_unbolded_hero_should_keep_the_whole_dollar_figure():
    assert '<div class="hero-num">$9.9M</div>' in _build_hero(
        "$9.9M invoiced this year. And more prose.", PERIOD
    )


@pytest.mark.parametrize(
    "delta,expected",
    [("+5.95%", "ok"), ("-12%", "bad"), ("−12%", "bad"), ("–12%", "bad"), ("", "flat"), ("5%", "flat")],
)
def test_classify_delta(delta, expected):
    assert _classify_delta(delta) == expected


def test_attach_hero_sub_appends_a_second_sub_div():
    hero = _build_hero("**$15.64M invoiced, +5.95% YoY.** Same dealers.", PERIOD)
    out = _attach_hero_sub(hero, "The substance lives here.")
    assert out.count('class="hero-sub"') == 2
    assert 'style="margin-top: 10px;">The substance lives here.</div>' in out


# ─── render_summary — block walking ────────────────────────────────────────

_HERO = "**$15.64M invoiced, +5.95% YoY.** Same dealers, more spend."
_METRICS = (
    "| | |\n| --- | --- |\n"
    "| Same dealers, more spend | **+29%** · 655 dealers |\n"
    "| $ at risk | **$2.18M** · 12 accounts fading |"
)
_THREE_LEAD = "**Three things you wouldn't have known without this report:**"
_CALLOUTS = (
    "1. **France and Sons is down 57% in six months.** The slope is unambiguous.\n"
    "2. **New dealers aren't coming back.** The second order never lands.\n"
    "3. **Your top account is 18% of LTM.** That is concentration, not scale."
)
_PRIORITIES_LEAD = "**Priority actions, by cadence:**"
_BULLETS = (
    "- **This week:** 7 named calls on $1.45M+ in play — France and Sons, OP Jenkins and five more. **$1.45M**\n"
    "- **This month:** Build the second-order push for the 212 first-time dealers who never returned.\n"
    "- **This quarter:** Run a territory review with the three reps carrying declining books."
)


def _summary(*blocks: str) -> str:
    return render_summary(_chunk("\n\n".join(blocks)), PERIOD)


def test_the_full_sarreid_shape_renders_every_band():
    html = _summary(_HERO, _METRICS, _THREE_LEAD, _CALLOUTS, _PRIORITIES_LEAD, _BULLETS)
    assert '<section class="section" id="summary">' in html
    assert '<h2 class="section-title">The 60-second read</h2>' in html
    assert 'class="hero-summary"' in html
    assert html.count('class="metric"') == 2
    assert html.count('<div class="ceo-num">') == 3
    assert html.count('class="priority"') == 3
    assert "Three things you wouldn&rsquo;t have known without this report" in html
    assert "Priority actions, by cadence" in html


def test_the_section_title_is_always_the_canonical_string():
    """The H2 in the MD varies across the cohort; the rendered title does not."""
    html = render_summary(_chunk(_HERO, heading="What's driving the +5.95%"), PERIOD)
    assert '<h2 class="section-title">The 60-second read</h2>' in html


def test_an_empty_chunk_renders_an_empty_section():
    html = render_summary(_chunk(""), PERIOD)
    assert 'id="summary"' in html
    assert "hero-summary" not in html


# ─── P0-4 — the structural lead-in must not be eaten as the hero sub ───────

def test_a_priorities_lead_after_the_hero_is_not_glued_into_the_hero():
    html = _summary(_HERO, _PRIORITIES_LEAD, _BULLETS)
    assert html.count('class="hero-sub"') == 1
    assert html.count("Priority actions, by cadence") == 1
    assert 'class="priority"' in html


def test_a_three_things_lead_after_the_hero_is_not_glued_into_the_hero():
    html = _summary(_HERO, _THREE_LEAD, _CALLOUTS)
    assert html.count('class="hero-sub"') == 1
    assert html.count("have known without this report") == 1
    assert html.count('<div class="ceo-num">') == 3


def test_a_genuine_narrative_block_after_the_hero_still_attaches():
    html = _summary(_HERO, "Same dealers spent more, and the top of the book held.")
    assert html.count('class="hero-sub"') == 2
    assert "the top of the book held" in html


def test_a_long_block_after_the_hero_stays_below_the_metrics_as_prose():
    long_para = "Same dealers spent more. " * 30  # > 600 chars
    html = _summary(_HERO, long_para)
    assert html.count('class="hero-sub"') == 1
    assert 'class="prose"' in html


def test_a_table_directly_after_the_hero_is_not_the_hero_sub():
    html = _summary(_HERO, _METRICS)
    assert html.count('class="hero-sub"') == 1
    assert html.count('class="metric"') == 2


def test_a_dangling_three_things_lead_with_no_list_renders_as_prose():
    """bri carried this shape — the lead survived with nothing under it."""
    html = _summary(_HERO, _THREE_LEAD)
    assert 'class="ceo-callout' not in html
    assert "sub-label" not in html
    assert "have known" in html


def test_a_dangling_priorities_lead_with_no_bullets_renders_as_prose():
    html = _summary(_HERO, _PRIORITIES_LEAD)
    assert 'class="priority"' not in html
    assert "Priority actions" in html


# ─── Lead-in / list detectors ──────────────────────────────────────────────

@pytest.mark.parametrize(
    "block,expected",
    [
        ("**Three things you wouldn't have known without this report:**", True),
        ("Three things you wouldn’t have known", True),   # curly apostrophe
        ("**What stands out:**", False),                   # the sanitizer's rewrite
        ("Three things to do", False),
    ],
)
def test_is_three_things_lead(block, expected):
    assert _is_three_things_lead(block) is expected


@pytest.mark.parametrize(
    "block,expected",
    [
        ("**Priority actions, by cadence:**", True),
        ("Priority actions by cadence", True),
        ("**Priority actions:**", False),   # needs both tokens
        ("Actions, by cadence", False),
    ],
)
def test_is_priorities_lead(block, expected):
    assert _is_priorities_lead(block) is expected


@pytest.mark.parametrize("block,expected", [("1. a", True), (" 2. b", True), ("- a", False), ("a", False)])
def test_is_numbered_list(block, expected):
    assert _is_numbered_list(block) is expected


@pytest.mark.parametrize("block,expected", [("- a", True), ("* a", True), ("1. a", False), ("a", False)])
def test_is_bullet_list(block, expected):
    assert _is_bullet_list(block) is expected


def test_looks_like_ceo_callouts_needs_exactly_three_bolded_items():
    assert _looks_like_ceo_callouts(_CALLOUTS) is True
    two = "\n".join(_CALLOUTS.splitlines()[:2])
    assert _looks_like_ceo_callouts(two) is False
    unbolded = _CALLOUTS.replace("**", "")
    assert _looks_like_ceo_callouts(unbolded) is False


def test_looks_like_priorities_needs_every_item_to_carry_a_cadence():
    assert _looks_like_priorities(_BULLETS) is True
    mixed = _BULLETS + "\n- A bullet with no cadence."
    assert _looks_like_priorities(mixed) is False
    single = "- **This week:** one item only"
    assert _looks_like_priorities(single) is False


def test_a_standalone_callout_list_with_no_lead_in_is_still_detected():
    html = _summary(_HERO, _METRICS, _CALLOUTS)
    assert html.count('<div class="ceo-num">') == 3


def test_a_standalone_priorities_list_with_no_lead_in_is_still_detected():
    html = _summary(_HERO, _METRICS, _BULLETS)
    assert html.count('class="priority"') == 3


def test_a_short_list_directly_after_the_hero_is_swallowed_as_the_hero_sub():
    """The hero-sub branch tests only for a table and the two lead-ins, so a
    list under 600 chars sitting directly after the hero never reaches the
    callout/priority detectors. Pinned, not endorsed (W2 finding F-5)."""
    html = _summary(_HERO, _CALLOUTS)
    assert html.count('<div class="ceo-num">') == 0
    assert html.count('class="hero-sub"') == 2
    assert _summary(_HERO, _BULLETS).count('class="priority"') == 0


@pytest.mark.xfail(
    reason="W2 finding F-5: a callout or priority list sitting directly after the "
           "hero is absorbed into the hero sub and never reaches its detector, so "
           "the cards silently vanish (Phase 4, T1-3)",
    strict=True,
)
def test_a_list_directly_after_the_hero_should_still_reach_its_detector():
    assert _summary(_HERO, _CALLOUTS).count('<div class="ceo-num">') == 3


def test_the_alternate_shape_where_the_lead_and_list_share_a_block():
    shared = "1. **Three things you wouldn't have known.** Body one.\n2. **B.** Body two.\n3. **C.** Body three."
    html = _summary(_HERO, _METRICS, shared)
    assert html.count('<div class="ceo-num">') == 3


# ─── Metric cards ──────────────────────────────────────────────────────────

def test_metric_table_detection_keys_on_a_blank_two_column_header():
    assert _looks_like_metric_table([["", ""], ["a", "b"]]) is True
    assert _looks_like_metric_table([["Label", "Value"], ["a", "b"]]) is False
    assert _looks_like_metric_table([["", "", ""], ["a", "b", "c"]]) is False
    assert _looks_like_metric_table([["", ""]]) is False


def test_metric_cards_split_the_bold_value_from_its_note():
    html = _build_metric_cards_from_table(
        [["", ""], ["Same dealers, more spend", "**+29%** · 655 dealers · $9.72M → $12.55M"]]
    )
    assert '<div class="metric-label">Same dealers, more spend</div>' in html
    assert '<div class="metric-value">+29%</div>' in html
    assert "655 dealers" in html


def test_a_metric_value_with_no_bold_carries_no_note():
    html = _build_metric_cards_from_table([["", ""], ["Reps", "25"]])
    assert '<div class="metric-value">25</div>' in html
    assert "metric-note" not in html


def test_short_metric_rows_are_skipped():
    html = _build_metric_cards_from_table([["", ""], ["orphan"]])
    assert "metric-label" not in html


def test_a_labelled_header_row_is_kept_as_a_card():
    """`_build_metric_cards_from_table` only drops the header when it is blank."""
    html = _build_metric_cards_from_table([["Label", "Value"], ["a", "b"]])
    assert html.count('class="metric"') == 2


@pytest.mark.parametrize(
    "value,note,expected",
    [
        ("+29%", "655 dealers", "ok"),
        ("-12%", "", "danger"),
        ("$2.18M", "12 accounts fading", "warn"),
        ("$2.18M", "at risk", "warn"),
        ("25", "reps", ""),
        ("29%", "more spend", "ok"),
    ],
)
def test_delta_note_class(value, note, expected):
    assert _delta_note_class(value, note) == expected


# ─── CEO callouts ──────────────────────────────────────────────────────────

def test_callouts_split_the_bold_headline_from_the_body():
    html = _build_ceo_callouts(_CALLOUTS)
    assert html.count('<div class="ceo-num">') == 3
    assert '<div class="ceo-num">57%</div>' in html
    assert "The slope is unambiguous." in html


def test_a_callout_without_a_bold_lead_falls_back_to_the_first_sentence():
    html = _build_ceo_callouts("1. France and Sons is down 57%. The rest is body.")
    assert '<div class="ceo-title">France and Sons is down 57%</div>' in html


def test_an_empty_list_block_renders_nothing():
    assert _build_ceo_callouts("") == ""
    assert _build_priorities("") == ""


@pytest.mark.parametrize(
    "text,expected",
    [
        ("down -57% in six months", "-57%"),
        ("$2.18M at risk", "$2.18M"),
        ("7 of 12 accounts", "7 of 12"),
        ("18% of LTM", "18%"),
        ("no numbers at all", "·"),
    ],
)
def test_extract_callout_num(text, expected):
    assert _extract_callout_num(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("down 57% in six months", "danger"),
        ("-12% and fading", "danger"),
        ("the account went dark", "danger"),
        ("new dealers aren't coming back", "warn"),
        ("the second order never lands, a reorder leak", "warn"),
        ("your top account is concentrated", "warn"),
        ("the book is growing", "info"),
        ("nothing tonal here", "info"),
    ],
)
def test_pick_callout_tone(text, expected):
    assert _pick_callout_tone(text) == expected


def test_a_decline_beats_a_warn_word():
    assert _pick_callout_tone("reorder rate is down 40%") == "danger"


@pytest.mark.parametrize(
    "text,tone,expected",
    [
        ("a territory pattern across three reps", "danger", ("team", "See the pattern")),
        ("new dealers aren't coming back", "warn", ("thismonth", "Build the push")),
        ("your top account is 18% of LTM", "info", ("risk", "See the exposure")),
        ("down 57% in six months", "danger", ("thisweek", "Call this week")),
        ("a structural leak", "warn", ("thismonth", "Work the play")),
        ("nothing to route", "info", ("", "")),
    ],
)
def test_callout_jump_routing(text, tone, expected):
    assert _callout_jump(text, tone) == expected


def test_a_routed_callout_emits_a_jump_link():
    html = _build_ceo_callouts("1. **France and Sons is down 57%.** Call them.")
    assert '<a class="ceo-jump" href="#thisweek">Call this week &rarr;</a>' in html


def test_an_unrouted_callout_emits_no_jump_link():
    html = _build_ceo_callouts("1. **Nothing to route here.** Plain body.")
    assert "ceo-jump" not in html


@pytest.mark.parametrize(
    "headline,expected",
    [
        ("Short and punchy", "Short and punchy"),
        ("Trailing period is dropped.", "Trailing period is dropped"),
        (
            "France and Sons — a $402K account — is down 56% in six months and placed an order today",
            "France and Sons",
        ),
    ],
)
def test_shorten_callout_title(headline, expected):
    assert _shorten_callout_title(headline) == expected


def test_a_long_headline_with_no_separator_is_word_trimmed():
    long = "A very long headline with no separator anywhere in it at all which keeps going onward"
    out = _shorten_callout_title(long)
    assert out.endswith("…")
    assert len(out) <= 59
    assert not out[:-1].endswith(" ")


# ─── Priorities ────────────────────────────────────────────────────────────

def test_priority_rows_carry_a_cadence_badge_and_impact():
    html = _build_priorities(_BULLETS)
    assert html.count('class="priority"') == 3
    assert '<span class="priority-badge high">This Week</span>' in html
    assert '<span class="priority-badge medium">This Month</span>' in html
    assert '<span class="priority-badge low">This Quarter</span>' in html
    assert '<div class="priority-impact">$1.45M</div>' in html


def test_a_bullet_without_a_cadence_gets_the_generic_action_badge():
    html = _build_priorities("- Call the top five accounts this afternoon and log the outcome.")
    assert '<span class="priority-badge low">Action</span>' in html


@pytest.mark.parametrize(
    "text,expected",
    [
        # 1. trailing bold dollar becomes the impact
        (
            "7 named calls on $1.45M+ in play — France and Sons and five more. **$1.45M**",
            ("7 named calls on $1.45M+ in play", "France and Sons and five more", "$1.45M"),
        ),
        # 2. em-dash split, both halves substantial
        (
            "Build the second-order push — 212 first-time dealers never returned",
            ("Build the second-order push", "212 first-time dealers never returned", ""),
        ),
        # 3. first-sentence split when the dash halves are too short
        (
            "Run a territory review. Three reps carry declining books.",
            ("Run a territory review.", "Three reps carry declining books.", ""),
        ),
        # 4. short em-dash halves still split when nothing else matches
        ("3 plays — go", ("3 plays", "go", "")),
        # 5. nothing to split
        ("Just one clause", ("Just one clause", "", "")),
    ],
)
def test_split_priority_text(text, expected):
    assert _split_priority_text(text) == expected


def test_a_decimal_dollar_does_not_trigger_the_sentence_split():
    title, desc, _ = _split_priority_text("Chase the $1.45M gap across the book right now")
    assert desc == ""
    assert "$1.45M" in title


def test_a_trailing_bold_without_a_number_is_not_an_impact():
    _, _, impact = _split_priority_text("Do the thing **carefully**")
    assert impact == ""


def test_priority_desc_is_omitted_when_empty():
    html = _build_priorities("- **This week:** Call five accounts")
    assert "priority-desc" not in html


# ─── Remainder blocks ──────────────────────────────────────────────────────

def test_unrecognised_blocks_fall_through_to_prose():
    html = _summary(_HERO, _METRICS, "A trailing note the heuristics do not claim.")
    assert '<p class="prose">A trailing note the heuristics do not claim.</p>' in html


def test_only_the_first_metric_table_becomes_cards():
    """A second metric table falls through to prose. Prose has to sit between
    them: `_split_paragraphs` re-joins two abutting pipe blocks into one."""
    second = _METRICS.replace("Same dealers, more spend", "Second table row")
    html = _summary(_HERO, _METRICS, "Prose between the tables.", second)
    assert html.count('class="metrics"') == 1
    assert "<table>" in html


def test_a_non_metric_table_after_the_hero_stays_a_table():
    labelled = "| Account | Value |\n| --- | --- |\n| France and Sons | $402K |"
    html = _summary(_HERO, labelled)
    assert "metric-label" not in html
    assert "<table>" in html
