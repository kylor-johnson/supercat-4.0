"""Gather: cache CSVs → typed dataclasses keyed by query family.

Single responsibility: turning CSV rows into well-named Python structures
for the rest of the pipeline. This module does not query the database
and does not interpret semantics (no "is this a decline?" — that's
signals.py).

Missing CSVs become empty lists (or None on singletons); templates surface
that as a QUERY-NEEDED marker instead of failing the render.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .cache import CachePaths


# ─── Row types ─────────────────────────────────────────────────────────────
# P0-5: several ERPs store account names ALL-CAPS (sarreid and cci are 12/12).
# Rendering them raw shouted "FRANCE AND SONS · AFA STORES" out of a CEO brief.
# Only fully-uppercase names are touched; anything already mixed-case (clc's
# "1Stoplighting.com dba Belami Inc") is returned untouched.
# Stay uppercase. Deliberately EXCLUDES Inc / Co / Corp / Ltd — those read as
# shouting in a title-cased name ("Swan's Nest INC"), so they get capitalised
# like any other word.
_NAME_ACRONYMS = frozenset({
    "LLC", "L.L.C.", "LLP", "PLC", "PC", "LP", "USA", "US", "DBA",
    "II", "III", "IV", "TV", "AV", "LED", "HVAC",
    "NY", "LA", "SF", "DC", "NE", "SE", "NW", "SW",
})

# Lowercased unless they lead the name.
_NAME_SMALL_WORDS = frozenset({"and", "of", "the", "for", "at", "in", "on", "to", "by"})


def _cap_word(word: str) -> str:
    """Capitalise one token: SWAN'S -> Swan's, O'BRIEN -> O'Brien, A-B -> A-B."""
    if not word:
        return word
    low = word.lower()
    out = low[0].upper() + low[1:]
    # Letters after an apostrophe or hyphen: capitalise real words ("O'Brien",
    # "Smith-Jones") but not a possessive "s" ("Swan's").
    out = re.sub(
        r"([\'\-])([a-z]+)",
        lambda m: m.group(1) + (m.group(2).capitalize() if len(m.group(2)) > 1 else m.group(2)),
        out,
    )
    return out


def normalize_account_name(name: str) -> str:
    """Title-case an ALL-CAPS account name, preserving known acronyms."""
    s = (name or "").strip()
    if not s or not s.isupper():
        return s
    words = s.split()
    out: list[str] = []
    for i, w in enumerate(words):
        if w.strip(".,()").upper() in _NAME_ACRONYMS:
            out.append(w)
            continue
        capped = _cap_word(w)
        if i > 0 and capped.strip(".,()").lower() in _NAME_SMALL_WORDS:
            capped = capped.lower()
        out.append(capped)
    return " ".join(out)


@dataclass
class AccountDecay:
    bill_to_number: str
    bill_to_name: str
    rep_number: Optional[str]
    rep_label: Optional[str]
    ltm_rev: float
    recent_6mo: float
    prior_6mo: float
    recent_vs_prior_pct: Optional[float]
    days_silent: int
    mean_order_gap_days: float
    lifetime_invoices: int
    last_invoice_date: str

    @property
    def has_display_name(self) -> bool:
        """True when bill_to_name is a real account name, not a code or blank."""
        from .outreach_screen import looks_like_code

        name = (self.bill_to_name or "").strip()
        if looks_like_code(name):
            return False
        if self.bill_to_number and name.casefold() == self.bill_to_number.casefold():
            return False
        return True

    @property
    def has_display_rep(self) -> bool:
        """True when rep_label is a person/agency name, not a code."""
        from .outreach_screen import looks_like_code

        label = (self.rep_label or "").strip()
        if looks_like_code(label):
            return False
        if re.fullmatch(r"rep\s*\S+", label, re.I):
            return False
        return True

    @property
    def display_label(self) -> Optional[str]:
        """Call-list / watchlist identity — never a blank ``rep  `` or ``rep (n)``."""
        return display_rep_label(
            rep_name_tier2=self.rep_label,
            rep_number=self.rep_number,
            rep_label=self.rep_label,
        )

    @property
    def is_real_decline(self) -> bool:
        if self.prior_6mo <= 0:
            return False
        return (self.recent_6mo / self.prior_6mo) < 0.6 and self.ltm_rev > 20_000

    @property
    def is_cadence_cliff(self) -> bool:
        if self.mean_order_gap_days <= 0 or self.recent_vs_prior_pct is None:
            return False
        return self.days_silent > 2 * self.mean_order_gap_days and self.recent_vs_prior_pct >= 0


# T1-4: a "do this week" list is a list of accounts where something is WRONG.
# Ranking was actionability x dollars with a 0.3 floor for healthy accounts, so a
# big growing book outranked a small collapsing one: hfg row 1 was +6.7% (0.3 x
# $602K) ahead of an account down 81.9% (0.9 x $130K), and kal row 1 was +20.0%.
# Sarreid never exposed it because its largest accounts happened to be the
# declining ones — the Sarreid overfit in miniature.
CALL_LIST_SOFTENING_PCT = -10.0


def account_needs_a_call(account: AccountDecay) -> bool:
    """True when this account has actually slipped — not merely large."""
    if account.is_real_decline or account.is_cadence_cliff:
        return True
    pct = account.recent_vs_prior_pct
    return pct is not None and pct <= CALL_LIST_SOFTENING_PCT


_HOUSE_REP_PREFIX = re.compile(r"^house\b", re.I)
# bmc labels its e-commerce desk "EC HOUSE ACCOUNTS" — plural, and not at
# the start of the label, so it escaped both halves of the old rule.
_HOUSE_REP_PHRASE = re.compile(r"\bhouse accounts?\b", re.I)


def rep_label_is_house(label: Optional[str]) -> bool:
    """The house-rep auto-rule, in one place.

    A "house account" rep is the inside desk, not a person to coach. The
    exclusion belongs on the REP surfaces (leaderboard, coaching cards) and
    nowhere else — the dealers that desk services are ordinary accounts and
    still belong on the call list. See `outreach_screen.account_is_screened`.
    """
    s = (label or "").strip()
    if not s:
        return False
    return bool(_HOUSE_REP_PREFIX.search(s) or _HOUSE_REP_PHRASE.search(s))


def account_is_identified(account: AccountDecay) -> bool:
    """True when this row names an account a rep could actually dial.

    S1 groups by `customer_bill_to_number`, so every invoice whose bill-to is
    blank collapses into ONE pseudo-account. On ali that bucket was $614K of
    unattributed invoices, and it led the call list as "(unnamed) - rep 75 -
    81 days silent": the top instruction of the week was to phone nobody.
    It is not one account, so it is not one call, and averaging its slope
    means nothing. It stays in `decay` (the dollars are real and feed the
    totals) and is kept off the surfaces that name a thing to do.
    """
    return bool((account.bill_to_number or "").strip() or (account.bill_to_name or "").strip())


def account_is_callable(account: AccountDecay) -> bool:
    """Has slipped AND can be dialed — the gate for every "call this" surface."""
    return account_is_identified(account) and account_needs_a_call(account)


def outreach_sort_key(account: AccountDecay) -> float:
    """Sort key for the outreach list (report operator §5a.3).

    Ordering: actionability × dollars-at-risk.
    A 30-days-silent decline outranks a 5-days-silent cadence-cliff
    at the same LTM.
    """
    if account.is_real_decline and account.days_silent > 30:
        actionability = 1.0
    elif account.is_real_decline:
        actionability = 0.9
    elif account.is_cadence_cliff:
        actionability = 0.6
    else:
        actionability = 0.3
    return actionability * max(account.ltm_rev, 1.0)


@dataclass
class RepRow:
    rep_number: str
    rep_label: Optional[str]
    rep_name_tier2: Optional[str]
    ltm_invoiced: float
    prior_ltm_invoiced: float
    yoy_pct: Optional[float]
    customer_count: int
    is_house: bool

    @property
    def display_label(self) -> Optional[str]:
        return display_rep_label(
            rep_name_tier2=self.rep_name_tier2,
            rep_number=self.rep_number,
            rep_label=self.rep_label,
        )


@dataclass
class RepRisk:
    rep_number: str
    rep_name_tier2: Optional[str]
    dollars_at_risk: float
    accounts_at_risk: int
    leak_dollars: Optional[float]
    leak_pct: Optional[float]

    @property
    def display_label(self) -> Optional[str]:
        return display_rep_label(
            rep_name_tier2=self.rep_name_tier2,
            rep_number=self.rep_number,
            rep_label=self.rep_name_tier2,
        )


# ─── P0-8: product descriptions are ERP spec strings, not product names ────
#
# HFG shipped this verbatim into a CEO brief:
#   9N00145405-3-14-DL105 | TYPE DL-105 | 34.5" H x 64.5" D x 92.5" L |
#   OPEN CENTER, ACRYLIC BOTTOM AND TOP DIFFUSERS
#
# The rule below is deliberately STRUCTURAL. It only removes material that is
# provably not part of the item's name — the item number repeated back, a
# purchase-order reference, a dimensional segment — and it never rewrites or
# invents a name. Case is touched only when every token in a segment is a real
# word, so ali's `FLMNT RND 5.5 inches...` and bri's `LED14DISC/7/930/J/WHRD/D`
# come through exactly as the ERP stores them: "Flmnt Rnd" would be worse than
# leaving it shouting.
#
# Verified against all 8 cohort catalogs that have a Q-PROD-TOP (sarreid, cci,
# clc, hfg, kal, ali, bmc, bri). da has no product CSVs; sca and bsc have the
# files with zero rows.

# Dimension-only segments: `34.5" H x 64.5" D x 92.5" L`, `16.3" H x 96" OD`.
_DIM_TOKENS = frozenset({"H", "W", "D", "L", "OD", "ID", "DIA", "SQ", "X"})
_DIM_QUOTE = "[\"\u2033\u201d']"
_DIM_MEASURE_RE = re.compile(r"^\d+(?:\.\d+)?" + _DIM_QUOTE + r"$")
_DIM_MEASURE_SUFFIXED_RE = re.compile(
    r"^\d+(?:\.\d+)?" + _DIM_QUOTE + r"(?:H|W|D|L|OD|ID|DIA)$", re.I
)
_DIM_PLAIN_NUM_RE = re.compile(r"^\d+(?:\.\d+)?$")

# A purchase-order reference leading the description (bmc): `PO644283 Eltham
# Wall Mirror`, `po-78500 Brookings Floor Mirror`, `PO Y0964 Hudson Server`.
# The digit lookahead is what keeps "POOL TABLE" safe.
_PO_PREFIX_RE = re.compile(r"^\s*P\.?O\.?[-#\s]*(?=[A-Za-z]?\d)[A-Za-z0-9-]*\s+", re.I)
# A long bare numeric code leading the description (bmc): `040003492 Round
# Coffee Table`. Six digits minimum so clc's `4 Light Pendant` is untouched.
_NUM_PREFIX_RE = re.compile(r"^\s*\d{6,}\s+")

# Kept as-is when a segment is title-cased: units, finish codes and electrical
# shorthand that would read as a typo in title case.
_PRODUCT_KEEP_UPPER = frozenset({
    "LED", "LT", "IN", "FT", "CM", "MM", "OD", "ID", "CRI", "CCT", "LM", "LMN",
    "W", "V", "K", "AC", "DC", "UV", "IP", "USB", "PK", "NAT", "BN", "OPL",
    "ACR", "CLR", "MBL", "WH", "BK", "US", "UL", "ETL", "ADA", "RGB",
})
_PRODUCT_SMALL_WORDS = frozenset({"and", "of", "the", "for", "at", "in", "on", "to", "by", "with"})
_WORDLIKE_RE = re.compile(r"^[A-Za-z][A-Za-z\'\-]{2,}$")

# A measurement token welded to its unit — `20W`, `1300LM`, `90CRI`, `3CCT`,
# `2700K`, `120V`, `4PK`. One of these anywhere in a description means the
# field is an electrical spec string, not a product name: ali's whole catalog
# and bri's part codes look like this. Those are left exactly as the ERP stores
# them, because "PEN LED 30W" title-cases to "Pen LED 30W" and `Pen` is an
# abbreviation for Pendant, not a word.
#
# LT and IN are deliberately NOT units here: `6LT` (light count) and `48IN`
# (inches) are how kal names a product, not how it specs one.
_SPEC_UNIT_RE = re.compile(
    r"(?<![A-Za-z])\d+(?:\.\d+)?(?:W|V|K|A|LM|LMD|LMN|NM|CRI|CCT|PK|WATT|LUMEN)\b",
    re.I,
)


def _is_dimension_segment(segment: str) -> bool:
    """True for a segment that is only measurements — the dimensional tail."""
    tokens = segment.replace("\u00d7", " x ").replace(",", " ").split()
    if not tokens:
        return False
    saw_measure = False
    for tok in tokens:
        upper = tok.upper()
        if upper in _DIM_TOKENS:
            continue
        if _DIM_MEASURE_RE.match(tok) or _DIM_MEASURE_SUFFIXED_RE.match(tok):
            saw_measure = True
            continue
        if _DIM_PLAIN_NUM_RE.match(tok):
            continue
        return False
    # Require at least one quoted measurement so a plain "5 x 3" (which could be
    # a light count or a pack size) is never silently dropped.
    return saw_measure


def _title_case_product_segment(segment: str) -> str:
    """Title-case a shouted segment, but only when every token is a real word.

    `OPEN CENTER, ACRYLIC BOTTOM AND TOP DIFFUSERS` becomes readable.
    `FLMNT RND`, `MULTI DROP PENDANT 6LT`, `LED14DISC/7/930/J/WHRD/D` do not
    qualify and come back untouched — there is no safe way to case a token
    that is not a word, and a half-cased spec string reads worse than a
    shouted one.
    """
    if not segment or not segment.isupper():
        return segment
    if _SPEC_UNIT_RE.search(segment):
        return segment
    tokens = segment.split()
    if not tokens:
        return segment
    saw_word = False
    for tok in tokens:
        bare = tok.strip(".,()/&")
        if not bare:
            continue
        if bare.upper() in _PRODUCT_KEEP_UPPER or bare.lower() in _PRODUCT_SMALL_WORDS:
            continue
        if any(ch.isdigit() for ch in bare):
            continue          # a part/size code riding along: DL-105, 6LT, 48IN
        if not _WORDLIKE_RE.match(bare) or not _VOWEL_RE.search(bare):
            return segment    # FLMNT, RND, GFR, SCN — no safe way to case these
        saw_word = True
    if not saw_word:
        return segment
    out: list[str] = []
    for i, tok in enumerate(tokens):
        bare = tok.strip(".,()/&")
        if bare.upper() in _PRODUCT_KEEP_UPPER or any(ch.isdigit() for ch in bare):
            out.append(tok)
            continue
        capped = _cap_word(tok)
        if i > 0 and capped.strip(".,()").lower() in _PRODUCT_SMALL_WORDS:
            capped = capped.lower()
        out.append(capped)
    return " ".join(out)


def normalize_product_description(description: str, item_number: str = "") -> str:
    """Render-facing product label: keep the identifying head, drop the spec tail.

    Never invents a name and never returns empty — an all-dropped description
    falls back to the raw string, and a blank one to the item number.
    """
    raw = (description or "").strip()
    if not raw:
        return (item_number or "").strip()

    segments = [s.strip() for s in raw.split("|")] if "|" in raw else [raw]
    item = (item_number or "").strip().casefold()

    kept: list[str] = []
    for seg in segments:
        if not seg:
            continue
        if item and seg.casefold() == item:
            continue          # the item number repeated back at the reader
        if _is_dimension_segment(seg):
            continue          # the dimensional tail
        kept.append(seg)
    if not kept:
        kept = [raw]

    kept = [_title_case_product_segment(_PO_PREFIX_RE.sub("", _NUM_PREFIX_RE.sub("", s), count=1)).strip()
            for s in kept]
    kept = [s for s in kept if s]
    if not kept:
        return raw

    out = " \u2014 ".join(kept)
    out = re.sub(r"\s{2,}", " ", out).strip(" \u2014-")
    return out or raw


@dataclass
class ProductRow:
    item_number: str
    description: str
    ltm_revenue: float
    units: int
    dealers: int

    @property
    def display_description(self) -> str:
        """Client-facing label. See ``normalize_product_description``."""
        return normalize_product_description(self.description, self.item_number)


_WORD_RE = re.compile(r"^[A-Za-z]{4,}$")
_VOWEL_RE = re.compile(r"[aeiouyAEIOUY]")


@dataclass
class FamilyRollup:
    family_label: str
    pattern: str
    ltm_revenue: float
    yoy_pct: Optional[float]
    dealer_count: int
    sku_count: int
    is_new: bool = False

    @property
    def display_label(self) -> str:
        """Client-facing family name. Several ERPs store collection_code ALL-CAPS
        (cci ships `BUNNY WILLIAMS`), which reads as shouting in a CEO brief.
        Derivation and grouping keep using ``family_label`` untouched — this is a
        render-time label only, same split as ``ProductRow.display_description``.
        """
        return normalize_account_name(self.family_label)

    @property
    def is_named(self) -> bool:
        """True only when family_label reads as a real product/collection name a CEO
        would recognize (e.g. "Bunny Williams", "Baker", "Winterthur") — not an internal
        code (COL410, U, O_U, RO-O_U, O-INV, O_3). Q-PROD-FAMILY groups by
        products.collection_code, which is a branded name for some orgs and an opaque key
        for others; there is no name table to join, so we never fake a name — an unnamed
        family is surfaced by its numbers, never by its code.

        A real name is either multi-word (a designer collab: "Bunny Williams") or a single
        pronounceable word ≥4 letters ("Baker"). Anything with a digit, underscore, or
        hyphen, or shorter than 4 letters, is treated as a code and suppressed."""
        label = (self.family_label or "").strip()
        if not label:
            return False
        if " " in label:  # multi-word: needs at least one real (vowel-bearing, ≥3-char) token
            return any(len(t) >= 3 and _VOWEL_RE.search(t) for t in label.split())
        return bool(_WORD_RE.fullmatch(label)) and bool(_VOWEL_RE.search(label))


@dataclass
class DealerCohort:
    active_ltm: int
    active_prior_ltm: int
    new_dealers: int
    lapsed: int
    returning: int
    returning_grew: int
    returning_declined: int
    returning_flat: int
    returning_expansion_dollars: float
    returning_contraction_dollars: float
    same_base_lift_pct: Optional[float]
    frequent_count: int
    occasional_count: int
    one_time_count: int
    frequent_rev: float
    occasional_rev: float
    one_time_rev: float
    second_year_return_rate: Optional[float]


@dataclass
class ChannelRow:
    order_origin: str
    label: str
    booked_dollars: float
    share_pct: float

    @property
    def is_unmapped(self) -> bool:
        """True when this row is the catch-all bucket (no per-org origin→channel
        map entry). We never present an unmapped bucket as if it were a channel."""
        lbl = (self.label or "").strip().lower()
        return lbl == "" or lbl.startswith("other (unmapped)") or lbl == "other"


@dataclass
class ChannelSplit:
    total_business_gmv: float
    ecat_gmv: float
    non_ecat_gmv: float
    ecat_pct: Optional[float]
    non_ecat_pct: Optional[float]
    report_decision: str

    @property
    def is_reportable(self) -> bool:
        return self.report_decision.upper().startswith("REPORT")


@dataclass
class ContribRow:
    bill_to_number: str
    bill_to_name: str
    ltm_rev: float
    prior_ltm_rev: float
    delta: float
    yoy_pct: Optional[float]


@dataclass
class ConcentrationProbe:
    top1_share: float
    top10_share: float
    hhi: float
    denominator: str


@dataclass
class CrossSellGap:
    anchor_item: str
    target_family: str
    gap_dealers: list[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.gap_dealers)


@dataclass
class NetRevenueRetention:
    prior_cohort_custs: int
    prior_base: float
    retained_plus_expansion: float
    nrr_pct: Optional[float]
    expansion_dollars: float
    contraction_dollars: float
    fully_churned_custs: int


@dataclass
class CustomerLeakage:
    customer_bill_to_number: str
    revenue_realized: float
    leakage_dollars: float
    skus_underpriced: int
    tier_or_volume_setaside: float
    house_suspect: bool


# ─── Rep behavior floor row types (Q-R1/R2/R4 — OWNED, always-on) ─────────

@dataclass
class RepActivityRow:
    """Q-R1 — org-level rep activity & cadence summary (one row)."""
    active_seats: int
    logins_30d: int
    quiet_seats: int       # 31–90 days since last login
    dark_seats: int        # 90+ days since last login
    order_authors_90d: int
    confirmed_orders_90d: int
    min_days_since_login: Optional[int]

    @property
    def any_data(self) -> bool:
        return self.active_seats > 0 or self.order_authors_90d > 0


@dataclass
class RepCoverageRow:
    """Q-R2 — org-level territory/book coverage summary (one row)."""
    total_customers: int
    touched_customers: int
    coverage_pct: Optional[float]
    untouched_customers: int

    @property
    def any_data(self) -> bool:
        return self.total_customers > 0


@dataclass
class RepQuoteDisciplineRow:
    """Q-R4 — org-level quote→submit discipline summary (one row)."""
    total_orders: int
    confirmed_orders: int
    draft_orders: int
    submit_rate_pct: Optional[float]
    top_draft_type: Optional[str]

    @property
    def any_data(self) -> bool:
        return self.total_orders > 0


# ─── Platform readiness row types (Q-08/09/10/11) ─────────────────────────
@dataclass
class DataFreshnessRow:
    entity_type: str
    last_updated: str
    days_since_update: int
    status: str  # Fresh / Monitor / Stale


@dataclass
class ImportHealthRow:
    month: str
    import_count: int


@dataclass
class FeatureEnablement:
    enable_sales_portal: bool
    enable_online_catalog: bool
    enable_online_ordering: bool
    kit_item_count: int
    contract_price_count: int
    enrollment_count: int
    smart_stack_count: int
    shared_resource_count: int
    portal_order_count: int


@dataclass
class ConfigCompletenessRow:
    entity_type: str
    last_updated: str
    days_stale: int
    related_record_count: Optional[int]


@dataclass
class GatherBundle:
    org: str
    date: str
    decay: list[AccountDecay] = field(default_factory=list)
    watchlist: list[AccountDecay] = field(default_factory=list)
    # Rep labels excluded by the org profile (§4), casefolded. The house
    # auto-rule lives in rep_label_is_house; this is the per-org list —
    # clc's own inside desk, "Capital Lighting Fixture", is one.
    screened_rep_labels: frozenset[str] = frozenset()
    outreach_list: list[AccountDecay] = field(default_factory=list)
    reps: list[RepRow] = field(default_factory=list)
    rep_risks: list[RepRisk] = field(default_factory=list)
    products: list[ProductRow] = field(default_factory=list)
    families: list[FamilyRollup] = field(default_factory=list)       # named-only (findings may name these)
    families_all: list[FamilyRollup] = field(default_factory=list)   # raw incl. coded collections (audit trace)
    dealers: Optional[DealerCohort] = None
    channels: list[ChannelRow] = field(default_factory=list)
    channel_split: Optional[ChannelSplit] = None
    lifters: list[ContribRow] = field(default_factory=list)
    decliners: list[ContribRow] = field(default_factory=list)
    conc_customer: Optional[ConcentrationProbe] = None
    conc_lift: Optional[ConcentrationProbe] = None
    cross_sell_gap: Optional[CrossSellGap] = None
    nrr: Optional[NetRevenueRetention] = None
    customer_leakage: list[CustomerLeakage] = field(default_factory=list)
    # Platform readiness (Q-08/09/10/11) — populated for all modes
    data_freshness: list[DataFreshnessRow] = field(default_factory=list)
    import_health: list[ImportHealthRow] = field(default_factory=list)
    feature_enablement: Optional[FeatureEnablement] = None
    config_completeness: list[ConfigCompletenessRow] = field(default_factory=list)
    # Rep behavior floor (Q-R1/R2/R4 — OWNED, always-on, ERP-optional)
    rep_activity: Optional[RepActivityRow] = None
    rep_coverage: Optional[RepCoverageRow] = None
    rep_quote_discipline: Optional[RepQuoteDisciplineRow] = None
    # Set by outreach_screen.apply — count of decay / coaching rows dropped
    # by the house / DTC / org-self screen before the top-7 cut.
    outreach_screened: int = 0
    outreach_reordered: bool = False
    house_cards_screened: int = 0

    @property
    def named_families(self) -> list["FamilyRollup"]:
        """Families whose collection_code reads as a real name — the only ones a
        finding may name. Orgs with opaque collection codes get an empty list, and
        the family callouts fall back to product/dealer facts instead of codes."""
        return [f for f in self.families if f.is_named]

    @property
    def channels_mapped(self) -> list["ChannelRow"]:
        """Channel rows that resolved to a real channel (drop the unmapped bucket)."""
        return [c for c in self.channels if not c.is_unmapped]

    @property
    def channel_decomposition_ok(self) -> bool:
        """True only when the per-org origin→channel map actually resolves a
        material share of booked dollars into ≥2 named channels. Otherwise the
        section is a single "Other (unmapped)" bar — suppress it rather than ship
        a fake chart (communication_guideline: never narrate machinery / fake data)."""
        mapped = self.channels_mapped
        if len(mapped) < 2:
            return False
        mapped_share = sum(c.share_pct for c in mapped)
        return mapped_share >= 50.0


# ─── Helpers ───────────────────────────────────────────────────────────────
def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _f(v) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _i(v) -> int:
    f = _f(v)
    return int(f) if f is not None else 0


def _s(v) -> str:
    return "" if v is None else str(v)


_REP_LABEL_RE = re.compile(r"^rep\s+(\S+)$", re.I)


def display_rep_label(
    *,
    rep_name_tier2: Optional[str] = None,
    rep_number: Optional[str] = None,
    rep_label: Optional[str] = None,
) -> Optional[str]:
    """One identity string for L3, leaderboard, coaching cards, and the call list.

    Priority: a real name on the row (agency or person — identity, not a
    fabricated person) → ``rep {n}`` from ``rep_number`` → the RS-01
    ``rep_label`` field Slot E already read. Never a blank ``rep  ``, never
    a positional ``rep (1)`` when a code or name exists. Returns None when
    the row has neither, so named grids can omit it.
    """
    from .outreach_screen import looks_like_code

    def _clean(value: Optional[str]) -> str:
        return (value or "").strip()

    def _is_name(value: str) -> bool:
        if not value:
            return False
        if _REP_LABEL_RE.fullmatch(value):
            return False
        if looks_like_code(value):
            return False
        return True

    def _as_rep_code(value: str) -> str:
        if _REP_LABEL_RE.fullmatch(value):
            return f"rep {value.split(None, 1)[1]}"
        if value.lower().startswith("rep "):
            return value
        return f"rep {value}"

    name = _clean(rep_name_tier2)
    if _is_name(name):
        return name
    number = _clean(rep_number)
    if number:
        return _as_rep_code(number)
    fallback = _clean(rep_label)
    if _is_name(fallback):
        return fallback
    if fallback:
        return _as_rep_code(fallback)
    return None


def _extract_rep_number(row: dict) -> str:
    """Return the bare rep identifier from whichever column carries it.

    Priority: explicit ``rep_number`` column → numeric suffix parsed from
    ``rep_label`` (e.g. "rep 101" → "101") → empty string.
    """
    explicit = _s(row.get("rep_number") or "").strip()
    if explicit:
        return explicit
    label = _s(row.get("rep_label") or "").strip()
    m = _REP_LABEL_RE.match(label)
    return m.group(1) if m else ""


def _validate_columns(query_id: str, rows: list[dict]) -> None:
    """Check that required columns (or known aliases) are present in the CSV.
    Logs warnings to stderr but never raises — degrade gracefully.
    """
    from . import config
    schema = config.QUERY_SCHEMAS.get(query_id)
    if schema is None or not rows:
        return
    actual_cols = set(rows[0].keys())
    aliases = schema.get("aliases", {})
    for col in schema["required"]:
        if col in actual_cols:
            continue
        col_aliases = aliases.get(col, [])
        if any(a in actual_cols for a in col_aliases):
            continue
        import sys
        print(f"SCHEMA WARNING: {query_id} missing required column '{col}' (no known alias found in {sorted(actual_cols)})", file=sys.stderr)


# ─── Per-query loaders ─────────────────────────────────────────────────────
def load_decay(rows: list[dict]) -> list[AccountDecay]:
    """S1 output. Maps from the actual S1 query SELECT aliases:
    subject, who_to_call, dollar_impact, days_silent, recent_6mo, prior_6mo, change_pct, severity.
    Also tolerates legacy column names (bill_to_number, ltm_rev, etc.).
    """
    _validate_columns("S1", rows)
    out: list[AccountDecay] = []
    for r in rows:
        recent = _f(r.get("recent_6mo")) or 0.0
        prior = _f(r.get("prior_6mo")) or 0.0
        pct = None
        if prior > 0:
            pct = ((recent - prior) / prior) * 100
        out.append(
            AccountDecay(
                bill_to_number=_s(r.get("subject") or r.get("bill_to_number") or r.get("customer_bill_to_number") or ""),
                bill_to_name=normalize_account_name(_s(r.get("bill_to_name") or r.get("customer_name") or "")),
                rep_number=_s(r.get("who_to_call") or r.get("rep_number") or "") or None,
                rep_label=normalize_account_name(_s(r.get("rep_name") or r.get("rep_label") or "")) or None,
                ltm_rev=_f(r.get("dollar_impact") or r.get("ltm_rev") or r.get("dollars_at_risk")) or 0.0,
                recent_6mo=recent,
                prior_6mo=prior,
                recent_vs_prior_pct=pct,
                days_silent=_i(r.get("days_silent")),
                mean_order_gap_days=_f(r.get("mean_order_gap_days")) or 0.0,
                lifetime_invoices=_i(r.get("lifetime_invoices") or r.get("n_invoices")),
                last_invoice_date=_s(r.get("last_invoice_date")),
            )
        )
    return sorted(out, key=lambda a: a.ltm_rev, reverse=True)


def load_reps(rows: list[dict]) -> list[RepRow]:
    """RS-01 output. Maps from actual RS-01 query aliases:
    rep_label, named, invoiced_net_ltm, house_net_excluded, accounts, is_house_rep_label.
    """
    _validate_columns("RS-01", rows)
    out: list[RepRow] = []
    for r in rows:
        ltm = _f(r.get("invoiced_net_ltm") or r.get("ltm_invoiced") or r.get("net_amount")) or 0.0
        prior = _f(r.get("prior_ltm_invoiced")) or 0.0
        pct = None
        if prior > 0:
            pct = ((ltm - prior) / prior) * 100
        out.append(
            RepRow(
                rep_number=_extract_rep_number(r),
                rep_label=normalize_account_name(_s(r.get("rep_label") or r.get("rep_name") or "")) or None,
                rep_name_tier2=normalize_account_name(_s(r.get("rep_label") or r.get("rep_name") or "")) or None,
                ltm_invoiced=ltm,
                prior_ltm_invoiced=prior,
                yoy_pct=pct,
                customer_count=_i(r.get("accounts") or r.get("customer_count") or r.get("n_customers")),
                is_house=str(r.get("is_house_rep_label") or r.get("is_house") or "false").lower() in ("true", "t", "1", "yes"),
            )
        )
    return sorted(out, key=lambda x: x.ltm_invoiced, reverse=True)


def load_channels(rows: list[dict]) -> list[ChannelRow]:
    """Q-CHAN-10 output. Sorted by booked_dollars desc."""
    _validate_columns("Q-CHAN-10", rows)
    out: list[ChannelRow] = []
    total = sum(_f(r.get("booked_dollars")) or 0.0 for r in rows) or 1.0
    for r in rows:
        d = _f(r.get("booked_dollars")) or 0.0
        out.append(
            ChannelRow(
                order_origin=_s(r.get("order_origin")),
                label=_s(r.get("canonical_channel") or r.get("channel") or r.get("order_origin")),
                booked_dollars=d,
                share_pct=100.0 * d / total,
            )
        )
    return sorted(out, key=lambda x: x.booked_dollars, reverse=True)


def load_channel_split(rows: list[dict]) -> Optional[ChannelSplit]:
    """Q-CHAN-05 output. One-row eCat vs non-eCat split."""
    _validate_columns("Q-CHAN-05", rows)
    if not rows:
        return None
    r = rows[0]
    return ChannelSplit(
        total_business_gmv=_f(r.get("total_business_gmv")) or 0.0,
        ecat_gmv=_f(r.get("ecat_gmv")) or 0.0,
        non_ecat_gmv=_f(r.get("non_ecat_gmv")) or 0.0,
        ecat_pct=_f(r.get("ecat_pct")),
        non_ecat_pct=_f(r.get("non_ecat_pct")),
        report_decision=_s(r.get("report_decision")),
    )


def load_rep_risks(rows: list[dict]) -> list[RepRisk]:
    """C2 output. Maps from: who_to_call, dollar_impact, leak_rate_pct, severity."""
    _validate_columns("C2", rows)
    out: list[RepRisk] = []
    for r in rows:
        out.append(
            RepRisk(
                rep_number=_s(r.get("who_to_call") or r.get("rep_number") or ""),
                rep_name_tier2=normalize_account_name(_s(r.get("rep_name") or r.get("rep_name_tier2") or "")) or None,
                dollars_at_risk=_f(r.get("dollar_impact")) or 0.0,
                accounts_at_risk=0,
                leak_dollars=_f(r.get("dollar_impact")),
                leak_pct=_f(r.get("leak_rate_pct")),
            )
        )
    return sorted(out, key=lambda x: x.dollars_at_risk, reverse=True)


def load_concentration(rows: list[dict]) -> Optional[ConcentrationProbe]:
    """Q-ECON-CONC output. Single row: customers, ltm_net, top1_pct, top5_pct, top10_pct, hhi."""
    _validate_columns("Q-ECON-CONC", rows)
    if not rows:
        return None
    r = rows[0]
    top1 = _f(r.get("top1_pct"))
    top10 = _f(r.get("top10_pct"))
    hhi = _f(r.get("hhi"))
    if top1 is None:
        return None
    return ConcentrationProbe(
        top1_share=top1,
        top10_share=top10 or 0.0,
        hhi=hhi or 0.0,
        denominator="LTM invoiced net",
    )


def load_contrib(rows: list[dict]) -> tuple[list[ContribRow], list[ContribRow]]:
    """Q-ECON-CONTRIB output. Returns (lifters, decliners) based on rank_shift."""
    _validate_columns("Q-ECON-CONTRIB", rows)
    lifters: list[ContribRow] = []
    decliners: list[ContribRow] = []
    for r in rows:
        ltm = _f(r.get("ltm_net")) or 0.0
        contrib = _f(r.get("contribution_proxy")) or 0.0
        shift = _f(r.get("rank_shift")) or 0.0
        row = ContribRow(
            bill_to_number=_s(r.get("customer_bill_to_number") or ""),
            bill_to_name=normalize_account_name(_s(r.get("name") or "")),
            ltm_rev=ltm,
            prior_ltm_rev=0.0,
            delta=contrib - ltm,
            yoy_pct=None,
        )
        if shift < 0:
            decliners.append(row)
        else:
            lifters.append(row)
    return lifters, decliners


def load_products(rows: list[dict]) -> list[ProductRow]:
    """Q-PROD-TOP output. Maps from: item_number, description, ltm_revenue, units, dealers."""
    _validate_columns("Q-PROD-TOP", rows)
    out: list[ProductRow] = []
    for r in rows:
        out.append(
            ProductRow(
                item_number=_s(r.get("item_number")),
                description=_s(r.get("description") or r.get("item_number") or ""),
                ltm_revenue=_f(r.get("ltm_revenue")) or 0.0,
                units=_i(r.get("units")),
                dealers=_i(r.get("dealers")),
            )
        )
    return sorted(out, key=lambda x: x.ltm_revenue, reverse=True)


def load_families(rows: list[dict]) -> list[FamilyRollup]:
    """Q-PROD-FAMILY output. Maps from: family_label, pattern, ltm_revenue, yoy_pct, dealer_count, sku_count, is_new."""
    _validate_columns("Q-PROD-FAMILY", rows)
    out: list[FamilyRollup] = []
    for r in rows:
        out.append(
            FamilyRollup(
                family_label=_s(r.get("family_label")),
                pattern=_s(r.get("pattern") or r.get("family_label") or ""),
                ltm_revenue=_f(r.get("ltm_revenue")) or 0.0,
                yoy_pct=_f(r.get("yoy_pct")),
                dealer_count=_i(r.get("dealer_count")),
                sku_count=_i(r.get("sku_count")),
                is_new=str(r.get("is_new") or "false").lower() in ("true", "t", "1", "yes"),
            )
        )
    return sorted(out, key=lambda x: x.ltm_revenue, reverse=True)


def load_dealer_cohort(rows: list[dict]) -> Optional[DealerCohort]:
    """Q-DEALER-COHORT output. Single-row summary of cohort flow and cadence."""
    _validate_columns("Q-DEALER-COHORT", rows)
    if not rows:
        return None
    r = rows[0]
    return DealerCohort(
        active_ltm=_i(r.get("active_ltm")),
        active_prior_ltm=_i(r.get("active_prior_ltm")),
        new_dealers=_i(r.get("new_dealers")),
        lapsed=_i(r.get("lapsed")),
        returning=_i(r.get("returning")),
        returning_grew=_i(r.get("returning_grew")),
        returning_declined=_i(r.get("returning_declined")),
        returning_flat=_i(r.get("returning_flat")),
        returning_expansion_dollars=_f(r.get("returning_expansion_dollars")) or 0.0,
        returning_contraction_dollars=_f(r.get("returning_contraction_dollars")) or 0.0,
        same_base_lift_pct=_f(r.get("same_base_lift_pct")),
        frequent_count=_i(r.get("frequent_count")),
        occasional_count=_i(r.get("occasional_count")),
        one_time_count=_i(r.get("one_time_count")),
        frequent_rev=_f(r.get("frequent_rev")) or 0.0,
        occasional_rev=_f(r.get("occasional_rev")) or 0.0,
        one_time_rev=_f(r.get("one_time_rev")) or 0.0,
        second_year_return_rate=_f(r.get("second_year_return_rate")),
    )


def load_cross_sell_gap(rows: list[dict]) -> Optional[CrossSellGap]:
    """Q-CROSS-SELL output. Rows: dealer_code, anchor_item, target_family.
    Returns None only if the query was never cached (missing CSV); an empty
    row set means the gap is zero (all anchor dealers already buy the target).
    """
    if rows is None:
        return None
    anchor = _s(rows[0].get("anchor_item")) if rows else ""
    family = _s(rows[0].get("target_family")) if rows else ""
    dealers = [_s(r.get("dealer_code")) for r in rows if _s(r.get("dealer_code"))]
    return CrossSellGap(anchor_item=anchor, target_family=family, gap_dealers=dealers)


def load_nrr(rows: list[dict]) -> Optional[NetRevenueRetention]:
    """Q-ECON-NRR output. Single-row same-base dollar retention."""
    _validate_columns("Q-ECON-NRR", rows)
    if not rows:
        return None
    r = rows[0]
    return NetRevenueRetention(
        prior_cohort_custs=_i(r.get("prior_cohort_custs")),
        prior_base=_f(r.get("prior_base")) or 0.0,
        retained_plus_expansion=_f(r.get("retained_plus_expansion")) or 0.0,
        nrr_pct=_f(r.get("nrr_pct")),
        expansion_dollars=_f(r.get("expansion_dollars")) or 0.0,
        contraction_dollars=_f(r.get("contraction_dollars")) or 0.0,
        fully_churned_custs=_i(r.get("fully_churned_custs")),
    )


def load_customer_leakage(rows: list[dict]) -> list[CustomerLeakage]:
    """Q-ECON-LEAK output. Customer-grain discretionary pricing leakage."""
    _validate_columns("Q-ECON-LEAK", rows)
    out: list[CustomerLeakage] = []
    for r in rows:
        out.append(
            CustomerLeakage(
                customer_bill_to_number=_s(r.get("customer_bill_to_number") or r.get("cust")),
                revenue_realized=_f(r.get("revenue_realized")) or 0.0,
                leakage_dollars=_f(r.get("leakage_dollars")) or 0.0,
                skus_underpriced=_i(r.get("skus_underpriced")),
                tier_or_volume_setaside=_f(r.get("tier_or_volume_setaside")) or 0.0,
                house_suspect=str(r.get("house_suspect") or "false").lower() in ("true", "t", "1", "yes"),
            )
        )
    return sorted(out, key=lambda x: (x.house_suspect, -x.leakage_dollars))


# ─── Platform readiness loaders (Q-08/09/10/11) ───────────────────────────
def load_data_freshness(rows: list[dict]) -> list[DataFreshnessRow]:
    """Q-08 output. Per-entity data freshness from data_versions."""
    return [
        DataFreshnessRow(
            entity_type=_s(r.get("entity_type")),
            last_updated=_s(r.get("last_updated")),
            days_since_update=_i(r.get("days_since_update")),
            status=_s(r.get("status")),
        )
        for r in rows
    ]


def load_import_health(rows: list[dict]) -> list[ImportHealthRow]:
    """Q-09 output. Monthly import counts over the last 6 months."""
    return [
        ImportHealthRow(
            month=_s(r.get("month")),
            import_count=_i(r.get("import_count")),
        )
        for r in rows
    ]


def load_feature_enablement(rows: list[dict]) -> Optional[FeatureEnablement]:
    """Q-10 output. Single row: feature flags and counts."""
    if not rows:
        return None
    r = rows[0]
    return FeatureEnablement(
        enable_sales_portal=str(r.get("enable_sales_portal", "false")).lower() in ("true", "t", "1"),
        enable_online_catalog=str(r.get("enable_online_catalog", "false")).lower() in ("true", "t", "1"),
        enable_online_ordering=str(r.get("enable_online_ordering", "false")).lower() in ("true", "t", "1"),
        kit_item_count=_i(r.get("kit_item_count")),
        contract_price_count=_i(r.get("contract_price_count")),
        enrollment_count=_i(r.get("enrollment_count")),
        smart_stack_count=_i(r.get("smart_stack_count")),
        shared_resource_count=_i(r.get("shared_resource_count")),
        portal_order_count=_i(r.get("portal_order_count")),
    )


def load_config_completeness(rows: list[dict]) -> list[ConfigCompletenessRow]:
    """Q-11 output. Entities >30 days stale with optional record counts."""
    return [
        ConfigCompletenessRow(
            entity_type=_s(r.get("entity_type")),
            last_updated=_s(r.get("last_updated")),
            days_stale=_i(r.get("days_stale")),
            related_record_count=_i(r.get("related_record_count")) if r.get("related_record_count") not in (None, "") else None,
        )
        for r in rows
    ]


# ─── Rep behavior floor loaders (Q-R1/R2/R4 — OWNED, always-on) ───────────

def load_rep_activity(rows: list[dict]) -> Optional[RepActivityRow]:
    """Q-R1 output. Single org-level row: active_seats, logins_30d, quiet_seats,
    dark_seats, order_authors_90d, confirmed_orders_90d, min_days_since_login."""
    if not rows:
        return None
    r = rows[0]
    seats = _i(r.get("active_seats"))
    authors = _i(r.get("order_authors_90d"))
    if seats == 0 and authors == 0:
        return None
    return RepActivityRow(
        active_seats=seats,
        logins_30d=_i(r.get("logins_30d")),
        quiet_seats=_i(r.get("quiet_seats")),
        dark_seats=_i(r.get("dark_seats")),
        order_authors_90d=authors,
        confirmed_orders_90d=_i(r.get("confirmed_orders_90d")),
        min_days_since_login=_i(r.get("min_days_since_login")) if r.get("min_days_since_login") not in (None, "") else None,
    )


def load_rep_coverage(rows: list[dict]) -> Optional[RepCoverageRow]:
    """Q-R2 output. Single org-level row: total_customers, touched_customers,
    coverage_pct, untouched_customers."""
    if not rows:
        return None
    r = rows[0]
    total = _i(r.get("total_customers"))
    if total == 0:
        return None
    return RepCoverageRow(
        total_customers=total,
        touched_customers=_i(r.get("touched_customers")),
        coverage_pct=_f(r.get("coverage_pct")),
        untouched_customers=_i(r.get("untouched_customers")),
    )


def load_rep_quote_discipline(rows: list[dict]) -> Optional[RepQuoteDisciplineRow]:
    """Q-R4 output. Single org-level row: total_orders, confirmed_orders,
    draft_orders, submit_rate_pct, top_draft_type."""
    if not rows:
        return None
    r = rows[0]
    total = _i(r.get("total_orders"))
    if total == 0:
        return None
    return RepQuoteDisciplineRow(
        total_orders=total,
        confirmed_orders=_i(r.get("confirmed_orders")),
        draft_orders=_i(r.get("draft_orders")),
        submit_rate_pct=_f(r.get("submit_rate_pct")),
        top_draft_type=_s(r.get("top_draft_type")) or None,
    )


# ─── Description-derived family fallback ───────────────────────────────────

_FAMILY_TOKEN_RE = re.compile(r"^[A-Z][a-z]{3,}$")


def derive_description_families(
    products: list[ProductRow],
    min_members: int = 3,
    min_aggregate_ltm: float = 50_000.0,
) -> list[FamilyRollup]:
    """When collection_code families are all unnamed (opaque), attempt to group
    products by a shared proper-noun token in their description. E.g. 'Giselle
    Jupe Dining Table Lg Lt Mink' + 'Austin Jupe Dining Table Large Walnut' ->
    family 'Jupe'. NLP-free heuristic: tokenize by space, extract capitalized
    words 4+ chars that appear in 3+ product descriptions, group by most-specific
    shared token (not the first word, which is often a generic prefix)."""
    from collections import Counter, defaultdict

    token_products: dict[str, list[ProductRow]] = defaultdict(list)
    for p in products:
        seen_tokens: set[str] = set()
        for token in p.description.split():
            clean = token.strip("()-,.'\"")
            if _FAMILY_TOKEN_RE.match(clean) and clean not in seen_tokens:
                seen_tokens.add(clean)
                token_products[clean].append(p)

    token_counts = Counter({t: len(ps) for t, ps in token_products.items()})
    too_common = {t for t, c in token_counts.items() if c > len(products) * 0.5}

    families: list[FamilyRollup] = []
    used_products: set[str] = set()

    for token, count in token_counts.most_common():
        if count < min_members:
            break
        if token in too_common:
            continue
        members = [p for p in token_products[token] if p.item_number not in used_products]
        if len(members) < min_members:
            continue
        aggregate_ltm = sum(m.ltm_revenue for m in members)
        if aggregate_ltm < min_aggregate_ltm:
            continue
        aggregate_dealers = max(m.dealers for m in members) if members else 0
        for m in members:
            used_products.add(m.item_number)
        families.append(FamilyRollup(
            family_label=token,
            pattern="description-derived",
            ltm_revenue=aggregate_ltm,
            yoy_pct=None,
            dealer_count=aggregate_dealers,
            sku_count=len(members),
            is_new=False,
        ))

    return sorted(families, key=lambda f: f.ltm_revenue, reverse=True)


# ─── Orchestration ─────────────────────────────────────────────────────────
def gather_all(org: str, date: str) -> GatherBundle:
    paths = CachePaths.for_run(org, date)
    bundle = GatherBundle(org=org, date=date)

    bundle.decay = load_decay(_read_csv(paths.csv_for("S1")))
    bundle.reps = load_reps(_read_csv(paths.csv_for("RS-01")))
    bundle.channels = load_channels(_read_csv(paths.csv_for("Q-CHAN-10")))
    bundle.channel_split = load_channel_split(_read_csv(paths.csv_for("Q-CHAN-05")))
    bundle.rep_risks = load_rep_risks(_read_csv(paths.csv_for("C2")))
    bundle.conc_customer = load_concentration(_read_csv(paths.csv_for("Q-ECON-CONC")))
    bundle.nrr = load_nrr(_read_csv(paths.csv_for("Q-ECON-NRR")))
    bundle.customer_leakage = load_customer_leakage(_read_csv(paths.csv_for("Q-ECON-LEAK")))
    bundle.lifters, bundle.decliners = load_contrib(_read_csv(paths.csv_for("Q-ECON-CONTRIB")))
    bundle.products = load_products(_read_csv(paths.csv_for("Q-PROD-TOP")))
    # Families a finding may NAME must have a real collection name; opaque codes
    # (COL410, U, O_U) are kept in families_all for the audit trace but never
    # surfaced as "the X family" prose. See FamilyRollup.is_named.
    bundle.families_all = load_families(_read_csv(paths.csv_for("Q-PROD-FAMILY")))
    bundle.families = [f for f in bundle.families_all if f.is_named]
    if not bundle.families and bundle.products:
        bundle.families = derive_description_families(bundle.products)
    bundle.dealers = load_dealer_cohort(_read_csv(paths.csv_for("Q-DEALER-COHORT")))

    # House / DTC / org-self screen BEFORE the top-7 cut. The auto-rule and
    # per-org EXCLUDE table lived on rep-grain SQL; the decay extract that
    # feeds the call list never applied them (cci HOUSE ACCOUNT, hfg DTC).
    from . import outreach_screen as _outreach_screen

    _outreach_screen.apply(bundle)

    # Populate accounts_at_risk from the screened decay (C2 CSV lacks this column)
    for risk in bundle.rep_risks:
        risk.accounts_at_risk = sum(
            1 for a in bundle.decay if a.rep_number == risk.rep_number
        )

    cs_path = paths.csv_for("Q-CROSS-SELL")
    if cs_path.exists():
        bundle.cross_sell_gap = load_cross_sell_gap(_read_csv(cs_path))
    else:
        bundle.cross_sell_gap = None

    # Platform readiness (Q-08/09/10/11) — loaded for all modes
    bundle.data_freshness = load_data_freshness(_read_csv(paths.csv_for("Q-08")))
    bundle.import_health = load_import_health(_read_csv(paths.csv_for("Q-09")))
    bundle.feature_enablement = load_feature_enablement(_read_csv(paths.csv_for("Q-10")))
    bundle.config_completeness = load_config_completeness(_read_csv(paths.csv_for("Q-11")))

    # Rep behavior floor (Q-R1/R2/R4 — OWNED, always-on, ERP-optional)
    bundle.rep_activity = load_rep_activity(_read_csv(paths.csv_for("Q-R1")))
    bundle.rep_coverage = load_rep_coverage(_read_csv(paths.csv_for("Q-R2")))
    bundle.rep_quote_discipline = load_rep_quote_discipline(_read_csv(paths.csv_for("Q-R4")))

    return bundle
