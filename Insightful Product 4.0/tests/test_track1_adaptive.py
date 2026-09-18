"""Track 1 adaptive-menu and rendered-claim regressions."""
from __future__ import annotations

import json

from pipeline import assemble, config, fact_bundles, gather, preflight, signals
from pipeline.availability import build_availability, outreach_mix
from pipeline.hero_sanitizer import sanitize_hero_framing


def _run_state(org: str, date: str):
    posture = preflight.run(org, date, cohort_validation=True)
    bundle = gather.gather_all(org, date)
    fired = signals.detect_all(bundle, posture)
    plays = fact_bundles.build_plays_from_gather(
        bundle, posture, fired
    )
    profile = (config.PROFILES_DIR / f"{org}.md").read_text(
        encoding="utf-8"
    )
    return posture, bundle, fired, plays, profile


def _hero(org: str, date: str) -> str:
    path = config.OUTPUTS_DIR / f"{org}_prose_{date}.json"
    return json.loads(path.read_text(encoding="utf-8"))["hero_framing"]


def _render(org: str, date: str, *, hero: str | None = None) -> str:
    posture, bundle, fired, plays, profile = _run_state(org, date)
    return assemble.assemble_report(
        posture=posture,
        gather=bundle,
        signals=fired,
        profile_text=profile,
        hero_framing=hero,
        plays=plays,
    )


def test_hfg_hero_cannot_leak_pre_screen_accounts_or_old_play_count():
    dirty = (
        "Handmade In Vermont.com leads the call list. "
        "Shop Hubbardton Forge is next. "
        "This month: 3 plays. Four unrelated calls.\n"
    )
    rendered = _render("hfg", "2026-07-02", hero=dirty)
    hero = rendered.split("## Do this week", 1)[0]
    assert "Handmade In Vermont.com" not in hero
    assert "Shop Hubbardton Forge" not in hero
    assert "3 plays" not in hero
    assert "four unrelated calls" not in hero
    assert "**This month:** 1 play — Axis cross-sell." in hero

    live = _render(
        "hfg", "2026-07-02", hero=_hero("hfg", "2026-07-02")
    ).split("## Do this week", 1)[0]
    assert "Handmade In Vermont.com" not in live
    assert "Shop Hubbardton Forge" not in live
    assert "3 plays" not in live


def test_cci_and_sca_stale_derived_hero_claims_are_removed():
    cci = _render(
        "cci", "2026-07-02", hero=_hero("cci", "2026-07-02")
    ).split("## Do this week", 1)[0]
    assert "Only Goodform" not in cci
    assert "Lamps.com" in cci  # P0-5: names are no longer shouted
    assert "11.4% of invoiced" not in cci

    ali = _render(
        "ali", "2026-06-30", hero=_hero("ali", "2026-06-30")
    ).split("## Do this week", 1)[0]
    assert "eCat is capturing $410 of $7.3M" not in ali
    assert "#1 at-risk account" not in ali
    assert "$1.16M across 10 accounts pulling back" not in ali

    sca = _render(
        "sca", "2026-07-02", hero=_hero("sca", "2026-07-02")
    ).split("## The team", 1)[0]
    assert "30 reps are enrolled" not in sca
    assert "30 enrolled reps" not in sca


def test_all_decline_call_list_dispatches_the_investigative_footer():
    """Phase 4: the footer must describe the list that actually rendered.

    T1-4 removed non-slipping accounts from the call list, so clc's three
    remaining rows are all declines. The footer used to say "the grow/flat rows
    need reinforcement" about rows that no longer existed — and hfg showed it
    with six rows all down 31-82%, because `outreach_mix` classified on
    `is_real_decline` (recent < 60% of prior) while MEMBERSHIP uses
    `account_needs_a_call` (<= -10%). Two rules for one concept.
    """
    assert outreach_mix(_run_state("clc", "2026-07-09")[1]) == "all_decline"
    rendered = _render("clc", "2026-07-09")
    this_week = rendered.split("## Do this week", 1)[1].split(
        "## Do this month", 1
    )[0]
    assert "Investigative call this week — walk the candidate explanations" in this_week
    assert "Two different conversations live in this list" not in this_week
    assert "grow/flat rows need reinforcement" not in this_week


def test_missing_cross_sell_gap_does_not_claim_buyer_profile_in_products():
    rendered = _render("ali", "2026-06-30")
    products = rendered.split("## What's selling", 1)[1].split(
        "## The dealer base", 1
    )[0]
    assert "share a buyer profile" not in products
    assert "cleanest, most specific play" not in products
    assert "already buys from the ROMA family" in products
    assert "not computed for this org" not in products


def test_code_like_hfg_anchor_uses_family_only_play_title():
    _, _, _, plays, _ = _run_state("hfg", "2026-07-02")
    assert [play["title"] for play in plays] == ["Axis cross-sell"]


def test_availability_hides_ali_prior_year_and_keeps_sca_floor():
    ali_posture, ali_bundle, _, ali_plays, _ = _run_state(
        "ali", "2026-06-30"
    )
    ali = build_availability(ali_bundle, ali_posture, ali_plays)
    assert not ali.layer_1
    assert all(play["type"] != "retention" for play in ali_plays)

    sca_posture, sca_bundle, _, sca_plays, _ = _run_state(
        "sca", "2026-07-02"
    )
    sca = build_availability(sca_bundle, sca_posture, sca_plays)
    assert sca.activity_floor
    assert not sca.this_week
    rendered = _render("sca", "2026-07-02", hero=_hero("sca", "2026-07-02"))
    assert "## Do this week" not in rendered
    assert "### Rep activity floor" in rendered
