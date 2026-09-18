"""Section transformers — convert per-section MD chunks into the HTML shapes
that match the Sarreid layout (hero, metric cards, CEO callouts, priority rows,
play cards, coaching cards, etc.).

Design notes:
- Each transformer is defensive: when the MD doesn't match the heuristic, it
  falls back to wrapping the raw MD render in a `.prose` block. We never lose
  content; we lose only the bespoke styling on that piece.
- We honor the §5a.6 don't-break invariants: §1 lays out the hero + 4 metric
  cards + 3 CEO callouts + priorities exactly as Sarreid does; §6 renders 5
  coaching cards (or fewer if <5 qualify); §11 honors the 6-item honest list.
- We do NOT add content the MD doesn't carry. If a section's MD has only a
  table and no callout, we render only the table.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Optional

from .md_parse import Chunk, ParsedReport
from .md_render import md_to_html, md_inline_to_html


# ─── Shared utilities ───────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _strip_em_wrappers(text: str) -> str:
    """Strip the trailing `*(NOTE)*` italic wrappers we sometimes pull from MD."""
    return re.sub(r"\s*\*\(.*?\)\*\s*$", "", text).strip()


def _strip_md_inline(text: str) -> str:
    """Strip MD inline markers (**, *, `) for raw-text uses (alt text, titles)."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def _split_heading_prefix(heading: str) -> str:
    """Return only the prefix before the first ' — ' or ' – ' separator.

    Used for h3 subsection titles where the full MD heading carries a suffix
    that belongs in the h2 subtitle, not the h3 label
    (e.g. 'What this report can't see — and what to add next' → 'What this report can't see').
    Falls back to the full heading when no separator is found.
    """
    for sep in (" — ", " – "):
        if sep in heading:
            return heading.split(sep, 1)[0].strip()
    return heading


def _split_paragraphs(md: str) -> list[str]:
    """Split MD into top-level paragraph blocks (blank-line delimited).

    Preserves blockquotes, list groups, table rows as cohesive blocks.

    Consecutive pipe-table blocks are re-joined: a stray blank line between a
    table's header+separator and its body rows (a common Jinja whitespace
    artifact) would otherwise split one table into an empty-body table plus a
    headerless table whose first data row renders as a `<thead>`. Two genuinely
    distinct tables are always separated by prose or a heading, never by a bare
    blank line, so re-joining only repairs the artifact.
    """
    blocks = [block.strip() for block in re.split(r"\n\s*\n", md.strip()) if block.strip()]
    merged: list[str] = []
    for block in blocks:
        if merged and _is_table(block) and _is_table(merged[-1]):
            merged[-1] = merged[-1] + "\n" + block
        else:
            merged.append(block)
    return merged


# ─── Client-facing cell cleanup (raw ERP strings → readable) ────────────────

# Connector words that stay lowercase inside a title-cased proper name.
_TITLE_CONNECTORS = {"and", "or", "of", "the", "for", "to", "a", "an", "in", "on", "at", "by", "&"}
# Short tokens / initialisms that stay ALL-CAPS (brand initials, LLC, USA…).
_TITLE_KEEP_UPPER = {"LLC", "DBA", "USA", "US", "LP", "LLP", "HQ", "TV", "NYC", "UK", "USP"}
# Common company suffixes that read better title-cased than shouted.
_TITLE_SUFFIX_MAP = {"INC": "Inc", "CO": "Co", "CORP": "Corp", "LTD": "Ltd", "LTDA": "Ltda", "COMPANY": "Company"}


def _smart_titlecase(text: str) -> str:
    """Title-case an ALL-CAPS proper name the way the north star renders it:
    "FRANCE AND SONS" → "France and Sons", "OP JENKINS FURNITURE & DESIGN" →
    "OP Jenkins Furniture & Design", "ENGLISH GEORGIAN AMERICA LLC" →
    "English Georgian America LLC". Only touches shouty strings; mixed-case
    input is returned unchanged by the caller."""
    out_words: list[str] = []
    for i, word in enumerate(text.split()):
        low = word.lower()
        upper = word.upper()
        if upper in _TITLE_KEEP_UPPER:
            out_words.append(upper)
        elif upper in _TITLE_SUFFIX_MAP:
            out_words.append(_TITLE_SUFFIX_MAP[upper])
        elif low in _TITLE_CONNECTORS and i != 0:
            out_words.append(low)
        elif word.isupper() and len(re.sub(r"[^A-Za-z]", "", word)) <= 3:
            # Short all-caps token → brand initialism (AFA, OP, JC): keep it.
            out_words.append(word)
        else:
            # Capitalize first letter, lowercase the rest; preserve apostrophes
            # ("SWAN'S" → "Swan's").
            out_words.append(word[:1].upper() + word[1:].lower())
    return " ".join(out_words)


def _clean_cell(text: str) -> str:
    """Normalize a raw table cell for client display: collapse whitespace runs
    (raw ERP item names carry double spaces) and title-case ALL-CAPS names
    (raw `bill_to_name` is shouted). Leaves mixed-case, numeric, and
    already-formatted cells untouched."""
    if not text:
        return text
    cleaned = re.sub(r"[ \t]{2,}", " ", text).strip()
    letters = re.sub(r"[^A-Za-z]", "", cleaned)
    # Only re-case a cell that is shouting: has letters, no lowercase at all.
    if len(letters) >= 3 and cleaned == cleaned.upper() and not cleaned.isdigit():
        cleaned = _smart_titlecase(cleaned)
    return cleaned


# A "table block" is two-or-more consecutive lines starting with `|`.
_TABLE_LINE = re.compile(r"^\s*\|")


def _parse_md_table(block: str) -> Optional[list[list[str]]]:
    """Parse a pipe-table block into rows of cells (text only — no rendering).

    The first row is the header; row 2 (the `|---|` separator) is discarded.
    Returns None if `block` doesn't look like a table.
    """
    lines = [ln for ln in block.splitlines() if ln.strip()]
    if len(lines) < 2 or not all(_TABLE_LINE.match(ln) for ln in lines):
        return None
    rows: list[list[str]] = []
    for ln in lines:
        # Skip the alignment separator row (---|---|---).
        if re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", ln) and "-" in ln:
            continue
        cells = ln.strip().strip("|").split("|")
        rows.append([c.strip() for c in cells])
    return rows


def _render_table_with_classes(rows: list[list[str]], row_class_fn=None) -> str:
    """Render a 2D `rows` list into a `<table>` wrapped in `.table-wrap`.

    `row_class_fn(cells, idx) -> str|None` lets callers tint rows.
    """
    if not rows:
        return ""
    header, *body = rows
    parts: list[str] = ['<div class="table-wrap">', "<table>"]
    parts.append("<thead><tr>")
    for cell in header:
        parts.append(f"<th>{md_inline_to_html(cell)}</th>")
    parts.append("</tr></thead>")
    parts.append("<tbody>")
    for idx, row in enumerate(body):
        row_cls = row_class_fn(row, idx) if row_class_fn else None
        parts.append(f'<tr class="{row_cls}">' if row_cls else "<tr>")
        for cell in row:
            parts.append(f"<td>{md_inline_to_html(_clean_cell(cell))}</td>")
        parts.append("</tr>")
    parts.append("</tbody>")
    parts.append("</table></div>")
    return "".join(parts)


# Bold-colon standalone paragraph → soft subsection boundary
# Matches: **ECat as a channel:** or **Two specific upgrades worth queuing:**
_BOLD_SECTION_LEAD = re.compile(r"^\s*\*\*([^*]+?):\*\*\s*$")

# Money / delta extraction
_DOLLAR = re.compile(r"\$[\d,]+(?:\.\d+)?\s*[KMB]?")
_DELTA = re.compile(r"([+\-−–]\d+(?:\.\d+)?\s*%(?:\s*YoY)?)")
_LONG_DOLLAR = re.compile(r"\$[\d,]+(?:\.\d+)?[KMB]?")


def _classify_delta(delta_text: str) -> str:
    """Return 'ok' / 'bad' / 'flat' based on the sign in a delta string."""
    if not delta_text:
        return "flat"
    cleaned = delta_text.replace("−", "-").replace("–", "-")
    if cleaned.startswith("-"):
        return "bad"
    if cleaned.startswith("+"):
        return "ok"
    return "flat"


# ─── §1 — Summary (hero + metric cards + CEO callouts + priorities) ─────────

def render_summary(
    chunk: Chunk, period_line: str = "", available_ids: set[str] | None = None
) -> str:
    """Render the always-expanded §1 60-second read.

    ``available_ids`` is the set of section ids that will actually render in
    this report. A CEO callout's jump link is dropped when its target is not
    among them — W3 found `#thismonth` dangling on hfg the moment a materiality
    floor made "Do this month" legitimately empty. ``None`` keeps the old
    behaviour (every jump link emitted unconditionally).
    """
    paragraphs = _split_paragraphs(chunk.body_md)
    if not paragraphs:
        return _wrap_open_section("summary", chunk.heading, "")

    # The first paragraph carries the topline (**$X invoiced, +Y% YoY**).
    hero_para = paragraphs[0]
    hero_html = _build_hero(hero_para, period_line)

    # The second paragraph is the "hero sub" prose continuation, if present
    # and short enough to belong in the hero band. The Sarreid HTML pulls it
    # into the hero-sub div; if longer (cohort variants), we keep it as a
    # standalone .prose below the metrics.
    hero_sub_para = ""
    rest_paras = paragraphs[1:]
    # P0-4: a STRUCTURAL lead-in is not the hero sub-paragraph. This branch
    # assumed the block after the hero is always narrative (the Sarreid
    # pattern). When the sanitizer collapses the hero and its numbered list
    # into one block, the next block is "**Priority actions, by cadence:**" —
    # which got glued into the hero as prose while the bullets below still
    # emitted the real sub-label, so 8 of 11 orgs shipped the heading twice.
    if (
        rest_paras
        and not _is_table(rest_paras[0])
        and len(rest_paras[0]) < 600
        and not _is_priorities_lead(rest_paras[0])
        and not _is_three_things_lead(rest_paras[0])
        # T1-3: nor a lead-in FUSED to its numbered findings, nor a bare
        # numbered list. The P0-4 guard only knew the two NAMED lead-ins, so an
        # authored hero using any other wording ("What stands out:") was
        # swallowed into the hero sub and its callout cards never rendered —
        # hfg, cci, ali and clc all shipped zero cards.
        and _split_lead_and_numbered_list(rest_paras[0]) is None
        and not _is_numbered_list(rest_paras[0])
        and not _is_bullet_list(rest_paras[0])
    ):
        hero_sub_para = rest_paras[0]
        rest_paras = rest_paras[1:]
        # If the hero-sub paragraph is what carries the per-metric narrative,
        # attach it to the hero block directly (the Sarreid pattern).
        hero_html = _attach_hero_sub(hero_html, hero_sub_para)
        hero_sub_para = ""

    # Walk the remaining blocks: the first 2-column table becomes the metric
    # cards; a numbered list under "Three things you wouldn't have known
    # without this report" becomes the CEO callouts; a bullet list under
    # "Priority actions, by cadence" becomes the priorities.
    metric_html = ""
    callouts_html = ""
    priorities_html = ""
    remainder_html: list[str] = []

    i = 0
    while i < len(rest_paras):
        block = rest_paras[i]
        # Metric cards: the first 2-column pipe table
        if not metric_html and _is_table(block):
            rows = _parse_md_table(block)
            if rows and _looks_like_metric_table(rows):
                metric_html = _build_metric_cards_from_table(rows)
                i += 1
                continue
        # CEO callouts: the numbered list under "Three things…" lead-in
        if not callouts_html and _is_three_things_lead(block):
            # The numbered list usually follows in the NEXT block
            j = i + 1
            list_block = rest_paras[j] if j < len(rest_paras) else ""
            if _is_numbered_list(list_block):
                callouts_html = _build_ceo_callouts(list_block, available_ids)
                i = j + 1
                continue
        # CEO callouts: alternate pattern where the lead and list share a block
        if not callouts_html and _is_numbered_list(block) and "wouldn'?t have known" in block.lower():
            callouts_html = _build_ceo_callouts(block, available_ids)
            i += 1
            continue
        # Priorities: bullet list under "Priority actions" lead-in
        if not priorities_html and _is_priorities_lead(block):
            j = i + 1
            list_block = rest_paras[j] if j < len(rest_paras) else ""
            if _is_bullet_list(list_block):
                priorities_html = _build_priorities(list_block)
                i = j + 1
                continue
        # Standalone numbered list that looks like CEO callouts (no lead-in)
        if not callouts_html and _is_numbered_list(block) and _looks_like_ceo_callouts(block):
            callouts_html = _build_ceo_callouts(block, available_ids)
            i += 1
            continue
        # A bold lead-in FUSED to its numbered list (no blank line between).
        if not callouts_html:
            split = _split_lead_and_numbered_list(block)
            if split and _looks_like_ceo_callouts(split[1]):
                callouts_html = _build_ceo_callouts(split[1], available_ids)
                i += 1
                continue
        # Standalone priorities bullet list (no lead-in)
        if not priorities_html and _is_bullet_list(block) and _looks_like_priorities(block):
            priorities_html = _build_priorities(block)
            i += 1
            continue
        # Anything else → render as prose under the hero band
        remainder_html.append(_wrap_prose(md_to_html(block)))
        i += 1

    sub_label_callouts = (
        '<div class="sub-label" style="margin-top: 28px;">'
        "Three things you wouldn&rsquo;t have known without this report"
        "</div>"
        if callouts_html else ""
    )
    sub_label_priorities = (
        '<div class="sub-label" style="margin-top: 30px;">Priority actions, by cadence</div>'
        if priorities_html else ""
    )

    body = (
        f"{hero_html}"
        f"{metric_html}"
        f"{(_wrap_prose(md_to_html(hero_sub_para)) if hero_sub_para else '')}"
        f"{sub_label_callouts}{callouts_html}"
        f"{sub_label_priorities}{priorities_html}"
        f"{''.join(remainder_html)}"
    )

    return _wrap_open_section("summary", "The 60-second read", body)


def _wrap_open_section(section_id: str, title: str, body: str) -> str:
    """Wrap an always-expanded section (§1 only in the gold layout)."""
    return (
        f'\n  <section class="section" id="{section_id}">\n'
        f'    <h2 class="section-title">{_esc(title)}</h2>\n'
        f'{body}\n'
        f'  </section>\n'
    )


_TAGS_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _plain(fragment: str) -> str:
    """Tag-stripped, entity-folded, whitespace-normalised text for comparison."""
    txt = _TAGS_RE.sub(" ", fragment or "")
    for ent, ch in (("&middot;", "·"), ("&rsquo;", "\u2019"), ("&nbsp;", " "),
                    ("&amp;", "&"), ("&mdash;", "—"), ("&ndash;", "–")):
        txt = txt.replace(ent, ch)
    return _WS_RE.sub(" ", txt).strip().rstrip(".").lower()


def _drop_leading_echo(body: str, sub_blurb: str) -> str:
    """Remove the body's opening paragraph when it just repeats the teaser."""
    teaser = _plain(sub_blurb)
    if not teaser or len(teaser) < 25:
        return body
    m = re.search(r"<p[^>]*>.*?</p>", body, re.S)
    if not m:
        return body
    first = _plain(m.group(0))
    if not (first == teaser or first.startswith(teaser)):
        return body
    remainder = body[: m.start()] + body[m.end():]
    # Never empty a section. When the echoed paragraph is the ONLY content, the
    # teaser is all the reader would get — keep the body and accept the repeat.
    if not _plain(remainder):
        return body
    return remainder


def _wrap_collapse_section(
    section_id: str,
    title: str,
    body: str,
    variant: str = "",
    is_open: bool = False,
    contents_blurb: str = "",
    sub_blurb: str = "",
    expand_hint: str = "Click to expand",
) -> str:
    """Wrap a `<details class="section-collapse">` collapsible.

    `variant` ∈ {"", "urgent", "month", "quarter"}.
    `title`, `sub_blurb`, `contents_blurb`, `expand_hint` are HTML-safe
    (callers may include `&middot;`, `<span>`, etc. without re-escape).
    """
    cls = f"section-collapse {variant}".strip()
    open_attr = " open" if is_open else ""
    # The teaser and the body were printing the SAME sentence back to back on
    # every section that uses `_default_sub_blurb` (which COPIES the first
    # sentence rather than lifting it, unlike `_render_table_section_smart`).
    # Expanded, the reader saw each section open by repeating its own header.
    body = _drop_leading_echo(body, sub_blurb)
    sub_html = f'<div class="section-sub">{sub_blurb}</div>' if sub_blurb else ""
    contents_html = (
        f'<div class="section-contents">{contents_blurb}</div>'
        if contents_blurb else ""
    )
    expand_html = (
        f'<span class="expand-hint">&#9662; {expand_hint}</span>'
        if not is_open else ""
    )
    return (
        f'\n  <details class="{cls}" id="{section_id}"{open_attr}>\n'
        f'    <summary>\n'
        f'      <h2 class="section-title">{title}</h2>\n'
        f'      {sub_html}\n'
        f'      {contents_html}\n'
        f'      {expand_html}\n'
        f'    </summary>\n'
        f'    <section class="section">\n'
        f'{body}\n'
        f'    </section>\n'
        f'  </details>\n'
    )


def _wrap_prose(rendered_html: str) -> str:
    """Wrap a markdown-it `<p>...</p>` chunk in our `.prose` class, since
    markdown-it doesn't tag <p>'s by default. We also normalize the wrapper:
    if the input is multi-paragraph, we wrap each <p> as a separate .prose."""
    if not rendered_html:
        return ""
    # Replace <p>...</p> with <p class="prose">...</p>
    out = re.sub(r"<p>", '<p class="prose">', rendered_html)
    # Tables and callouts come through as <table>... — pass through unchanged.
    return out


def _is_table(block: str) -> bool:
    return bool(_TABLE_LINE.match(block.splitlines()[0])) if block else False


def _is_numbered_list(block: str) -> bool:
    return bool(re.match(r"^\s*\d+\.\s+", block))


def _is_bullet_list(block: str) -> bool:
    return bool(re.match(r"^\s*[-*]\s+", block))


def _looks_like_metric_table(rows: list[list[str]]) -> bool:
    """A metric table is the 2-column unlabeled-header table the MD uses for
    the §1 "Same dealers, more spend / Jupe / Top field reps / $ at risk" set.
    Header row is often blank (`| | |`)."""
    if len(rows) < 2:
        return False
    header = rows[0]
    # 2-column unlabeled header is the dead giveaway
    return len(header) == 2 and all(not h.strip() for h in header)


HERO_CALLOUTS_MARKER = "<!--hero:callouts-->"


def _split_lead_and_numbered_list(block: str) -> tuple[str, str] | None:
    """Separate a bold lead-in fused to its numbered list.

    T1-3: authored prose files are inconsistent about the blank line between
    the lead-in and the findings — sarreid and kal leave one, hfg/cci/ali do
    not. Without the blank they arrive as ONE markdown block, so neither the
    lead-in test nor the standalone-list test matches and the CEO callout
    cards silently vanish. Presentation must not depend on that convention.
    """
    lines = block.strip().splitlines()
    if len(lines) < 2:
        return None
    lead = lines[0].strip()
    if not (lead.startswith("**") and lead.endswith(("**", "**:", ":")) and len(lead) < 120):
        return None
    rest = "\n".join(lines[1:]).strip()
    if not _is_numbered_list(rest):
        return None
    return lead, rest


def _is_three_things_lead(block: str) -> bool:
    """T1-3: the callout cards are keyed on a STRUCTURAL marker the template
    emits, not on the English of the heading.

    Presentation used to depend on the literal string "Three things you
    wouldn't have known…" — which `hero_sanitizer` rewrites to "What stands
    out:" whenever the numbered-item count isn't exactly 3. One stage rewrote a
    string a later stage pattern-matched on, so the cards silently collapsed to
    a plain numbered list (Sarreid and hfg both lost them). The English is now
    free to change; the marker is the contract.
    """
    if HERO_CALLOUTS_MARKER in block:
        return True
    low = block.lower()
    return "three things you wouldn" in low and "have known" in low


def _looks_like_ceo_callouts(block: str) -> bool:
    """Heuristic: 3 numbered items, each starts with a bolded headline."""
    items = re.split(r"\n\d+\.\s+", "\n" + block.strip())
    items = [it for it in items if it.strip()]
    return len(items) == 3 and all(it.lstrip().startswith("**") for it in items)


def _is_priorities_lead(block: str) -> bool:
    low = block.lower()
    return "priority actions" in low and "cadence" in low


def _looks_like_priorities(block: str) -> bool:
    """A priorities bullet list has each item starting with **This week**: or **This month**:."""
    items = [ln for ln in block.splitlines() if re.match(r"^\s*[-*]\s+", ln)]
    if len(items) < 2:
        return False
    return all(re.search(r"\*\*this\s+(week|month|quarter)[:*]", it.lower()) for it in items)


def _build_hero(first_para: str, period_line: str) -> str:
    """Build the .hero-summary div from the §1 first paragraph.

    `period_line` is treated as HTML-safe (the caller passes "LTM invoiced
    &middot; through Jun 29, 2026" with the entity intact). We do NOT re-escape.
    """
    # Pull the lead bold (everything between the first `**...**` pair)
    lead_match = re.search(r"\*\*(.+?)\*\*", first_para)
    headline_md = lead_match.group(1) if lead_match else first_para.split(".")[0]
    # Pull a $ amount and a delta from the headline
    dollar_match = _DOLLAR.search(headline_md)
    delta_match = _DELTA.search(headline_md)
    headline_dollar = dollar_match.group(0) if dollar_match else ""
    headline_delta = delta_match.group(1) if delta_match else ""
    delta_class = _classify_delta(headline_delta)

    # The rest of the first paragraph (after the lead bold) is the hero sub
    if lead_match:
        rest = first_para[lead_match.end():].lstrip(" .,—-:")
    else:
        rest = first_para
    hero_sub_html = md_inline_to_html(rest.strip()) if rest.strip() else ""

    eyebrow = period_line if period_line else "LTM invoiced"

    if headline_dollar:
        return (
            '\n    <div class="hero-summary">\n'
            f'      <div class="hero-eyebrow">{eyebrow}</div>\n'
            f'      <div class="hero-num">{_esc(headline_dollar)}</div>\n'
            f'      {f"<div class=\"hero-delta {delta_class}\">{_esc(headline_delta)}</div>" if headline_delta else ""}\n'
            f'      <div class="hero-sub">{hero_sub_html}</div>\n'
            '    </div>\n'
        )
    # Headline-less variant: just render the whole para as the hero-sub
    return (
        '\n    <div class="hero-summary">\n'
        f'      <div class="hero-eyebrow">{eyebrow}</div>\n'
        f'      <div class="hero-sub">{md_inline_to_html(first_para)}</div>\n'
        '    </div>\n'
    )


def _attach_hero_sub(hero_html: str, sub_md: str) -> str:
    """Append a `.hero-sub` paragraph to the hero block (for cohort MDs where
    the topline para is short and the substance lives in the next para)."""
    sub_html = md_inline_to_html(sub_md)
    return hero_html.replace(
        '</div>\n    </div>\n',
        f'</div>\n      <div class="hero-sub" style="margin-top: 10px;">{sub_html}</div>\n    </div>\n',
        1,
    )


def _build_metric_cards_from_table(rows: list[list[str]]) -> str:
    """Convert a 2-column metric table into a `.metrics` grid of `.metric`
    cards. The Sarreid pattern is exactly 4 cards; we render however many rows
    the MD carries (the §5a.6 invariant guards the count at the source)."""
    # rows[0] is the (empty) header
    body_rows = rows[1:] if len(rows) > 1 and not any(h.strip() for h in rows[0]) else rows
    parts: list[str] = ['\n    <div class="metrics">\n']
    for row in body_rows:
        if len(row) < 2:
            continue
        label, value_text = row[0], row[1]
        # Heuristic split: the value_text often contains a bolded value plus an
        # extended note (e.g. "**+29%** · 655 dealers · $9.72M → $12.55M").
        bold_match = re.match(r"\*\*([^*]+)\*\*\s*(.*)", value_text.strip())
        if bold_match:
            value = bold_match.group(1).strip()
            note = bold_match.group(2).strip(" ·-—")
        else:
            value = value_text.strip()
            note = ""
        note_class = _delta_note_class(value, note)
        parts.append(
            '      <div class="metric">\n'
            f'        <div class="metric-label">{md_inline_to_html(_strip_md_inline(label))}</div>\n'
            f'        <div class="metric-value">{md_inline_to_html(value)}</div>\n'
            f'        {f"<div class=\"metric-note {note_class}\">{md_inline_to_html(note)}</div>" if note else ""}\n'
            '      </div>\n'
        )
    parts.append("    </div>\n")
    return "".join(parts)


def _delta_note_class(value: str, note: str) -> str:
    """Pick ok / warn / danger for the metric-note based on tone signals."""
    combined = f"{value} {note}".lower()
    if any(t in combined for t in ["fading", "at risk", "lapsed", "below", "down"]):
        return "warn"
    if value.lstrip().startswith(("-", "−", "–")):
        return "danger"
    if value.lstrip().startswith("+") or "growth" in combined or "more spend" in combined:
        return "ok"
    return ""


def _build_ceo_callouts(list_block: str, available_ids: set[str] | None = None) -> str:
    """Convert a numbered-list block into 3 `.ceo-callout` divs.

    Expected per-item shape:
        1. **France and Son — your #3 account — is down 57% in six months and is still ordering.** That's why no one has surfaced it. The slope is unambiguous; the cause needs a phone call this week, not a quarter from now.
    """
    items = re.split(r"\n\s*\d+\.\s+", "\n" + list_block.strip())
    items = [it.strip() for it in items if it.strip()]
    if not items:
        return ""

    cards: list[str] = ['\n    <div class="ceo-callouts">\n']
    for item in items:
        # Split the lead **bold** title from the rest of the prose
        lead_match = re.match(r"\*\*(.+?)\*\*\s*(.*)", item, re.DOTALL)
        if lead_match:
            headline = lead_match.group(1).strip()
            body_md = lead_match.group(2).strip()
        else:
            headline = item.split(".")[0]
            body_md = item[len(headline):].lstrip(" .")
        full = headline + " " + body_md
        title = _shorten_callout_title(headline)
        # Extract a callout number from either the bold (e.g. "−57%") or the
        # body's first delta/dollar
        big_num = _extract_callout_num(full)
        tone_class = _pick_callout_tone(full)
        jump_href, jump_label = _callout_jump(full, tone_class, available_ids)
        jump_html = (
            f'        <a class="ceo-jump" href="#{jump_href}">{jump_label} &rarr;</a>\n'
            if jump_href else ""
        )
        cards.append(
            f'      <div class="ceo-callout {tone_class}">\n'
            f'        <div class="ceo-num">{_esc(big_num)}</div>\n'
            f'        <div class="ceo-title">{md_inline_to_html(title)}</div>\n'
            f'        <div class="ceo-body">{md_inline_to_html(body_md)}</div>\n'
            f'{jump_html}'
            f'      </div>\n'
        )
    cards.append("    </div>\n")
    return "".join(cards)


def _shorten_callout_title(headline: str) -> str:
    """CEO-callout titles are short and punchy in the north star
    ("France and Son · your #3 account"). If the authored headline is a long
    sentence, keep the crisp lead: the segment before the first ` — `/` · `
    break (when that lead is substantial), else a word-boundary trim."""
    text = headline.strip().rstrip(".")
    if len(text) <= 60:
        return text
    for sep in (" — ", " – ", " · "):
        if sep in text:
            lead = text.split(sep, 1)[0].strip()
            if 12 <= len(lead) <= 70:
                return lead
    return _truncate_clean(text, 58)


def _extract_callout_num(text: str) -> str:
    """Pull the most prominent number from a callout (a delta first, then a
    dollar, then a bare percentage)."""
    m = re.search(r"([+\-−–]?\d+(?:\.\d+)?\s*%(?:\s*YoY)?)", text)
    if m:
        return m.group(1).strip()
    m = _DOLLAR.search(text)
    if m:
        return m.group(0).strip()
    m = re.search(r"\b\d+\s+of\s+\d+\b", text)
    if m:
        return m.group(0).strip()
    m = re.search(r"\b\d{2,3}(?:\.\d+)?%\b", text)
    if m:
        return m.group(0).strip()
    return "·"


def _pick_callout_tone(text: str) -> str:
    """Map prose tone to ok / warn / danger / info CSS class.

    A real *account decline* is danger (red): an explicit negative delta, a
    "down NN%", or hard-decline language (fading, went dark, declining). A
    *structural leak* — new-dealer return rate, second-order gap, concentration
    — is warn (amber), matching the north-star coloring: those are things to
    build a play around, not a fire to put out this week."""
    low = text.lower()
    has_negative = bool(re.search(r"[\-−–]\d+(?:\.\d+)?\s*%", text))
    down_decline = bool(re.search(r"\bdown\s+\d", low)) or "declin" in low
    hard_danger = ["fading", "at risk", "went dark", "gone dark", "collaps", "fallen"]
    warn_words = [
        "aren't coming back", "not coming back", "didn't come back", "coming back",
        "second-year", "second order", "reorder", "return rate", "leak",
        "concentrated", "concentration", "one-time", "churn",
    ]
    if any(t in low for t in warn_words) and not (down_decline or has_negative):
        return "warn"
    if has_negative or down_decline or any(t in low for t in hard_danger):
        return "danger"
    if any(t in low for t in ["growing", "grew", "up ", "doubled", "breakout"]):
        return "info"
    return "info"


def _callout_jump(
    text: str, tone: str, available_ids: set[str] | None = None
) -> tuple[str, str]:
    """Pick the (anchor, label) for a CEO-callout jump link — the north star
    routes each callout to where the reader acts on it.

    Every candidate whose section did not render is skipped, and if none
    survives the callout ships without a link rather than with a dead one.
    """
    low = text.lower()
    candidates: list[tuple[str, str]] = []
    if any(t in low for t in ["pattern", "cluster", "territory", "rep ", "coverage review"]):
        candidates.append(("team", "See the pattern"))
    if any(t in low for t in ["coming back", "second-year", "second order", "reorder", "return rate", "one-time"]):
        candidates.append(("thismonth", "Build the push"))
    if any(t in low for t in ["concentration", "concentrated", "% of ltm", "top customer", "top account"]):
        candidates.append(("risk", "See the exposure"))
    if tone == "danger":
        candidates.append(("thisweek", "Call this week"))
    if tone == "warn":
        candidates.append(("thismonth", "Work the play"))
    if not candidates:
        return "", ""
    if available_ids is None:
        return candidates[0]
    for anchor, label in candidates:
        if anchor in available_ids:
            return anchor, label
    return "", ""


def _build_priorities(list_block: str) -> str:
    """Convert a bullet list into `.priority` rows.

    Expected per-item shape:
        - **This week:** 7 named calls on $1.45M+ in play — France and Son · OP Jenkins …
    """
    items = re.findall(r"^\s*[-*]\s+(.+?)(?=\n\s*[-*]\s+|\Z)", list_block, re.DOTALL | re.M)
    if not items:
        return ""
    parts: list[str] = ['\n    <div class="priorities">\n']
    for item in items:
        item = item.strip()
        # Pull the leading **Cadence:** badge
        badge_match = re.match(r"\*\*\s*(this\s+week|this\s+month|this\s+quarter|next\s+quarter)\s*[:*]+\*\*\s*(.*)", item, re.I | re.DOTALL)
        if badge_match:
            cadence = badge_match.group(1).strip().title()
            rest = badge_match.group(2).strip()
        else:
            cadence = "Action"
            rest = item
        badge_cls = (
            "high" if "week" in cadence.lower()
            else ("medium" if "month" in cadence.lower() else "low")
        )
        # Split the rest into a "title" (the first sentence-ish) and a "desc"
        # plus an "impact" dollar at the end. The Sarreid pattern has the
        # impact rendered as a separate column; cohort MDs often put it inline.
        title_md, desc_md, impact_md = _split_priority_text(rest)
        parts.append(
            '      <div class="priority">\n'
            f'        <span class="priority-badge {badge_cls}">{_esc(cadence)}</span>\n'
            '        <div>\n'
            f'          <div class="priority-title">{md_inline_to_html(title_md)}</div>\n'
            f'          {f"<div class=\"priority-desc\">{md_inline_to_html(desc_md)}</div>" if desc_md else ""}\n'
            '        </div>\n'
            f'        {f"<div class=\"priority-impact\">{md_inline_to_html(impact_md)}</div>" if impact_md else ""}\n'
            '      </div>\n'
        )
    parts.append("    </div>\n")
    return "".join(parts)


def _split_priority_text(text: str) -> tuple[str, str, str]:
    """Split a priority row body into (title, description, impact-dollar).

    Strategy (in priority order):
      1. Pull the trailing **bold dollar** as the impact, if present.
      2. Try em-dash split — accept only if BOTH halves are substantial
         (>= 20 chars) so we don't strand "3 plays" as the title.
      3. Try first-sentence split (period followed by space) for cohort
         MDs that use `Action sentence. Detail sentence.` shape.
      4. Fall back to title-only.
    """
    text = text.strip()
    impact = ""
    impact_match = re.search(r"\*\*([^*]+?)\*\*\.?\s*$", text)
    if impact_match and any(
        sym in impact_match.group(1) for sym in ("$", "%", "K", "M")
    ):
        impact = impact_match.group(1).strip(" .")
        text = text[: impact_match.start()].rstrip(" .—-")

    # Attempt 1: em-dash split, both halves >= 20 chars
    dash_parts = re.split(r"\s+[—–-]\s+", text, maxsplit=1)
    if len(dash_parts) == 2 and len(dash_parts[0].strip()) >= 20 and len(dash_parts[1].strip()) >= 20:
        return dash_parts[0].strip(), dash_parts[1].strip(), impact

    # Attempt 2: first-sentence split (period + space, but only outside `$X.YM`-style decimals)
    # Look for a period followed by whitespace that is NOT preceded by a digit.
    sentence_match = re.search(r"(?<!\d)\.\s+", text)
    if sentence_match:
        title = text[: sentence_match.start() + 1].strip()
        desc = text[sentence_match.end():].strip()
        if len(title) >= 20 and len(desc) >= 10:
            return title, desc, impact

    # Attempt 3: em-dash split even if short title
    if len(dash_parts) == 2:
        return dash_parts[0].strip(), dash_parts[1].strip(), impact

    return text.strip(), "", impact


# ─── §2 — Do this week ──────────────────────────────────────────────────────

def render_thisweek(chunk: Chunk) -> str:
    """The 7-row call list + the don't-conflate callout + nested 'how chosen'."""
    body_html, contents_blurb, sub_blurb = _render_table_section_smart(
        chunk,
        callout_keywords={
            "two different conversations": "alert",
            "don't conflate": "alert",
            "do not conflate": "alert",
        },
        nested_keywords={
            "how these were chosen": "How these were chosen",
            "selection logic": "How these were chosen",
        },
        contents_blurb="Call list · talking points · declines vs beat-skips",
    )
    title_html = _enrich_title(chunk.heading, accent_class="var(--danger)")
    return _wrap_collapse_section(
        section_id="thisweek",
        title=title_html,
        body=body_html,
        variant="urgent",
        is_open=True,
        contents_blurb=contents_blurb or "Call list · talking points · declines vs beat-skips",
        sub_blurb=sub_blurb or _default_sub_blurb(chunk.body_md),
        expand_hint="Click to expand the call list",
    )


def _enrich_title(heading: str, accent_class: str = "") -> str:
    """The Sarreid title pattern: 'Do this week · 7 calls, $1.45M+ in play' —
    where the suffix after the ` · ` is colored. We split on ` — ` first
    (cohort variants use the em-dash) then fall back to ` · `."""
    text = heading.strip()
    # Split on " — " or " · " (the Sarreid pattern is ` · ` after the noun)
    for sep in (" — ", " – ", " · ", " - "):
        if sep in text:
            prefix, suffix = text.split(sep, 1)
            if accent_class:
                return f"{md_inline_to_html(prefix)} &middot; <span style=\"color: {accent_class};\">{md_inline_to_html(suffix)}</span>"
            return f"{md_inline_to_html(prefix)} &middot; {md_inline_to_html(suffix)}"
    return md_inline_to_html(text)


_BOLD_LEAD = re.compile(r"^\s*\*\*[^*]+:\*\*\s*$")


def _default_sub_blurb(md: str) -> str:
    """Pull the first non-table, non-heading paragraph as the section-summary
    sub-blurb. Heading lines (`###`, `####`), inline subsection lead-ins
    (`**eCat as a channel:**`), and blockquotes are skipped so the blurb
    doesn't leak a subsection marker into the section card header."""
    for block in _split_paragraphs(md):
        if (
            _is_table(block)
            or _is_numbered_list(block)
            or _is_bullet_list(block)
            or block.startswith(">")
            or block.startswith("#")
            or _BOLD_LEAD.match(block)
        ):
            continue
        # Keep to roughly one sentence (or two) for the sub-blurb
        first_sentence = re.split(r"(?<=\.)\s+", block, maxsplit=1)[0]
        return md_inline_to_html(_truncate_clean(first_sentence, 240))
    return ""


def _truncate_clean(text: str, max_chars: int) -> str:
    """Truncate to max_chars on a word boundary (no mid-word chops)."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return cut + "…"


def _render_table_section_smart(
    chunk: Chunk,
    callout_keywords: dict[str, str] | None = None,
    nested_keywords: dict[str, str] | None = None,
    contents_blurb: str = "",
) -> tuple[str, str, str]:
    """Walk a chunk's blocks and emit HTML, tinting tables / callouts / nested
    details by keyword match. Returns (body_html, contents_blurb, sub_blurb)."""
    callout_keywords = {k.lower(): v for k, v in (callout_keywords or {}).items()}
    nested_keywords = {k.lower(): v for k, v in (nested_keywords or {}).items()}
    blocks = _split_paragraphs(chunk.body_md)
    out: list[str] = []
    sub_blurb = ""
    sub_blurb_pulled = False

    i = 0
    while i < len(blocks):
        block = blocks[i]
        low = block.lower()

        if _is_table(block):
            rows = _parse_md_table(block)
            if rows:
                out.append(_render_table_with_classes(rows, row_class_fn=_call_list_row_class))
                i += 1
                continue

        # Nested-details collapsibles fire on a paragraph containing "How
        # these were chosen" (which is usually italicized as a section break in
        # the source MD). The CONTENT for the nested details is the next prose
        # block.
        nested_match = None
        for kw, label in nested_keywords.items():
            if kw in low:
                nested_match = label
                break
        if nested_match:
            j = i + 1
            nested_body_md_parts = []
            while j < len(blocks) and not _is_table(blocks[j]) and not blocks[j].startswith(">"):
                nested_body_md_parts.append(blocks[j])
                j += 1
            nested_body_md = "\n\n".join(nested_body_md_parts)
            out.append(_build_nested_details(nested_match, nested_body_md))
            i = j
            continue

        # Callouts fire on any matching keyword
        callout_class = None
        for kw, cls in callout_keywords.items():
            if kw in low:
                callout_class = cls
                break
        if callout_class:
            out.append(_build_callout(block, callout_class))
            i += 1
            continue

        # Blockquote (un-tagged) -> render as insight callout (Sarreid uses
        # this in §3 Play 03 and §6 discount-discipline)
        if block.startswith(">"):
            out.append(_build_callout(block, "insight"))
            i += 1
            continue

        # Default: render as prose. The first prose block doubles as the
        # section-sub (rendered in the collapsed <summary>). To avoid a
        # verbatim 12-word echo between summary header and body (Step-10 [9]),
        # we lift the first sentence into the sub-blurb and render only the
        # residual sentences as body prose. If the para is a single sentence,
        # we drop it from the body entirely.
        if not sub_blurb_pulled and not _is_table(block):
            split = re.split(r"(?<=\.)\s+", block, maxsplit=1)
            first_sentence = split[0]
            residual = split[1] if len(split) > 1 else ""
            sub_blurb = md_inline_to_html(_strip_md_inline(first_sentence)[:240])
            sub_blurb_pulled = True
            if residual.strip():
                out.append(_wrap_prose(md_to_html(residual)))
            i += 1
            continue
        out.append(_wrap_prose(md_to_html(block)))
        i += 1

    return "\n".join(out), contents_blurb, sub_blurb


def _call_list_row_class(cells: list[str], idx: int) -> Optional[str]:
    """Tint call-list rows by slope tag in the stakes column.

    - `(beat-skip` or positive delta on a flagged row → row-highlight (green)
    - "pattern" / "cluster" override forces row-warn (calmer; the call is the
      cluster review, not the individual account)
    - Decline ≥ 40% → row-danger
    - Decline ≥ 20% → row-warn
    - Otherwise no tint
    """
    blob = " ".join(cells).lower()
    if "beat-skip" in blob or "growing" in blob or re.search(r"\+\s?\d{2,}", blob):
        return "row-highlight"
    decline_match = re.search(r"[\-−–]\s?(\d{1,3})(?:\.\d+)?\s?%", blob)
    if decline_match:
        if "pattern" in blob or "cluster" in blob:
            return "row-warn"
        pct = int(decline_match.group(1))
        if pct >= 40:
            return "row-danger"
        if pct >= 20:
            return "row-warn"
    return None


def _build_callout(block: str, css_class: str) -> str:
    """Emit a `.callout.{css_class}` block from a MD paragraph. If the para
    starts with a `**Title.**` bold sentence, we lift it as the callout-title."""
    if block.startswith(">"):
        # Blockquote — strip the leading `> ` markers
        inner = "\n".join(re.sub(r"^>\s?", "", ln) for ln in block.splitlines())
    else:
        inner = block
    title_match = re.match(r"\*\*([^*]+?)\.?\*\*\s*(.*)", inner, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip(" .")
        body = title_match.group(2).strip()
    else:
        title = ""
        body = inner
    title_html = (
        f'<div class="callout-title">{md_inline_to_html(title)}</div>'
        if title else ""
    )
    body_html = md_inline_to_html(body) if body else ""
    return (
        f'\n    <div class="callout {css_class}">\n'
        f'      {title_html}\n'
        f'      {body_html}\n'
        '    </div>\n'
    )


def _build_nested_details(label: str, body_md: str) -> str:
    """A `<details class="nested">` (in-section disclosure) collapsible."""
    body_html = _wrap_prose(md_to_html(body_md)) if body_md else ""
    return (
        '\n      <details class="nested">\n'
        f'        <summary>{_esc(label)} &middot; selection logic</summary>\n'
        f'        <div class="nested-body">{body_html}</div>\n'
        '      </details>\n'
    )


# ─── §3 — Do this month (play cards) ────────────────────────────────────────

_H3_PATTERN = re.compile(r"(?m)^###\s+(.+?)\s*$")


def render_thismonth(chunk: Chunk) -> str:
    """Each `### N. Title` becomes a `.play-card`. Anything before the first
    H3 is treated as the section-summary blurb."""
    text = chunk.body_md
    h3_matches = list(_H3_PATTERN.finditer(text))
    sub_blurb_md = text[: h3_matches[0].start()].strip() if h3_matches else text
    sub_blurb = ""
    if sub_blurb_md:
        first_para = _split_paragraphs(sub_blurb_md)[0]
        first_sentence = re.split(r"(?<=\.)\s+", first_para, maxsplit=1)[0]
        sub_blurb = md_inline_to_html(_strip_md_inline(first_sentence)[:280])

    cards: list[str] = []
    for i, m in enumerate(h3_matches):
        title = m.group(1).strip()
        start = m.end()
        end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(text)
        card_md = text[start:end].strip()
        cards.append(_build_play_card(i + 1, title, card_md))

    if not cards:
        # No H3 plays found — render the chunk as a single section block
        body = _wrap_prose(md_to_html(text))
    else:
        body = "\n".join(cards)

    title_html = _enrich_title(chunk.heading, accent_class="var(--warn)")
    return _wrap_collapse_section(
        section_id="thismonth",
        title=title_html,
        body=body,
        variant="month",
        contents_blurb=_collect_h3_titles(text),
        sub_blurb=sub_blurb,
        expand_hint=f"Click to expand the {len(cards)} plays" if cards else "Click to expand",
    )


def _collect_h3_titles(text: str) -> str:
    """Build the section-contents blurb from the H3 plays."""
    titles = [_strip_md_inline(m.group(1)).split(".", 1)[-1].strip(" :—-") for m in _H3_PATTERN.finditer(text)]
    # Use a word-boundary truncation; the section-contents line should read,
    # not get chopped mid-word.
    return " · ".join(_truncate_clean(t, 42) for t in titles[:4])


def _build_play_card(n: int, raw_title: str, body_md: str) -> str:
    """Render a single Play card.

    The MD body typically has prose paragraphs, sometimes a small table, sometimes
    a callout-style blockquote, and a closing `**$X upside…**` line.
    """
    # The "1. Title" prefix → keep only the part after the dot
    title = re.sub(r"^\s*\d+\.\s*", "", _strip_md_inline(raw_title)).strip()

    blocks = _split_paragraphs(body_md)
    body_parts: list[str] = []
    upside_chip = ""
    for block in blocks:
        if _is_table(block):
            rows = _parse_md_table(block)
            if rows and _looks_like_metric_table(rows):
                body_parts.append(_build_metric_cards_from_table(rows))
            elif rows:
                body_parts.append(_render_table_with_classes(rows))
            continue
        if block.startswith(">"):
            body_parts.append(_build_callout(block, "insight"))
            continue
        # Trailing bold $X-upside line (Sarreid uses `**$90K – $160K product upside &middot; ESTIMATED**`)
        if (re.match(r"^\s*\*\*[^*]*\$[^*]*\*\*\s*\.?\s*$", block)
                or re.match(r"^\s*\*\*[^*]*upside[^*]*\*\*\s*\.?\s*$", block, re.I)
                or re.match(r"^\s*\*\*[^*]*directional[^*]*\*\*\s*\.?\s*$", block, re.I)
                or re.match(r"^\s*\*\*\+\$[^*]*\*\*\s*\.?\s*$", block)):
            upside_text = _strip_md_inline(block).strip(" .")
            upside_chip = f'      <div class="play-upside">{_esc(upside_text)}</div>\n'
            continue
        # Standard "play-sub" prose
        rendered_html = md_inline_to_html(block)
        body_parts.append(f'      <p class="play-sub">{rendered_html}</p>\n')

    return (
        '\n      <div class="play-card">\n'
        f'        <span class="play-card-num">Play {n:02d}</span>\n'
        f'        <h4>{md_inline_to_html(title)}</h4>\n'
        f'{"".join(body_parts)}'
        f'{upside_chip}'
        '      </div>\n'
    )


# ─── §5 — Growth engine (subsections) ───────────────────────────────────────

def render_growth(chunk: Chunk) -> str:
    body, contents = _render_subsection_section(chunk, var="growth")
    return _wrap_collapse_section(
        section_id="growth",
        title=_enrich_title(chunk.heading),
        body=body,
        contents_blurb=contents,
        sub_blurb=_default_sub_blurb(chunk.body_md),
        expand_hint="Click to expand the layers",
    )


def _render_subsection_section(chunk: Chunk, var: str) -> tuple[str, str]:
    """Walk H3-delimited subsections, wrapping each in `.subsection`. If there
    are no H3 boundaries (cohort variants of §10 Channels and §9 Dealer base
    often live as a flat sequence of tables + prose), we additionally split on
    `**Bold lead-in:**` paragraphs as soft subsection boundaries so the body
    still gets the metric/table rendering it deserves (without raw
    markdown-it table emission)."""
    text = chunk.body_md
    h3_matches = list(_H3_PATTERN.finditer(text))
    if not h3_matches:
        # No H3 — check for bold-colon soft subsection boundaries
        # (e.g. `**eCat as a channel:**` in §10 Channels).
        # These are standalone paragraphs that consist entirely of `**Title:**`.
        all_blocks = _split_paragraphs(text)
        soft_boundaries: list[tuple[int, re.Match]] = [
            (i, _BOLD_SECTION_LEAD.match(b))  # type: ignore[arg-type]
            for i, b in enumerate(all_blocks)
            if _BOLD_SECTION_LEAD.match(b)
        ]
        if soft_boundaries:
            parts_soft: list[str] = []
            titles_soft: list[str] = []
            prev_end = 0
            for j, (bound_idx, m) in enumerate(soft_boundaries):
                # Render blocks before this boundary as flat (no subsection title)
                if bound_idx > prev_end:
                    intro_text = "\n\n".join(all_blocks[prev_end:bound_idx])
                    parts_soft.append(_render_freeform_blocks(intro_text))
                # Determine content extent for this subsection
                next_bound = soft_boundaries[j + 1][0] if j + 1 < len(soft_boundaries) else len(all_blocks)
                sub_text = "\n\n".join(all_blocks[bound_idx + 1:next_bound])
                title_text = _strip_md_inline(m.group(1)).strip()  # type: ignore[union-attr]
                titles_soft.append(title_text)
                style_attr = ' style="margin-top: 0;"' if not parts_soft and not titles_soft[:-1] else ""
                parts_soft.append(
                    f'\n      <div class="subsection"{style_attr}>\n'
                    f'        <h3 class="subsection-title">{md_inline_to_html(title_text)}</h3>\n'
                    f'{_render_freeform_blocks(sub_text)}\n'
                    '      </div>\n'
                )
                prev_end = next_bound
            if prev_end < len(all_blocks):
                parts_soft.append(_render_freeform_blocks("\n\n".join(all_blocks[prev_end:])))
            contents_soft = " · ".join(_truncate_clean(t, 40) for t in titles_soft[:5])
            return "\n".join(parts_soft), contents_soft
        # No soft boundaries either — render flat.
        return _render_freeform_blocks(text), ""

    parts: list[str] = []
    titles: list[str] = []
    intro_md = text[: h3_matches[0].start()].strip()
    if intro_md:
        parts.append(_render_freeform_blocks(intro_md))

    for i, m in enumerate(h3_matches):
        title = _strip_md_inline(m.group(1)).strip()
        titles.append(title.split("—", 1)[-1].strip(" -·"))
        start = m.end()
        end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(text)
        sub_md = text[start:end].strip()
        sub_html = _render_freeform_blocks(sub_md)
        style_attr = ' style="margin-top: 0;"' if i == 0 else ""
        parts.append(
            f'\n      <div class="subsection"{style_attr}>\n'
            f'        <h3 class="subsection-title">{_enrich_title(title)}</h3>\n'
            f'{sub_html}\n'
            '      </div>\n'
        )
    contents = " · ".join(_truncate_clean(t, 40) for t in titles[:5])
    return "\n".join(parts), contents


def _render_freeform_blocks(md: str) -> str:
    """Generic block-walker for subsections (used by §5, §8, §9, §10).

    Tables, blockquotes (→ callout.insight), bullet lists, and plain prose.
    """
    out: list[str] = []
    for block in _split_paragraphs(md):
        if _is_table(block):
            rows = _parse_md_table(block)
            if not rows:
                out.append(_wrap_prose(md_to_html(block)))
                continue
            # 2-column unlabeled tables → metric cards; otherwise standard table
            if _looks_like_metric_table(rows):
                out.append(_build_metric_cards_from_table(rows))
            else:
                out.append(_render_table_with_classes(rows, row_class_fn=_generic_row_class))
            continue
        if block.startswith(">"):
            out.append(_build_callout(block, "opportunity" if "opportunity" in block.lower() else "insight"))
            continue
        out.append(_wrap_prose(md_to_html(block)))
    return "\n".join(out)


def _generic_row_class(cells: list[str], idx: int) -> Optional[str]:
    """Tint a row green when it's a 'highlight' (bolded label) row."""
    if any("**" in c and c.startswith("**") for c in cells[:1]):
        # First column is bold — heuristic: highlight
        if any("$" in c for c in cells) and idx == 0:
            return "row-highlight"
    return None


# ─── §6 — Team (leaderboard + coaching cards + discount note) ───────────────

_COACHING_CARD_HEADER = re.compile(
    r"^\s*\*\*\s*Card\s+(\d+)\s*[—–-]\s*([^*·]+?)(?:\s*·\s*([^*]+))?\s*\*\*\s*",
    re.I,
)


def render_team(chunk: Chunk) -> str:
    """Top-N leaderboard table + 5 coaching cards + discount-discipline note."""
    text = chunk.body_md
    h3_matches = list(_H3_PATTERN.finditer(text))

    parts: list[str] = []
    contents_titles: list[str] = []

    # Walk H3 subsections
    if h3_matches:
        intro_md = text[: h3_matches[0].start()].strip()
        if intro_md:
            parts.append(_wrap_prose(md_to_html(intro_md)))
        for i, m in enumerate(h3_matches):
            title = _strip_md_inline(m.group(1)).strip()
            contents_titles.append(title.split("—", 1)[0].strip())
            start = m.end()
            end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(text)
            sub_md = text[start:end].strip()
            sub_html = _render_team_subsection(sub_md)
            style_attr = ' style="margin-top: 0;"' if i == 0 else ""
            parts.append(
                f'\n      <div class="subsection"{style_attr}>\n'
                f'        <h3 class="subsection-title">{_enrich_title(title)}</h3>\n'
                f'{sub_html}\n'
                '      </div>\n'
            )
    else:
        parts.append(_render_team_subsection(text))

    return _wrap_collapse_section(
        section_id="team",
        title=_enrich_title(chunk.heading),
        body="\n".join(parts),
        contents_blurb=" · ".join(_truncate_clean(t, 40) for t in contents_titles[:3]),
        sub_blurb=_default_sub_blurb(chunk.body_md),
        expand_hint="Click to expand",
    )


def _render_team_subsection(md: str) -> str:
    """Walk a team subsection's blocks: convert blockquotes-with-Card-N headers
    into `.coaching-card` divs; tables → leaderboard; trailing prose → discount
    discipline note (rendered as `.callout.insight`)."""
    out: list[str] = []
    # First, peel off coaching-card blockquotes: each is a contiguous run of
    # `> ...` lines that starts with `> **Card N — …`. We split the chunk into
    # quote-blocks vs everything else.
    segments = _split_quotes_vs_prose(md)
    for kind, block in segments:
        if kind == "quote":
            card_html = _try_render_coaching_card(block)
            if card_html:
                out.append(card_html)
            else:
                # Generic blockquote -> insight callout
                out.append(_build_callout(block, "insight"))
        else:
            for sub in _split_paragraphs(block):
                if _is_table(sub):
                    rows = _parse_md_table(sub)
                    if rows:
                        out.append(_render_table_with_classes(rows, row_class_fn=_team_row_class))
                    else:
                        out.append(_wrap_prose(md_to_html(sub)))
                elif sub.startswith("**A note on") or "discount discipline" in sub.lower()[:60]:
                    out.append(_build_callout(sub, "insight"))
                else:
                    out.append(_wrap_prose(md_to_html(sub)))
    return "\n".join(out)


def _split_quotes_vs_prose(md: str) -> list[tuple[str, str]]:
    """Return [(kind, block)] where kind ∈ {'quote', 'prose'}; quote blocks are
    contiguous runs of `> ` lines (possibly with blank lines between cards)."""
    lines = md.splitlines()
    segments: list[tuple[str, str]] = []
    buf: list[str] = []
    current_kind = None

    def flush():
        nonlocal buf, current_kind
        if buf:
            segments.append((current_kind, "\n".join(buf).rstrip()))
            buf = []
            current_kind = None

    for ln in lines:
        is_quote = ln.lstrip().startswith(">")
        is_blank = not ln.strip()
        if current_kind is None:
            current_kind = "quote" if is_quote else "prose"
            buf.append(ln)
            continue
        if current_kind == "quote":
            if is_quote or is_blank:
                buf.append(ln)
            else:
                flush()
                current_kind = "prose"
                buf.append(ln)
        else:  # prose
            if is_quote:
                # If the next line transitions into a quote, flush prose
                flush()
                current_kind = "quote"
                buf.append(ln)
            else:
                buf.append(ln)
    flush()

    # Split a single 'quote' segment into multiple cards on blank separator
    expanded: list[tuple[str, str]] = []
    for kind, block in segments:
        if kind == "quote":
            # Split on blank lines between Card N headers
            sub_blocks = re.split(r"\n\s*\n", block.strip())
            for sb in sub_blocks:
                if sb.strip():
                    expanded.append(("quote", sb.strip()))
        else:
            expanded.append((kind, block))
    return expanded


def _try_render_coaching_card(quote_block: str) -> Optional[str]:
    """If the blockquote starts with `> **Card N — …**`, render as
    `.coaching-card`. Otherwise return None.
    """
    inner = "\n".join(re.sub(r"^>\s?", "", ln) for ln in quote_block.splitlines()).strip()
    header_match = _COACHING_CARD_HEADER.match(inner)
    if not header_match:
        return None
    card_n = header_match.group(1)
    rep_name = header_match.group(2).strip()
    badge_text = (header_match.group(3) or "").strip()
    rest = inner[header_match.end():].strip()

    # The first sentence after the header is the coaching-stats line; everything
    # else is the body. Heuristic: if `rest` starts with a sentence ending in
    # something measurable (rate, threshold, etc.) we lift it as stats.
    stats_md, body_md = _split_card_stats_and_body(rest)

    # Pick a tone class
    tone_cls = _pick_card_tone(badge_text + " " + rest)
    badge_cls = _pick_card_badge_class(badge_text)

    badge_html = (
        f'<span class="badge {badge_cls}">{md_inline_to_html(badge_text)}</span>'
        if badge_text else ""
    )

    name_html = md_inline_to_html(rep_name)

    return (
        f'\n        <div class="coaching-card {tone_cls}">\n'
        '          <div class="coaching-header">\n'
        f'            <div class="coaching-name">Card {card_n} &middot; {name_html}</div>\n'
        f'            {badge_html}\n'
        '          </div>\n'
        f'          {f"<div class=\"coaching-stats\">{md_inline_to_html(stats_md)}</div>" if stats_md else ""}\n'
        f'          <div class="coaching-body">{md_inline_to_html(body_md)}</div>\n'
        '        </div>\n'
    )


def _split_card_stats_and_body(text: str) -> tuple[str, str]:
    """Pull the first sentence/clause as 'stats' ONLY if it looks like a real
    stats line — i.e. starts with `**$XK at risk**` or `**rate $Y%**` and is
    short (< 120 chars). Otherwise the entire text is the body. The cohort MDs
    rarely carry a separate stats sentence; conflating the first sentence as
    stats fires a stats div that reads like a headline."""
    text = text.strip()
    # Strict shape: leading **bold metric** (with $, K, M, or %) + optional
    # clauses delimited by · or — , ending at the FIRST sentence boundary.
    strict = re.match(
        r"((?:\*\*[^*]+[\$%KM][^*]*\*\*[^.\n]*?){1,3})\.\s+(.+)",
        text,
        re.DOTALL,
    )
    if strict and len(strict.group(1)) < 160:
        return strict.group(1).strip(" .—"), strict.group(2).strip()
    # Otherwise — body only, no stats line
    return "", text


def _pick_card_tone(text: str) -> str:
    low = text.lower()
    if "all the dollars" in low or "1 account" in low or "alarm" in low or "only top-10 book" in low:
        return "alarm"
    if "growing" in low or "both accounts growing" in low or "growing book" in low:
        return "growing"
    if "pattern" in low or "7-account" in low or "cluster" in low:
        return "pattern"
    return ""


def _pick_card_badge_class(badge_text: str) -> str:
    low = badge_text.lower()
    # Danger: single-account-at-risk, alarm-shaped declines, only-top-10-shrank
    if (
        re.search(r"\b1\s+account\b", low)
        or re.search(r"\bon\s+1\s+\w+\b", low)
        or "all the dollars" in low
        or "alarm" in low
        or "only top" in low
        or "danger" in low
    ):
        return "danger"
    # Growing / positive cluster
    if "growing" in low or ("both" in low and ("account" in low or "growing" in low)):
        return "ok"
    # Pattern / multi-account flagged at risk → info
    if "pattern" in low or "at risk" in low or "across" in low or "account" in low:
        return "info"
    return "muted"


def _team_row_class(cells: list[str], idx: int) -> Optional[str]:
    """Tint declining-rep rows warn/danger; growers stay neutral."""
    blob = " ".join(cells).lower()
    # YoY delta is usually in column 3 or 4
    if re.search(r"[\-−–]\s?(\d{1,2})(\.\d+)?\s?%", blob):
        m = re.search(r"[\-−–]\s?(\d{1,2})(\.\d+)?\s?%", blob)
        if m:
            pct = float(m.group(1))
            if pct >= 15:
                return "row-warn"
    return None


# ─── §7 — Risk watchlist (single big table) ─────────────────────────────────

def render_risk(chunk: Chunk) -> str:
    body = _render_freeform_blocks_with_row_class(chunk.body_md, _call_list_row_class)
    return _wrap_collapse_section(
        section_id="risk",
        title=_enrich_title(chunk.heading),
        body=body,
        contents_blurb="tail of the watchlist",
        sub_blurb=_default_sub_blurb(chunk.body_md),
        expand_hint="Click to expand the tail",
    )


def _render_freeform_blocks_with_row_class(md: str, row_class_fn) -> str:
    out: list[str] = []
    for block in _split_paragraphs(md):
        if _is_table(block):
            rows = _parse_md_table(block)
            if rows:
                out.append(_render_table_with_classes(rows, row_class_fn=row_class_fn))
                continue
        if block.startswith(">"):
            out.append(_build_callout(block, "insight"))
            continue
        out.append(_wrap_prose(md_to_html(block)))
    return "\n".join(out)


# ─── §8 — Product intelligence ──────────────────────────────────────────────

def render_products(chunk: Chunk) -> str:
    body, contents = _render_subsection_section(chunk, var="")
    if not contents:
        contents = "Top items · the cross-sell"
    return _wrap_collapse_section(
        section_id="products",
        title=_enrich_title(chunk.heading),
        body=body,
        contents_blurb=contents,
        sub_blurb=_default_sub_blurb(chunk.body_md),
    )


# ─── §9 — Dealer base ───────────────────────────────────────────────────────

def render_base(chunk: Chunk) -> str:
    body = _render_freeform_blocks(chunk.body_md)
    return _wrap_collapse_section(
        section_id="base",
        title=_enrich_title(chunk.heading),
        body=body,
        contents_blurb="In · out · returning · buyer cadence",
        sub_blurb=_default_sub_blurb(chunk.body_md),
    )


# ─── §10 — Channels ─────────────────────────────────────────────────────────

def render_channels(chunk: Chunk) -> str:
    body, contents = _render_subsection_section(chunk, var="")
    if not contents:
        contents = "Channel mix · eCat as a channel"
    return _wrap_collapse_section(
        section_id="channels",
        title=_enrich_title(chunk.heading),
        body=body,
        contents_blurb=contents,
        sub_blurb=_default_sub_blurb(chunk.body_md),
    )


# ─── §11 — Methodology (gaps + trust) ───────────────────────────────────────

def render_methodology(gaps_chunk: Optional[Chunk], trust_chunk: Optional[Chunk]) -> str:
    """Combine "What this report can't see" + "How to trust these numbers"
    into one `<details id="methodology">` collapsible (Sarreid pattern) or
    two sequential subsections (cohort pattern). Either is gold per §5a.1."""
    parts: list[str] = []
    contents_blurbs: list[str] = []

    if gaps_chunk:
        # Use only the prefix before " — " so the h3 reads cleanly
        # (e.g. "What this report can't see" not "What this report can't see — and what to add next")
        gaps_h3 = md_inline_to_html(_split_heading_prefix(gaps_chunk.heading))
        parts.append(
            '\n      <div class="subsection" style="margin-top: 0;">\n'
            f'        <h3 class="subsection-title">{gaps_h3}</h3>\n'
            f'{_render_methodology_body(gaps_chunk.body_md)}\n'
            '      </div>\n'
        )
        contents_blurbs.append("Data gaps · upgrades to queue")
    if trust_chunk:
        trust_h3 = md_inline_to_html(_split_heading_prefix(trust_chunk.heading))
        parts.append(
            '\n      <div class="subsection">\n'
            f'        <h3 class="subsection-title">{trust_h3}</h3>\n'
            f'{_render_methodology_body(trust_chunk.body_md)}\n'
            '      </div>\n'
        )
        contents_blurbs.append("Methodology")

    if not parts:
        return ""

    sub_blurb = (
        "The honest disclosure block. What the single-feed view can't see, "
        "the upgrades worth queuing, and the methodology stamp the topline rides on."
    )
    title = "What this report can&rsquo;t see &middot; how to trust the numbers"
    return _wrap_collapse_section(
        section_id="methodology",
        title=title,
        body="\n".join(parts),
        variant="quarter",
        contents_blurb=" · ".join(contents_blurbs),
        sub_blurb=sub_blurb,
    )


def _render_methodology_body(md: str) -> str:
    """The methodology bodies are typically: 1 intro paragraph, 1 bullet list
    (the 6-item honest list), 0–2 callout-style "upgrade" blocks, 1–2 trailing
    prose paragraphs. We honor that shape."""
    out: list[str] = []
    for block in _split_paragraphs(md):
        if _is_table(block):
            rows = _parse_md_table(block)
            if rows:
                out.append(_render_table_with_classes(rows))
                continue
        if block.startswith(">"):
            out.append(_build_callout(block, "note"))
            continue
        # Standalone bold-colon paragraph → inline h3 subsection-title
        # (e.g. "**Two specific upgrades worth queuing:**")
        bold_colon_match = _BOLD_SECTION_LEAD.match(block)
        if bold_colon_match:
            title_text = _strip_md_inline(bold_colon_match.group(1)).strip()
            out.append(f'        <h3 class="subsection-title">{md_inline_to_html(title_text)}</h3>\n')
            continue
        # An "upgrade-style" paragraph leads with `**Bold title.**` (e.g.
        # "**A cost feed (any channel).**")
        upgrade_match = re.match(r"\*\*([^*]+?\.)\*\*\s*(.*)", block, re.DOTALL)
        if upgrade_match and len(upgrade_match.group(1)) < 100:
            out.append(_build_callout(block, "note"))
            continue
        out.append(_wrap_prose(md_to_html(block)))
    return "\n".join(out)



# ─── Mode-2 Gate-STOP variant ───────────────────────────────────────────────

def render_gatestop(report: ParsedReport) -> tuple[str, str]:
    """Render a Mode-2 Gate-STOP MD as (summary_block_html, body_html).

    The summary block carries the gate-STOP banner + the Bottom-line gate table;
    the body assembles the preflights, user-grain concentration, patch notes
    (collapsed), recommended next action, and appendix.
    """
    # Preamble (the `> Profile state` / "**This is a PASS3 output**" callouts)
    # gets rendered as the summary lead-in.
    summary_lead_html = ""
    if report.preamble_md:
        # The preamble is multiple blockquote/`>` paragraphs in sca's MD.
        summary_lead_html = _wrap_prose(md_to_html(report.preamble_md))

    # Walk each gatestop chunk and emit the appropriate body
    summary_extra: list[str] = []
    body_parts: list[str] = []

    for chunk in report.chunks:
        sid = chunk.section_id
        if sid == "summary":
            # The "Bottom line" gate table + Conclusion goes in the summary
            summary_extra.append(
                f'\n    <div class="subsection" style="margin-top: 20px;">\n'
                f'      <h3 class="subsection-title">{md_inline_to_html(chunk.heading)}</h3>\n'
                f'{_render_freeform_blocks(chunk.body_md)}\n'
                '    </div>\n'
            )
        elif sid == "preflights":
            body_parts.append(_wrap_collapse_section(
                section_id="preflights",
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
                contents_blurb="Q-ECON-00 · RP-2 · Q-CHAN-00 · eCat behavior",
                sub_blurb="The economics, rep-identity, and channel preflights that fired the Gate-STOP.",
                is_open=True,
            ))
        elif sid == "concentration":
            body_parts.append(_wrap_collapse_section(
                section_id="concentration",
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
                variant="quarter",
                contents_blurb="One-user concentration finding (Mode-2 only, §5b.3)",
                sub_blurb="Per the patched operator §5b.3 user-grain rule: structural concentration when one org_user_id exceeds 80% of LTM eCat capture.",
                is_open=True,
            ))
        elif sid == "patchnotes":
            body_parts.append(_wrap_collapse_section(
                section_id="patchnotes",
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
                contents_blurb="PASS1 → PASS3 register, closed-state check",
                sub_blurb="Per-defect close-out from the 2026-06-30 cohort patch + gold-stamp absorption.",
            ))
        elif sid == "nextaction":
            body_parts.append(_wrap_collapse_section(
                section_id="nextaction",
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
                variant="month",
                contents_blurb="Recommendation only — no canon change",
                sub_blurb="What an operator can run next to either re-qualify the org or move it permanently onto the rep-copilot surface.",
                is_open=True,
            ))
        elif sid == "appendix":
            body_parts.append(_wrap_collapse_section(
                section_id="appendix",
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
                contents_blurb="Identity · live query trace · per-check ledger state",
                sub_blurb="Per-figure provenance trace + explicit Step-10 13-check ledger state.",
            ))
        else:
            body_parts.append(_wrap_collapse_section(
                section_id=sid,
                title=md_inline_to_html(chunk.heading),
                body=_render_freeform_blocks(chunk.body_md),
            ))

    summary_block_html = summary_lead_html + "\n".join(summary_extra)
    body_html = "\n".join(body_parts)
    return summary_block_html, body_html
