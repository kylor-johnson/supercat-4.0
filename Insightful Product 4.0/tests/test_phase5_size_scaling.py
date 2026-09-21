"""Phase 5 / W3 — size-relative signal thresholds.

The overfit these pin down: `DECLINE_MIN_LTM_DOLLARS = 50_000` was tuned on
Sarreid ($15.8M) and means 0.07% of the year on cci ($70.0M) and 0.72% on bmc
($6.9M) — a 10x spread in what counts as "material". The mechanism replaces the
bare constant with `max(absolute_floor, pct x the org's own size)`.

The SHIPPED profile is BASELINE, which is 4.0 byte-for-byte (every pct is 0.0);
the cohort and golden set prove that. These tests exercise the mechanism itself,
so they set their own profiles rather than relying on whichever one is active.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

import pytest

from pipeline import fact_bundles as fb
from pipeline.signals import (
    ACTIVE_PROFILE,
    BASELINE_PROFILE,
    DEFAULT_THRESHOLDS,
    RECOMMENDED_PROFILE,
    SizeScaledFloor,
    coaching_card_reps,
    detect_real_decline,
    detect_rep_atrisk_book,
    org_size_base,
    resolve_thresholds,
)


# ─── Test doubles ──────────────────────────────────────────────────────────
@dataclass
class _Acct:
    bill_to_number: str = "1"
    bill_to_name: str = "An Account"
    rep_number: Optional[str] = "R1"
    rep_label: Optional[str] = None
    ltm_rev: float = 0.0
    recent_6mo: float = 0.0
    prior_6mo: float = 0.0
    recent_vs_prior_pct: Optional[float] = None
    days_silent: int = 0
    mean_order_gap_days: float = 0.0

    @property
    def is_real_decline(self) -> bool:
        if self.prior_6mo <= 0:
            return False
        return (self.recent_6mo / self.prior_6mo) < 0.6 and self.ltm_rev > 20_000

    @property
    def is_cadence_cliff(self) -> bool:
        if self.mean_order_gap_days <= 0 or self.recent_vs_prior_pct is None:
            return False
        return self.days_silent > 2 * self.mean_order_gap_days and self.recent_vs_prior_pct >= 0


@dataclass
class _Risk:
    rep_number: str = "R1"
    rep_name_tier2: Optional[str] = None
    dollars_at_risk: float = 0.0
    accounts_at_risk: int = 1
    leak_dollars: Optional[float] = None
    leak_pct: Optional[float] = None
    display_label: Optional[str] = None


@dataclass
class _Posture:
    inv_ltm_net: float = 0.0
    commerce_confidence: str = "STRONG"


@dataclass
class _Dealers:
    active_ltm: int = 0


@dataclass
class _Gather:
    dealers: Optional[_Dealers] = None
    rep_risks: list = None
    decay: list = None
    products: list = None
    families: list = None
    cross_sell_gap: object = None


def _decline(ltm: float) -> _Acct:
    """An unambiguous 80% half-over-half collapse at the given LTM."""
    return _Acct(ltm_rev=ltm, recent_6mo=ltm * 0.1, prior_6mo=ltm * 0.5,
                 recent_vs_prior_pct=-80.0)


# ─── The mechanism ─────────────────────────────────────────────────────────
def test_the_shipped_profile_is_the_recommended_one():
    """W3 proposed; the owner decided. Flipped 2026-09-18 as its own stamped act,
    after the card-ranking fix — flipping first would have blanked §6 on three
    orgs (cci 3->0, clc 5->0, hfg 5->0) because the floor was judged against a
    discount-leak proxy rather than the at-risk book."""
    # Flipped 2026-09-18 after the card-ranking fix. The guard stays: the
    # shipped profile must be one of the two named profiles, never an
    # ad-hoc literal, so a reader can see which numbers are live.
    assert ACTIVE_PROFILE is RECOMMENDED_PROFILE
    assert ACTIVE_PROFILE.name == "recommended"


def test_baseline_reproduces_the_pre_w3_absolute_constants():
    t = BASELINE_PROFILE.resolve(70_016_164, 7_570)
    assert t.decline_min_ltm == 50_000
    assert t.rep_atrisk_min == 20_000
    assert t.new_line_min_revenue == 100_000
    assert t.growth_pocket_min_dealers == 10
    assert t.new_line_min_dealers == 5
    assert t.coaching_card_min_dollars == 0
    assert t.play_min_upside == 0


def test_a_small_org_and_a_large_org_reach_the_same_RELATIVE_threshold():
    """The whole point: 0.10% of the year means the same thing at every size."""
    gate = SizeScaledFloor(floor=0.0, pct=0.0010)
    small = gate.resolve(6_944_922)    # bmc
    large = gate.resolve(70_016_164)   # cci
    assert small == pytest.approx(6_944.922)
    assert large == pytest.approx(70_016.164)
    # Same share of each org's own year, a 10x spread in absolute dollars.
    assert small / 6_944_922 == pytest.approx(large / 70_016_164)
    assert large / small == pytest.approx(70_016_164 / 6_944_922)


def test_the_absolute_floor_still_binds_on_a_tiny_org():
    """A $2M client must not fire on $2,000 of "risk"."""
    gate = SizeScaledFloor(floor=25_000, pct=0.0010)
    assert gate.resolve(2_000_000) == 25_000       # 0.10% = $2K → floor wins
    assert gate.resolve(41_170_115) == pytest.approx(41_170.115)  # hfg → pct wins


@pytest.mark.parametrize("base", [0, 0.0, None, -1.0, float("nan"), float("inf")])
def test_a_missing_or_absent_size_base_degrades_to_the_floor(base):
    """`commerce_confidence = NONE` orgs (da, sca, bsc) carry inv_ltm_net == 0."""
    assert SizeScaledFloor(floor=25_000, pct=0.50).resolve(base) == 25_000


def test_a_NONE_confidence_org_resolves_without_dividing_by_zero():
    posture = _Posture(inv_ltm_net=0.0, commerce_confidence="NONE")
    gather = _Gather(dealers=None, rep_risks=[], decay=[])
    assert org_size_base(posture, gather) == (0.0, 0)
    t = resolve_thresholds(posture, gather, RECOMMENDED_PROFILE)
    assert t.decline_min_ltm == 25_000        # the floor, not 0 and not a crash
    assert t.growth_pocket_min_dealers == 5
    assert t.play_min_upside == 10_000


def test_detectors_called_without_thresholds_keep_the_old_absolute_gates():
    assert detect_real_decline(_decline(49_999)) is None
    assert detect_real_decline(_decline(50_001)) is not None
    assert DEFAULT_THRESHOLDS.decline_min_ltm == 50_000


def test_the_same_account_fires_or_not_depending_on_the_ORGS_size():
    """$60K is material to a $7M client and noise to a $70M one."""
    account = _decline(60_000)
    prof = replace(BASELINE_PROFILE, decline_min_ltm=SizeScaledFloor(25_000, 0.0010))
    small = prof.resolve(6_944_922, 879)     # floor $25K
    large = prof.resolve(70_016_164, 7_570)  # 0.10% = $70K
    assert detect_real_decline(account, small) is not None
    assert detect_real_decline(account, large) is None


def test_rep_atrisk_signal_reads_the_resolved_floor():
    risk = _Risk(dollars_at_risk=22_038)      # hfg CANOREP
    prof = replace(BASELINE_PROFILE, rep_atrisk_min=SizeScaledFloor(10_000, 0.0010))
    assert detect_rep_atrisk_book(risk, prof.resolve(8_761_029, 572)) is not None
    assert detect_rep_atrisk_book(risk, prof.resolve(41_170_115, 2_422)) is None


# ─── S1 — "Do this month" materiality ──────────────────────────────────────
_HFG_PLAY = {
    "type": "cross_sell", "title": "Axis cross-sell", "gap_available": True,
    "gap_count": 1, "target_ltm": 597_183.0, "target_dealers": 24,
}


def test_the_hfg_one_door_play_is_worth_a_fraction_of_a_percent_of_the_year():
    ceiling = fb.play_upside_ceiling(_HFG_PLAY, _Gather())
    assert ceiling == pytest.approx(12_441.3, abs=1.0)     # the "$7K-$12K" play
    assert ceiling / 41_170_115 < 0.0005                   # 0.03% of the year


def test_a_play_below_the_orgs_floor_is_dropped_not_padded():
    t = RECOMMENDED_PROFILE.resolve(41_170_115, 2_422)
    assert fb.play_upside_ceiling(_HFG_PLAY, _Gather()) < t.play_min_upside


def test_the_baseline_floor_of_zero_keeps_every_play():
    t = BASELINE_PROFILE.resolve(41_170_115, 2_422)
    assert t.play_min_upside == 0
    assert fb.play_upside_ceiling(_HFG_PLAY, _Gather()) >= t.play_min_upside


def test_an_unquantifiable_play_scores_zero_rather_than_raising():
    assert fb.play_upside_ceiling({"type": "cross_sell", "gap_available": False}, _Gather()) == 0.0
    assert fb.play_upside_ceiling({"type": "retention"}, _Gather()) == 0.0
    assert fb.play_upside_ceiling({"type": "who knows"}, _Gather()) == 0.0


# ─── S2 — one definition of "this account has slipped", five surfaces ───────
# hfg's real rows: CANOREP carries $22K "at risk" and the only account on that
# book is 1489, +6.7% and ordered two days ago.
_CANOREP = _Risk(rep_number="CANOREP", dollars_at_risk=22_038, accounts_at_risk=1)
_ACCT_1489 = _Acct(bill_to_number="1489", rep_number="CANOREP", ltm_rev=602_445,
                   recent_6mo=311_000, prior_6mo=291_500, recent_vs_prior_pct=6.7,
                   days_silent=2)
_REP_12328 = _Risk(rep_number="12328", dollars_at_risk=804, accounts_at_risk=3)
_ACCT_11936 = _Acct(bill_to_number="11936", rep_number="12328", ltm_rev=179_763,
                    recent_6mo=67_000, prior_6mo=107_200, recent_vs_prior_pct=-37.5,
                    days_silent=13)


def test_cards_are_built_from_the_at_risk_book_not_the_leak_proxy():
    """Phase-5 follow-up: the card set is derived from the DECAY side.

    It used to be bounded by the leak query and ranked on `dollars_at_risk`, so
    hfg led with rep CANOREP ($22K of leak) on a +6.7% account while rep 12328
    ($446K across three real declines) never appeared. CANOREP carries no
    slipped account, so it is not a coaching card at any threshold.
    """
    cards = coaching_card_reps([_CANOREP, _REP_12328], [_ACCT_1489, _ACCT_11936],
                               BASELINE_PROFILE.resolve(41_170_115, 2_422))
    assert [c.risk.rep_number for c in cards] == ["12328"]
    assert cards[0].account is _ACCT_11936
    assert cards[0].at_risk_ltm == _ACCT_11936.ltm_rev


def test_a_rep_whose_flagged_accounts_are_all_growing_gets_no_risk_card():
    """The S2 defect: a RISK card about an account that is pacing UP.

    Isolated from the dollar floor — this pins the CONSISTENCY half, which the
    brief says must land even if the materiality numbers need the owner.
    """
    consistency_only = replace(
        BASELINE_PROFILE, coaching_cards_require_needs_a_call=True
    ).resolve(41_170_115, 2_422)
    cards = coaching_card_reps([_CANOREP, _REP_12328], [_ACCT_1489, _ACCT_11936],
                               consistency_only)
    assert [c.risk.rep_number for c in cards] == ["12328"]
    assert cards[0].account is _ACCT_11936


def test_a_leak_only_rep_is_dropped_and_the_real_one_survives_the_floor():
    """Raising the floor against the leak proxy removed the RIGHT cards too.

    Under the old shape both of these dropped at RECOMMENDED — CANOREP on
    consistency, 12328 because its leak figure is $804 on a $41.2M book. Judged
    on the at-risk BOOK instead, 12328's $180K clears the floor comfortably and
    CANOREP is gone for the only reason that matters: nothing on its book
    slipped.
    """
    t = RECOMMENDED_PROFILE.resolve(41_170_115, 2_422)
    assert _REP_12328.dollars_at_risk < t.coaching_card_min_dollars   # the proxy fails
    cards = coaching_card_reps([_CANOREP, _REP_12328], [_ACCT_1489, _ACCT_11936], t)
    assert [c.risk.rep_number for c in cards] == ["12328"]
    assert cards[0].at_risk_ltm > t.coaching_card_min_dollars          # the book clears


def test_the_card_names_an_account_that_actually_slipped_not_the_biggest_one():
    """sarreid rep 099: two accounts, the larger one is only -6.2%."""
    big_but_fine = _Acct(bill_to_number="31060", rep_number="099", ltm_rev=198_992,
                         recent_6mo=93_000, prior_6mo=99_100, recent_vs_prior_pct=-6.2)
    small_and_slipping = _Acct(bill_to_number="32530", rep_number="099", ltm_rev=66_172,
                               recent_6mo=3_000, prior_6mo=30_300,
                               recent_vs_prior_pct=-90.1, days_silent=111)
    risk = _Risk(rep_number="099", dollars_at_risk=36_424, accounts_at_risk=2)
    rows = [big_but_fine, small_and_slipping]
    # The card names the account that SLIPPED under either profile now — the
    # -6.2% account is not at risk, so it is not what the card is about.
    for profile in (BASELINE_PROFILE, RECOMMENDED_PROFILE):
        cards = coaching_card_reps([risk], rows, profile.resolve(15_767_336, 1_399))
        assert cards[0].account is small_and_slipping
        assert cards[0].at_risk_ltm == small_and_slipping.ltm_rev
        assert big_but_fine not in cards[0].flagged


def test_a_pure_discount_leak_rep_never_becomes_a_card():
    leak_only = _Risk(rep_number="016", dollars_at_risk=13_752, accounts_at_risk=0)
    for profile in (BASELINE_PROFILE, RECOMMENDED_PROFILE):
        assert coaching_card_reps([leak_only], [], profile.resolve(15_767_336, 1_399)) == []


def test_the_card_floor_scales_with_the_org():
    """$1K is a card on 4.0. It is 0.002% of hfg's year."""
    tiny = _Risk(rep_number="41168", dollars_at_risk=1_414, accounts_at_risk=1)
    row = _Acct(bill_to_number="1531", rep_number="41168", ltm_rev=181_351,
                recent_6mo=97_000, prior_6mo=83_900, recent_vs_prior_pct=15.6)
    # The account is +15.6% — growing — so it is not a card under EITHER
    # profile now. The floor still scales; it is just no longer what decides
    # this case.
    assert coaching_card_reps([tiny], [row], BASELINE_PROFILE.resolve(41_170_115, 2_422)) == []
    t = RECOMMENDED_PROFILE.resolve(41_170_115, 2_422)
    assert t.coaching_card_min_dollars == pytest.approx(8_234.023)
    assert coaching_card_reps([tiny], [row], t) == []


# ─── S3 — which same-dealer measure the hero leads with ────────────────────
@pytest.mark.parametrize(
    "org,lift,nrr,lift_says,nrr_says",
    [
        ("sarreid", 29.1, 106.4, "up", "up"),
        ("cci", 3.8, 88.5, "flat", "less"),
        ("clc", 71.9, 173.2, "up", "up"),
        ("hfg", -1.8, 83.7, "flat", "less"),
        ("kal", -4.0, 91.8, "flat", "less"),
        ("bmc", -62.1, 76.0, "less", "less"),
        ("bri", -5.9, 92.1, "less", "less"),
    ],
)
def test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one(
    org, lift, nrr, lift_says, nrr_says
):
    t = BASELINE_PROFILE.resolve(1.0, 1)

    def verdict(value, up_at, down_at):
        return "up" if value > up_at else ("less" if value < down_at else "flat")

    assert verdict(lift, 5.0, t.hero_lift_spending_less_pct) == lift_says
    assert verdict(nrr, 105.0, t.hero_nrr_spending_less_pct) == nrr_says
    # Where they disagree, `lift` never reports the harsher verdict.
    order = {"less": 0, "flat": 1, "up": 2}
    assert order[lift_says] >= order[nrr_says]


def test_the_hero_measure_is_a_profile_choice_not_a_hardcoded_one():
    assert BASELINE_PROFILE.resolve(1.0, 1).hero_same_base_measure == "lift"
    assert RECOMMENDED_PROFILE.resolve(1.0, 1).hero_same_base_measure == "nrr"


# ─── S1 — "no play qualified this month" must be a REACHABLE state ─────────
_CALLOUT_MD = (
    "**$41.17M invoiced (LTM).** Your existing accounts are spending less.\n"
    "\n"
    "**Three things you wouldn't have known without this report:**\n"
    "\n"
    "1. **998 dealers placed a first-ever order last year.** A 56% second-year "
    "return rate means you are winning accounts at the front door and losing "
    "them at the back.\n"
)


def _summary_chunk():
    from report_render.md_parse import Chunk

    return Chunk(section_id="summary", heading="The 60-second read", body_md=_CALLOUT_MD)


def test_a_callout_jump_never_points_at_a_section_that_did_not_render():
    """W3 found this by making "Do this month" legitimately empty on hfg: the
    hero still shipped `href="#thismonth"` and step10 check [12] failed."""
    from report_render.sections import render_summary

    with_month = render_summary(_summary_chunk(), "", {"summary", "thismonth", "thisweek"})
    assert 'href="#thismonth"' in with_month

    without_month = render_summary(_summary_chunk(), "", {"summary", "thisweek"})
    assert 'href="#thismonth"' not in without_month


def test_omitting_available_ids_keeps_the_pre_w3_rendering():
    """Every existing caller and all 11 golden orgs go through this path."""
    from report_render.sections import render_summary

    assert render_summary(_summary_chunk(), "") == render_summary(
        _summary_chunk(), "", {"summary", "thismonth", "thisweek", "team", "risk"}
    )


def test_an_empty_play_list_turns_the_whole_section_off():
    """`_base.md.j2` gates §3 on `availability.this_month`, and "Do this month"
    is NOT a smoke_check-required heading — so zero plays is a clean omission,
    not a "0 plays" stub."""
    from pipeline.smoke_check import _STANDARD_REQUIRED_SECTIONS

    assert "## Do this month" not in _STANDARD_REQUIRED_SECTIONS


# ─── Identity and the house desk ───────────────────────────────────────────
# Three rules that only became reachable once S1 was pulled with the R11/§7.1
# name bridge. Before that, S1 carried no bill_to_name and no rep_name for 8
# of 11 orgs, so none of this could fire — and none of it was tested.
def test_an_unidentified_row_is_not_a_call_and_not_a_card():
    """S1 groups by bill-to, so every blank bill-to collapses into ONE row.

    On ali that bucket was $614K of unattributed invoices and it LED the call
    list as "(unnamed) - rep 75 - 81 days silent": the top instruction of the
    week was to phone nobody. It is not one account, so its slope is not one
    account's slope either.
    """
    from pipeline.gather import account_is_callable, account_is_identified

    nameless = _Acct(bill_to_number="", bill_to_name="", rep_number="75",
                     ltm_rev=614_299.0, recent_6mo=274_746.0, prior_6mo=339_553.0,
                     recent_vs_prior_pct=-19.1, days_silent=81)
    assert not account_is_identified(nameless)
    assert not account_is_callable(nameless)
    assert coaching_card_reps([], [nameless], BASELINE_PROFILE.resolve(7_341_307, 1_004)) == []

    # A row with only a number is still dialable — the rep can look it up.
    numbered = _Acct(bill_to_number="11359", bill_to_name="", rep_number="21",
                     ltm_rev=29_998.0, recent_6mo=9_268.0, prior_6mo=20_730.0,
                     recent_vs_prior_pct=-55.3, days_silent=103)
    assert account_is_identified(numbered)
    assert account_is_callable(numbered)


def test_the_house_desk_gets_no_card_but_its_dealers_stay_callable():
    """cci shipped "Card 3 - House Account" the moment rep labels arrived.

    You do not coach the inside desk. Haverty's is still a real account that
    is really slipping, so it stays on the call list.
    """
    from pipeline.gather import account_is_callable

    havertys = _Acct(bill_to_number="383325", bill_to_name="Haverty's Furniture Companies",
                     rep_number="99", rep_label="House Account", ltm_rev=174_000.0,
                     recent_6mo=70_000.0, prior_6mo=86_700.0,
                     recent_vs_prior_pct=-19.3, days_silent=4)
    assert account_is_callable(havertys)
    assert coaching_card_reps([], [havertys], BASELINE_PROFILE.resolve(41_170_115, 2_422)) == []


def test_a_rep_label_the_profile_excludes_gets_no_card():
    """clc names its own inside desk "Capital Lighting Fixture" (profile §4).

    That desk carries a $390K account down 68% — the account is the point, the
    card is not.
    """
    belami = _Acct(bill_to_number="9001", bill_to_name="1Stoplighting.com dba Belami Inc",
                   rep_number="900", rep_label="Capital Lighting Fixture",
                   ltm_rev=390_000.0, recent_6mo=95_000.0, prior_6mo=297_000.0,
                   recent_vs_prior_pct=-68.0, days_silent=3)
    t = BASELINE_PROFILE.resolve(26_000_000, 1_187)
    assert [c.risk.rep_number for c in coaching_card_reps([], [belami], t)] == ["900"]
    assert coaching_card_reps([], [belami], t, frozenset({"capital lighting fixture"})) == []


def test_cadence_decay_needs_a_rhythm_to_be_off():
    """Q-ORG-DECAY rows without a mean gap carry no cadence signal.

    This is the same hole that makes AccountDecay.is_cadence_cliff dead across
    the cohort: S1 never selects mean_order_gap_days, so all 88 decay rows
    carry 0.0 and the cliff branch can never fire. Q-ORG-DECAY supplies the
    gap from the platform-order side, and a row missing it is dropped rather
    than treated as "0 days between orders".
    """
    from pipeline.gather import load_cadence_decay

    rows = [
        {"customer_num": "2465", "customer_name": "The Parker Company LLC", "state": "FL",
         "ltm_orders": "25", "ltm_gmv": "3353051.28", "days_since_last": "97",
         "avg_days_between": "18.2", "decay_ratio": "5.3"},
        {"customer_num": "9", "customer_name": "No Rhythm Co", "state": "TX",
         "ltm_orders": "5", "ltm_gmv": "50000", "days_since_last": "40",
         "avg_days_between": "0", "decay_ratio": ""},
        {"customer_num": "", "customer_name": "", "state": "", "ltm_orders": "6",
         "ltm_gmv": "99999", "days_since_last": "80", "avg_days_between": "10",
         "decay_ratio": "8.0"},
    ]
    out = load_cadence_decay(rows)
    assert [c.customer_num for c in out] == ["2465"]
    assert out[0].cadence_phrase == "every 18 days"
    assert out[0].decay_ratio == 5.3


def test_is_cadence_cliff_is_unreachable_on_the_current_s1_columns():
    """Pins the defect so the fix is visible when S1 starts supplying the gap.

    account_needs_a_call() reads as `is_real_decline OR is_cadence_cliff OR
    pct <= -10`, but the middle term has never been able to fire.
    """
    a = _Acct(ltm_rev=100_000.0, recent_6mo=60_000.0, prior_6mo=50_000.0,
              recent_vs_prior_pct=20.0, days_silent=90, mean_order_gap_days=0.0)
    assert not a.is_cadence_cliff          # no gap -> no rhythm -> no cliff
    a_with_gap = _Acct(ltm_rev=100_000.0, recent_6mo=60_000.0, prior_6mo=50_000.0,
                       recent_vs_prior_pct=20.0, days_silent=90, mean_order_gap_days=10.0)
    assert a_with_gap.is_cadence_cliff     # supply the gap and it fires
