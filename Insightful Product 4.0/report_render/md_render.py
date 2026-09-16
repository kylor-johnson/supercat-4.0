"""Markdown rendering helpers — wrap markdown-it-py with the table plugin
on, and expose a single `md_to_html` entry point that the section
transformers share.

We pin GFM-table syntax + soft-break-to-space (matches the Sarreid HTML's
behavior: paragraph wraps don't introduce <br>). HTML-escaping is OFF for the
fenced code-spans the source MD already encodes (we trust the MD, which has
already passed §P).

HTML comments (<!-- ... -->, including multi-line) are stripped from the
Markdown source BEFORE rendering. markdown-it with {"html": False} escapes
them into visible client-facing text rather than dropping them; stripping
pre-render is the durable class-wide fix.
"""
from __future__ import annotations

import re

from markdown_it import MarkdownIt


_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

_md = (
    MarkdownIt("commonmark", {"html": False, "breaks": False, "linkify": False, "typographer": False})
    .enable("table")
    .enable("strikethrough")
)


def _strip_html_comments(text: str) -> str:
    """Remove HTML comments (<!-- ... -->, including multi-line) from MD source."""
    return _HTML_COMMENT_RE.sub("", text)


def md_to_html(text: str) -> str:
    """Convert a chunk of MD source to HTML using the shared renderer."""
    if not text or not text.strip():
        return ""
    return _md.render(_strip_html_comments(text))


def md_inline_to_html(text: str) -> str:
    """Inline-only render (no surrounding <p>): used for table cells, badges, etc."""
    if not text:
        return ""
    return _md.renderInline(_strip_html_comments(text))
