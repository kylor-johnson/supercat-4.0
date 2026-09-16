"""
Insightful Product 3.0 — Context Bundle Builder

Runs after data_gather.py and before section building (Step 2.5).
Produces one section_NN_context.md per INCLUDE section, bundling:
  - shared_rules excerpt (per-section — NOT the full file)
  - gate_flags.md (full)
  - section_confidence.md (full)
  - the section guide (verbatim)
  - section_shared_contract.md (verbatim)
  - all cache files the section needs (verbatim or "(not present)")
  - authority excerpts where required (Q-02/Q-03 for §5, peer_benchmark for §7)

No database calls — pure file I/O. Completes in under 1 second.

Usage:
    python build_context.py --shortname ufi --run-date 2026-06-16
    python build_context.py --shortname ufi --run-date 2026-06-16 --section 2
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Section guide filenames (relative to guides/)
SECTION_GUIDES: dict[int, str] = {
    1: "section_01_signals.md",
    2: "section_02_accounts.md",
    3: "section_03_product.md",
    4: "section_04_commerce.md",
    5: "section_05_team.md",
    6: "section_06_platform.md",
}

# Gold-standard report (authority/) — the canonical example. We slice the matching
# section out of it and embed it in each bundle as a "match this markup exactly"
# target. This is what keeps parallel section agents converging on one structure
# instead of each reconstructing HTML from prose and drifting.
GOLD_REPORT_FILE = "example-co-intelligence-report.html"

# section_num -> the id="" of its block in the gold report.
GOLD_SECTION_IDS: dict[int, str] = {
    1: "signals",
    2: "accounts",
    3: "product",
    4: "commerce",
    5: "team",
    6: "platform",
}

# All section ids in the order they appear in the gold report, plus the trailing
# "appendix" as an end sentinel so the last real section slices cleanly.
GOLD_IDS_IN_FILE_ORDER = [
    "signals", "team", "accounts", "product", "commerce", "platform", "appendix",
]

# Shared rules sections each report section needs.
# All sections get the BASE set; some get additional sections.
SHARED_RULES_BASE = ["A0", "A1", "H", "K"]
SHARED_RULES_EXTRA: dict[int, list[str]] = {
    2: ["E", "M"],
    4: ["E"],
    5: ["D", "E"],
}

# Max table rows to embed in context bundles (prevents 1.4MB bundles).
# Files not listed here are embedded in full.
CACHE_TRUNCATION: dict[str, int] = {
    "Q-38a_results.md": 50,
    "Q-ORG-NBP_results.md": 30,
    "Q-ORG-NEWITEM_results.md": 25,
    "Q-53_results.md": 20,
    "Q-01_step1_results.md": 40,
}

# Cache files each section needs (derived from each guide's "Query Inputs" block)
SECTION_CACHE_FILES: dict[int, list[str]] = {
    1: [
        "signal_rank.md",
    ],
    2: [
        "signal_rank.md",
        "top_accounts.md",
        "Q-12_results.md",
        "Q-14_results.md",
        "Q-14b_results.md",
        "Q-17_results.md",
        "Q-17_atrisk_results.md",
        "Q-40_results.md",
        "Q-41_results.md",
        "Q-41_rep_results.md",
        "Q-52_results.md",
        "Q-53_results.md",
        "Q-54_results.md",
        "Q-57_results.md",
        "Q-66_results.md",
        "Q-67_results.md",
        "Q-68_results.md",
        "Q-ORG-DECAY_results.md",
        "Q-ORG-DECAY_items_results.md",
        "Q-ORG-NBP_results.md",
        "Q-ORG-CONTRACTION_results.md",
        "Q-ORG-VELOCITY_results.md",
        "Q-ORG-STOCKOUT_results.md",
    ],
    3: [
        "signal_rank.md",
        "Q-07_results.md",
        "Q-37_results.md",
        "Q-38a_results.md",
        "Q-39_category_results.md",
        "Q-39_collection_results.md",
        "Q-42_results.md",
        "Q-59_results.md",
        "Q-61_results.md",
        "Q-ORG-GHOST_results.md",
        "Q-ORG-STOCKOUT_results.md",
        "Q-ORG-NEWITEM_results.md",
    ],
    4: [
        "signal_rank.md",
        "Q-CHANNEL-MIX_results.md",
        "Q-13_results.md",
        "Q-16_results.md",
        "Q-18_partA_results.md",
        "Q-18_partB_results.md",
        "Q-18_results.md",
        "Q-19_results.md",
        "Q-20_results.md",
        "Q-21_results.md",
        "Q-41_results.md",
        "Q-45_results.md",
        "Q-52_results.md",
        "Q-55_results.md",
        "Q-56_results.md",
        "Q-58_results.md",
        "Q-58b_results.md",
        "Q-60_results.md",
        "Q-69_results.md",
        "Q-ORG-VELOCITY_results.md",
    ],
    5: [
        "signal_rank.md",
        "coaching_candidates.md",
        "Q-01_step1_results.md",
        "Q-01_step2_results.md",
        "Q-04_results.md",
        "Q-05_results.md",
        "Q-06_results.md",
        "Q-18_results.md",
        "Q-43_results.md",
        "Q-43_step2_results.md",
        "Q-51_results.md",
        "Q-62_results.md",
        "Q-63_results.md",
        "Q-64_results.md",
        "Q-65_results.md",
        "Q-70_results.md",
        "showroom_scan_results.md",
        "user_group_mapping.md",
    ],
    6: [
        "signal_rank.md",
        "Q-07_results.md",
        "Q-08_results.md",
        "Q-09_results.md",
        "Q-09_recent_results.md",
        "Q-10_results.md",
        "Q-11_results.md",
        "Q-22_results.md",
        "Q-CI-02_results.md",
        "Q-CI-03_results.md",
        "Q-CI-03_benchmarks_results.md",
        "Q-CI-05_results.md",
        "peer_benchmark_extract.md",
    ],
}


def parse_shared_rules_sections(text: str) -> dict[str, str]:
    """Parse shared_rules.md into a dict of section_id -> section_text.

    Section IDs are extracted from headings like '## A0.', '## A1.', '## A.', etc.
    """
    heading_re = re.compile(r"^## ([A-Z]\d?)\.", re.MULTILINE)
    matches = list(heading_re.finditer(text))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        section_id = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[section_id] = text[start:end].rstrip()
    return sections


def build_shared_rules_excerpt(
    shared_rules_text: str, section_num: int
) -> str:
    """Build a per-section excerpt of shared_rules.md."""
    parsed = parse_shared_rules_sections(shared_rules_text)
    needed = list(SHARED_RULES_BASE)
    extras = SHARED_RULES_EXTRA.get(section_num, [])
    needed.extend(extras)

    parts: list[str] = []
    parts.append("# Shared Rules (excerpt for this section)\n")
    for section_id in needed:
        content = parsed.get(section_id)
        if content:
            parts.append(content)
            parts.append("")

    return "\n".join(parts)


def parse_manifest(manifest_path: Path) -> dict[int, str]:
    """Parse section_manifest.md → {section_num: status}."""
    text = manifest_path.read_text(encoding="utf-8")
    sections: dict[int, str] = {}
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "§" in line.lower():
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 4:
            try:
                num = int(cells[1])
                status = cells[3]
                sections[num] = status
            except (ValueError, IndexError):
                continue
    return sections


def extract_query_library_excerpt(ql_path: Path, q_ids: list[str]) -> str:
    """Extract specific Q-ID sections from query_library.md."""
    if not ql_path.exists():
        return "(authority/query_library.md not found)\n"

    text = ql_path.read_text(encoding="utf-8")
    header_re = re.compile(r"^### (Q-[\w-]+(?:\s+(?:Step\s+\d+|Part\s+[A-Z]))?):", re.MULTILINE)
    sections = list(header_re.finditer(text))

    excerpts: list[str] = []
    for target in q_ids:
        for i, m in enumerate(sections):
            if m.group(1).strip() == target:
                start = m.start()
                end_idx = sections[i + 1].start() if i + 1 < len(sections) else len(text)
                chunk = text[start:end_idx].rstrip()
                if chunk.endswith("---"):
                    chunk = chunk[:-3].rstrip()
                excerpts.append(chunk)
                break
        else:
            excerpts.append(f"(Q-ID {target} not found in query_library.md)")

    return "\n\n".join(excerpts)


def extract_gold_section(gold_html: str, section_num: int) -> str | None:
    """Slice the matching section out of the gold-standard report.

    Returns the HTML for this section's `<details>`/`<div>` block, or None if the
    section id isn't present. Boundaries: from this block's opening tag up to the
    next section block's opening tag (in file order), which lands exactly on the
    block's own closing tag because the gold report glues sections together
    (`...</details><details id="next">...`).
    """
    target_id = GOLD_SECTION_IDS.get(section_num)
    if not target_id:
        return None

    def open_pos(sid: str) -> int | None:
        m = re.search(
            r'<(?:div|details)\b[^>]*\bid="' + re.escape(sid) + r'"[^>]*>',
            gold_html,
        )
        return m.start() if m else None

    start = open_pos(target_id)
    if start is None:
        return None

    # End = nearest following section-block opening tag in the gold report.
    later = [p for sid in GOLD_IDS_IN_FILE_ORDER
             if (p := open_pos(sid)) is not None and p > start]
    end = min(later) if later else len(gold_html)
    return gold_html[start:end].strip()


def read_file_safe(path: Path) -> str | None:
    """Read a file, returning None if it doesn't exist or is empty."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text if text else None


def build_section_context(
    section_num: int,
    cache_dir: Path,
    guides_dir: Path,
    authority_dir: Path,
    shared_rules_text: str,
    gate_flags: str,
    section_confidence: str,
    client_name: str,
    shortname: str,
    run_date: str,
    gold_html: str,
) -> str:
    """Build the complete context bundle for one section."""
    parts: list[str] = []

    parts.append(
        f"# Section {section_num} Context Bundle — {client_name} ({shortname})\n"
        f"Run date: {run_date}\n"
    )

    # Gate flags (full — small enough and sections reference different subsets)
    parts.append("## Gate Flags\n")
    parts.append(gate_flags)

    # Section confidence
    parts.append("\n## Section Confidence\n")
    parts.append(section_confidence)

    # Section guide (verbatim)
    guide_file = SECTION_GUIDES.get(section_num)
    if guide_file:
        guide_path = guides_dir / guide_file
        guide_text = read_file_safe(guide_path)
        if guide_text:
            parts.append(f"\n## Section Guide — {guide_file}\n")
            parts.append(guide_text)
        else:
            parts.append(f"\n## Section Guide — {guide_file}\n")
            parts.append(f"(ERROR: {guide_file} not found at {guide_path})")

    # Gold-standard target structure for THIS section (the canonical example).
    gold_section = extract_gold_section(gold_html, section_num)
    if gold_section:
        parts.append(
            "\n## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)\n"
        )
        parts.append(
            "This is the corresponding section from the canonical reference report. "
            "It is the source of truth for HTML structure: tag nesting, class names, "
            "column headers, subsection order, which subsections carry a "
            "`what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` "
            "patterns. The data values below are illustrative — replace them with "
            "this client's data — but reproduce the STRUCTURE exactly. Where this "
            "target and the prose guide disagree on markup, THIS WINS.\n"
        )
        parts.append("```html")
        parts.append(gold_section)
        parts.append("```")
    else:
        parts.append(
            "\n## TARGET STRUCTURE — Gold Standard\n"
            f"(WARNING: no gold-standard block found for section {section_num})"
        )

    # Shared contract (cross-section boilerplate: confidence headers, gate checks, etc.)
    contract_path = guides_dir / "section_shared_contract.md"
    contract_text = read_file_safe(contract_path)
    if contract_text:
        parts.append("\n## Section Shared Contract\n")
        parts.append(contract_text)
    else:
        parts.append("\n## Section Shared Contract\n")
        parts.append(f"(WARNING: section_shared_contract.md not found at {contract_path})")

    # Shared rules (per-section excerpt — NOT the full file)
    parts.append("\n")
    parts.append(build_shared_rules_excerpt(shared_rules_text, section_num))

    # Authority excerpts (section-specific)
    if section_num == 5:
        parts.append("\n## Authority — Q-02 & Q-03 Derivation Rules\n")
        parts.append(
            "These classification and funnel-gap rules are applied to Q-01 Step 1 data "
            "when building the Behavioral Scorecard and Coaching subsections. "
            "They are not pre-computed by Stage 1.\n\n"
        )
        ql_path = authority_dir / "query_library.md"
        parts.append(extract_query_library_excerpt(ql_path, ["Q-02", "Q-03"]))

    if section_num == 7:
        parts.append("\n## Authority — Peer Benchmark Reference\n")
        pb_path = authority_dir / "peer_benchmark.md"
        pb_text = read_file_safe(pb_path)
        if pb_text:
            parts.append(pb_text)
        else:
            parts.append(f"(ERROR: peer_benchmark.md not found at {pb_path})")

    # Cache data (verbatim per file, with explicit "not present" for missing)
    cache_files = SECTION_CACHE_FILES.get(section_num, [])
    if cache_files:
        parts.append("\n## Cache Data\n")
        for filename in cache_files:
            parts.append(f"### {filename}\n")
            file_path = cache_dir / filename
            content = read_file_safe(file_path)
            if content:
                max_lines = CACHE_TRUNCATION.get(filename)
                if max_lines and content.count("\n") > max_lines:
                    lines = content.split("\n")
                    header_end = next(
                        (i for i, l in enumerate(lines) if l.startswith("| ---")), 6
                    ) + 1
                    header = "\n".join(lines[:header_end])
                    data_lines = [l for l in lines[header_end:] if l.strip().startswith("|")]
                    total_rows = len(data_lines)
                    kept = data_lines[:max_lines]
                    content = header + "\n" + "\n".join(kept) + f"\n\n*(Truncated: showing top {max_lines} of {total_rows} rows. Full data in cache file.)*"
                parts.append(content)
            else:
                parts.append(f"(not present — file does not exist or is empty)")
            parts.append("")  # blank line separator

    return "\n".join(parts)


def extract_client_name(gate_flags_text: str) -> str:
    """Extract client name from gate_flags.md Org Identity section."""
    for line in gate_flags_text.splitlines():
        if "Client name" in line:
            match = re.search(r"\*\*Client name\*\*:\s*(.+)", line)
            if match:
                return match.group(1).strip()
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Insightful Product 3.0 — Context Bundle Builder",
    )
    parser.add_argument("--shortname", required=True, help="Org shortname")
    parser.add_argument("--run-date", required=True, help="Run date (YYYY-MM-DD)")
    parser.add_argument(
        "--section", type=int, default=None,
        help="Build bundle for a single section only (e.g. --section 2)",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    cache_dir = project_root / "runs" / f"{args.shortname}_{args.run_date}" / "cache"
    guides_dir = project_root / "operators" / "external" / "guides"
    authority_dir = project_root / "authority"

    if not cache_dir.exists():
        print(f"ERROR: Cache directory not found: {cache_dir}", file=sys.stderr)
        sys.exit(1)

    manifest_path = cache_dir / "section_manifest.md"
    if not manifest_path.exists():
        print(f"ERROR: section_manifest.md not found in {cache_dir}", file=sys.stderr)
        sys.exit(1)

    # Load shared files once
    shared_rules_path = authority_dir / "shared_rules.md"
    shared_rules_text = read_file_safe(shared_rules_path) or "(ERROR: shared_rules.md not found)"

    gold_path = authority_dir / GOLD_REPORT_FILE
    gold_html = read_file_safe(gold_path)
    if gold_html is None:
        print(
            f"WARNING: gold-standard report not found at {gold_path} — "
            "bundles will omit the TARGET STRUCTURE block.",
            file=sys.stderr,
        )
        gold_html = ""

    gate_flags_path = cache_dir / "gate_flags.md"
    gate_flags = read_file_safe(gate_flags_path) or "(ERROR: gate_flags.md not found)"

    confidence_path = cache_dir / "section_confidence.md"
    section_confidence = read_file_safe(confidence_path) or "(section_confidence.md not present)"

    client_name = extract_client_name(gate_flags)

    # Parse manifest for INCLUDE sections
    manifest = parse_manifest(manifest_path)
    include_sections = sorted(
        num for num, status in manifest.items()
        if status == "INCLUDE" and num in SECTION_GUIDES
    )

    # Filter to single section if requested
    if args.section is not None:
        if args.section not in include_sections:
            print(
                f"ERROR: Section {args.section} is not in INCLUDE list "
                f"(available: {include_sections})",
                file=sys.stderr,
            )
            sys.exit(1)
        include_sections = [args.section]

    if not include_sections:
        print("No INCLUDE sections found in manifest — nothing to bundle.")
        return

    print(f"Building context bundles for {len(include_sections)} section(s)...")

    for section_num in include_sections:
        context = build_section_context(
            section_num=section_num,
            cache_dir=cache_dir,
            guides_dir=guides_dir,
            authority_dir=authority_dir,
            shared_rules_text=shared_rules_text,
            gate_flags=gate_flags,
            section_confidence=section_confidence,
            client_name=client_name,
            shortname=args.shortname,
            run_date=args.run_date,
            gold_html=gold_html,
        )

        output_path = cache_dir / f"section_{section_num:02d}_context.md"
        output_path.write_text(context, encoding="utf-8")

        cache_files = SECTION_CACHE_FILES.get(section_num, [])
        present = sum(1 for f in cache_files if (cache_dir / f).exists())
        size_kb = len(context.encode("utf-8")) / 1024

        print(
            f"  §{section_num}: {output_path.name} "
            f"({size_kb:.1f} KB, {present}/{len(cache_files)} cache files present)"
        )

    print(f"\nDone. Context bundles written to {cache_dir}/")


if __name__ == "__main__":
    main()
