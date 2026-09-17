"""P0-5 — ALL-CAPS account names were shouted into a CEO brief.

sarreid and cci store 12/12 account names in ALL CAPS, so the priority card
read "FRANCE AND SONS · AFA STORES · THE SWAN'S NEST INC". clc already stores
mixed case and must not be touched.
"""
from __future__ import annotations

import pytest

from pipeline.gather import normalize_account_name as n


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("FRANCE AND SONS", "France and Sons"),
        ("ANTIQUE PURVEYOR", "Antique Purveyor"),
        ("LIGHTING NEW YORK", "Lighting New York"),
        # possessive s stays lowercase; Inc/Co are words, not shouted acronyms
        ("THE SWAN'S NEST INC", "The Swan's Nest Inc"),
        ("O'BRIEN LIGHTING CO.", "O'Brien Lighting Co."),
        # real acronyms survive
        ("ENGLISH GEORGIAN AMERICA LLC", "English Georgian America LLC"),
        ("RENEGADE FURNITURE GROUP INC DBA", "Renegade Furniture Group Inc DBA"),
        ("SMITH-JONES LLC", "Smith-Jones LLC"),
        # ampersand and conjunctions
        ("OP JENKINS FURNITURE & DESIGN", "Op Jenkins Furniture & Design"),
    ],
)
def test_normalises_all_caps_names(raw, expected):
    assert n(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "1Stoplighting.com dba Belami Inc",   # clc — already mixed case
        "Currey & Company",
        "1489",                                # hfg — a code, not a name
        "",
    ],
)
def test_leaves_non_all_caps_untouched(raw):
    assert n(raw) == raw


def test_leading_small_word_is_still_capitalised():
    assert n("THE LIGHTING GROUP") == "The Lighting Group"
