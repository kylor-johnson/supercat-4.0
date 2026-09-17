"""Extract client-visible text from a rendered report.

The baseline/diff harness compares what a CEO actually READS, not markup.
A template refactor that changes class names but no copy must produce a
zero-line diff; a copy change must produce a readable one.

Usage: python tools/html_to_text.py <file.html|file.md>
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

_DROP_ELEMENTS = re.compile(r"(?is)<(script|style|svg|head)\b.*?</\1>")
_BREAKS = re.compile(r"(?i)<br\s*/?>")
_BLOCK_END = re.compile(
    r"(?i)</(p|div|h1|h2|h3|h4|h5|li|tr|section|table|blockquote|details|summary)>"
)
_CELL_END = re.compile(r"(?i)</t[dh]>")
_TAGS = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t]+")
_BLANKS = re.compile(r"\n\s*\n\s*\n+")


def to_text(source: str) -> str:
    source = _DROP_ELEMENTS.sub(" ", source)
    source = _BREAKS.sub("\n", source)
    source = _BLOCK_END.sub("\n", source)
    source = _CELL_END.sub(" | ", source)
    source = _TAGS.sub("", source)
    source = html.unescape(source)
    source = _WS.sub(" ", source)
    source = "\n".join(line.strip() for line in source.splitlines())
    source = _BLANKS.sub("\n\n", source)
    return source.strip() + "\n"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: html_to_text.py <file>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1
    sys.stdout.write(to_text(path.read_text(encoding="utf-8", errors="replace")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
