"""Extract the deterministic core of a report by stripping LLM slot content.

Used by regression.sh for split verification: the deterministic core must be
byte-identical across runs; the prose slots are validated separately by
prose_conformance_check.py.

Slot boundary markers have the form:
    <!--slot:X-->...content...<!--/slot:X-->

Everything between (and including) the markers is replaced with a stable
placeholder so the remaining file checksums identically regardless of LLM output.

Usage:
    python -m pipeline.extract_deterministic_core <file.html|file.md>
    # Writes deterministic core to stdout (for piping to shasum)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SLOT_PATTERN = re.compile(
    r"<!--slot:([A-F])-->(.*?)<!--/slot:\1-->",
    re.DOTALL,
)

PLACEHOLDER = "<!--slot:{slot}-->[LLM_PROSE]<!--/slot:{slot}-->"


def extract_deterministic_core(content: str) -> str:
    """Replace all slot content with stable placeholders."""
    def _replace(m: re.Match) -> str:
        slot = m.group(1)
        return PLACEHOLDER.format(slot=slot)

    return SLOT_PATTERN.sub(_replace, content)


def core_sha256(content: str) -> str:
    """SHA-256 of the deterministic core."""
    import hashlib
    core = extract_deterministic_core(content)
    return hashlib.sha256(core.encode("utf-8")).hexdigest()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m pipeline.extract_deterministic_core <file>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    core = extract_deterministic_core(content)
    sys.stdout.write(core)


if __name__ == "__main__":
    main()
