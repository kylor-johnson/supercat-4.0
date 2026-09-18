"""Fact bundles: per-slot structured inputs for the 6 LLM prose slots.

Each bundle has two layers:
  - facts: raw values from gather/posture/signals
  - derived_facts: pre-computed derivations (ratios, per-point deltas, estimate ranges)

The LLM is told: "Use only numbers that appear in facts or derived_facts.
Do not compute new ones."

All functions return plain dicts (JSON-serializable). No LLM calls, no external APIs.
"""
from __future__ import annotations

from typing import Optional

from .gather import (
    AccountDecay,
    CrossSellGap,
    DealerCohort,
    FamilyRollup,
    GatherBundle,
    RepRisk,
    RepRow,
)
from .preflight import RunPosture
from .signals import Signal


# ─── Helpers ───────────────────────────────────────────────────────────────

def _fmt_millions(v: float) -> str:
    return f"${v / 1_000_000:.2f}M"


def _fmt_thousands(v: float) -> str:
    return f"${v / 1_000:.0f}K"


def estimate_cross_sell_upside(
    gap_count: int, target_ltm: float, target_dealers: int
) -> tuple[float, float]:
    """Returns (low, high) directional upside estimate."""
    per_dealer = target_ltm / max(target_dealers, 1)
    return (gap_count * per_dealer * 0.3, gap_count * per_dealer * 0.5)


def estimate_return_rate_lever(
    new_dealers: int, avg_first_year_rev: float
) -> tuple[float, float]:
    """Returns (per_5pt_full_base, per_5pt_addressable)."""
    full = new_dealers * avg_first_year_rev * 0.05
    return (full, full * 0.5)


# ─── Slot A: Hero ──────────────────────────────────────────────────────────

def build_hero_bundle(
    posture: RunPosture,
    top_signals: list[Signal],
    gather: GatherBundle,
) -> dict:
    signals_slice = top_signals[:7]
    signal_dicts = [
        {
            "kind": s.kind,
            "headline": s.headline,
            "dollar_impact": s.dollar_impact,
            "context": s.context,
        }
        for s in signals_slice
    ]

    # P0-1: `lapsed` (Q-DEALER-COHORT) is the ONE client-facing "went dark"
    # count. It is load-bearing — §9's dealer flow only reconciles with it
    # (hfg: 2,504 - 1,080 + 998 = 2,422). `nrr.fully_churned_custs` measures a
    # near-synonym on a different denominator (the invoiced-dollar cohort,
    # 2,499 not 2,504) and rendered as the same English claim, so hfg shipped
    # "1,075 prior-year accounts went dark" in §1 and "1,080 dealers ordered
    # nothing this year" in §9. Both were right; the report was not. It is
    # withheld from the bundle so prose cannot cite it at all.
    dealers_facts: dict = {}
    if gather.dealers:
        dealers_facts = {
            "same_base_lift_pct": gather.dealers.same_base_lift_pct,
            "returning": gather.dealers.returning,
            "second_year_return_rate": gather.dealers.second_year_return_rate,
            "new_dealers": gather.dealers.new_dealers,
            "lapsed": gather.dealers.lapsed,
            "active_prior_ltm": gather.dealers.active_prior_ltm,
        }

    nrr_facts: dict = {}
    if gather.nrr:
        nrr_facts = {
            "nrr_pct": gather.nrr.nrr_pct,
            "expansion_dollars": gather.nrr.expansion_dollars,
            "contraction_dollars": gather.nrr.contraction_dollars,
        }

    total_at_risk_ltm = sum(a.ltm_rev for a in gather.decay)

    # Platform facts (feature enablement) — included when available so Mode-2 / thin-data
    # prose can cite enrollment counts, feature flags, and smart stack depth.
    platform_facts: dict = {}
    if gather.feature_enablement:
        fe = gather.feature_enablement
        platform_facts = {
            "enrollment_count": fe.enrollment_count,
            "smart_stack_count": fe.smart_stack_count,
            "online_ordering": fe.enable_online_ordering,
            "online_catalog": fe.enable_online_catalog,
            "portal_order_count": fe.portal_order_count,
        }

    facts = {
        "posture": {
            "inv_ltm_net": posture.inv_ltm_net,
            "n_inv_ltm": posture.n_inv_ltm,
            "report_through_date": posture.report_through_date,
            "ecat_ltm_confirmed_gmv": posture.ecat_ltm_confirmed_gmv,
            "ecat_pct_of_invoiced": posture.ecat_pct_of_invoiced,
            "report_mode": posture.report_mode,
        },
        "top_signals": signal_dicts,
        "dealers": dealers_facts,
        "nrr": nrr_facts,
        "decay_summary": {
            "total_at_risk_ltm": total_at_risk_ltm,
            "count": len(gather.decay),
        },
        "platform": platform_facts,
    }

    # Derived facts
    same_dealer_spend_ratio: Optional[float] = None
    if gather.dealers and gather.dealers.same_base_lift_pct is not None:
        same_dealer_spend_ratio = round(1 + gather.dealers.same_base_lift_pct / 100, 2)

    non_house_reps = [r for r in gather.reps if not r.is_house and r.yoy_pct is not None]
    non_house_reps.sort(key=lambda r: r.ltm_invoiced, reverse=True)
    top_rep_yoy_range = ""
    if len(non_house_reps) >= 2:
        top3 = non_house_reps[:3]
        yoys = [r.yoy_pct for r in top3 if r.yoy_pct is not None]
        if yoys:
            top_rep_yoy_range = f"{min(yoys):+.0f}% to {max(yoys):+.0f}%"

    derived_facts = {
        "same_dealer_spend_ratio": same_dealer_spend_ratio,
        "at_risk_total_formatted": _fmt_millions(total_at_risk_ltm),
        "top_rep_yoy_range": top_rep_yoy_range,
        "watchlist_count": len(gather.decay),
    }

    return {"facts": facts, "derived_facts": derived_facts}


# ─── Slot B: Talking Points ───────────────────────────────────────────────

def build_talking_points_bundle(
    outreach_list: list[AccountDecay],
    posture: RunPosture,
    profile_text: str,
) -> dict:
    all_sorted = sorted(outreach_list, key=lambda a: a.ltm_rev, reverse=True)

    accounts = []
    for idx, acct in enumerate(outreach_list):
        rank = next(
            (i + 1 for i, a in enumerate(all_sorted) if a.bill_to_number == acct.bill_to_number),
            idx + 1,
        )

        # pace_description
        if acct.prior_6mo > 0:
            pace = acct.recent_6mo / acct.prior_6mo
        else:
            pace = 1.0
        if pace < 0.5:
            pace_description = "collapsed"
        elif pace < 0.7:
            pct_down = int((1 - pace) * 100)
            pace_description = f"down {pct_down}% in six months"
        elif acct.is_cadence_cliff:
            pace_description = "skipped a beat"
        else:
            pace_description = f"down {int((1 - pace) * 100)}% in six months" if pace < 1.0 else "flat or growing"

        # gap_multiple
        gap_multiple = ""
        if acct.mean_order_gap_days > 0:
            gap_multiple = f"{acct.days_silent / acct.mean_order_gap_days:.1f}x their normal gap"

        # share_of_total
        share_of_total = f"#{rank} account"

        # yoy_direction
        yoy_direction = "growing" if (acct.recent_vs_prior_pct or 0) > 0 else "declining"

        entry_facts = {
            "bill_to_name": acct.bill_to_name,
            "rep_label": acct.rep_label,
            "ltm_rev": acct.ltm_rev,
            "recent_6mo": acct.recent_6mo,
            "prior_6mo": acct.prior_6mo,
            "recent_vs_prior_pct": acct.recent_vs_prior_pct,
            "days_silent": acct.days_silent,
            "mean_order_gap_days": acct.mean_order_gap_days,
            "lifetime_invoices": acct.lifetime_invoices,
            "is_real_decline": acct.is_real_decline,
            "is_cadence_cliff": acct.is_cadence_cliff,
        }
        entry_derived = {
            "pace_description": pace_description,
            "share_of_total": share_of_total,
            "gap_multiple": gap_multiple,
            "yoy_direction": yoy_direction,
        }
        accounts.append({"facts": entry_facts, "derived_facts": entry_derived})

    return {
        "accounts": accounts,
        "posture_inv_ltm_net": posture.inv_ltm_net,
        "account_count": len(outreach_list),
    }


# ─── Slot C: Coaching Cards ──────────────────────────────────────────────

def build_coaching_bundle(
    card_reps: list[RepRisk],
    decay: list[AccountDecay],
    posture: RunPosture,
) -> dict:
    cards = []
    for rep in card_reps[:5]:
        rep_decay = [
            a for a in decay
            if a.rep_number == rep.rep_number
        ]
        rep_decay.sort(key=lambda a: a.ltm_rev, reverse=True)
        top3 = rep_decay[:3]

        account_entries = []
        for a in top3:
            account_entries.append({
                "bill_to_name": a.bill_to_name,
                "ltm_rev": a.ltm_rev,
                "recent_6mo": a.recent_6mo,
                "prior_6mo": a.prior_6mo,
                "recent_vs_prior_pct": a.recent_vs_prior_pct,
                "days_silent": a.days_silent,
                "is_real_decline": a.is_real_decline,
                "is_cadence_cliff": a.is_cadence_cliff,
            })

        card_facts = {
            "rep_name_tier2": rep.rep_name_tier2,
            "dollars_at_risk": rep.dollars_at_risk,
            "accounts_at_risk": rep.accounts_at_risk,
            "leak_pct": rep.leak_pct,
            "top_accounts": account_entries,
        }

        # Derived facts from top account
        card_derived: dict = {}
        if top3:
            top_acct = top3[0]
            decay_dollars = top_acct.prior_6mo - top_acct.recent_6mo

            # Three-way beat classification: cliff (cadence skip) / decline (hard slope) /
            # growing (account expanded) / mild softening (down but below is_real_decline threshold).
            if top_acct.is_cadence_cliff:
                _bsl = "beat-skip, not decline"
            elif top_acct.is_real_decline:
                _bsl = "real decline"
            elif top_acct.recent_6mo >= top_acct.prior_6mo:
                _bsl = "growing"
            else:
                _bsl = "mild softening"
            card_derived["beat_skip_label"] = _bsl
            card_derived["decay_dollars"] = decay_dollars

            # top_account_share_of_risk only makes sense when the account actually declined.
            # Use _fmt_thousands (divides by 1 000, adds K) — values are raw dollars.
            if decay_dollars > 0 and rep.dollars_at_risk > 0:
                card_derived["top_account_share_of_risk"] = (
                    f"{_fmt_thousands(decay_dollars)} of {_fmt_thousands(rep.dollars_at_risk)}"
                )
            else:
                card_derived["top_account_share_of_risk"] = None  # growing; no "share of risk" framing

        cards.append({"facts": card_facts, "derived_facts": card_derived})

    return {"cards": cards, "card_count": len(card_reps[:5])}


# ─── Slot D: Play Framing ─────────────────────────────────────────────────

def play_upside_ceiling(play: dict, gather: GatherBundle) -> float:
    """The largest dollar figure this play is entitled to claim.

    S1: "Do this month" had NO materiality floor at all, so hfg — a $41.2M
    company — shipped a single play worth $7K-$12K off a ONE-dealer overlap:
    0.02% of the year presented as the month's work. Each play type is scored
    on the same basis the section itself renders, so the floor and the copy
    cannot disagree.
    """
    ptype = play.get("type")
    if ptype == "cross_sell":
        if not play.get("gap_available") or not play.get("gap_count"):
            return 0.0
        _, high = estimate_cross_sell_upside(
            int(play.get("gap_count") or 0),
            float(play.get("target_ltm") or 0.0),
            int(play.get("target_dealers") or 0),
        )
        return high
    if ptype == "retention":
        rate = play.get("second_year_return_rate")
        if rate is None:
            return 0.0
        return float(play.get("one_time_rev") or 0.0) * (1.0 - float(rate))
    if ptype == "pricing":
        return float(play.get("total_leak_dollars") or 0.0)
    return 0.0


def build_plays_from_gather(
    gather: GatherBundle,
    posture: RunPosture,
    fired_signals: list[Signal] | None = None,
    thresholds=None,
) -> list[dict]:
    """Select up to three plays from fired signals, ranked by ``Signal.rank``.

    A play that cannot clear the org's own materiality floor is DROPPED, not
    padded — "no play qualified this month" is a legitimate output (the section
    is optional in `_base.md.j2` and is not a smoke_check-required heading).
    """
    from .signals import resolve_thresholds

    if fired_signals is None:
        from .signals import detect_all

        fired_signals = detect_all(gather, posture)
    t = thresholds or resolve_thresholds(posture, gather)

    eligible = {
        "cross_sell_pocket",
        "second_year_gap",
        "leakage_discipline",
        "new_line_takeoff",
        "growth_pocket",
    }
    ranked = sorted(
        (signal for signal in fired_signals if signal.kind in eligible),
        key=lambda signal: signal.rank,
        reverse=True,
    )

    plays: list[dict] = []
    selected_types: set[str] = set()
    for signal in ranked:
        if signal.kind in {
            "cross_sell_pocket",
            "new_line_takeoff",
            "growth_pocket",
        }:
            if "cross_sell" in selected_types or not (
                gather.products and gather.families
            ):
                continue
            family_name = str(signal.context.get("family") or "")
            target = next(
                (
                    family
                    for family in gather.families
                    if family.family_label == family_name
                ),
                gather.families[0],
            )
            gap = gather.cross_sell_gap
            anchor = (
                gap.anchor_item
                if gap and gap.anchor_item
                else gather.products[0].display_description
            )
            from .outreach_screen import looks_like_code

            title = (
                f"{target.family_label} cross-sell"
                # P0-8: the code test reads the RAW field. hfg's top item is an
                # ERP spec string, and normalising it into a readable label must
                # not turn "Axis cross-sell" into a 60-character play heading.
                if looks_like_code(gather.products[0].description)
                else (
                    f"{gather.products[0].display_description.strip()} "
                    f"→ {target.family_label} cross-sell"
                )
            )
            play = {
                "type": "cross_sell",
                "title": title,
                "signal_kind": signal.kind,
                "signal_rank": signal.rank,
                "anchor_item": anchor,
                "anchor_dealers": gather.products[0].dealers,
                "target_family": target.family_label,
                "target_ltm": target.ltm_revenue,
                "target_yoy": target.yoy_pct,
                "target_dealers": target.dealer_count,
                "gap_available": gap is not None,
                "gap_count": gap.count if gap is not None else None,
            }
            selected_types.add("cross_sell")
        elif signal.kind == "second_year_gap":
            if "retention" in selected_types or not gather.dealers:
                continue
            play = {
                "type": "retention",
                "title": "A second-order push for new dealers",
                "signal_kind": signal.kind,
                "signal_rank": signal.rank,
                "new_dealers": gather.dealers.new_dealers,
                "returning": gather.dealers.returning,
                "second_year_return_rate": gather.dealers.second_year_return_rate,
                "one_time_rev": gather.dealers.one_time_rev,
                "active_ltm": gather.dealers.active_ltm,
            }
            selected_types.add("retention")
        else:
            if "pricing" in selected_types or not gather.rep_risks:
                continue
            leak_rows = [
                risk for risk in gather.rep_risks if risk.leak_pct is not None
            ]
            if not leak_rows or max(risk.leak_pct or 0 for risk in leak_rows) <= 10:
                continue
            top_leak = max(leak_rows, key=lambda risk: risk.leak_pct or 0)
            bottom_leak = min(leak_rows, key=lambda risk: risk.leak_pct or 0)
            play = {
                "type": "pricing",
                "title": "Pricing / discipline review",
                "signal_kind": signal.kind,
                "signal_rank": signal.rank,
                "top_leak_rep": top_leak.rep_name_tier2
                or f"rep {top_leak.rep_number}",
                "top_leak_pct": top_leak.leak_pct,
                "bottom_leak_pct": bottom_leak.leak_pct,
                "total_leak_dollars": sum(
                    risk.dollars_at_risk for risk in gather.rep_risks
                ),
                "inv_ltm_net": posture.inv_ltm_net,
            }
            selected_types.add("pricing")

        if play_upside_ceiling(play, gather) < t.play_min_upside:
            # Dropped on materiality. `selected_types` still carries the type so
            # a second, smaller play of the same kind cannot backfill the slot.
            continue
        plays.append(play)
        if len(plays) == 3:
            break

    return plays


def index_play_framing(
    plays: list[dict], play_framing: list[str] | None
) -> dict[str, str]:
    """Map slot-D bodies onto play type. Positional zip — validator enforces
    that body i matches play i's type, so the template never injects a
    leakage paragraph under a cross-sell title.
    """
    if not plays or not play_framing:
        return {}
    indexed: dict[str, str] = {}
    for play, body in zip(plays, play_framing):
        if (
            play["type"] == "cross_sell"
            and (
                not play.get("gap_available")
                or not play.get("gap_count")
            )
        ):
            continue
        indexed[play["type"]] = body
    return indexed


def build_play_framing_bundle(
    plays: list[dict],
    gather: GatherBundle,
    posture: RunPosture,
) -> dict:
    entries = []
    for play in plays[:3]:
        ptype = play["type"]

        if ptype == "cross_sell":
            gap_count = play["gap_count"]
            target_ltm = play["target_ltm"]
            target_dealers = play["target_dealers"]
            anchor_dealers = play["anchor_dealers"]

            entry_facts = {
                "anchor_item": play["anchor_item"],
                "anchor_dealers": anchor_dealers,
                "target_family": play["target_family"],
                "target_ltm": target_ltm,
                "target_yoy": play["target_yoy"],
                "target_dealers": target_dealers,
                "gap_available": play["gap_available"],
                "gap_count": gap_count,
            }
            if gap_count is not None and gap_count > 0:
                low, high = estimate_cross_sell_upside(
                    gap_count, target_ltm, target_dealers
                )
                entry_derived = {
                    "upside_range": (
                        f"{_fmt_thousands(low)}-{_fmt_thousands(high)} "
                        "DIRECTIONAL"
                    ),
                    "gap_fraction": f"{gap_count} of {anchor_dealers}",
                }
            else:
                entry_derived = {}

        elif ptype == "retention":
            new_dealers = play["new_dealers"]
            one_time_rev = play["one_time_rev"]
            avg_first_year_rev = one_time_rev / max(new_dealers, 1)
            per_5pt, addressable = estimate_return_rate_lever(new_dealers, avg_first_year_rev)

            entry_facts = {
                "new_dealers": new_dealers,
                "returning": play["returning"],
                "second_year_return_rate": play["second_year_return_rate"],
                "one_time_rev": one_time_rev,
                "active_ltm": play["active_ltm"],
            }
            entry_derived = {
                "per_5pt_lever": per_5pt,
                "addressable_subset_lever": addressable,
                "return_rate_pct": play["second_year_return_rate"] * 100,
            }

        elif ptype == "pricing":
            inv_ltm_net = play["inv_ltm_net"]
            total_leak_dollars = play["total_leak_dollars"]
            top_leak_pct = play["top_leak_pct"]
            bottom_leak_pct = play["bottom_leak_pct"]

            entry_facts = {
                "top_leak_rep": play["top_leak_rep"],
                "top_leak_pct": top_leak_pct,
                "bottom_leak_pct": bottom_leak_pct,
                "total_leak_dollars": total_leak_dollars,
                "inv_ltm_net": inv_ltm_net,
            }
            entry_derived = {
                "leak_rate_org_pct": total_leak_dollars / max(inv_ltm_net, 1) * 100,
                "spread_formatted": f"{bottom_leak_pct:.1f}% to {top_leak_pct:.1f}%",
            }
        else:
            entry_facts = play
            entry_derived = {}

        entries.append({
            "type": ptype,
            "facts": entry_facts,
            "derived_facts": entry_derived,
        })

    return {"plays": entries, "play_count": len(entries)}


# ─── Slot E: Growth Connective ────────────────────────────────────────────

def build_growth_connective_bundle(
    gather: GatherBundle,
    posture: RunPosture,
) -> dict:
    # Layer 1: NRR + dealer base dynamics
    layer1_facts: dict = {}
    layer1_derived: dict = {}
    if gather.nrr:
        layer1_facts["nrr_pct"] = gather.nrr.nrr_pct
        layer1_facts["expansion_dollars"] = gather.nrr.expansion_dollars
        layer1_facts["contraction_dollars"] = gather.nrr.contraction_dollars
    if gather.dealers:
        layer1_facts["returning"] = gather.dealers.returning
        layer1_facts["same_base_lift_pct"] = gather.dealers.same_base_lift_pct
        if gather.dealers.same_base_lift_pct is not None:
            ratio = 1 + gather.dealers.same_base_lift_pct / 100
            layer1_derived["spend_ratio"] = f"${ratio:.2f} for every $1 last year"

    # Layer 2: top named family
    layer2_facts: dict = {}
    layer2_derived: dict = {}
    named = gather.named_families
    if named:
        top_fam = named[0]
        layer2_facts = {
            "family_label": top_fam.family_label,
            "ltm_revenue": top_fam.ltm_revenue,
            "yoy_pct": top_fam.yoy_pct,
            "dealer_count": top_fam.dealer_count,
            "sku_count": top_fam.sku_count,
        }
        if posture.inv_ltm_net > 0:
            share = top_fam.ltm_revenue / posture.inv_ltm_net * 100
            layer2_derived["family_share_of_total"] = f"{share:.1f}%"
    else:
        layer2_facts["no_branded_family"] = True

    # Layer 3: top 3 non-house reps
    non_house = [r for r in gather.reps if not r.is_house]
    non_house.sort(key=lambda r: r.ltm_invoiced, reverse=True)
    top3_reps = non_house[:3]

    layer3_facts = [
        {
            "rep_label": r.rep_label,
            "ltm_invoiced": r.ltm_invoiced,
            "yoy_pct": r.yoy_pct,
            "customer_count": r.customer_count,
        }
        for r in top3_reps
    ]

    layer3_derived: dict = {}
    if top3_reps and posture.inv_ltm_net > 0:
        layer3_derived["top_rep_share"] = (
            top3_reps[0].ltm_invoiced / posture.inv_ltm_net * 100
        )

    return {
        "layer1": {"facts": layer1_facts, "derived_facts": layer1_derived},
        "layer2": {"facts": layer2_facts, "derived_facts": layer2_derived},
        "layer3": {"facts": layer3_facts, "derived_facts": layer3_derived},
    }


# ─── Slot F: Outreach Framing ─────────────────────────────────────────────

def build_outreach_framing_bundle(outreach_list: list[AccountDecay]) -> dict:
    rows = []
    decline_count = 0
    beat_skip_count = 0

    for acct in outreach_list:
        rows.append({
            "account_name": acct.bill_to_name,
            "is_real_decline": acct.is_real_decline,
            "is_cadence_cliff": acct.is_cadence_cliff,
        })
        if acct.is_real_decline:
            decline_count += 1
        if acct.is_cadence_cliff:
            beat_skip_count += 1

    decline_names = [
        acct.bill_to_name for acct in outreach_list if acct.is_real_decline
    ][:3]
    beat_skip_names = [
        acct.bill_to_name for acct in outreach_list if acct.is_cadence_cliff
    ][:3]

    if decline_count > 0 and beat_skip_count > 0:
        framing_hint = "Two different conversations — declines vs beat-skips"
    elif beat_skip_count > 0:
        framing_hint = "All beat-skips — confirm calls, not rescue calls"
    elif decline_count > 0:
        framing_hint = "All declines — unified approach"
    else:
        # No at-risk accounts on the outreach list (e.g. Mode 2 / thin-data orgs).
        framing_hint = None

    return {
        "facts": {
            "rows": rows,
            "decline_count": decline_count,
            "beat_skip_count": beat_skip_count,
        },
        "derived_facts": {
            "decline_names": decline_names,
            "beat_skip_names": beat_skip_names,
            "framing_hint": framing_hint,
        },
    }
