"""Canonical output filenames for the Insightful 4.0 factory.

SHIP HTML:  {DisplayName}_CEO_intelligence_report_{date}.html  (from ratified profile H1)
PREVIEW:    {org}_PREVIEW_{date}.html
DRAFT MD:   {org}_DRAFT_{date}.md
GATESTOP:   {org}_GATESTOP_{date}.md
"""
from __future__ import annotations

import re
from pathlib import Path


def parse_display_name_from_profile_text(profile_text: str, fallback: str) -> str:
    """Recover the client display name from a profile markdown H1."""
    if not profile_text:
        return fallback
    m = re.search(r"^#\s+(.+?)\s*$", profile_text, re.M)
    if not m:
        return fallback
    h1_text = m.group(1).strip()
    h1_text = re.sub(r"^Client\s+Profile\s+[—–-]\s+", "", h1_text)
    h1_text = re.sub(r"\s+[—–-]\s+(?:eCat\s+)?client\s+profile\s*$", "", h1_text, flags=re.I)
    h1_text = re.sub(r"\s*\(\s*`[^`]+`\s*\)\s*$", "", h1_text)
    return h1_text.strip() or fallback


def sanitize_display_name(display_name: str) -> str:
    """Filesystem-safe token derived from the profile display name."""
    return (
        display_name.replace(" ", "_")
        .replace(",", "")
        .replace("&", "and")
        .replace("'", "")
        .replace("/", "_")
    )


def ship_html_filename(display_name: str, date: str) -> str:
    return f"{sanitize_display_name(display_name)}_CEO_intelligence_report_{date}.html"


def preview_html_filename(org: str, date: str) -> str:
    return f"{org}_PREVIEW_{date}.html"


def draft_md_filename(org: str, date: str) -> str:
    return f"{org}_DRAFT_{date}.md"


def gatestop_md_filename(org: str, date: str) -> str:
    return f"{org}_GATESTOP_{date}.md"


def ship_html_path(outputs_dir: Path, display_name: str, date: str) -> Path:
    return outputs_dir / ship_html_filename(display_name, date)
