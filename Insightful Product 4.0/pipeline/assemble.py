"""Assembly: signals + gather + posture → Jinja2 → MD draft.

Single responsibility: rendering. This module never runs SQL, never
detects signals, never makes editorial judgments. It picks the right
template per mode, fills slots, and concatenates.

The Jinja2 templates in templates/ are derived from the existing PASS3
MDs — treat those as the gold-standard reference; templates are their
slotted form.

Output convention:
  outputs/{org}_DRAFT_{date}.md       — Mode-1 / Mode-1 Tier-1 degraded
  outputs/{org}_GATESTOP_{date}.md    — Mode 2 / Gate-STOP

The DRAFT suffix is intentional — these are inputs to surgical hand-edit
per SURGICAL_EDIT_GUIDE.md.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from . import __version__, config
from .gather import GatherBundle
from .preflight import RunPosture
from .signals import Signal


_env: Optional[Environment] = None


def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(config.TEMPLATE_DIR)),
            undefined=StrictUndefined,
            autoescape=select_autoescape(disabled_extensions=(), default_for_string=False),
            keep_trailing_newline=True,
            trim_blocks=False,
            lstrip_blocks=False,
        )
        # T1-1: the hero picks one finding per NARRATIVE ARC BAND so its three
        # slots span momentum → intelligence → opportunity → risk. Exposed as a
        # global so the band mapping stays defined once, in signals.py.
        from .signals import SIGNAL_ARC_ORDER

        _env.globals["signal_arc_band"] = lambda kind: SIGNAL_ARC_ORDER.get(kind, 99)
    return _env


def _derive_org_display_name(org: str, profile_text: str) -> str:
    """Pull the display name from the profile H1 (same rules as report_render.naming).
    Falls back to cache.resolve_org_name() (not a bare title-case) when there's
    no profile text — though after profile auto-derivation there always is one.
    """
    from report_render.naming import parse_display_name_from_profile_text

    from .cache import resolve_org_name

    fallback = resolve_org_name(org)
    return parse_display_name_from_profile_text(profile_text, fallback)


def assemble_report(
    *,
    posture: RunPosture,
    gather: GatherBundle,
    signals: list[Signal],
    profile_text: str,
    hero_framing: Optional[str] = None,
    talking_points: Optional[list[str]] = None,
    coaching_narratives: Optional[list[str]] = None,
    play_framing: Optional[list[str]] = None,
    growth_connective: Optional[dict[str, str]] = None,
    outreach_framing: Optional[str] = None,
    inline_draft_profile: bool = False,
    plays: Optional[list[dict]] = None,
) -> str:
    """Top-level assembly. Always uses _base.md.j2 regardless of mode.

    Gate-STOP orgs still get the _GATESTOP_ filename suffix (via write_draft),
    so run.sh can detect them and exit 2. But the template is the same for all
    modes — thin-data sections degrade gracefully through their own fallback paths.
    """
    from . import fact_bundles as fb
    from .availability import build_availability, outreach_mix
    from .hero_sanitizer import sanitize_hero_framing

    plays = plays or []
    play_framing_by_type = fb.index_play_framing(plays, play_framing)
    availability = build_availability(gather, posture, plays)
    # T1-1: the arc-ordered summary set (momentum → intelligence → opportunity →
    # risk, >=3 positive, finding #1 positive). The hero template used to build
    # its own `top_signals` with `signals | sort(attribute='rank', reverse=True)`,
    # which THREW THE ARC AWAY and re-imposed rank-descending — and since
    # rank = surprise x dollar_impact x actionability, declines always won. That
    # was the third and deepest of three layers defeating the arc.
    from .signals import signal_summary_set

    context = {
        "posture": posture,
        "gather": gather,
        "signals": signals,
        "top_signals": signal_summary_set(signals),
        "profile_text": profile_text,
        "hero_framing": sanitize_hero_framing(hero_framing),
        "talking_points": talking_points,
        "coaching_narratives": coaching_narratives,
        "play_framing": play_framing,
        "play_framing_by_type": play_framing_by_type,
        "plays": plays,
        "availability": availability,
        "outreach_mix": outreach_mix(gather),
        "growth_connective": growth_connective,
        "outreach_framing": outreach_framing,
        "inline_draft_profile": inline_draft_profile,
        "org_display_name": _derive_org_display_name(posture.org, profile_text),
        "pipeline_version": __version__,
    }

    template = env().get_template("_base.md.j2")
    return template.render(**context)


def write_draft(md_text: str, org: str, date: str, *, gatestop: bool = False) -> Path:
    suffix = "GATESTOP" if gatestop else "DRAFT"
    out = config.OUTPUTS_DIR / f"{org}_{suffix}_{date}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md_text, encoding="utf-8")
    return out
