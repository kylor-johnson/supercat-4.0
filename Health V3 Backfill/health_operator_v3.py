#!/usr/bin/env python3
"""
Health V3 — Operator

Reads the V3 README scoring spec, queries Postgres + BigQuery + the MAL CSV,
scores all 4 dimensions per org, applies the §5.1 ghost-account override,
and emits one CSV row per scored org.

Usage:
    python health_operator_v3.py \\
        --mal "/path/to/master_account_list.csv" \\
        --score-date 2026-05-11 \\
        --output-dir "/path/to/Health V3/runs"
    python health_operator_v3.py --mal ... --single-org tam --dry-run

Connections:
    Postgres: DATABASE_URL or PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD
    BigQuery: standard application-default credentials (gcloud auth)
"""

import argparse
import ast
import csv
import os
import re
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

BQ_PROJECT = "supercat-data-pipeline"

INTERNAL_DOMAINS = {
    "supercatsolutions.com", "lojic.com", "railsfever.com",
    "samedis.com", "jimmythrasher.com", "upwardtechnologies.com",
}

GENERIC_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "aol.com", "outlook.com",
    "icloud.com", "comcast.net", "msn.com", "me.com", "att.net",
    "live.com", "sbcglobal.net", "verizon.net", "bellsouth.net",
    "charter.net", "cox.net", "earthlink.net", "ymail.com", "mac.com",
    "protonmail.com",
}

# §1 Engagement bands
LOGIN_BANDS = [(3000, 100), (1000, 88), (500, 75), (200, 60), (50, 40), (1, 20), (0, 0)]
RATIO_BANDS = [(0.90, 100), (0.75, 82), (0.50, 65), (0.25, 45), (0.01, 20), (0, 0)]
VELOCITY_BANDS = [(1.5, 100), (0.75, 90), (0.50, 60), (0.25, 30), (0.0, 10)]
# velocity_ratio > 0 → minimum 10; velocity_ratio = 0 or undefined → 0

# §4 Catalog completeness step ladder (per spec §4 sub-signal 1)
CATALOG_LADDER = [(0.90, 100), (0.60, 60), (0, 20)]

# §4 Data freshness staleness ratio
FRESHNESS_BANDS = [(1.0, 100), (1.5, 80), (2.5, 50), (4.0, 20)]  # > 4.0 → 0

# §4 Health bands
HEALTH_BANDS = [(80, "Thriving"), (60, "Healthy"), (40, "Watch"), (20, "At Risk"), (0, "Critical")]

# Import types excluded from health scoring due to known parser artifacts (100% error rate)
EXCLUDED_IMPORT_TYPES_HEALTH = frozenset({
    "Multifile Import",
    "Import File Processing",
    "Product Image Downloads",
})

# §5.1 Ghost account override
GHOST_ARR_THRESHOLD = 5000
GHOST_CAP = 20

# §5.2 Behavioral floor override
BEHAVIORAL_FLOOR_CAP = 40.0

NEW_ORG_DAYS = 90

# Bundle normalization (MAL stack column → canonical)
BUNDLE_MAP = {
    "iPad-only": "iPad-only", "iPad+Catalog": "iPad+Catalog",
    "iPad+Catalog+Cart": "iPad+Catalog+Cart",
    "iPad+Catalog+Portal": "iPad+Catalog+Portal", "Full": "Full",
    "Full (Cart+Portal)": "Full",
}

# Bundles where enabled_users is inflated by B2B portal customer accounts
INFLATED_DENOM_BUNDLES = frozenset({"Full", "iPad+Catalog+Cart"})


# ---------------------------------------------------------------------------
# NARRATIVE HELPERS (V3.1 — interpretive layer)
# ---------------------------------------------------------------------------

def _vel_label(velocity_ratio):
    """Map a velocity ratio to a plain-English label for use in narratives."""
    if velocity_ratio is None:
        return None
    if velocity_ratio >= 1.5:
        return "accelerating"
    if velocity_ratio >= 0.75:
        return "holding steady"
    if velocity_ratio >= 0.50:
        return "cooling off — worth monitoring"
    return "sharp deceleration — usage has dropped significantly from baseline"


def _build_engagement_narrative(logins, active, enabled, ratio, velocity_ratio,
                                 login_score, ratio_score, velocity_score,
                                 denom_note, score):
    ratio_pct = int(round(ratio * 100))
    vel = _vel_label(velocity_ratio)
    if velocity_ratio is not None:
        vel_detail = f"pace {vel} at {velocity_ratio:.1f}x baseline"
    else:
        vel_detail = "pace: insufficient history"

    denom_suffix = ""
    if denom_note and "inflated" in denom_note:
        denom_suffix = (" Rep headcount estimated from annual login history "
                        "(portal accounts excluded from denominator).")
    elif denom_note:
        denom_suffix = " (headcount from annual active-user fallback)."

    # vel_label_phrase: "holding steady at 1.1x" — for use inside sentences
    if velocity_ratio is not None:
        vel_phrase = f"{vel} at {velocity_ratio:.1f}x baseline"
    else:
        vel_phrase = "insufficient history"

    if score >= 75:
        narrative = (f"{logins:,} logins in 90 days — solid activity for this team size, "
                     f"with {active} of {enabled} reps logging in regularly "
                     f"and pace {vel_phrase}. No engagement concern here.")
    elif score >= 50:
        weakest = min(
            [("login volume", login_score),
             ("team penetration", ratio_score),
             ("velocity", velocity_score)],
            key=lambda x: x[1],
        )[0]
        if weakest == "login volume":
            narrative = (f"{logins:,} logins in 90 days is on the lower side for "
                         f"{enabled} enabled reps — {active} of {enabled} ({ratio_pct}%) "
                         f"are active, but session depth is limited. "
                         f"Pace is {vel_phrase}.")
        elif weakest == "team penetration":
            narrative = (f"{logins:,} logins in 90 days, but only {active} of {enabled} reps "
                         f"({ratio_pct}%) have logged in this quarter — most of the team isn't "
                         f"engaged. Pace is {vel_phrase}.")
        else:
            narrative = (f"{logins:,} logins in 90 days from {active} of {enabled} reps "
                         f"({ratio_pct}% active), but pace is {vel_phrase} — "
                         f"worth monitoring for continued fade.")
    else:
        if logins == 0:
            return ("Zero logins in 90 days. No active usage this quarter — "
                    "treat as a ghost-account candidate if ARR ≥ $5K.")
        is_fade = (velocity_ratio is not None and velocity_ratio < 0.50 and logins > 100)
        is_low_pen = ratio_pct <= 20
        if is_fade:
            narrative = (f"{logins:,} logins in 90 days but pace has {vel} ({velocity_ratio:.1f}x baseline) — "
                         f"clear dropoff from historical baseline. "
                         f"Only {active} of {enabled} reps ({ratio_pct}%) are still active. "
                         f"CS should find out what changed and re-engage the team.")
        elif is_low_pen:
            narrative = (f"Only {logins:,} logins in 90 days from just {active} of {enabled} "
                         f"reps ({ratio_pct}%) — most of the team is not using the app this quarter. "
                         f"Prioritize an engagement call to identify adoption barriers.")
        else:
            narrative = (f"Low engagement: {logins:,} logins in 90 days from "
                         f"{active} of {enabled} reps ({ratio_pct}% active), pace is {vel_phrase}. "
                         f"Below-threshold activity across the board — proactive outreach warranted.")
    return narrative + denom_suffix


def _build_adoption_narrative(score, used_count, applicable_count, unused):
    if score >= 100:
        return "Using every configured feature — nothing unused."

    feature_msgs = []
    for f in unused:
        if f == "Sales Data":
            feature_msgs.append(
                "Sales Data is configured but no import has run in 90 days — "
                "check whether the feed is broken or the integration was never fully set up"
            )
        elif f == "Sales Portal":
            feature_msgs.append(
                "Sales Portal is enabled but reps haven't opened it in 90 days — "
                "consider a rep training touchpoint"
            )
        elif f == "Smart Stacks":
            feature_msgs.append(
                "Smart Stacks haven't been used — a CS demo of the feature could unlock this"
            )
        elif f == "Sharing/quoting":
            feature_msgs.append(
                "Reps aren't using sharing or quoting in the field — "
                "zero email drafts in 90 days"
            )
        elif f == "Inventory Management":
            feature_msgs.append(
                "Inventory Management feed has gone quiet — no imports in 90 days"
            )
        elif f == "eCat Online Catalog":
            feature_msgs.append(
                "eCat Online Catalog is enabled but no portal traffic in 90 days"
            )
        elif f == "Online Ordering":
            feature_msgs.append(
                "Online Ordering (B2B Cart) is enabled but no portal orders in 90 days"
            )
        else:
            feature_msgs.append(f"{f} is configured but not being used")

    if score >= 75:
        gap_text = feature_msgs[0] if feature_msgs else f"{', '.join(unused)} not in use"
        # Capitalize first char only if it isn't a brand name already cased correctly
        cap_text = gap_text[0].upper() + gap_text[1:]
        return (f"Using {used_count} of {applicable_count} applicable features — mostly adopted. "
                f"{cap_text}.")
    else:
        is_config_issue = any(f in unused for f in ["Sales Data", "Inventory Management"])
        is_coaching_opp = any(f in unused for f in
                               ["Smart Stacks", "Sharing/quoting", "Sales Portal",
                                "eCat Online Catalog", "Online Ordering"])
        # Preserve brand-name casing (eCat, iPad) — don't force-capitalize first char
        top_msgs = "; ".join(feature_msgs)
        if is_config_issue and is_coaching_opp:
            action = "investigate the feed configuration and schedule a rep coaching session"
        elif is_config_issue:
            action = "check the integration setup — this may be a broken feed, not a usage gap"
        else:
            action = "schedule a rep coaching session to build these habits"
        return (f"Using {used_count} of {applicable_count} applicable features — "
                f"real breadth gaps here. {top_msgs}. CS should {action}.")


def _build_value_delivery_narrative(score, achieved_names, gap_names, applicable_count,
                                     ipad_orders_90d, mp_share_count, portal_orders_90d,
                                     inv_runs_90d):
    if score >= 100:
        return "All configured channels are producing outcomes."

    def _gap_detail(g):
        if g == "Order volume (iPad)":
            if ipad_orders_90d == 0:
                return "No iPad orders submitted in 90 days — reps are not converting activity into orders"
            if ipad_orders_90d < 5:
                return (f"No meaningful iPad order activity — only "
                        f"{ipad_orders_90d} order{'s' if ipad_orders_90d != 1 else ''} in 90 days "
                        f"(threshold is 10)")
            return (f"iPad order volume close but short — "
                    f"{ipad_orders_90d} orders in 90 days (threshold is 10, roughly one per week)")
        if g == "Sharing activity":
            return (f"sharing/quoting near zero "
                    f"({mp_share_count} event{'s' if mp_share_count != 1 else ''} in 90d)")
        if g == "Online catalog active":
            return "online catalog is enabled but no portal traffic in 90d"
        if g == "Portal ordering":
            return "B2B Cart is configured but no portal orders in 90d"
        if g == "Sales Portal engagement":
            return "Sales Portal is configured but no portal orders in 90d"
        if g == "Inventory data flowing":
            return "inventory feed has gone silent — no imports in 90d"
        return f"{g} not producing outcomes"

    gap_details = [_gap_detail(g) for g in gap_names]
    achieved_count = len(achieved_names)

    if score >= 60:
        if len(gap_names) == 1 and gap_names[0] == "Sharing activity":
            return (f"{achieved_count} of {applicable_count} configured channels producing outcomes — "
                    f"reps are active but not using sharing/quoting in the field. "
                    f"A short demo of the share flow in the next QBR could move this.")
        gap_text = "; ".join(gap_details)
        cap_gap = gap_text[0].upper() + gap_text[1:] if gap_text else ""
        return (f"{achieved_count} of {applicable_count} configured channels producing outcomes. "
                f"Gap: {cap_gap}.")

    # score < 60 — most important narrative
    only_inv_active = (
        "Inventory data flowing" in achieved_names
        and achieved_count == 1
        and "Order volume (iPad)" in gap_names
        and "Sharing activity" in gap_names
    )
    if only_inv_active:
        order_word = "order" if ipad_orders_90d == 1 else "orders"
        event_word = "event" if mp_share_count == 1 else "events"
        return (f"Only inventory is flowing — iPad order volume ({ipad_orders_90d} {order_word}) "
                f"and sharing activity ({mp_share_count} {event_word}) are both near zero. "
                f"Reps appear to be logging in but not converting activity into outcomes. "
                f"CS should investigate whether reps are actively using the iPad in the field "
                f"or just checking catalogs.")
    gap_text = "; ".join(gap_details[:2])
    cap_gap = gap_text[0].upper() + gap_text[1:] if gap_text else "Multiple gaps present"
    return (f"Only {achieved_count} of {applicable_count} applicable channels are producing outcomes. "
            f"{cap_gap}. "
            f"CS should identify the highest-impact gap and address it in the next touchpoint.")


def _build_ops_narrative(score, cat_pct, cat_score, contract_pricing,
                          scoreable_imports, imp_score, fresh_score, stale_feeds, as_of):
    """stale_feeds: list of (import_type, staleness_ratio, days_since_last, mean_gap_days)
    as_of: datetime anchor for any "days ago" computations (the score_date), so cache-mode
    re-runs are deterministic. Must be passed in — no wall-clock fallback.
    """
    parts = []

    # Catalog sub-signal
    if cat_pct is not None:
        cat_pct_int = int(round(cat_pct * 100))
        cp_note = " (contract pricing — price check skipped)" if contract_pricing else ""
        if cat_score == 100:
            parts.append(f"catalog {cat_pct_int}% complete{cp_note}")
        elif cat_score == 60:
            parts.append(f"catalog {cat_pct_int}% complete{cp_note} — healthy but with room to improve")
        else:  # 20
            if cat_pct_int == 0:
                parts.append("catalog is empty — no products have complete data")
            else:
                parts.append(
                    f"catalog completeness at {cat_pct_int}%{cp_note} is a blocker for field use — "
                    f"reps are working with incomplete product data; flag for a catalog audit"
                )

    # Import health sub-signal
    if imp_score is not None:
        n_total = len(scoreable_imports)
        n_healthy = sum(1 for r in scoreable_imports if not r["last_run_had_error"])
        if imp_score >= 100:
            parts.append(f"all {n_total} import feed{'s' if n_total != 1 else ''} healthy")
        else:
            _now = as_of
            errored_parts = []
            for r in scoreable_imports:
                if r["last_run_had_error"]:
                    last_at = r.get("last_run_at")
                    if last_at is not None:
                        last_at = last_at.replace(tzinfo=None) if hasattr(last_at, "tzinfo") and last_at.tzinfo else last_at
                        days_ago = int((_now - last_at).total_seconds() / 86400)
                        if days_ago > 60:
                            errored_parts.append(f"{r['import_type']} ({days_ago}d ago)")
                        else:
                            errored_parts.append(r["import_type"])
                    else:
                        errored_parts.append(r["import_type"])
            errored_str = ", ".join(errored_parts)
            parts.append(
                f"{n_healthy} of {n_total} import feeds healthy; "
                f"{errored_str} last ran with errors"
            )

    # Freshness sub-signal
    if fresh_score is not None:
        if fresh_score >= 80:
            # Even if aggregate is healthy, surface any individual feed that is severely overdue
            outlier_feeds = [(name, ratio, days, gap) for name, ratio, days, gap in stale_feeds if ratio > 4.0]
            if outlier_feeds:
                worst_out = max(outlier_feeds, key=lambda x: x[1])
                o_name, _, o_days, o_gap = worst_out
                parts.append(
                    f"data feeds mostly on cadence — {o_name} is "
                    f"{int(round(o_days))}d overdue against a ~{int(round(o_gap))}d expected cadence and needs attention"
                )
            else:
                parts.append(f"data feeds running on cadence")
        elif stale_feeds:
            worst = max(stale_feeds, key=lambda x: x[1])
            feed_name, stale_ratio, days_since, mean_gap = worst
            days_r = int(round(days_since))
            gap_r = int(round(mean_gap))
            urgency = "critical" if stale_ratio > 4.0 else "declining"
            parts.append(
                f"data freshness {urgency} — the {feed_name} feed last ran {days_r}d ago "
                f"against a ~{gap_r}d expected cadence"
            )
            if fresh_score < 30 and score < 60:
                parts[-1] += " — escalate to ops"
        else:
            parts.append(f"data freshness score {fresh_score:.0f}")

    if not parts:
        return "No operational signals available."

    narrative = "; ".join(parts)
    narrative = narrative[0].upper() + narrative[1:] + "."

    if score >= 85:
        return narrative
    if score < 60 and any("blocker" in p or "errors" in p or "critical" in p for p in parts):
        return f"Ops concern — {narrative[0].lower()}{narrative[1:]}"
    return narrative


def _build_composite_narrative(org_name, score, band, eng_score, ado_score, val_score, ops_score,
                               bundle, arr, cohort_year):
    """Plain-English narrative for the composite score, readable by CS and
    exec audiences alike. Lead with the business situation; close with the
    implication or warranted action. Max 2 sentences per output.

    Ghost and behavioral-floor narratives are produced upstream in `main()`;
    this function is only called for normal accounts.

    Shape categories are checked top-to-bottom; first match wins. Anything
    that doesn't match a clean shape falls through to a mixed-profile fallback
    that names strongest/weakest dimensions and an action keyed off the band.
    """
    e = eng_score if eng_score is not None else 50.0
    a = ado_score if ado_score is not None else 50.0
    v = val_score if val_score is not None else 50.0
    o = ops_score if ops_score is not None else 50.0

    scored = {k: s for k, s in [
        ("engagement", eng_score), ("adoption", ado_score),
        ("value delivery", val_score), ("operational health", ops_score),
    ] if s is not None}

    if not scored:
        return (f"{org_name} has insufficient data to score any dimension this period. "
                "Verify the data pipeline before drawing any conclusions.")

    def _fmt(s):
        return f"{s:.0f}" if s is not None else "N/A"

    ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    top_dim, top_val = ranked[0]
    low_dim, low_val = ranked[-1]

    # -----------------------------------------------------------------------
    # Fix 3 — Value delivery = 0 outside the floor path. Name the absence of
    # outcomes explicitly rather than burying it in mixed-profile language.
    # -----------------------------------------------------------------------
    if val_score == 0:
        if band in ("Thriving", "Healthy"):
            tail = ("Investigate which channel was expected to fire and why it isn't — a single "
                    "fix may move the score materially.")
        elif band == "Watch":
            tail = ("Focus the next conversation on which channel was expected to convert activity "
                    "into orders, and what is blocking it.")
        else:
            tail = ("This needs an active recovery conversation — identify whether the gap is "
                    "technical (broken feed), commercial (no orders flowing), or behavioral "
                    "(reps not converting).")
        return (f"The platform isn't generating any measurable business outcomes for {org_name} — "
                f"no channel (orders, quotes, portal activity, or data flow) is currently producing "
                f"results. {tail}")

    # -----------------------------------------------------------------------
    # Shape 1 — all dimensions strong (>= 70). Three sub-shapes:
    #   1a — clean Thriving (score >= 90 AND min dim >= 80)
    #   1b — boundary Thriving (score 80-84) per Fix 2
    #   1b' — mixed-profile Thriving (score 85+ but a dim < 80) per Fix 2
    #   1c — all-strong Healthy
    # -----------------------------------------------------------------------
    if all(s >= 70 for s in scored.values()):
        min_val = min(scored.values())
        if band == "Thriving" and score >= 90 and min_val >= 80:
            return (f"{org_name} is performing well across the board — every dimension is at "
                    f"{_fmt(min_val)} or higher and the overall score of {_fmt(score)} reflects "
                    f"consistent strength rather than one area carrying the others. "
                    f"No action needed; monitor at standard cadence.")
        if band == "Thriving" and score < 85:
            return (f"{org_name} is in Thriving territory ({_fmt(score)}), but the score sits "
                    f"just above the Healthy cutoff — {low_dim} ({_fmt(low_val)}) is the relative "
                    f"weakness while {top_dim} ({_fmt(top_val)}) is doing the lifting. "
                    f"A focused check-in on {low_dim} would solidify the Thriving position "
                    f"before any drift sets in.")
        if band == "Thriving":
            return (f"{org_name} is performing well overall ({_fmt(score)}) — {low_dim} "
                    f"({_fmt(low_val)}) is the relative drag, but every dimension is in "
                    f"acceptable shape. Monitor at standard cadence.")
        # all-strong Healthy
        return (f"{org_name} is in solid shape — every dimension is at 70 or above and the "
                f"overall score of {_fmt(score)} sits in Healthy range. {low_dim.capitalize()} "
                f"({_fmt(low_val)}) is the area worth a coaching conversation; addressing it is "
                f"the most direct path back toward Thriving.")

    # -----------------------------------------------------------------------
    # Shape 2 — breadth gap (e >= 60, a < 60). Reps showing up but not using
    # the full platform. Cohort-aware escalation for 2023+ cohorts with
    # minimal outcomes.
    # -----------------------------------------------------------------------
    if e >= 60 and a < 60:
        eng_qualifier = "consistently" if e >= 70 else "at a limited rate"
        if cohort_year is not None and cohort_year >= 2023 and v < 40:
            return (f"{org_name}'s reps are logging in {eng_qualifier} (engagement {_fmt(e)}), "
                    f"but the platform is producing minimal outcomes (value delivery {_fmt(v)}) "
                    f"and feature coverage is thin (adoption {_fmt(a)}). For a {cohort_year} "
                    f"cohort, this is proactive-outreach territory — identify the one or two "
                    f"highest-ROI unused features and anchor the next conversation around them.")
        if val_score is not None and val_score < 60:
            gap_clause = (f"adoption ({_fmt(a)}) and value delivery ({_fmt(v)}) reflect")
        else:
            gap_clause = f"adoption ({_fmt(a)}) reflects"
        return (f"{org_name}'s reps are logging in {eng_qualifier} (engagement {_fmt(e)}), "
                f"but they are using only a portion of the platform — {gap_clause} a "
                f"feature-coverage gap, not an activity problem. Run a targeted coaching session "
                f"on the highest-ROI unused features to convert this activity into stronger "
                f"outcomes.")

    # -----------------------------------------------------------------------
    # Shape 3 — passive value: outcomes hold up but engagement is thin
    # (e < 55, v >= 50). Ops collapse is called out explicitly because it
    # changes the action.
    # -----------------------------------------------------------------------
    if e < 55 and v >= 50:
        if ops_score is not None and ops_score < 30:
            return (f"The platform is producing some outcomes for {org_name} (value delivery "
                    f"{_fmt(v)}), but rep engagement is thin (engagement {_fmt(e)}) and the data "
                    f"infrastructure is in critical shape (ops {_fmt(o)}) — usage and "
                    f"infrastructure issues are likely reinforcing each other. Both need parallel "
                    f"attention; fixing the infrastructure alone will not bring the broader team "
                    f"back.")
        return (f"The platform is producing some outcomes for {org_name} (value delivery "
                f"{_fmt(v)}), but rep engagement is thin (engagement {_fmt(e)}) — a small slice "
                f"of the team is doing most of the work. Re-engaging the broader team is the "
                f"most important next step: identify which reps have gone quiet and whether "
                f"coverage or enablement gaps are driving it.")

    # -----------------------------------------------------------------------
    # Shape 4 — near-dormant (e < 55, v < 50, floor did not fire). Catches
    # accounts just inside the threshold lines but not capped at 40.
    # -----------------------------------------------------------------------
    if e < 55 and v < 50:
        ops_tail = (
            f"Operational health ({_fmt(o)}) is clean, but well-maintained data is only useful "
            f"when reps are logging in."
            if ops_score is not None and ops_score >= 70 else
            f"Operational health ({_fmt(o)}) also has gaps that need attention alongside the "
            f"re-engagement work."
        )
        return (f"{org_name} is showing minimal activity on both sides — engagement ({_fmt(e)}) "
                f"and value delivery ({_fmt(v)}) are both below where they need to be, and the "
                f"platform is producing little observable value. {ops_tail} Re-establishing "
                f"contact and determining whether this relationship is recoverable is the "
                f"urgent next step.")

    # -----------------------------------------------------------------------
    # Shape 5 — surface-strong with ops drag (ops < 50, e >= 60, v >= 60).
    # Infrastructure is the hidden risk.
    # -----------------------------------------------------------------------
    if ops_score is not None and ops_score < 50 and e >= 60 and v >= 60:
        return (f"{org_name} looks strong on the surface — engagement ({_fmt(e)}) and value "
                f"delivery ({_fmt(v)}) are both healthy — but the data infrastructure "
                f"(ops {_fmt(o)}) has real problems that will eventually surface as a rep "
                f"experience issue. An infrastructure review (catalog completeness and import "
                f"health) is the right next step before this becomes rep-facing.")

    # -----------------------------------------------------------------------
    # Fallback — mixed profile with no clean shape. Name strongest + weakest
    # and pair with an action keyed off the band + weakest dim.
    # -----------------------------------------------------------------------
    band_action = {
        ("Thriving", "operational health"): ("Address the data infrastructure when the next "
            "review cycle allows — the rest of the picture is strong enough to support it."),
        ("Thriving", "adoption"):            ("A feature coaching session targeting the unused "
            "capabilities is the highest-leverage next step."),
        ("Thriving", "value delivery"):      ("Investigate why activity is not converting into "
            "outcomes — an order pipeline review or portal activation check is the starting point."),
        ("Thriving", "engagement"):          ("Monitor closely — an engagement dip in an otherwise "
            "Thriving account is an early warning worth tracking."),
        ("Healthy", "operational health"):   ("Addressing catalog and import health in the next "
            "review cycle is the cleanest path back toward Thriving."),
        ("Healthy", "adoption"):             ("A focused coaching session would help this team "
            "use more of the platform; rep activity is already there to support it."),
        ("Healthy", "value delivery"):       ("Focus the next conversation on converting activity "
            "into outcomes; portal activation or an order-workflow review is the starting point."),
        ("Healthy", "engagement"):           ("Monitor engagement closely; a continued downward "
            "trend would push this into Watch territory."),
        ("Watch", "operational health"):     ("Escalate the data infrastructure issues to the ops "
            "team before they degrade the rep experience further."),
        ("Watch", "adoption"):               ("Run a feature coaching session targeting the "
            "unused capabilities with the highest impact for this team."),
        ("Watch", "value delivery"):         ("Focus the next conversation on what is blocking "
            "orders or portal adoption — converting activity into outcomes is the priority."),
        ("Watch", "engagement"):             ("Re-activate the team and identify what is driving "
            "the low participation; a proactive engagement call is the next step."),
    }
    severe_default = ("Escalate to leadership — at this severity, the account needs a senior-level "
                      "conversation about whether the relationship can be recovered.")
    if band in ("Thriving", "Healthy"):
        s1 = (f"{org_name} is in {band} territory ({_fmt(score)}) with a mixed profile — "
              f"{top_dim} ({_fmt(top_val)}) is the strongest area and {low_dim} ({_fmt(low_val)}) "
              f"is the drag.")
    elif band == "Watch":
        s1 = (f"{org_name} is in Watch ({_fmt(score)}) with a mixed performance profile — "
              f"no single dimension dominates, but {low_dim} ({_fmt(low_val)}) is the largest gap.")
    else:
        s1 = (f"{org_name} is in {band} territory ({_fmt(score)}); the score reflects a mixed "
              f"profile with {low_dim} ({_fmt(low_val)}) as the largest gap.")
    action = band_action.get((band, low_dim), severe_default)
    return f"{s1} {action}"


def band_score(value, bands, lower_is_better=False):
    """Map a value to a score using a list of (threshold, score) bands."""
    if value is None:
        return None
    if lower_is_better:
        for threshold, score in bands:
            if value <= threshold:
                return score
        return 0
    for threshold, score in bands:
        if value >= threshold:
            return score
    return 0


def band_for_score(score):
    """Map a composite score to a health band label."""
    if score is None:
        return None
    for threshold, label in HEALTH_BANDS:
        if score >= threshold:
            return label
    return "Critical"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Health V3 scoring operator")
    p.add_argument("--mal", required=True, help="Path to MAL CSV")
    p.add_argument("--score-date", required=True,
                   help="YYYY-MM-DD anchor for all scoring math (required for deterministic output)")
    p.add_argument("--output-dir", default="Health V3/runs",
                   help="Parent dir; a {score-date} subdir is created inside")
    p.add_argument("--single-org", help="Score only this org_shortname (for debugging)")
    p.add_argument("--dry-run", action="store_true",
                   help="Compute scores and print to stdout; do not write CSV")
    p.add_argument(
        "--pg-cache-dir", default=None,
        help=(
            "Directory containing pre-cached CSV files from a prior MCP "
            "cache-population pass. When set, the operator reads all Postgres "
            "and BigQuery data from CSVs in this directory instead of opening "
            "live connections."
        ),
    )
    # V3.1 convenience aliases for --pg-cache-dir
    p.add_argument("--cache", action="store_true",
                   help="Enable cache mode (shorthand for --pg-cache-dir).")
    p.add_argument("--cache-dir", default=None,
                   help="Cache directory (alias for --pg-cache-dir).")
    return p.parse_args()


# ---------------------------------------------------------------------------
# CONNECTIONS
# ---------------------------------------------------------------------------

def connect_pg():
    import psycopg2
    url = os.environ.get("DATABASE_URL")
    if url:
        conn = psycopg2.connect(url)
    else:
        conn = psycopg2.connect(
            host=os.environ.get("PGHOST"),
            port=os.environ.get("PGPORT", "5432"),
            dbname=os.environ.get("PGDATABASE", "supercat_production"),
            user=os.environ.get("PGUSER", "postgres"),
            password=os.environ.get("PGPASSWORD", ""),
        )
    conn.set_session(readonly=True, autocommit=True)
    return conn


def connect_bq():
    from google.cloud import bigquery
    return bigquery.Client(project=BQ_PROJECT)


def pg_query(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


# ---------------------------------------------------------------------------
# CACHE-MODE HELPERS
# ---------------------------------------------------------------------------
#
# When --pg-cache-dir is supplied, every loader below reads its data from a
# CSV in that directory instead of opening a live Postgres/BigQuery
# connection. The cache files are produced by a separate MCP-driven workflow
# (see README.md §"How to populate the cache"). This mirrors V2's --pg-cache-dir
# behavior but with two deliberate deviations:
#   1) V3 uses one flag for both Postgres and BigQuery caches (V2 splits them
#      into --pg-cache-dir and --bq-cache-dir).
#   2) V3 fails fast when a required cache file is missing instead of falling
#      back to a live query (V2 silently falls back). Cache mode in V3 is
#      all-or-nothing because the credential-less environment cannot recover.
#
# Cache files written by the MCP serialize bool columns as 'True'/'False'
# strings, timestamp columns as ISO strings, and array columns as their
# Python repr. The helpers below coerce these back to the dtypes the rest
# of the operator expects.

_TRUTHY = frozenset({"true", "t", "1", "yes", "y"})


def _coerce_bool_columns(df: pd.DataFrame, cols) -> pd.DataFrame:
    """Coerce string 'True'/'False' (and 1/0) back to Python bool.

    Required because scoring code (which is locked) uses `bool(value)` and
    `if not value:` against these columns. A naive read_csv leaves them as
    object/string dtype where 'False' is truthy. Live psycopg2 returns real
    bools; this restores parity for cache mode.
    """
    for col in cols:
        if col not in df.columns:
            continue
        if df[col].dtype == bool:
            continue
        df[col] = (df[col].astype(str).str.strip().str.lower().isin(_TRUTHY))
    return df


def _parse_tag_list(value):
    """Best-effort parse of an ARRAY_AGG cell that was written to CSV.

    Live BigQuery returns a numpy array of strings; CSV round-trip turns it
    into the repr of that array. Both Python-list repr ("['a', 'b']") and
    numpy whitespace repr ("['a' 'b']") are accepted. Returns a list.
    """
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if isinstance(value, float) and pd.isna(value):
        return []
    s = str(value).strip()
    if not s or s.lower() == "nan":
        return []
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, (list, tuple)):
            return list(parsed)
        return [parsed]
    except (ValueError, SyntaxError):
        inner = s.strip("[]").replace("'", "").replace('"', "")
        return [p.strip() for p in re.split(r"[,\s]+", inner) if p.strip()]


def _read_cache_csv(
    cache_dir, filename, parse_dates=None, bool_cols=None
) -> pd.DataFrame:
    """Read a cache CSV and restore dtypes the operator expects.

    Fails fast (FileNotFoundError) if the file is absent. Cache mode is
    all-or-nothing — if the agent populating the cache missed a file, the
    operator must stop, not silently fall back to a live connection it
    cannot open in this environment.
    """
    path = Path(cache_dir) / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Cache mode enabled but {path} not found. "
            f"Populate the cache (see README.md §'How to populate the cache') "
            f"before running."
        )
    df = pd.read_csv(path, parse_dates=parse_dates or [])
    if bool_cols:
        df = _coerce_bool_columns(df, bool_cols)
    return df


# ---------------------------------------------------------------------------
# DATA LOADERS
# ---------------------------------------------------------------------------

def load_mal(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"ord_id": "org_shortname", "stack": "bundle"})
    df["org_shortname"] = df["org_shortname"].astype(str).str.lower().str.strip()
    df["bundle"] = df["bundle"].astype(str).str.strip().map(BUNDLE_MAP).fillna(df["bundle"])
    df["arr"] = pd.to_numeric(df["arr"].astype(str).str.replace("[$,]", "", regex=True),
                              errors="coerce").fillna(0)
    df["cohort_year"] = pd.to_numeric(df["cohort_year"], errors="coerce").fillna(0).astype(int)
    return df[["org_shortname", "company", "bundle", "arr", "cohort_year"]]


_ORG_CONFIG_BOOLS = [
    "contract_pricing_enabled", "enable_sales_data",
    "enable_online_catalog", "enable_online_ordering", "enable_sales_portal",
]


def load_pg_org_config(conn, cache_dir=None):
    if cache_dir is not None:
        return _read_cache_csv(
            cache_dir, "pg_org_config.csv", bool_cols=_ORG_CONFIG_BOOLS,
        )
    return pg_query(conn, """
        WITH ms_agg AS (
          SELECT organization_id,
                 BOOL_OR(COALESCE(enable_online_catalog, false)) AS enable_online_catalog,
                 BOOL_OR(COALESCE(enable_online_ordering, false)) AS enable_online_ordering,
                 BOOL_OR(COALESCE(enable_sales_portal, false)) AS enable_sales_portal
          FROM mobile_sites GROUP BY organization_id
        )
        SELECT o.id AS organization_id, LOWER(o.shortname) AS org_shortname,
               o.name AS org_name, COALESCE(o.contract_pricing_enabled, false) AS contract_pricing_enabled,
               COALESCE(o.enable_sales_data, false) AS enable_sales_data,
               COALESCE(m.enable_online_catalog, false) AS enable_online_catalog,
               COALESCE(m.enable_online_ordering, false) AS enable_online_ordering,
               COALESCE(m.enable_sales_portal, false) AS enable_sales_portal
        FROM organizations o LEFT JOIN ms_agg m ON m.organization_id = o.id
    """)


def load_pg_engagement(conn, cache_dir=None):
    """Logins, distinct active users, last/earliest login, internal-user denominator."""
    if cache_dir is not None:
        # NOTE: Cache must be regenerated to include logins_30d and logins_180d before running velocity scoring in cache mode.
        return _read_cache_csv(
            cache_dir, "pg_engagement.csv",
            parse_dates=["last_login_at", "first_login_at"],
        )
    return pg_query(conn, """
        WITH login_agg AS (
          SELECT organization_id,
                 COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days') AS logins_90d,
                 COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days')  AS logins_30d,
                 COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '180 days') AS logins_180d,
                 COUNT(DISTINCT user_id) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days') AS active_users_90d,
                 MAX(created_at) AS last_login_at,
                 MIN(created_at) AS first_login_at,
                 COUNT(DISTINCT user_id) FILTER (WHERE created_at >= NOW() - INTERVAL '365 days') AS active_users_365d
          FROM login_events
          GROUP BY organization_id
        ),
        user_agg AS (
          SELECT ou.organization_id,
                 COUNT(*) FILTER (
                   WHERE COALESCE(ou.disabled, false) = false
                   AND (u.email IS NULL OR LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN %(internal)s)
                 ) AS enabled_users
          FROM org_users ou
          LEFT JOIN users u ON u.id = ou.user_id
          GROUP BY ou.organization_id
        )
        SELECT o.id AS organization_id,
               COALESCE(la.logins_90d, 0) AS logins_90d,
               COALESCE(la.logins_30d, 0) AS logins_30d,
               COALESCE(la.logins_180d, 0) AS logins_180d,
               COALESCE(la.active_users_90d, 0) AS active_users_90d,
               la.last_login_at, la.first_login_at,
               COALESCE(la.active_users_365d, 0) AS active_users_365d,
               COALESCE(ua.enabled_users, 0) AS enabled_users
        FROM organizations o
        LEFT JOIN login_agg la ON la.organization_id = o.id
        LEFT JOIN user_agg ua ON ua.organization_id = o.id
    """, {"internal": tuple(INTERNAL_DOMAINS)})


def load_pg_smart_stacks(conn, cache_dir=None):
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "pg_smart_stacks.csv")
    return pg_query(conn, "SELECT organization_id, COUNT(*) AS smart_stack_count FROM smart_stacks GROUP BY organization_id")


def load_pg_orders(conn, cache_dir=None):
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "pg_orders.csv")
    return pg_query(conn, """
        SELECT organization_id,
               COUNT(*) FILTER (
                 WHERE LOWER(order_source) = 'ipad' AND is_submitted = true
                   AND order_state = 'active' AND submit_date >= NOW() - INTERVAL '90 days'
               ) AS ipad_orders_90d
        FROM orders GROUP BY organization_id
    """)


def load_pg_portal_orders(conn, cache_dir=None):
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "pg_portal_orders.csv")
    return pg_query(conn, """
        SELECT organization_id, COUNT(*) AS portal_orders_90d
        FROM portal_orders WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY organization_id
    """)


def load_pg_catalog(conn, cache_dir=None):
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "pg_catalog.csv")
    return pg_query(conn, """
        SELECT p.organization_id,
               COUNT(*) FILTER (WHERE COALESCE(p.deleted, false) = false) AS total_active,
               COUNT(*) FILTER (
                 WHERE COALESCE(p.deleted, false) = false
                   AND p.long_description IS NOT NULL AND p.long_description <> ''
                   AND p.image_exists = true
                   AND ( p.net_price > 0
                         OR COALESCE(o.contract_pricing_enabled, false) = true
                         OR (p.prices_json IS NOT NULL AND p.prices_json <> '{}'::text) )
               ) AS complete_products
        FROM products p
        LEFT JOIN organizations o ON o.id = p.organization_id
        GROUP BY p.organization_id
    """)


def load_pg_imports(conn, cache_dir=None):
    """One row per (org, import_type) with run history. Type extracted from YAML data field."""
    if cache_dir is not None:
        return _read_cache_csv(
            cache_dir, "pg_imports.csv",
            parse_dates=["last_run_at", "first_run_at"],
            bool_cols=["last_run_had_error"],
        )
    return pg_query(conn, """
        WITH typed AS (
          SELECT organization_id, created_at, data,
                 TRIM(SUBSTRING(data FROM '---\\s*\\n\\s*-\\s*-\\s*([^\\n]+)')) AS import_type,
                 (data LIKE '%:error%' OR data LIKE '%:fatal%') AS had_error
          FROM import_events
          WHERE created_at >= NOW() - INTERVAL '180 days'
        ),
        last_run AS (
          SELECT DISTINCT ON (organization_id, import_type)
                 organization_id, import_type, had_error AS last_run_had_error
          FROM typed
          WHERE import_type IS NOT NULL AND import_type <> ''
          ORDER BY organization_id, import_type, created_at DESC
        ),
        agg AS (
          SELECT organization_id, import_type,
                 COUNT(*) AS run_count_180d,
                 COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '90 days') AS run_count_90d,
                 MAX(created_at) AS last_run_at,
                 MIN(created_at) AS first_run_at
          FROM typed WHERE import_type IS NOT NULL AND import_type <> ''
          GROUP BY organization_id, import_type
        )
        SELECT a.*, l.last_run_had_error
        FROM agg a JOIN last_run l USING (organization_id, import_type)
    """)


def load_bq_mp_sharing(bq, cache_dir=None):
    """Mixpanel sharing/quoting/portal events per org, trailing 90d."""
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "bq_mp_sharing.csv")
    sql = """
        SELECT
          LOWER(COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, ''))) AS org_shortname,
          COUNTIF(event_name = 'item_email_drafted') AS mp_item_email_drafted_90d,
          COUNTIF(event_name = 'document_email_drafted') AS mp_document_email_drafted_90d,
          COUNTIF(event_name = 'view_portal') AS mp_view_portal_90d
        FROM `supercat-data-pipeline.mixpanel.events`
        WHERE event_name IN ('item_email_drafted', 'document_email_drafted', 'view_portal')
          AND DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
          AND COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, '')) IS NOT NULL
        GROUP BY org_shortname
    """
    return bq.query(sql).to_dataframe()


def load_bq_helpscout_fires(bq, cache_dir=None):
    """Open conversations with L3/L4/S1/S2 tags, plus their primaryCustomer email domains."""
    if cache_dir is not None:
        df = _read_cache_csv(
            cache_dir, "bq_helpscout_fires.csv",
            parse_dates=["most_recent_open_at"],
        )
        if "sample_tags" in df.columns:
            df["sample_tags"] = df["sample_tags"].apply(_parse_tag_list)
        return df
    sql = """
        SELECT
          LOWER(REGEXP_EXTRACT(SAFE.STRING(primaryCustomer.email), r'@(.+)$')) AS email_domain,
          COUNT(*) AS open_fire_conv_count,
          MAX(PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))) AS most_recent_open_at,
          ARRAY_AGG(DISTINCT LOWER(JSON_EXTRACT_SCALAR(t, '$.tag')) IGNORE NULLS LIMIT 5) AS sample_tags
        FROM `supercat-data-pipeline.helpscout.conversations`,
             UNNEST(JSON_EXTRACT_ARRAY(TO_JSON_STRING(tags))) AS t
        WHERE status IN ('active', 'pending')
          AND SAFE.STRING(primaryCustomer.email) IS NOT NULL
          AND ( LOWER(JSON_EXTRACT_SCALAR(t, '$.tag')) LIKE 'l3%'
             OR LOWER(JSON_EXTRACT_SCALAR(t, '$.tag')) LIKE 'l4%'
             OR LOWER(JSON_EXTRACT_SCALAR(t, '$.tag')) LIKE 's1%'
             OR LOWER(JSON_EXTRACT_SCALAR(t, '$.tag')) LIKE 's2%' )
        GROUP BY email_domain HAVING email_domain IS NOT NULL
    """
    return bq.query(sql).to_dataframe()


def build_domain_map(conn, cache_dir=None):
    """Domain → org_shortname map, derived from users + org_users, excluding generic + internal domains."""
    if cache_dir is not None:
        return _read_cache_csv(cache_dir, "pg_domain_map.csv")
    excluded = tuple(INTERNAL_DOMAINS | GENERIC_DOMAINS)
    return pg_query(conn, """
        WITH d AS (
          SELECT LOWER(o.shortname) AS org_shortname,
                 LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) AS domain,
                 COUNT(*) AS n
          FROM users u JOIN org_users ou ON ou.user_id = u.id
                       JOIN organizations o ON ou.organization_id = o.id
          WHERE u.email::text LIKE '%@%'
            AND LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN %(excluded)s
          GROUP BY 1, 2
        ),
        ranked AS (
          SELECT org_shortname, domain, n,
                 ROW_NUMBER() OVER (PARTITION BY domain ORDER BY n DESC, org_shortname ASC) AS rn
          FROM d WHERE n >= 2
        )
        SELECT domain, org_shortname FROM ranked WHERE rn = 1
    """, {"excluded": excluded})


# ---------------------------------------------------------------------------
# SCORING
# ---------------------------------------------------------------------------

def score_engagement(eng_row, bundle=""):
    """Returns (score, narrative_dict). score is None only when no usable data."""
    logins = int(eng_row.get("logins_90d") or 0)
    active = int(eng_row.get("active_users_90d") or 0)
    enabled = int(eng_row.get("enabled_users") or 0)
    fallback = int(eng_row.get("active_users_365d") or 0)
    last_login = eng_row.get("last_login_at")

    inflated = enabled > 500 and bundle in INFLATED_DENOM_BUNDLES
    if (enabled == 0 or inflated) and fallback > 0:
        enabled = fallback
        denom_note = (
            " (denominator switched to annual active users"
            " — org_users inflated by portal accounts)"
            if inflated else
            " (denominator from active_users_365d fallback)"
        )
    else:
        denom_note = ""

    if enabled == 0 and logins == 0:
        return None, {"reason": "no logins, no provisioned users"}

    raw_ratio = (active / enabled) if enabled > 0 else 0.0
    ratio = min(raw_ratio, 1.0)
    denominator_quality = "stale" if raw_ratio > 1.0 else None

    login_score = band_score(logins, LOGIN_BANDS)
    ratio_score = band_score(ratio, RATIO_BANDS)

    logins_30d = int(eng_row.get("logins_30d") or 0)
    logins_180d = int(eng_row.get("logins_180d") or 0)
    if logins_180d == 0:
        velocity_score = 0
        velocity_ratio = None
    else:
        velocity_ratio = round((logins_30d / logins_180d) * 6, 2)
        velocity_score = band_score(velocity_ratio, VELOCITY_BANDS) if velocity_ratio > 0 else 0

    score = round((login_score + ratio_score + velocity_score) / 3, 1)
    narrative = _build_engagement_narrative(
        logins, active, enabled, ratio, velocity_ratio,
        login_score, ratio_score, velocity_score,
        denom_note, score,
    )
    return score, {"narrative": narrative, "denominator_quality": denominator_quality,
                   "logins_90d": logins, "velocity_ratio": velocity_ratio}


def score_adoption(org_cfg, eng_row, mp_row, ss_count, portal_orders_90d, import_types_active):
    """Returns (score, narrative_dict)."""
    features = []  # list of (name, applicable, used)

    features.append(("iPad", True, (eng_row.get("logins_90d") or 0) > 0))
    features.append(("Smart Stacks", True, ss_count > 0))

    mp_share = (mp_row.get("mp_item_email_drafted_90d", 0) or 0) + (mp_row.get("mp_document_email_drafted_90d", 0) or 0)
    features.append(("Sharing/quoting", True, mp_share > 0))

    eoc = bool(org_cfg.get("enable_online_catalog"))
    eoo = bool(org_cfg.get("enable_online_ordering"))
    esp = bool(org_cfg.get("enable_sales_portal"))
    esd = bool(org_cfg.get("enable_sales_data"))

    view_portal_90d = int(mp_row.get("mp_view_portal_90d", 0) or 0)

    features.append(("eCat Online Catalog", eoc, portal_orders_90d > 0))
    features.append(("Online Ordering", eoo, portal_orders_90d > 0))
    features.append(("Sales Portal", esp, view_portal_90d > 0))

    inv_in_history = "Inventory" in import_types_active
    inv_runs_90d = import_types_active.get("Inventory", {}).get("run_count_90d", 0)
    features.append(("Inventory Management", inv_in_history, inv_runs_90d > 0))

    sd_runs_90d = import_types_active.get("Sales Data", {}).get("run_count_90d", 0)
    features.append(("Sales Data", esd, sd_runs_90d > 0))

    applicable = [f for f in features if f[1]]
    used = [f for f in applicable if f[2]]
    if len(applicable) < 3:
        return None, {"reason": "fewer than 3 applicable features"}

    score = round(len(used) / len(applicable) * 100, 1)
    unused = [f[0] for f in applicable if not f[2]]
    narrative = _build_adoption_narrative(score, len(used), len(applicable), unused)

    # Bundle/config mismatch: MAL bundle is iPad-only but mobile_sites flags say cart/portal
    return score, {"narrative": narrative}


def score_value_delivery(org_cfg, ipad_orders_90d, mp_share_count, portal_orders_90d, import_types_active):
    activities = []
    activities.append(("Order volume (iPad)", True, ipad_orders_90d >= 10))
    activities.append(("Sharing activity", True, mp_share_count >= 3))

    eoc = bool(org_cfg.get("enable_online_catalog"))
    eoo = bool(org_cfg.get("enable_online_ordering"))
    esp = bool(org_cfg.get("enable_sales_portal"))

    activities.append(("Online catalog active", eoc, portal_orders_90d > 0))
    activities.append(("Portal ordering", eoo, portal_orders_90d > 0))
    activities.append(("Sales Portal engagement", esp, portal_orders_90d > 0))

    inv_active = "Inventory" in import_types_active
    inv_runs_90d = import_types_active.get("Inventory", {}).get("run_count_90d", 0)
    activities.append(("Inventory data flowing", inv_active, inv_runs_90d > 0))

    applicable = [a for a in activities if a[1]]
    achieved = [a for a in applicable if a[2]]
    if not applicable:
        return None, {"reason": "no applicable channels"}

    score = round(len(achieved) / len(applicable) * 100, 1)
    achieved_names = [a[0] for a in achieved]
    gap_names = [a[0] for a in applicable if not a[2]]
    narrative = _build_value_delivery_narrative(
        score, achieved_names, gap_names, len(applicable),
        ipad_orders_90d, mp_share_count, portal_orders_90d, inv_runs_90d,
    )
    return score, {"narrative": narrative}


def score_operational_health(catalog_row, import_rows, contract_pricing_enabled, as_of):
    """as_of: datetime anchor (the score_date) for staleness/freshness math.
    Must be passed in — using wall-clock time would make cache-mode runs non-deterministic."""
    sub = []  # list of (name, score)

    # Sub-signal 1: Catalog Completeness (step ladder)
    if catalog_row is None or (catalog_row.get("total_active") or 0) == 0:
        cat_score = None
        cat_pct = None
    else:
        total = catalog_row["total_active"]
        complete = catalog_row["complete_products"] or 0
        cat_pct = complete / total
        cat_score = band_score(cat_pct, CATALOG_LADDER)
    if cat_score is not None:
        sub.append(("catalog", cat_score))

    # Sub-signal 2: Import Health (active types only)
    active_types = []
    for row in import_rows:
        # An import type is "active" if it has run in trailing 180d (which is the load window).
        # Need to apply the initial-load carve-out to determine which types count toward import health.
        active_types.append(row)
    scoreable_imports = [r for r in active_types
                         if r.get("import_type") not in EXCLUDED_IMPORT_TYPES_HEALTH]
    if scoreable_imports:
        healthy = [r for r in scoreable_imports if not r["last_run_had_error"]]
        imp_score = round(len(healthy) / len(scoreable_imports) * 100, 1)
        sub.append(("imports", imp_score))
    else:
        imp_score = None

    # Sub-signal 3: Data Freshness
    # Each entry: (band_score, run_count_180d, import_type, staleness_ratio, days_since_last, mean_gap)
    fresh_entries = []
    now = as_of
    for r in active_types:
        runs = r["run_count_180d"]
        if runs < 3:
            continue  # min history not met
        first_run = r["first_run_at"]
        last_run = r["last_run_at"]
        if first_run is None or last_run is None:
            continue
        first_run = first_run.replace(tzinfo=None) if hasattr(first_run, "tzinfo") else first_run
        last_run = last_run.replace(tzinfo=None) if hasattr(last_run, "tzinfo") else last_run
        days_span = (last_run - first_run).total_seconds() / 86400
        days_since_first = (now - first_run).total_seconds() / 86400
        days_since_last = (now - last_run).total_seconds() / 86400
        if runs < 5 and days_span <= 7 and days_since_first <= 14:
            # Burst of <5 runs all within 7 days AND the burst happened within the last 14 days
            # → treat as initial load, not a stale feed
            continue
        mean_gap = days_span / max(runs - 1, 1)
        gap = max(mean_gap, 1.0)
        stale_ratio = days_since_last / gap
        fscore = band_score(stale_ratio, FRESHNESS_BANDS, lower_is_better=True)
        fresh_entries.append((fscore, r["run_count_180d"],
                               r.get("import_type", "Unknown"), stale_ratio,
                               days_since_last, gap))
    if fresh_entries:
        total_weight = sum(w for _, w, *_ in fresh_entries)
        if total_weight > 0:
            fresh_score = round(
                sum(s * w for s, w, *_ in fresh_entries) / total_weight, 1
            )
        else:
            fresh_score = round(
                sum(s for s, *_ in fresh_entries) / len(fresh_entries), 1
            )
        sub.append(("freshness", fresh_score))
    else:
        fresh_score = None

    if not sub:
        return None, {"reason": "no operational signals available"}

    score = round(sum(s for _, s in sub) / len(sub), 1)

    # Collect stale feeds for narrative (staleness_ratio > 1.5 = notably late or worse)
    stale_feeds = [
        (imp_type, stale_ratio, days_since, gap)
        for _, _, imp_type, stale_ratio, days_since, gap in fresh_entries
        if stale_ratio > 1.5
    ]

    narrative = _build_ops_narrative(
        score, cat_pct, cat_score, contract_pricing_enabled,
        scoreable_imports, imp_score, fresh_score, stale_feeds, as_of,
    )
    return score, {"narrative": narrative, "catalog_pct": cat_pct,
                   "import_score": imp_score, "freshness_score": fresh_score}


def composite(eng, ado, val, ops):
    dims = [s for s in [eng, ado, val, ops] if s is not None]
    n = len(dims)
    if n == 0:
        return None, "blocked", 0
    if n == 1:
        return None, "blocked", 1
    score = round(sum(dims) / n, 1)
    status = "complete" if n == 4 else "partial"
    return score, status, n


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    score_date = args.score_date

    print(f"[INFO] Health V3 score run — {score_date}")
    mal = load_mal(args.mal)
    print(f"[OK] MAL loaded: {len(mal)} orgs")

    if args.single_org:
        mal = mal[mal["org_shortname"] == args.single_org.lower()]
        if mal.empty:
            print(f"[FATAL] --single-org {args.single_org} not in MAL")
            sys.exit(1)

    # Resolve --cache / --cache-dir aliases to the canonical pg_cache_dir variable
    cache_dir = args.pg_cache_dir or args.cache_dir
    if args.cache and cache_dir is None:
        print("[FATAL] --cache requires --cache-dir <path>")
        sys.exit(1)
    if cache_dir is not None:
        cache_path = Path(cache_dir)
        if not cache_path.is_dir():
            print(f"[FATAL] --pg-cache-dir not found or not a directory: {cache_dir}")
            sys.exit(1)
        print(f"[INFO] Cache mode: reading Postgres + BigQuery data from {cache_path}")
        pg = None
        bq = None
    else:
        pg = connect_pg()
        print("[OK] Postgres connected")
        bq = connect_bq()
        print("[OK] BigQuery client ready")

    print("[INFO] Loading Postgres data ...")
    org_cfg = load_pg_org_config(pg, cache_dir=cache_dir).set_index("org_shortname")
    eng_pg = load_pg_engagement(pg, cache_dir=cache_dir).set_index("organization_id")
    ss_pg = load_pg_smart_stacks(pg, cache_dir=cache_dir).set_index("organization_id")
    orders_pg = load_pg_orders(pg, cache_dir=cache_dir).set_index("organization_id")
    portal_pg = load_pg_portal_orders(pg, cache_dir=cache_dir).set_index("organization_id")
    cat_pg = load_pg_catalog(pg, cache_dir=cache_dir).set_index("organization_id")
    imp_pg = load_pg_imports(pg, cache_dir=cache_dir)
    print(f"[OK] org_cfg={len(org_cfg)} eng={len(eng_pg)} catalog={len(cat_pg)} imports={len(imp_pg)}")

    print("[INFO] Loading BigQuery data ...")
    mp_share = load_bq_mp_sharing(bq, cache_dir=cache_dir).set_index("org_shortname")
    hs_fires = load_bq_helpscout_fires(bq, cache_dir=cache_dir)
    print(f"[OK] mixpanel_sharing_orgs={len(mp_share)} helpscout_fire_domains={len(hs_fires)}")

    print("[INFO] Building domain map ...")
    domain_map = build_domain_map(pg, cache_dir=cache_dir).set_index("domain")["org_shortname"].to_dict()

    # Resolve fire-flag conversations to orgs
    fires_by_org = {}
    for _, row in hs_fires.iterrows():
        org = domain_map.get(row["email_domain"])
        if not org:
            continue
        if org not in fires_by_org or row["most_recent_open_at"] > fires_by_org[org]["most_recent_open_at"]:
            fires_by_org[org] = {"count": int(row["open_fire_conv_count"]),
                                 "most_recent_open_at": row["most_recent_open_at"],
                                 "tags": list(row["sample_tags"])}

    # New-org exclusion
    rows = []
    skipped = []
    current_year = int(score_date[:4])
    score_date_dt = datetime.fromisoformat(score_date)
    today = score_date_dt

    for _, mal_row in mal.iterrows():
        org = mal_row["org_shortname"]
        if org not in org_cfg.index:
            skipped.append((org, "not_in_postgres"))
            continue
        cfg = org_cfg.loc[org].to_dict() if not isinstance(org_cfg.loc[org], pd.DataFrame) else org_cfg.loc[org].iloc[0].to_dict()
        org_id = cfg["organization_id"]
        eng_data = eng_pg.loc[org_id].to_dict() if org_id in eng_pg.index else {}

        # New-org check
        first_login = eng_data.get("first_login_at")
        if first_login is not None:
            days_since_first = (today - first_login.replace(tzinfo=None)).days
            if days_since_first < NEW_ORG_DAYS:
                skipped.append((org, "onboarding_window"))
                continue
        elif int(mal_row["cohort_year"]) == current_year:
            skipped.append((org, "onboarding_window"))
            continue

        # Per-org imports → dict by import_type
        org_imports = imp_pg[imp_pg["organization_id"] == org_id]
        import_types_active = {}
        for _, ir in org_imports.iterrows():
            import_types_active[ir["import_type"]] = ir.to_dict()

        ss_count = int(ss_pg.loc[org_id, "smart_stack_count"]) if org_id in ss_pg.index else 0
        ipad_orders_90d = int(orders_pg.loc[org_id, "ipad_orders_90d"]) if org_id in orders_pg.index else 0
        portal_orders_90d = int(portal_pg.loc[org_id, "portal_orders_90d"]) if org_id in portal_pg.index else 0
        mp_row = mp_share.loc[org].to_dict() if org in mp_share.index else {}
        mp_share_count = int((mp_row.get("mp_item_email_drafted_90d") or 0) + (mp_row.get("mp_document_email_drafted_90d") or 0))

        # Score dimensions
        eng_score, eng_meta = score_engagement(eng_data, bundle=mal_row["bundle"]) if eng_data else (None, {"reason": "no engagement data"})
        ado_score, ado_meta = score_adoption(cfg, eng_data, mp_row, ss_count, portal_orders_90d, import_types_active)
        val_score, val_meta = score_value_delivery(cfg, ipad_orders_90d, mp_share_count, portal_orders_90d, import_types_active)
        cat_row = cat_pg.loc[org_id].to_dict() if org_id in cat_pg.index else None
        ops_score, ops_meta = score_operational_health(cat_row, list(org_imports.to_dict("records")), bool(cfg.get("contract_pricing_enabled")), as_of=score_date_dt)

        composite_score, status, n_dims = composite(eng_score, ado_score, val_score, ops_score)

        # §5.2 behavioral floor override
        behavioral_floor_applied = bool(
            eng_score is not None and val_score is not None
            and eng_score < 55 and val_score < 40
        )
        if behavioral_floor_applied and composite_score is not None:
            composite_score = min(composite_score, BEHAVIORAL_FLOOR_CAP)

        # §5.1 ghost account override
        ghost = bool(mal_row["arr"] >= GHOST_ARR_THRESHOLD and (eng_data.get("logins_90d") or 0) == 0)
        ghost_note = None
        if ghost:
            ghost_note = f"ARR ${int(mal_row['arr']):,}, zero logins in 90d"
            if composite_score is not None:
                composite_score = min(composite_score, GHOST_CAP)
            else:
                composite_score = GHOST_CAP

        band = band_for_score(composite_score)

        # Composite-level override narratives (§5.1 / §5.2)
        _org_name = cfg.get("org_name") or mal_row["company"]

        def _fmt_score(s):
            return f"{s:.0f}" if s is not None else "N/A"

        _arr_str = f"${int(mal_row['arr']):,}" if mal_row['arr'] else "the contract value involved"

        if ghost:
            composite_narrative = (
                f"No one at {_org_name} has logged into the platform in the last 90 days despite "
                f"{_arr_str} in annual contract value. This is an urgent churn risk that needs an "
                f"immediate conversation with the client."
            )
        elif behavioral_floor_applied:
            # Profile-aware sub-shapes per V3.2.4 narrative rewrite:
            #   C — critically low across the board (eng < 25 AND val <= 10)
            #   A — full adoption, users gone dark (adoption >= 80)
            #   B — clean infrastructure, users gone dark (ops >= 75)
            #   D — standard floor (everything else)
            # C is checked first so the most severe profile wins when an org satisfies
            # multiple conditions (e.g., critically low usage on a fully-configured stack).
            _floor_eng = _fmt_score(eng_score)
            _floor_val = _fmt_score(val_score)
            critically_low = (
                eng_score is not None and eng_score < 25
                and val_score is not None and val_score <= 10
            )
            full_adoption_dark = ado_score is not None and ado_score >= 80
            clean_ops_dark = ops_score is not None and ops_score >= 75

            if critically_low:
                # Sub-shape C
                composite_narrative = (
                    f"{_org_name} has essentially no active usage — {_floor_eng} engagement and "
                    f"{_floor_val} value delivery mean the platform is running but not being used "
                    f"in any meaningful way. At {_arr_str} this is an urgent recovery situation."
                )
            elif full_adoption_dark:
                # Sub-shape A
                composite_narrative = (
                    f"{_org_name} has the full platform configured and adopted, but rep logins "
                    f"have dropped off sharply — engagement is at {_floor_eng} and the platform "
                    f"isn't generating observable outcomes. Outreach is needed to understand "
                    f"whether reps have gone dark on a coverage issue or whether a more "
                    f"fundamental re-engagement effort is required."
                )
            elif clean_ops_dark:
                # Sub-shape B
                composite_narrative = (
                    f"{_org_name}'s data infrastructure is healthy, but reps aren't using the "
                    f"platform — engagement is at {_floor_eng} and no business outcomes are "
                    f"being generated. The infrastructure isn't the problem; this is a rep "
                    f"adoption and activation conversation."
                )
            else:
                # Sub-shape D
                composite_narrative = (
                    f"{_org_name}'s rep activity ({_floor_eng} engagement) and platform outcomes "
                    f"({_floor_val} value delivery) are both too low to support a healthy "
                    f"relationship. Re-establishing contact to understand why reps have gone "
                    f"quiet is the first step — determine whether this is a coverage gap, a "
                    f"product fit issue, or something else."
                )
        else:
            composite_narrative = None

        # Build composite narrative for normal accounts (not ghost / behavioral floor)
        if composite_narrative is None and composite_score is not None:
            composite_narrative = _build_composite_narrative(
                org_name=_org_name,
                score=composite_score,
                band=band,
                eng_score=eng_score,
                ado_score=ado_score,
                val_score=val_score,
                ops_score=ops_score,
                bundle=mal_row["bundle"],
                arr=float(mal_row["arr"]),
                cohort_year=int(mal_row["cohort_year"]),
            )

        # Bundle/config mismatch
        mal_bundle = mal_row["bundle"]
        config_implies_cart = bool(cfg.get("enable_online_ordering"))
        config_implies_catalog = bool(cfg.get("enable_online_catalog"))
        bundle_says_cart = "Cart" in mal_bundle or "Full" in mal_bundle
        bundle_says_catalog = "Catalog" in mal_bundle or "Full" in mal_bundle
        bundle_config_mismatch = (config_implies_cart and not bundle_says_cart) or (config_implies_catalog and not bundle_says_catalog)

        # Support fire
        fire = fires_by_org.get(org)
        support_fire = fire is not None
        if support_fire:
            tag_str = ", ".join(fire["tags"][:2])
            support_note = f"{fire['count']} open conversation(s) tagged: {tag_str}"
            fire_ts = pd.Timestamp(fire["most_recent_open_at"]).replace(tzinfo=None)
            support_fire_days_open = (score_date_dt - fire_ts).days
        else:
            support_note = None
            support_fire_days_open = None
        support_data_available = (org in domain_map.values()) or support_fire

        rows.append({
            "org_shortname": org,
            "org_name": cfg.get("org_name") or mal_row["company"],
            "run_date": score_date,
            "bundle": mal_bundle, "arr": float(mal_row["arr"]),
            "cohort_year": int(mal_row["cohort_year"]),
            "engagement_score": eng_score,
            "engagement_narrative": eng_meta.get("narrative") or eng_meta.get("reason"),
            "adoption_score": ado_score,
            "adoption_narrative": ado_meta.get("narrative") or ado_meta.get("reason"),
            "value_delivery_score": val_score,
            "value_delivery_narrative": val_meta.get("narrative") or val_meta.get("reason"),
            "operational_health_score": ops_score,
            "operational_health_narrative": ops_meta.get("narrative") or ops_meta.get("reason"),
            "composite_score": composite_score, "health_band": band,
            "composite_narrative": composite_narrative,
            "ghost_account": ghost, "ghost_account_note": ghost_note,
            "behavioral_floor_applied": behavioral_floor_applied,
            "support_fire": support_fire, "support_fire_notes": support_note,
            "support_fire_days_open": support_fire_days_open,
            "support_data_available": support_data_available,
            "scoring_status": status, "dimensions_scored": n_dims,
            "denominator_quality": eng_meta.get("denominator_quality"),
            "bundle_config_mismatch": bundle_config_mismatch,
        })

    print(f"[OK] Scored {len(rows)} orgs; skipped {len(skipped)}")

    df = pd.DataFrame(rows)
    if args.dry_run:
        print(df.to_string(index=False))
        return

    out_dir = Path(args.output_dir)
    if out_dir.name != score_date:
        out_dir = out_dir / score_date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"client_health_scores_{score_date}.csv"
    df.to_csv(out_csv, index=False)
    print(f"[OK] Wrote {out_csv} ({len(df)} rows)")

    # Formatted CSV: user-facing column subset, reordered for stakeholder readability
    _fmt_cols = [
        "org_shortname",
        "org_name",
        "bundle",
        "arr",
        "cohort_year",
        "composite_score",
        "health_band",
        "composite_narrative",
        "engagement_score",
        "engagement_narrative",
        "adoption_score",
        "adoption_narrative",
        "value_delivery_score",
        "value_delivery_narrative",
        "operational_health_score",
        "operational_health_narrative",
        "support_fire_notes",
        "support_fire_days_open",
        "bundle_config_mismatch",
        "run_date",
    ]
    df_fmt = df[[c for c in _fmt_cols if c in df.columns]]
    fmt_csv = out_dir / f"client_health_scores_{score_date}_formatted.csv"
    df_fmt.to_csv(fmt_csv, index=False)
    print(f"Formatted CSV: {fmt_csv} ({len(df_fmt)} rows, {len(df_fmt.columns)} columns)")

    if skipped:
        skip_csv = out_dir / "skipped_new_orgs.csv"
        pd.DataFrame(skipped, columns=["org_shortname", "reason"]).to_csv(skip_csv, index=False)
        print(f"[OK] Wrote {skip_csv} ({len(skipped)} rows)")

    # run_metadata.md
    band_counts = df["health_band"].value_counts().to_dict()
    status_counts = df["scoring_status"].value_counts().to_dict()
    _cache_flags = f' --cache --cache-dir "{cache_dir}"' if cache_dir else ''
    metadata_md = f"""# Health V3 run metadata — {score_date}

- Command: `python health_operator_v3.py --mal "{args.mal}" --score-date {score_date}{_cache_flags} --output-dir "{args.output_dir}"`
- MAL: `{args.mal}`
- Output CSV: `{out_csv}`
- Rows scored: {len(df)}
- Rows skipped (new-org exclusion or not in Postgres): {len(skipped)}

## Distribution

Health band counts: {band_counts}
Scoring status counts: {status_counts}
Ghost accounts: {int(df['ghost_account'].sum())}
Behavioral floor applied: {int(df['behavioral_floor_applied'].sum())}
Support fire flags: {int(df['support_fire'].sum())}
Bundle/config mismatches: {int(df['bundle_config_mismatch'].sum())}
"""
    (out_dir / "run_metadata.md").write_text(metadata_md)
    print(f"[OK] Wrote run_metadata.md")


if __name__ == "__main__":
    main()
