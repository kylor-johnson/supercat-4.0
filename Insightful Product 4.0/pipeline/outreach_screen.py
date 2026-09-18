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
        if _HOUSE_PREFIX.search(s) or _HOUSE_ACCOUNT.search(s):
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


def account_is_screened(account: AccountDecay, rules: ScreenRules) -> bool:
    if rules.label_is_house(account.rep_label):
        return True
    if rules.label_is_house(account.bill_to_name):
        return True
    if account.rep_number and _fold(account.rep_number) in rules.exclude_rep_numbers:
        return True
    if account.bill_to_number and _fold(account.bill_to_number) in rules.bill_to_codes:
        return True
    name = _fold(account.bill_to_name or "")
    if name and name in rules.bill_to_names:
        return True
    if name:
        for n in rules.bill_to_names:
            if n and (n in name or name in n):
                return True
    return False


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
    callable_rows = [a for a in ranked if account_needs_a_call(a)]
    before_cards = len(bundle.rep_risks)
    bundle.rep_risks = screen_rep_risks(bundle.rep_risks, rules)
    bundle.outreach_list = callable_rows[:7]
    bundle.outreach_screened = len(dropped)
    bundle.outreach_reordered = [
        account.bill_to_number for account in bundle.outreach_list
    ] != [account.bill_to_number for account in legacy_order]
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
