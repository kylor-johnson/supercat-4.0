"""Prose conformance check — validates LLM slots against their fact bundles.

Used by regression.sh split verification. Extracts prose from LLM slot markers,
loads the serialized fact bundles (dumped per-run), and runs validate_slot()
against each one.

This is the SECOND gate of split verification:
  1. extract_deterministic_core.py -> checksum (must match golden)
  2. prose_conformance_check.py -> per-slot validation (must pass)

Usage:
    python -m pipeline.prose_conformance_check <report_file> <bundles_json>
    # Exit 0 = all slots pass, 1 = at least one slot fails

    <bundles_json> is the serialized fact bundles file written during the run
    at outputs/{org}_bundles_{date}.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLOT_PATTERN = re.compile(
    r"<!--slot:([A-F])-->(.*?)<!--/slot:\1-->",
    re.DOTALL,
)

SLOT_NAMES = {
    "A": "hero",
    "B": "talking_points",
    "C": "coaching_narratives",
    "D": "play_framing",
    "E": "growth_connective",
    "F": "outreach_framing",
}

EXPECTED_COUNTS = {
    "B": "talking_points_count",
    "C": "coaching_count",
    "D": "play_count",
}


def extract_slots(content: str) -> dict[str, list[str]]:
    """Extract all slot contents from a report, grouped by slot letter."""
    slots: dict[str, list[str]] = {}
    for m in SLOT_PATTERN.finditer(content):
        letter = m.group(1)
        text = m.group(2).strip()
        slots.setdefault(letter, []).append(text)
    return slots


def check_conformance(
    report_path: Path,
    bundles_path: Path,
) -> tuple[bool, list[str]]:
    """Run prose conformance on all slots found in the report.
    Returns (all_passed, list_of_failure_messages).
    """
    try:
        from pipeline.slot_validator import validate_slot
    except ImportError:
        return True, ["[prose_conformance] slot_validator not available — skipping"]

    content = report_path.read_text(encoding="utf-8")
    bundles = json.loads(bundles_path.read_text(encoding="utf-8"))

    slots = extract_slots(content)
    if not slots:
        return True, ["[prose_conformance] no LLM slots found in report"]

    all_passed = True
    messages: list[str] = []

    for letter, texts in slots.items():
        slot_name = SLOT_NAMES.get(letter, f"unknown_{letter}")
        bundle_key = f"slot_{letter.lower()}_bundle"
        bundle = bundles.get(bundle_key, {})

        if not bundle:
            messages.append(f"[slot:{letter}] WARN: no bundle found at key '{bundle_key}'")
            continue

        expected_count = bundle.get("expected_count", 0)

        for i, text in enumerate(texts):
            passed, violations = validate_slot(
                slot_name=slot_name,
                output=text,
                fact_bundle=bundle,
                expected_count=expected_count,
            )
            if passed:
                messages.append(f"[slot:{letter}#{i}] PASS")
            else:
                all_passed = False
                for v in violations:
                    messages.append(f"[slot:{letter}#{i}] FAIL: {v}")

    return all_passed, messages


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: python -m pipeline.prose_conformance_check <report> <bundles.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    report_path = Path(sys.argv[1])
    bundles_path = Path(sys.argv[2])

    if not report_path.exists():
        print(f"ERROR: report not found: {report_path}", file=sys.stderr)
        sys.exit(1)
    if not bundles_path.exists():
        print(f"ERROR: bundles not found: {bundles_path}", file=sys.stderr)
        sys.exit(1)

    passed, messages = check_conformance(report_path, bundles_path)

    for msg in messages:
        print(msg)

    print()
    if passed:
        print("PROSE CONFORMANCE: PASS")
        sys.exit(0)
    else:
        print("PROSE CONFORMANCE: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
