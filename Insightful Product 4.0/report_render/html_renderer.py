"""Main entry point — render a PASS3 MD into a Sarreid-quality HTML.

CLI:
    python -m report_render.html_renderer \
        --md outputs/cci_PASS3_intelligence_report_2026-06-30.md \
        --profile profiles/cci.md \
        --out outputs/Currey_and_Company_CEO_intelligence_report_2026-06-30.html

The renderer is deterministic: same MD + same profile → same HTML (modulo the
ledger timestamp the operator injects). It does not query live data.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .md_parse import (
    CANONICAL_TOC,
    GATESTOP_TOC,
    ParsedReport,
    parse_md,
)
from .md_render import md_inline_to_html
from .sections import (
    render_base,
    render_channels,
    render_gatestop,
    render_growth,
    render_methodology,
    render_products,
    render_risk,
    render_summary,
    render_team,
    render_thismonth,
    render_thisweek,
)


HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(disabled_extensions=(), default_for_string=False),
    keep_trailing_newline=True,
)


# ─── Profile loading (minimal — for org display name + period framing) ──────

def load_profile_basics(profile_path: Path) -> dict:
    """Profiles are MD with a `# {Org name}` H1. We pick the display name; the
    rest of the profile content is consumed by the operator, not the renderer.

    Profile H1s vary in shape across the cohort:
        sarreid.md:  "# Client Profile — Sarreid, Ltd. (`sarreid`)"
        cci.md:      "# Currey & Company (`cci`) — eCat client profile"
        hfg.md:      "# Hubbardton Forge (`hfg`) — eCat client profile"
        kal.md:      "# Kalco Lighting (`kal`) — eCat client profile"
        sca.md:      (no ratified profile; inline draft)

    We strip the prefix and the `(shortname)` suffix to recover the org name.
    If the profile H1 isn't recognizably a clean org-name, we let the caller
    fall back to the MD's display_name.
    """
    if not profile_path or not profile_path.exists():
        return {}
    text = profile_path.read_text(encoding="utf-8")
    h1_match = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if not h1_match:
        return {"raw": text}
    h1_text = h1_match.group(1).strip()
    # Drop a leading "Client Profile — " prefix
    h1_text = re.sub(r"^Client\s+Profile\s+[—–-]\s+", "", h1_text)
    # Drop a trailing " — eCat client profile" suffix
    h1_text = re.sub(r"\s+[—–-]\s+(?:eCat\s+)?client\s+profile\s*$", "", h1_text, flags=re.I)
    # Drop a trailing "(`shortname`)" tag
    h1_text = re.sub(r"\s*\(\s*`[^`]+`\s*\)\s*$", "", h1_text)
    return {
        "display_name": h1_text.strip(),
        "raw": text,
    }


# ─── Subtitle / period derivation ───────────────────────────────────────────

_BEHAVIOR_ONLY = re.compile(
    r"behavior-only|no invoiced ERP feed", re.IGNORECASE
)

_PERIOD_LINE = re.compile(
    r"Trailing\s+12\s+months\s+through\s+([A-Z][a-z]+\s+\d{1,2}(?:,?\s*\d{4})?)",
    re.I,
)


def derive_period_line(report: ParsedReport) -> str:
    """Pull the trailing-12-months line out of the H3 sub-header or preamble."""
    candidates = [report.org_subtitle, report.preamble_md]
    for text in candidates:
        if not text:
            continue
        m = _PERIOD_LINE.search(text)
        if m:
            return (
                f"Trailing 12 months through <strong>{m.group(1)}</strong> "
                "&middot; vs the prior matching 12&nbsp;months"
            )
    return report.org_subtitle or ""


def derive_subtitle(report: ParsedReport) -> str:
    """The "Selling & Commerce Intelligence — CEO Brief" line below the org name."""
    if report.mode == "gatestop":
        return "Selling &amp; Commerce Intelligence &mdash; Gate-STOP artifact (Mode-2)"
    return "Selling &amp; Commerce Intelligence &mdash; CEO Brief"


def derive_header_badge(report: ParsedReport) -> tuple[str, str]:
    """Return (badge_html, badge_class). Sarreid uses an `info` badge with a
    read-time hint; the gate-STOP variant doesn't need one."""
    if report.mode == "gatestop":
        return "", ""
    return (
        "Read top to bottom in 60 seconds &middot; click any section to go deeper",
        "info",
    )


# ─── Body assembly (Mode-1 vs Gate-STOP) ────────────────────────────────────

def assemble_mode1(report: ParsedReport, period_line: str) -> tuple[str, str, list[dict]]:
    """Walk the canonical §5a section order, render each chunk that exists,
    and return (summary_html, body_html, toc_links).
    """
    summary_html = ""
    body_parts: list[str] = []
    rendered_ids: set[str] = set()
    toc_links: list[dict] = []

    # §1 — summary (always-expanded)
    summary_chunk = report.chunk_by_id("summary")
    if summary_chunk:
        summary_html = render_summary(summary_chunk, period_line=_eyebrow_text(report))
        rendered_ids.add("summary")
        toc_links.append({"id": "summary", "label": "60-sec read"})

    # §2 — thisweek
    thisweek_chunk = report.chunk_by_id("thisweek")
    if thisweek_chunk:
        body_parts.append(render_thisweek(thisweek_chunk))
        rendered_ids.add("thisweek")
        toc_links.append({"id": "thisweek", "label": "Do this week"})

    # §3 — thismonth
    thismonth_chunk = report.chunk_by_id("thismonth")
    if thismonth_chunk:
        body_parts.append(render_thismonth(thismonth_chunk))
        rendered_ids.add("thismonth")
        toc_links.append({"id": "thismonth", "label": "Do this month"})

    # §5 — growth
    growth_chunk = report.chunk_by_id("growth")
    if growth_chunk:
        body_parts.append(render_growth(growth_chunk))
        rendered_ids.add("growth")
        toc_links.append({"id": "growth", "label": "Growth engine"})

    # §6 — team
    team_chunk = report.chunk_by_id("team")
    if team_chunk:
        body_parts.append(render_team(team_chunk))
        rendered_ids.add("team")
        toc_links.append({"id": "team", "label": "Team"})

    # §7 — risk
    risk_chunk = report.chunk_by_id("risk")
    if risk_chunk:
        body_parts.append(render_risk(risk_chunk))
        rendered_ids.add("risk")
        toc_links.append({"id": "risk", "label": "Risk watchlist"})

    # §8 — products
    products_chunk = report.chunk_by_id("products")
    if products_chunk:
        body_parts.append(render_products(products_chunk))
        rendered_ids.add("products")
        toc_links.append({"id": "products", "label": "Products"})

    # §9 — base
    base_chunk = report.chunk_by_id("base")
    if base_chunk:
        body_parts.append(render_base(base_chunk))
        rendered_ids.add("base")
        toc_links.append({"id": "base", "label": "Dealer base"})

    # §10 — channels (may not render — kal pattern, Q-CHAN-00=NONE)
    channels_chunk = report.chunk_by_id("channels")
    if channels_chunk:
        body_parts.append(render_channels(channels_chunk))
        rendered_ids.add("channels")
        toc_links.append({"id": "channels", "label": "Channels"})

    # ERP-unlock close — NONE-feed (behavior-only) reports only. Placed after
    # channels, before methodology. Renders as a collapsible; no invoiced data.
    unlock_chunk = report.chunk_by_id("unlock")
    if unlock_chunk:
        from .sections import _wrap_collapse_section
        from .sections import _render_freeform_blocks
        body_parts.append(_wrap_collapse_section(
            section_id="unlock",
            title=md_inline_to_html(unlock_chunk.heading),
            body=_render_freeform_blocks(unlock_chunk.body_md),
            contents_blurb="What connecting an invoiced ERP feed adds",
            sub_blurb="The behavior floor above is live today; this is the brief a connected feed unlocks.",
        ))
        rendered_ids.add("unlock")
        toc_links.append({"id": "unlock", "label": "What ERP unlocks"})

    # §11/§12 — methodology (combined or split)
    gaps_chunk = report.chunk_by_id("methodology_gaps")
    trust_chunk = report.chunk_by_id("methodology_trust")
    if gaps_chunk or trust_chunk:
        body_parts.append(render_methodology(gaps_chunk, trust_chunk))
        rendered_ids.update({"methodology_gaps", "methodology_trust"})
        toc_links.append({"id": "methodology", "label": "Methodology"})

    # Appendix (cohort MDs carry this; Sarreid doesn't) — render collapsed
    appendix_chunk = report.chunk_by_id("appendix")
    if appendix_chunk:
        from .sections import _wrap_collapse_section
        from .sections import _render_freeform_blocks
        body_parts.append(_wrap_collapse_section(
            section_id="appendix",
            title=md_inline_to_html(appendix_chunk.heading),
            body=_render_freeform_blocks(appendix_chunk.body_md),
            contents_blurb="Data readiness · where the dollars come from",
            sub_blurb="Plain-English notes on sources and confidence — expand only if you want the detail.",
        ))
        rendered_ids.add("appendix")
        toc_links.append({"id": "appendix", "label": "Appendix"})

    # Catch-all for any unclassified chunks (e.g. `misc-…`)
    for chunk in report.chunks:
        if chunk.section_id in rendered_ids:
            continue
        from .sections import _wrap_collapse_section
        from .sections import _render_freeform_blocks
        body_parts.append(_wrap_collapse_section(
            section_id=chunk.section_id,
            title=md_inline_to_html(chunk.heading),
            body=_render_freeform_blocks(chunk.body_md),
            contents_blurb="",
            sub_blurb="",
        ))

    return summary_html, "\n".join(body_parts), toc_links


def _eyebrow_text(report: ParsedReport) -> str:
    """The hero eyebrow line, e.g. 'LTM invoiced · through Jun 29, 2026'.

    P0-2: a behavior-only report (COMMERCE_CONFIDENCE = NONE) has no invoice
    feed at all — its hero number is confirmed platform order volume. Labelling
    it "LTM invoiced" put those two words directly above the report's own
    sentence "There is no invoiced total in this window" (da, sca). The header
    subtitle is the rendered signal for that posture.
    """
    subtitle = report.org_subtitle or ""
    if _BEHAVIOR_ONLY.search(subtitle):
        return "Confirmed platform orders &middot; trailing 12 months"
    m = _PERIOD_LINE.search(subtitle)
    if m:
        return f"LTM invoiced &middot; through {m.group(1)}"
    return "LTM invoiced"



# ─── Footer text + ledger lines ─────────────────────────────────────────────

def derive_footer_text(report: ParsedReport, profile: dict) -> str:
    """Footer disclosure — pulled or templated."""
    org_name = profile.get("display_name") or report.org_display_name
    if report.mode == "gatestop":
        return (
            f"{org_name} &middot; Gate-STOP artifact &mdash; this org did not clear the gates Sarreid cleared. "
            "Behavior-only Rep Copilot output is the correct ceiling until an invoice feed arrives."
        )
    return (
        f"{org_name} &middot; Built from a live read of your invoice data. "
        "This is your invoiced business &mdash; billed, not collected. Built to be acted on, not filed."
    )


# ─── Public render() entry point ────────────────────────────────────────────

def render(md_path: Path, profile_path: Optional[Path] = None) -> str:
    """Render the given MD into HTML and return as a string."""
    text = md_path.read_text(encoding="utf-8")
    report = parse_md(text)
    profile = load_profile_basics(profile_path) if profile_path else {}

    period_line = derive_period_line(report)
    subtitle = derive_subtitle(report)
    badge_text, badge_cls = derive_header_badge(report)

    summary_html, body_html, toc_links = assemble_mode1(report, period_line)
    gatestop_summary = ""

    template = _env.get_template("report.html.j2")
    template_mode = "mode1"
    return template.render(
        org_display_name=profile.get("display_name") or report.org_display_name,
        subtitle=subtitle,
        period_line=period_line,
        header_badge=badge_text,
        header_badge_class=badge_cls,
        toc_links=toc_links,
        mode=template_mode,
        gatestop_summary=gatestop_summary,
        summary_html=summary_html,
        body_html=body_html,
        footer_text=derive_footer_text(report, profile),
        ledger_lines=report.footer_code_lines,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", required=True, type=Path, help="Source MD path")
    parser.add_argument("--profile", type=Path, default=None, help="Ratified profile MD path")
    parser.add_argument("--out", required=True, type=Path, help="Output HTML path")
    parser.add_argument(
        "--internal",
        action="store_true",
        help="Allow rendering Gate-STOP MDs (internal artifact only). "
             "Without this flag, Gate-STOP inputs are refused to prevent "
             "accidental CEO Brief packaging.",
    )
    args = parser.parse_args(argv)

    if not args.md.exists():
        print(f"ERROR: MD not found: {args.md}", file=sys.stderr)
        return 2
    if args.profile and not args.profile.exists():
        print(f"WARN: profile not found at {args.profile} (continuing with no profile context)", file=sys.stderr)

    text = args.md.read_text(encoding="utf-8")
    report = parse_md(text)
    if report.mode == "gatestop" and not args.internal:
        print(
            f"REFUSED: {args.md.name} is a Gate-STOP artifact (zero signal).\n"
            "  Use --internal if you intentionally need an internal-only HTML render.",
            file=sys.stderr,
        )
        return 2

    html = render(args.md, args.profile)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"rendered {args.md.name} → {args.out} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
