"""P0-10 — the deterministic fallback must satisfy §Q at every confidence level.

`README.md` claims "a run still ships with `--no-narrative` / no API key / no
prose file." It did not. With no API key every prose slot is skipped, the
deterministic templates still emit Tier-A dollar claims, and at PARTIAL
confidence §Q requires each of those claims to carry a sensitivity marker
within +/-400 chars. bmc (PARTIAL) emitted three unmarked dollars and
`smoke_check` failed the run — the org could not produce a report at all.

These tests run the deterministic path for the whole pinned cohort, so the
claim is checked where it is made rather than on one org.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import assemble, config, fact_bundles, gather, preflight, signals
from pipeline.smoke_check import (
    _HEDGE_MARKERS,
    _check_sensitivity_hedge,
)

COHORT_CONF = Path(__file__).resolve().parents[1] / "tools" / "cohort.conf"


def _cohort() -> list[tuple[str, str]]:
    """The pinned org -> cache-date map. Offline; never resolves a date."""
    pairs = []
    for line in COHORT_CONF.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        org, date = line.split("\t", 1)
        pairs.append((org.strip(), date.strip()))
    return pairs


COHORT = _cohort()


def _render_deterministic(org: str, date: str) -> tuple[str, str]:
    """Assemble with every prose slot empty — the --no-narrative path."""
    posture = preflight.run(org, date, cohort_validation=True)
    bundle = gather.gather_all(org, date)
    fired = signals.detect_all(bundle, posture)
    plays = fact_bundles.build_plays_from_gather(bundle, posture, fired)
    profile_path = config.PROFILES_DIR / f"{org}.md"
    profile = profile_path.read_text(encoding="utf-8") if profile_path.exists() else ""
    md = assemble.assemble_report(
        posture=posture,
        gather=bundle,
        signals=fired,
        profile_text=profile,
        plays=plays,
    )
    return md, posture.commerce_confidence


@pytest.mark.parametrize("org,date", COHORT, ids=[o for o, _ in COHORT])
def test_deterministic_render_satisfies_sensitivity_hedge(org, date):
    if not (config.CACHE_DIR / org / date).exists():
        pytest.skip(f"no cache for {org}/{date}")
    md, confidence = _render_deterministic(org, date)
    issues: list[str] = []
    _check_sensitivity_hedge(md, issues, confidence)
    assert issues == [], f"{org} ({confidence}): " + "; ".join(issues)


def test_cohort_still_exercises_a_hedged_confidence_level():
    """Guard against the test above going vacuous.

    Every check in `_check_sensitivity_hedge` short-circuits at STRONG. If the
    cohort ever drifts to all-STRONG the parametrised test would pass while
    testing nothing, and P0-10 could silently regress.
    """
    levels = set()
    for org, date in COHORT:
        if not (config.CACHE_DIR / org / date).exists():
            continue
        posture = preflight.run(org, date, cohort_validation=True)
        levels.add(posture.commerce_confidence)
    assert levels - {"STRONG"}, f"cohort is all STRONG — §Q is never exercised ({levels})"


@pytest.mark.parametrize("confidence", ["PARTIAL", "LIMITED", "NONE"])
def test_hero_cards_carry_the_hedge_below_strong(confidence):
    """The §1 metric cards are Tier-A claims and gain the hedge below STRONG.

    NONE is included deliberately: those orgs have no invoiced dollars, so the
    cards are not rendered at all and the hedge must not appear either.
    """
    org, date = "bmc", "2026-07-09"
    if not (config.CACHE_DIR / org / date).exists():
        pytest.skip(f"no cache for {org}/{date}")
    posture = preflight.run(org, date, cohort_validation=True)
    posture.commerce_confidence = confidence
    bundle = gather.gather_all(org, date)
    fired = signals.detect_all(bundle, posture)
    plays = fact_bundles.build_plays_from_gather(bundle, posture, fired)
    md = assemble.assemble_report(
        posture=posture,
        gather=bundle,
        signals=fired,
        profile_text="",
        plays=plays,
    )
    hero = md.split("## Do this week")[0]
    if confidence == "NONE":
        assert "What would change this read" not in hero
    else:
        assert "What would change this read" in hero
        assert _HEDGE_MARKERS.search(hero)


def test_hedge_names_the_uncertainty_class_not_a_bracket():
    """§Q.4(a): the hedge must name the uncertainty, not stamp a label.

    The stale and non-stale branches say different things — a frozen feed and
    an un-cross-verified one are different reasons to distrust the size.
    """
    template = assemble.env().from_string(
        "{% from '_macros.md.j2' import sensitivity_hedge %}"
        "{{ sensitivity_hedge(posture, 'every dollar figure above', singular=true) }}"
    )

    class _Posture:
        def __init__(self, stale):
            self.is_stale = stale
            self.stale_age_phrase = "223 days (about 7 months)"

    stale = template.render(posture=_Posture(True))
    fresh = template.render(posture=_Posture(False))

    for text in (stale, fresh):
        assert text.startswith("What would change this read:")
        assert _HEDGE_MARKERS.search(text), text
        assert "pressure-test" in text

    assert "stopped updating 223 days (about 7 months) ago" in stale
    assert "cross-verified" in fresh
    assert stale != fresh
