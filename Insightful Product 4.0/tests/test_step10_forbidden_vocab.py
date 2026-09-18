"""Characterization — §P forbidden-vocabulary sweep, check [4] (W2 / Phase 3).

Phase 8 rewrites this list ("claims, not tokens"). Every one of the 83 patterns
in `_FORBIDDEN_PATTERNS` therefore gets BOTH:

  * a fires-on case — prose that must still be caught, and
  * a does-not-fire-on case — the near-miss or §P.2 allow-listed context that
    must stay clean.

`test_every_forbidden_pattern_is_covered` fails if a pattern is added without a
pair, so the list cannot silently loosen.

A does-not-fire-on case asserts only that THAT pattern stays quiet — the prose
may legitimately trip a different rule. The six §P.2 allow-lists
(yoy-acronym / ecat / cohort / supercat / product / version) additionally get
whole-sweep-clean tests below.
"""
from __future__ import annotations

import re

import pytest
from bs4 import BeautifulSoup

from report_render.step10_check import (
    _ECAT_ALLOWED_SECTIONS,
    _FORBIDDEN_PATTERNS,
    _check_forbidden_vocab,
    _cohort_allowed,
    _ecat_allowed_in_section,
    _nearest_id,
    _yoy_allowed,
)


def _soup(inner: str, section_id: str = "thisweek") -> BeautifulSoup:
    return BeautifulSoup(
        f'<html><body><div class="page">'
        f'<section id="{section_id}">{inner}</section>'
        f"</div></body></html>",
        "lxml",
    )


def _violations(text: str, section_id: str = "thisweek") -> list[str]:
    return _check_forbidden_vocab(_soup(f"<p>{text}</p>", section_id))


_TOKEN_RE = re.compile(r"^\[4\] §P forbidden token '(.*?)' \((.*?)\) in section", re.S)


def _tokens(text: str, section_id: str = "thisweek") -> list[str]:
    """The matched tokens only — the message also carries a context excerpt."""
    out = []
    for v in _violations(text, section_id):
        m = _TOKEN_RE.match(v)
        if m:
            out.append(m.group(1))
    return out


def _fires(pattern: str, text: str, section_id: str = "thisweek") -> bool:
    """Did THIS pattern produce a violation (ignoring any others)?"""
    return any(re.fullmatch(pattern, tok, re.I) for tok in _tokens(text, section_id))


# ─── The 83-pattern matrix ──────────────────────────────────────────────────
# (regex source, fires-on prose, does-not-fire-on prose)

CASES: list[tuple[str, str, str]] = [
    # § P.1.A — SaaS / CRO / revenue-ops
    (r"\bNRR\b", "NRR came in strong.", "The NRRX index is unrelated."),
    (r"\bnet\s+revenue\s+retention\b", "Net revenue retention held.", "Net revenue rose."),
    (r"\bGRR\b", "GRR held flat.", "GRRs are noise."),
    (r"\bgross\s+revenue\s+retention\b", "Gross revenue retention held.", "Gross revenue grew."),
    (r"\bMRR\b", "MRR is the wrong lens.", "The MRRX label is unrelated."),
    (r"\bARR\b", "ARR is the wrong lens.", "The account is in arrears."),
    (r"\bnew\s+logos?\b", "Chasing new logos.", "Chasing new dealer names."),
    (r"\bplaybook\b", "Run the playbook.", "The play worked."),
    (r"\bcohort\b", "The cohort shrank.", "The buyer cohort shrank."),
    (r"\bICP\b", "Your ICP is clear.", "Your ideal customer is clear."),
    (r"\bTAM\b", "TAM is large.", "Tampa dealers grew."),
    (r"\bSAM\b", "SAM is large.", "Sample orders held."),
    (r"\bCAC\b", "CAC is rising.", "A cache of orders."),
    (r"\bLTV\b", "LTV of a dealer.", "Lifetime value of a dealer."),
    # No trailing period in the fires-on prose: `_yoy_allowed` treats a bare
    # `.` as a number (see test_a_bare_full_stop_satisfies_the_yoy_proximity_test).
    (r"\bMoM\b", "The MoM view is noisy", "Spend rose 4% MoM"),
    (r"\bQoQ\b", "The QoQ view is noisy", "Spend rose 4% QoQ"),
    (r"\bYoY\b", "The YoY view is noisy", "Spend rose 82.5% YoY"),
    (r"\bfunnel\b", "Top of funnel.", "Three funnels."),
    (r"\bpipeline\s+coverage\b", "Pipeline coverage is thin.", "The order pipeline is thin."),
    (r"\bwin\s+rate\b", "Win rate improved.", "Reorder rate improved."),
    (r"\bmotion\b", "The selling motion.", "The promotional calendar."),
    (r"\bGTM\b", "The GTM plan.", "The go-to-market plan."),
    (r"\bexpansion\s+revenue\b", "Expansion revenue grew.", "Expansion of revenue."),
    (r"\bland\s+and\s+expand\b", "Land and expand.", "Landed and expanded."),
    (r"\bPLG\b", "PLG is not our model.", "The plug-in is not our model."),
    (r"\bnorth[-\s]?star\b", "The north star metric.", "The northern star."),
    (r"\bDAU\b", "DAU is not a metric here.", "Daughter accounts are separate."),
    (r"\bMAU\b", "MAU is not a metric here.", "Maui dealers are separate."),

    # § P.1.B — internal codes / system identifiers
    (r"\bVM-\d+\b", "VM-12 fired.", "The VM catalog."),
    (r"\bQ-(?:ECON|CHAN|CI|PROV|ORG)-\w+\b", "Q-ECON-00 returned zero.", "Q-SALES-01 returned zero."),
    (r"\bRung-\d\b", "Rung-3 evidence.", "A rung of the ladder."),
    (r"\boperator-\d\b", "See operator-2.", "Operator training."),
    (r"\bRS-\d+\b", "RS-01 sold the most.", "The RS label."),
    (r"\bFEED_COMPLETENESS\b", "FEED_COMPLETENESS is STALE.", "Feed completeness is stale."),
    (r"\bCOMMERCE_CONFIDENCE\b", "COMMERCE_CONFIDENCE is PARTIAL.", "Commerce confidence is partial."),
    (r"\bREP_IDENTITY_TIER\b", "REP_IDENTITY_TIER is 2.", "Rep identity tier is 2."),
    (r"\bDATA_MASS_TIER\b", "DATA_MASS_TIER is 1.", "Data mass tier is 1."),
    (r"\bREPORT_INTELLIGENCE_TIER\b", "REPORT_INTELLIGENCE_TIER is 0.", "Report intelligence tier is 0."),
    (r"\bTIER-[123]\b", "A TIER-2 org.", "A Tier 2 org."),
    (
        r"\bMode\s+[123]\s+(?:Standard|Activation|Reactivation)\b",
        "This is Mode 1 Standard.",
        "This is Mode 1 reporting.",
    ),
    (r"\bpreflight\b", "The preflight fired.", "A pre-flight check."),
    (r"\bfeed\s+posture\b", "The feed posture is single.", "The feed is stale."),
    (r"\bsingle-feed\s+posture\b", "A single-feed posture.", "A single-feed view."),
    (r"\bGate-STOP\b", "A Gate-STOP artifact.", "The gate stopped short."),
    (r"\bcohort-validation\b", "A cohort-validation pass.", "A validation pass."),

    # § P.1.C — system / pipeline / process language
    (r"\bthe\s+operator\b", "The operator decides.", "An operator decides."),
    (r"\bthe\s+report\s+run\b", "The report run finished.", "The report shows this."),
    (r"\bthis\s+run\b", "This run produced 11 reports.", "This report produced the list."),
    (r"\bthe\s+render\s+pipeline\b", "The render pipeline emitted it.", "The render step emitted it."),
    (r"\bthe\s+renderer\b", "The renderer emitted it.", "A renderer emitted it."),
    (r"\bthe\s+gate\s+(?:passed|failed|fired)\b", "The gate failed.", "The gate opened."),
    (r"\bdelivered\s+HTML\b", "The delivered HTML.", "The delivered report."),
    (r"\breport\s+stage\s+badge\b", "The report stage badge.", "The report stage."),
    (r"\bTODO\b", "TODO: fix this.", "A to do list."),
    (r"\bFIXME\b", "FIXME before shipping.", "Fix me before shipping."),
    (r"\bhouse_suspect\b", "Flagged house_suspect.", "Flagged as a house suspect."),
    (r"\bhouse-rep\b", "A house-rep order.", "A house rep order."),
    (r"\bhouse/sample/accom\b", "Excludes house/sample/accom.", "Excludes house samples."),
    (r"\bshortname\b", "The shortname is sarreid.", "The short name is Sarreid."),
    (r"\borg_id\b", "Keyed on org_id.", "Keyed on org id."),
    (r"\borganization_id\b", "Keyed on organization_id.", "Keyed on organization id."),
    (r"\bportal_invoices\b", "From portal_invoices.", "From portal invoices."),
    (r"\bportal_orders\b", "From portal_orders.", "From portal orders."),
    (r"\bsales_data\b", "From sales_data.", "From sales data."),

    # DB columns
    (r"\brep_number\b", "Grouped by rep_number.", "Grouped by rep number."),
    (r"\brep_name\b", "Grouped by rep_name.", "Grouped by rep name."),
    (r"\brep_label\b", "Grouped by rep_label.", "Grouped by rep label."),
    (r"\bbill_to_number\b", "Keyed on bill_to_number.", "Keyed on the bill-to number."),
    (r"\bship_to_number\b", "Keyed on ship_to_number.", "Keyed on the ship-to number."),
    (r"\bitem_number\b", "Keyed on item_number.", "Keyed on the item number."),
    (r"\bcustomer_num\b", "Keyed on customer_num.", "Keyed on the customer number."),
    (
        r"\bcustomer_bill_to_number\b",
        "Keyed on customer_bill_to_number.",
        "Keyed on the customer bill-to number.",
    ),
    (r"\borg_user_id\b", "Keyed on org_user_id.", "Keyed on the user id."),
    (r"\bnet_amount\b", "Summed net_amount.", "Summed the net amount."),
    (r"\border_origin\b", "Split by order_origin.", "Split by order origin."),
    (r"\bsubmit_date\b", "Sorted by submit_date.", "Sorted by submit date."),
    (r"\bis_submitted\b", "Filtered on is_submitted.", "Filtered on submitted orders."),
    (
        r"\b\w+_\w+\s*[→\-]+>?\s*\w+_\w+\b",
        "Mapped order_source → channel_label.",
        "Mapped order_source and channel_label.",
    ),

    # § P.1.D — internal product names / version numbers
    (r"\bInsightful\s+Product\b", "Built by Insightful Product.", "Built by the Product team."),
    (r"\bInsightful\b(?!\s+Product)", "Built by Insightful.", "Built by Insightful Product."),
    (r"\bSuperCat\b", "Delivered by SuperCat.", "Delivered by your vendor."),
    (r"\beCat\b", "Orders placed in eCat.", "Orders placed on the platform."),
    (r"\b[Vv]4(?:\.\d)?\b", "The product v4.0 layout.", "The v4.0 layout."),
]


def test_every_forbidden_pattern_is_covered():
    """Phase 8 rewrites this list — it must not lose a rule unnoticed."""
    assert {p for p, _ in _FORBIDDEN_PATTERNS} == {p for p, _, _ in CASES}
    assert len(CASES) == len(_FORBIDDEN_PATTERNS) == 83


@pytest.mark.parametrize("pattern,positive,_neg", CASES, ids=[p for p, _, _ in CASES])
def test_pattern_fires_on_its_positive_case(pattern, positive, _neg):
    assert _fires(pattern, positive), f"{pattern!r} did not fire on {positive!r}"


@pytest.mark.parametrize("pattern,_pos,negative", CASES, ids=[p for p, _, _ in CASES])
def test_pattern_does_not_fire_on_its_negative_case(pattern, _pos, negative):
    assert not _fires(pattern, negative), f"{pattern!r} fired on {negative!r}"


# ─── §P.2 allow-lists — the whole sweep stays clean ─────────────────────────

@pytest.mark.parametrize(
    "text",
    [
        "Spend rose 82.5% YoY",
        "Spend rose 4% QoQ",
        "Down 3.1% MoM",
    ],
)
def test_yoy_acronyms_are_clean_next_to_a_number(text):
    assert _violations(text) == []


def test_a_bare_full_stop_satisfies_the_yoy_proximity_test():
    """`_yoy_allowed` scans its ±30-char window with `[\\d\\.%]` — the `.` is
    inside the class, so any sentence-ending period reads as a number. Pinned,
    not endorsed (W2 finding F-1)."""
    assert _violations("The YoY view is noisy") != []
    assert _violations("The YoY view is noisy.") == []


@pytest.mark.xfail(
    reason="W2 finding F-1: the `[\\d\\.%]` proximity window treats a sentence-ending "
           "period as a number, so any `YoY` in ordinary prose passes (Phase 8)",
    strict=True,
)
def test_a_bare_full_stop_should_not_satisfy_the_yoy_proximity_test():
    assert _violations("The YoY view is noisy.") != []


@pytest.mark.xfail(
    reason="W2 finding F-2: `_yoy_allowed` reads the immediate parent only, so a "
           "number in the surrounding block does not reach `<strong>YoY</strong>` "
           "— the exact shape its own docstring allows (Phase 8)",
    strict=True,
)
def test_yoy_is_allowed_when_the_number_is_in_the_surrounding_block():
    assert _violations("+82.5% <strong>YoY</strong>") == []


def test_yoy_is_allowed_as_a_column_header_with_no_number_in_it():
    soup = _soup("<table><tr><th>YoY</th></tr><tr><td>-12%</td></tr></table>")
    assert _check_forbidden_vocab(soup) == []


def test_yoy_alone_in_a_td_still_fires():
    soup = _soup("<table><tr><td>The YoY view is noisy</td></tr></table>")
    assert any("YoY" in v for v in _check_forbidden_vocab(soup))


@pytest.mark.parametrize("section_id", sorted(_ECAT_ALLOWED_SECTIONS))
def test_ecat_is_allowed_in_its_five_sections(section_id):
    assert _violations("Orders placed in eCat.", section_id) == []


@pytest.mark.parametrize("section_id", ["thisweek", "thismonth", "team", "risk", "products", "base"])
def test_ecat_fires_outside_those_sections(section_id):
    assert any("eCat" in v for v in _violations("Orders placed in eCat.", section_id))


def test_ecat_allow_list_membership():
    assert _ecat_allowed_in_section("summary") is True
    assert _ecat_allowed_in_section("thisweek") is False
    assert _ecat_allowed_in_section(None) is False


@pytest.mark.parametrize("text", ["The buyer cohort held.", "The design cohort held."])
def test_domain_true_cohort_phrases_are_clean(text):
    assert _violations(text) == []


def test_cohort_allowed_needs_the_qualifier_immediately_before():
    text = "buyer cohort"
    assert _cohort_allowed(text, (6, 12)) is True
    bare = "the cohort"
    assert _cohort_allowed(bare, (4, 10)) is False


def test_supercat_is_allowed_in_the_about_block():
    assert _violations("About SuperCat — we build selling software.") == []


def test_supercat_fires_elsewhere():
    assert any("SuperCat" in v for v in _violations("Delivered by SuperCat."))


@pytest.mark.parametrize(
    "text",
    [
        "Insightful CEO Brief",
        "Insightful Customer Intelligence",
    ],
)
def test_product_name_is_allowed_beside_its_own_title(text):
    assert _violations(text) == []


def test_version_token_needs_a_version_word_nearby():
    """`v4.0` on its own is clean; `product v4.0` / `version v4` are not."""
    assert _violations("The v4.0 layout.") == []
    assert any("v4" in v for v in _violations("The product v4.0 layout."))


def test_a_dollar_figure_is_not_read_as_a_version():
    assert _violations("Invoiced $15.64M this year.") == []


# ─── Document-level skips ───────────────────────────────────────────────────

def test_gatestop_documents_skip_the_whole_sweep():
    soup = BeautifulSoup(
        '<html><body><div class="page"><div class="gate-stop-banner">STOP</div>'
        '<section id="preflights"><p>Q-ECON-00 returned zero. COMMERCE_CONFIDENCE is NONE.</p>'
        "</section></div></body></html>",
        "lxml",
    )
    assert _check_forbidden_vocab(soup) == []


def test_the_appendix_is_internal_provenance():
    assert _violations("Q-ECON-00 returned zero.", "appendix") == []


def test_the_footer_ledger_is_internal_provenance():
    soup = BeautifulSoup(
        '<html><body><div class="page"><div class="footer-ledger">'
        "<span>[STEP-10 LEDGER · Q-ECON-00 · 1:pass]</span></div></div></body></html>",
        "lxml",
    )
    assert _check_forbidden_vocab(soup) == []


def test_clean_client_prose_produces_no_violations():
    assert _violations(
        "France and Sons is down 56% in six months and ordered within the last day, "
        "so this is a slip, not a goodbye."
    ) == []


def test_identical_messages_are_deduped():
    """The same token in one text node reports once per occurrence position,
    but an identical message is emitted only once."""
    v = _violations("NRR. NRR.")
    assert len(v) == len(set(v))


def test_violation_message_names_the_token_context_and_section():
    v = _violations("The playbook is set.", "thismonth")
    assert len(v) == 1
    assert "'playbook'" in v[0]
    assert "(saas)" in v[0]
    assert "#thismonth" in v[0]


# ─── `_nearest_id` / `_yoy_allowed` units ───────────────────────────────────

def test_nearest_id_walks_up_from_a_string_node():
    soup = _soup("<div><p>hello</p></div>", "growth")
    node = soup.find(string="hello")
    assert _nearest_id(node) == "growth"


def test_nearest_id_returns_none_when_nothing_has_an_id():
    soup = BeautifulSoup("<div><p>hello</p></div>", "lxml")
    assert _nearest_id(soup.find(string="hello")) is None


def test_yoy_allowed_window_is_thirty_characters():
    text = "12% " + " " * 40 + "YoY"
    span = (text.index("YoY"), len(text))
    assert _yoy_allowed(text, span) is False
    near = "12% YoY"
    assert _yoy_allowed(near, (4, 7)) is True
