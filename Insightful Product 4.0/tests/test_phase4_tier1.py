"""Phase 4 Tier-1 fixes: T1-2, T1-4, T1-5.

T1-1 (narrative arc) and T1-3 (structural card marker) are exercised through the
cohort and the golden set; these are the unit-level pins.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pytest

from pipeline.gather import account_needs_a_call
from pipeline.slot_validator import align_talking_points
from pipeline.smoke_check import _check_named_quantity_consistency


@dataclass
class _Acct:
    bill_to_name: str = ""
    bill_to_number: str = ""
    recent_vs_prior_pct: Optional[float] = None
    is_real_decline: bool = False
    is_cadence_cliff: bool = False


# ─── T1-2 ──────────────────────────────────────────────────────────────────
_FRANCE = _Acct("France and Sons", "29925")
_SWAN = _Acct("The Swan's Nest Inc", "31060")
_JENKINS = _Acct("OP JENKINS FURNITURE & DESIGN", "40001")

_B_FRANCE = "France and Sons — a $402K account — is down 56% in six months."
_B_SWAN = "The Swan's Nest is down 90% on a $66K book and dark for 111 days."
_B_JENKINS = "OP Jenkins is down 59% in six months but ordered days ago."


def test_reordering_no_longer_discards_the_whole_array():
    """The Sarreid regression: one row moving nulled all seven bodies."""
    out = align_talking_points([_SWAN, _FRANCE], [_B_FRANCE, _B_SWAN])
    assert out == [_B_SWAN, _B_FRANCE]


def test_corporate_suffixes_do_not_block_the_match():
    """The ERP says "The Swan's Nest Inc"; the author wrote "The Swan's Nest"."""
    assert align_talking_points([_SWAN], [_B_SWAN]) == [_B_SWAN]


def test_all_caps_source_name_matches_a_prose_short_form():
    assert align_talking_points([_JENKINS], [_B_JENKINS]) == [_B_JENKINS]


def test_a_screened_out_row_leaves_the_others_intact():
    """A dropped row must not shift the remaining bodies onto wrong accounts."""
    out = align_talking_points([_FRANCE], [_B_FRANCE, _B_SWAN])
    assert out == [_B_FRANCE]


def test_an_unmatched_row_gets_an_empty_body_not_a_wrong_one():
    out = align_talking_points([_FRANCE, _Acct("Brand New Co", "99")], [_B_FRANCE])
    assert out == [_B_FRANCE, ""]


def test_no_matches_returns_none_so_the_template_fills_every_row():
    assert align_talking_points([_Acct("Nobody", "1")], [_B_FRANCE]) is None


# ─── T1-4 ──────────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    "acct,expected",
    [
        (_Acct(recent_vs_prior_pct=6.7), False),      # hfg row 1
        (_Acct(recent_vs_prior_pct=20.0), False),     # kal row 1
        (_Acct(recent_vs_prior_pct=49.4), False),     # clc Lighting & Locks
        (_Acct(recent_vs_prior_pct=-2.6), False),     # flat
        (_Acct(recent_vs_prior_pct=-10.0), True),     # at the floor
        (_Acct(recent_vs_prior_pct=-56.0), True),
        (_Acct(recent_vs_prior_pct=5.0, is_real_decline=True), True),
        (_Acct(recent_vs_prior_pct=5.0, is_cadence_cliff=True), True),
        (_Acct(recent_vs_prior_pct=None), False),
    ],
)
def test_only_slipping_accounts_belong_on_a_call_list(acct, expected):
    assert account_needs_a_call(acct) is expected


# ─── T1-5 ──────────────────────────────────────────────────────────────────
_P01 = (
    "## The 60-second read\n"
    "**1,075** prior-year accounts went dark, and 998 new dealers refilled it.\n"
    "## The dealer base\n"
    "- **1,080 dealers** who bought last year ordered nothing this year\n"
)


def test_one_claim_with_two_values_is_a_ship_blocker():
    issues: list[str] = []
    _check_named_quantity_consistency(_P01, issues)
    assert len(issues) == 1
    assert "accounts that went dark" in issues[0]
    assert "1075" in issues[0] and "1080" in issues[0]


def test_the_same_claim_agreeing_everywhere_is_clean():
    issues: list[str] = []
    _check_named_quantity_consistency(_P01.replace("1,075", "1,080"), issues)
    assert issues == []


def test_a_report_that_states_the_claim_once_is_clean():
    issues: list[str] = []
    _check_named_quantity_consistency(
        "**1,080** prior-year accounts went dark.", issues
    )
    assert issues == []
