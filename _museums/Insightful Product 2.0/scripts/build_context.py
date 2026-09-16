"""
Insightful Product 2.0 — Context Bundle Builder

Runs after data_gather.py and before section building (Step 2).
Produces one section_NN_context.md per INCLUDE section, bundling:
  - shared_rules.md (verbatim)
  - gate_flags.md (full)
  - section_confidence.md (full)
  - the section guide (verbatim)
  - all cache files the section needs (verbatim or "(not present)")
  - authority excerpts where required (Q-02/Q-03 for §2, peer_benchmark for §7)

No database calls — pure file I/O. Completes in under 1 second.

Usage:
    python build_context.py --shortname ufi --run-date 2026-06-16
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Section guide filenames (relative to guides/)
SECTION_GUIDES: dict[int, str] = {
    2: "section_02_sales_team.md",
    3: "section_03_customers.md",
    4: "section_04_product.md",
    5: "section_05_commerce.md",
    6: "section_06_portal.md",
    7: "section_07_peer.md",
    8: "section_08_platform.md",
}

# Cache files each section needs (derived from each guide's "Query Inputs" block)
SECTION_CACHE_FILES: dict[int, list[str]] = {
    2: [
        "Q-01_step1_results.md",
        "Q-01_step2_results.md",
        "Q-04_results.md",
        "Q-05_results.md",
        "Q-06_results.md",
        "Q-43_step2_results.md",
        "showroom_scan_results.md",
        "Q-51_results.md",
        "Q-62_results.md",
        "Q-63_results.md",
        "Q-64_results.md",
        "Q-65_results.md",
        "Q-70_results.md",
        "user_group_mapping.md",
    ],
    3: [
        "Q-12_results.md",
        "Q-14_results.md",
        "Q-17_results.md",
        "Q-17_atrisk_results.md",
        "Q-40_results.md",
        "Q-41_results.md",
        "Q-41_rep_results.md",
        "Q-52_results.md",
        "Q-53_results.md",
        "Q-54_results.md",
        "Q-14b_results.md",
        "Q-57_results.md",
        "Q-66_results.md",
        "Q-67_results.md",
        "Q-68_results.md",
    ],
    4: [
        "Q-07_results.md",
        "Q-37_results.md",
        "Q-38a_results.md",
        "Q-39_category_results.md",
        "Q-39_collection_results.md",
        "Q-42_results.md",
        "Q-59_results.md",
        "Q-61_results.md",
    ],
    5: [
        "Q-13_results.md",
        "Q-16_results.md",
        "Q-18_partA_results.md",
        "Q-18_partB_results.md",
        "Q-20_results.md",
        "Q-21_results.md",
        "Q-45_results.md",
        "Q-52_results.md",
        "Q-55_results.md",
        "Q-56_results.md",
        "Q-58_results.md",
        "Q-58b_results.md",
        "Q-60_results.md",
        "Q-69_results.md",
    ],
    6: [
        "Q-CL-01_results.md",
        "Q-CL-03_results.md",
        "Q-CL-05_results.md",
    ],
    7: [
        "peer_benchmark_extract.md",
        "Q-CI-02_results.md",
        "Q-CI-03_results.md",
        "Q-CI-03_benchmarks_results.md",
        "Q-CI-05_results.md",
    ],
    8: [
        "Q-07_results.md",
        "Q-08_results.md",
        "Q-09_results.md",
        "Q-09_recent_results.md",
        "Q-10_results.md",
        "Q-11_results.md",
        "Q-22_results.md",
        "Q-46_pg_results.md",
        "Q-46_bq_results.md",
        "Q-47_results.md",
        "Q-50_results.md",
        "user_group_mapping.md",
    ],
}


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
    header_re = re.compile(r"^### (Q-\d+[a-z]?(?:\s+(?:Step\s+\d+|Part\s+[A-Z]))?):", re.MULTILINE)
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
    shared_rules: str,
    gate_flags: str,
    section_confidence: str,
    client_name: str,
    shortname: str,
    run_date: str,
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

    # Shared rules (verbatim)
    parts.append("\n## Shared Rules\n")
    parts.append(shared_rules)

    # Authority excerpts (section-specific)
    if section_num == 2:
        parts.append("\n## Authority — Q-02 & Q-03 Derivation Rules\n")
        parts.append(
            "These classification and funnel-gap rules are applied to Q-01 Step 1 data "
            "when building subsections 2, 3, and 4. They are not pre-computed by Stage 1.\n\n"
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
        description="Insightful Product 2.0 — Context Bundle Builder",
    )
    parser.add_argument("--shortname", required=True, help="Org shortname")
    parser.add_argument("--run-date", required=True, help="Run date (YYYY-MM-DD)")
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
    shared_rules_path = guides_dir / "shared_rules.md"
    shared_rules = read_file_safe(shared_rules_path) or "(ERROR: shared_rules.md not found)"

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

    if not include_sections:
        print("No INCLUDE sections found in manifest — nothing to bundle.")
        return

    print(f"Building context bundles for {len(include_sections)} sections...")

    for section_num in include_sections:
        context = build_section_context(
            section_num=section_num,
            cache_dir=cache_dir,
            guides_dir=guides_dir,
            authority_dir=authority_dir,
            shared_rules=shared_rules,
            gate_flags=gate_flags,
            section_confidence=section_confidence,
            client_name=client_name,
            shortname=args.shortname,
            run_date=args.run_date,
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
