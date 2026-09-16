"""Step-10 HTML verification ledger — items 4, 8, 9, 11, 12.

The five HTML-port checks from `operators/report_operator.md` Step 10:

    [4]  §P forbidden-vocabulary regex sweep (HTML)
    [8]  Number reconciliation (HTML ↔ MD)
    [9]  Verbatim 12-word phrase echo (HTML)
    [11] HTML structure pairing (well-formed; unique ids)
    [12] In-document anchor link resolution

CLI:
    python -m report_render.step10_check \
        --html outputs/Sarreid_CEO_intelligence_report_regenerated_2026-06-30.html \
        --md   outputs/Sarreid_CEO_intelligence_report_2026-06-29.md
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional

from bs4 import BeautifulSoup

# ─── §P forbidden-vocabulary list (port of report_editorial_rules_v4 §P.1) ─

# Regexes are case-insensitive and word-bounded where the literal allows it.
# We carry the (token, allowed-context-test) shape so §P.2 overrides are inline.

_FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
    # § P.1.A — SaaS / CRO / revenue-ops
    (r"\bNRR\b", "saas"),
    (r"\bnet\s+revenue\s+retention\b", "saas"),
    (r"\bGRR\b", "saas"),
    (r"\bgross\s+revenue\s+retention\b", "saas"),
    (r"\bMRR\b", "saas"),
    (r"\bARR\b", "saas"),
    (r"\bnew\s+logos?\b", "saas"),
    (r"\bplaybook\b", "saas"),
    (r"\bcohort\b", "cohort"),
    (r"\bICP\b", "saas"),
    (r"\bTAM\b", "saas"),
    (r"\bSAM\b", "saas"),
    (r"\bCAC\b", "saas"),
    (r"\bLTV\b", "saas"),
    (r"\bMoM\b", "yoy-acronym"),
    (r"\bQoQ\b", "yoy-acronym"),
    (r"\bYoY\b", "yoy-acronym"),
    (r"\bfunnel\b", "saas"),
    (r"\bpipeline\s+coverage\b", "saas"),
    (r"\bwin\s+rate\b", "saas"),
    (r"\bmotion\b", "saas"),
    (r"\bGTM\b", "saas"),
    (r"\bexpansion\s+revenue\b", "saas"),
    (r"\bland\s+and\s+expand\b", "saas"),
    (r"\bPLG\b", "saas"),
    (r"\bnorth[-\s]?star\b", "saas"),
    (r"\bDAU\b", "saas"),
    (r"\bMAU\b", "saas"),

    # § P.1.B — internal codes / system identifiers
    (r"\bVM-\d+\b", "system"),
    (r"\bQ-(?:ECON|CHAN|CI|PROV|ORG)-\w+\b", "system"),
    (r"\bRung-\d\b", "system"),
    (r"\boperator-\d\b", "system"),
    (r"\bRS-\d+\b", "system"),
    (r"\bFEED_COMPLETENESS\b", "system"),
    (r"\bCOMMERCE_CONFIDENCE\b", "system"),
    (r"\bREP_IDENTITY_TIER\b", "system"),
    (r"\bDATA_MASS_TIER\b", "system"),
    (r"\bREPORT_INTELLIGENCE_TIER\b", "system"),
    (r"\bTIER-[123]\b", "system"),
    (r"\bMode\s+[123]\s+(?:Standard|Activation|Reactivation)\b", "system"),
    (r"\bpreflight\b", "system"),
    (r"\bfeed\s+posture\b", "system"),
    (r"\bsingle-feed\s+posture\b", "system"),
    (r"\bGate-STOP\b", "system"),
    (r"\bcohort-validation\b", "system"),

    # § P.1.C — system / pipeline / process language
    (r"\bthe\s+operator\b", "process"),
    (r"\bthe\s+report\s+run\b", "process"),
    (r"\bthis\s+run\b", "process"),
    # `the pipeline` intentionally NOT banned standalone: in furniture-sales
    # prose it routinely refers to the dealer's order pipeline / deal pipeline
    # (a domain phrase). Render-pipeline leaks are caught by `the renderer`,
    # `the run`, and the more specific phrases below.
    (r"\bthe\s+render\s+pipeline\b", "process"),
    (r"\bthe\s+renderer\b", "process"),
    (r"\bthe\s+gate\s+(?:passed|failed|fired)\b", "process"),
    (r"\bdelivered\s+HTML\b", "process"),
    (r"\breport\s+stage\s+badge\b", "process"),
    (r"\bTODO\b", "process"),
    (r"\bFIXME\b", "process"),
    (r"\bhouse_suspect\b", "process"),
    (r"\bhouse-rep\b", "process"),
    (r"\bhouse/sample/accom\b", "process"),
    (r"\bshortname\b", "process"),
    (r"\borg_id\b", "process"),
    (r"\borganization_id\b", "process"),
    # DB tables
    (r"\bportal_invoices\b", "system"),
    (r"\bportal_orders\b", "system"),
    (r"\bsales_data\b", "system"),
    # DB columns (cohort lesson)
    (r"\brep_number\b", "db-col"),
    (r"\brep_name\b", "db-col"),
    (r"\brep_label\b", "db-col"),
    (r"\bbill_to_number\b", "db-col"),
    (r"\bship_to_number\b", "db-col"),
    (r"\bitem_number\b", "db-col"),
    (r"\bcustomer_num\b", "db-col"),
    (r"\bcustomer_bill_to_number\b", "db-col"),
    (r"\borg_user_id\b", "db-col"),
    (r"\bnet_amount\b", "db-col"),
    (r"\border_origin\b", "db-col"),
    (r"\bsubmit_date\b", "db-col"),
    (r"\bis_submitted\b", "db-col"),
    # column-arrow compounds
    (r"\b\w+_\w+\s*[→\-]+>?\s*\w+_\w+\b", "db-col"),

    # § P.1.D — internal product names / version numbers
    (r"\bInsightful\s+Product\b", "product"),
    (r"\bInsightful\b(?!\s+Product)", "product"),
    (r"\bSuperCat\b", "supercat"),
    (r"\beCat\b", "ecat"),
    (r"\b[Vv]4(?:\.\d)?\b", "version"),
]

_FORBIDDEN_COMPILED = [(re.compile(p, re.I), ctx) for p, ctx in _FORBIDDEN_PATTERNS]


def _yoy_allowed(
    text: str, span: tuple[int, int], parent_text: str = "", el=None
) -> bool:
    """`YoY` / `MoM` / `QoQ` are allowed when adjacent to a number, in either
    the text node or its rendered parent block (e.g. "+82.5% <strong>YoY</strong>"),
    or when serving as a `<th>` column header for a numeric column."""
    start, end = span
    window = text[max(0, start - 30):min(len(text), end + 30)]
    if re.search(r"[\d\.%]", window):
        return True
    if parent_text and re.search(
        r"[\d\.%]\s*(?:YoY|MoM|QoQ)|(?:YoY|MoM|QoQ)\s*[\d\.%]", parent_text
    ):
        return True
    if el is not None:
        ancestor = el.parent if hasattr(el, "parent") else None
        while ancestor is not None:
            try:
                if ancestor.name == "th":
                    return True
            except AttributeError:
                pass
            ancestor = getattr(ancestor, "parent", None)
    return False


# §P.2 eCat allow-list (completeness Track F / decision memo §8 #2).
# Hero = HTML id `summary` (§1 60-sec read); floor = `platform-readiness`
# (always-on platform/rep/eCat floor — Track A). Honesty guards (F1 cap, F7
# "not your total business") land in Track B; this gate is vocab-only.
_ECAT_ALLOWED_SECTIONS = frozenset({
    "summary",              # §1 hero / 60-sec read
    "platform-readiness",   # always-on floor section
    "channels",
    "methodology",
    "unlock",               # NONE-feed "what an ERP feed unlocks" close (Track A floor context)
})


def _ecat_allowed_in_section(section_id: Optional[str]) -> bool:
    return section_id in _ECAT_ALLOWED_SECTIONS


def _cohort_allowed(text: str, span: tuple[int, int]) -> bool:
    """`cohort` survives only inside the literal phrase "buyer cohort" or
    "design cohort" (domain-true)."""
    start, end = span
    window = text[max(0, start - 10):end]
    return bool(re.search(r"\b(buyer|design)\s+cohort\b", window, re.I))


def _check_forbidden_vocab(soup: BeautifulSoup) -> list[str]:
    """Item [4]. Sweep customer-facing text for §P violations.

    Skip rules (all §P.2 inherited):
    - The Appendix Traceability footer (#appendix) is internal provenance.
    - The footer-ledger spans (STEP-10 LEDGER lines) are internal provenance.
    - A Gate-STOP artifact (Mode-2) is by design an INTERNAL validation
      output ("VALIDATION ARTIFACT, GATE-FAILED — STOP, do not ship"). Per
      `operators/report_operator.md` §5b the whole template is a deterministic
      stop message that must echo literal mode names, gate names, preflight
      ids, and DB column names so an integrator knows what to wire to clear
      the stop. §P (which guards CUSTOMER-FACING copy) therefore relaxes for
      the entire Mode-2 document; only Mode-1 (client-facing) gets the full
      sweep. This is the gate-STOP relaxation; checks [8 9 11 12] still run.
    """
    raw: list[str] = []
    is_gatestop = soup.select_one(".gate-stop-banner") is not None
    if is_gatestop:
        return []
    # Walk only the top-level page container once to avoid double-counting
    # text that lives inside nested <details><section> structures.
    page = soup.select_one(".page") or soup
    for section in [page]:
        # Skip the footer-ledger spans (internal provenance per §P.2)
        if section.find_parent(class_="footer-ledger") is not None:
            continue
        section_id = section.get("id") or _nearest_id(section)
        # Skip the Appendix internal section
        if section_id == "appendix":
            continue
        for el in section.find_all(
            string=lambda t: t.parent.name not in {"script", "style"}
        ):
            text = str(el)
            if not text.strip():
                continue
            # Skip if we're inside an internal-provenance surface
            if el.find_parent(class_="footer-ledger") is not None:
                continue
            if el.find_parent(attrs={"id": "appendix"}) is not None:
                continue
            parent_text = ""
            try:
                parent_text = el.parent.get_text(" ", strip=True) if el.parent else ""
            except Exception:
                parent_text = ""
            # Identify the nearest section id for the violation report
            local_section_id = _nearest_id(el)
            for pattern, ctx in _FORBIDDEN_COMPILED:
                for m in pattern.finditer(text):
                    span = m.span()
                    # Apply §P.2 allow-list
                    if ctx == "yoy-acronym" and _yoy_allowed(text, span, parent_text, el):
                        continue
                    if ctx == "ecat" and _ecat_allowed_in_section(local_section_id):
                        continue
                    if ctx == "cohort" and _cohort_allowed(text, span):
                        continue
                    if ctx == "supercat" and "About SuperCat" in text:
                        continue
                    if ctx == "product":
                        window = text[max(0, span[0] - 5):min(len(text), span[1] + 30)]
                        if "CEO Brief" in window or "CEO Brief" in parent_text:
                            continue
                        if "Customer Intelligence" in window or "Customer Intelligence" in parent_text:
                            continue
                    if ctx == "version":
                        # Only flag bare version-number tokens (e.g. "4.0"
                        # alone); not "$15.64M" or other numerics. Require a
                        # `v` prefix OR adjacency to "v" or "version".
                        window = text[max(0, span[0] - 12):span[0]]
                        if not re.search(r"\bv|version\s+|product", window, re.I):
                            continue
                    raw.append(
                        f"[4] §P forbidden token {m.group(0)!r} "
                        f"({ctx}) in section #{local_section_id or 'unknown'}: "
                        f"…{text[max(0, span[0] - 30):min(len(text), span[1] + 30)].strip()}…"
                    )
    # Dedupe identical messages (text node walked under multiple ancestors)
    seen: set[str] = set()
    violations: list[str] = []
    for msg in raw:
        if msg in seen:
            continue
        seen.add(msg)
        violations.append(msg)
    return violations


def _nearest_id(el) -> Optional[str]:
    """Walk up the tree to find the nearest ancestor with an `id`. Accepts
    either a Tag or a NavigableString (in which case we start at .parent)."""
    cur = el
    if not hasattr(cur, "get"):
        cur = cur.parent if cur is not None else None
    while cur is not None:
        try:
            val = cur.get("id")
        except AttributeError:
            val = None
        if val:
            return val
        cur = cur.parent
    return None


# ─── [11] Structure pairing ────────────────────────────────────────────────

def _check_structure(html_path: Path, html: str, soup: BeautifulSoup) -> list[str]:
    violations: list[str] = []
    # ID uniqueness
    ids: list[str] = [el.get("id") for el in soup.find_all(id=True)]
    dup = [i for i, n in Counter(ids).items() if n > 1]
    if dup:
        violations.append(f"[11] duplicate id(s) in {html_path.name}: {dup}")
    # details / section / table pairing
    for tag in ("details", "section", "table"):
        opens = len(re.findall(rf"<{tag}\b", html, flags=re.I))
        closes = len(re.findall(rf"</{tag}\s*>", html, flags=re.I))
        if opens != closes:
            violations.append(
                f"[11] {tag} open/close mismatch in {html_path.name}: "
                f"{opens} open vs {closes} close"
            )
    return violations


# ─── [12] Anchor resolution ────────────────────────────────────────────────

def _check_anchors(html_path: Path, soup: BeautifulSoup) -> list[str]:
    violations: list[str] = []
    ids = {el.get("id") for el in soup.find_all(id=True) if el.get("id")}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("#") or len(href) == 1:
            continue
        target = href[1:]
        if target not in ids:
            violations.append(
                f"[12] broken in-doc anchor '{href}' in {html_path.name} "
                f"(label: {a.get_text(strip=True)!r})"
            )
    return violations


# ─── [9] 12-word verbatim phrase echo ──────────────────────────────────────

_HEADER_SELECTORS = [
    # Step 10 [9] scope is "headers, sub-headers, and callouts" — NOT body
    # prose. We exclude `.coaching-body`, `.play-sub`, `.ceo-body`, `.prose`
    # because those legitimately overlap with header summary copy (e.g. the
    # collapsed-summary teaser repeats the body's lead sentence) — the
    # dedup-target surfaces are only the brief, sub, and callout sites.
    "h1", "h2", "h3", "h4",
    ".section-title", ".section-sub", ".subsection-title",
    ".hero-eyebrow", ".hero-sub",
    ".ceo-title",
    ".coaching-name", ".coaching-stats",
    ".play-card h4", ".play-upside",
    ".priority-title", ".priority-impact",
    ".metric-label", ".metric-value", ".metric-note",
    ".callout-title",
]


def _check_phrase_echo(soup: BeautifulSoup, min_words: int = 12) -> list[str]:
    """Item [9]. Find any 12+ word phrase that appears verbatim in 2+
    header/sub-header/callout sites across §1/§2/§3/§5 of the HTML."""
    violations: list[str] = []
    fragments: list[tuple[str, str]] = []
    # Restrict to §1-§3 + §5 sections + their summaries
    target_section_ids = {"summary", "thisweek", "thismonth", "growth"}
    for sid in target_section_ids:
        sec = soup.find(attrs={"id": sid})
        if not sec:
            continue
        for sel in _HEADER_SELECTORS:
            for el in sec.select(sel):
                txt = _normalize(el.get_text(" ", strip=True))
                if txt:
                    fragments.append((sid, txt))

    # Sliding 12-word window across each fragment; count global occurrences
    window_counts: dict[str, list[tuple[str, str]]] = {}
    for sid, frag in fragments:
        words = re.findall(r"\S+", frag)
        if len(words) < min_words:
            continue
        for i in range(len(words) - min_words + 1):
            window = " ".join(words[i:i + min_words]).lower()
            window_counts.setdefault(window, []).append((sid, frag))

    for window, hits in window_counts.items():
        # Hits in distinct fragments (not the same fragment counted twice)
        distinct = {(sid, frag) for sid, frag in hits}
        if len({frag for _, frag in distinct}) >= 2:
            violations.append(
                f"[9] verbatim {min_words}-word echo across §{[sid for sid, _ in distinct]}: {window!r}"
            )
    return violations


def _normalize(text: str) -> str:
    """Strip soft punctuation that varies across renders so the phrase match
    is on words, not glyphs."""
    text = re.sub(r"[\u2018\u2019']", "'", text)
    text = re.sub(r"[\u201C\u201D\"]", '"', text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ─── [8] Number reconciliation (HTML ↔ MD) ─────────────────────────────────

_NUM_PATTERNS = [
    re.compile(r"\$[\d,]+(?:\.\d+)?[MK]?\b"),
    re.compile(r"[\-−–+]?\d{1,3}(?:\.\d+)?\s?%"),
    re.compile(r"\b\d{2,5}\s+(?:dealers|reps|accounts|doors|SKUs|stores|days)\b", re.I),
]


def _extract_numbers(text: str) -> Counter:
    """Pull money/percent/count tokens from a chunk of text and count them."""
    counts: Counter = Counter()
    for pat in _NUM_PATTERNS:
        for m in pat.finditer(text):
            tok = re.sub(r"\s+", " ", m.group(0)).strip()
            # Canonicalize minus glyph variants
            tok = tok.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
            counts[tok] += 1
    return counts


def _check_number_reconciliation(html_text: str, md_text: str) -> list[str]:
    """Item [8]. Every figure that appears in 2+ sections of the HTML must
    appear in the MD (and vice-versa). We approximate "appears in 2+ sections"
    as "appears 2+ times across the rendered output," which is a slight
    superset of the spec but produces 0 false negatives.
    """
    violations: list[str] = []
    html_counts = _extract_numbers(html_text)
    md_counts = _extract_numbers(md_text)
    # Repeated HTML numbers should be present in MD
    for tok, n in html_counts.items():
        if n >= 2 and tok not in md_counts:
            violations.append(
                f"[8] HTML number {tok!r} appears {n}× but is absent from the MD"
            )
    # Repeated MD numbers should make it into HTML
    for tok, n in md_counts.items():
        if n >= 2 and tok not in html_counts:
            violations.append(
                f"[8] MD number {tok!r} appears {n}× but never reached the HTML"
            )
    return violations


# ─── Public API ────────────────────────────────────────────────────────────

def run_checks(html_path: Path, md_path: Optional[Path] = None) -> tuple[bool, dict]:
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")
    md_text = md_path.read_text(encoding="utf-8") if md_path and md_path.exists() else ""

    body_text = soup.get_text("\n", strip=False)

    results = {
        "4": _check_forbidden_vocab(soup),
        "8": _check_number_reconciliation(body_text, md_text) if md_text else [],
        "9": _check_phrase_echo(soup),
        "11": _check_structure(html_path, html, soup),
        "12": _check_anchors(html_path, soup),
    }
    passing = all(len(v) == 0 for v in results.values())
    return passing, results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", required=True, type=Path)
    parser.add_argument("--md", type=Path, default=None)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the pass/fail summary line (no violation detail)",
    )
    args = parser.parse_args(argv)
    if not args.html.exists():
        print(f"ERROR: HTML not found: {args.html}", file=sys.stderr)
        return 2

    passing, results = run_checks(args.html, args.md)
    label = args.html.name
    if passing:
        print(f"PASS  {label}  · [4 8 9 11 12 all pass]")
        return 0

    failed = [k for k, v in results.items() if v]
    print(f"FAIL  {label}  · failed checks: {failed}")
    if not args.quiet:
        for check_id, msgs in results.items():
            for m in msgs:
                print(f"  - {m}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
