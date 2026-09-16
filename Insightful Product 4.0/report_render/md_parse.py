"""MD section parser — chunks a PASS3 markdown into per-section bundles.

The Insightful 4.0 CEO Brief MDs (Sarreid and the 4 cohort PASS3 outputs) follow
a recognizable §5a structure. This module's job: chunk the MD by H2 boundary,
classify each chunk into the canonical section ids (`summary`, `thisweek`,
`thismonth`, `growth`, `team`, `risk`, `products`, `base`, `channels`,
`methodology`, `appendix` for Mode-1; `gatestop_*` ids for Mode-2). The
section-specific transformers in `sections.py` consume these chunks.

The parser is defensive: cohort variants drop sections (kal has no `channels`),
degrade sections (hfg has no coaching cards), or replace the entire body with a
Gate-STOP variant (sca). We do not invent missing sections; we render what's
there.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# Canonical 13-section ids (per report_product_architecture.md §5a.1) + the
# Mode-2 Gate-STOP ids. The "id" is the HTML anchor; the "label" is the TOC pill.
CANONICAL_TOC = [
    ("summary", "60-sec read"),
    ("thisweek", "Do this week"),
    ("thismonth", "Do this month"),
    ("growth", "Growth engine"),
    ("team", "Team"),
    ("risk", "Risk watchlist"),
    ("products", "Products"),
    ("base", "Dealer base"),
    ("channels", "Channels"),
    ("methodology", "Methodology"),
]

GATESTOP_TOC = [
    ("summary", "Gate state"),
    ("preflights", "Preflights"),
    ("concentration", "User concentration"),
    ("nextaction", "Next action"),
    ("appendix", "Appendix"),
]


@dataclass
class Chunk:
    """A single H2-bounded chunk of the source MD."""
    section_id: str            # canonical id (summary, thisweek, …)
    heading: str               # the original H2 heading text (no leading ##)
    body_md: str               # MD source between this H2 and the next
    raw_heading_line: str = "" # the literal `## …` line (for round-trip)


@dataclass
class ParsedReport:
    mode: str                          # "mode1" | "gatestop"
    org_display_name: str              # H1 first token (e.g. "Sarreid, Ltd.")
    org_h1_full: str                   # the full H1 text
    org_subtitle: str                  # H3 sub-header or built default
    preamble_md: str                   # any prose between H1/H3 and first H2
    chunks: list[Chunk] = field(default_factory=list)
    footer_code_lines: list[str] = field(default_factory=list)  # `[STEP-10 LEDGER · …]` etc.

    def chunk_by_id(self, section_id: str) -> Optional[Chunk]:
        for c in self.chunks:
            if c.section_id == section_id:
                return c
        return None


# ─── H2 → section_id classification ─────────────────────────────────────────

_MODE1_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("summary",      re.compile(r"\b60[\s-]?second\s+read\b", re.I)),
    ("thisweek",     re.compile(r"\bdo\s+this\s+week\b", re.I)),
    ("thismonth",    re.compile(r"\bdo\s+this\s+month\b", re.I)),
    # §5 Growth engine has multiple naming variants across cohort:
    #   Sarreid:  "## The growth engine — three layers, all real"
    #   cci:      "## What's driving the +5.95% — three layers"
    #   hfg/kal:  "## The growth engine — …" or "## What's driving …"
    ("growth",       re.compile(r"\b(growth\s+engine|what'?s\s+driving)\b", re.I)),
    ("team",         re.compile(r"\bthe\s+team\b", re.I)),
    # §7 Risk watchlist variants:
    #   Sarreid: "## The full risk picture — 30 dealers, $2.18M at risk"
    #   cci:     "## The full at-risk picture — positions 6–25, $2.4M more in the tail"
    ("risk",         re.compile(r"\b(risk\s+picture|at[\s-]?risk\s+picture|risk\s+watchlist|watchlist)\b", re.I)),
    ("products",     re.compile(r"\b(what'?s\s+selling|product\s+intelligence|products?\s+&\s+the\s+cross[\s-]?sell)\b", re.I)),
    ("base",         re.compile(r"\bdealer\s+base\b", re.I)),
    ("channels",     re.compile(r"^channels\b", re.I)),
    # NONE-feed (behavior-only) close: "What an invoiced ERP feed would unlock"
    ("unlock",       re.compile(r"\bwould\s+unlock\b", re.I)),
    # §11 (methodology) and §12 (trust) — we group both into the same chunk
    # if they appear separately, but they live under the same `methodology` id.
    ("methodology_gaps",  re.compile(r"\bwhat\s+this\s+report\s+can'?t\s+see\b", re.I)),
    ("methodology_trust", re.compile(r"\bhow\s+to\s+trust\s+these\s+numbers\b", re.I)),
    ("appendix",     re.compile(r"^appendix\b", re.I)),
]


_GATESTOP_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("summary",        re.compile(r"^bottom\s+line\b", re.I)),
    ("preflights",     re.compile(r"\bwhat\s+the\s+preflights\s+returned\b", re.I)),
    ("concentration",  re.compile(r"\buser[\s-]?grain\s+concentration\s+finding\b", re.I)),
    ("patchnotes",     re.compile(r"\bpatch[\s-]?validation\s+observations\b", re.I)),
    ("nextaction",     re.compile(r"\brecommended\s+next\s+action\b", re.I)),
    ("appendix",       re.compile(r"^appendix\b", re.I)),
]


def _classify_h2(heading: str, mode: str) -> str:
    """Return the canonical section_id for a given H2 heading."""
    h = heading.lstrip("# ").strip()
    h_low = h.lower()
    if mode == "gatestop":
        table = _GATESTOP_PATTERNS
    else:
        table = _MODE1_PATTERNS
    for section_id, pat in table:
        if pat.search(h_low):
            return section_id
    # Fall back: synthesize a slug
    slug = re.sub(r"[^a-z0-9]+", "-", h_low).strip("-") or "section"
    return f"misc-{slug}"


def _detect_mode(text: str) -> str:
    """Mode detection from H1 markers.

    Gate-STOP: "VALIDATION ARTIFACT, GATE-FAILED"
    Mode-1: everything else (including thin-data orgs)
    """
    if re.search(r"VALIDATION ARTIFACT,?\s*GATE[\s-]?FAILED", text):
        return "gatestop"
    if re.search(r"^#\s+.*GATE[\s-]?FAILED", text, re.M | re.I):
        return "gatestop"
    return "mode1"


# ─── Footer-code-line extraction ────────────────────────────────────────────

# Footer lines look like `[STEP-10 LEDGER · org · ts · 1:pass 2:pass …]`
# wrapped in single backticks at the bottom of every PASS3 MD. Multiple lines
# may stack (STEP-0 OVERRIDE, STEP-10 LEDGER, POST-REVIEW PATCH, etc.).
_FOOTER_CODE_LINE = re.compile(r"^`(\[[^`]+\])`\s*$", re.M)


def _extract_footer_lines(text: str) -> tuple[str, list[str]]:
    """Pull the trailing `[STEP-* …]` code-span lines off the MD body.

    Returns (md_without_footers, footer_lines). Order preserved.
    """
    lines = text.rstrip().splitlines()
    footers: list[str] = []
    while lines:
        last = lines[-1].strip()
        if not last:
            lines.pop()
            continue
        m = _FOOTER_CODE_LINE.match(last)
        if m:
            footers.insert(0, m.group(1))
            lines.pop()
            continue
        break
    return "\n".join(lines), footers


# ─── Public entry point ─────────────────────────────────────────────────────

_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
_H3 = re.compile(r"^###\s+(.+?)\s*$", re.M)
_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)


def parse_md(text: str) -> ParsedReport:
    """Parse a PASS3 MD into chunks classified by canonical section id."""
    body, footers = _extract_footer_lines(text)
    mode = _detect_mode(body)

    # H1 (org display name)
    h1_match = _H1.search(body)
    org_h1_full = h1_match.group(1).strip() if h1_match else "Untitled"
    # Strip trailing modifiers like " — CEO Intelligence Brief", "  *(PASS3 — VALIDATION …)*"
    # The "display name" is the segment before " — " or " *("
    org_display_name = re.split(r"\s+—\s+|\s+\*\(", org_h1_full)[0].strip()

    # H3 sub-header (period framing or stop-line)
    h3_match = _H3.search(body)
    org_subtitle = h3_match.group(1).strip() if h3_match else ""

    # Body after H1 (and H3, if present, before the first H2)
    if h1_match:
        body_after_h1 = body[h1_match.end():]
    else:
        body_after_h1 = body

    # H2 split
    h2_positions = [m for m in _H2.finditer(body_after_h1)]
    chunks: list[Chunk] = []
    preamble_md = ""

    if not h2_positions:
        # Whole document is one chunk (e.g. extremely degraded output).
        preamble_md = body_after_h1.strip()
    else:
        preamble_md = body_after_h1[: h2_positions[0].start()].strip()
        # If H3 lives in preamble, strip it from the visible preamble (we've
        # captured it as `org_subtitle` already).
        if h3_match and h3_match.group(0) in preamble_md:
            preamble_md = preamble_md.replace(h3_match.group(0), "").strip()

        for i, m in enumerate(h2_positions):
            heading_text = m.group(1).strip()
            section_id = _classify_h2(heading_text, mode)
            start = m.end()
            end = h2_positions[i + 1].start() if i + 1 < len(h2_positions) else len(body_after_h1)
            body_md = body_after_h1[start:end].strip()
            # Strip the leading H3-rule (---) that often sits between H2 chunks
            # in the source MD. The MD library would render it as <hr/>; we
            # don't want a stray <hr/> at the top of each section.
            body_md = re.sub(r"^---\s*\n?", "", body_md)
            body_md = re.sub(r"\n---\s*$", "", body_md)
            # Strip bare slot-marker comment LINES (`<!--slot:C-->` on their own
            # line). Left in place they shatter the structures they wrap: a slot
            # comment between two `> ` lines breaks a coaching-card blockquote in
            # two (empty card + orphan callout), and one inside a table detaches
            # rows. md_render strips inline comments for final HTML anyway; these
            # markers carry no meaning past assembly, so drop the whole line
            # (incl. its newline) here. Inline comments inside a content line
            # (e.g. `| … <!--slot:B-->text<!--/slot:B--> | …`) are preserved and
            # cleaned later by md_render.
            body_md = re.sub(r"(?m)^[ \t]*<!--.*?-->[ \t]*\n?", "", body_md)
            chunks.append(Chunk(
                section_id=section_id,
                heading=heading_text,
                body_md=body_md,
                raw_heading_line=m.group(0),
            ))

    return ParsedReport(
        mode=mode,
        org_display_name=org_display_name,
        org_h1_full=org_h1_full,
        org_subtitle=org_subtitle,
        preamble_md=preamble_md,
        chunks=chunks,
        footer_code_lines=footers,
    )


def merge_methodology(report: ParsedReport) -> ParsedReport:
    """Combine `methodology_gaps` + `methodology_trust` (and trailing `appendix`)
    into a single `methodology` chunk for the renderer, preserving order.

    Per §5a.1 position-10 split nuance: the source MD may carry one or two
    methodology sections; either way the HTML emits one `<details id=methodology>`
    collapsible. The appendix (if present and >200 words) renders as its own
    collapsible at position 10b — handled by `sections.render_methodology`.
    """
    return report  # no-op for now; the renderer handles both shapes inline.
