"""Track 2.5 send-blockers: Slot C slope, identity labels, same-dealer card, floor copy."""
from __future__ import annotations

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


def test_clc_grow_row_card_is_not_a_decline_walk_without_slot_c():
    team = _render("clc", "2026-07-09").split("## The team", 1)[1].split(
        "## Full risk", 1
    )[0]
    card1 = team.split("Card 1", 1)[1].split("Card 2", 1)[0]
    assert "Lighting & Locks" in card1
    assert "Walk the top at-risk account" not in card1
    assert "decline walk" not in card1.lower() or "not a decline walk" in card1.lower()
    assert "keep-pace" in card1.lower() or "growing" in card1.lower()


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
    this_week = rendered.split("## Do this week", 1)[1].split("## Do this month", 1)[0]
    assert "Envision Lighting Sales" in card1
    assert "Lighting & Locks" in card1
    assert "growing" in card1.lower()
    assert "Walk the top at-risk account" not in card1
    assert "49%" in this_week
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
