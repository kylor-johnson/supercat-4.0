"""P0-7 — a $2.6M custom project was 6.4% of HFG's year and nothing named it.

HFG's top-12 is 25% one-off custom SKUs, one dealer each. They crowded the real
catalog story out of §8, and the more interesting fact — one project, one door,
6.4% of a $41.2M year — was never stated.

The rule has two gates and BOTH are relative (AUDIT_FINDINGS §2.1 — absolute
dollar constants are the Sarreid overfit this programme exists to undo):

  1. cluster share of invoiced LTM      >= PROJECT_MIN_SHARE_OF_LTM
  2. cluster $/unit vs catalog median   >= PROJECT_MIN_UNIT_PRICE_RATIO

Gate 2 carries the weight. ali's `SB-23*` pair is also >2% of LTM through a
single door, but it moves 2,750 units at $69 — a channel, not a project.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import config, gather, preflight
from pipeline.gather import ProductRow
from pipeline.signals import (
    PROJECT_MIN_SHARE_OF_LTM,
    PROJECT_MIN_UNIT_PRICE_RATIO,
    detect_single_door_project,
)

COHORT_CONF = Path(__file__).resolve().parents[1] / "tools" / "cohort.conf"


def _cohort() -> list[tuple[str, str]]:
    pairs = []
    for line in COHORT_CONF.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        org, date = line.split("\t", 1)
        pairs.append((org.strip(), date.strip()))
    return pairs


COHORT = _cohort()

# Every org in the pinned cohort whose catalog must stay silent. hfg is the one
# true positive; the rest are the false-positive surface.
EXPECTED_FIRES = {"hfg"}


def _catalog(org: str, date: str):
    if not (config.CACHE_DIR / org / date).exists():
        return None, 0.0
    bundle = gather.gather_all(org, date)
    posture = preflight.run(org, date, cohort_validation=True)
    return bundle.products, posture.inv_ltm_net


@pytest.mark.parametrize("org,date", COHORT, ids=[o for o, _ in COHORT])
def test_fires_on_hfg_and_nowhere_else(org, date):
    products, ltm = _catalog(org, date)
    if products is None:
        pytest.skip(f"no cache for {org}/{date}")
    sig = detect_single_door_project(products, ltm)
    if org in EXPECTED_FIRES:
        assert sig is not None, f"{org} should fire the project signal"
    else:
        assert sig is None, f"false positive on {org}: {sig.headline}"


def test_hfg_names_the_project():
    products, ltm = _catalog("hfg", "2026-07-02")
    if products is None:
        pytest.skip("no hfg cache")
    sig = detect_single_door_project(products, ltm)
    ctx = sig.context
    assert ctx["prefix"].startswith("9N00145405")
    assert ctx["sku_count"] == 4
    assert 2_600_000 < ctx["dollars"] < 2_700_000
    assert 6.0 < ctx["share_pct"] < 7.0
    assert ctx["unit_price_ratio"] > PROJECT_MIN_UNIT_PRICE_RATIO


def _rows(spec):
    return [
        ProductRow(item_number=i, description=i, ltm_revenue=r, units=u, dealers=d)
        for i, r, u, d in spec
    ]


# A catalog of ordinary items so the median unit price is well defined.
_BASELINE = [(f"ORD-{n:03d}", 50_000.0, 50, 25) for n in range(10)]  # $1,000/unit


def test_unit_price_gate_rejects_a_single_door_channel():
    """ali's shape: one door, over the share gate, but high-volume/low-price."""
    products = _rows(_BASELINE + [
        ("SB-23941-MBL", 95_000.0, 1_800, 1),
        ("SB-23768-MBL", 94_000.0, 950, 1),
    ])
    assert detect_single_door_project(products, 5_000_000.0) is None


def test_share_gate_rejects_an_immaterial_one_off():
    """kal's shape: a genuine custom SKU at 26x unit price, but 0.6% of LTM."""
    products = _rows(_BASELINE + [("MODD-3TIER-QUADRO", 52_000.0, 3, 1)])
    assert detect_single_door_project(products, 8_800_000.0) is None


def test_multi_door_items_never_cluster():
    products = _rows(_BASELINE + [
        ("PROJ-A-01", 900_000.0, 10, 2),
        ("PROJ-A-02", 800_000.0, 10, 3),
    ])
    assert detect_single_door_project(products, 5_000_000.0) is None


def test_thresholds_are_size_relative_not_absolute():
    """The same catalog shape must get the same verdict at any org size.

    This is the P0-7 acceptance test for AUDIT_FINDINGS §2.1: scale every
    dollar by 20x and the answer may not change.
    """
    shape = _BASELINE + [("PROJ-A-01", 600_000.0, 10, 1), ("PROJ-A-02", 400_000.0, 8, 1)]
    small = detect_single_door_project(_rows(shape), 5_000_000.0)
    big = detect_single_door_project(
        _rows([(i, r * 20, u, d) for i, r, u, d in shape]), 100_000_000.0
    )
    assert small is not None and big is not None
    assert small.context["share_pct"] == pytest.approx(big.context["share_pct"])
    assert small.context["unit_price_ratio"] == pytest.approx(big.context["unit_price_ratio"])


def test_share_gate_is_a_real_boundary():
    """Just under the share floor is silence; just over it fires."""
    base_ltm = 10_000_000.0
    just_under = base_ltm * PROJECT_MIN_SHARE_OF_LTM * 0.9
    just_over = base_ltm * PROJECT_MIN_SHARE_OF_LTM * 1.1
    for dollars, expect_fire in ((just_under, False), (just_over, True)):
        products = _rows(_BASELINE + [
            ("PROJ-A-01", dollars / 2, 2, 1),
            ("PROJ-A-02", dollars / 2, 2, 1),
        ])
        sig = detect_single_door_project(products, base_ltm)
        assert (sig is not None) is expect_fire, f"${dollars:,.0f} → {sig}"


def test_no_products_or_no_revenue_is_silent():
    assert detect_single_door_project([], 5_000_000.0) is None
    assert detect_single_door_project(_rows(_BASELINE), 0.0) is None
