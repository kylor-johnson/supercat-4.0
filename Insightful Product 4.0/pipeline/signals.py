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


# ─── Thresholds (named constants, not magic numbers) ──────────────────────
DECLINE_PACE_THRESHOLD = 0.6        # recent < 60% of prior = real decline
DECLINE_MIN_LTM_DOLLARS = 50_000    # only fire for material accounts
CADENCE_CLIFF_GAP_MULTIPLIER = 2.0  # silence > 2× mean gap
GROWTH_POCKET_MIN_YOY_PCT = 20.0    # family must grow >20% YoY
GROWTH_POCKET_MIN_DEALERS = 10      # on a broad dealer base
NEW_LINE_MIN_REVENUE = 100_000      # year-1 must clear $100K
NEW_LINE_MIN_DEALERS = 5            # sold to ≥5 dealers
LIFT_CONC_TOP5_THRESHOLD = 60.0     # top-5 lifters hold >60% of lift = concentrated
REP_OVERPERFORM_MIN_YOY = 30.0      # ≥30% YoY growth
REP_UNDERPERFORM_MAX_YOY = -20.0    # ≤-20% YoY decline
REP_ATRISK_MIN_DOLLARS = 20_000     # $20K+ at risk to fire
CHANNEL_CONC_THRESHOLD = 70.0       # one channel >70% of total
ECAT_MINORITY_THRESHOLD = 15.0      # eCat <15% of invoiced LTM
LEAKAGE_LOW_THRESHOLD = 3.0         # org-wide leak rate <3% = disciplined
SECOND_YEAR_RETURN_THRESHOLD = 0.50 # <50% of first-timers come back
CROSS_SELL_ADDRESSABLE_FRACTION = 0.30  # editorial estimate of addressable cross-sell potential

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

def detect_real_decline(account: AccountDecay) -> Optional[Signal]:
    if account.prior_6mo <= 0:
        return None
    pace = account.recent_6mo / account.prior_6mo
    if pace >= DECLINE_PACE_THRESHOLD or account.ltm_rev < DECLINE_MIN_LTM_DOLLARS:
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


def detect_growth_pocket(family: FamilyRollup) -> Optional[Signal]:
    if family.yoy_pct is None or family.yoy_pct < GROWTH_POCKET_MIN_YOY_PCT:
        return None
    if family.dealer_count < GROWTH_POCKET_MIN_DEALERS:
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


def detect_new_line_takeoff(family: FamilyRollup) -> Optional[Signal]:
    if not family.is_new:
        return None
    if family.ltm_revenue < NEW_LINE_MIN_REVENUE or family.dealer_count < NEW_LINE_MIN_DEALERS:
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


def detect_rep_overperform(rep: RepRow) -> Optional[Signal]:
    if rep.yoy_pct is None or rep.yoy_pct < REP_OVERPERFORM_MIN_YOY:
        return None
    if rep.is_house or rep.ltm_invoiced < 100_000:
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


def detect_rep_underperform(rep: RepRow) -> Optional[Signal]:
    if rep.yoy_pct is None or rep.yoy_pct > REP_UNDERPERFORM_MAX_YOY:
        return None
    if rep.is_house or rep.ltm_invoiced < 100_000:
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


def detect_rep_atrisk_book(risk: RepRisk) -> Optional[Signal]:
    if risk.dollars_at_risk < REP_ATRISK_MIN_DOLLARS:
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


def detect_cross_sell_pocket(anchor: ProductRow, target_family: FamilyRollup, gather: GatherBundle) -> Optional[Signal]:
    if gather.cross_sell_gap is None:
        return None
    if target_family.dealer_count < 5:
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


def detect_second_year_gap(cohort: DealerCohort) -> Optional[Signal]:
    if cohort.second_year_return_rate is None:
        return None
    if cohort.second_year_return_rate >= SECOND_YEAR_RETURN_THRESHOLD:
        return None
    lapsed_value = cohort.one_time_rev * (1.0 - cohort.second_year_return_rate)
    if lapsed_value < 50_000:
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


# ─── Orchestration ─────────────────────────────────────────────────────────
def detect_all(gather: GatherBundle, posture: RunPosture) -> list[Signal]:
    """Run every detection rule against the gather bundle. Returns all
    fired signals, unsorted. Caller ranks + selects the top N per section.
    """
    signals: list[Signal] = []

    for account in gather.decay:
        sig = detect_real_decline(account)
        if sig:
            signals.append(sig)
        sig = detect_cadence_cliff(account)
        if sig:
            signals.append(sig)

    for family in gather.families:
        sig = detect_growth_pocket(family)
        if sig:
            signals.append(sig)
        sig = detect_new_line_takeoff(family)
        if sig:
            signals.append(sig)

    if gather.products and gather.families:
        sig = detect_cross_sell_pocket(
            gather.products[0], gather.families[0], gather
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
        sig = detect_rep_overperform(rep)
        if sig:
            signals.append(sig)
        sig = detect_rep_underperform(rep)
        if sig:
            signals.append(sig)

    for risk in gather.rep_risks:
        sig = detect_rep_atrisk_book(risk)
        if sig:
            signals.append(sig)

    if gather.dealers:
        sig = detect_second_year_gap(gather.dealers)
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
