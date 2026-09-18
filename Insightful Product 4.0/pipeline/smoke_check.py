"""Validation — exits 0 if the draft looks structurally valid.

Checks (numbered per operators §10 verification ledger):

  1. Output MD exists and is > 100 lines
  2. All declared sections present and non-empty
  3. Appendix Traceability block with Q-ECON-00
  4. No leaked Jinja artifacts ({{ }} or {% %})
  5. §Q sensitivity-hedge gate (dollars without markers)
  6. §R concentration-framing mismatch
  7. §S addressable-base qualifier
 13. Topline parity (cache vs rendered MD)

The HTML-side checks (4, 8, 9, 11, 12 from operators §10) live in
report_render/step10_check.py and run after the MD → HTML pass — not here.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from . import config


_JINJA_LEAK = re.compile(r"\{\{[^}]+\}\}|\{%[^%]+%\}")


# NOTE: the watchlist H2 renders as "## Full risk watchlist …" (the north-star
# title, section_07_watchlist.md.j2) — NOT the doctrine phrase "The full at-risk
# picture". The Appendix + `[org · date · profile]` ledger stamp were dropped
# from the client-facing brief (owner call 2026-07-13; section_11_methodology
# now ends on "How to trust these numbers"), so neither is required here.
_STANDARD_REQUIRED_SECTIONS = [
    "## The 60-second read",
    "## Do this week",
    "## What's driving",
    "## The team",
    "## Full risk watchlist",
    "## What's selling",
    "## The dealer base",
    "## Channels",
    "## What this report can't see",
    "## How to trust these numbers",
]

_GATESTOP_REQUIRED_SECTIONS = [
    "## Bottom line",
    "## What the preflights returned",
    "## Appendix",
]

# NONE feed (behavior-only) layout: the ERP-dependent sections (Do this week,
# What's driving, at-risk picture, What's selling, dealer base) are intentionally
# omitted — there is no invoiced data behind them. Same _base.md.j2 template,
# NONE ordering branch (leads with the rep-activity floor + eCat, closes with the
# ERP-unlock block). See _base.md.j2 and section_01_hero.md.j2 NONE branches.
_NONE_REQUIRED_SECTIONS = [
    "## The 60-second read",
    "## The team",
    "## Channels",
    "## What an invoiced ERP feed would unlock",
    "## What this report can't see",
    "## How to trust these numbers",
]


def _is_gatestop(md_path: Path, text: str) -> bool:
    """Distinguish true Gate-STOP artifacts (zero signal) from full drafts.

    Two signals — either counts:
      1. Filename contains _GATESTOP_ (run_report.py naming convention)
      2. Header contains the "VALIDATION ARTIFACT, GATE-FAILED" marker
         (idempotent for renamed files)
    """
    if "_GATESTOP_" in md_path.name:
        return True
    if "VALIDATION ARTIFACT, GATE-FAILED" in text[:500]:
        return True
    return False


_BROAD_FRAMING = re.compile(
    r'\b(?:broad[- ]based|broadly\s+spread|diversified|well[- ]distributed)\b',
    re.IGNORECASE,
)


def _check_concentration_framing(text: str, issues: list[str]) -> None:
    """Check [6] §R: reject 'broad-based' framing when concentration is high."""
    matches = list(_BROAD_FRAMING.finditer(text))
    if not matches:
        return
    top1_match = re.search(r'top[- ]?1[^|]*?\|\s*([\d.]+)\s*%', text, re.IGNORECASE)
    hhi_match = re.search(r'HHI[^|]*?\|\s*([\d,.]+)', text, re.IGNORECASE)
    top1 = float(top1_match.group(1)) if top1_match else None
    hhi_str = hhi_match.group(1).replace(",", "") if hhi_match else None
    hhi = float(hhi_str) if hhi_str else None
    if (top1 is not None and top1 >= 25.0) or (hhi is not None and hhi >= 1500.0):
        for m in matches:
            issues.append(
                f"CONCENTRATION FRAMING: '{m.group()}' at pos {m.start()} "
                f"but top-1={top1}% / HHI={hhi}"
            )


_DOLLAR_RE = re.compile(r'\$[\d,]+(?:\.\d+)?[KMB]?')
_HEDGE_MARKERS = re.compile(
    r'\b(?:directional|floor|at least|estimated|approximate|partial feed|query result)\b',
    re.IGNORECASE,
)


def _check_sensitivity_hedge(text: str, issues: list[str], confidence: str | None = None) -> None:
    """Check [5] §Q: dollar claims in early sections should have hedge markers
    when commerce confidence is not STRONG.
    """
    if confidence and confidence.upper() == "STRONG":
        return
    early_sections = []
    for heading in ("## The 60-second read", "## Do this week", "## Do this month"):
        start = text.find(heading)
        if start < 0:
            continue
        next_h2 = text.find("\n## ", start + len(heading))
        section_text = text[start:next_h2] if next_h2 > 0 else text[start:start + 3000]
        early_sections.append((heading, section_text))
    for heading, section_text in early_sections:
        for m in _DOLLAR_RE.finditer(section_text):
            window_start = max(0, m.start() - 400)
            window_end = min(len(section_text), m.end() + 400)
            window = section_text[window_start:window_end]
            if not _HEDGE_MARKERS.search(window):
                issues.append(
                    f"SENSITIVITY HEDGE: {m.group()} in {heading} without marker "
                    f"(confidence={confidence or 'unknown'})"
                )


_ADDRESSABLE_PATTERN = re.compile(r'(?:\+\$[\d,]+[KMB]?|per\s+\d+-?point)', re.IGNORECASE)
_BASE_QUALIFIER = re.compile(r'\b(?:addressable|full base|base of)\b', re.IGNORECASE)


def _check_addressable_base(text: str, issues: list[str]) -> None:
    """Check [7] §S: growth projections should state the addressable base."""
    for m in _ADDRESSABLE_PATTERN.finditer(text):
        window_start = max(0, m.start() - 300)
        window_end = min(len(text), m.end() + 300)
        window = text[window_start:window_end]
        if not _BASE_QUALIFIER.search(window):
            issues.append(
                f"ADDRESSABLE BASE: '{m.group()}' at pos {m.start()} without base qualifier"
            )


def _check_topline_parity(text: str, issues: list[str], cache_dir: Path | None = None) -> None:
    """Check [13]: topline parity between MD appendix and cached Q-ECON-00."""
    if cache_dir is None:
        return
    econ_csv = cache_dir / "Q-ECON-00.csv"
    if not econ_csv.exists():
        return
    import csv
    with econ_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return
    cache_val_str = rows[0].get("inv_ltm_net", "")
    if not cache_val_str:
        return
    try:
        cache_val = float(cache_val_str.replace(",", ""))
    except (ValueError, TypeError):
        return

    appendix_idx = text.find("## Appendix")
    if appendix_idx < 0:
        return
    appendix = text[appendix_idx:]
    inv_match = re.search(
        r'(?:inv_ltm_net|Invoiced\s+LTM)[^|]*\|\s*\$?([\d,]+(?:\.\d+)?)',
        appendix,
        re.IGNORECASE,
    )
    if not inv_match:
        return
    try:
        md_val = float(inv_match.group(1).replace(",", ""))
    except (ValueError, TypeError):
        return
    if abs(md_val - cache_val) > 1.0:
        issues.append(
            f"TOPLINE PARITY: MD shows ${md_val:,.0f} but cache has ${cache_val:,.0f}"
        )



# ─── T1-5: one named quantity, one value ──────────────────────────────────
# hfg shipped "1,075 prior-year accounts went dark" in §1 and "1,080 dealers
# who bought last year ordered nothing this year" in §9. Both numbers were
# CORRECT for their own denominator (the NRR cohort vs the dealer-activity
# base) and both traced to a fact bundle, so the number-parity gate passed
# them — it checks traceability, never consistency. cci was 62 apart and bmc
# 198 apart (36%). A CEO reads those as one claim.
#
# Each entry is one CLAIM a reader will treat as a single fact, with every
# phrasing the report uses for it. Two distinct values under one claim is a
# ship blocker regardless of which query each came from.
_CONSISTENCY_CLAIMS: dict[str, tuple[str, ...]] = {
    "accounts that went dark": (
        r"\*{0,2}([\d,]+)\*{0,2}\s+prior-year accounts?\s+(?:that\s+)?went dark",
        r"\*{0,2}([\d,]+)\s*dealers?\*{0,2}\s+who bought last year ordered nothing",
    ),
    "first-ever orders (new dealers)": (
        r"\*{0,2}([\d,]+)\*{0,2}\s+(?:new\s+)?dealers?\s+placed a first[- ]ever order",
        r"\*{0,2}([\d,]+)\s*new dealers?\*{0,2}\s+placed a first[- ]ever order",
    ),
}


def _check_named_quantity_consistency(text: str, issues: list[str]) -> None:
    """Fail when one claim carries two different numbers anywhere in the report."""
    for claim, patterns in _CONSISTENCY_CLAIMS.items():
        found: dict[str, list[str]] = {}
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                value = m.group(1).replace(",", "")
                found.setdefault(value, []).append(m.group(0).strip()[:60])
        if len(found) > 1:
            shown = "; ".join(
                f"{v} ({found[v][0]!r})" for v in sorted(found, key=lambda x: int(x))
            )
            issues.append(
                f"NAMED-QUANTITY CONFLICT: '{claim}' rendered with "
                f"{len(found)} different values — {shown}"
            )


def smoke(md_path: Path, *, confidence: str | None = None, cache_dir: Path | None = None) -> tuple[bool, list[str]]:
    """Return (pass, list of failure messages).

    Two profiles:
      standard    → full 11-section CEO report (all modes go through _base.md.j2)
      gatestop    → true Gate-STOP artifact, zero signal (3 required sections)

    Short-length check is profile-specific.
    """
    issues: list[str] = []

    if not md_path.exists():
        return False, [f"MISSING: {md_path}"]

    text = md_path.read_text(encoding="utf-8")

    _check_named_quantity_consistency(text, issues)
    lines = text.splitlines()
    gatestop = _is_gatestop(md_path, text)

    # 1. Length sanity — profile-specific
    if gatestop:
        if len(lines) < 20:
            issues.append(f"TOO SHORT (gatestop): {len(lines)} lines (< 20)")
    else:
        if len(lines) < 100:
            issues.append(f"TOO SHORT: {len(lines)} lines (< 100)")

    # 2. Required section headings — profile-specific
    # assemble.py always uses _base.md.j2 regardless of mode; Gate-STOP orgs
    # get the _GATESTOP_ filename suffix but their content follows the NONE
    # ordering branch (same template). Use _NONE_REQUIRED_SECTIONS for Gate-STOP
    # files with NONE confidence, and _GATESTOP_REQUIRED_SECTIONS only for
    # legacy zero-signal artifacts that truly have no template content.
    if gatestop and confidence and confidence.upper() == "NONE":
        required = _NONE_REQUIRED_SECTIONS
    elif gatestop:
        required = _GATESTOP_REQUIRED_SECTIONS
    elif confidence and confidence.upper() == "NONE":
        required = _NONE_REQUIRED_SECTIONS
    else:
        required = _STANDARD_REQUIRED_SECTIONS
    for h in required:
        if h not in text:
            issues.append(f"MISSING SECTION: {h}")

    # 3. Appendix trace row — the client-facing standard/none brief no longer
    # carries an Appendix (owner call 2026-07-13). Gate-STOP files with NONE
    # confidence use the NONE-mode template (no Appendix). The legacy zero-signal
    # Gate-STOP artifact (non-NONE confidence) still requires an Appendix.
    appendix_idx = text.find("## Appendix")
    is_none_gatestop = gatestop and (confidence or "").upper() == "NONE"
    if appendix_idx >= 0:
        appendix = text[appendix_idx:]
        if "Q-ECON-00" not in appendix:
            issues.append("APPENDIX missing Q-ECON-00 trace reference")
    elif gatestop and not is_none_gatestop:
        issues.append("APPENDIX block missing entirely")

    # 4. No Jinja leakage
    leaks = _JINJA_LEAK.findall(text)
    if leaks:
        issues.append(f"JINJA LEAK: {len(leaks)} unfilled artifacts (first: {leaks[0][:60]})")

    # 5. Sensitivity hedge (early-section dollars without markers)
    _check_sensitivity_hedge(text, issues, confidence=confidence)

    # 6. Concentration framing mismatch
    _check_concentration_framing(text, issues)

    # 7. Addressable-base qualifier
    _check_addressable_base(text, issues)

    # 13. Topline parity (cache vs rendered MD)
    _check_topline_parity(text, issues, cache_dir=cache_dir)

    return (len(issues) == 0), issues


def main() -> int:
    p = argparse.ArgumentParser(description="Smoke-check an Insightful pipeline MD draft.")
    p.add_argument("md", help="Path to *_DRAFT_*.md or *_GATESTOP_*.md")
    p.add_argument("--confidence", default=None, help="Commerce confidence level (e.g. STRONG, PARTIAL)")
    p.add_argument("--cache-dir", default=None, help="Path to pipeline cache directory for parity checks")
    args = p.parse_args()

    cache_path = Path(args.cache_dir) if args.cache_dir else None
    ok, issues = smoke(Path(args.md), confidence=args.confidence, cache_dir=cache_path)
    if ok:
        print(f"PASS: {args.md}")
        return 0
    print(f"FAIL: {args.md}")
    for i in issues:
        print(f"  - {i}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
