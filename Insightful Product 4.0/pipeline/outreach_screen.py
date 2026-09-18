"""House / DTC / org-self screen for outreach rows.

Applied *after* S1 load and *before* the top-7 cut. The house-rep auto-rule
and per-org EXCLUDE table already exist for rep-grain SQL; they were never
applied to the decay extract that feeds the call list. Profile section 4
carries DTC / org-self bill-tos (hfg webstores) that the auto-rule cannot
see by name.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import cache, config
from .gather import (
    AccountDecay,
    GatherBundle,
    RepRisk,
    UnactivatedAccount,
    account_is_callable,
    rep_label_is_house,
    account_needs_a_call,
    outreach_sort_key,
)


_HOUSE_PREFIX = re.compile(r"^house\b", re.I)
_HOUSE_ACCOUNT = re.compile(r"\bhouse account\b", re.I)
_NUMERIC = re.compile(r"^[0-9]+$")
_CODEISH = re.compile(r"^[A-Z0-9][A-Z0-9._-]{1,20}$")
_SECTION_4 = re.compile(r"^##\s+4\.\s", re.M)
_NEXT_H2 = re.compile(r"^##\s+", re.M)
_BT_LINE = re.compile(
    r"^[\s>*-]*`([A-Za-z0-9][A-Za-z0-9._-]{1,24})`\s+(.+)$",
    re.M,
)
_REP_NUMBER = re.compile(
    r"rep_number\s*=\s*`([^`]+)`",
    re.I,
)
_GLOBBY = re.compile(r"[*%]")


@dataclass
class ScreenRules:
    exclude_labels: set[str] = field(default_factory=set)
    bill_to_codes: set[str] = field(default_factory=set)
    bill_to_names: set[str] = field(default_factory=set)
    exclude_rep_numbers: set[str] = field(default_factory=set)

    def label_is_house(self, label: str | None) -> bool:
        s = (label or "").strip()
        if not s:
            return False
        if rep_label_is_house(s):
            return True
        return s.casefold() in self.exclude_labels


def _fold(s: str) -> str:
    return s.strip().casefold()


def _section_4(profile_text: str) -> str:
    m = _SECTION_4.search(profile_text or "")
    if not m:
        return ""
    rest = profile_text[m.end() :]
    n = _NEXT_H2.search(rest)
    return rest[: n.start()] if n else rest


def parse_profile_screens(profile_text: str) -> ScreenRules:
    """Pull DTC / org-self bill-tos and excluded rep numbers from profile §4."""
    rules = ScreenRules()
    section = _section_4(profile_text)
    if not section:
        return rules
    for m in _BT_LINE.finditer(section):
        code = m.group(1)
        if _GLOBBY.search(code):
            continue
        rules.bill_to_codes.add(_fold(code))
        tail = re.split(r"\s+[—–]\s+", m.group(2), maxsplit=1)[0]
        tail = re.sub(r"\s*\([^)]*\)\s*$", "", tail).strip()
        if tail and not _NUMERIC.fullmatch(tail):
            rules.bill_to_names.add(_fold(tail))
    for m in _REP_NUMBER.finditer(section):
        tok = m.group(1).strip()
        if tok:
            rules.exclude_rep_numbers.add(_fold(tok))
    return rules


def load_screen_rules(org: str, profile_text: str = "") -> ScreenRules:
    rules = parse_profile_screens(profile_text)
    exclusions = config.load_house_exclusions()
    try:
        org_id = str(cache.resolve_org_id(org))
    except (ValueError, KeyError):
        org_id = ""
    for label in exclusions.get("exclude", {}).get(org_id, []):
        if label:
            rules.exclude_labels.add(_fold(str(label)))
    return rules


def _profile_text(org: str) -> str:
    for name in (f"{org}.md", f"{org}.draft.md"):
        path = config.PROFILES_DIR / name
        if path.exists():
            return path.read_text(encoding="utf-8")
    return ""


def bill_to_is_screened(code: str | None, name: str | None, rules: ScreenRules) -> bool:
    """The bill-to half of the screen, in one place.

    Both the call list and the Q-53 activation list have to apply it: hfg's
    profile names 10505 (Handmade In Vermont.com) and 35639 (Shop Hubbardton
    Forge) as its OWN direct-to-consumer sites, and they are the #5 and #10
    rows of its unactivated list. Telling a CEO to go activate their own
    webstore is the kind of thing that costs a report its credibility.
    """
    if rules.label_is_house(name):
        return True
    code_f = _fold(code or "")
    if code_f and code_f in rules.bill_to_codes:
        return True
    name_f = _fold(name or "")
    if not name_f:
        return False
    if name_f in rules.bill_to_names:
        return True
    return any(n and (n in name_f or name_f in n) for n in rules.bill_to_names)


def screen_unactivated(
    accounts: list[UnactivatedAccount], rules: ScreenRules
) -> list[UnactivatedAccount]:
    """Q-53 rows that survive the profile's house/internal bill-to screen."""
    return [
        a for a in accounts
        if not bill_to_is_screened(a.customer_code, a.customer_name, rules)
    ]


def account_is_screened(account: AccountDecay, rules: ScreenRules) -> bool:
    # The house rule is a REP-level exclusion: profiles scope it to "excluded
    # from the rep leaderboard render" and from the leakage math, which is
    # what screen_rep_risks() below enforces. It is NOT a reason to hide the
    # dealer. Lighting New York, Capitol Lighting and Rainbow Lighting are
    # real kal accounts that happen to be serviced in-house; screening them
    # here took $0.21M of live decay off the watchlist and dropped one of the
    # seven calls. This never fired before only because those orgs had no rep
    # labels to match — pulling S1 with the name bridge turned it on, and the
    # CEO stopped being told about accounts that are genuinely slipping.
    if account.rep_number and _fold(account.rep_number) in rules.exclude_rep_numbers:
        return True
    return bill_to_is_screened(account.bill_to_number, account.bill_to_name, rules)


def screen_accounts(
    accounts: list[AccountDecay], rules: ScreenRules
) -> tuple[list[AccountDecay], list[AccountDecay]]:
    kept: list[AccountDecay] = []
    dropped: list[AccountDecay] = []
    for a in accounts:
        if account_is_screened(a, rules):
            dropped.append(a)
        else:
            kept.append(a)
    return kept, dropped


def screen_rep_risks(risks: list[RepRisk], rules: ScreenRules) -> list[RepRisk]:
    out: list[RepRisk] = []
    for r in risks:
        if rules.label_is_house(r.rep_name_tier2):
            continue
        if r.rep_number and _fold(r.rep_number) in rules.exclude_rep_numbers:
            continue
        out.append(r)
    return out


def apply(bundle: GatherBundle, profile_text: str | None = None) -> GatherBundle:
    """Mutate *bundle*: screen decay, rebuild outreach_list, drop house cards."""

    text = profile_text if profile_text is not None else _profile_text(bundle.org)
    rules = load_screen_rules(bundle.org, text)
    kept, dropped = screen_accounts(bundle.decay, rules)
    legacy_order = sorted(kept, key=lambda account: account.ltm_rev, reverse=True)[:7]
    ranked = sorted(kept, key=outreach_sort_key, reverse=True)
    bundle.decay = ranked
    # T1-4: only accounts that have actually slipped belong on the call list.
    # They stay in `decay` so the watchlist and the coaching cards still see
    # them; this gates the seven rows a rep is told to phone this week.
    callable_rows = [a for a in ranked if account_is_callable(a)]
    before_cards = len(bundle.rep_risks)
    bundle.rep_risks = screen_rep_risks(bundle.rep_risks, rules)
    bundle.outreach_list = callable_rows[:7]
    # C1: the watchlist renders from the same set. `decay` keeps every
    # screened row so signal detection is unchanged; only what is shown
    # under the heading "risk watchlist" is gated on actual risk.
    bundle.watchlist = callable_rows
    bundle.outreach_screened = len(dropped)
    bundle.outreach_reordered = [
        account.bill_to_number for account in bundle.outreach_list
    ] != [account.bill_to_number for account in legacy_order]
    bundle.unactivated_accounts = screen_unactivated(bundle.unactivated_accounts, rules)
    bundle.screened_rep_labels = frozenset(rules.exclude_labels)
    bundle.house_cards_screened = before_cards - len(bundle.rep_risks)
    return bundle


def looks_like_code(value: str | None) -> bool:
    s = (value or "").strip()
    if not s:
        return True
    if s.casefold() in {"(unnamed)", "unnamed", "n/a", "-", "—"}:
        return True
    if _NUMERIC.fullmatch(s):
        return True
    if "|" in s:
        return True
    if _CODEISH.fullmatch(s) and not re.search(r"[a-z]", s) and len(s) <= 12:
        return True
    return False
