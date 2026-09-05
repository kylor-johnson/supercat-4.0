#!/usr/bin/env python3
"""SUPERSEDED 2026-07-09 — do not run.

This builder targets the pre-Round-2 markdown shape and still hardcodes
"Gabriella White removed" / "108 orgs". The live HTML generator is:

  Customer Segmentation/current/build_segmentation_html.py

which reads the corrected MASTER CSV + current MD and writes
current/SuperCat_Client_Segmentation_v4.0.html.
"""
raise SystemExit(
    "Superseded: use Customer Segmentation/current/build_segmentation_html.py"
)

# --- original script retained below for archaeology only ---
"""Generate SuperCat_Client_Segmentation_v4.0.html from the markdown source (STALE)."""

import re
from pathlib import Path

DIR = Path(__file__).parent
MD = DIR / "SuperCat_Client_Segmentation_v4.0.md"
OUT = DIR / "SuperCat_Client_Segmentation_v4.0.html"

SEGMENTS = {
    "1. Luxury Specification": {"slug": "luxury", "color": "#B8860B", "bg": "#FDF8EC", "border": "#E8D5A0"},
    "2. Premium Trade Brand": {"slug": "premium", "color": "#6B4FBB", "bg": "#F5F0FC", "border": "#D4C4F0"},
    "3. Mid-Market Multi-Channel": {"slug": "midmarket", "color": "#1F8A5C", "bg": "#EDF7F1", "border": "#A8DCC0"},
    "4. Volume Distribution": {"slug": "volume", "color": "#C44D4D", "bg": "#FDF0F0", "border": "#E8B4B4"},
    "5. Specialty/Non-Traditional": {"slug": "specialty", "color": "#6B7280", "bg": "#F3F4F6", "border": "#D1D5DB"},
}

FLAG_ORGS = {"cci", "hf", "rf", "sarreid", "cfg", "fsf", "ap", "mh"}

GLOSSARY = {
    "Best Price": "The single most trustworthy unit-price signal. Uses invoiced unit prices when available; otherwise catalog median after stripping $5 accessories and $50K outliers. Primary segmentation axis.",
    "IQR": "Interquartile range — middle 50% of prices across orgs in a segment (25th–75th percentile).",
    "Orders": "Total eCat orders ever submitted (all time). Rough proxy for platform usage depth.",
    "T12M": "Trailing 12 months — orders in the last year only. Shows current activity vs. historical.",
    "AOV": "Average Order Value — order dollars ÷ order count. Big AOV = project orders; small = replenishment.",
    "PCodes": "Price levels configured in eCat (e.g. Dealer, Designer, Net, Retail). More = more complex channel pricing.",
    "Customers": "Customer records loaded in eCat — from 34 (bespoke) to 92,000+ (massive dealer network).",
    "Territories": "Geographic territory assignments in eCat. Zero means not configured — not proof of no coverage.",
    "Users": "eCat user accounts (reps + portal buyers). 8K+ often means B2B buyer logins, not 8K salespeople.",
    "DCs": "Distribution centers in eCat. Most orgs show 0 — fulfillment happens outside the platform.",
    "org": "Postgres shortname — internal identifier for the client org.",
}

KEY_CALLS = [
    ("Keep v3.2 membership", "No orgs reclassified in this reset build."),
    ("Price = supporting evidence", "Cleaned best-price layer stays central; outliers scrubbed, not abandoned."),
    ("Enrichment ≠ classifier", "Customer count, territories, users, T12M orders explain scale within a segment."),
    ("fms AOV corrected", "$92,048 → $3,649 after excluding 23 corrupt duplicate orders."),
    ("shl AOV corrected", "$75,722 → $6,942 after excluding one $464M corrupt order."),
    ("Gabriella White removed", "Duplicate of Summer Classics (org sc) — already in Premium Trade Brand."),
]

SUMMARY_HEADERS = [
    "Segment", "N", "Median Best Price", "IQR", "Median Orders",
    "Median AOV", "Median PCodes", "Median Customers", "Median T12M Orders",
]

FRAMEWORK_QUESTIONS = [
    ("What do they sell?", "Product type and price point — furniture, lighting, housewares; $3/unit vs $9,100/unit."),
    ("How do they sell it?", "Specification, brand-building, multi-channel distribution, or commodity replenishment."),
    ("Who buys from them?", "Designers, showroom dealers, retail chains, category managers, hospitality specifiers."),
]


def parse_md(text: str) -> dict:
    data = {}
    # Segment summary table
    m = re.search(
        r"## Segment Summary\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)+)",
        text,
    )
    summary_rows = []
    if m:
        for line in m.group(1).strip().splitlines():
            cols = [c.strip() for c in line.strip("|").split("|")]
            summary_rows.append(cols)
    data["summary"] = summary_rows

    # Rosters
    rosters = {}
    for seg_name in SEGMENTS:
        pat = rf"### {re.escape(seg_name)} \(\d+ accounts\)\n\n([^\n]+)\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)+)"
        m = re.search(pat, text)
        if m:
            rosters[seg_name] = {
                "desc": m.group(1).strip(),
                "rows": [
                    [c.strip() for c in ln.strip("|").split("|")]
                    for ln in m.group(2).strip().splitlines()
                ],
            }
    data["rosters"] = rosters

    # Enrichment bullets
    m = re.search(r"## What The Enrichment Adds\n\n((?:- .+\n)+)", text)
    enrichment = []
    if m:
        for line in m.group(1).strip().splitlines():
            line = line.lstrip("- ").strip()
            if ":" in line:
                title, body = line.split(":", 1)
                title = title.strip().strip("*").strip()
                body = body.strip().strip("*").strip()
                enrichment.append((title, body))
            else:
                enrichment.append(("", line.strip("*").strip()))
    data["enrichment"] = enrichment

    # Review candidates
    m = re.search(
        r"## Pre-Stamp Review Candidates\n\n[^\n]+\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)+)",
        text,
    )
    review = []
    if m:
        for line in m.group(1).strip().splitlines():
            cols = [c.strip() for c in line.strip("|").split("|")]
            review.append(cols)
    data["review"] = review

    # Boundaries table
    m = re.search(
        r"\| Boundary \| What separates them \|\n\|[^\n]+\n((?:\|[^\n]+\n)+)",
        text,
    )
    boundaries = []
    if m:
        for line in m.group(1).strip().splitlines():
            cols = [c.strip() for c in line.strip("|").split("|")]
            boundaries.append(cols)
    data["boundaries"] = boundaries

    # Data layers table
    m = re.search(
        r"\| Layer \| Source \| What it tells us \|\n\|[^\n]+\n((?:\|[^\n]+\n)+)",
        text,
    )
    layers = []
    if m:
        for line in m.group(1).strip().splitlines():
            cols = [c.strip() for c in line.strip("|").split("|")]
            layers.append(cols)
    data["layers"] = layers

    # Segment profiles
    profiles = {}
    m = re.search(r"## Segment Profiles\n\n(.*?)---\n\n## Segment Summary", text, re.DOTALL)
    if m:
        body = m.group(1)
        for seg_name in SEGMENTS:
            pat = rf"### {re.escape(seg_name)} \(\d+ accounts\)\n\n(.*?)(?=\n### |\Z)"
            pm = re.search(pat, body, re.DOTALL)
            if not pm:
                continue
            block = pm.group(1)

            def field(label: str) -> str:
                fm = re.search(
                    rf"\*\*{re.escape(label)}:\*\* (.+?)(?=\n\n\*\*|\Z)",
                    block,
                    re.DOTALL,
                )
                return fm.group(1).strip() if fm else ""

            def bullets(label: str) -> list:
                raw = field(label)
                items = [ln[2:].strip() for ln in raw.splitlines() if ln.strip().startswith("- ")]
                return items if items else ([raw] if raw else [])

            profiles[seg_name] = {
                "defined_by": field("Defined by"),
                "what": field("What they sell"),
                "how": bullets("How they sell"),
                "who": bullets("Who buys"),
                "truth": field("Key commercial truth"),
            }
    data["profiles"] = profiles

    return data


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt_cell(val: str, col_idx: int, headers: list) -> str:
    v = val.strip()
    if v in ("--", "??", ""):
        return '<span class="missing">—</span>'
    if col_idx == 1 and headers[1].lower() == "org":
        return f'<code class="org-tag">{esc(v)}</code>'
    if v.startswith("$") or re.match(r"^[\d,]+$", v.replace(",", "")):
        return f'<span class="num">{esc(v)}</span>'
    if "*" in v:
        v = v.replace(" *", "").strip()
        return f'{esc(v)}<span class="flag-dot" title="See footnote">*</span>'
    return esc(v)


def render_table(headers: list, rows: list, flagged_col: int = 1) -> str:
    ths = []
    for i, h in enumerate(headers):
        cls = "num" if i > 0 and h not in ("Company", "org", "Current v4.0 Segment", "Current Segment", "Default Decision", "Why It Is Flagged") else ""
        abbr = ""
        label = h
        for key in GLOSSARY:
            if key.lower() in h.lower() or h == key:
                abbr = f' title="{esc(GLOSSARY[key])}"'
                break
        if h == "T12M Orders":
            abbr = f' title="{esc(GLOSSARY["T12M"])}"'
            label = "T12M"
        ths.append(f'<th class="{cls}"{abbr}>{esc(label)}</th>')

    trs = []
    for row in rows:
        org = row[1] if len(row) > 1 else ""
        flagged = org in FLAG_ORGS
        cls = ' class="flagged"' if flagged else ""
        tds = []
        for i, cell in enumerate(row):
            tds.append(f"<td>{fmt_cell(cell, i, headers)}</td>")
        flag_badge = '<span class="review-badge">review</span>' if flagged else ""
        if flagged and tds:
            tds[0] = f"<td>{fmt_cell(row[0], 0, headers)}{flag_badge}</td>"
        trs.append(f"<tr{cls}>{''.join(tds)}</tr>")

    return f"""<div class="table-wrap"><table>
<thead><tr>{''.join(ths)}</tr></thead>
<tbody>{''.join(trs)}</tbody>
</table></div>"""


def render_list(items: list) -> str:
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def render_profile_card(seg_name: str, profile: dict, n: str, meta: dict) -> str:
    slug = meta["slug"]
    short = seg_name.split(". ", 1)[-1]
    return f"""
    <article class="profile-card" id="profile-{slug}" style="--seg-color:{meta['color']};--seg-bg:{meta['bg']};--seg-border:{meta['border']}">
      <div class="profile-header">
        <span class="seg-pill" style="background:{meta['bg']};color:{meta['color']};border-color:{meta['border']}">{esc(short)}</span>
        <h3>{esc(short)}</h3>
        <span class="profile-count">{esc(n)} accounts</span>
      </div>
      <p class="profile-defined"><strong>Defined by:</strong> {esc(profile.get('defined_by', ''))}</p>
      <div class="profile-grid">
        <div class="profile-block">
          <h4>What they sell</h4>
          <p>{esc(profile.get('what', ''))}</p>
        </div>
        <div class="profile-block">
          <h4>How they sell</h4>
          {render_list(profile.get('how', []))}
        </div>
        <div class="profile-block">
          <h4>Who buys</h4>
          {render_list(profile.get('who', []))}
        </div>
      </div>
      <div class="profile-truth">
        <strong>Key commercial truth</strong>
        <p>{esc(profile.get('truth', ''))}</p>
      </div>
      <a class="profile-jump" href="#seg-{slug}">View {esc(n)}-account roster →</a>
    </article>"""


def build_html(data: dict) -> str:
    total_orgs = sum(int(r[1]) for r in data["summary"])

    seg_cards = []
    for row in data["summary"]:
        name = row[0]
        n = row[1]
        price = row[2]
        meta = SEGMENTS.get(name, {})
        slug = meta.get("slug", "specialty")
        short = name.split(". ", 1)[-1] if ". " in name else name
        seg_cards.append(f"""
        <a href="#seg-{slug}" class="seg-card seg-{slug}">
          <div class="seg-card-num">{n}</div>
          <div class="seg-card-name">{esc(short)}</div>
          <div class="seg-card-price">median {esc(price)}</div>
        </a>""")

    summary_headers = SUMMARY_HEADERS
    summary_body = data["summary"]

    profile_cards = []
    for row in data["summary"]:
        seg_name = row[0]
        n = row[1]
        profile = data.get("profiles", {}).get(seg_name, {})
        if profile:
            profile_cards.append(render_profile_card(seg_name, profile, n, SEGMENTS[seg_name]))

    boundaries_table = ""
    if data.get("boundaries"):
        boundaries_table = render_table(["Boundary", "What separates them"], data["boundaries"])

    layers_table = ""
    if data.get("layers"):
        layers_table = render_table(["Layer", "Source", "What it tells us"], data["layers"])

    questions_html = "".join(
        f'<div class="q-card"><strong>{esc(q)}</strong><span>{esc(a)}</span></div>'
        for q, a in FRAMEWORK_QUESTIONS
    )

    roster_html = []
    for seg_name, info in data["rosters"].items():
        meta = SEGMENTS[seg_name]
        slug = meta["slug"]
        short = seg_name.split(". ", 1)[-1]
        n = len(info["rows"])
        headers = [
            "Company", "org", "Best Price", "Orders", "T12M Orders", "AOV",
            "PCodes", "Customers", "Territories", "Users", "DCs",
        ]
        table = render_table(headers, info["rows"])
        footnotes = ""
        if slug == "luxury":
            footnotes = """
            <div class="footnotes">
              <p><span class="flag-dot">*</span> <strong>sbl $14:</strong> Only 1 of 4,186 Schonbek products has catalog <code>net_price</code>. The $14 is an accessory, not brand pricing (chandeliers $1K–$100K+). Placement validated by AOV ($14,255).</p>
              <p><strong>Gabriella White:</strong> Removed — Postgres confirms org <code>sc</code> = Summer Classics, already in Premium Trade Brand.</p>
            </div>"""
        roster_html.append(f"""
        <details class="roster-block" id="seg-{slug}">
          <summary style="--seg-color:{meta['color']};--seg-bg:{meta['bg']};--seg-border:{meta['border']}">
            <div class="roster-summary-inner">
              <span class="seg-pill" style="background:{meta['bg']};color:{meta['color']};border-color:{meta['border']}">{esc(short)}</span>
              <span class="roster-title">{n} accounts</span>
              <span class="roster-desc">{esc(info['desc'])}</span>
              <span class="expand-label">View roster</span>
            </div>
          </summary>
          <div class="roster-body">
            {table}
            {footnotes}
          </div>
        </details>""")

    key_calls_html = "".join(
        f'<div class="call-pill"><strong>{esc(t)}</strong><span>{esc(b)}</span></div>'
        for t, b in KEY_CALLS
    )

    enrich_items = []
    for title, body in data["enrichment"]:
        seg_key = next((k for k in SEGMENTS if title in k), "5. Specialty/Non-Traditional")
        color = SEGMENTS[seg_key]["color"]
        enrich_items.append(
            f'<div class="enrich-item" style="--seg-color:{color}">'
            f'<div class="enrich-seg">{esc(title)}</div><p>{esc(body)}</p></div>'
        )

    review_headers = ["Company", "org", "Current v4.0 Segment", "Default Decision", "Why It Is Flagged"]
    review_table = render_table(review_headers, data["review"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SuperCat Client Segmentation v4.0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #FAFAF8; --surface: #FFF; --panel: #F5F4F1; --border: #E8E5DE; --border-light: #F0EDE6;
  --text: #2C2925; --text-2: #6B6660; --text-muted: #9B958C;
  --accent: #4A6FA5; --accent-deep: #2E4A6E; --accent-glow: rgba(74,111,165,.08); --accent-border: rgba(74,111,165,.22);
  --ok: #1F8A5C; --ok-bg: #EDF7F1;
  --warn: #B8863A; --warn-bg: #FDF8EC; --warn-border: rgba(184,134,58,.3);
  --fd: 'DM Sans', system-ui, sans-serif; --fm: 'IBM Plex Mono', ui-monospace, monospace; --r: 10px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font: 400 14px/1.65 var(--fd); color: var(--text); background: var(--bg); -webkit-font-smoothing: antialiased; }}
.page {{ max-width: 1040px; margin: 0 auto; padding: 0 28px 72px; }}

/* Header */
.hero {{ padding: 48px 0 36px; border-bottom: 1px solid var(--border); margin-bottom: 8px; position: relative; }}
.hero-top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }}
.eyebrow {{ font: 600 10px/1 var(--fm); letter-spacing: .14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }}
.hero h1 {{ font: 700 36px/1.08 var(--fd); letter-spacing: -.02em; color: var(--text); max-width: 720px; }}
.hero-sub {{ font-size: 16px; color: var(--text-2); margin-top: 8px; max-width: 640px; }}
.status-badge {{ font: 600 10px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; padding: 8px 14px; border-radius: 20px; background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(31,138,92,.25); white-space: nowrap; }}
.meta-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.meta-chip {{ font: 500 11px/1.4 var(--fm); padding: 6px 12px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 6px; color: var(--text-2); }}
.meta-chip strong {{ color: var(--text); font-weight: 600; }}
.hero-accent {{ position: absolute; bottom: -1px; left: 0; width: 72px; height: 2px; background: var(--accent); }}

/* TOC */
.toc {{ position: sticky; top: 0; z-index: 50; display: flex; gap: 6px; padding: 14px 0; margin-bottom: 28px; background: var(--bg); border-bottom: 1px solid var(--border); overflow-x: auto; }}
.toc a {{ padding: 6px 12px; font: 500 11px/1 var(--fd); color: var(--text-2); text-decoration: none; background: var(--panel); border: 1px solid var(--border-light); border-radius: 20px; white-space: nowrap; transition: .12s; }}
.toc a:hover, .toc a.active {{ color: var(--accent-deep); background: var(--accent-glow); border-color: var(--accent-border); }}

/* Sections */
.section {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 28px 32px; margin-bottom: 20px; }}
.section-head {{ margin-bottom: 20px; }}
.section-head h2 {{ font: 700 22px/1.2 var(--fd); letter-spacing: -.015em; margin-bottom: 6px; }}
.section-head p {{ font-size: 13px; color: var(--text-muted); max-width: 680px; }}

/* Executive */
.exec-lead {{ font-size: 15px; line-height: 1.6; color: var(--text-2); margin-bottom: 20px; max-width: 720px; }}
.exec-lead strong {{ color: var(--text); }}
.calls-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; }}
.call-pill {{ padding: 14px 16px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 8px; }}
.call-pill strong {{ display: block; font-size: 12px; font-weight: 600; color: var(--text); margin-bottom: 4px; }}
.call-pill span {{ font-size: 12px; color: var(--text-muted); line-height: 1.45; }}

/* Framework */
.framework-lead {{ font-size: 14px; color: var(--text-2); line-height: 1.6; margin-bottom: 18px; max-width: 720px; }}
.q-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 20px; }}
.q-card {{ padding: 14px 16px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 8px; }}
.q-card strong {{ display: block; font-size: 13px; color: var(--text); margin-bottom: 4px; }}
.q-card span {{ font-size: 12px; color: var(--text-muted); line-height: 1.45; }}
.subsection-label {{ font: 600 10px/1 var(--fm); letter-spacing: .1em; text-transform: uppercase; color: var(--text-muted); margin: 20px 0 10px; }}

/* Profile cards */
.profile-card {{ border: 1px solid var(--border); border-left: 4px solid var(--seg-color); border-radius: var(--r); padding: 24px 28px; margin-bottom: 16px; background: var(--surface); }}
.profile-header {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }}
.profile-header h3 {{ font: 700 20px/1.2 var(--fd); color: var(--text); }}
.profile-count {{ font: 500 11px/1 var(--fm); color: var(--text-muted); margin-left: auto; }}
.profile-defined {{ font-size: 13px; color: var(--text-2); line-height: 1.55; margin-bottom: 16px; padding: 12px 14px; background: var(--seg-bg, var(--panel)); border-radius: 6px; }}
.profile-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 14px; }}
@media (max-width: 800px) {{ .profile-grid {{ grid-template-columns: 1fr; }} }}
.profile-block h4 {{ font: 600 10px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; color: var(--seg-color); margin-bottom: 8px; }}
.profile-block p {{ font-size: 13px; color: var(--text-2); line-height: 1.5; }}
.profile-block ul {{ list-style: none; padding: 0; }}
.profile-block li {{ font-size: 13px; color: var(--text-2); line-height: 1.45; padding-left: 14px; position: relative; margin-bottom: 5px; }}
.profile-block li::before {{ content: '—'; position: absolute; left: 0; color: var(--text-muted); }}
.profile-truth {{ padding: 14px 16px; background: var(--panel); border-radius: 8px; border: 1px solid var(--border-light); margin-bottom: 12px; }}
.profile-truth strong {{ display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--text-muted); margin-bottom: 6px; }}
.profile-truth p {{ font-size: 13px; color: var(--text-2); line-height: 1.55; }}
.profile-jump {{ font-size: 12px; font-weight: 600; color: var(--accent); text-decoration: none; }}
.profile-jump:hover {{ color: var(--accent-deep); text-decoration: underline; }}

/* Segment cards */
.seg-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 4px; }}
@media (max-width: 900px) {{ .seg-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
@media (max-width: 560px) {{ .seg-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.seg-card {{ text-decoration: none; text-align: center; padding: 18px 12px; border-radius: var(--r); border: 1px solid var(--border); background: var(--surface); transition: transform .15s, box-shadow .15s; }}
.seg-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.06); }}
.seg-card-num {{ font: 700 32px/1 var(--fd); margin-bottom: 4px; }}
.seg-card-name {{ font: 600 11px/1.3 var(--fd); color: var(--text); margin-bottom: 6px; }}
.seg-card-price {{ font: 500 10px/1 var(--fm); color: var(--text-muted); }}
.seg-luxury {{ border-top: 3px solid #B8860B; }} .seg-luxury .seg-card-num {{ color: #B8860B; }}
.seg-premium {{ border-top: 3px solid #6B4FBB; }} .seg-premium .seg-card-num {{ color: #6B4FBB; }}
.seg-midmarket {{ border-top: 3px solid #1F8A5C; }} .seg-midmarket .seg-card-num {{ color: #1F8A5C; }}
.seg-volume {{ border-top: 3px solid #C44D4D; }} .seg-volume .seg-card-num {{ color: #C44D4D; }}
.seg-specialty {{ border-top: 3px solid #6B7280; }} .seg-specialty .seg-card-num {{ color: #6B7280; }}

/* Tables */
.table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; margin: 12px 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
thead {{ background: var(--panel); }}
th {{ text-align: left; padding: 10px 12px; font: 600 9.5px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; color: var(--text-muted); border-bottom: 1px solid var(--border); cursor: help; }}
th.num {{ text-align: right; }}
td .num {{ display: inline-block; width: 100%; text-align: right; }}
td {{ padding: 9px 12px; border-bottom: 1px solid var(--border-light); vertical-align: top; }}
tr:last-child td {{ border-bottom: none; }}
tbody tr:hover {{ background: var(--accent-glow); }}
tr.flagged {{ background: var(--warn-bg); }}
tr.flagged:hover {{ background: #FBF0D8; }}
.missing {{ color: var(--text-muted); }}
.org-tag {{ font: 500 10.5px/1 var(--fm); padding: 2px 6px; background: var(--panel); border: 1px solid var(--border); border-radius: 4px; color: var(--text-2); }}
.num {{ font: 500 12px/1 var(--fm); font-variant-numeric: tabular-nums; }}
.review-badge {{ display: inline-block; margin-left: 6px; font: 600 8px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; padding: 2px 5px; border-radius: 3px; background: var(--warn-bg); color: var(--warn); border: 1px solid var(--warn-border); vertical-align: middle; }}
.flag-dot {{ color: var(--warn); font-weight: 700; margin-left: 2px; }}

/* Glossary */
details.glossary > summary {{ display: flex; align-items: center; gap: 10px; padding: 16px 20px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--r); cursor: pointer; list-style: none; font-weight: 600; font-size: 14px; }}
details.glossary > summary::-webkit-details-marker {{ display: none; }}
details.glossary > summary::before {{ content: '▸'; color: var(--accent); transition: transform .15s; }}
details.glossary[open] > summary::before {{ transform: rotate(90deg); }}
details.glossary > summary .hint {{ margin-left: auto; font: 400 10px/1 var(--fm); color: var(--text-muted); text-transform: uppercase; letter-spacing: .06em; }}
.glossary-body {{ padding: 16px 4px 4px; margin-bottom: 20px; }}
.glossary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }}
.glossary-item {{ padding: 14px 16px; background: var(--surface); border: 1px solid var(--border-light); border-radius: 8px; }}
.glossary-item dt {{ font: 600 12px/1.3 var(--fd); margin-bottom: 6px; }}
.glossary-item dt code {{ font: 500 11px/1 var(--fm); color: var(--accent-deep); }}
.glossary-item dd {{ font-size: 12px; color: var(--text-2); line-height: 1.5; }}

/* Rosters */
.roster-block {{ margin-bottom: 12px; border: 1px solid var(--border); border-radius: var(--r); overflow: hidden; background: var(--surface); }}
.roster-block > summary {{ list-style: none; cursor: pointer; padding: 0; border-left: 4px solid var(--seg-color, var(--accent)); }}
.roster-block > summary::-webkit-details-marker {{ display: none; }}
.roster-summary-inner {{ padding: 18px 22px; display: grid; grid-template-columns: auto 1fr auto; grid-template-rows: auto auto; gap: 4px 14px; align-items: center; }}
.seg-pill {{ font: 600 10px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; padding: 5px 10px; border-radius: 5px; border: 1px solid; grid-row: span 2; }}
.roster-title {{ font: 700 16px/1.2 var(--fd); color: var(--text); }}
.roster-desc {{ grid-column: 2; font-size: 12.5px; color: var(--text-muted); line-height: 1.45; }}
.expand-label {{ grid-row: span 2; font: 600 9px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); opacity: .7; }}
.roster-block[open] .expand-label {{ display: none; }}
.roster-block > summary:hover {{ background: var(--seg-bg, var(--panel)); }}
.roster-body {{ padding: 0 16px 16px; border-top: 1px solid var(--border-light); }}
.footnotes {{ margin-top: 12px; padding: 12px 14px; background: var(--panel); border-radius: 6px; font-size: 12px; color: var(--text-2); line-height: 1.55; }}
.footnotes p + p {{ margin-top: 8px; }}
.footnotes code {{ font: 500 10.5px/1 var(--fm); }}

/* Enrichment */
.enrich-grid {{ display: grid; gap: 10px; }}
.enrich-item {{ padding: 14px 18px; border-left: 3px solid var(--seg-color, var(--accent)); background: var(--panel); border-radius: 0 8px 8px 0; }}
.enrich-seg {{ font: 600 11px/1 var(--fm); letter-spacing: .04em; text-transform: uppercase; color: var(--seg-color); margin-bottom: 6px; }}
.enrich-item p {{ font-size: 13px; color: var(--text-2); line-height: 1.5; }}

/* Review */
.review-banner {{ display: flex; gap: 14px; padding: 16px 18px; background: var(--warn-bg); border: 1px solid var(--warn-border); border-radius: 8px; margin-bottom: 16px; align-items: flex-start; }}
.review-banner-icon {{ font: 700 18px/1 var(--fd); color: var(--warn); }}
.review-banner p {{ font-size: 13px; color: var(--text-2); line-height: 1.5; }}

/* Next */
.next-step {{ text-align: center; padding: 32px; background: linear-gradient(135deg, var(--surface), var(--accent-glow)); border: 1px solid var(--accent-border); border-radius: var(--r); }}
.next-step h2 {{ font: 700 20px/1.2 var(--fd); margin-bottom: 8px; }}
.next-step p {{ font-size: 14px; color: var(--text-2); max-width: 520px; margin: 0 auto; }}

@media print {{
  .toc {{ display: none; }}
  .roster-block {{ break-inside: avoid; }}
  details {{ open: true; }}
}}
</style>
</head>
<body>
<div class="page">

<header class="hero">
  <div class="hero-top">
    <div>
      <div class="eyebrow">SuperCat Ops · Customer Segmentation</div>
      <h1>Client Segmentation v4.0</h1>
      <p class="hero-sub">By how they sell and to whom — not by how they use eCat</p>
    </div>
    <span class="status-badge">Ready for stamp</span>
  </div>
  <div class="meta-grid">
    <span class="meta-chip"><strong>Date</strong> July 7, 2026</span>
    <span class="meta-chip"><strong>Universe</strong> {total_orgs} active orgs</span>
    <span class="meta-chip"><strong>Baseline</strong> v3.2 (Kylor-stamped Jul 2)</span>
    <span class="meta-chip"><strong>Purpose</strong> Rep co-pilot buckets</span>
  </div>
  <div class="hero-accent"></div>
</header>

<nav class="toc" id="toc">
  <a href="#framework">Framework</a>
  <a href="#profiles">Profiles</a>
  <a href="#summary">Changes</a>
  <a href="#overview">Data</a>
  <a href="#glossary">Column key</a>
  <a href="#rosters">Rosters</a>
  <a href="#review">Review flags</a>
  <a href="#next">Next step</a>
</nav>

<section class="section" id="framework">
  <div class="section-head">
    <h2>How We Segment</h2>
    <p>Stamped v3 → v3.2 framework, preserved in v4. Price validates; selling motion classifies.</p>
  </div>
  <p class="framework-lead">This is <strong>not</strong> eCat usage segmentation. A company with 175,000 orders and a company with 2 orders can share a bucket if they sell the same way in the market.</p>
  <div class="q-grid">{questions_html}</div>
  <div class="subsection-label">Segment boundaries</div>
  {boundaries_table}
  <div class="subsection-label">Data layers (v3.2 baseline + v4 enrichment)</div>
  {layers_table}
  <p class="framework-lead" style="margin-top:14px;font-size:13px">v4 adds customers, territories, users, T12M orders, and DCs as <strong>scale context within</strong> a segment — not as reclassification logic.</p>
</section>

<section class="section" id="profiles">
  <div class="section-head">
    <h2>Segment Profiles</h2>
    <p>What they sell, how they sell, who buys — the co-pilot context Kjael asked for.</p>
  </div>
  {''.join(profile_cards)}
</section>

<section class="section" id="summary">
  <div class="section-head">
    <h2>v4.0 Changes</h2>
    <p>Refinement of stamped v3.2 — same membership, cleaner metrics, Postgres enrichment.</p>
  </div>
  <p class="exec-lead">Four primary <strong>selling-motion buckets</strong> plus a small Specialty exception. Segmentation reflects how firms sell in the market — not how they configure eCat. Enough structure to keep co-pilot recommendations from being tone-deaf, without overfitting to platform data.</p>
  <div class="calls-grid">{key_calls_html}</div>
</section>

<section class="section" id="overview">
  <div class="section-head">
    <h2>Segment Data at a Glance</h2>
    <p>Counts and median metrics — supporting evidence, not the classifier.</p>
  </div>
  <div class="seg-grid">{''.join(seg_cards)}</div>
  <div style="margin-top:24px">
    <div class="section-head" style="margin-bottom:12px"><h2 style="font-size:17px">Median Profile by Segment</h2></div>
    {render_table(summary_headers, summary_body)}
  </div>
</section>

<details class="glossary" id="glossary">
  <summary>Column Key <span class="hint">eCat &amp; data terms</span></summary>
  <div class="glossary-body">
    <div class="glossary-grid">
      {''.join(f'<dl class="glossary-item"><dt><code>{esc(k)}</code></dt><dd>{esc(v)}</dd></dl>' for k, v in GLOSSARY.items())}
    </div>
  </div>
</details>

<section class="section" id="rosters" style="padding:24px 28px">
  <div class="section-head">
    <h2>Segment Rosters</h2>
    <p>108 orgs across five buckets. Rows marked <span class="review-badge">review</span> are pre-stamp flags — not moves.</p>
  </div>
  {''.join(roster_html)}
</section>

<section class="section" id="enrichment">
  <div class="section-head">
    <h2>What the Enrichment Adds</h2>
    <p>Operational scale signals within each segment — context for co-pilot tone, not reclassification logic.</p>
  </div>
  <div class="enrich-grid">{''.join(enrich_items)}</div>
</section>

<section class="section" id="review">
  <div class="section-head">
    <h2>Pre-Stamp Review Candidates</h2>
  </div>
  <div class="review-banner">
    <span class="review-banner-icon">⚑</span>
    <p><strong>8 accounts flagged for judgment call.</strong> Corrected v4.0 does not move them — they stay in their v3.2 segment unless you decide otherwise based on real-world selling motion, not eCat configuration.</p>
  </div>
  {review_table}
</section>

<section class="next-step" id="next">
  <h2>Next Step</h2>
  <p>Stamp this segmentation, then build <strong>personas within each segment</strong> for rep co-pilot initialization.</p>
</section>

</div>
<script>
(function() {{
  const toc = document.getElementById('toc');
  const links = [...toc.querySelectorAll('a')];
  const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const obs = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
      }}
    }});
  }}, {{ rootMargin: '-20% 0 -70% 0' }});
  sections.forEach(s => obs.observe(s));
}})();
</script>
</body>
</html>"""


def main():
    text = MD.read_text(encoding="utf-8")
    data = parse_md(text)
    OUT.write_text(build_html(data), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
