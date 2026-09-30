#!/usr/bin/env python3
"""Mechanical lint of a draft's client text, run before the LLM verify pass.

usage: lint_client_text.py <DRAFT.md> [--out LINT.md]

Finds the `## Draft` block (the fenced code block under that heading) and flags each
sentence that matches a pattern the claims standard (ecat-client-email/CLAIMS_STANDARD.md)
says must be checked. A placeholder is an automatic failure; every other hit is a row the
verifier must rule on. Free and instant: it replaces the part of the verify pass that
was only pattern-spotting.
Exit code: 2 if a placeholder is present, 1 if there are other hits, 0 if none.
"""
import argparse, re, sys
from pathlib import Path

PATTERNS = [
    ("placeholder", r"\[[^\]]{0,40}\]|<[^>]{1,30}>|\bTBD\b|\bXX\b|\?\?\?"),
    ("relative time", r"\b(today|yesterday|tomorrow|this (morning|afternoon|evening|week)|last (week|night)|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"),
    ("exclusive / count", r"\b(only|all|every|each|none|never|always|no one|nobody|the rest of)\b"),
    ("past-tense action by us", r"\b(i|we)('ve| have)? (sent|attached|passed|raised|enabled|fixed|updated|uploaded|changed|logged|asked|added|removed|set up|turned on)\b"),
    ("likely cause", r"\b(most likely|probably|looks like|seems to|appears to|likely)\b"),
    ("causal link", r"\b(because|which is why|that's why|so that|since the)\b"),
    ("concession / apology", r"\b(fair point|you're right|you are right|that's on me|we should have|sorry|apologi[sz]e)\b"),
    ("release / time promise", r"\b(next update|next release|this week|by (monday|tuesday|wednesday|thursday|friday|end of)|shortly|soon)\b"),
    ("run limit", r"\b(i can't|i cannot|i'm unable|i don't have access|i couldn't) (open|see|view|access|read)\b"),
    ("menu path / label", r"(>|→)|\b(settings|tools|admin reports|my account|tap|click|select)\b"),
    ("state from an earlier message", r"\b(as (i|we) (said|mentioned|noted)|we (loaded|imported|set up) |from the files we|once the .{0,40}(is|are) (finished|done|fixed))\b"),
]

def client_text(md: str) -> tuple[str, int]:
    m = re.search(r"^## Draft\s*$", md, re.M)
    if not m:
        sys.exit("no '## Draft' heading")
    rest = md[m.end():]
    f = re.search(r"```[a-z]*\n(.*?)```", rest, re.S)
    if not f:
        sys.exit("no fenced block under '## Draft'")
    start_line = md[:m.end()].count("\n") + rest[:f.start()].count("\n") + 2
    return f.group(1), start_line

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--out")
    a = ap.parse_args()
    md = Path(a.draft).read_text()
    text, first = client_text(md)
    rows, placeholder = [], False
    for i, line in enumerate(text.splitlines()):
        for name, pat in PATTERNS:
            for hit in re.finditer(pat, line, re.I):
                if name == "placeholder" and re.fullmatch(r"<https?://[^>]+>", hit.group(0)):
                    continue
                rows.append((first + i, name, hit.group(0), line.strip()[:160]))
                placeholder |= name == "placeholder"
    words = len(text.split())
    out = ["## Lint (mechanical)", "", f"Client text: {words} words, {len(rows)} hits."
           + (" PLACEHOLDER PRESENT: automatic FAIL." if placeholder else ""),
           "", "| line | pattern | match | sentence |", "|---|---|---|---|"]
    out += [f"| {l} | {n} | `{h}` | {s.replace('|', '/')} |" for l, n, h, s in rows]
    report = "\n".join(out) + "\n"
    if a.out:
        Path(a.out).write_text(report)
    print(report)
    sys.exit(2 if placeholder else (1 if rows else 0))

if __name__ == "__main__":
    main()
