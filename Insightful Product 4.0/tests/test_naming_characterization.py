"""Characterization — `report_render/naming.py` (W2 / Phase 3).

Pins the display-name derivation and the four canonical output filenames for
every org in the pinned cohort. `profiles/*.md` is tracked source (unlike
`outputs/` and `pipeline/cache/`), so these run in a clean checkout.

These tests assert what the code does TODAY. They are a change detector for
Phases 4-11, not a statement that every name below is the one we want.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from report_render.naming import (
    draft_md_filename,
    gatestop_md_filename,
    parse_display_name_from_profile_text,
    preview_html_filename,
    sanitize_display_name,
    ship_html_filename,
    ship_html_path,
)

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles"
COHORT_CONF = ROOT / "tools" / "cohort.conf"


def _cohort() -> list[tuple[str, str]]:
    pairs = []
    for line in COHORT_CONF.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        org, date = line.split("\t", 1)
        pairs.append((org.strip(), date.strip()))
    return pairs


COHORT = _cohort()

# The display name each org's ratified profile H1 resolves to today, and the
# sanitized token that becomes its SHIP filename.
EXPECTED_DISPLAY = {
    "sarreid": ("Sarreid, Ltd.", "Sarreid_Ltd."),
    "cci": ("Currey & Company", "Currey_and_Company"),
    "da": ("Dainolite Ltd.", "Dainolite_Ltd."),
    "clc": ("Capital Lighting Fixture Co.", "Capital_Lighting_Fixture_Co."),
    "hfg": ("Hubbardton Forge", "Hubbardton_Forge"),
    "kal": ("Kalco Lighting / Allegri Crystal", "Kalco_Lighting___Allegri_Crystal"),
    "ali": ("Access Lighting", "Access_Lighting"),
    "sca": ("Shadow Catchers", "Shadow_Catchers"),
    "bsc": ("Butler Specialty Company", "Butler_Specialty_Company"),
    "bmc": ("Bassett Mirror", "Bassett_Mirror"),
    "bri": ("Bulbrite", "Bulbrite"),
}


def test_cohort_and_expectations_cover_the_same_orgs():
    """Guard: if the cohort grows, this file must grow with it."""
    assert {o for o, _ in COHORT} == set(EXPECTED_DISPLAY)


@pytest.mark.parametrize("org", sorted(EXPECTED_DISPLAY), ids=sorted(EXPECTED_DISPLAY))
def test_display_name_from_profile(org):
    text = (PROFILES / f"{org}.md").read_text(encoding="utf-8")
    assert parse_display_name_from_profile_text(text, org) == EXPECTED_DISPLAY[org][0]


@pytest.mark.parametrize("org", sorted(EXPECTED_DISPLAY), ids=sorted(EXPECTED_DISPLAY))
def test_sanitized_token_from_profile(org):
    text = (PROFILES / f"{org}.md").read_text(encoding="utf-8")
    display = parse_display_name_from_profile_text(text, org)
    assert sanitize_display_name(display) == EXPECTED_DISPLAY[org][1]


@pytest.mark.parametrize("org,date", COHORT, ids=[o for o, _ in COHORT])
def test_ship_filename_for_every_cohort_org(org, date):
    text = (PROFILES / f"{org}.md").read_text(encoding="utf-8")
    display = parse_display_name_from_profile_text(text, org)
    expected = f"{EXPECTED_DISPLAY[org][1]}_CEO_intelligence_report_{date}.html"
    assert ship_html_filename(display, date) == expected


# ─── H1 shape handling ──────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "h1,expected",
    [
        ("# Client Profile — Sarreid, Ltd. (`sarreid`)", "Sarreid, Ltd."),
        ("# Currey & Company (`cci`) — eCat client profile", "Currey & Company"),
        ("# Hubbardton Forge (`hfg`) — client profile", "Hubbardton Forge"),
        # en-dash and hyphen separators are accepted alongside the em-dash
        ("# Client Profile – Access Lighting (`ali`)", "Access Lighting"),
        ("# Client Profile - Access Lighting (`ali`)", "Access Lighting"),
        # no shortname tag, no prefix — the H1 is the name
        ("# Bulbrite", "Bulbrite"),
        # The (`shortname`) strip is anchored at end-of-string, so an H1 that
        # carries a trailing marker keeps the shortname tag in the display
        # name. Only the un-ratified `*.draft.md` profiles have this shape, and
        # the renderer never loads those — pinned, not endorsed.
        (
            "# Client Profile — Da (`da`)  *(INLINE DRAFT — NOT YET RATIFIED)*",
            "Da (`da`)  *(INLINE DRAFT — NOT YET RATIFIED)*",
        ),
    ],
)
def test_h1_shapes(h1, expected):
    assert parse_display_name_from_profile_text(h1, "fallback") == expected


@pytest.mark.parametrize("text", ["", "no heading at all", "## not an h1"])
def test_falls_back_when_no_h1(text):
    assert parse_display_name_from_profile_text(text, "fallback") == "fallback"


def test_empty_h1_falls_back():
    """An H1 that reduces to nothing after stripping returns the fallback."""
    assert parse_display_name_from_profile_text("# Client Profile — (`x`)", "fb") == "fb"


# ─── sanitize_display_name — the five substitutions, and what it leaves ─────

@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Sarreid, Ltd.", "Sarreid_Ltd."),
        ("Currey & Company", "Currey_and_Company"),
        ("Kalco Lighting / Allegri Crystal", "Kalco_Lighting___Allegri_Crystal"),
        ("O'Brien Lighting", "OBrien_Lighting"),
        # the trailing period is NOT stripped — it survives into the filename
        ("Dainolite Ltd.", "Dainolite_Ltd."),
        # characters outside the five substitutions pass through untouched
        ("Smith (US) Inc.", "Smith_(US)_Inc."),
    ],
)
def test_sanitize_display_name(raw, expected):
    assert sanitize_display_name(raw) == expected


# ─── The four filename builders ─────────────────────────────────────────────

def test_filename_builders():
    assert (
        ship_html_filename("Sarreid, Ltd.", "2026-07-02")
        == "Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html"
    )
    assert preview_html_filename("sarreid", "2026-07-02") == "sarreid_PREVIEW_2026-07-02.html"
    assert draft_md_filename("sarreid", "2026-07-02") == "sarreid_DRAFT_2026-07-02.md"
    assert gatestop_md_filename("bsc", "2026-07-14") == "bsc_GATESTOP_2026-07-14.md"


def test_ship_html_path_joins_onto_the_outputs_dir(tmp_path):
    p = ship_html_path(tmp_path, "Currey & Company", "2026-07-02")
    assert p.parent == tmp_path
    assert p.name == "Currey_and_Company_CEO_intelligence_report_2026-07-02.html"
