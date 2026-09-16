"""Preflight: read cache CSVs (Q-ECON-00, Q-CHAN-00, Q-CHAN-06, RP-2), emit RunPosture.

Single responsibility: posture resolution from already-cached data. This
module does not query the database; if the cache is missing a required
CSV, raise — do not silently fall back.

Mode resolution is transcribed from
  operators/report_operator.md §5b.1 Mode Resolution

verbatim. Per the cross-cutting "no edits to canon" constraint, the
operator doc is the source of truth; this module mirrors it.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

from . import cache as _cache, config
from .cache import CachePaths


Mode = Literal[
    "Mode 1 - Standard",
    "Mode 1 - Tier-1 degraded",
    "Mode 2 - Activation",
    "Gate-STOP",
]
Confidence = Literal["STRONG", "PARTIAL", "LIMITED", "NONE"]
FeedCompleteness = Literal[
    "CORROBORATED", "UNVERIFIED-SINGLE-FEED", "PROVABLY-INCOMPLETE", "STALE", "DEAD"
]
TotalBusinessSource = Literal["INVOICES", "ORDERS", "SALES_DATA", "NONE"]
ChannelPosture = Literal["STRONG-CANDIDATE", "PARTIAL", "NONE"]


@dataclass
class RunPosture:
    """Output of Step-1 preflight (operators/report_operator.md §1). Caps
    everything downstream.
    """
    org: str
    organization_id: int
    report_through_date: str  # YYYY-MM-DD, clamped per Q-ECON-00

    # Economics (Q-ECON-00)
    total_business_source: TotalBusinessSource
    n_inv_ltm: int
    inv_ltm_net: float
    credit_memos_ltm: Optional[int]
    salesdata_over_invoiced: Optional[float]
    days_since_last_invoice: Optional[int]
    ecat_ltm_confirmed_gmv: float

    # Confidence stack
    commerce_confidence: Confidence
    feed_completeness: FeedCompleteness
    data_mass_tier: Confidence
    report_intelligence_tier: Confidence

    # Rep identity (RP-2)
    rep_identity_tier: int
    distinct_repnum: int
    name_bridge_pct: Optional[float]

    # Channels (Q-CHAN-00)
    channel_posture: ChannelPosture
    booked_rows_ltm: int
    distinct_origins: int
    ecat_recon_ratio: Optional[float]
    ecat_tag_status: str

    # eCat-SALE confirmed-ratio pre-check (Q-CHAN-06 / red-team F1). Gates
    # whether an eCat figure may stand as a report hero (Spine §6.5).
    ecat_f1_confirmed_gmv: Optional[float] = None
    ecat_f1_all_gmv: Optional[float] = None
    ecat_f1_blank_share_pct: Optional[float] = None
    ecat_f1_verdict: str = ""  # "CLEAN" | "CAP_CONFIDENCE_AND_CAVEAT" | "" (not checked)

    # Resolved
    report_mode: Mode = "Gate-STOP"
    has_ratified_profile: bool = False

    # Side-channel availability flags from Q-ECON-00
    flags: dict = field(default_factory=dict)

    # ─── Track B — single source of truth for the eCat dollar figure ──────
    # `ecat_ltm_confirmed_gmv` (Q-ECON-00) is the ONE canonical eCat dollar —
    # every template/signal must read it, never re-derive an eCat $ from
    # Q-CHAN-10's order_origin "eCat" bucket (which tags orders differently
    # and produced the original 11.4%-vs-11.5% contradiction, audit_cci §4.1)
    # and never from Q-CHAN-05's `chan_split.ecat_gmv` either — Track E's
    # 2026-07-09 re-baseline diff found Q-CHAN-05 does NOT actually apply an
    # identical filter/window: it live-diverges from this figure (Sarreid:
    # $2,041,136.71 here vs Q-CHAN-05's $2,049,865.61 — a ~0.4% gap that
    # rounds to a visibly different "$2.04M" vs "$2.05M"). Q-CHAN-05 may still
    # supply its own `total_business_gmv` / `non_ecat_gmv` split context, but
    # its `ecat_gmv` must never be displayed as *the* eCat dollar figure.
    # See `signals.detect_ecat_minority` and `section_10_channels.md.j2`.
    @property
    def ecat_pct_of_invoiced(self) -> Optional[float]:
        if self.inv_ltm_net <= 0:
            return None
        return 100.0 * self.ecat_ltm_confirmed_gmv / self.inv_ltm_net

    # ─── Track B — F1 eCat-SALE confirmed-ratio pre-check ──────────────────
    @property
    def ecat_confidence_capped(self) -> bool:
        """True when Q-CHAN-06 found a material (>=5%) blank/null `order_type`
        share defaulting to 'Confirmed' via the eCat-SALE filter's COALESCE.
        Caller must cap the eCat figure's confidence and add the caveat
        sentence (`ecat_caveat_sentence`) rather than rendering it clean."""
        return self.ecat_f1_verdict == "CAP_CONFIDENCE_AND_CAVEAT"

    @property
    def ecat_caveat_sentence(self) -> str:
        if not self.ecat_confidence_capped:
            return ""
        return "Includes orders without an explicit sale status."

    # ─── Track B — F7 eCat-hero honesty sentence ───────────────────────────
    @property
    def ecat_is_hero(self) -> bool:
        """eCat stands in as the report's headline commercial figure when
        there is no usable invoice feed (NONE) or the invoice feed is stale
        — matches the decision memo's "NONE/STALE" hero condition."""
        return (self.total_business_source == "NONE" or self.feed_completeness == "STALE") \
            and self.ecat_ltm_confirmed_gmv > 0

    @property
    def ecat_hero_sentence(self) -> str:
        if not self.ecat_is_hero:
            return ""
        return (
            "This is confirmed order volume through the platform — not your "
            "total business, which we can't size without an invoice feed."
        )

    # ─── Track C — posture framing flags: STALE + PROVABLY-INCOMPLETE ──────
    # Two framing treatments on the single spine (decision memo §3/§3b/§4
    # Track C). NO new mode, NO new template — these flags are consumed by
    # the existing section templates.
    @property
    def is_stale(self) -> bool:
        """STALE feed: the invoice window is frozen (>45 days since the last
        invoice, Spine §6.3). Decline signals below describe a past state; the
        live commercial signal is the eCat channel. Drives the §1 live-eCat-
        first lead + "refresh the feed" recovery framing and the historical
        stamping of the decay sections."""
        return self.feed_completeness == "STALE"

    @property
    def is_provably_incomplete(self) -> bool:
        """PROVABLY-INCOMPLETE feed (F6): confirmed eCat capture exceeds
        invoiced net (>1.05×, Spine §6.3), so the invoice feed is provably a
        channel subset — "invoiced net = total business" is most misleading
        here. Both figures render in absolute $; the eCat-vs-invoiced RATE is
        suppressed (VM-CHAN-1 gate)."""
        return self.feed_completeness == "PROVABLY-INCOMPLETE"

    # F2 (critical): stamp dates BY SOURCE. The report_through_date clamp
    # (Spine §6.4) binds ERP/invoiced dollars only; the eCat live window is the
    # sanctioned §0 carve-out — eCat is windowed to CURRENT_DATE (Spine §6.5)
    # and stamped "live through today", NEVER the stale invoice clamp. Stamping
    # the live eCat number with the stale date reverses the entire finding.
    @property
    def erp_asof_stamp(self) -> str:
        """"as of <report_through_date>" — for ERP/invoiced dollars ONLY."""
        return f"as of {self.report_through_date}" if self.report_through_date else "as of the last invoice date"

    @property
    def ecat_live_stamp(self) -> str:
        """"live through today" — for eCat capture ONLY (F2 carve-out)."""
        return "live through today"

    @property
    def stale_age_phrase(self) -> str:
        """Proportional staleness wording (state the actual gap), while the
        gate itself stays binary. E.g. "223 days (about 7 months)"."""
        d = self.days_since_last_invoice
        if d is None:
            return ""
        months = d // 30
        if months >= 2:
            return f"{d} days (about {months} months)"
        return f"{d} days"

    @property
    def suppress_ecat_vs_invoiced_rate(self) -> bool:
        """The eCat-vs-invoiced % is meaningless-to-misleading when the
        invoice denominator is stale (a live numerator over a frozen
        denominator) or provably a subset (rate > 100%, VM-CHAN-1 gate).
        Suppress the RATE; both figures still render in absolute $."""
        return self.feed_completeness in ("STALE", "PROVABLY-INCOMPLETE")

    @property
    def invoiced_channel_subset_sentence(self) -> str:
        """F6/§3b: replace any "total/complete business" implication on the
        invoiced topline with the honest channel-subset framing."""
        if not self.is_provably_incomplete:
            return ""
        return (
            "Invoiced net is a channel subset — confirmed eCat capture alone "
            "exceeds it — not your total or complete business."
        )


# ─── Helpers ───────────────────────────────────────────────────────────────
def _read_one_row(path: Path) -> dict:
    """Read a one-row CSV (preflight CSVs always have a single row)."""
    if not path.exists():
        raise FileNotFoundError(f"Missing preflight CSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return {}
    return rows[0]


def _f(v) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _i(v) -> Optional[int]:
    f = _f(v)
    return int(f) if f is not None else None


def _read_one_row_optional(path: Path) -> dict:
    """Like `_read_one_row` but tolerant of a missing CSV — returns {}
    instead of raising. Used for Q-CHAN-06 (Track B / F1): the guardrail
    must not hard-fail a report whose cache predates this pre-check; an
    org with no F1 cache simply renders with `ecat_f1_verdict=""` (not
    checked), which `ecat_confidence_capped` treats as clean/unknown."""
    if not path.exists():
        return {}
    return _read_one_row(path)


# ─── Derivations from Q-ECON-00 ────────────────────────────────────────────
def _derive_total_business_source(econ: dict) -> TotalBusinessSource:
    """Spine §6.3 / operator §1 step 1. Invoice feed present → INVOICES.
    Otherwise fall back to ORDERS if booked is present (Q-CHAN-00.booked_rows),
    then SALES_DATA, then NONE. Q-ECON-00 emits invoice_feed_present.
    """
    if str(econ.get("invoice_feed_present", "false")).lower() in ("true", "t", "1"):
        return "INVOICES"
    # NONE-feed: caller must consult Q-CHAN-00 booked_rows + sales_data via
    # a separate probe. For Phase-1 preflight from cache, INVOICES vs NONE
    # is the only deterministic call without extra queries.
    return "NONE"


def _derive_feed_completeness(econ: dict) -> FeedCompleteness:
    """Per Q-ECON-00 inline logic + Spine §6.3:
      n_inv=0                                   → DEAD
      days_since_last_invoice > 45              → STALE
      ecat_confirmed > 1.05 × inv_ltm_net       → PROVABLY-INCOMPLETE
      else (single fresh invoice feed)          → UNVERIFIED-SINGLE-FEED
      (CORROBORATED requires two independent feeds; not derivable from Q-ECON-00 alone.)
    """
    n_inv = _i(econ.get("n_inv")) or 0
    if n_inv == 0:
        return "DEAD"
    days = _i(econ.get("days_since_last_invoice"))
    if days is not None and days > 45:
        return "STALE"
    ecat = _f(econ.get("ecat_ltm_confirmed_gmv")) or 0.0
    inv = _f(econ.get("inv_ltm_net")) or 0.0
    if inv > 0 and ecat > 1.05 * inv:
        return "PROVABLY-INCOMPLETE"
    return "UNVERIFIED-SINGLE-FEED"


def _derive_data_mass_tier(econ: dict) -> Confidence:
    """Mass tier (Spine §6.3): how much invoiced $ / how many invoices.
    Operator §1 ladder (worked-example calibration):
      n_inv >= 5000  AND inv_ltm_net >= $5M  → STRONG
      n_inv >= 1000  AND inv_ltm_net >= $1M  → PARTIAL
      n_inv >= 100   AND inv_ltm_net >= $100K → LIMITED
      else                                   → NONE
    """
    n = _i(econ.get("n_inv")) or 0
    rev = _f(econ.get("inv_ltm_net")) or 0.0
    if n >= 5000 and rev >= 5_000_000:
        return "STRONG"
    if n >= 1000 and rev >= 1_000_000:
        return "PARTIAL"
    if n >= 100 and rev >= 100_000:
        return "LIMITED"
    return "NONE"


def _intelligence_tier(mass: Confidence, conf: Confidence) -> Confidence:
    """REPORT_INTELLIGENCE_TIER = LEAST(DATA_MASS_TIER, confidence_to_tier(COMMERCE_CONFIDENCE))."""
    mass_rank = config.CONFIDENCE_RANK.get(mass, 0)
    conf_rank = config.CONFIDENCE_RANK.get(conf, 0)
    return config.TIER_NAMES[min(mass_rank, conf_rank)]


# F1 threshold (decision_completeness_no_drift_2026-07-09.md §0 red-team F1 /
# track_B_ecat_labeling.md task 4c): blank/null `order_type` GMV that
# defaults to 'Confirmed' via the eCat-SALE filter's COALESCE, as a share of
# confirmed GMV. >=5% caps the eCat figure's confidence and adds the caveat.
ECAT_F1_BLANK_SHARE_CAP_THRESHOLD = 5.0


def _derive_ecat_f1_verdict(blank_share_pct: Optional[float]) -> str:
    """Q-CHAN-06 emits the raw blank_default_share_pct; the >=5% cap rule
    (task 4c) is threshold logic, not SQL — applied here, once, so every
    caller reads `RunPosture.ecat_confidence_capped` instead of re-checking
    the number. Empty string ("not checked") when the pre-check has no
    cached result — treated as clean/unknown, never as capped."""
    if blank_share_pct is None:
        return ""
    if blank_share_pct >= ECAT_F1_BLANK_SHARE_CAP_THRESHOLD:
        return "CAP_CONFIDENCE_AND_CAVEAT"
    return "CLEAN"


def _derive_channel_posture(chan: dict) -> ChannelPosture:
    """Q-CHAN-00 emits the gate string in channel_confidence_gate.
    NONE if SUPPRESS; STRONG-CANDIDATE if CANDIDATE; else PARTIAL."""
    gate = str(chan.get("channel_confidence_gate", "")).upper()
    if gate.startswith("NONE"):
        return "NONE"
    if "CANDIDATE" in gate:
        return "STRONG-CANDIDATE"
    return "PARTIAL"


# ─── Mode resolution (verbatim §5b.1) ──────────────────────────────────────
def resolve_mode(
    *,
    commerce_confidence: Confidence,
    rep_identity_tier: int,
    ecat_ltm_confirmed_gmv: float,
    has_ratified_profile: bool,
    cohort_validation: bool = False,
    ecat_materiality_threshold: float = 250_000.0,
) -> Mode:
    """Per operators/report_operator.md §5b.1 Mode Resolution table.

    Gate-STOP rules (table row 4):
      - COMMERCE_CONFIDENCE = NONE AND eCat capture missing or below materiality, OR
      - Step 0: no ratified profile (and no --cohort-validation override), OR
      - Hard preflight failure (caller's job to detect)

    Mode-2 Activation (table row 3):
      - COMMERCE_CONFIDENCE = NONE OR REP_IDENTITY_TIER = 0
      - and eCat capture IS present and material

    Mode-1 Tier-1 degraded (table row 2):
      - REP_IDENTITY_TIER = 1 AND COMMERCE_CONFIDENCE >= PARTIAL

    Mode-1 Standard (table row 1):
      - otherwise (every other gate clears the Sarreid baseline)
    """
    if not has_ratified_profile and not cohort_validation:
        return "Gate-STOP"

    if commerce_confidence == "NONE":
        if ecat_ltm_confirmed_gmv < ecat_materiality_threshold:
            return "Gate-STOP"
        return "Mode 2 - Activation"

    if rep_identity_tier == 0:
        if ecat_ltm_confirmed_gmv < ecat_materiality_threshold:
            return "Gate-STOP"
        return "Mode 2 - Activation"

    if rep_identity_tier == 1 and config.CONFIDENCE_RANK[commerce_confidence] >= config.CONFIDENCE_RANK["PARTIAL"]:
        return "Mode 1 - Tier-1 degraded"

    return "Mode 1 - Standard"


# ─── Entrypoint ────────────────────────────────────────────────────────────
def run(org: str, date: str, *, cohort_validation: bool = False) -> RunPosture:
    """Read cache CSVs, resolve posture, return RunPosture."""
    paths = CachePaths.for_run(org, date)

    econ = _read_one_row(paths.csv_for("Q-ECON-00"))
    chan = _read_one_row(paths.csv_for("Q-CHAN-00"))
    repi = _read_one_row(paths.csv_for("RP-2"))
    f1 = _read_one_row_optional(paths.csv_for("Q-CHAN-06"))

    commerce_conf: Confidence = (econ.get("commerce_confidence") or "NONE").upper()  # type: ignore[assignment]
    feed_completeness = _derive_feed_completeness(econ)
    data_mass = _derive_data_mass_tier(econ)
    tier = _intelligence_tier(data_mass, commerce_conf)
    total_source = _derive_total_business_source(econ)
    channel_posture = _derive_channel_posture(chan)

    rep_tier = _i(repi.get("rep_identity_tier")) or 0
    # Deadband carry-over: if SQL returns Tier 1 but org is a declared
    # Tier-2 hold in the 78-82% deadband, override to Tier 2.
    # Source: rep_copilot_operator.md §1 hysteresis band.
    overrides = config.load_tier_overrides()
    deadband = overrides.get("tier2_deadband_hold", {})
    if rep_tier == 1 and org in deadband:
        rep_tier = 2
    distinct_repnum = _i(repi.get("distinct_repnum")) or 0
    name_bridge_pct = _f(repi.get("name_bridge_pct"))

    inv_ltm_net = _f(econ.get("inv_ltm_net")) or 0.0
    ecat_gmv = _f(econ.get("ecat_ltm_confirmed_gmv")) or 0.0

    profile_path = config.PROFILES_DIR / f"{org}.md"
    has_profile = profile_path.exists()

    mode = resolve_mode(
        commerce_confidence=commerce_conf,
        rep_identity_tier=rep_tier,
        ecat_ltm_confirmed_gmv=ecat_gmv,
        has_ratified_profile=has_profile,
        cohort_validation=cohort_validation,
    )

    flag_keys = (
        "invoice_feed_present",
        "leakage_dispersion_ok",
        "netrev_freight_ok",
        "returns_ok",
        "terms_ok",
        "carrier_ok",
        "leadtime_ok",
        "channel_ok",
    )
    flags = {k: str(econ.get(k, "")).lower() in ("true", "t", "1") for k in flag_keys}

    return RunPosture(
        org=org,
        organization_id=_cache.resolve_org_id(org),
        report_through_date=str(econ.get("report_through_date") or ""),
        total_business_source=total_source,
        n_inv_ltm=_i(econ.get("n_inv")) or 0,
        inv_ltm_net=inv_ltm_net,
        credit_memos_ltm=_i(econ.get("credit_memos")),
        salesdata_over_invoiced=_f(econ.get("salesdata_over_invoiced")),
        days_since_last_invoice=_i(econ.get("days_since_last_invoice")),
        ecat_ltm_confirmed_gmv=ecat_gmv,
        commerce_confidence=commerce_conf,
        feed_completeness=feed_completeness,
        data_mass_tier=data_mass,
        report_intelligence_tier=tier,
        rep_identity_tier=rep_tier,
        distinct_repnum=distinct_repnum,
        name_bridge_pct=name_bridge_pct,
        channel_posture=channel_posture,
        booked_rows_ltm=_i(chan.get("booked_rows")) or 0,
        distinct_origins=_i(chan.get("distinct_origins")) or 0,
        ecat_recon_ratio=_f(chan.get("ecat_recon_ratio")),
        ecat_tag_status=str(chan.get("ecat_tag_status") or ""),
        ecat_f1_confirmed_gmv=_f(f1.get("confirmed_gmv")),
        ecat_f1_all_gmv=_f(f1.get("all_ecat_gmv")),
        ecat_f1_blank_share_pct=_f(f1.get("blank_default_share_pct")),
        ecat_f1_verdict=_derive_ecat_f1_verdict(_f(f1.get("blank_default_share_pct"))),
        report_mode=mode,
        has_ratified_profile=has_profile,
        flags=flags,
    )
