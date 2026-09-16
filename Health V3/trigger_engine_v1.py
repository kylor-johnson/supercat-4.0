#!/usr/bin/env python3
"""
Health V3 — Trigger Engine (V2)

Reads a series of monthly canonical scorecards and emits the month-over-month
CS trigger list: what changed, who owns it, and what to do about it.

Trigger types (TRIGGER_ORDER):
    new_ghost             — ghost_account fired for the first time
    oscillating_band      — band flipped between exactly two bands for 4+ months
    chronic_at_risk       — N+ consecutive months in a distress band
    fire_duration         — support fire flag open longer than FIRE_DURATION_DAYS
    band_transition_down  — band regressed (and composite moved >= the min delta)
    score_drop            — composite fell >= SCORE_DROP_THRESHOLD without a band change
    band_transition_up    — band improved (reported separately as a positive signal)

Usage:
    python trigger_engine_v1.py                       # auto-detect the series
    python trigger_engine_v1.py --current-only        # this month's changes only
    python trigger_engine_v1.py --production-csv runs/2026-05-13/client_health_scores_2026-05-13.csv

Outputs land in trigger_reports/:
    trigger_report_{score_date}.csv     — full detail, one row per trigger
    trigger_summary_{score_date}.txt    — the plain-text brief a CS rep reads

PROVENANCE — read before trusting this file.
    Reconstructed 2026-09-16 from TRIGGER_ENGINE_V2_PATCH.md plus the shipped
    outputs in trigger_reports/ (the original was never committed and was lost).
    Thresholds recovered from those outputs are exact; three values could not be
    observed and are marked RECONSTRUCTED below.

    It also FIXES the bug that produced those outputs: the shipped engine built
    its history from the unweighted runs/historical/ CSVs while taking the
    latest month from the V3.3.0-weighted production canonical. Four of the
    eleven 2026-05-13 triggers were artifacts of that mismatch rather than
    client behaviour. This version detects each input's weighting scheme and
    refuses to run on a mixed series.
"""

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

# Composite must fall at least this far for a score_drop.  Recovered exactly:
# the smallest standalone score_drop in the shipped report is 10.1 pts.
SCORE_DROP_THRESHOLD = 10.0

# band_transition_down/up only fires if the composite ALSO moved this far.
# Recovered exactly: the smallest shipped band_transition_down delta is 3.0.
# Suppresses boundary noise (vic 80.0 -> 78.9, ali 80.0 -> 79.9).
BAND_TRANSITION_MIN_SCORE_DELTA = 3.0

# Consecutive months in a distress band before chronic_at_risk fires.
# RECONSTRUCTED — the shipped report only shows orgs at 7 months (krb, tel) and
# at 1 month (hmjc, st), so any value in 2..7 fits the evidence. 3 is the
# conventional choice and matches the README §10 "sustained distress" framing.
CHRONIC_MIN_MONTHS = 3

DISTRESS_BANDS = {"At Risk", "Critical"}

# oscillating_band: longest trailing window (up to MAX) in which the band
# changed on EVERY consecutive pair and exactly two distinct bands appear.
# Recovered exactly from bp: 5 alternating transitions since 2025-12-31.
OSCILLATION_MIN_TRANSITIONS = 4
OSCILLATION_MAX_LOOKBACK = 8

# support_fire open longer than this many days.
FIRE_DURATION_DAYS = 14

# ARR tiers drive urgency. Recovered exactly from the shipped report:
# Tier 1 min $25,200 / Tier 2 $10,365-$24,029 / Tier 3 max $9,540.
ARR_TIERS = [(25000, "Tier 1 (>=$25k)", "Immediate"),
             (10000, "Tier 2 ($10-25k)", "High"),
             (0,     "Tier 3 (<$10k)",   "Standard")]

TRIGGER_ORDER = ["new_ghost", "oscillating_band", "chronic_at_risk",
                 "fire_duration", "band_transition_down", "score_drop",
                 "band_transition_up"]

DIMENSIONS = [("engagement_score", "Engagement"),
              ("adoption_score", "Adoption"),
              ("value_delivery_score", "Value Delivery"),
              ("operational_health_score", "Ops")]

# CS_ACTIONS[trigger_type][urgency].  Every Standard/High string here is
# verbatim from the shipped report. The three Immediate strings marked
# RECONSTRUCTED were never exercised (no Tier 1 account hit those types).
CS_ACTIONS = {
    "new_ghost": {
        "Immediate": "Immediate CS call — paying account with zero logins. Confirm whether the account is still live before any renewal conversation.",
        "High": "Call this week — paying account with zero logins. Establish whether reps have moved off the platform.",
        "Standard": "Confirm account status. Zero logins against active ARR needs an explanation before the next renewal.",
    },
    "oscillating_band": {
        # From TRIGGER_ENGINE_V2_PATCH.md Change 6, verbatim.
        "Immediate": "Structural instability at high-ARR account — 4+ months alternating bands. CS leadership review required. Do not treat as a routine check-in.",
        "High": "Assign a dedicated CS owner. This account has failed to stabilize — current touch cadence is insufficient.",
        "Standard": "Escalate from reactive to proactive. Review call history; account is not responding to current intervention.",
    },
    "chronic_at_risk": {
        "Immediate": "Executive escalation — sustained distress at a top-ARR account. Involve CS leadership and agree a save plan this week.",  # RECONSTRUCTED
        "High": "Formal save play — schedule intervention call, identify specific recovery actions.",
        "Standard": "Escalate from watch to active intervention. Assign dedicated save-play owner.",
    },
    "fire_duration": {
        "Immediate": "Support fire open past SLA at a top-ARR account. Escalate to support leadership today.",  # RECONSTRUCTED
        "High": "Support fire has been open too long. Chase the ticket owner and give the client a status update.",
        "Standard": "Long-running support fire. Confirm the ticket is still live and the client knows where it stands.",
    },
    "band_transition_down": {
        "Immediate": "Immediate outreach — band regression at high-ARR account. Escalate to CS leadership if entering At Risk or Critical.",
        "High": "Proactive outreach within 5 business days. Note which dimension(s) drove the transition.",
        "Standard": "Log in CRM. Review on next scheduled call.",
    },
    "score_drop": {
        "Immediate": "Same-week root cause review at a top-ARR account. Bring findings to CS leadership.",  # RECONSTRUCTED
        "High": "CS-led root cause review within 1 week. Flag in weekly CS meeting.",
        "Standard": "Add to watch list. Review on next scheduled call.",
    },
    "band_transition_up": {
        "Immediate": "Acknowledge improvement on next call. Document what changed — this is a reference story at this ARR.",  # RECONSTRUCTED
        "High": "Acknowledge improvement on next call. Document what changed.",
        "Standard": "Positive signal — note in CRM.",
    },
}

OUTPUT_COLS = ["urgency", "trigger_type", "org_shortname", "org_name", "run_date",
               "prior_date", "arr", "arr_tier", "bundle", "score_now", "score_prior",
               "band_now", "band_prior", "eng_now", "ado_now", "val_now", "ops_now",
               "top_dim_driver", "detail", "cs_action", "composite_narrative"]


# ---------------------------------------------------------------------------
# INPUT LOADING + WEIGHTING-SCHEME GUARD
# ---------------------------------------------------------------------------

def _truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes")


def detect_weighting(df):
    """Infer which weighting scheme produced a scorecard, from the data itself.

    The canonical CSV does not record the scheme, so compare each row's stored
    composite against both candidate recomputations and see which one wins.
    Rows under a §5.1/§5.2 override are skipped — their composite is a cap, not
    a weighted average, so it carries no information about the weights.
    """
    schemes = {"equal": (.25, .25, .25, .25), "v330": (.25, .20, .35, .20)}
    votes = {k: 0 for k in schemes}
    checked = 0
    for _, r in df.iterrows():
        if _truthy(r.get("behavioral_floor_applied")) or _truthy(r.get("ghost_account")):
            continue
        dims = [(r[c], w) for (c, _), w in zip(DIMENSIONS, [1, 1, 1, 1]) if pd.notna(r[c])]
        if len(dims) < 2 or pd.isna(r.get("composite_score")):
            continue
        checked += 1
        for name, ws in schemes.items():
            avail = [(r[c], w) for (c, _), w in zip(DIMENSIONS, ws) if pd.notna(r[c])]
            tot = sum(w for _, w in avail)
            if len(set(w for _, w in avail)) == 1:
                val = round(sum(s for s, _ in avail) / len(avail), 1)
            else:
                val = round(sum(s * w for s, w in avail) / tot, 1)
            if abs(val - r["composite_score"]) <= 0.051:
                votes[name] += 1
    if not checked:
        return "unknown", 0.0
    best = max(votes, key=votes.get)
    return best, votes[best] / checked


def load_series(history_dirs, production_csv=None):
    """Load every canonical scorecard into one frame, newest run last."""
    paths = []
    for d in history_dirs:
        for p in sorted(Path(d).rglob("client_health_scores_*.csv")):
            if "formatted" in p.name or "_archive" in p.parts:
                continue
            paths.append(p)
    if production_csv:
        pp = Path(production_csv)
        if pp not in paths:
            paths.append(pp)
    if not paths:
        sys.exit("[ERROR] No canonical scorecards found. Pass --history-dir / --production-csv.")

    frames, schemes = [], {}
    for p in sorted(set(paths)):
        df = pd.read_csv(p)
        if "run_date" not in df.columns:
            continue
        scheme, conf = detect_weighting(df)
        rd = str(df["run_date"].iloc[0])[:10]
        schemes[rd] = (scheme, conf, p)
        frames.append(df)

    series = pd.concat(frames, ignore_index=True)
    series["run_date"] = series["run_date"].astype(str).str[:10]
    series = series.drop_duplicates(subset=["org_shortname", "run_date"], keep="last")
    return series.sort_values(["org_shortname", "run_date"]), schemes


def enforce_single_scheme(schemes, allow_mixed=False):
    """Refuse to compare months scored by different engines.

    This is the bug that produced the shipped 2026-05-13 report: six unweighted
    historical months compared against one V3.3.0-weighted month. Four of the
    eleven triggers at that run_date were artifacts of the engine change.
    """
    found = {s for s, _, _ in schemes.values()}
    print("[INFO] Weighting scheme per snapshot:")
    for rd in sorted(schemes):
        s, c, p = schemes[rd]
        print(f"         {rd}  {s:8s} (confidence {c:.0%})  {p}")
    if len(found) <= 1:
        return
    msg = ("[ERROR] Mixed weighting schemes across the series: "
           + ", ".join(sorted(found)) + ".\n"
           "        Month-over-month deltas would reflect the engine change, not the client.\n"
           "        Re-run health_operator_v3.py with one --weights value for every month,\n"
           "        or pass --allow-mixed-weights if you accept contaminated deltas.")
    if allow_mixed:
        print(msg.replace("[ERROR]", "[WARN] "))
        print("[WARN]  Continuing anyway because --allow-mixed-weights was passed.")
    else:
        sys.exit(msg)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def arr_tier(arr):
    arr = 0 if pd.isna(arr) else float(arr)
    for floor, label, urgency in ARR_TIERS:
        if arr >= floor:
            return label, urgency
    return ARR_TIERS[-1][1], ARR_TIERS[-1][2]


def top_driver(prior, curr, direction):
    """Dimension with the largest decline (down) or gain (up) between two runs."""
    deltas = []
    for i, (col, label) in enumerate(DIMENSIONS):
        a, b = prior.get(col), curr.get(col)
        if pd.notna(a) and pd.notna(b):
            deltas.append((b - a, i, label))
    if not deltas:
        return ""
    # Ties break by DIMENSIONS order (Engagement first), not alphabetically —
    # matches the shipped engine. A four-way tie at 0.0 means nothing actually
    # moved, which the mixed-weighting guard now prevents from reaching here.
    key = min(deltas, key=lambda d: (d[0], d[1])) if direction == "down" \
        else max(deltas, key=lambda d: (d[0], -d[1]))
    return key[2]


def base_row(curr, prior_date, trigger_type, driver=""):
    label, urgency = arr_tier(curr.get("arr"))
    return {
        "urgency": urgency, "trigger_type": trigger_type,
        "org_shortname": curr["org_shortname"], "org_name": curr.get("org_name"),
        "run_date": curr["run_date"], "prior_date": prior_date,
        "arr": curr.get("arr"), "arr_tier": label, "bundle": curr.get("bundle"),
        "score_now": curr.get("composite_score"), "score_prior": None,
        "band_now": curr.get("health_band"), "band_prior": None,
        "eng_now": curr.get("engagement_score"), "ado_now": curr.get("adoption_score"),
        "val_now": curr.get("value_delivery_score"), "ops_now": curr.get("operational_health_score"),
        "top_dim_driver": driver, "detail": "",
        "cs_action": CS_ACTIONS[trigger_type][urgency],
        "composite_narrative": curr.get("composite_narrative", ""),
    }


# ---------------------------------------------------------------------------
# DETECTION
# ---------------------------------------------------------------------------

def detect_triggers(series, current_only=False):
    dates = sorted(series["run_date"].unique())
    date_ix = {d: i for i, d in enumerate(dates)}
    latest = dates[-1]
    triggers = []

    for org, g in series.groupby("org_shortname"):
        runs = g.sort_values("run_date").to_dict("records")
        if len(runs) < 2:
            continue

        pairs = range(len(runs) - 1, len(runs)) if current_only else range(1, len(runs))
        for i in pairs:
            if i < 1:
                continue
            prior, curr = runs[i - 1], runs[i]
            # Only compare adjacent snapshots. An org skipped for a few months
            # (new-org exclusion, or absent from the MAL) would otherwise show a
            # multi-month swing as a single month-over-month move — e.g. prog is
            # missing Dec–Feb, so its Nov→Mar pair is a 4-month jump, not a
            # transition worth paging a CS rep about.
            if date_ix[curr["run_date"]] - date_ix[prior["run_date"]] != 1:
                continue
            sp, sn = prior.get("composite_score"), curr.get("composite_score")
            bp, bn = prior.get("health_band"), curr.get("health_band")

            # --- new_ghost
            if _truthy(curr.get("ghost_account")) and not _truthy(prior.get("ghost_account")):
                r = base_row(curr, prior["run_date"], "new_ghost")
                r.update(score_prior=sp, band_prior=bp,
                         detail=f"Ghost-account flag fired: {curr.get('ghost_account_note') or 'paying account with no logins'}")
                triggers.append(r)

            # --- fire_duration
            days = curr.get("support_fire_days_open")
            if _truthy(curr.get("support_fire")) and pd.notna(days) and float(days) > FIRE_DURATION_DAYS:
                r = base_row(curr, prior["run_date"], "fire_duration")
                r.update(score_prior=sp, band_prior=bp,
                         detail=f"Support fire open {int(days)} days (> {FIRE_DURATION_DAYS})")
                triggers.append(r)

            if pd.isna(sp) or pd.isna(sn) or bp is None or bn is None:
                continue
            delta = sn - sp
            big_enough = abs(delta) >= BAND_TRANSITION_MIN_SCORE_DELTA

            # --- band transitions
            if bp != bn and big_enough:
                direction = "down" if delta < 0 else "up"
                ttype = f"band_transition_{direction}"
                drv = top_driver(prior, curr, direction)
                r = base_row(curr, prior["run_date"], ttype, drv)
                verb = "regressed" if direction == "down" else "improved"
                r.update(score_prior=sp, band_prior=bp,
                         detail=f"Band {verb}: {bp} → {bn}" + (f" | Driver: {drv}" if drv else ""))
                triggers.append(r)

            # --- score_drop
            if delta <= -SCORE_DROP_THRESHOLD:
                drv = top_driver(prior, curr, "down")
                r = base_row(curr, prior["run_date"], "score_drop", drv)
                r.update(score_prior=sp, band_prior=bp,
                         detail=f"Composite dropped {abs(delta):.1f} pts ({sp:.1f} → {sn:.1f})"
                                + (f" | Driver: {drv}" if drv else ""))
                triggers.append(r)

        # --- chronic_at_risk (full history, emitted at latest only)
        bands = [r.get("health_band") for r in runs]
        streak = 0
        for b in reversed(bands):
            if b in DISTRESS_BANDS:
                streak += 1
            else:
                break
        if streak >= CHRONIC_MIN_MONTHS and runs[-1]["run_date"] == latest:
            start = runs[len(runs) - streak]["run_date"]
            r = base_row(runs[-1], start, "chronic_at_risk")
            r["detail"] = f"{streak} consecutive months in distress band (since {start})"
            triggers.append(r)

        # --- oscillating_band (full history, emitted at latest only)
        if runs[-1]["run_date"] == latest:
            osc = _oscillation(runs)
            if osc:
                n_trans, start, pair = osc
                r = base_row(runs[-1], start, "oscillating_band")
                r["band_prior"] = runs[-(n_trans + 1)].get("health_band")
                r["detail"] = (f"{n_trans} months alternating between {pair[0]} and {pair[1]} "
                               f"(since {start})")
                triggers.append(r)

    return _dedupe(triggers, latest)


def _oscillation(runs):
    """Longest trailing window where the band changed on every consecutive pair
    and exactly two distinct bands appear. Returns (n_transitions, start, pair).

    Counts raw band history: an org that flips between two bands every month is
    unstable whether or not each individual hop clears the 3.0-pt delta filter
    (Open Question C — the pattern is the signal, not the size of each step)."""
    bands = [r.get("health_band") for r in runs]
    best = None
    for n in range(min(OSCILLATION_MAX_LOOKBACK, len(bands) - 1), OSCILLATION_MIN_TRANSITIONS - 1, -1):
        window = bands[-(n + 1):]
        if any(b is None for b in window):
            continue
        if all(window[j] != window[j + 1] for j in range(len(window) - 1)) and len(set(window)) == 2:
            pair = sorted(set(window))
            best = (n, runs[-(n + 1)]["run_date"], pair)
            break
    return best


def _dedupe(triggers, latest):
    """Change 2 — merge band_transition_down + score_drop for the same org/month.
    Change 3 — a pattern-level trigger supersedes point-in-time ones at latest."""
    by_key = {}
    for t in triggers:
        by_key.setdefault((t["org_shortname"], t["run_date"]), []).append(t)

    drop = set()
    for key, ts in by_key.items():
        types = {t["trigger_type"]: t for t in ts}
        if "band_transition_down" in types and "score_drop" in types:
            types["band_transition_down"]["detail"] += " | Also a score_drop trigger."
            drop.add(id(types["score_drop"]))

    # Pattern-level suppression at the latest run only.
    pattern_orgs = {t["org_shortname"] for t in triggers
                    if t["trigger_type"] in ("chronic_at_risk", "oscillating_band")
                    and t["run_date"] == latest}
    for t in triggers:
        # DECISION A: suppress band_transition_down only. A concurrent score_drop
        # quantifies how fast a known-bad account is still falling, which the
        # pattern trigger does not say — that stays visible.
        if (t["org_shortname"] in pattern_orgs and t["run_date"] == latest
                and t["trigger_type"] == "band_transition_down"):
            drop.add(id(t))

    kept = [t for t in triggers if id(t) not in drop]
    order = {k: i for i, k in enumerate(TRIGGER_ORDER)}
    kept.sort(key=lambda t: (order.get(t["trigger_type"], 99),
                             -(t["arr"] or 0), t["org_shortname"], t["run_date"]))
    return kept


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------

def write_outputs(triggers, score_date, out_dir, current_only=False):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"trigger_report_{score_date}.csv"
    txt_path = out_dir / f"trigger_summary_{score_date}.txt"

    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUTPUT_COLS, extrasaction="ignore")
        w.writeheader()
        for t in triggers:
            w.writerow(t)

    ups = [t for t in triggers if t["trigger_type"] == "band_transition_up"]
    title = f"Health V3.3 Trigger Report{' (Current Month)' if current_only else ''} — {score_date}"
    L = [title, "=" * 55, "", f"Total triggers: {len(triggers)}", "", "By urgency:"]
    for u in ("Immediate", "High", "Standard"):
        L.append(f"  {u:<12}: {sum(1 for t in triggers if t['urgency'] == u)}")
    L += ["", f"Positive signals (band_up): {len(ups)}", "", "By trigger type:"]
    for k in TRIGGER_ORDER:
        L.append(f"  {k:<22}: {sum(1 for t in triggers if t['trigger_type'] == k)}")

    def fmt(t):
        out = [f"  [{t['trigger_type']}] {t['org_shortname']} | {t['run_date']} | "
               f"ARR ${(t['arr'] or 0):,.0f} ({t['arr_tier']})"]
        sp = "—" if t["score_prior"] is None or pd.isna(t["score_prior"]) else f"{t['score_prior']:.1f}"
        bp = t["band_prior"] or "—"
        out.append(f"  Score: {sp} → {t['score_now']:.1f}  Band: {bp} → {t['band_now']}")
        out.append(f"  {t['detail']}")
        out.append(f"  ACTION: {t['cs_action']}")
        return "\n".join(out)

    for label, level in [("IMMEDIATE", "Immediate"), ("HIGH PRIORITY", "High"),
                         ("STANDARD", "Standard")]:
        items = [t for t in triggers
                 if t["urgency"] == level and t["trigger_type"] != "band_transition_up"]
        L += ["", "=" * 55, f"{label} ({len(items)} triggers)", "=" * 55, ""]
        L += ["\n".join([fmt(t), ""]) for t in items] or ["  (none)", ""]

    L += ["", "=" * 55, f"POSITIVE SIGNALS — band improvements ({len(ups)})", "=" * 55, ""]
    for t in ups:
        drv = f" | Driver: {t['top_dim_driver']}" if t["top_dim_driver"] else ""
        L.append(f"  [{t['trigger_type']}] {t['org_shortname']} | {t['run_date']} | "
                 f"ARR ${(t['arr'] or 0):,.0f} ({t['arr_tier']})")
        L.append(f"  Score: {t['score_prior']:.1f} → {t['score_now']:.1f}  "
                 f"Band: {t['band_prior']} → {t['band_now']}{drv}")
        L.append(f"  ACTION: {t['cs_action']}")
        L.append("")

    txt_path.write_text("\n".join(L) + "\n")
    print(f"[OK] Wrote {csv_path} ({len(triggers)} triggers)")
    print(f"[OK] Wrote {txt_path}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Health V3 trigger engine")
    p.add_argument("--history-dir", action="append", default=None,
                   help="Directory tree of canonical scorecards (repeatable). "
                        "Default: runs/historical and runs/")
    p.add_argument("--production-csv", default=None,
                   help="The latest canonical CSV, if it lives outside --history-dir")
    p.add_argument("--output-dir", default="trigger_reports")
    p.add_argument("--current-only", action="store_true",
                   help="Limit month-over-month detection to the most recent pair")
    p.add_argument("--allow-mixed-weights", action="store_true",
                   help="Proceed even if the series mixes weighting schemes (not recommended)")
    args = p.parse_args()

    hist = args.history_dir or ["runs/historical", "runs"]
    series, schemes = load_series(hist, args.production_csv)
    enforce_single_scheme(schemes, args.allow_mixed_weights)

    dates = sorted(series["run_date"].unique())
    print(f"[OK] {len(dates)} snapshots, {series['org_shortname'].nunique()} orgs "
          f"({dates[0]} → {dates[-1]})")

    triggers = detect_triggers(series, current_only=args.current_only)
    write_outputs(triggers, dates[-1], args.output_dir, args.current_only)


if __name__ == "__main__":
    main()
