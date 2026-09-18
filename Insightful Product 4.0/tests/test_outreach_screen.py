"""House / DTC / org-self screen — applied to decay BEFORE the top-7 cut."""
from __future__ import annotations

from pipeline.gather import AccountDecay, RepRisk
from pipeline.outreach_screen import (
    account_is_screened,
    looks_like_code,
    parse_profile_screens,
    screen_accounts,
    screen_rep_risks,
)


def _acct(**kwargs) -> AccountDecay:
    defaults = dict(
        bill_to_number="X",
        bill_to_name="Dealer Co",
        rep_number="1",
        rep_label="Jane Rep",
        ltm_rev=100_000.0,
        recent_6mo=40_000.0,
        prior_6mo=60_000.0,
        recent_vs_prior_pct=-33.0,
        days_silent=10,
        mean_order_gap_days=20.0,
        lifetime_invoices=12,
        last_invoice_date="2026-06-01",
    )
    defaults.update(kwargs)
    return AccountDecay(**defaults)


def test_the_house_rep_does_not_screen_the_dealer_it_services():
    """The house rule is a REP-level exclusion, not a reason to hide a dealer.

    Lighting New York is a real kal account that happens to be serviced
    in-house. Screening it here took it off the call list and out of the
    at-risk total the moment S1 started carrying rep labels — the CEO
    stopped hearing about an account that is genuinely slipping.
    """
    rules = parse_profile_screens("")
    in_house = _acct(rep_label="HOUSE ACCOUNT", bill_to_name="LIGHTING NEW YORK")
    dealer = _acct(rep_label="JASON SCHLEICH", bill_to_name="LIGHTOLOGY")
    assert not account_is_screened(in_house, rules)
    assert not account_is_screened(dealer, rules)


def test_a_bill_to_actually_named_house_is_still_screened():
    """The bill-to side of the rule is untouched: a sample/house *account*
    is not a dealer and never belonged on a call list."""
    rules = parse_profile_screens("")
    assert account_is_screened(_acct(bill_to_name="HOUSE ACCOUNT", rep_label="JASON SCHLEICH"), rules)
    assert account_is_screened(_acct(bill_to_name="HOUSE SAMPLES", rep_label="JASON SCHLEICH"), rules)


def test_the_house_rep_is_still_kept_off_the_rep_surfaces():
    """screen_rep_risks is where the house exclusion belongs, and still is."""
    kept = screen_rep_risks(
        [
            RepRisk(rep_number="0999", rep_name_tier2="House Account", dollars_at_risk=1.0,
                    accounts_at_risk=1, leak_dollars=None, leak_pct=None),
            RepRisk(rep_number="0011", rep_name_tier2="Kirk Marshall Sales", dollars_at_risk=1.0,
                    accounts_at_risk=1, leak_dollars=None, leak_pct=None),
        ],
        parse_profile_screens(""),
    )
    assert [r.rep_number for r in kept] == ["0011"]


def test_profile_dtc_codes_screen_hfg_webstores():
    profile = """
## 4. House / sample / internal accounts to screen

- `10505` Handmade In Vermont.com (~$716K LTM) — HF's own DTC site
- `35639` Shop Hubbardton Forge (~$559K LTM) — HF's own retail site
- **`rep_number = NENOREP`** ($1.35M LTM) — a no-rep placeholder bucket
"""
    rules = parse_profile_screens(profile)
    dtc = _acct(bill_to_number="10505", bill_to_name="", rep_number="NENOREP", rep_label=None)
    other = _acct(bill_to_number="1489", bill_to_name="", rep_number="CANOREP")
    kept, dropped = screen_accounts([dtc, other], rules)
    assert [a.bill_to_number for a in dropped] == ["10505"]
    assert [a.bill_to_number for a in kept] == ["1489"]


def test_looks_like_code_for_unnamed_and_numeric():
    assert looks_like_code("")
    assert looks_like_code("(unnamed)")
    assert looks_like_code("0003476")
    assert looks_like_code("10505")
    assert not looks_like_code("France and Sons")
    assert not looks_like_code("LIGHTING NEW YORK")


def test_looks_like_code_for_hfg_pipe_delimited_sku_description():
    raw = (
        '9N00145405-3-14-DL105 | TYPE DL-105 | 34.5" H x 64.5" D '
        'x 92.5" L | OPEN CENTER'
    )
    assert looks_like_code(raw)
