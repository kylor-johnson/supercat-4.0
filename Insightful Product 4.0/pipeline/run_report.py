"""CLI: run_report.py — produce a PASS3-quality MD draft from cached data.

    .venv-renderer/bin/python -m pipeline.run_report --org sarreid
    .venv-renderer/bin/python -m pipeline.run_report --org cci --date 2026-06-30
    .venv-renderer/bin/python -m pipeline.run_report --org any-org

Reads from cache/{org}/{date}/ (populate it first with populate_cache.py).
Writes outputs/{org}_DRAFT_{date}.md  (or _GATESTOP_).

There is no profile gate: if profiles/{org}.md doesn't exist yet, it is
auto-derived from the live posture (and cached data) and written before
the report is assembled, so every org SHIPs on first run. The profile is
a correction layer you edit AFTER seeing the output, not a gate that
blocks you from seeing it — see handoffs/profile_gate_removal.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from . import assemble, cache, config, gather, narrative, preflight, signals, smoke_check


def _emit_inline_draft_profile(org: str, posture, score_date: str) -> Path:
    """Auto-derive profiles/{org}.md from the live posture and cached data.
    Every section is filled from a data source (see handoffs/profile_gate_removal.md
    §"The profile contains 8 sections"); nothing is left as a placeholder that
    would block shipping. The client should still review and correct any
    section after seeing the output.

    Never overwrites an existing profile (idempotent per org) — if
    profiles/{org}.md already exists (ratified or previously auto-derived),
    this returns immediately without touching it.
    """
    path = config.PROFILES_DIR / f"{org}.md"
    if path.exists():
        return path

    client_name = cache.resolve_org_name(org)
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    through_date = posture.report_through_date or today

    # §3 Channel model
    ecat_share_pct = (
        posture.ecat_ltm_confirmed_gmv * 100 / posture.inv_ltm_net
        if posture.inv_ltm_net
        else 0.0
    )

    # §4 House / sample screens — config/house_rep_exclusions.json
    exclusions = config.load_house_exclusions()
    org_excludes = exclusions.get("exclude", {}).get(str(posture.organization_id))
    if org_excludes:
        house_screen_note = (
            f"Per-org exclusions on file for `organization_id={posture.organization_id}`: "
            + ", ".join(f"`{name}`" for name in org_excludes)
            + "."
        )
    else:
        auto_rules = ", ".join(f"`{r}`" for r in exclusions.get("auto_rules", []))
        house_screen_note = (
            f"No per-org exclusions on file for `{org}` — auto-rules only "
            f"(name patterns: {auto_rules})."
        )

    # §6 Structural concentration — read Q-ECON-CONC directly (gather bundle
    # isn't built yet at this point in the pipeline). Use the actual run
    # cache dir (score_date), not report_through_date, which can be blank
    # for NONE-confidence orgs and would otherwise miss the cached CSV.
    cache_paths = cache.CachePaths.for_run(org, score_date)
    conc = gather.load_concentration(gather._read_csv(cache_paths.csv_for("Q-ECON-CONC")))
    if conc is not None:
        conc_note = (
            f"Top-1 customer = **{conc.top1_share:.1f}%** of LTM invoiced net "
            f"(top-10 = {conc.top10_share:.1f}%, HHI {conc.hhi:.0f}). "
            "Confirm whether this reflects a known-structural account "
            "(e.g. a marketplace/drop-ship partner) before treating it as a finding."
        )
    else:
        conc_note = "No `Q-ECON-CONC` data cached for this run — concentration context unavailable."

    # §7 Hard-gap suppressions — derived from posture.flags (Q-ECON-00 side channels)
    flag_labels = {
        "returns_ok": "returns",
        "carrier_ok": "carrier / shipping-method mix",
        "terms_ok": "payment terms",
        "leadtime_ok": "lead-time",
        "netrev_freight_ok": "net-revenue freight adjustment",
        "leakage_dispersion_ok": "leakage dispersion",
        "channel_ok": "channel attribution",
    }
    detected_suppressions = [
        label for key, label in flag_labels.items() if posture.flags.get(key) is False
    ]
    if detected_suppressions:
        suppressions_note = "Detected from live side-channel flags: " + "; ".join(
            f"no {label} data" for label in detected_suppressions
        ) + "."
    else:
        suppressions_note = "No side-channel gaps detected in the live flags for this run."
    always_missing_note = (
        "Always suppressed (never in the ERP feed): margin/COGS, AR/DSO aging, "
        "competitive-loss reasons."
    )

    text = f"""# Client Profile — {client_name} (`{org}`)

> **Status:** AUTO-DERIVED {today} — review output and correct any section that needs it.
>
> This profile was auto-populated by `pipeline/run_report.py` from live
> preflight/cache data (see `handoffs/profile_gate_removal.md`). It is
> treated as a ratified profile for pipeline purposes — SHIP output is not
> gated on human review. Edit any section below and re-run to correct it.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | {client_name} | `cache.resolve_org_name()` |
| `organization_id` (Postgres) | `{posture.organization_id}` | Q-ECON-00 preflight |
| Shortname | `{org}` | live |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed → {through_date} |

## 2. Business model / segment

- **Model:** _(one line, factual — manufacturer / distributor / marketplace seller / hybrid)_
- **Client segment (SuperCat v4.0, stamped):** _STAMP FROM MASTER._ Look up `{org}` (org_id `{posture.organization_id}`) in `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` and copy the `v4_segment` label WITHOUT its leading "N. " (Luxury Specification | Premium Trade Brand | Mid-Market Multi-Channel | Volume Distribution). Also stamp **How they sell** (`how_they_sell`), **What they sell** (`what_they_sell`), **Who they sell to** (`who_they_sell_to`), and **Price (continuous, not a boundary)** ≈ `$best_price` (a correlate, not the classifier), then cite the MASTER row with the verified org_id. If `{org}` is NOT on the stamped 109-org roster, mark **Client segment: unassigned** and do NOT infer one. This is the client's selling-motion class (Workstream A); it is NOT the frozen in-client customer segmentation (Q-SEG-DERIVE, Spine §8).

## 3. Channel model (how they sell)

Preflight surface (live, {through_date}):
- `channel_posture` = `{posture.channel_posture}` ({posture.distinct_origins} distinct origins on {posture.booked_rows_ltm:,} booked rows)
- eCat confirmed GMV LTM = ${posture.ecat_ltm_confirmed_gmv:,.0f} ({ecat_share_pct:.1f}% of invoiced)

## 4. House / sample / marketplace accounts to screen

{house_screen_note}

## 5. Buyer-type context

Default editorial standard: treat one-time buyers as a **conversion opportunity**, not assumed churn.

## 6. Structural concentration (context, NOT a finding)

{conc_note}

## 7. Report mode default + scope exclusions

- **Default mode (live gate):** `{posture.report_mode}` — the gate resolved this at preflight.
- **Hard-gap suppressions:** {suppressions_note} {always_missing_note}

## 8. Sensitive callouts — per-client scrubbing policy

None configured — review output and add overrides if needed.

---

### Ratification log

- {today} — AUTO-DERIVED by `pipeline/run_report.py` — pipeline
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--org", required=True, help="Org shortname")
    p.add_argument("--date", default=None, help="YYYY-MM-DD (UTC). Defaults to today UTC.")
    p.add_argument(
        "--cohort-validation",
        action="store_true",
        help="Deprecated — profile auto-derivation is now the default. Kept for backward compatibility.",
    )
    p.add_argument(
        "--no-narrative",
        action="store_true",
        help="Skip all LLM prose slots; use deterministic template prose only.",
    )
    p.add_argument(
        "--no-smoke",
        action="store_true",
        help="Skip the smoke_check pass after writing.",
    )
    args = p.parse_args()

    score_date = args.date or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    cache_paths = cache.CachePaths.for_run(args.org, score_date)
    if not cache_paths.exists():
        print(f"ERROR: no cache at {cache_paths.dir}", file=sys.stderr)
        print(f"  run: python -m pipeline.populate_cache --org {args.org} --date {score_date}", file=sys.stderr)
        return 2

    profile_path = config.PROFILES_DIR / f"{args.org}.md"
    has_ratified = profile_path.exists()

    try:
        # cohort_validation=True unconditionally: the profile gate inside
        # preflight.resolve_mode is now a no-op by design (see
        # handoffs/profile_gate_removal.md) — a missing profile no longer
        # forces Gate-STOP, since one is auto-derived a few lines down.
        # This has no effect for orgs that already have a ratified profile
        # (has_ratified_profile short-circuits that branch either way).
        posture = preflight.run(args.org, score_date, cohort_validation=True)
    except NotImplementedError as e:
        print(f"STUB: preflight.run ({e})")
        return 2
    print(f"preflight: mode={posture.report_mode} confidence={posture.commerce_confidence} tier={posture.rep_identity_tier}")

    if not has_ratified:
        _emit_inline_draft_profile(args.org, posture, score_date)
        profile_path = config.PROFILES_DIR / f"{args.org}.md"
        has_ratified = True
        print(f"auto-derived profile emitted: {profile_path.relative_to(config.WORKSPACE_ROOT)}")

    try:
        bundle = gather.gather_all(args.org, score_date)
    except NotImplementedError as e:
        print(f"STUB: gather.gather_all ({e})")
        return 2

    fired = signals.detect_all(bundle, posture)
    print(f"signals: {len(fired)} fired")

    profile_text = profile_path.read_text(encoding="utf-8") if has_ratified else ""

    from . import fact_bundles as fb
    from .slot_validator import (
        align_talking_points,
        _narrative_contradicts_card,
        align_coaching_narratives,
        check_play_alignment,
        reorder_play_framing,
    )

    thresholds = signals.resolve_thresholds(posture, bundle)
    plays = fb.build_plays_from_gather(bundle, posture, fired, thresholds)
    # W3/S2: ONE coaching-card definition. This list keys slot C's prose and
    # `align_coaching_narratives`; the template renders the same list through
    # `availability.coaching_cards`. Re-deriving it here is how the narratives
    # would end up attached to the wrong cards the moment the gate moves.
    _cards = signals.coaching_card_reps(bundle.rep_risks, bundle.decay, thresholds)[:5]
    card_reps = [card.risk for card in _cards]
    slot_d_fail = False

    # Multi-slot LLM prose generation
    import json as _json

    prose_vars: dict = {}
    prose_file = config.OUTPUTS_DIR / f"{args.org}_prose_{score_date}.json"
    bundles_path = config.OUTPUTS_DIR / f"{args.org}_bundles_{score_date}.json"

    if not args.no_narrative:
        # Always write bundles first (enables agent-driven prose generation)
        try:
            # T1-1: signal_summary_set applies the narrative arc
            # (momentum → intelligence → opportunity → risk), the >=3-positive
            # floor, finding-#1-positive and max-4-per-section diversity. It was
            # implemented, correct, and had ZERO callers — both hero paths used
            # raw rank-descending instead. Since rank = surprise x dollar_impact
            # x actionability and declines carry the largest dollar impact, every
            # 4.0 hero opened decline-first. That is the single biggest reason the
            # reports read as an alarm board rather than intelligence.
            top_signals = signals.signal_summary_set(fired)
            outreach_list = list(bundle.outreach_list)

            all_bundles = {
                "slot_a_bundle": fb.build_hero_bundle(posture, top_signals, bundle),
                "slot_b_bundle": fb.build_talking_points_bundle(outreach_list, posture, profile_text),
                "slot_c_bundle": fb.build_coaching_bundle(card_reps, bundle.decay, posture),
                "slot_d_bundle": fb.build_play_framing_bundle(plays, bundle, posture),
                "slot_e_bundle": fb.build_growth_connective_bundle(bundle, posture),
                "slot_f_bundle": fb.build_outreach_framing_bundle(outreach_list),
            }
            all_bundles["expected_counts"] = {
                "talking_points": len(outreach_list),
                "coaching_narratives": len(card_reps),
                "play_framing": len(plays),
                "growth_connective": 3,
                "outreach_framing": 1,
            }
            bundles_path.write_text(_json.dumps(all_bundles, default=str, indent=2), encoding="utf-8")
            print(f"bundles: {bundles_path.name}")
        except Exception as e:
            print(f"bundles: WARN could not write ({e})")

        # Check for agent-generated prose file (takes priority over API calls)
        if prose_file.exists():
            try:
                prose_data = _json.loads(prose_file.read_text(encoding="utf-8"))
                prose_vars = {
                    "hero_framing": prose_data.get("hero_framing"),
                    "talking_points": prose_data.get("talking_points"),
                    "coaching_narratives": prose_data.get("coaching_narratives"),
                    "play_framing": prose_data.get("play_framing"),
                    "growth_connective": prose_data.get("growth_connective"),
                    "outreach_framing": prose_data.get("outreach_framing"),
                }
                active = sum(1 for v in prose_vars.values() if v is not None)
                print(f"slots: loaded {active}/6 from {prose_file.name}")

                # Outreach list changed after house/DTC screen — old slot B/F
                # bodies are zipped onto the wrong rows. Fall back to template.
                if bundle.outreach_screened or bundle.outreach_reordered:
                    reasons = []
                    if bundle.outreach_screened:
                        reasons.append(
                            f"{bundle.outreach_screened} house/DTC rows screened"
                        )
                    if bundle.outreach_reordered:
                        reasons.append("actionability ranking changed row order")
                    # T1-2: re-key Slot B by account identity rather than
                    # discarding it. Slot F is a single framing sentence about
                    # the list as a whole, so a changed list genuinely
                    # invalidates it — that one still drops.
                    original_b = prose_vars.get("talking_points")
                    aligned_b = align_talking_points(
                        bundle.outreach_list, original_b
                    )
                    prose_vars["talking_points"] = aligned_b
                    prose_vars["outreach_framing"] = None
                    kept = sum(1 for b in (aligned_b or []) if b)
                    total = len(bundle.outreach_list)
                    print(
                        f"slots: re-keyed talking_points to the post-screen list "
                        f"({kept}/{total} rows matched); dropped outreach_framing "
                        f"({'; '.join(reasons)})"
                    )
                # Slot C must ship whenever coaching cards render. House-card
                # screens used to null the whole array, which left grow-row
                # cards on the decline-walk fallback (clc Envision / Lighting
                # & Locks). Re-key if the prose array drifted; never drop C
                # while _card_reps is non-empty.
                original_c = prose_vars.get("coaching_narratives")
                if card_reps:
                    aligned_c = align_coaching_narratives(card_reps, original_c)
                    # The card set is derived from the at-risk book now, so an
                    # authored body can survive the rep re-key while describing
                    # a DIFFERENT account on that rep. clc shipped "up 49%...
                    # there is no decline to chase" on a card whose subject
                    # account is down 63%. Blank a body that contradicts its own
                    # card; the slope-aware template fallback fills that row.
                    if aligned_c:
                        checked = []
                        dropped = 0
                        for body, card in zip(aligned_c, _cards[: len(aligned_c)]):
                            subject = getattr(card, "account", None)
                            is_decline = bool(
                                subject is not None
                                and getattr(subject, "is_real_decline", False)
                            )
                            if body and _narrative_contradicts_card(body, is_decline):
                                checked.append("")
                                dropped += 1
                            else:
                                checked.append(body)
                        if dropped:
                            print(
                                f"slots: dropped {dropped} coaching narrative(s) that "
                                f"contradicted their card"
                            )
                        aligned_c = checked
                    if aligned_c != original_c:
                        prose_vars["coaching_narratives"] = aligned_c
                        print(
                            "slots: re-keyed coaching_narratives to remaining cards"
                        )
                elif original_c:
                    prose_vars["coaching_narratives"] = None
                    print("slots: dropped coaching_narratives (no cards after screen)")

                original_play_framing = prose_vars.get("play_framing")
                aligned_play_framing = reorder_play_framing(
                    plays, original_play_framing
                )
                if aligned_play_framing != original_play_framing:
                    prose_vars["play_framing"] = aligned_play_framing
                    print(
                        "slots: re-keyed play_framing to ranked play order "
                        "(prose JSON unchanged)"
                    )
                d_issues = check_play_alignment(
                    plays, prose_vars.get("play_framing")
                )
                if d_issues:
                    slot_d_fail = True
                    prose_vars["play_framing"] = None
                    print("slots: SLOT-D-MISMATCH — falling back to template bodies")
                    for issue in d_issues:
                        print(f"  - {issue}")
            except Exception as e:
                print(f"slots: prose file exists but failed to load ({e})")
                prose_vars = {}
        else:
            # Try Anthropic API (works if key is set; falls back gracefully if not)
            try:
                slot_results = narrative.generate_all_slots_sync(
                    posture=posture,
                    gather=bundle,
                    signals=fired,
                    profile_text=profile_text,
                )
                prose_vars = slot_results
                if "slot_status" in slot_results:
                    print(f"slots: {slot_results['slot_status']}")
            except Exception as e:
                print(f"narrative slots: FELL BACK (orchestrator error: {e})")
                prose_vars = {}
    else:
        # Legacy: deterministic-only mode with --no-narrative
        hero = narrative.generate_hero_framing(
            posture=posture, top_signals=signals.signal_summary_set(fired),
            profile_text=profile_text,
            gather=bundle,
        )
        prose_vars = {"hero_framing": hero}

    md_text = assemble.assemble_report(
        posture=posture,
        gather=bundle,
        signals=fired,
        profile_text=profile_text,
        hero_framing=prose_vars.get("hero_framing"),
        talking_points=prose_vars.get("talking_points"),
        coaching_narratives=prose_vars.get("coaching_narratives"),
        play_framing=prose_vars.get("play_framing"),
        growth_connective=prose_vars.get("growth_connective"),
        outreach_framing=prose_vars.get("outreach_framing"),
        inline_draft_profile=not has_ratified,
        plays=plays,
    )

    gatestop = posture.report_mode == "Gate-STOP"
    out_path = assemble.write_draft(md_text, args.org, score_date, gatestop=gatestop)
    print(f"wrote: {out_path}")

    if not args.no_smoke:
        ok, issues = smoke_check.smoke(
            out_path,
            confidence=posture.commerce_confidence,
            cache_dir=cache_paths.dir,
        )
        if ok:
            print("smoke_check: PASS")
        else:
            print("smoke_check: FAIL")
            for i in issues:
                print(f"  - {i}")
            return 1

    if slot_d_fail:
        print("SLOT-D-MISMATCH: play_framing does not match selected plays — run failed")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
