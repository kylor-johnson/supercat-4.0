"""Remove mutable list/action claims from authored Slot A prose.

Slot A may synthesize the story, but the post-screen call list, selected plays,
and live activity counts belong to deterministic template blocks.
"""
from __future__ import annotations

import re


_PRIORITY_ACTIONS = re.compile(
    r"(?im)^\s*\*\*priority actions[^\n]*\*\*\s*$"
)
_DERIVED_LINE = re.compile(
    r"(?:"
    r"\bcall[- ]list\b|"
    r"\bcall queue\b|"
    r"\bat-risk list\b|"
    r"\bwatch\s*list\b|"
    r"\bwatchlist\b|"
    r"#\d+\s+at-risk\s+account\b|"
    r"\bsecond\s+call\b|"
    r"\bfull\s+queue\b|"
    r"\bleads? the (?:call|at-risk) list\b|"
    r"\b\d+(?:-call|\s+calls?)\b|"
    r"\b(?:one|two|three|four|five|six|seven)(?:\s+\w+){0,2}\s+calls?\b|"
    r"\b\d+\s+plays?\b|"
    r"\bplays? below\b|"
    r"\bonly\b[^\n.]*\bdecline\b[^\n.]*\bother\b|"
    r"\b\d[\d,]*\s+reps?\s+are\s+enrolled\b|"
    r"\b\d[\d,]*\s+enrolled\s+reps?\b|"
    r"\bactive\s+(?:iPad\s+)?seats?\b"
    r")",
    re.IGNORECASE,
)
_NUMBERED = re.compile(r"^(\s*)\d+\.\s+(.*)$")
_THREE_THINGS = re.compile(
    r"^\s*\*\*Three things you wouldn['’]t have known without this report:\*\*\s*$",
    re.IGNORECASE,
)
_ECAT_RATE = re.compile(
    r"(?:\d+(?:\.\d+)?%|\$[\d,.]+[KMB]?\s+of\s+\$|of\s+the\s+total)",
    re.IGNORECASE,
)
_WATCHLIST_CLAUSE = re.compile(
    r",?\s+and\s+\$[\d,.]+[KMB]?\s+across\s+\d[\d,]*\s+accounts?"
    r"\s+(?:pulling back|at risk)",
    re.IGNORECASE,
)


def _strip_ecat_rate_sentences(line: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", line)
    kept = [
        sentence
        for sentence in sentences
        if not (
            re.search(r"\becat\b", sentence, re.IGNORECASE)
            and _ECAT_RATE.search(sentence)
        )
    ]
    return " ".join(kept)


def sanitize_hero_framing(text: str | None) -> str | None:
    """Strip mutable section-menu claims while preserving narrative synthesis."""
    if not text:
        return text

    priority = _PRIORITY_ACTIONS.search(text)
    if priority:
        text = text[: priority.start()]

    kept: list[str] = []
    for line in text.splitlines():
        line = _WATCHLIST_CLAUSE.sub("", line)
        line = _strip_ecat_rate_sentences(line)
        if not line.strip():
            continue
        if _DERIVED_LINE.search(line):
            continue
        kept.append(line.rstrip())

    numbered_indexes = [
        i for i, line in enumerate(kept) if _NUMBERED.match(line)
    ]
    if len(numbered_indexes) != 3:
        kept = [
            "**What stands out:**" if _THREE_THINGS.match(line) else line
            for line in kept
        ]

    next_number = 1
    for i, line in enumerate(kept):
        match = _NUMBERED.match(line)
        if match:
            kept[i] = f"{match.group(1)}{next_number}. {match.group(2)}"
            next_number += 1

    cleaned = "\n".join(kept).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned or None
