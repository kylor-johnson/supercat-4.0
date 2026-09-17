"""Unit tests for pipeline.slot_validator — the riskiest component."""
from __future__ import annotations

import json

import pytest

from pipeline.slot_validator import (
    _bundle_values,
    _extract_numbers,
    _traces,
    align_coaching_narratives,
    check_number_parity,
    check_play_alignment,
    check_structure,
    check_voice_lint,
    reorder_play_framing,
    validate_slot,
)

# ─── Shared fixtures ────────────────────────────────────────────────────────

BUNDLE_BASIC: dict = {
    "facts": {
        "ttm_revenue": 1_553_412,
        "yoy_growth": 79.3,
        "door_count": 304,
        "avg_order": 4_820,
    },
    "derived_facts": {
        "revenue_per_door": 1.29,
        "range_low": 90_000,
        "range_high": 160_000,
        "top_customer_pct": 42.5,
    },
}


# ─── 1. Known-trace: raw dollar in facts ────────────────────────────────────

def test_raw_dollar_traces():
    output = "Total TTM revenue was $1,553,412."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert issues == [], f"expected clean trace, got: {issues}"


# ─── 2. Known-trace: rounded dollar ($1,553,412 -> $1.55M) ─────────────────

def test_rounded_dollar_traces():
    output = "Revenue reached $1.55M in the trailing twelve months."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert issues == [], f"expected $1.55M to trace, got: {issues}"


# ─── 3. Known-trace: derived_fact ratio ("$1.29") ──────────────────────────

def test_derived_ratio_traces():
    output = "Average revenue per door is $1.29."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert issues == [], f"expected $1.29 to trace via derived_facts, got: {issues}"


# ─── 4. Known-trace: derived_fact range ("$90K-$160K") ─────────────────────

def test_derived_range_traces():
    output = "The mid-tier order band runs $90K–$160K."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert issues == [], f"expected range to trace, got: {issues}"


# ─── 5. Known-no-trace: LLM-invented dollar ────────────────────────────────

def test_invented_dollar_rejects():
    output = "This segment contributes roughly $47K annually."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert any("$47K" in i for i in issues), f"expected $47K rejection, got: {issues}"


# ─── 6. Known-no-trace: LLM-computed percentage ────────────────────────────

def test_invented_percentage_rejects():
    output = "Together these two segments represent 38% of revenue."
    issues = check_number_parity(output, BUNDLE_BASIC)
    assert any("38" in i for i in issues), f"expected 38% rejection, got: {issues}"


# ─── 7. Edge: zero values, negative percentages, "n/a" strings ─────────────

def test_edge_zero_and_negative():
    bundle = {
        "facts": {"zero_metric": 0, "negative_pct": -12.5},
        "derived_facts": {},
    }
    output = "The metric is 0 accounts and declined -12.5%."
    issues = check_number_parity(output, bundle)
    assert issues == [], f"expected zero and negative to trace, got: {issues}"


def test_edge_na_string_ignored():
    """Strings like 'n/a' should not extract as numbers."""
    nums = _extract_numbers("Revenue was n/a for the period.")
    assert nums == [], f"expected no extraction from n/a, got: {nums}"


# ─── 8. Voice lint: forbidden vocab detected ───────────────────────────────

def test_voice_lint_forbidden_vocab():
    output = "The NRR for this cohort improved via the GTM playbook."
    issues = check_voice_lint(output, BUNDLE_BASIC)
    assert len(issues) > 0, "expected forbidden-vocab violations"
    matched_terms = " ".join(issues).lower()
    assert "playbook" in matched_terms or "cute label" in matched_terms


# ─── 9. Voice lint: cute labels detected ───────────────────────────────────

def test_voice_lint_cute_labels():
    output = "The company's franchise model acts as a flywheel for growth."
    issues = check_voice_lint(output, BUNDLE_BASIC)
    cute_issues = [i for i in issues if "cute label" in i]
    assert len(cute_issues) >= 2, f"expected ≥2 cute-label violations, got: {cute_issues}"


# ─── 10. Voice lint: clean output passes ───────────────────────────────────

def test_voice_lint_clean_passes():
    output = (
        "Revenue grew 79% year over year across 304 active doors, "
        "driven by order-volume gains in the Southeast territory."
    )
    bundle = {
        "facts": {"yoy_growth": 79, "door_count": 304, "territory": "Southeast"},
        "derived_facts": {},
    }
    issues = check_voice_lint(output, bundle)
    assert issues == [], f"expected clean pass, got: {issues}"


# ─── 11. Structure: valid JSON array of N strings passes ───────────────────

def test_structure_valid_array():
    arr = json.dumps(["Finding one.", "Finding two.", "Finding three."])
    issues = check_structure(arr, "B", expected_count=3)
    assert issues == [], f"expected valid structure, got: {issues}"


# ─── 12. Structure: wrong count rejects ────────────────────────────────────

def test_structure_wrong_count():
    arr = json.dumps(["Finding one.", "Finding two."])
    issues = check_structure(arr, "B", expected_count=3)
    assert any("expected exactly 3" in i for i in issues), f"expected count mismatch, got: {issues}"


# ─── Supplementary: structure checks for other slots ────────────────────────

def test_structure_slot_c_range():
    arr = json.dumps(["One.", "Two."])
    assert check_structure(arr, "C", expected_count=5) == []
    # Zero items should fail
    assert check_structure(json.dumps([]), "C", expected_count=5) != []


def test_structure_slot_e_keys():
    obj = json.dumps({"layer_1": "a", "layer_2": "b", "layer_3": "c"})
    assert check_structure(obj, "E") == []
    # Missing key
    bad = json.dumps({"layer_1": "a", "layer_2": "b"})
    issues = check_structure(bad, "E")
    assert any("layer_3" in i for i in issues)


def test_structure_slot_f_bare_string():
    assert check_structure("Just a plain string.", "F") == []
    assert check_structure(json.dumps("A quoted string."), "F") == []


def test_structure_slot_a_freeform():
    assert check_structure("# Anything goes\n\nMarkdown is fine.", "A") == []


# ─── Supplementary: helper unit tests ──────────────────────────────────────

def test_extract_numbers_basic():
    nums = _extract_numbers("Revenue hit $1.55M with +79% growth across 304 doors.")
    types = {t for _, _, t in nums}
    assert "dollar" in types
    assert "percent" in types
    assert "count" in types


def test_bundle_values_recursion():
    bundle = {
        "facts": {"a": 100, "nested": {"b": 200, "c": [300, 400]}},
        "derived_facts": {"d": "500"},
    }
    vals = _bundle_values(bundle)
    assert {100, 200, 300, 400, 500}.issubset(vals)


def test_traces_exact():
    assert _traces(100.0, {100.0})
    assert not _traces(100.0, {200.0})


def test_traces_rounding():
    allowed = {1_553_412.0}
    assert _traces(1_550_000.0, allowed)  # $1.55M
    assert _traces(1_600_000.0, allowed)  # $1.6M
    assert _traces(1_553_000.0, allowed)  # $1,553K


# ─── Supplementary: validate_slot integration ──────────────────────────────

def test_validate_slot_passes_clean():
    output = json.dumps(["Revenue reached $1.55M.", "Growth was 79%."])
    passed, violations = validate_slot("B", output, BUNDLE_BASIC, expected_count=2)
    assert passed, f"expected pass, got violations: {violations}"


def test_validate_slot_fails_on_invented():
    output = json.dumps(["Revenue reached $999M.", "Growth was 12%."])
    passed, violations = validate_slot("B", output, BUNDLE_BASIC, expected_count=2)
    assert not passed
    assert len(violations) > 0


# ─── Slot D play-title vs body alignment (ali / hfg defect) ────────────────

def test_play_alignment_pricing_body_under_cross_sell_fails():
    """ali: play 1 titled ROMA cross-sell, slot D body was $25K leak rates."""
    plays = [{"type": "cross_sell", "target_family": "ROMA", "anchor_item": "LED FMT"}]
    framing = [
        "$25K flagged across the rep base in discretionary-price dispersion — "
        "0.34% of $7.3M invoiced. Leak rates run 5.6% to 7.1%."
    ]
    issues = check_play_alignment(plays, framing)
    assert issues, "expected mismatch to fail"
    assert any("cross_sell" in i for i in issues)


def test_play_alignment_pricing_body_under_retention_fails():
    """hfg: play 2 titled second-order push, slot D body was discount leakage."""
    plays = [
        {"type": "cross_sell", "target_family": "Axis"},
        {"type": "retention", "second_year_return_rate": 0.56},
    ]
    framing = [
        "The Axis family is the cross-sell target.",
        "Discount leakage is immaterial: about $46K across the whole rep base.",
    ]
    issues = check_play_alignment(plays, framing)
    assert any("retention" in i for i in issues)


def test_play_alignment_length_mismatch_fails():
    plays = [{"type": "cross_sell", "target_family": "Jupe"}]
    framing = ["Jupe overlap list.", "Second-year return rate 46.9%."]
    issues = check_play_alignment(plays, framing)
    assert any("expected 1" in i and "got 2" in i for i in issues)


def test_play_alignment_matching_bodies_pass():
    plays = [
        {"type": "cross_sell", "target_family": "Jupe", "anchor_item": "Lilac"},
        {"type": "retention"},
        {"type": "pricing"},
    ]
    framing = [
        "The Lilac Sideboard → Jupe family cross-sell. Dealers who never bought Jupe.",
        "743 dealers placed a first order last year and 46.9% came back. Second-year return rate.",
        "About $171K sits in discount leakage. Cookie Birardi at 14.1% leak rate.",
    ]
    assert check_play_alignment(plays, framing) == []


def test_play_alignment_empty_framing_passes():
    assert check_play_alignment([{"type": "cross_sell"}], None) == []
    assert check_play_alignment([], []) == []


def test_rank_change_rekeys_complete_old_play_array_without_json_rewrite():
    plays = [
        {"type": "retention"},
        {"type": "cross_sell", "target_family": "Jupe"},
        {"type": "pricing"},
    ]
    old_order = [
        "The Jupe family is the cross-sell target.",
        "The second-year return rate needs a reorder push.",
        "Discount leakage warrants a pricing review.",
    ]
    reordered = reorder_play_framing(plays, old_order)
    assert reordered == [old_order[1], old_order[0], old_order[2]]
    assert check_play_alignment(plays, reordered) == []


class _CardRep:
    def __init__(self, name=None, number=None):
        self.rep_name_tier2 = name
        self.rep_number = number


def test_align_coaching_keeps_positional_when_lengths_match():
    cards = [_CardRep("Envision Lighting Sales", "1"), _CardRep("Philip Winston Inc", "2")]
    bodies = ["Envision keep-pace", "Philip growing"]
    assert align_coaching_narratives(cards, bodies) == bodies


def test_align_coaching_rekeys_when_house_card_removed():
    cards = [_CardRep("Envision Lighting Sales", "1"), _CardRep("Philip Winston Inc", "2")]
    bodies = [
        "HOUSE ACCOUNT walk the top at-risk account",
        "Envision Lighting Sales keep-pace on Lighting & Locks",
        "Philip Winston Inc growing",
    ]
    aligned = align_coaching_narratives(cards, bodies)
    assert aligned[0].startswith("Envision")
    assert aligned[1].startswith("Philip")
    assert "HOUSE ACCOUNT" not in "".join(aligned)


def test_align_coaching_none_when_no_cards():
    assert align_coaching_narratives([], ["body"]) is None


# ─── P0-9: Slot-D superset drift (kal could not ship at all) ───────────────
# kal_prose_2026-07-02.json authors TWO play bodies (cross-sell + pricing) but
# only the cross-sell play survives selection. That is a superset, not a
# misalignment — yet reorder_play_framing bailed on any length mismatch and
# check_play_alignment then failed the whole run with exit 1.

_XSELL_BODY = (
    "The FLINT family is your clearest cross-sell. Its anchor SKU sits on 84 "
    "dealers and 42 of those have never bought the rest of the family."
)
_PRICING_BODY = (
    "Discount dispersion across the rep base is healthy in aggregate; the "
    "spread is wide enough to be worth one discount-authority conversation."
)
_RETENTION_BODY = (
    "New dealers are not coming back — the second-year return rate is the "
    "number to move, so run a reorder push at the first-time buyers."
)
_XSELL_PLAY = {"type": "cross_sell", "target_family": "FLINT", "anchor_item": "519275WB"}
_PRICING_PLAY = {"type": "pricing"}
_RETENTION_PLAY = {"type": "retention"}


def test_reorder_play_framing_drops_orphaned_body_superset():
    """Two authored bodies, one selected play → keep the match, drop the rest."""
    out = reorder_play_framing([_XSELL_PLAY], [_XSELL_BODY, _PRICING_BODY])
    assert out == [_XSELL_BODY]
    assert check_play_alignment([_XSELL_PLAY], out) == []


def test_reorder_play_framing_superset_picks_by_type_not_position():
    """The surviving play is authored SECOND — position must not decide."""
    out = reorder_play_framing([_PRICING_PLAY], [_XSELL_BODY, _PRICING_BODY])
    assert out == [_PRICING_BODY]
    assert check_play_alignment([_PRICING_PLAY], out) == []


def test_reorder_play_framing_superset_reorders_while_dropping():
    """Three bodies, two plays, inverted order — re-key and drop the orphan."""
    plays = [_PRICING_PLAY, _XSELL_PLAY]
    out = reorder_play_framing(plays, [_XSELL_BODY, _RETENTION_BODY, _PRICING_BODY])
    assert out == [_PRICING_BODY, _XSELL_BODY]
    assert check_play_alignment(plays, out) == []


def test_reorder_play_framing_subset_returns_original():
    """Fewer bodies than plays cannot be covered — leave it to the gate."""
    plays = [_XSELL_PLAY, _PRICING_PLAY]
    assert reorder_play_framing(plays, [_XSELL_BODY]) == [_XSELL_BODY]


def test_reorder_play_framing_ambiguous_returns_original():
    """Two bodies matching one play is unresolvable — the gate must still fire."""
    plays = [_XSELL_PLAY]
    framing = [_XSELL_BODY, _XSELL_BODY]
    assert reorder_play_framing(plays, framing) == framing
    assert check_play_alignment(plays, framing) != []
