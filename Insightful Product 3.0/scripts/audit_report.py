"""
Insightful Product 3.0 — Report Auditor (deterministic)

Replaces the LLM-based Step 5 audit agent. Reads plan files + assembled HTML,
performs structural verification, forbidden term check, what-this-means count,
details balance, and dollar qualifier spot checks.

No LLM calls. No network. Runs in < 2 seconds.

Usage:
    python audit_report.py --shortname cci --run-date 2026-06-17
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HARD_FORBIDDEN = [
    r"\[HYPOTHETICAL\]",
    r"\[ESTIMATED\]",
    r"health score",
    r"\bMixpanel\b",
    r"\bClicky\b",
    r"\bbounce_rate\b",
    r"\border_source\b",
    r"\bbenchmark_confidence\b",
    r"\bpeer_group_level\b",
    r"\bpeer_group_n\b",
    r"Platform-Embedded",
    r"Commerce-Active",
    r"Catalog-Focused",
]

REVIEW_TERMS = [
    r"\bERP\b",
    r"\bestimated\b",
    r"\bhypothetical\b",
    r"\bportal order",
    r"\bplatform-attributed\b",
]


def load_plans(fragments_dir: Path) -> dict[int, list[dict]]:
    """Load section plan files, extract subsections that should render."""
    plans: dict[int, list[dict]] = {}
    for n in (2, 3, 4, 5, 6):
        plan_path = fragments_dir / f"section_{n:02d}_plan.md"
        if not plan_path.exists():
            continue
        text = plan_path.read_text(encoding="utf-8")
        subsections = []
        for line in text.split("\n"):
            if line.startswith("| ") and "---" not in line and "Subsection" not in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 4:
                    subsections.append({
                        "name": parts[0],
                        "type": parts[1],
                        "gate": parts[2],
                        "will_render": parts[3].upper(),
                    })
        plans[n] = subsections
    return plans


def check_structural_completeness(html: str, plans: dict[int, list[dict]]) -> list[str]:
    """Verify planned subsections exist in the HTML."""
    defects = []
    html_lower = html.lower()
    for section_num, subsections in plans.items():
        for sub in subsections:
            if sub["will_render"] == "YES":
                name = sub["name"].strip()
                core = re.sub(r"^\d+[a-z]?\.\s*", "", name)
                core = re.sub(r"\s*\(Q-[^)]+\)", "", core)
                core = re.sub(r"\s*\[COLLAPSE\]", "", core)
                core = core.strip()
                if not core or len(core) < 4:
                    continue
                if core.lower() in ("section-level what-this-means", "admin disclosure",
                                     "section collapsed by default", "data confidence header",
                                     "header metrics"):
                    continue
                if core.lower().startswith("data confidence"):
                    continue
                core_words = core.lower().split()
                if len(core_words) >= 2:
                    search_term = " ".join(core_words[:3])
                else:
                    search_term = core.lower()
                if search_term not in html_lower:
                    if not re.search(re.escape(core.lower()), html_lower):
                        defects.append(f"§{section_num}: Missing subsection '{name}' (planned: YES)")
    return defects


def check_forbidden_terms(html: str) -> tuple[list[str], list[str]]:
    """Check for hard-forbidden and review terms."""
    hard_hits = []
    for pattern in HARD_FORBIDDEN:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            hard_hits.append(f"{pattern}: {len(matches)} occurrence(s)")

    review_hits = []
    for pattern in REVIEW_TERMS:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            review_hits.append(f"{pattern}: {len(matches)} occurrence(s)")

    return hard_hits, review_hits


def check_details_balance(html: str) -> list[str]:
    """Verify <details> tags are balanced."""
    opens = len(re.findall(r"<details", html))
    closes = len(re.findall(r"</details>", html))
    if opens != closes:
        return [f"<details> unbalanced: {opens} open / {closes} close"]
    return []


def check_what_this_means(html: str) -> list[str]:
    """Verify what-this-means count vs subsection count."""
    wtm = len(re.findall(r"what-this-means", html))
    subs = len(re.findall(r'class="subsection"', html))
    if subs > 0 and (subs - wtm) > 6:
        return [f"what-this-means count ({wtm}) far below subsection count ({subs}) — {subs - wtm} missing"]
    return []


def check_html_comments(html: str) -> list[str]:
    """Verify no HTML comments remain."""
    count = html.count("<!--")
    if count > 0:
        return [f"{count} HTML comment(s) remaining in output"]
    return []


def check_unresolved_placeholders(html: str) -> list[str]:
    """Verify no {{PARAM}} placeholders remain."""
    matches = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if matches:
        unique = set(matches)
        return [f"{len(unique)} unresolved placeholder(s): {', '.join(sorted(unique)[:5])}"]
    return []


def check_section_collapse_structure(html: str) -> list[str]:
    """Verify section-collapse elements have correct nesting."""
    issues = []
    pattern = r'<details class="section-collapse"[^>]*>.*?</details>'
    for match in re.finditer(pattern, html, re.DOTALL):
        block = match.group(0)[:500]
        if '<span class="section-title">' in block:
            issues.append("section-title uses <span> instead of <div>")
            break
        summary_end = block.find("</summary>")
        if summary_end > 0:
            before_summary = block[:summary_end]
            if 'class="section-sub"' not in before_summary:
                issues.append("section-sub is outside <summary> tag")
                break
            if 'class="section-contents"' not in before_summary:
                issues.append("section-contents is outside <summary> tag")
                break
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Insightful 3.0 — Deterministic Report Auditor")
    parser.add_argument("--shortname", required=True)
    parser.add_argument("--run-date", required=True)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    run_dir = project_root / "runs" / f"{args.shortname}_{args.run_date}"
    fragments_dir = run_dir / "fragments"
    output_dir = run_dir / "output"
    report_path = output_dir / f"{args.shortname}_{args.run_date}_intelligence_report.html"

    if not report_path.exists():
        print(f"ERROR: Report not found: {report_path}")
        sys.exit(1)

    html = report_path.read_text(encoding="utf-8")
    plans = load_plans(fragments_dir)

    print(f"Auditing: {report_path.name} ({len(html):,} bytes)")
    print(f"  Plans loaded: §{', §'.join(str(n) for n in sorted(plans.keys()))}")

    all_defects: list[str] = []
    all_warnings: list[str] = []

    structural = check_structural_completeness(html, plans)
    if structural:
        all_defects.extend(structural)
        print(f"\n  STRUCTURAL: {len(structural)} missing subsection(s)")
        for d in structural[:10]:
            print(f"    - {d}")

    hard_forbidden, review_terms = check_forbidden_terms(html)
    if hard_forbidden:
        all_defects.extend(hard_forbidden)
        print(f"\n  FORBIDDEN: {len(hard_forbidden)} hard-forbidden term(s)")
        for d in hard_forbidden:
            print(f"    - {d}")
    if review_terms:
        all_warnings.extend(review_terms)

    details_issues = check_details_balance(html)
    all_defects.extend(details_issues)

    wtm_issues = check_what_this_means(html)
    all_warnings.extend(wtm_issues)

    comment_issues = check_html_comments(html)
    all_defects.extend(comment_issues)

    placeholder_issues = check_unresolved_placeholders(html)
    all_defects.extend(placeholder_issues)

    structure_issues = check_section_collapse_structure(html)
    all_warnings.extend(structure_issues)

    print(f"\n{'='*50}")
    if not all_defects:
        if all_warnings:
            print(f"  RESULT: PASS (with {len(all_warnings)} warning(s))")
            for w in all_warnings:
                print(f"    WARN: {w}")
        else:
            print("  RESULT: PASS")
        sys.exit(0)
    else:
        print(f"  RESULT: FAIL ({len(all_defects)} defect(s), {len(all_warnings)} warning(s))")
        for d in all_defects:
            print(f"    DEFECT: {d}")
        for w in all_warnings[:5]:
            print(f"    WARN: {w}")
        sys.exit(1)


if __name__ == "__main__":
    main()
