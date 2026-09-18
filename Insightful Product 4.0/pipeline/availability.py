"""Adaptive report-section availability.

Availability is derived from the post-screen gather bundle. Templates consume
this map; they do not infer a Mode-1/Sarreid-shaped report from commerce mode.
"""
from __future__ import annotations

from dataclasses import dataclass

from .gather import GatherBundle
from .preflight import RunPosture


def outreach_mix(gather: GatherBundle) -> str:
    """Classify the post-screen call list for footer dispatch."""
    rows = gather.outreach_list
    if not rows:
        return "empty"
    from .gather import account_needs_a_call

    decline_count = sum(1 for row in rows if account_needs_a_call(row))
    if decline_count == len(rows):
        return "all_decline"
    if decline_count == 0:
        return "all_reinforce"
    return "mixed"


@dataclass(frozen=True)
class SectionAvailability:
    hero: bool
    methodology: bool
    this_week: bool
    this_month: bool
    layer_1: bool
    layer_2: bool
    layer_3: bool
    team: bool
    activity_floor: bool
    watchlist: bool
    products: bool
    dealers: bool
    invoiced_dealers: bool
    channels: bool
    erp_unlock: bool

    @property
    def layers(self) -> bool:
        return self.layer_1 or self.layer_2 or self.layer_3

    @property
    def team_section(self) -> bool:
        return self.team or self.activity_floor


def build_availability(
    gather: GatherBundle,
    posture: RunPosture,
    plays: list[dict],
) -> SectionAvailability:
    """Return the section menu supported by this org's actual data."""
    has_invoiced = posture.inv_ltm_net > 0
    has_prior_same_dealer = bool(
        has_invoiced
        and (
            (
                gather.nrr
                and gather.nrr.prior_cohort_custs > 0
                and gather.nrr.prior_base > 0
            )
            or (
                gather.dealers
                and gather.dealers.active_prior_ltm > 0
                and gather.dealers.returning > 0
            )
        )
    )
    activity_floor = bool(
        (gather.rep_activity and gather.rep_activity.any_data)
        or (gather.rep_quote_discipline and gather.rep_quote_discipline.any_data)
        or (
            posture.commerce_confidence != "NONE"
            and gather.rep_coverage
            and gather.rep_coverage.any_data
        )
    )
    invoiced_dealers = bool(
        has_invoiced and gather.dealers and gather.dealers.active_ltm > 0
    )
    has_account_coverage = bool(
        gather.rep_coverage and gather.rep_coverage.any_data
    )

    return SectionAvailability(
        hero=True,
        methodology=True,
        this_week=bool(gather.outreach_list),
        this_month=bool(plays),
        layer_1=has_prior_same_dealer,
        layer_2=bool(gather.families or gather.products),
        layer_3=bool(
            has_invoiced
            and posture.rep_identity_tier in (1, 2)
            and gather.reps
        ),
        team=bool(gather.rep_risks),
        activity_floor=activity_floor,
        # The watchlist is part of the required report shape (smoke_check
        # enforces it), so it renders whenever there is any risk at all —
        # not only when a tail exists beyond the call list.
        watchlist=bool(gather.watchlist),
        products=bool(gather.products or gather.families),
        dealers=invoiced_dealers or has_account_coverage,
        invoiced_dealers=invoiced_dealers,
        channels=bool(
            posture.distinct_origins > 1
            or posture.inv_ltm_net > 0
            or posture.ecat_ltm_confirmed_gmv > 0
        ),
        erp_unlock=posture.commerce_confidence == "NONE",
    )
