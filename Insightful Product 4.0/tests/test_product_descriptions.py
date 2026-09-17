"""P0-8 — SKU descriptions reached the client as raw ERP spec strings.

HFG's §8 shipped this verbatim:

    9N00145405-3-14-DL105 | TYPE DL-105 | 34.5" H x 64.5" D x 92.5" L |
    OPEN CENTER, ACRYLIC BOTTOM AND TOP DIFFUSERS

The rule keeps the identifying head, drops the dimensional tail, never invents
a name, and never collapses two SKUs onto one label. The cohort sweep at the
bottom of this file is the DoD: it runs against every catalog that exists, not
just HFG.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import pytest

from pipeline import config
from pipeline.gather import normalize_product_description as norm

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


# ─── the defect itself ──────────────────────────────────────────────────────

def test_hfg_spec_string_keeps_the_head_and_drops_the_dimensions():
    raw = (
        '9N00145405-3-14-DL105 | TYPE DL-105 | 34.5" H x 64.5" D x 92.5" L | '
        "OPEN CENTER, ACRYLIC BOTTOM AND TOP DIFFUSERS"
    )
    assert norm(raw, "9N00145405-3-14-DL105") == (
        "Type DL-105 — Open Center, Acrylic Bottom and Top Diffusers"
    )


@pytest.mark.parametrize(
    "raw,item,expected",
    [
        ('9N00145405-2-14-DL104 | TYPE DL-104 | 24.5" H x 64.5" x 64.5"',
         "9N00145405-2-14-DL104", "Type DL-104"),
        ('9N00145405-4-14-DL107 | TYPE DL-107 | 16.3" H x 96" OD',
         "9N00145405-4-14-DL107", "Type DL-107"),
    ],
)
def test_dimension_only_tail_is_dropped(raw, item, expected):
    assert norm(raw, item) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        # bmc: purchase-order references leading a real product name
        ("po-78500 Brookings Floor Mirror", "Brookings Floor Mirror"),
        ("PO-Y2723 Newport Rect Cocktail", "Newport Rect Cocktail"),
        ("PO644283 Eltham Wall Mirror", "Eltham Wall Mirror"),
        ("PO Y0964 Hudson Server", "Hudson Server"),
        ("PO11124 Beaded Floor Mirror", "Beaded Floor Mirror"),
        ("040003492 Round Coffee Table", "Round Coffee Table"),
        # sarreid: ERP double spaces
        ("Lilac Sideboard  Blue Finish", "Lilac Sideboard Blue Finish"),
        # cci: shouted names
        ("MALVASIA BRASS WALL SCONCE", "Malvasia Brass Wall Sconce"),
        ("BRIALLEN WHITE DEMI-LUNE CABIN", "Briallen White Demi-Lune Cabin"),
        # kal: a name with a size/light code riding along
        ("FLINT 5 LT MULTI DROP", "Flint 5 LT Multi Drop"),
        ("VERDE 6LT CHANDELIER", "Verde 6LT Chandelier"),
        ("ESTRELLA 48IN PENDANT", "Estrella 48IN Pendant"),
    ],
)
def test_structural_and_case_normalisation(raw, expected):
    assert norm(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        # ali: electrical spec strings. "FLMNT RND" must not become "Flmnt Rnd",
        # and "PEN"/"VAN"/"MIR" are abbreviations, not words.
        "FLMNT RND 9\" BATT BU 100-277V",
        "LED FMT 35 WATT 1500LMN 120V 90CRI JA8",
        "PEN LED 30W 2400LM 3000K 90CRI",
        "VAN LED 20W 3CCT 1300LM 90CRI",
        "MIR LED 54X42 40W 4800LM 90CRI 120V",
        "ODR WALL 9W",
        "[K] PEN LED 7W 600LM 2700K 90CRI",
        # bri: part codes, no natural-language name at all
        "LED14DISC/7/5CCT/927-950/J/WHRD/D",
        "NOS40-1890-4PK",
        # bmc: a three-letter code with no vowel is not a word
        "GFR",
        # clc / sarreid: already mixed case, nothing to do
        "4 Light Pendant",
        "20 Light Chandelier",
        "Beacon Hill Display Case",
        "*the Harley Chair",
        "Pendant: Volterra, Linear",
        "Outdr: Axis, Med, LED",
    ],
)
def test_left_exactly_as_the_erp_stores_it(raw):
    assert norm(raw) == raw


def test_never_returns_empty():
    assert norm("", "ITEM-1") == "ITEM-1"
    assert norm('24.5" H x 38.5" D', "ITEM-1") == '24.5" H x 38.5" D'
    assert norm("ITEM-1", "ITEM-1") == "ITEM-1"


def test_pool_table_is_not_a_purchase_order():
    """The digit lookahead is what stops the PO rule eating a real name."""
    assert norm("POOL TABLE OAK") == "Pool Table Oak"
    assert norm("Porter Console") == "Porter Console"


# ─── the DoD sweep: every catalog that exists ───────────────────────────────

def _catalog(org: str, date: str) -> list[dict]:
    path = config.CACHE_DIR / org / date / "Q-PROD-TOP.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@pytest.mark.parametrize("org,date", COHORT, ids=[o for o, _ in COHORT])
def test_no_new_sku_collisions_in_any_catalog(org, date):
    """clc already ships two SKUs labelled `4 Light Pendant`. That collision is
    in the source data; the rule must not ADD one anywhere."""
    rows = _catalog(org, date)
    if not rows:
        pytest.skip(f"{org} has no catalog rows")

    raw_groups, new_groups = defaultdict(set), defaultdict(set)
    for row in rows:
        item = row["item_number"]
        raw_groups[row["description"]].add(item)
        new_groups[norm(row["description"], item)].add(item)

    before = {frozenset(v) for v in raw_groups.values() if len(v) > 1}
    after = {frozenset(v) for v in new_groups.values() if len(v) > 1}
    assert after <= before, f"{org} gained a label collision: {after - before}"


@pytest.mark.parametrize("org,date", COHORT, ids=[o for o, _ in COHORT])
def test_no_catalog_row_renders_a_dimension_or_pipe(org, date):
    rows = _catalog(org, date)
    if not rows:
        pytest.skip(f"{org} has no catalog rows")
    for row in rows:
        label = norm(row["description"], row["item_number"])
        assert label.strip(), f"{org}/{row['item_number']} normalised to nothing"
        assert "|" not in label, f"{org}/{row['item_number']}: pipe survived — {label}"
        assert '" H x' not in label and '" D x' not in label, (
            f"{org}/{row['item_number']}: dimensional tail survived — {label}"
        )
