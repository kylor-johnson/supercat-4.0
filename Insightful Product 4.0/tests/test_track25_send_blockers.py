"""Track 2.5 send-blockers: Slot C slope, identity labels, same-dealer card, floor copy."""
from __future__ import annotations

import re

import json

from pipeline import assemble, config, fact_bundles, gather, preflight, signals
from pipeline.gather import display_rep_label


def _run_state(org: str, date: str):
    posture = preflight.run(org, date, cohort_validation=True)
    bundle = gather.gather_all(org, date)
    fired = signals.detect_all(bundle, posture)
    plays = fact_bundles.build_plays_from_gather(bundle, posture, fired)
    profile = (config.PROFILES_DIR / f"{org}.md").read_text(encoding="utf-8")
    return posture, bundle, fired, plays, profile


def _prose(org: str, date: str) -> dict:
    path = config.OUTPUTS_DIR / f"{org}_prose_{date}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _render(org: str, date: str, **slot_kwargs) -> str:
    posture, bundle, fired, plays, profile = _run_state(org, date)
    return assemble.assemble_report(
        posture=posture,
        gather=bundle,
        signals=fired,
        profile_text=profile,
        plays=plays,
        **slot_kwargs,
    )


def test_display_rep_label_prefers_agency_name_over_positional_index():
    assert (
        display_rep_label(
            rep_name_tier2="BrandJump, LLC",
            rep_number="",
            rep_label="BrandJump, LLC",
        )
        == "BrandJump, LLC"
    )
    assert (
        display_rep_label(
            rep_name_tier2=None,
            rep_number="12328",
            rep_label=None,
        )
        == "rep 12328"
    )
    assert (
        display_rep_label(
            rep_name_tier2="rep NENOREP",
            rep_number="NENOREP",
            rep_label="rep NENOREP",
        )
        == "rep NENOREP"
    )
    assert (
        display_rep_label(rep_name_tier2=None, rep_number="", rep_label="")
        is None
    )


def test_clc_cards_name_the_reps_carrying_the_at_risk_book():
    """Phase-5 follow-up: there is no grow-row card to soften any more.

    Track 2.5 fixed the COPY on a card about a growing account. The card should
    never have existed: clc's five cards came from the leak query and not one
    named a rep carrying a slipped account — reps 51, 74 and 1402 do, and none
    of them were in `rep_risks` at all, so no threshold could surface them.
    Cards are now built from the decay side, so clc leads with the real book.
    """
    team = _render("clc", "2026-07-09").split("## The team", 1)[1].split(
        "## Full risk", 1
    )[0]
    card1 = team.split("Card 1", 1)[1].split("Card 2", 1)[0]
    assert "of book at risk across" in card1
    assert "Lighting & Locks" not in card1      # the +49.4% grow row is gone
    assert "Walk the top at-risk account" not in card1


def test_clc_slot_c_keeps_envision_keep_pace_when_loaded():
    prose = _prose("clc", "2026-07-09")
    rendered = _render(
        "clc",
        "2026-07-09",
        coaching_narratives=prose["coaching_narratives"],
        talking_points=prose["talking_points"],
    )
    team = rendered.split("## The team", 1)[1].split("## Full risk", 1)[0]
    card1 = team.split("Card 1", 1)[1].split("Card 2", 1)[0]
    # Bound on the NEXT heading, not on "## Do this month" — under the shipped
    # profile an org whose only play is immaterial has no month section at all,
    # and splitting on a missing heading swallowed the rest of the document
    # (including the coaching cards) into `this_week`.
    _tail = rendered.split("## Do this week", 1)[1]
    this_week = re.split(r"\n## ", _tail, maxsplit=1)[0]
    assert "Envision Lighting Sales" in card1
    assert "Lighting & Locks" in card1
    assert "growing" in card1.lower()
    assert "Walk the top at-risk account" not in card1
    # T1-4 (Phase 4): "Lighting & Locks.com - BLS" is +49.4% — GROWING. It used
    # to lead clc's "Do this week" because the call list ranked on
    # actionability x dollars with a 0.3 floor for healthy accounts. A call list
    # is a list of accounts where something is wrong, so a growing account is no
    # longer on it. The Slot-C assertions above are the real subject of this
    # test and still hold: a grow-row rep card must read keep-pace, not
    # decline-walk.
    assert "49%" not in this_week
    assert "Lighting & Locks.com - BLS" not in this_week
    assert "keep-pace" in this_week.lower()


def test_hfg_l3_and_leaderboard_use_rs01_agency_names():
    rendered = _render("hfg", "2026-07-02")
    layer3 = rendered.split("### Layer 3", 1)[1].split("## The team", 1)[0]
    assert "BrandJump" in layer3
    assert "| rep  |" not in layer3
    leaderboard = rendered.split("### Top 10 reps", 1)[1].split(
        "### Top-", 1
    )[0]
    assert "BrandJump" in leaderboard
    assert "Martha Graham" in leaderboard
    assert "Glassman Brands" in leaderboard
    assert "rep (1)" not in leaderboard
    assert "| rep  |" not in leaderboard


def test_hfg_hero_card_is_labeled_spend_change_not_nrr():
    rendered = _render(
        "hfg", "2026-07-02", hero_framing=_prose("hfg", "2026-07-02")["hero_framing"]
    )
    hero = rendered.split("## Do this week", 1)[0]
    assert "Same-dealer spend change" in hero
    assert "Same-dealer base — contracting" not in hero
    assert "spent -2% more" not in rendered
    assert "same-dealer spend change" in rendered.split("## The dealer base", 1)[1].lower()


def test_sca_and_da_floor_copy_matches_quiet_plus_dark():
    sca = _render("sca", "2026-07-02")
    da = _render("da", "2026-07-09")
    sca_floor = sca.split("### Rep activity floor", 1)[1].split("##", 1)[0]
    da_floor = da.split("### Rep activity floor", 1)[1].split("##", 1)[0]
    assert "19 of 34 seats are quiet or dark" in sca_floor
    assert "19 of 34 seats have gone 90+" not in sca_floor
    assert "15 of 41 seats are quiet or dark" in da_floor
    assert "15 of 41 seats have gone 90+" not in da_floor
    assert "14 — re-activation needed" in da_floor


# ─── Hero "at-risk dollars" must agree with the coaching cards ──────────────
# The hero once summed RepRisk.dollars_at_risk (the discount-leak proxy) while
# section 6 rendered the at-risk BOOK. The two numbers were sourced from
# different queries, so the hero understated the cards by 6-40x across the
# cohort — hfg led with "~$0.04M to act on" above three cards totalling $841K.
# Both surfaces now read availability.coaching_cards; this is the guard.
_HERO_AT_RISK = re.compile(r"~\$([\d,]+\.\d\d)M of at-risk dollars")
_CARD_BOOK = re.compile(r"\$([\d,]+)K of book at risk")


def _hero_and_cards(org: str, date: str) -> tuple[float | None, list[float]]:
    md = _render(org, date)
    hero = _HERO_AT_RISK.search(md)
    hero_dollars = float(hero.group(1).replace(",", "")) * 1_000_000 if hero else None
    cards = [float(m.replace(",", "")) * 1_000 for m in _CARD_BOOK.findall(md)]
    return hero_dollars, cards


def test_hero_at_risk_figure_equals_the_rendered_coaching_cards():
    for org, date in (("sarreid", "2026-07-02"), ("hfg", "2026-07-02"), ("clc", "2026-07-09")):
        hero, cards = _hero_and_cards(org, date)
        assert cards, f"{org}: expected coaching cards to render"
        assert hero is not None, f"{org}: expected a hero at-risk figure"
        # The hero prints 2dp in millions; compare at that resolution.
        expected = round(sum(cards[:5]) / 1_000_000, 2)
        assert round(hero / 1_000_000, 2) == expected, (
            f"{org}: hero says ${hero/1_000_000:,.2f}M but its cards total ${expected:,.2f}M"
        )


def test_hero_at_risk_figure_is_absent_when_no_coaching_cards_render():
    # The line is gated on availability.coaching_cards, not on rep_risks, so an
    # org with leak rows but no slipped account must not advertise a figure.
    hero, cards = _hero_and_cards("sca", "2026-07-02")
    if not cards:
        assert hero is None, "hero advertised at-risk dollars with no cards to walk"
