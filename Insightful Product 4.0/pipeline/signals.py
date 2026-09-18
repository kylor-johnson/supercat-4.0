"""Signal detection: gather output → fired Signals with SIGNAL_RANK.

Single responsibility: turning data into ranked observations. Each rule
is a small function that returns Optional[Signal]. Rules are
deterministic — no LLM, no prose, no editorial decisions.

SIGNAL_RANK formula (operators/report_operator.md Step 4):
    SIGNAL_RANK = surprise × dollar_impact × actionability

  surprise:       0.0 - 1.0    (1.0 = "CEO would not have known")
  dollar_impact:  $  raw       (normalized at consumption time)
  actionability:  0.0 - 1.0    (1.0 = "specific named call this week")

A signal's confidence ceiling = LEAST(its ceiling, COMMERCE_CONFIDENCE).
A pattern explained by knowledge/industry_context.md is context, not a
signal (down-weight in rank, do not skip detection).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, TypedDict

from .gather import (
    AccountDecay,
    ChannelRow,
    ConcentrationProbe,
    ContribRow,
    DealerCohort,
    FamilyRollup,
    GatherBundle,
    ProductRow,
    RepRisk,
    RepRow,
)
from .preflight import Confidence, RunPosture


class DeclineContext(TypedDict, total=False):
    account: str
    rep: str
    pace: float


class CadenceContext(TypedDict, total=False):
    account: str
    days_silent: int


class ConcentrationContext(TypedDict, total=False):
    top1_pct: float
    hhi: float


class RepContext(TypedDict, total=False):
    rep: str
    yoy: float


class CrossSellContext(TypedDict, total=False):
    anchor: str
    target: str


class RetentionContext(TypedDict, total=False):
    return_rate: float


class ChannelContext(TypedDict, total=False):
    channel: str
    pct: float


class LeakContext(TypedDict, total=False):
    leak_pct: float
    total_leak_dollars: float


class ProjectContext(TypedDict, total=False):
    prefix: str
    sku_count: int
    dollars: float
    share_pct: float
    units: int
    unit_price: float
    unit_price_ratio: float
    items: list


class EcatContext(TypedDict, total=False):
    ecat_pct: float
    inv_ltm_net: float


SignalKind = Literal[
    "real_decline",          # account: pace < 0.6x prior on >$50K
    "cadence_cliff",         # account: silence > 2x mean gap, but growing
    "growth_pocket",         # product family: high YoY on broad dealer base
    "new_line_takeoff",      # product family: $X cleared on Y dealers in year 1
    "lift_concentration",    # top-N accounts hold a disproportionate share of $-lift
    "rep_overperform",       # rep: top YoY % growth
    "rep_underperform",      # rep: top YoY % decline
    "rep_atrisk_book",       # rep: largest $-at-risk
    "cross_sell_pocket",     # dealers buying X but not Y (where Y is growing)
    "second_year_gap",       # large lapsed first-timer cohort
    "channel_concentration", # one channel >X% of total
    "ecat_minority",         # eCat is <15% of invoiced LTM (suppresses share framing)
    "leakage_discipline",    # org-wide leakage well below industry-normal
    "territory_cluster_decay",  # 3+ accounts under one rep all in real_decline
    "single_door_project",   # a custom project: few units, one door, material share of the year
]


Section = Literal["hero", "thisweek", "thismonth", "layers", "team", "watchlist", "products", "dealers", "channels"]

# Narrative-arc ordering for signal_summary_set() (report_operator.md Step 7)
SIGNAL_ARC_ORDER: dict[str, int] = {
    "growth_pocket": 0,        # momentum
    "new_line_takeoff": 0,     # momentum
    "rep_overperform": 0,      # momentum
    "leakage_discipline": 1,   # intelligence
    "lift_concentration": 1,   # intelligence
    "channel_concentration": 1,  # intelligence
    "ecat_minority": 1,        # intelligence
    "cross_sell_pocket": 2,    # opportunity
    "second_year_gap": 2,      # opportunity
    "real_decline": 3,         # risk
    "cadence_cliff": 3,        # risk
    "rep_underperform": 3,     # risk
    "rep_atrisk_book": 3,      # risk
    "territory_cluster_decay": 3,  # risk
    "single_door_project": 1,  # intelligence — it explains the catalog, it is not a call
}


@dataclass
class Signal:
    kind: SignalKind
    section: Section
    headline: str             # short label, not prose
    surprise: float           # 0.0-1.0
    dollar_impact: float      # $ raw
    actionability: float      # 0.0-1.0
    confidence_ceiling: Confidence
    context: dict = field(default_factory=dict)  # query result rows the signal points at
    is_positive: bool = True  # for tone-balance in Signal Summary

    @property
    def rank(self) -> float:
        return self.surprise * max(self.dollar_impact, 1.0) * self.actionability


# ─── Thresholds ───────────────────────────────────────────────────────────
#
# Phase 5 (W3) classified every gate in this module into TWO kinds. The
# distinction is the whole point of the phase, so it is recorded in the code,
# not only in the audit:
#
#   SIZE-NEUTRAL — a ratio, a multiplier, or a percentage. A $3M client and a
#     $70M client mean the same thing by "recent is 60% of prior". These may
#     still be mis-tuned, but they are NOT overfit to Sarreid's size, and they
#     stay plain module constants below.
#
#   SIZE-DEPENDENT — an absolute dollar floor or a raw count. $50,000 is 0.07%
#     of cci's year and 0.72% of bmc's: a 10x spread in what counts as
#     "material". Ten dealers is 0.13% of cci's active base and 1.75% of kal's.
#     These are expressed as max(absolute floor, share of the org's own size)
#     through ThresholdProfile, below.
#
# ── SIZE-NEUTRAL: ratios. Leave them alone; they do not encode Sarreid's size.
DECLINE_PACE_THRESHOLD = 0.6        # recent < 60% of prior = real decline
CADENCE_CLIFF_GAP_MULTIPLIER = 2.0  # silence > 2× mean gap
GROWTH_POCKET_MIN_YOY_PCT = 20.0    # family must grow >20% YoY
LIFT_CONC_TOP5_THRESHOLD = 60.0     # top-5 lifters hold >60% of lift = concentrated
REP_OVERPERFORM_MIN_YOY = 30.0      # ≥30% YoY growth
REP_UNDERPERFORM_MAX_YOY = -20.0    # ≤-20% YoY decline
CHANNEL_CONC_THRESHOLD = 70.0       # one channel >70% of total
ECAT_MINORITY_THRESHOLD = 15.0      # eCat <15% of invoiced LTM
LEAKAGE_LOW_THRESHOLD = 3.0         # org-wide leak rate <3% = disciplined
SECOND_YEAR_RETURN_THRESHOLD = 0.50 # <50% of first-timers come back
PRICING_PLAY_MIN_LEAK_SPREAD_PCT = 10.0  # top rep leak rate must clear 10%
CROSS_SELL_ADDRESSABLE_FRACTION = 0.30  # editorial estimate of addressable cross-sell potential

# ── SIZE-DEPENDENT: kept as module names so the OLD absolute value stays
# readable and greppable, but nothing reads them directly any more — they are
# the `floor` half of the BASELINE profile below. Changing one here changes
# only the floor, never the size-relative half.
DECLINE_MIN_LTM_DOLLARS = 50_000    # account LTM floor for a real-decline signal
REP_ATRISK_MIN_DOLLARS = 20_000     # $ at risk on one rep's book
NEW_LINE_MIN_REVENUE = 100_000      # a new family's year-1 invoiced
NEW_LINE_MIN_DEALERS = 5            # ...on at least this many dealers
GROWTH_POCKET_MIN_DEALERS = 10      # a growing family must span this many dealers
REP_BOOK_MIN_DOLLARS = 100_000      # rep book floor for over/under-perform
SECOND_YEAR_MIN_LAPSED_DOLLARS = 50_000  # $ left behind by non-returning first-timers
CROSS_SELL_MIN_TARGET_DEALERS = 5   # target family must already span this many dealers
CROSS_SELL_HERO_MIN_DEALERS = 3     # a gap this small is not a hero finding
PLAY_MIN_UPSIDE_DOLLARS = 0         # "Do this month" materiality — none today (S1)
COACHING_CARD_MIN_DOLLARS = 0       # coaching-card materiality — none today (S2)

# ─── Size-relative threshold machinery (Phase 5 / W3) ─────────────────────
#
# Every size-dependent gate takes the form
#
#     threshold = max(ABSOLUTE_FLOOR, PCT_OF_BASE × <the org's own size>)
#
# The floor keeps a tiny org from firing on noise; the percentage keeps a large
# org from drowning in it. Two size BASES are used, because two kinds of gate
# are overfit in two different ways:
#
#   inv_ltm_net      — dollar floors ("material account", "$ at risk")
#   active_dealers   — raw counts ("across 10 dealers", "5 dealers in year 1")
#
# `pct = 0.0` means the mechanism is present but dormant: the floor alone
# decides, which is exactly 4.0's behaviour today. That is what BASELINE ships,
# per the W3 brief's hard constraint — W3 proposes, the OWNER picks the
# numbers. RECOMMENDED carries W3's proposal; the calibration sweep behind it
# is in handoffs/exec/W3_evidence.md. Flipping ACTIVE_PROFILE is a deliberate
# act that moves the cohort and needs a golden re-stamp.


@dataclass(frozen=True)
class SizeScaledFloor:
    """One gate as ``max(floor, pct × base)``.

    ``pct`` is a fraction (0.002 = 0.2%). A missing, zero, negative or
    non-finite base degrades to the absolute floor — a `commerce_confidence =
    NONE` org has `inv_ltm_net == 0` and must not divide, blow up, or silently
    lose its floor.
    """

    floor: float
    pct: float = 0.0

    def resolve(self, base: float | int | None) -> float:
        if base is None:
            return float(self.floor)
        base = float(base)
        if base <= 0.0 or base != base or base in (float("inf"), float("-inf")):
            return float(self.floor)
        return max(float(self.floor), self.pct * base)


@dataclass(frozen=True)
class Thresholds:
    """Size-dependent gates resolved against ONE org. Plain numbers from here on."""

    decline_min_ltm: float
    rep_atrisk_min: float
    new_line_min_revenue: float
    rep_book_min: float
    second_year_min_lapsed: float
    play_min_upside: float
    coaching_card_min_dollars: float
    growth_pocket_min_dealers: int
    new_line_min_dealers: int
    cross_sell_min_target_dealers: int
    cross_sell_hero_min_dealers: int
    # S2 — the coaching cards are the FIFTH surface of gather.account_needs_a_call.
    coaching_cards_require_needs_a_call: bool
    # S3 — which same-dealer measure the hero leads with, and where it turns.
    hero_same_base_measure: str      # "lift" | "nrr"
    hero_lift_spending_less_pct: float
    hero_nrr_spending_less_pct: float


@dataclass(frozen=True)
class ThresholdProfile:
    """A named set of (floor, pct) pairs. Resolve it against an org to get Thresholds."""

    name: str
    decline_min_ltm: SizeScaledFloor
    rep_atrisk_min: SizeScaledFloor
    new_line_min_revenue: SizeScaledFloor
    rep_book_min: SizeScaledFloor
    second_year_min_lapsed: SizeScaledFloor
    play_min_upside: SizeScaledFloor
    coaching_card_min_dollars: SizeScaledFloor
    growth_pocket_min_dealers: SizeScaledFloor
    new_line_min_dealers: SizeScaledFloor
    cross_sell_min_target_dealers: SizeScaledFloor
    cross_sell_hero_min_dealers: SizeScaledFloor
    coaching_cards_require_needs_a_call: bool
    hero_same_base_measure: str
    hero_lift_spending_less_pct: float
    hero_nrr_spending_less_pct: float

    def resolve(self, inv_ltm_net: float, active_dealers: float | int = 0) -> Thresholds:
        return Thresholds(
            decline_min_ltm=self.decline_min_ltm.resolve(inv_ltm_net),
            rep_atrisk_min=self.rep_atrisk_min.resolve(inv_ltm_net),
            new_line_min_revenue=self.new_line_min_revenue.resolve(inv_ltm_net),
            rep_book_min=self.rep_book_min.resolve(inv_ltm_net),
            second_year_min_lapsed=self.second_year_min_lapsed.resolve(inv_ltm_net),
            play_min_upside=self.play_min_upside.resolve(inv_ltm_net),
            coaching_card_min_dollars=self.coaching_card_min_dollars.resolve(inv_ltm_net),
            growth_pocket_min_dealers=int(
                round(self.growth_pocket_min_dealers.resolve(active_dealers))
            ),
            new_line_min_dealers=int(
                round(self.new_line_min_dealers.resolve(active_dealers))
            ),
            cross_sell_min_target_dealers=int(
                round(self.cross_sell_min_target_dealers.resolve(active_dealers))
            ),
            cross_sell_hero_min_dealers=int(
                round(self.cross_sell_hero_min_dealers.resolve(active_dealers))
            ),
            coaching_cards_require_needs_a_call=self.coaching_cards_require_needs_a_call,
            hero_same_base_measure=self.hero_same_base_measure,
            hero_lift_spending_less_pct=self.hero_lift_spending_less_pct,
            hero_nrr_spending_less_pct=self.hero_nrr_spending_less_pct,
        )


# 4.0 exactly as it ships today: every pct dormant, every floor the Sarreid-era
# absolute. `make check` is green against this and only this.
BASELINE_PROFILE = ThresholdProfile(
    name="baseline",
    decline_min_ltm=SizeScaledFloor(DECLINE_MIN_LTM_DOLLARS, 0.0),
    rep_atrisk_min=SizeScaledFloor(REP_ATRISK_MIN_DOLLARS, 0.0),
    new_line_min_revenue=SizeScaledFloor(NEW_LINE_MIN_REVENUE, 0.0),
    rep_book_min=SizeScaledFloor(REP_BOOK_MIN_DOLLARS, 0.0),
    second_year_min_lapsed=SizeScaledFloor(SECOND_YEAR_MIN_LAPSED_DOLLARS, 0.0),
    play_min_upside=SizeScaledFloor(PLAY_MIN_UPSIDE_DOLLARS, 0.0),
    coaching_card_min_dollars=SizeScaledFloor(COACHING_CARD_MIN_DOLLARS, 0.0),
    growth_pocket_min_dealers=SizeScaledFloor(GROWTH_POCKET_MIN_DEALERS, 0.0),
    new_line_min_dealers=SizeScaledFloor(NEW_LINE_MIN_DEALERS, 0.0),
    cross_sell_min_target_dealers=SizeScaledFloor(CROSS_SELL_MIN_TARGET_DEALERS, 0.0),
    cross_sell_hero_min_dealers=SizeScaledFloor(CROSS_SELL_HERO_MIN_DEALERS, 0.0),
    coaching_cards_require_needs_a_call=False,
    hero_same_base_measure="lift",
    hero_lift_spending_less_pct=-5.0,
    hero_nrr_spending_less_pct=97.0,
)

# W3's PROPOSAL. NOT ACTIVE. Every number is the candidate the 11-org × 4-value
# sweep in handoffs/exec/W3_evidence.md §Calibration selected, with the
# one-line rationale beside it. Where the cohort did not discriminate between
# candidates, the evidence file says so rather than implying it did.
RECOMMENDED_PROFILE = ThresholdProfile(
    name="recommended",
    # sweep B: small orgs gain coverage (sarreid 5→9, kal 5→6, ali 3→4), large
    # orgs unchanged (cci 2, clc 1, hfg 4). The 10× spread closes.
    decline_min_ltm=SizeScaledFloor(25_000, 0.0010),          # 0.10% of invoiced LTM
    # sweep A. 0.10% is too hard: it zeroes cci AND hfg, deleting a real $66K book.
    rep_atrisk_min=SizeScaledFloor(10_000, 0.0005),           # 0.05% of invoiced LTM
    # sweep A — S2. hfg 5→1 (the four `$1K at risk` cards go), cci 3→1, kal 4→1,
    # ali 3→1; sarreid/clc/bri/bmc keep every card. 0.10% deletes cci, clc and
    # hfg's card block outright, which is over-correction, not materiality.
    coaching_card_min_dollars=SizeScaledFloor(5_000, 0.0002), # 0.02% of invoiced LTM
    # sweep A — S1. hfg 1→0 ("no play qualified this month"), clc 1→0, ali 1→0;
    # sarreid 3→2, cci/kal/bri/bmc unchanged.
    play_min_upside=SizeScaledFloor(10_000, 0.0010),          # 0.10% of invoiced LTM
    # sweep A. The cohort does not discriminate — only ali has new families, and
    # all 13 clear every candidate. Size-relative on principle, not on evidence.
    new_line_min_revenue=SizeScaledFloor(50_000, 0.0025),     # 0.25% of invoiced LTM
    rep_book_min=SizeScaledFloor(50_000, 0.0025),             # 0.25% of invoiced LTM
    second_year_min_lapsed=SizeScaledFloor(25_000, 0.0025),   # 0.25% of invoiced LTM
    # Counts scale on the ACTIVE-DEALER base, not on dollars. No cohort org
    # changes at any candidate; these keep a 200-dealer client reachable.
    growth_pocket_min_dealers=SizeScaledFloor(5, 0.005),      # 0.5% of active dealers
    new_line_min_dealers=SizeScaledFloor(5, 0.0025),
    cross_sell_min_target_dealers=SizeScaledFloor(5, 0.0025),
    # S1: replaces the hero-only stopgap of 3. 0.50% starts suppressing bri's
    # legitimate 10-door gap; 0.25% suppresses only what 3 already suppressed.
    cross_sell_hero_min_dealers=SizeScaledFloor(3, 0.0025),
    # S2 consistency: one definition of "this account has slipped", five surfaces.
    coaching_cards_require_needs_a_call=True,
    # S3: the two measures disagree on 3 of 8 commerce orgs (cci, hfg, kal) and
    # the lift measure is the gentler one every time. NRR is what §5 already
    # reports, so leading on it removes the contradiction rather than papering
    # over it.
    hero_same_base_measure="nrr",
    hero_lift_spending_less_pct=-5.0,
    hero_nrr_spending_less_pct=97.0,
)

# ← OWNER: this is the one line Phase 5 hands over. Flipping it to
#   RECOMMENDED_PROFILE moves the cohort deliberately and requires a golden
#   re-stamp (EXECUTION_PLAN.md §stamp protocol).
ACTIVE_PROFILE = RECOMMENDED_PROFILE


def org_size_base(posture: RunPosture, gather: Optional[GatherBundle] = None) -> tuple[float, int]:
    """(invoiced-LTM base, active-dealer base) for threshold resolution.

    Both degrade to 0 rather than raising, so a NONE-confidence org resolves to
    the absolute floors instead of dividing by an absent topline.
    """
    inv = float(getattr(posture, "inv_ltm_net", 0.0) or 0.0)
    dealers = 0
    cohort = getattr(gather, "dealers", None) if gather is not None else None
    if cohort is not None:
        dealers = int(getattr(cohort, "active_ltm", 0) or 0)
    return (inv if inv > 0 else 0.0), max(dealers, 0)


def resolve_thresholds(
    posture: RunPosture,
    gather: Optional[GatherBundle] = None,
    profile: Optional[ThresholdProfile] = None,
) -> Thresholds:
    """The ONE place an org's size-dependent gates are computed."""
    inv, dealers = org_size_base(posture, gather)
    return (profile or ACTIVE_PROFILE).resolve(inv, dealers)


# Used only by detectors called without an explicit `thresholds=` (unit tests,
# and any caller predating W3). Identical to today's absolute constants.
DEFAULT_THRESHOLDS = BASELINE_PROFILE.resolve(0.0, 0)


# ─── S2: the coaching cards are the FIFTH surface of ONE definition ───────
#
# Phase 4 established `gather.account_needs_a_call(account)` as the single
# definition of "this account has actually slipped". The call list, the
# watchlist, the hero at-risk card and the call-list footer all read it. The
# coaching cards did not, and it shows:
#
#   hfg card 1 — "Rep CANOREP's flagged book is about $22K of near-term risk,
#   and it sits on a $602K account that is actually pacing up (+$19K H/H)."
#
# A RISK card about a GROWING account. Two separate defects produce it:
#
#   1. `RepRisk.accounts_at_risk` is populated in gather.gather_all as
#      `sum(1 for a in decay if a.rep_number == risk.rep_number)` — a PRESENCE
#      count over the top-N decay extract, not a risk count. clc's five cards
#      are five reps who each own one large account; not one of those accounts
#      needs a call.
#   2. The card renders the rep's HIGHEST-LTM decay row, which need not be a
#      row that slipped. On hfg that is account 1489 at +6.7%.
#
# Both are decided here, once, so the template renders what it is handed.


@dataclass(frozen=True)
class CoachingCard:
    """One rendered coaching card: the rep, the account it is about, the evidence."""

    risk: RepRisk
    account: Optional[AccountDecay]
    flagged: tuple[AccountDecay, ...]

    @property
    def flagged_count(self) -> int:
        return len(self.flagged)

    @property
    def at_risk_ltm(self) -> float:
        """LTM revenue of the accounts on this rep's book that have slipped.

        This — not ``RepRisk.dollars_at_risk`` — is what the card is about.
        `dollars_at_risk` is a discount-LEAK proxy, and it does not track the
        at-risk book: on hfg the two reps carrying the six declining accounts
        (12328 with $446K across 3, 42332 with $231K across 2) do not appear in
        the top six `rep_risks` rows at all, while rep CANOREP leads on $22K of
        leak sitting on an account that is *growing*.
        """
        return sum(a.ltm_rev for a in self.flagged)


def coaching_card_reps(
    rep_risks: list[RepRisk],
    decay: list[AccountDecay],
    thresholds: Optional[Thresholds] = None,
) -> list[CoachingCard]:
    """The coaching-card set, built from the AT-RISK BOOK and ranked by it.

    Two things were wrong before, and the second one no threshold could fix:

    1. **Ranked on the wrong quantity.** ``RepRisk.dollars_at_risk`` is a
       discount-LEAK proxy. hfg led with rep CANOREP ($22K of leak) on an
       account that is *growing*, while rep 12328 — $446K across three real
       declines — never appeared.
    2. **Sourced from the wrong side.** The set was bounded by the leak query
       (C2). clc's three reps carrying a slipped account (51, 74, 1402) are not
       in ``rep_risks`` **at all**, so clc could never produce a correct card no
       matter where the floor sat. Raising it only took the wrong cards away
       (cci 3->0, clc 5->0, hfg 5->0).

    So the set is now derived from the decay extract: every rep carrying at
    least one account that ``account_needs_a_call`` gets a card, ranked by the
    LTM of that book, with the leak row joined on for context when one exists.
    A rep with leak but no slipped account routes to the discount-discipline
    note, exactly as before — that is not a coaching card.
    """
    from .gather import account_needs_a_call

    t = thresholds or DEFAULT_THRESHOLDS
    by_rep: dict[str, list[AccountDecay]] = {}
    for account in decay:
        rep = (account.rep_number or "").strip()
        if not rep or not account_needs_a_call(account):
            continue
        by_rep.setdefault(rep, []).append(account)

    risk_by_rep = {(r.rep_number or "").strip(): r for r in rep_risks}
    cards: list[CoachingCard] = []
    for rep, accounts in by_rep.items():
        flagged = tuple(sorted(accounts, key=lambda a: a.ltm_rev, reverse=True))
        risk = risk_by_rep.get(rep) or RepRisk(
            rep_number=rep,
            rep_name_tier2=next(
                (a.rep_label for a in flagged if getattr(a, "rep_label", None)), None
            ),
            dollars_at_risk=0.0,
            accounts_at_risk=len(flagged),
            leak_dollars=None,
            leak_pct=None,
        )
        card = CoachingCard(risk=risk, account=flagged[0], flagged=flagged)
        if card.at_risk_ltm < t.coaching_card_min_dollars:
            continue
        cards.append(card)
    cards.sort(key=lambda c: c.at_risk_ltm, reverse=True)
    return cards


# ─── P0-7: single-door project concentration ──────────────────────────────
# HFG's top-12 is 25% one-off custom SKUs, one dealer each, and the far more
# interesting fact — that a single ~$2.6M custom project in ONE door drove 6.4%
# of a $41.2M year — was never stated anywhere in the brief.
#
# Both gates are RELATIVE, per AUDIT_FINDINGS §2.1: one to the org's topline,
# one to the org's own catalog. An absolute dollar floor here would be the
# Sarreid overfit in a new place.
#
# Gate 2 is what separates a project from a channel. ali's `SB-23*` pair is
# 2.6% of LTM across one door too — but it ships 2,750 units at $69 each. That
# is a marketplace or direct account, not a fabricated project, and it is
# already covered by concentration signals. HFG's cluster ships 63 units at
# $41,871 each: 26× its own catalog's median unit price.
#
# Calibration across the 8 cohort catalogs that have one is in
# handoffs/exec/W1_evidence.md. Candidates (2%, 5×) / (3%, 8×) / (5%, 10×) all
# fire on hfg alone and on nothing else, so the cohort does not discriminate
# between them — these are the middle values and they are the OWNER'S to move.
PROJECT_MIN_SHARE_OF_LTM = 0.03      # cluster ≥3% of invoiced LTM
PROJECT_MIN_UNIT_PRICE_RATIO = 8.0   # cluster $/unit ≥8× the catalog median
PROJECT_SKU_PREFIX_MIN_LEN = 4       # shared SKU-prefix length that makes a cluster

# ─── Editorial weights (surprise × actionability per signal kind) ─────────
SIGNAL_WEIGHTS = {
    "real_decline":          {"surprise_warning": 0.6, "surprise_critical": 0.9, "actionability": 0.9},
    "cadence_cliff":         {"surprise": 0.6, "actionability": 0.9},
    "growth_pocket":         {"surprise": 0.6, "actionability": 0.3},
    "new_line_takeoff":      {"surprise": 0.9, "actionability": 0.3},
    "lift_concentration":    {"surprise_low": 0.6, "surprise_high": 0.9, "actionability": 0.3},
    "rep_overperform":       {"surprise": 0.6, "actionability": 0.3},
    "rep_underperform":      {"surprise": 0.6, "actionability": 0.6},
    "rep_atrisk_book":       {"surprise": 0.6, "actionability": 0.6},
    "cross_sell_pocket":     {"surprise": 0.6, "actionability": 0.6},
    "second_year_gap":       {"surprise": 0.6, "actionability": 0.6},
    "channel_concentration": {"surprise_low": 0.3, "surprise_high": 0.6, "actionability": 0.3},
    "ecat_minority":         {"surprise": 0.3, "actionability": 0.3},
    "leakage_discipline":    {"surprise": 0.3, "actionability": 0.3},
    "territory_cluster_decay": {"surprise": 0.9, "actionability": 0.8},
    "single_door_project":   {"surprise": 0.9, "actionability": 0.3},
}

# ─── Industry-context downweights (knowledge/industry_context.md) ─────────
# When a signal matches a known industry-normal pattern, multiply its
# surprise by the downweight factor. This prevents the pipeline from
# "discovering" things that are simply true of the furniture/lighting/décor
# wholesale industry.
INDUSTRY_CONTEXT_DOWNWEIGHT: dict[str, dict] = {
    "channel_concentration": {
        "condition": "single_channel_is_marketplace_or_dtc",
        "factor": 0.5,
        "rationale": "Multi-channel is the norm; a dominant marketplace (Wayfair) is structurally common",
    },
    "ecat_minority": {
        "condition": "always",
        "factor": 0.5,
        "rationale": "eCat capture is almost always a minority of total business — structural, not a finding",
    },
    "cadence_cliff": {
        "condition": "buyer_type_is_project_or_designer",
        "factor": 0.4,
        "rationale": "Project/designer buyers order in bursts; 60-day silence is normal cadence, not a cliff",
    },
    "lift_concentration": {
        "condition": "no_second_qualifying_fact",
        "factor": 0.3,
        "rationale": "Big-account concentration is structurally normal; only a finding when paired with decline, single-rep risk, or concentration growth",
    },
    "second_year_gap": {
        "condition": "buyer_type_is_project_or_designer",
        "factor": 0.6,
        "rationale": "Project/designer buyers order once by definition; low return rate is structural, not a gap",
    },
    "real_decline": {
        "condition": "seasonal_q1_to_q2_dip_under_25pct",
        "factor": 0.5,
        "rationale": "Post-market spring→summer cooling is the normal seasonal pattern, not a warning sign",
    },
}


# ─── Detection rules ───────────────────────────────────────────────────────

def detect_real_decline(
    account: AccountDecay, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if account.prior_6mo <= 0:
        return None
    pace = account.recent_6mo / account.prior_6mo
    if pace >= DECLINE_PACE_THRESHOLD or account.ltm_rev < t.decline_min_ltm:
        return None
    severity = "CRITICAL" if pace < 0.4 else "WARNING"
    w = SIGNAL_WEIGHTS["real_decline"]
    return Signal(
        kind="real_decline",
        section="watchlist",
        headline=f"Account {account.bill_to_number} down {int((1-pace)*100)}% H/H",
        surprise=w["surprise_warning"] if severity == "WARNING" else w["surprise_critical"],
        dollar_impact=account.ltm_rev,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=DeclineContext(account=account.bill_to_number, rep=account.rep_number, pace=pace),
        is_positive=False,
    )


def detect_cadence_cliff(account: AccountDecay) -> Optional[Signal]:
    if account.mean_order_gap_days <= 0:
        return None
    if account.days_silent <= CADENCE_CLIFF_GAP_MULTIPLIER * account.mean_order_gap_days:
        return None
    if account.recent_vs_prior_pct is not None and account.recent_vs_prior_pct < 0:
        return None
    w = SIGNAL_WEIGHTS["cadence_cliff"]
    return Signal(
        kind="cadence_cliff",
        section="thisweek",
        headline=f"Account {account.bill_to_number} silent {account.days_silent}d (gap={int(account.mean_order_gap_days)}d)",
        surprise=w["surprise"],
        dollar_impact=account.ltm_rev,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=CadenceContext(account=account.bill_to_number, days_silent=account.days_silent),
        is_positive=False,
    )


def detect_growth_pocket(
    family: FamilyRollup, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if family.yoy_pct is None or family.yoy_pct < GROWTH_POCKET_MIN_YOY_PCT:
        return None
    if family.dealer_count < t.growth_pocket_min_dealers:
        return None
    w = SIGNAL_WEIGHTS["growth_pocket"]
    return Signal(
        kind="growth_pocket",
        section="products",
        headline=f"{family.family_label} +{int(family.yoy_pct)}% YoY across {family.dealer_count} dealers",
        surprise=w["surprise"],
        dollar_impact=family.ltm_revenue,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context={"family": family.family_label, "yoy": family.yoy_pct},
        is_positive=True,
    )


def detect_new_line_takeoff(
    family: FamilyRollup, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if not family.is_new:
        return None
    if family.ltm_revenue < t.new_line_min_revenue or family.dealer_count < t.new_line_min_dealers:
        return None
    w = SIGNAL_WEIGHTS["new_line_takeoff"]
    return Signal(
        kind="new_line_takeoff",
        section="products",
        headline=f"New line {family.family_label}: ${int(family.ltm_revenue/1000)}K on {family.dealer_count} dealers in year 1",
        surprise=w["surprise"],
        dollar_impact=family.ltm_revenue,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context={"family": family.family_label},
        is_positive=True,
    )


def detect_lift_concentration(
    probe: ConcentrationProbe,
    lifters: list[ContribRow],
    decay: list["AccountDecay"] | None = None,
    rep_risks: list["RepRisk"] | None = None,
) -> Optional[Signal]:
    """Concentration is context, not a finding, unless paired with a second
    qualifying fact (industry_context.md). Second facts: the top account is
    declining, a single rep carries >60% of book on that account, or
    concentration grew >10pp YoY (not yet measurable — requires prior-period
    probe). Without a second fact, surprise is near-suppressed (0.1)."""
    if probe is None:
        return None
    if probe.top1_share < 20.0:
        return None
    top5_total = sum(l.ltm_rev for l in lifters[:5])
    all_total = sum(l.ltm_rev for l in lifters) if lifters else 1.0
    if all_total <= 0:
        return None
    top5_share = 100.0 * top5_total / all_total
    if top5_share < LIFT_CONC_TOP5_THRESHOLD and probe.top1_share < 25.0:
        return None

    has_second_fact = False
    top_account_id = lifters[0].bill_to_number if lifters else ""
    if decay and top_account_id:
        top_in_decay = next((a for a in decay if a.bill_to_number == top_account_id), None)
        if top_in_decay and top_in_decay.is_real_decline:
            has_second_fact = True
    if not has_second_fact and rep_risks and top_account_id:
        for risk in rep_risks:
            if risk.dollars_at_risk > 0 and risk.accounts_at_risk <= 2:
                has_second_fact = True
                break

    w = SIGNAL_WEIGHTS["lift_concentration"]
    surprise = w["surprise_low"] if probe.top1_share < 30 else w["surprise_high"]
    if not has_second_fact:
        surprise = 0.1

    return Signal(
        kind="lift_concentration",
        section="layers",
        headline=f"Top-1 customer = {probe.top1_share:.0f}% of LTM revenue (HHI {probe.hhi:.0f})",
        surprise=surprise,
        dollar_impact=lifters[0].ltm_rev if lifters else 0.0,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=ConcentrationContext(top1_pct=probe.top1_share, hhi=probe.hhi),
        is_positive=False,
    )


def detect_rep_overperform(
    rep: RepRow, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if rep.yoy_pct is None or rep.yoy_pct < REP_OVERPERFORM_MIN_YOY:
        return None
    if rep.is_house or rep.ltm_invoiced < t.rep_book_min:
        return None
    w = SIGNAL_WEIGHTS["rep_overperform"]
    return Signal(
        kind="rep_overperform",
        section="team",
        headline=f"{rep.rep_label or rep.rep_number} +{int(rep.yoy_pct)}% YoY (${int(rep.ltm_invoiced/1000)}K)",
        surprise=w["surprise"],
        dollar_impact=rep.ltm_invoiced,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=RepContext(rep=rep.rep_label, yoy=rep.yoy_pct),
        is_positive=True,
    )


def detect_rep_underperform(
    rep: RepRow, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if rep.yoy_pct is None or rep.yoy_pct > REP_UNDERPERFORM_MAX_YOY:
        return None
    if rep.is_house or rep.ltm_invoiced < t.rep_book_min:
        return None
    w = SIGNAL_WEIGHTS["rep_underperform"]
    return Signal(
        kind="rep_underperform",
        section="team",
        headline=f"{rep.rep_label or rep.rep_number} {int(rep.yoy_pct)}% YoY (${int(rep.ltm_invoiced/1000)}K)",
        surprise=w["surprise"],
        dollar_impact=rep.ltm_invoiced * abs(rep.yoy_pct) / 100.0,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=RepContext(rep=rep.rep_label, yoy=rep.yoy_pct),
        is_positive=False,
    )


def detect_rep_atrisk_book(
    risk: RepRisk, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if risk.dollars_at_risk < t.rep_atrisk_min:
        return None
    w = SIGNAL_WEIGHTS["rep_atrisk_book"]
    return Signal(
        kind="rep_atrisk_book",
        section="team",
        headline=f"Rep {risk.rep_number} carries ${int(risk.dollars_at_risk/1000)}K at-risk book",
        surprise=w["surprise"],
        dollar_impact=risk.dollars_at_risk,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context={"rep": risk.rep_number, "leak_pct": risk.leak_pct},
        is_positive=False,
    )


def detect_cross_sell_pocket(
    anchor: ProductRow,
    target_family: FamilyRollup,
    gather: GatherBundle,
    thresholds: Optional[Thresholds] = None,
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if gather.cross_sell_gap is None:
        return None
    if target_family.dealer_count < t.cross_sell_min_target_dealers:
        return None
    w = SIGNAL_WEIGHTS["cross_sell_pocket"]
    gap_count = gather.cross_sell_gap.count
    return Signal(
        kind="cross_sell_pocket",
        section="products",
        headline=(
            f"{gap_count} dealers buying {anchor.item_number} have not bought "
            f"{target_family.family_label}"
            if gap_count > 0
            else (
                f"{anchor.item_number} buyers already overlap fully with "
                f"{target_family.family_label}"
            )
        ),
        surprise=w["surprise"],
        dollar_impact=target_family.ltm_revenue * CROSS_SELL_ADDRESSABLE_FRACTION,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=CrossSellContext(anchor=anchor.item_number, target=target_family.family_label),
        is_positive=True,
    )


def detect_second_year_gap(
    cohort: DealerCohort, thresholds: Optional[Thresholds] = None
) -> Optional[Signal]:
    t = thresholds or DEFAULT_THRESHOLDS
    if cohort.second_year_return_rate is None:
        return None
    if cohort.second_year_return_rate >= SECOND_YEAR_RETURN_THRESHOLD:
        return None
    lapsed_value = cohort.one_time_rev * (1.0 - cohort.second_year_return_rate)
    if lapsed_value < t.second_year_min_lapsed:
        return None
    w = SIGNAL_WEIGHTS["second_year_gap"]
    return Signal(
        kind="second_year_gap",
        section="dealers",
        headline=f"Only {int(cohort.second_year_return_rate*100)}% of first-timers return — ${int(lapsed_value/1000)}K at stake",
        surprise=w["surprise"],
        dollar_impact=lapsed_value,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=RetentionContext(return_rate=cohort.second_year_return_rate),
        is_positive=False,
    )


def detect_channel_concentration(channels: list[ChannelRow]) -> Optional[Signal]:
    if not channels:
        return None
    top = channels[0]
    if top.share_pct < CHANNEL_CONC_THRESHOLD:
        return None
    w = SIGNAL_WEIGHTS["channel_concentration"]
    return Signal(
        kind="channel_concentration",
        section="channels",
        headline=f"{top.label} = {top.share_pct:.0f}% of booked revenue",
        surprise=w["surprise_low"] if top.share_pct < 85 else w["surprise_high"],
        dollar_impact=top.booked_dollars,
        actionability=w["actionability"],
        confidence_ceiling="PARTIAL",
        context=ChannelContext(channel=top.label, pct=top.share_pct),
        is_positive=False,
    )


def detect_ecat_minority(inv_ltm_net: float, ecat_confirmed_gmv: float = 0.0) -> Optional[Signal]:
    """Track B fix (audit_cci §4.1): this used to prefer the Q-CHAN-10
    order_origin "eCat" row's `booked_dollars` over `ecat_confirmed_gmv`,
    which tags orders differently than the eCat-SALE filter and produced a
    second, divergent eCat % (11.5% vs the canonical 11.4%). The eCat-SALE
    confirmed figure (`posture.ecat_ltm_confirmed_gmv`, same source as
    Q-CHAN-05 and `RunPosture.ecat_pct_of_invoiced`) is now the ONLY input —
    single source of truth for this signal's percentage.
    """
    if inv_ltm_net <= 0:
        return None
    ecat_pct = 100.0 * ecat_confirmed_gmv / inv_ltm_net
    if ecat_pct >= ECAT_MINORITY_THRESHOLD:
        return None
    w = SIGNAL_WEIGHTS["ecat_minority"]
    return Signal(
        kind="ecat_minority",
        section="channels",
        headline=f"eCat = {ecat_pct:.1f}% of invoiced LTM (below {ECAT_MINORITY_THRESHOLD}% threshold)",
        surprise=w["surprise"],
        dollar_impact=inv_ltm_net * (ECAT_MINORITY_THRESHOLD - ecat_pct) / 100.0,
        actionability=w["actionability"],
        confidence_ceiling="PARTIAL",
        context=EcatContext(ecat_pct=ecat_pct, inv_ltm_net=inv_ltm_net),
        is_positive=False,
    )


def detect_leakage_discipline(rep_risks: list[RepRisk], inv_ltm_net: float) -> Optional[Signal]:
    if not rep_risks or inv_ltm_net <= 0:
        return None
    total_leak = sum(r.dollars_at_risk for r in rep_risks)
    org_leak_pct = 100.0 * total_leak / inv_ltm_net
    if org_leak_pct >= LEAKAGE_LOW_THRESHOLD:
        return None
    w = SIGNAL_WEIGHTS["leakage_discipline"]
    return Signal(
        kind="leakage_discipline",
        section="layers",
        headline=f"Org-wide leakage = {org_leak_pct:.1f}% (well below {LEAKAGE_LOW_THRESHOLD}% norm)",
        surprise=w["surprise"],
        dollar_impact=total_leak,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=LeakContext(leak_pct=org_leak_pct, total_leak_dollars=total_leak),
        is_positive=True,
    )


def detect_territory_cluster_decay(
    decay: list[AccountDecay],
    rep_number: str,
    min_accounts: int = 3,
) -> Optional[Signal]:
    """A territory-cluster signal fires when 3+ accounts under one rep are ALL
    in real_decline. This is a territory problem, not a coincidence of independent
    account decisions — it needs a different conversation than individual coaching."""
    rep_decay = [a for a in decay if a.rep_number == rep_number and a.is_real_decline]
    if len(rep_decay) < min_accounts:
        return None
    total_at_risk = sum(a.ltm_rev for a in rep_decay)
    w = SIGNAL_WEIGHTS["territory_cluster_decay"]
    return Signal(
        kind="territory_cluster_decay",
        section="team",
        headline=f"Territory cluster: rep {rep_number} has {len(rep_decay)} accounts in real decline (${int(total_at_risk/1000)}K)",
        surprise=w["surprise"],
        dollar_impact=total_at_risk,
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context={
            "rep": rep_number,
            "accounts": len(rep_decay),
            "total_at_risk": total_at_risk,
            "account_names": [a.bill_to_name or a.bill_to_number for a in rep_decay[:5]],
        },
        is_positive=False,
    )


def _shared_prefix(a: str, b: str) -> str:
    out = []
    for x, y in zip(a, b):
        if x != y:
            break
        out.append(x)
    return "".join(out)


def detect_single_door_project(
    products: list[ProductRow],
    inv_ltm_net: float,
) -> Optional[Signal]:
    """A custom project shipped to ONE door, large enough to move the year.

    Groups the single-dealer items in the top-N catalog by shared SKU prefix,
    then applies two size-relative gates: share of invoiced LTM, and unit price
    against the org's own catalog median. See the constants above for why both
    are needed and why neither is an absolute dollar figure.

    Under-detects by construction: Q-PROD-TOP carries the top 25 items only, so
    a project whose SKUs rank below that is invisible here. It never
    over-detects — every gate is a floor.
    """
    if not products or inv_ltm_net <= 0:
        return None

    priced = [p for p in products if p.units > 0 and p.ltm_revenue > 0]
    if len(priced) < 3:
        return None
    unit_prices = sorted(p.ltm_revenue / p.units for p in priced)
    mid = len(unit_prices) // 2
    median_unit_price = (
        unit_prices[mid]
        if len(unit_prices) % 2
        else (unit_prices[mid - 1] + unit_prices[mid]) / 2
    )
    if median_unit_price <= 0:
        return None

    singles = [p for p in priced if p.dealers == 1]
    if not singles:
        return None

    clusters: list[dict] = []
    for product in singles:
        for cluster in clusters:
            shared = _shared_prefix(cluster["prefix"], product.item_number)
            if len(shared) >= PROJECT_SKU_PREFIX_MIN_LEN:
                cluster["prefix"] = shared
                cluster["items"].append(product)
                break
        else:
            clusters.append({"prefix": product.item_number, "items": [product]})

    best: Optional[dict] = None
    for cluster in clusters:
        dollars = sum(p.ltm_revenue for p in cluster["items"])
        units = sum(p.units for p in cluster["items"])
        if units <= 0:
            continue
        share = dollars / inv_ltm_net
        unit_price = dollars / units
        if share < PROJECT_MIN_SHARE_OF_LTM:
            continue
        if unit_price / median_unit_price < PROJECT_MIN_UNIT_PRICE_RATIO:
            continue
        cluster.update(
            dollars=dollars, units=units, share=share, unit_price=unit_price,
            ratio=unit_price / median_unit_price,
        )
        if best is None or dollars > best["dollars"]:
            best = cluster
    if best is None:
        return None

    items = sorted(best["items"], key=lambda p: p.ltm_revenue, reverse=True)
    w = SIGNAL_WEIGHTS["single_door_project"]
    return Signal(
        kind="single_door_project",
        section="products",
        headline=(
            f"{len(items)} single-dealer SKUs sharing prefix {best['prefix']} "
            f"carry ${int(best['dollars'] / 1000)}K — "
            f"{best['share'] * 100:.1f}% of invoiced LTM"
        ),
        surprise=w["surprise"],
        dollar_impact=best["dollars"],
        actionability=w["actionability"],
        confidence_ceiling="STRONG",
        context=ProjectContext(
            prefix=best["prefix"],
            sku_count=len(items),
            dollars=best["dollars"],
            share_pct=best["share"] * 100,
            units=int(best["units"]),
            unit_price=best["unit_price"],
            unit_price_ratio=best["ratio"],
            items=[
                {
                    "item_number": p.item_number,
                    "label": p.display_description,
                    "ltm_revenue": p.ltm_revenue,
                    "units": int(p.units),
                }
                for p in items
            ],
        ),
        is_positive=True,
    )


# ─── Orchestration ─────────────────────────────────────────────────────────
def detect_all(
    gather: GatherBundle,
    posture: RunPosture,
    thresholds: Optional[Thresholds] = None,
) -> list[Signal]:
    """Run every detection rule against the gather bundle. Returns all
    fired signals, unsorted. Caller ranks + selects the top N per section.

    `thresholds` resolves the size-dependent gates against THIS org. Omitted,
    it is derived from `posture`/`gather` through ACTIVE_PROFILE — so callers
    that predate W3 get the org-correct thresholds rather than Sarreid's.
    """
    t = thresholds or resolve_thresholds(posture, gather)
    signals: list[Signal] = []

    for account in gather.decay:
        sig = detect_real_decline(account, t)
        if sig:
            signals.append(sig)
        sig = detect_cadence_cliff(account)
        if sig:
            signals.append(sig)

    for family in gather.families:
        sig = detect_growth_pocket(family, t)
        if sig:
            signals.append(sig)
        sig = detect_new_line_takeoff(family, t)
        if sig:
            signals.append(sig)

    sig = detect_single_door_project(gather.products, posture.inv_ltm_net)
    if sig:
        signals.append(sig)

    if gather.products and gather.families:
        sig = detect_cross_sell_pocket(
            gather.products[0], gather.families[0], gather, t
        )
        if sig:
            signals.append(sig)

    if gather.conc_customer:
        sig = detect_lift_concentration(
            gather.conc_customer, gather.lifters,
            decay=gather.decay, rep_risks=gather.rep_risks,
        )
        if sig:
            signals.append(sig)

    for rep in gather.reps:
        sig = detect_rep_overperform(rep, t)
        if sig:
            signals.append(sig)
        sig = detect_rep_underperform(rep, t)
        if sig:
            signals.append(sig)

    for risk in gather.rep_risks:
        sig = detect_rep_atrisk_book(risk, t)
        if sig:
            signals.append(sig)

    if gather.dealers:
        sig = detect_second_year_gap(gather.dealers, t)
        if sig:
            signals.append(sig)

    sig = detect_channel_concentration(gather.channels)
    if sig:
        signals.append(sig)

    sig = detect_ecat_minority(posture.inv_ltm_net, getattr(posture, "ecat_ltm_confirmed_gmv", 0.0))
    if sig:
        signals.append(sig)

    sig = detect_leakage_discipline(gather.rep_risks, posture.inv_ltm_net)
    if sig:
        signals.append(sig)

    # Territory-cluster decay: 3+ accounts under one rep all declining
    seen_reps: set[str] = set()
    for risk in gather.rep_risks:
        if risk.rep_number not in seen_reps:
            seen_reps.add(risk.rep_number)
            sig = detect_territory_cluster_decay(gather.decay, risk.rep_number)
            if sig:
                signals.append(sig)

    # Cap confidence at COMMERCE_CONFIDENCE
    from . import config
    commerce_rank = config.CONFIDENCE_RANK.get(posture.commerce_confidence, 0)
    for s in signals:
        sig_rank = config.CONFIDENCE_RANK.get(s.confidence_ceiling, 3)
        if sig_rank > commerce_rank:
            s.confidence_ceiling = posture.commerce_confidence

    _apply_industry_downweights(signals)

    return signals


def _apply_industry_downweights(signals: list[Signal]) -> list[Signal]:
    """Down-weight signals that match known industry-normal patterns.

    Per knowledge/industry_context.md: if a pattern is explained by industry
    structure, it is context, not a finding. We reduce surprise (which feeds
    into SIGNAL_RANK) rather than suppressing the signal entirely.

    Honesty (2026-07-13 re-anchor D1): only condition == "always" is LIVE today
    (ecat_minority). All other conditions are STUBs — logged to stderr and
    skipped. See foundation/WHAT_ACTUALLY_RUNS.md §Industry downweights.
    """
    import sys
    for s in signals:
        entry = INDUSTRY_CONTEXT_DOWNWEIGHT.get(s.kind)
        if entry is None:
            continue
        condition = entry["condition"]
        if condition == "always":
            old_surprise = s.surprise
            s.surprise *= entry["factor"]
            print(
                f"INDUSTRY DOWNWEIGHT: {s.kind} surprise {old_surprise:.2f} → {s.surprise:.2f} "
                f"({entry['rationale']})",
                file=sys.stderr,
            )
        else:
            # Profile-backed or calendar-backed conditions — not wired yet.
            print(
                f"INDUSTRY DOWNWEIGHT STUB: {s.kind} condition '{condition}' "
                f"not evaluated — skipping (factor would be {entry['factor']})",
                file=sys.stderr,
            )
    return signals


def top_n_by_rank(signals: list[Signal], n: int) -> list[Signal]:
    return sorted(signals, key=lambda s: s.rank, reverse=True)[:n]


def signal_summary_set(signals: list[Signal]) -> list[Signal]:
    """Build the Signal Summary set per Step 7:
    top 5-7 by rank, re-sorted into narrative arc (momentum → intelligence
    → opportunity → risk), diversity max 4 from one section, ≥3 positive
    findings, finding #1 positive.
    """
    ranked = top_n_by_rank(signals, 12)

    section_counts: dict[str, int] = {}
    selected: list[Signal] = []
    for s in ranked:
        if len(selected) >= 7:
            break
        if section_counts.get(s.section, 0) >= 4:
            continue
        selected.append(s)
        section_counts[s.section] = section_counts.get(s.section, 0) + 1

    positive = [s for s in selected if s.is_positive]
    negative = [s for s in selected if not s.is_positive]
    if len(positive) < 3 and len(selected) > 3:
        extra_pos = [s for s in ranked if s.is_positive and s not in selected]
        while len(positive) < 3 and extra_pos:
            p = extra_pos.pop(0)
            selected.append(p)
            positive.append(p)

    # Arc-sort: momentum → intelligence → opportunity → risk (stable, preserves rank within category)
    selected.sort(key=lambda s: SIGNAL_ARC_ORDER.get(s.kind, 99))

    # Finding #1 must be positive (tone-balance)
    if selected and not selected[0].is_positive and positive:
        idx = next((i for i, s in enumerate(selected) if s.is_positive), None)
        if idx is not None:
            selected[0], selected[idx] = selected[idx], selected[0]

    return selected[:7]
